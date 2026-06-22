"""
VMware 日语 DLL → 中文 DLL 逆向重建工具

将 D:\vmware\messages\ja\ 下的 vmui-ja.dll / vmappsdk-ja.dll 的语言 ID
从 0x411 (日语) 改为 0x804 (简体中文)，生成到 D:\vmware\messages\zh\。

策略：
  1. 只操作 .rsrc 节（资源节）
  2. 资源目录第3层（语言层）的 ID 从 0x411 → 0x804
  3. VERSIONINFO 资源内部的 StringFileInfo 语言 ID 同步更新
  4. 其他二进制资源数据不变（图片/图标/布局等）
"""

import os
import struct
import shutil

# ── 路径 ──────────────────────────────────────────────
JA_DIR = r"D:\vmware\messages\ja"
ZH_DIR = r"D:\vmware\messages\zh"
DLLS = ["vmui-ja.dll", "vmappsdk-ja.dll"]
LANG_JA = 0x411   # 日语
LANG_CN = 0x804   # 简体中文

# ── PE 常量 ───────────────────────────────────────────
IMAGE_DOS_SIGNATURE = 0x5A4D        # MZ
IMAGE_NT_SIGNATURE  = 0x00004550    # PE\0\0

# 资源类型 ID
RT_CURSOR       = 1
RT_BITMAP       = 2
RT_ICON         = 3
RT_MENU         = 4
RT_DIALOG       = 5
RT_STRING       = 6
RT_FONTDIR      = 7
RT_FONT         = 8
RT_ACCELERATOR  = 9
RT_RCDATA       = 10
RT_MESSAGETABLE = 11
RT_GROUP_CURSOR = 12
RT_GROUP_ICON   = 14
RT_VERSION      = 16
RT_DLGINCLUDE   = 17
RT_PLUGPLAY     = 19
RT_VXD          = 20
RT_ANICURSOR    = 21
RT_ANIICON      = 22
RT_HTML         = 23
RT_MANIFEST     = 24

# ── PE 解析 ───────────────────────────────────────────

class PE:
    """最小化 PE 解析器：只关心节表和 .rsrc"""
    def __init__(self, data):
        self.data = data
        self.dos_header = data[:64]
        assert struct.unpack('<H', data[:2])[0] == IMAGE_DOS_SIGNATURE, "Not a PE file"

        e_lfanew = struct.unpack('<I', data[60:64])[0]
        assert struct.unpack('<I', data[e_lfanew:e_lfanew+4])[0] == IMAGE_NT_SIGNATURE

        self.nt_offset = e_lfanew
        self.file_header = data[e_lfanew+4:e_lfanew+24]
        self.optional_header = self._read_optional_header()

        # 节表
        self.sections = []
        self._parse_sections()

    def _read_optional_header(self):
        """读取可选头部以获取 SizeOfOptionalHeader"""
        magic = struct.unpack('<H', self.data[self.nt_offset+24:self.nt_offset+26])[0]
        if magic == 0x10b:  # PE32
            return self.data[self.nt_offset+24:self.nt_offset+24+224]
        elif magic == 0x20b:  # PE32+
            return self.data[self.nt_offset+24:self.nt_offset+24+240]
        else:
            raise ValueError(f"Unknown PE magic: 0x{magic:04x}")

    @property
    def size_of_optional_header(self):
        return struct.unpack('<H', self.data[self.nt_offset+20:self.nt_offset+22])[0]

    def _parse_sections(self):
        sec_offset = self.nt_offset + 24 + self.size_of_optional_header
        num_sections = struct.unpack('<H', self.data[self.nt_offset+6:self.nt_offset+8])[0]
        for i in range(num_sections):
            raw = self.data[sec_offset + i*40 : sec_offset + (i+1)*40]
            name = raw[:8].rstrip(b'\x00').decode('ascii', errors='replace')
            (virt_size, virt_addr, raw_size, raw_offset,
             reloc_ptr, linenum_ptr, num_relocs, num_linenums,
             characteristics) = struct.unpack('<IIIIIIIIII', raw[8:48])
            self.sections.append({
                'name': name,
                'virt_size': virt_size,
                'virt_addr': virt_addr,
                'raw_size': raw_size,
                'raw_offset': raw_offset,
                'characteristics': characteristics,
            })

    def rva_to_offset(self, rva):
        """将 RVA 转换为文件偏移"""
        for sec in self.sections:
            sec_end = sec['virt_addr'] + sec['virt_size']
            if sec['virt_addr'] <= rva < sec_end:
                return rva - sec['virt_addr'] + sec['raw_offset']
        return None

    def get_section(self, name):
        for sec in self.sections:
            if sec['name'] == name:
                return sec
        return None

    def rebuild(self):
        """重建 PE 数据（替换 .rsrc 后）"""
        return self.data


# ── 资源目录解析 ──────────────────────────────────────

class ResourceEntry:
    """单个资源目录条目"""
    def __init__(self, name_id, is_dir, offset):
        self.name_id = name_id      # int ID 或 str name
        self.is_dir = is_dir        # True=子目录, False=DataEntry
        self.offset = offset        # 目录偏移 或 DataEntry 偏移
        self.children = []          # 子节点（仅目录）
        self.data_entry = None      # (rva, size, codepage) 仅叶子节点

    def __repr__(self):
        typ = "DIR" if self.is_dir else "LEAF"
        return f"[{typ} id=0x{self.name_id:x if isinstance(self.name_id,int) else self.name_id}]"


class ResourceTree:
    """递归资源树"""
    def __init__(self, data, base_offset):
        self.data = data
        self.base_offset = base_offset  # .rsrc raw_offset
        self.root = None
        self.flattened = []  # [(depth, entry, parent), ...]

    def parse(self):
        self.root = self._parse_dir(0, self.base_offset)
        return self

    def _parse_dir(self, depth, dir_offset):
        """递归解析资源目录"""
        dir_data = self.data[dir_offset:dir_offset+16]
        (characteristics, ts, ver_major, ver_minor,
         named_entries, id_entries) = struct.unpack('<IIHHHH', dir_data)

        entry = ResourceEntry(None, True, dir_offset)
        total_entries = named_entries + id_entries

        for i in range(total_entries):
            ent_data = self.data[dir_offset + 16 + i*8 : dir_offset + 24 + i*8]
            name_id, offset_to = struct.unpack('<II', ent_data)

            # 判断是 name(ID高位=1) 还是 id
            is_string_name = (name_id >> 31) & 1
            if is_string_name:
                str_offset = name_id & 0x7FFFFFFF
                s = self._read_string(str_offset)
                child = ResourceEntry(s, False, 0)  # will update below
            else:
                child = ResourceEntry(name_id, False, 0)

            # 判断是子目录还是 DataEntry
            is_subdir = (offset_to >> 31) & 1
            child.is_dir = is_subdir
            real_offset = offset_to & 0x7FFFFFFF

            if is_subdir:
                child.offset = self.base_offset + real_offset
                child.children = self._parse_dir(depth + 1, self.base_offset + real_offset).children
            else:
                child.offset = self.base_offset + real_offset
                de = self.data[self.base_offset + real_offset : self.base_offset + real_offset + 16]
                (rva, size, cp, reserved) = struct.unpack('<IIII', de)
                child.data_entry = (rva, size, cp)

            entry.children.append(child)
            self.flattened.append((depth, child, entry))

        return entry

    def _read_string(self, offset):
        """读取 Unicode 字符串（资源 name）"""
        raw = self.data[offset:]
        length = struct.unpack('<H', raw[:2])[0]
        chars = struct.unpack(f'<{length}H', raw[2:2+length*2])
        return ''.join(chr(c) for c in chars)


# ── 核心：直接修改 .rsrc 二进制中的语言 ID ──

def patch_rsrc_language_ids(pe, old_lang=0x411, new_lang=0x804):
    """
    直接在 .rsrc 二进制数据中遍历资源目录，
    在 depth=2 的条目中，将 ID = old_lang 改为 new_lang。
    同时更新 VERSIONINFO 资源内部的 StringFileInfo 语言代码。
    
    返回: (dir_changes, version_changes)
    """
    rsrc_sec = pe.get_section('.rsrc')
    if not rsrc_sec:
        print("  ❌ 未找到 .rsrc 节")
        return 0, 0

    rsrc_data = bytearray(pe.data[rsrc_sec['raw_offset']:rsrc_sec['raw_offset']+rsrc_sec['raw_size']])
    dir_changes = 0
    version_changes = 0

    def parse_dir_at(dir_offset, depth):
        nonlocal dir_changes
        if dir_offset + 16 > len(rsrc_data):
            return
        (_, _, _, _, named_entries, id_entries) = struct.unpack('<IIHHHH',
            rsrc_data[dir_offset:dir_offset+16])
        total = named_entries + id_entries

        for i in range(total):
            ent_off = dir_offset + 16 + i * 8
            if ent_off + 8 > len(rsrc_data):
                continue
            name_id, offset_to = struct.unpack('<II', rsrc_data[ent_off:ent_off+8])
            is_subdir = (offset_to >> 31) & 1
            real_off = offset_to & 0x7FFFFFFF

            if is_subdir:
                parse_dir_at(real_off, depth + 1)
            elif depth == 2 and isinstance(name_id, int):
                if name_id == old_lang:
                    struct.pack_into('<I', rsrc_data, ent_off, new_lang)
                    dir_changes += 1
                elif name_id != new_lang:
                    pass  # 其他语言 ID 不动

    # ── 解析顶层 Type 目录 ──
    parse_dir_at(0, 0)

    # ── 处理 VERSIONINFO 资源内容 ──
    def find_and_patch_version(dir_offset, depth=0):
        if dir_offset + 16 > len(rsrc_data):
            return
        (_, _, _, _, named_entries, id_entries) = struct.unpack('<IIHHHH',
            rsrc_data[dir_offset:dir_offset+16])
        total = named_entries + id_entries

        for i in range(total):
            ent_off = dir_offset + 16 + i * 8
            if ent_off + 8 > len(rsrc_data):
                continue
            name_id, offset_to = struct.unpack('<II', rsrc_data[ent_off:ent_off+8])
            is_subdir = (offset_to >> 31) & 1
            real_off = offset_to & 0x7FFFFFFF

            if is_subdir:
                if depth == 0 and isinstance(name_id, int) and name_id == RT_VERSION:
                    _patch_version_resources(rsrc_data, real_off, pe)
                else:
                    find_and_patch_version(real_off, depth + 1)

    def _patch_version_resources(rsrc_data, dir_off, pe):
        """更新 VERSIONINFO 资源内部的 StringFileInfo 语言代码"""
        nonlocal version_changes
        (_, _, _, _, named_entries, id_entries) = struct.unpack('<IIHHHH',
            rsrc_data[dir_off:dir_off+16])
        total = named_entries + id_entries

        for i in range(total):
            ent_off = dir_off + 16 + i * 8
            name_id, offset_to = struct.unpack('<II', rsrc_data[ent_off:ent_off+8])
            is_subdir = (offset_to >> 31) & 1
            real_off = offset_to & 0x7FFFFFFF

            if is_subdir:
                # depth=2 (Language 层) - 找到 DataEntry
                (_, _, _, _, n2, i2) = struct.unpack('<IIHHHH',
                    rsrc_data[real_off:real_off+16])
                for j in range(n2 + i2):
                    eo = real_off + 16 + j * 8
                    nid, oto = struct.unpack('<II', rsrc_data[eo:eo+8])
                    is_sd = (oto >> 31) & 1
                    real_oto = oto & 0x7FFFFFFF
                    if not is_sd:
                        de_data = rsrc_data[real_oto:real_oto+16]
                        rva, size, cp, _ = struct.unpack('<IIII', de_data)
                        file_off = pe.rva_to_offset(rva)
                        if file_off is None:
                            continue
                        raw_ver = bytearray(pe.data[file_off:file_off+size])
                        patches = _patch_version_lang(raw_ver, old_lang, new_lang)
                        if patches > 0:
                            pe.data[file_off:file_off+size] = bytes(raw_ver)
                            version_changes += patches

    find_and_patch_version(0, 0)

    # 将修改后的 .rsrc 写回 PE 数据
    pe.data[rsrc_sec['raw_offset']:rsrc_sec['raw_offset']+len(rsrc_data)] = bytes(rsrc_data)
    return dir_changes, version_changes


def _patch_version_lang(data, old_lang=0x411, new_lang=0x804):
    """
    在 VERSIONINFO 资源的 StringFileInfo 块中，
    将语言/代码页标识从 old_lang 改为 new_lang。
    
    lang-codepage 是 8 字符十六进制字符串，前4位 = 语言ID
    """
    old_hex = f'{old_lang:04x}'.encode('utf-16-le')
    new_hex = f'{new_lang:04x}'.encode('utf-16-le')
    changes = 0
    pos = 0
    while True:
        pos = data.find(old_hex, pos)
        if pos < 0:
            break
        data[pos:pos+len(old_hex)] = new_hex
        changes += 1
        pos += len(new_hex)
    return changes


# ── 分析 ──────────────────────────────────────────────

def analyze_dll(filepath):
    """分析 DLL 并打印概览"""
    print(f"\n{'='*60}")
    print(f"分析: {os.path.basename(filepath)}")
    print(f"{'='*60}")

    with open(filepath, 'rb') as f:
        pe = PE(f.read())

    print(f"  节表:")
    for sec in pe.sections:
        print(f"    {sec['name']:>8s}  VA=0x{sec['virt_addr']:08x}  "
              f"VSize=0x{sec['virt_size']:x}  "
              f"ROff=0x{sec['raw_offset']:x}  "
              f"RSize=0x{sec['raw_size']:x}")

    rsrc = pe.get_section('.rsrc')
    if rsrc:
        rsrc_data = pe.data[rsrc['raw_offset']:rsrc['raw_offset']+rsrc['raw_size']]
        print(f"\n  .rsrc 大小: {len(rsrc_data)} bytes ({len(rsrc_data)/1024:.1f} KB)")

        tree = ResourceTree(rsrc_data, 0).parse()
        dir_counts = {}
        for depth, entry, _ in tree.flattened:
            if not entry.is_dir:
                dir_counts[depth] = dir_counts.get(depth, 0) + 1
        for d in sorted(dir_counts):
            print(f"    depth={d}: {dir_counts[d]} 叶子条目")

        lang_ids = {}
        for depth, entry, _ in tree.flattened:
            if depth == 2 and isinstance(entry.name_id, int):
                lid = entry.name_id
                lang_ids[lid] = lang_ids.get(lid, 0) + 1
        print(f"  语言 ID 分布:")
        for lid in sorted(lang_ids):
            print(f"    0x{lid:04x}: {lang_ids[lid]} 条目")


# ── 重建 ──────────────────────────────────────────────

def rework_dll(src_path, dst_path, old_lang=0x411, new_lang=0x804):
    """
    逆向重建单个 DLL：
    1. 解析 PE
    2. 修改 .rsrc 中的语言 ID
    3. 更新 VERSIONINFO 中的语言代码
    4. 写出新 DLL
    """
    print(f"\n{'='*60}")
    print(f"处理: {os.path.basename(src_path)}")
    print(f"  → {dst_path}")
    print(f"{'='*60}")

    with open(src_path, 'rb') as f:
        pe = PE(f.read())

    rsrc = pe.get_section('.rsrc')
    if not rsrc:
        print("  ❌ 无可用的 .rsrc 节")
        return False

    print(f"  .rsrc 偏移: 0x{rsrc['raw_offset']:x}, 大小: {rsrc['raw_size']}")

    dir_changes, ver_changes = patch_rsrc_language_ids(pe, old_lang, new_lang)
    print(f"  资源目录语言修改: {dir_changes} 处")
    print(f"  VERSIONINFO 语言修改: {ver_changes} 处")

    if dir_changes == 0 and ver_changes == 0:
        print("  ⚠ 没有需要修改的条目")
        return False

    # 清零校验和
    magic = struct.unpack('<H', pe.data[pe.nt_offset+24:pe.nt_offset+26])[0]
    if magic == 0x10b:  # PE32
        checksum_off = pe.nt_offset + 24 + 0x58
    else:  # PE32+
        checksum_off = pe.nt_offset + 24 + 0x40
    struct.pack_into('<I', pe.data, checksum_off, 0)
    print("  校验和已清零")

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, 'wb') as f:
        f.write(bytes(pe.data))

    size = os.path.getsize(dst_path)
    print(f"  ✅ 已写出: {dst_path} ({size:,} bytes)")
    return True


# ── 验证 ──────────────────────────────────────────────

def verify_dll(filepath, expected_lang=0x804):
    """验证 DLL 的语言 ID 是否已改为目标值"""
    print(f"\n验证: {os.path.basename(filepath)}")
    with open(filepath, 'rb') as f:
        pe = PE(f.read())

    rsrc = pe.get_section('.rsrc')
    if not rsrc:
        print("  ❌ 无 .rsrc 节")
        return False

    rsrc_data = pe.data[rsrc['raw_offset']:rsrc['raw_offset']+rsrc['raw_size']]
    tree = ResourceTree(rsrc_data, 0).parse()

    lang_ids = {}
    for depth, entry, _ in tree.flattened:
        if depth == 2 and isinstance(entry.name_id, int):
            lang_ids[entry.name_id] = lang_ids.get(entry.name_id, 0) + 1

    print(f"  语言 ID 分布:")
    old_count = 0
    new_count = 0
    for lid in sorted(lang_ids):
        c = lang_ids[lid]
        if lid == LANG_JA:
            old_count = c
            print(f"    0x{lid:04x} (日语)  : {c} 条目 ⚠ 残留!")
        elif lid == LANG_CN:
            new_count = c
            print(f"    0x{lid:04x} (中文)  : {c} 条目 ✅")
        else:
            print(f"    0x{lid:04x} (其他)  : {c} 条目")

    if old_count == 0 and new_count > 0:
        print(f"  ✅ 验证通过! 全部 {new_count} 个语言条目已改为 0x{expected_lang:04x}")
        return True
    elif old_count > 0:
        print(f"  ⚠ 仍有 {old_count} 个日语条目残留")
        return False
    else:
        print(f"  ⚠ 未找到目标语言条目")
        return False


# ── 入口 ──────────────────────────────────────────────

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--analyze':
        for dll in DLLS:
            path = os.path.join(JA_DIR, dll)
            if os.path.exists(path):
                analyze_dll(path)
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == '--verify':
        for dll in DLLS:
            out_name = dll.replace('-ja.dll', '-zh.dll')
            path = os.path.join(ZH_DIR, out_name)
            if os.path.exists(path):
                verify_dll(path)
        sys.exit(0)

    print("=" * 60)
    print("VMware 日语 DLL → 中文 DLL 逆向重建")
    print("=" * 60)
    print(f"源目录: {JA_DIR}")
    print(f"目标目录: {ZH_DIR}")
    print(f"语言: 0x{LANG_JA:04x} (日语) → 0x{LANG_CN:04x} (简体中文)")

    # Step 1: 分析
    print(f"\n{'#'*60}")
    print("# 步骤 1: 分析源 DLL")
    print(f"{'#'*60}")
    for dll in DLLS:
        path = os.path.join(JA_DIR, dll)
        if os.path.exists(path):
            analyze_dll(path)

    # Step 2: 重建
    print(f"\n{'#'*60}")
    print("# 步骤 2: 重建 DLL")
    print(f"{'#'*60}")
    success = 0
    for dll in DLLS:
        src = os.path.join(JA_DIR, dll)
        out_name = dll.replace('-ja.dll', '-zh.dll')
        dst = os.path.join(ZH_DIR, out_name)
        if os.path.exists(src):
            if rework_dll(src, dst):
                success += 1

    # Step 3: 验证
    print(f"\n{'#'*60}")
    print("# 步骤 3: 验证结果")
    print(f"{'#'*60}")
    verified = 0
    for dll in DLLS:
        out_name = dll.replace('-ja.dll', '-zh.dll')
        path = os.path.join(ZH_DIR, out_name)
        if os.path.exists(path):
            if verify_dll(path):
                verified += 1

    print(f"\n{'='*60}")
    print(f"总结: 成功重建 {success}/{len(DLLS)}，验证通过 {verified}/{len(DLLS)}")
    print(f"{'='*60}")
    if success == len(DLLS) and verified == len(DLLS):
        print("✅ 全部完成! DLL 已放入 D:\\vmware\\messages\\zh\\")
