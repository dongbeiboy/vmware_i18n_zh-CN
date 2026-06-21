#!/usr/bin/env python3
"""
vm.vmsg 逐条对照精准翻译 V3
"""
import re, os, shutil
from collections import OrderedDict

EN_FILE = r"d:\vmware\i18n\OVFTool\env\en\vm.vmsg"
ZH_FILE = r"d:\vmware\i18n\OVFTool\env\zh-CN\vm.vmsg"
OUTPUT_FILE = r"d:\vmware\i18n\OVFTool\env\zh-CN\vm.vmsg"
BACKUP_DIR = r"d:\vmware\i18n\.backup"
BACKUP_FILE = os.path.join(BACKUP_DIR, "vm_vmsg_zh_backup.vmsg")
ENTRY_RE = re.compile(r'^(?P<key>\S+)\s*=\s*"(?P<value>.*)"\s*$')
PH_PATTERN = re.compile(r'(\{[^}]*\})|(%[0-9$_.Iudl|a-zA-Z]+)')

def protect(text):
    tokens = []
    def repl(m):
        t = '\x00PH%d\x00' % len(tokens)
        tokens.append((t, m.group(0)))
        return t
    return PH_PATTERN.sub(repl, text), tokens

def restore(text, tokens):
    for t, orig in tokens:
        text = text.replace(t, orig)
    return text

def has_en(text):
    clean = PH_PATTERN.sub('', text)
    words = re.findall(r'\b[a-zA-Z]{2,}\b', clean)
    cjk_stuck = re.findall(r'[\u4e00-\u9fff]([a-zA-Z]{2,})', clean)
    all_words = words + cjk_stuck
    known = {'ID','VM','IP','OS','PC','WD','CE','BI',
             'KB','MB','GB','ROM','PCI','SCSI','SATA','AHCI','NVMe','NVM',
             'USB','MAC','xHCI','CPU','VMCI','VMI','TPM','QAT','WDT','NTP',
             'PTP','NVDIMM','GRID','vGPU','OUI','LUN','RDM','VMDK','ESX',
             'ESXi','GSX','PS2','DVD','ATAPI','CD','ISO','DVSwitch','SIO',
             'IDE','SAS','LSI','SR','IOV','RoCEv1','RoCEv2','FLP','Logitech',
             'Mouseman','Intellimouse','Explorer','Microsoft','Serial','Mouse',
             'Systems','BusLogic','ThinPrint','Append','Redolog','Snapshot',
             'SectorFormat','Persistent','Nonpersistent','Virtual','Physical',
             'Autodetect','Assigned','Generated','Manual','Host','Client',
             'Server','Native','Project','Publish','Device','DirectPath',
             'NVME','Paravirtual','Partition','Mapping','Flat','Sparse',
             'SeSparse','Independent','Undoable','Passthrough','NVIDIA',
             'FilterSpec','Queuepair','Datagram','Doorbell','Stream',
             'Hypervisor','Dynamic','Plugin','Vmiop','Dvx','Vendor',
             'Watchdog','NVDIMM','Unit','ATAPI','BusLogic',
             'Opaque','Sriov','Ethernet','Vrdma','VFlash','Cache',
             'ThinPrint','VMI','VMCI','vSocket','Sockets','SVGA',
             'RoCEv1','RoCEv2','NTP','PTP','SAS','GSX','SR','IOV',
             'SE','SPARSE','NVME','AHCI','SIO','IDE','RDM','VMDK'}
    unknown = [w for w in all_words if w not in known]
    return len(unknown) > 0

# 句式模板
SENTENCE_TEMPLATES = []
def register(pattern, translator):
    SENTENCE_TEMPLATES.append((re.compile(pattern), translator))

# --- 设备后端描述 ---
register(r'^Host device (?P<g0>\{[^}]+\}) backs a device in a virtual machine$',
    lambda g: f'主机设备 {g["g0"]} 作为虚拟机中设备的后端')
register(r'^File (?P<g0>\{[^}]+\}) backing for a device in a virtual machine$',
    lambda g: f'文件 {g["g0"]} 作为虚拟机中设备的后端')
register(r'^Pipe (?P<g0>\{[^}]+\}) backing of a device in a virtual machine$',
    lambda g: f'管道 {g["g0"]} 作为虚拟机中设备的后端')
register(r'^Remote device (?P<g0>\{[^}]+\}) backing used by a device in a virtual machine$',
    lambda g: f'远程设备 {g["g0"]} 由虚拟机中的设备使用')
register(r'^Backing a virtual disk using a host file with the flat file format used in GSX Server 3\.x and in ESX 2\.x and later$',
    lambda g: '使用主机文件的平面文件格式作为虚拟磁盘后端，适用于 GSX Server 3.x 及 ESX 2.x 及更高版本')
register(r'^Backing a virtual disk using a host file with the (?P<g0>sesparse|flat) file format used in ESX 5\.x and later$',
    lambda g: f'使用主机文件的 {g["g0"]} 文件格式作为虚拟磁盘后端，适用于 ESX 5.x 及更高版本')
register(r'^Backing a virtual disk using one or more partitions on a physical disk device$',
    lambda g: '使用物理磁盘设备上的一个或多个分区作为虚拟磁盘后端')
register(r'^Backing a virtual disk using persistent memory$',
    lambda g: '使用持久内存作为虚拟磁盘后端')
register(r'^Backing a virtual disk using a raw device mapping on ESX 2\.5 and later$',
    lambda g: '使用原始设备映射作为虚拟磁盘后端，适用于 ESX 2.5 及更高版本')
register(r'^The file backing option data object type contains file-specific backing options$',
    lambda g: '文件后端选项数据对象类型包含特定于文件的后端选项')
register(r'^Backing a serial port with a host serial port device$',
    lambda g: '使用主机串行端口设备作为串行端口后端')
register(r'^Backing a serial port with a ThinPrint device$',
    lambda g: '使用 ThinPrint 设备作为串行端口后端')
register(r'^Options for backing a serial port with a host file$',
    lambda g: '使用主机文件作为串行端口后端的选项')
register(r'^Backing a serial port device with a pipe to another process$',
    lambda g: '使用管道与另一进程通信作为串行端口设备后端')
register(r'^Backing a serial port device with a remote connection$',
    lambda g: '使用远程连接作为串行端口设备后端')
register(r'^Backing a virtual pointing device data$',
    lambda g: '虚拟指针设备后端数据')

# --- Options ---
register(r'^Options? for a (?P<g0>.+)$', lambda g: f'{g["g0"]}的选项')
register(r'^Options? for (?P<g0>.+)$', lambda g: f'{g["g0"]}的选项')
register(r'^Options? of (?P<g0>.+)$', lambda g: f'{g["g0"]}的选项')
register(r'^Options? for the (?P<g0>.+)$', lambda g: f'{g["g0"]}的选项')
register(r'^Options? for a remote (?P<g0>.+)$', lambda g: f'远程 {g["g0"]}的选项')
register(r'^Options? for remote (?P<g0>.+)$', lambda g: f'远程 {g["g0"]}的选项')
register(r'^Options for NVIDIA GRID vGPU$', lambda g: 'NVIDIA GRID vGPU 的选项')
register(r'^Options for Device Virtualization Extensions$', lambda g: '设备虚拟化扩展的选项')
register(r'^Options for DeviceGroup$', lambda g: '设备组的选项')
register(r'^Options for the Dynamic DirectPath device backing$', lambda g: '动态 DirectPath 设备后端的选项')
register(r'^Options for the plugin backing$', lambda g: '插件后端的选项')
register(r'^Options for a passthrough CD/DVD device backing$', lambda g: '直通 CD/DVD 设备后端的选项')
register(r'^Options for a remote passthrough CD/DVD device backing$', lambda g: '远程直通 CD/DVD 设备后端的选项')
register(r'^Options for a remote device backing$', lambda g: '远程设备后端的选项')
register(r'^Options for the device backing$', lambda g: '设备后端的选项')

# --- Connected ---
register(r'^Connected: (?P<g0>.+)$', lambda g: f'已连接: {g["g0"]}')
register(r'^Connected to a client$', lambda g: '已连接到客户端')
register(r'^Connected to a server$', lambda g: '已连接到服务器')
register(r'^Connect as a client$', lambda g: '作为客户端连接')
register(r'^Wait for incoming connections$', lambda g: '等待传入连接')

# --- 类型 ---
register(r'^Type: (?P<g0>.+) MAC: (?P<g1>.+)$', lambda g: f'类型: {g["g0"]} MAC: {g["g1"]}')

# --- 后端选项 label ---
register(r'^(?P<g0>.+) backing option$', lambda g: f'{g["g0"]}后端选项')
register(r'^(?P<g0>.+) Backing Option$', lambda g: f'{g["g0"]}后端选项')
register(r'^(?P<g0>.+) backing options$', lambda g: f'{g["g0"]}后端选项')
register(r'^(?P<g0>.+) device backing options?$', lambda g: f'{g["g0"]}设备后端选项')

# --- 后端选项 summary ---
register(r'^Device-specific backing options$', lambda g: '设备特定的后端选项')
register(r'^Remote device backing options$', lambda g: '远程设备后端选项')
register(r'^File-specific backing options$', lambda g: '文件特定的后端选项')
register(r'^CD/DVD device backing options?$', lambda g: 'CD/DVD 设备后端选项')
register(r'^Remote CD/DVD device backing options?$', lambda g: '远程 CD/DVD 设备后端选项')
register(r'^Virtual network card backing options$', lambda g: '虚拟网卡后端选项')
register(r'^SR-IOV specific backing options$', lambda g: 'SR-IOV 特定后端选项')
register(r'^Pipe backing options$', lambda g: '管道后端选项')

# --- VFlash ---
register(r'^Cache data consistency is guaranteed after a crash$', lambda g: '崩溃后可保证缓存数据一致性')
register(r'^Cache data consistency is not guaranteed after a crash$', lambda g: '崩溃后无法保证缓存数据一致性')
register(r'^Writes to the cache cause writes to the underlying storage$', lambda g: '写入缓存会导致写入底层存储')
register(r"^Writes to the cache do not go to the underlying storage right away\. Cache holds data temporarily till it can be permanently saved or otherwise modified\.$",
    lambda g: '写入缓存不会立即写入底层存储。缓存临时保存数据，直到可以永久保存或以其他方式修改为止。')

# --- VMCI ---
register(r'^Allow communication$', lambda g: '允许通信')
register(r'^Deny communication$', lambda g: '拒绝通信')
register(r'^Communication in any direction \(guest-to-host or host-to-guest\)$', lambda g: '任意方向的通信（客户机到主机或主机到客户机）')
register(r'^Communication over any protocol$', lambda g: '通过任意协议通信')
register(r'^Communication over the datagram protocol$', lambda g: '通过数据报协议通信')
register(r'^Communication over the doorbell protocol$', lambda g: '通过门铃协议通信')
register(r'^Communication in the guest-to-host direction$', lambda g: '客户机到主机方向的通信')
register(r'^Communication in the host-to-guest direction$', lambda g: '主机到客户机方向的通信')
register(r'^Communication over the hypervisor protocol$', lambda g: '通过虚拟机监控程序协议通信')
register(r'^Communication over the queuepair protocol$', lambda g: '通过队列对协议通信')
register(r'^Communication over the vSockets STREAM protocol$', lambda g: '通过 vSockets STREAM 协议通信')

# --- 配置版本 ---
register(r'^ESX 3\.x virtual machine$', lambda g: 'ESX 3.x 虚拟机')
register(r'^ESX 2\.x virtual machine$', lambda g: 'ESX 2.x 虚拟机')
register(r'^Server 2\.0 hardware version 4 virtual machine$', lambda g: 'Server 2.0 硬件版本 4 虚拟机')
register(r'^Server 2\.0 hardware version 6 virtual machine$', lambda g: 'Server 2.0 硬件版本 6 虚拟机')
register(r'^GSX Server 3\.x virtual machine$', lambda g: 'GSX Server 3.x 虚拟机')
register(r'^Server 2\.0 virtual machine$', lambda g: 'Server 2.0 虚拟机')
register(r'^ESX/ESXi 4\.x virtual machine$', lambda g: 'ESX/ESXi 4.x 虚拟机')
register(r'^ESXi (?P<g0>[0-9]+\.[0-9]+( U[0-9]+)?) virtual machine$', lambda g: f'ESXi {g["g0"]} 虚拟机')
register(r'^Workstation (?P<g0>[0-9]+) virtual machine$', lambda g: f'Workstation {g["g0"]} 虚拟机')
register(r'^Unrecognized virtual machine$', lambda g: '无法识别的虚拟机')

# --- 物理/虚拟模式 ---
register(r'^Physical mode - Commands are passed through to the LUN$', lambda g: '物理模式 - 命令直通到 LUN')
register(r'^Virtual mode - Disk modes are respected$', lambda g: '虚拟模式 - 遵循磁盘模式')

# --- 精度时钟 ---
register(r'^Virtual clock device providing precision time$', lambda g: '提供精确时间的虚拟时钟设备')
register(r'^Options for a precision clock using host system clock as reference$', lambda g: '使用主机系统时钟作为参考的精确时钟选项')

# --- ROM/VMCI ---
register(r'^ROM on the virtual machine PCI bus that provides support for VMI$', lambda g: '虚拟机 PCI 总线上的 ROM，提供对 VMI 的支持')
register(r'^Device on the virtual machine PCI bus that provides support for the virtual machine communication interface$',
    lambda g: '虚拟机 PCI 总线上的设备，提供对虚拟机通信接口的支持')

# --- Auto connect ---
register(r'^Auto connect (?P<g0>.+)$', lambda g: f'自动连接 {g["g0"]}')

# --- data object contains ---
register(r'^(?P<g0>.+) data object type contains (?P<g1>.+)$', lambda g: f'{g["g0"]}数据对象类型包含{g["g1"]}')

# 术语词典
TERM_DICT = OrderedDict()
def add_term(en, zh):
    TERM_DICT[en] = zh

for t in [
    ('CD/DVD drive', 'CD/DVD 驱动器'), ('Hard disk', '硬盘'), ('Floppy drive', '软驱'),
    ('Network adapter', '网络适配器'), ('Serial port', '串行端口'), ('Parallel port', '并行端口'),
    ('Pointing device', '指针设备'), ('Video card', '显卡'), ('Sound card', '声卡'),
    ('HD audio', 'HD 音频'), ('Audio', '音频'), ('Keyboard', '键盘'),
    ('Watchdog timer', '看门狗定时器'), ('Precision Clock', '精确时钟'), ('Precision clock', '精确时钟'),
    ('Virtual TPM', '虚拟 TPM'), ('Virtual QAT', '虚拟 QAT'), ('NVDIMM Controller', 'NVDIMM 控制器'),
    ('NVDIMM', 'NVDIMM'), ('USB xHCI controller', 'USB xHCI 控制器'), ('USB controller', 'USB 控制器'),
    ('SATA controller', 'SATA 控制器'), ('SIO controller', 'SIO 控制器'),
    ('SCSI controller', 'SCSI 控制器'), ('SCSI device', 'SCSI 设备'), ('PCI device', 'PCI 设备'),
    ('PCI controller', 'PCI 控制器'), ('NVMe controller', 'NVMe 控制器'),
    ('NVME controller', 'NVMe 控制器'), ('IDE controller', 'IDE 控制器'),
    ('AHCI', 'AHCI'), ('BusLogic', 'BusLogic'), ('LSI Logic SAS', 'LSI Logic SAS'),
    ('LSI Logic', 'LSI Logic'), ('VMware paravirtual SCSI', 'VMware 半虚拟化 SCSI'),
    ('SR-IOV network adapter', 'SR-IOV 网络适配器'), ('Virtual machine ROM', '虚拟机 ROM'),
    ('Persistent', '持久'), ('persistent', '持久'), ('nonpersistent', '非持久'),
    ('non-persistent', '非持久'), ('Independent persistent', '独立持久'),
    ('Independent nonpersistent', '独立非持久'), ('Independent-nonpersistent', '独立非持久'),
    ('Independent-persistent', '独立持久'), ('Independent non-persistent', '独立非持久'),
    ('Undoable', '可撤销'), ('Append', '追加'), ('Redolog based', '基于重做日志'),
    ('Native Snapshot based', '基于本机快照'), ('Redolog-based', '基于重做日志'),
    ('Native-Snapshot-based', '基于本机快照'), ('delta disk', '增量磁盘'),
    ('SectorFormat native_512', '扇区格式 本机 512 字节'),
    ('SectorFormat emulated_512', '扇区格式 模拟 512 字节'),
    ('SectorFormat native_4k', '扇区格式 本机 4K'),
    ('Disk file', '磁盘文件'), ('RDM description file', 'RDM 描述文件'),
    ('Disk description file', '磁盘描述文件'), ('Virtual mode', '虚拟模式'),
    ('Physical mode', '物理模式'), ('Physical', '物理'), ('Virtual', '虚拟'),
    ('Native', '本机'), ('Flat', '平面'), ('Sparse', '稀疏'), ('Local', '本地'),
    ('Raw', '原始'), ('raw', '原始'), ('partition', '分区'),
    ('Bridged', '桥接'), ('Bridged network', '桥接网络'), ('Host only', '仅主机'),
    ('Host-only network', '仅主机网络'), ('Network address translation', '网络地址转换'),
    ('ESX network', 'ESX 网络'), ('Custom', '自定义'), ('Assigned', '已分配'),
    ('Generated', '已生成'), ('Manual', '手动'),
    ('.vmdk', '.vmdk'), ('.iso', '.iso'), ('.flp', '.flp'), ('.rdm', '.rdm'), ('.dsk', '.dsk'),
    ('strong', '强'), ('weak', '弱'), ('write_thru', '直写'), ('write_back', '回写'),
    ('OK', '确定'), ('Cancel', '取消'), ('Retry', '重试'), ('Yes', '是'), ('No', '否'),
    ('Abort', '中止'), ('Allow', '允许'), ('Deny', '拒绝'), ('Any direction', '任意方向'),
    ('Any protocol', '任意协议'), ('Datagram', '数据报'), ('Doorbell', '门铃'),
    ('Queuepair', '队列对'), ('Stream', '流'), ('Hypervisor', '虚拟机监控程序'),
    ('Passthrough', '直通'), ('passthrough', '直通'), ('Pass-through', '直通'),
    ('Dynamic DirectPath', '动态 DirectPath'), ('PCI plugin', 'PCI 插件'),
    ('ThinPrint device', 'ThinPrint 设备'), ('NVIDIA GRID vGPU', 'NVIDIA GRID vGPU'),
    ('Device Virtualization Extensions', '设备虚拟化扩展'), ('SR-IOV', 'SR-IOV'),
    ('Device Group', '设备组'), ('Vendor Device Group', '供应商设备组'),
    ('Non-volatile memory', '非易失性内存'), ('Persistent memory', '持久内存'),
    ('persistent memory', '持久内存'), ('USB device', 'USB 设备'),
    ('Virtual USB device', '虚拟 USB 设备'), ('Host Remote USB device', '主机远程 USB 设备'),
    ('Client Remote USB device', '客户端远程 USB 设备'), ('Floppy image', '软盘映像'),
    ('Image backing', '映像后端'), ('Host device', '主机设备'), ('Remote device', '远程设备'),
    ('backing option', '后端选项'), ('Backing Option', '后端选项'), ('backing type', '后端类型'),
    ('device backing', '设备后端'), ('file backing', '文件后端'), ('pipe backing', '管道后端'),
    ('device-specific', '设备特定的'), ('file-specific', '文件特定的'),
    ('OUI', 'OUI'), ('MAC', 'MAC'), ('Auto connect', '自动连接'), ('Host system', '主机系统'),
    ('system clock', '系统时钟'), ('as reference', '作为参考'), ('Unit', '单元'),
    ('Non-volatile', '非易失性'), ('Virtual Trusted Platform Module', '虚拟受信任平台模块'),
    ('Virtual QuickAssist Technology', '虚拟 QuickAssist 技术'), ('description file', '描述文件'),
    ('description', '描述'), ('independent', '独立'), ('Partitioned', '已分区'),
    ('mapping', '映射'), ('precision', '精确'), ('clock', '时钟'), ('format', '格式'),
    ('later', '更高版本'), ('backing', '后端'), ('Backing', '后端'),
    ('Precision Time Protocol', '精确时间协议'), ('Network Time Protocol', '网络时间协议'),
    ('Host', '主机'), ('host', '主机'), ('Guest', '客户机'), ('guest', '客户机'),
    ('Device', '设备'), ('device', '设备'), ('File', '文件'), ('file', '文件'),
    ('files', '文件'), ('Pipe', '管道'), ('pipe', '管道'), ('Remote', '远程'),
    ('remote', '远程'), ('Image', '映像'), ('image', '映像'), ('Network', '网络'),
    ('network', '网络'), ('Virtual', '虚拟'), ('virtual', '虚拟'),
    ('IDE', 'IDE'), ('SCSI', 'SCSI'), ('SATA', 'SATA'), ('PCI', 'PCI'),
    ('NVMe', 'NVMe'), ('NVME', 'NVMe'), ('USB', 'USB'), ('ATAPI', 'ATAPI'),
    ('CD-ROM', 'CD-ROM'), ('ESX', 'ESX'), ('ESXi', 'ESXi'),
    ('controller', '控制器'), ('Controller', '控制器'), ('adapter', '适配器'),
    ('Adapter', '适配器'), ('drive', '驱动器'), ('Drive', '驱动器'),
    ('disk', '磁盘'), ('Disk', '磁盘'), ('disks', '磁盘'), ('port', '端口'),
    ('Port', '端口'), ('mode', '模式'), ('Mode', '模式'), ('type', '类型'),
    ('Type', '类型'), ('option', '选项'), ('Option', '选项'), ('options', '选项'),
    ('Options', '选项'), ('Connected', '已连接'), ('connected', '已连接'),
    ('Autodetect', '自动检测'), ('using', '使用'), ('contains', '包含'),
    ('provides', '提供'), ('data object', '数据对象'), ('Extensions', '扩展'),
    ('Extension', '扩展'), ('Technology', '技术'), ('Platform', '平台'),
    ('Module', '模块'), ('Timer', '定时器'), ('Watchdog', '看门狗'),
    ('memory', '内存'), ('Memory', '内存'), ('storage', '存储'), ('Storage', '存储'),
    ('server', '服务器'), ('Server', '服务器'), ('communication', '通信'),
    ('Communication', '通信'), ('interface', '接口'), ('bus', '总线'),
    ('Bus', '总线'), ('connection', '连接'), ('connections', '连接'),
    ('crash', '崩溃'), ('temporarily', '临时'), ('underlying', '底层'),
    ('data', '数据'), ('Data', '数据'), ('cache', '缓存'), ('Cache', '缓存'),
    ('consistency', '一致性'), ('unrecognized', '无法识别'), ('Unrecognized', '无法识别'),
    ('Client', '客户端'), ('Server', '服务器'), ('Project', '项目'), ('Publish', '发布'),
    ('ThinPrint', 'ThinPrint'), ('RoCEv1 device', 'RoCEv1 设备'), ('RoCEv2 device', 'RoCEv2 设备'),
    ('ISO image', 'ISO 映像'), ('ISO image files', 'ISO 映像文件'), ('ISO Backing', 'ISO 后端'),
    ('Serial port output files', '串行端口输出文件'), ('Parallel port output files', '并行端口输出文件'),
    ('output files', '输出文件'), ('Any', '任意'),
]:
    add_term(*t)

TERM_KEYS = sorted(TERM_DICT.keys(), key=len, reverse=True)

def translate_by_terms(en_text):
    protected, tokens = protect(en_text)
    result = protected
    for term in TERM_KEYS:
        if term in result:
            result = result.replace(term, TERM_DICT[term])
    # 清理英文虚词
    result = re.sub(r'\b(a|an|the|is|are|was|were|be|been|in|on|at|to|for|of|by|with|from|that|this|these|those|it|its|or|and|not|as|but|do|does|did|has|have|had|can|could|will|would|shall|should|may|might|per|each|all|some|any|no|both|either|neither|such|which|what|when|where|how|whose|whom|than|then|there|here|into|onto|upon|without|within|through|during|before|after|above|below|between|among|off|over|under|up|out|about|along|around|down|past|since|till|until|via|use|used|set|using)\b', '', result)
    result = re.sub(r'\s{2,}', ' ', result)
    result = re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])', '', result)
    result = re.sub(r'\s+([，。；：、？！）])', r'\1', result)
    result = re.sub(r'（\s+', '（', result)
    result = result.strip()
    result = restore(result, tokens)
    return result

def try_template_translate(en_value):
    for pattern, translator in SENTENCE_TEMPLATES:
        m = pattern.match(en_value.strip())
        if m:
            try:
                result = translator(m.groupdict())
                result = translate_by_terms(result)
                return result
            except:
                continue
    return None

def translate_value(en_value):
    result = try_template_translate(en_value)
    return result if result is not None else translate_by_terms(en_value)

def fix_key_name(key):
    return key.replace('Pass到', 'Passthrough')

def main():
    print("=" * 70)
    print("VMware vm.vmsg 逐条对照精准翻译 V3")
    print("=" * 70)
    en_entries = {}; zh_entries = {}
    with open(EN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            m = ENTRY_RE.match(line)
            if m: en_entries[m.group('key')] = m.group('value')
    with open(ZH_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            m = ENTRY_RE.match(line)
            if m: zh_entries[m.group('key')] = m.group('value')
    os.makedirs(BACKUP_DIR, exist_ok=True)
    if not os.path.exists(BACKUP_FILE):
        shutil.copy2(ZH_FILE, BACKUP_FILE)
        print(f"已备份: {BACKUP_FILE}")
    with open(ZH_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    stats = {'key_fixed': 0, 'value_updated': 0, 'template_matched': 0, 'term_translated': 0}
    output_lines = []
    for line in lines:
        m = ENTRY_RE.match(line.rstrip('\n'))
        if not m:
            output_lines.append(line); continue
        orig_key = m.group('key'); orig_value = m.group('value')
        fixed_key = fix_key_name(orig_key)
        if fixed_key != orig_key: stats['key_fixed'] += 1
        en_value = en_entries.get(fixed_key) or en_entries.get(orig_key)
        if en_value is None:
            output_lines.append(line.replace(orig_key, fixed_key, 1) if fixed_key != orig_key else line)
            continue
        if not has_en(orig_value):
            output_lines.append(line.replace(orig_key, fixed_key, 1) if fixed_key != orig_key else line)
            continue
        new_value = translate_value(en_value)
        if new_value != orig_value:
            stats['value_updated'] += 1
            if new_value == translate_by_terms(en_value):
                stats['term_translated'] += 1
            else:
                stats['template_matched'] += 1
        new_line = f'{fixed_key}="{new_value}"\n'
        output_lines.append(new_line)
        if stats['value_updated'] <= 8:
            print(f"\n  [{stats['value_updated']}] {fixed_key[:55]}")
            print(f"    原: {orig_value[:80]}")
            print(f"    新: {new_value[:80]}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(output_lines)
    print(f"\n{'=' * 70}")
    print(f"修复完成!")
    print(f"  Key 名修复: {stats['key_fixed']}")
    print(f"  Value 翻译更新: {stats['value_updated']}")
    print(f"    句式模板: {stats['template_matched']}")
    print(f"    术语词典: {stats['term_translated']}")
    print(f"  输出文件: {OUTPUT_FILE}")
    print(f"{'=' * 70}")

if __name__ == '__main__':
    main()
