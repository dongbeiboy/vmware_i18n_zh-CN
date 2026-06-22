"""快速分析 DLL 资源结构"""
import struct, os

def analyze(path, label):
    print(f"\n{'='*60}")
    print(f"分析: {os.path.basename(path)} ({label})")
    print(f"{'='*60}")
    
    with open(path, 'rb') as f:
        data = f.read()
    
    # PE
    e_lfanew = struct.unpack('<I', data[60:64])[0]
    num_sections = struct.unpack('<H', data[e_lfanew+6:e_lfanew+8])[0]
    size_oh = struct.unpack('<H', data[e_lfanew+20:e_lfanew+22])[0]
    sec_off = e_lfanew + 24 + size_oh

    print(f"  节表:")
    for i in range(num_sections):
        raw = data[sec_off + i*40 : sec_off + (i+1)*40]
        name = raw[:8].rstrip(b'\x00').decode('ascii', errors='replace')
        vs, va, rs, ro = struct.unpack('<IIII', raw[8:24])
        print(f"    {name:>8s}  VA=0x{va:08x}  VSize={vs:>8,}  ROff=0x{ro:08x}  RSize={rs:>8,}")
        if name == '.rsrc':
            rsrc_off, rsrc_sz, rsrc_va = ro, rs, va

    # 资源树
    rsrc_data = data[rsrc_off:rsrc_off+rsrc_sz]
    
    RT_TYPES = {
        1:'CURSOR',2:'BITMAP',3:'ICON',4:'MENU',5:'DIALOG',
        6:'STRING TABLE',7:'FONTDIR',8:'FONT',9:'ACCELERATOR',10:'RCDATA',
        11:'MESSAGETABLE',12:'GRP_CURSOR',14:'GRP_ICON',16:'VERSION',
        17:'DLGINCLUDE',19:'PLUGPLAY',20:'VXD',21:'ANICURSOR',22:'ANIICON',
        23:'HTML',24:'MANIFEST'
    }

    def count_entries(dir_off, depth):
        """返回资源类型ID及其叶子数量"""
        _, _, _, _, ne, ie = struct.unpack('<IIHHHH', rsrc_data[dir_off:dir_off+16])
        results = []
        for i in range(ne + ie):
            ent_off = dir_off + 16 + i*8
            name_id, offset_to = struct.unpack('<II', rsrc_data[ent_off:ent_off+8])
            is_subdir = (offset_to >> 31) & 1
            real_off = offset_to & 0x7FFFFFFF
            name_val = name_id & 0x7FFFFFFF
            if not is_str_name(name_id):
                name_val = name_id
            if is_subdir:
                results.extend(count_entries(real_off, depth + 1))
            else:
                # 收集RVA和大小
                de = rsrc_data[real_off:real_off+16]
                rva, size, cp, _ = struct.unpack('<IIII', de)
                results.append((name_val, rva, size, cp))
        return results

    def is_str_name(n):
        return (n >> 31) & 1

    # 读取顶层类型目录
    _, _, _, _, ne, ie = struct.unpack('<IIHHHH', rsrc_data[0:16])
    print(f"\n  资源类型分布:")
    total_items = 0
    for i in range(ne + ie):
        ent_off = 16 + i*8
        name_id, offset_to = struct.unpack('<II', rsrc_data[ent_off:ent_off+8])
        type_id = name_id & 0x7FFFFFFF
        subdir_off = offset_to & 0x7FFFFFFF
        entries = count_entries(subdir_off, 1)
        count = len(entries)
        total_size = sum(e[2] for e in entries)
        type_name = RT_TYPES.get(type_id, f'UNK({type_id})')
        print(f"    {type_name:15s} (0x{type_id:03x}): {count:5d} items, {total_size:>10,} bytes")
        total_items += count

    print(f"    {'─'*50}")
    print(f"    {'TOTAL':15s}           {total_items:5d} items")
    
    # 提取 DIALOG 和 MENU 的文本内容
    # 解析顶层目录
    _, _, _, _, ne, ie = struct.unpack('<IIHHHH', rsrc_data[0:16])
    type_map = {}
    for i in range(ne + ie):
        ent_off = 16 + i*8
        name_id, offset_to = struct.unpack('<II', rsrc_data[ent_off:ent_off+8])
        type_id = name_id & 0x7FFFFFFF
        type_map[type_id] = offset_to & 0x7FFFFFFF
    
    # 提取 DIALOG/MENU 中文本
    for tid in [4, 5]:
        type_name = RT_TYPES.get(tid, f'UNK({tid})')
        if tid not in type_map:
            continue
        id_dir_off = type_map[tid]
        # depth=1: 资源 ID
        _, _, _, _, n1, i1 = struct.unpack('<IIHHHH', rsrc_data[id_dir_off:id_dir_off+16])
        for j in range(n1 + i1):
            eo = id_dir_off + 16 + j*8
            nid, oto = struct.unpack('<II', rsrc_data[eo:eo+8])
            is_sd = (oto >> 31) & 1
            real_oto = oto & 0x7FFFFFFF
            res_id = nid & 0x7FFFFFFF
            if not is_sd:
                continue
            # depth=2: lang
            _, _, _, _, n2, i2 = struct.unpack('<IIHHHH', rsrc_data[real_oto:real_oto+16])
            for k in range(n2 + i2):
                eo2 = real_oto + 16 + k*8
                nid2, oto2 = struct.unpack('<II', rsrc_data[eo2:eo2+8])
                is_sd2 = (oto2 >> 31) & 1
                if is_sd2:
                    continue
                de_off = oto2 & 0x7FFFFFFF
                de = rsrc_data[de_off:de_off+16]
                rva, size, cp, _ = struct.unpack('<IIII', de)
                # 获取实际资源数据
                file_off = rva - rsrc_va + rsrc_off
                raw = data[file_off:file_off+size]
                # 提取其中可打印字符串
                strings = set()
                for b in range(len(raw)):
                    if raw[b] >= 0x20 and raw[b] < 0x7f:
                        end = b
                        while end < len(raw) and raw[end] >= 0x20 and raw[end] < 0x7f:
                            end += 1
                        s = raw[b:end].decode('ascii')
                        if len(s) >= 3:
                            strings.add(s)
                        b = end
                # 提取 UTF-16 字符串
                strings16 = set()
                off = 0
                while off < len(raw) - 1:
                    cu = struct.unpack('<H', raw[off:off+2])[0]
                    if 0x3040 <= cu <= 0x309F or 0x30A0 <= cu <= 0x30FF or \
                       0x4E00 <= cu <= 0x9FFF or 0x080 <= cu <= 0x8FFF or \
                       0x3400 <= cu <= 0x4DBF or (cu >= 0x20 and cu < 0x7F and raw[off+1] == 0):
                        # Found Japanese/CJK start
                        end_off = off
                        while end_off < len(raw) - 1:
                            c = struct.unpack('<H', raw[end_off:end_off+2])[0]
                            if c == 0:
                                break
                            end_off += 2
                        s = raw[off:end_off].decode('utf-16-le', errors='replace')
                        # Filter to show only Japanese-containing strings
                        has_ja = any(0x3040 <= ord(ch) <= 0x309F or 0x30A0 <= ord(ch) <= 0x30FF or 0x4E00 <= ord(ch) <= 0x9FFF for ch in s)
                        has_long_en = len(s) >= 8 and all(ord(ch) < 0x80 for ch in s)
                        if has_ja:
                            strings16.add(s)
                        off = end_off + 2
                    else:
                        off += 2
                
                if strings16:
                    print(f"\n    {type_name} ID={res_id} (日语文本):")
                    for s in sorted(strings16, key=len, reverse=True)[:15]:
                        print(f"      \"{s[:80]}\"")
                if strings and type_name == 'MENU':
                    print(f"\n    MENU ID={res_id} (ASCII文本):")
                    for s in sorted(strings, key=len, reverse=True)[:10]:
                        print(f"      \"{s}\"")
    

# 分析两个 DLL
analyze(r'D:\vmware\messages\ja\vmui-ja.dll', '日语')
analyze(r'D:\vmware\messages\es\vmui-es.dll', '西班牙语(参考)')
analyze(r'D:\vmware\messages\ja\vmappsdk-ja.dll', '日语')
analyze(r'D:\vmware\messages\es\vmappsdk-es.dll', '西班牙语(参考)')
