#!/usr/bin/env python3
"""
locmsg.vmsg zh-CN Translation Fix v4

A clean, reliable script that:
1. Backs up original file to .backup/
2. Parses EN and ZH entries
3. For each entry with remaining English issues, retranslates from EN source
4. Protects placeholders before any text processing
5. Writes fixed output

Usage: python fix_locmsg_v4.py
"""

import os, re, shutil
from datetime import datetime

EN_FILE = r"D:\vmware\i18n\OVFTool\env\en\locmsg.vmsg"
ZH_FILE = r"D:\vmware\i18n\OVFTool\env\zh-CN\locmsg.vmsg"
BACKUP_DIR = r"D:\vmware\i18n\.backup"

# ── Term dictionary: multi-word phrases FIRST, then single words ──
TERMS = [
    # Multi-word phrases (must come before their component words)
    ("host bus adapter", "主机总线适配器"),
    ("network adapter", "网络适配器"),
    ("physical network adapter", "物理网络适配器"),
    ("vmkernel network adapter", "VMkernel 网络适配器"),
    ("distributed port group", "分布式端口组"),
    ("distributed switch", "分布式交换机"),
    ("resource pool", "资源池"),
    ("content library item", "内容库项目"),
    ("content library", "内容库"),
    ("fault tolerance", "容错"),
    ("resource profile", "资源配置文件"),
    ("maintenance mode", "维护模式"),
    ("standby mode", "待机模式"),
    ("lockdown mode", "锁定模式"),
    ("power state", "电源状态"),
    ("powered on", "已打开电源"),
    ("powered off", "已关闭电源"),
    ("power on", "打开电源"),
    ("power off", "关闭电源"),
    ("power up", "启动"),
    ("power down", "关闭"),
    ("thin provisioned", "已精简置备"),
    ("thin-provisioned", "已精简置备"),
    ("zeroed thick", "零置备厚格式"),
    ("zeroed-thick", "零置备厚格式"),
    ("port group", "端口组"),
    ("file system", "文件系统"),
    ("default gateway", "默认网关"),
    ("ip address", "IP 地址"),
    ("mac address", "MAC 地址"),
    ("subnet mask", "子网掩码"),
    ("disk group", "磁盘组"),
    ("virtual machine", "虚拟机"),
    ("virtual disk", "虚拟磁盘"),
    ("virtual device", "虚拟设备"),
    ("virtual switch", "虚拟交换机"),
    ("fault tolerance", "容错"),
    ("vmware tools", "VMware Tools"),
    ("vcenter server", "vCenter Server"),
    ("vcenter ha", "vCenter HA"),
    ("vsphere replication", "vSphere 复制"),
    
    # States and adjectives
    ("enabled", "已启用"),
    ("disabled", "已禁用"),
    ("connected", "已连接"),
    ("disconnected", "已断开连接"),
    ("associated", "已关联"),
    ("registered", "已注册"),
    ("unregistered", "已注销"),
    ("initialized", "已初始化"),
    ("installed", "已安装"),
    ("licensed", "已授权"),
    ("expired", "已过期"),
    ("reserved", "已预留"),
    ("removed", "已移除"),
    ("deleted", "已删除"),
    ("created", "已创建"),
    ("modified", "已修改"),
    ("updated", "已更新"),
    ("locked", "已锁定"),
    ("unlocked", "已解锁"),
    ("stopped", "已停止"),
    ("started", "已启动"),
    ("completed", "已完成"),
    ("finished", "已完成"),
    ("succeeded", "已成功"),
    ("configured", "已配置"),
    ("synchronized", "已同步"),
    ("migrated", "已迁移"),
    ("deployed", "已部署"),
    ("cloned", "已克隆"),
    ("attached", "已附加"),
    ("mounted", "已挂载"),
    ("unmounted", "已卸载"),
    ("generated", "已生成"),
    ("specified", "指定"),
    ("suspended", "已挂起"),
    ("supported", "支持"),
    ("unsupported", "不支持"),
    
    # Core nouns
    ("virtual machine", "虚拟机"),
    ("virtual disk", "虚拟磁盘"),
    ("virtual device", "虚拟设备"),
    ("host", "主机"),
    ("hosts", "主机"),
    ("server", "服务器"),
    ("service", "服务"),
    ("services", "服务"),
    ("device", "设备"),
    ("devices", "设备"),
    ("disk", "磁盘"),
    ("disks", "磁盘"),
    ("storage", "存储"),
    ("memory", "内存"),
    ("network", "网络"),
    ("cluster", "集群"),
    ("clusters", "集群"),
    ("datastore", "数据存储"),
    ("datastores", "数据存储"),
    ("snapshot", "快照"),
    ("snapshots", "快照"),
    ("sector", "扇区"),
    ("sectors", "扇区"),
    ("partition", "分区"),
    ("volume", "卷"),
    ("user", "用户"),
    ("users", "用户"),
    ("username", "用户名"),
    ("password", "密码"),
    ("account", "帐户"),
    ("certificate", "证书"),
    ("certificates", "证书"),
    ("token", "令牌"),
    ("session", "会话"),
    ("profile", "配置文件"),
    ("policy", "策略"),
    ("policies", "策略"),
    ("rule", "规则"),
    ("folder", "文件夹"),
    ("folders", "文件夹"),
    ("file", "文件"),
    ("files", "文件"),
    ("directory", "目录"),
    ("path", "路径"),
    ("paths", "路径"),
    ("name", "名称"),
    ("names", "名称"),
    ("type", "类型"),
    ("types", "类型"),
    ("state", "状态"),
    ("status", "状态"),
    ("log", "日志"),
    ("logs", "日志"),
    ("event", "事件"),
    ("events", "事件"),
    ("error", "错误"),
    ("errors", "错误"),
    ("warning", "警告"),
    ("warnings", "警告"),
    ("message", "消息"),
    ("messages", "消息"),
    ("version", "版本"),
    ("config", "配置"),
    ("configuration", "配置"),
    ("property", "属性"),
    ("properties", "属性"),
    ("parameter", "参数"),
    ("parameters", "参数"),
    ("attribute", "属性"),
    ("component", "组件"),
    ("components", "组件"),
    ("feature", "功能"),
    ("features", "功能"),
    ("capability", "能力"),
    ("capacity", "容量"),
    ("resource", "资源"),
    ("resources", "资源"),
    ("privilege", "特权"),
    ("permission", "权限"),
    ("authorization", "授权"),
    ("authentication", "身份验证"),
    ("security", "安全性"),
    ("encryption", "加密"),
    ("encrypted", "已加密"),
    ("namespace", "命名空间"),
    ("provider", "提供程序"),
    ("adapter", "适配器"),
    ("adapters", "适配器"),
    ("controller", "控制器"),
    ("operation", "操作"),
    ("operations", "操作"),
    ("information", "信息"),
    ("description", "描述"),
    ("label", "标签"),
    ("summary", "摘要"),
    ("number", "数量"),
    ("count", "计数"),
    ("total", "总计"),
    ("amount", "数量"),
    ("size", "大小"),
    ("length", "长度"),
    ("limit", "限制"),
    ("threshold", "阈值"),
    ("level", "级别"),
    ("priority", "优先级"),
    ("action", "操作"),
    ("task", "任务"),
    ("method", "方法"),
    ("mode", "模式"),
    ("option", "选项"),
    ("setting", "设置"),
    ("format", "格式"),
    ("tag", "标签"),
    ("role", "角色"),
    ("entity", "实体"),
    ("entities", "实体"),
    ("object", "对象"),
    ("objects", "对象"),
    ("target", "目标"),
    ("source", "源"),
    ("destination", "目标"),
    ("input", "输入"),
    ("output", "输出"),
    ("value", "值"),
    ("values", "值"),
    ("reason", "原因"),
    ("condition", "条件"),
    ("context", "上下文"),
    ("attempt", "尝试"),
    ("detail", "详细信息"),
    ("details", "详细信息"),
    ("workload", "工作负载"),
    ("instance", "实例"),
    ("edition", "版本"),
    ("subsystem", "子系统"),
    ("specification", "规范"),
    ("parent", "父"),
    ("child", "子"),
    ("base", "基本"),
    ("beyond", "超出"),
    ("feature", "功能"),
    ("node", "节点"),
    ("nodes", "节点"),
    ("port", "端口"),
    ("ports", "端口"),
    ("uplink", "上行链路"),
    ("uplinks", "上行链路"),
    ("license", "许可证"),
    ("support", "支持"),
    
    # Verbs - common
    ("cannot", "无法"),
    ("can not", "无法"),
    ("failed to", "无法"),
    ("fail to", "无法"),
    ("fails to", "无法"),
    ("unable to", "无法"),
    ("allow", "允许"),
    ("disallow", "不允许"),
    ("enable", "启用"),
    ("disable", "禁用"),
    ("process", "处理"),
    ("perform", "执行"),
    ("request", "请求"),
    ("verify", "验证"),
    ("ensure", "确保"),
    ("select", "选择"),
    ("specify", "指定"),
    ("provide", "提供"),
    ("configure", "配置"),
    ("reconfigure", "重新配置"),
    ("deploy", "部署"),
    ("deployment", "部署"),
    ("migrate", "迁移"),
    ("migration", "迁移"),
    ("migrating", "正在迁移"),
    ("clone", "克隆"),
    ("cloning", "正在克隆"),
    ("attach", "附加"),
    ("detach", "分离"),
    ("remove", "移除"),
    ("removing", "正在移除"),
    ("add", "添加"),
    ("adding", "正在添加"),
    ("update", "更新"),
    ("updating", "正在更新"),
    ("modify", "修改"),
    ("delete", "删除"),
    ("deleting", "正在删除"),
    ("create", "创建"),
    ("creating", "正在创建"),
    ("rename", "重命名"),
    ("move", "移动"),
    ("moving", "正在移动"),
    ("import", "导入"),
    ("export", "导出"),
    ("generate", "生成"),
    ("synchronize", "同步"),
    ("restart", "重新启动"),
    ("reboot", "重新引导"),
    ("suspend", "挂起"),
    ("resume", "恢复"),
    ("resolve", "解决"),
    ("recover", "恢复"),
    ("recovery", "恢复"),
    ("allocate", "分配"),
    ("release", "释放"),
    ("assign", "分配"),
    ("consume", "消耗"),
    ("consumed", "已消耗"),
    ("exceed", "超过"),
    ("exceeded", "超过"),
    ("increase", "增加"),
    ("decrease", "减少"),
    ("reduce", "减少"),
    ("extend", "扩展"),
    ("extending", "正在扩展"),
    ("expand", "展开"),
    ("upgrade", "升级"),
    ("upgraded", "已升级"),
    ("convert", "转换"),
    ("conversion", "转换"),
    ("transfer", "传输"),
    ("transferring", "正在传输"),
    ("mount", "挂载"),
    ("unmount", "卸载"),
    ("load", "加载"),
    ("loading", "正在加载"),
    ("unload", "卸载"),
    ("wait", "等待"),
    ("waiting", "正在等待"),
    ("match", "匹配"),
    ("detect", "检测"),
    ("detected", "已检测"),
    ("identify", "标识"),
    ("identifying", "正在标识"),
    ("obtain", "获取"),
    ("receive", "接收"),
    ("received", "已接收"),
    ("send", "发送"),
    ("submit", "提交"),
    ("return", "返回"),
    ("display", "显示"),
    ("show", "显示"),
    ("hide", "隐藏"),
    ("override", "覆盖"),
    ("overwrite", "覆盖"),
    ("reset", "重置"),
    ("refresh", "刷新"),
    ("clear", "清除"),
    ("confirm", "确认"),
    ("save", "保存"),
    ("store", "存储"),
    ("stored", "已存储"),
    ("restore", "还原"),
    ("discover", "发现"),
    ("register", "注册"),
    ("unregister", "注销"),
    ("install", "安装"),
    ("uninstall", "卸载"),
    ("apply", "应用"),
    ("applied", "已应用"),
    ("applying", "正在应用"),
    ("execute", "执行"),
    ("read", "读取"),
    ("write", "写入"),
    ("written", "已写入"),
    ("writing", "正在写入"),
    ("occurred", "发生"),
    ("contains", "包含"),
    ("contain", "包含"),
    ("include", "包括"),
    ("includes", "包括"),
    ("including", "包括"),
    ("requires", "需要"),
    ("require", "需要"),
    ("corresponds", "对应"),
    ("corresponding", "对应"),
    ("retry", "重试"),
    ("retries", "重试"),
    ("failure", "失败"),
    ("failover", "故障切换"),
    ("monitor", "监视"),
    ("maintain", "维护"),
    ("manage", "管理"),
    ("management", "管理"),
    ("managed", "已管理"),
    ("managing", "正在管理"),
    ("preserve", "保留"),
    ("reconnect", "重新连接"),
    ("reload", "重新加载"),
    ("replace", "替换"),
    ("replicate", "复制"),
    ("replication", "复制"),
    ("report", "报告"),
    ("terminate", "终止"),
    ("abort", "中止"),
    ("aborted", "已中止"),
    ("cancel", "取消"),
    ("canceled", "已取消"),
    ("cancelled", "已取消"),
    
    # Adjectives & attributes
    ("maximum", "最大"),
    ("minimum", "最小"),
    ("optimal", "最佳"),
    ("correct", "正确"),
    ("correctly", "正确"),
    ("incorrect", "不正确"),
    ("proper", "正确"),
    ("properly", "正确"),
    ("generic", "常规"),
    ("specific", "特定"),
    ("duplicate", "重复"),
    ("conflicting", "冲突"),
    ("missing", "缺失"),
    ("empty", "空"),
    ("valid", "有效"),
    ("invalid", "无效"),
    ("available", "可用"),
    ("unavailable", "不可用"),
    ("accessible", "可访问"),
    ("inaccessible", "不可访问"),
    ("compatible", "兼容"),
    ("incompatible", "不兼容"),
    ("sufficient", "足够"),
    ("insufficient", "不足"),
    ("unknown", "未知"),
    ("pending", "待定"),
    ("queued", "已排队"),
    ("active", "活动"),
    ("inactive", "非活动"),
    ("passive", "被动"),
    ("standalone", "独立"),
    ("normal", "正常"),
    ("temporary", "临时"),
    ("temporarily", "临时"),
    ("permanent", "永久"),
    ("permanently", "永久"),
    ("automatic", "自动"),
    ("automatically", "自动"),
    ("manual", "手动"),
    ("manually", "手动"),
    ("explicit", "显式"),
    ("implicit", "隐式"),
    ("initial", "初始"),
    ("final", "最终"),
    ("primary", "主要"),
    ("secondary", "辅助"),
    ("major", "主要"),
    ("minor", "次要"),
    ("critical", "严重"),
    ("severe", "严重"),
    ("partial", "部分"),
    ("full", "完全"),
    ("complete", "完全"),
    ("incomplete", "不完全"),
    ("entire", "整个"),
    ("absolute", "绝对"),
    ("relative", "相对"),
    ("local", "本地"),
    ("remote", "远程"),
    ("internal", "内部"),
    ("external", "外部"),
    ("virtual", "虚拟"),
    ("physical", "物理"),
    ("logical", "逻辑"),
    ("dynamic", "动态"),
    ("static", "静态"),
    ("offline", "离线"),
    ("online", "在线"),
    ("advanced", "高级"),
    ("basic", "基本"),
    ("simple", "简单"),
    ("complex", "复杂"),
    ("consistent", "一致"),
    ("inconsistent", "不一致"),
    ("immediate", "立即"),
    ("immediately", "立即"),
    ("ongoing", "正在进行的"),
    
    # Conjunctions / prepositions
    ("and", "和"),
    ("or", "或"),
    ("but", "但"),
    ("if", "如果"),
    ("then", "则"),
    ("else", "否则"),
    ("because", "因为"),
    ("while", "同时"),
    ("when", "时"),
    ("where", "其中"),
    ("whether", "是否"),
    ("unless", "除非"),
    ("although", "虽然"),
    ("however", "但是"),
    ("therefore", "因此"),
    ("thus", "因此"),
    ("also", "也"),
    ("only", "仅"),
    ("just", "仅"),
    ("already", "已"),
    ("still", "仍"),
    ("even", "即使"),
    ("not", "未"),
    ("no", "无"),
    ("any", "任何"),
    ("all", "所有"),
    ("both", "两者"),
    ("either", "任一"),
    ("neither", "两者均不"),
    ("some", "某些"),
    ("many", "许多"),
    ("much", "很多"),
    ("more", "更多"),
    ("most", "最多"),
    ("less", "更少"),
    ("least", "最少"),
    ("other", "其他"),
    ("another", "另一个"),
    ("each", "每个"),
    ("every", "每个"),
    ("multiple", "多个"),
    ("various", "各种"),
    ("certain", "特定"),
    ("following", "以下"),
    ("existing", "现有"),
    ("current", "当前"),
    ("previously", "先前"),
    ("previous", "先前"),
    ("original", "原始"),
    ("additional", "额外"),
    ("extra", "额外"),
    ("same", "相同"),
    ("different", "不同"),
    ("separate", "单独"),
    ("individual", "单个"),
    ("such", "此类"),
    ("according to", "根据"),
    ("based on", "基于"),
    ("due to", "由于"),
    ("regardless of", "无论"),
    ("instead of", "而不是"),
    ("as well as", "以及"),
    ("per", "每"),
    ("via", "通过"),
    ("through", "通过"),
    ("within", "内"),
    ("without", "没有"),
    ("during", "期间"),
    ("since", "自"),
    ("until", "直到"),
    ("after", "后"),
    ("before", "前"),
    ("between", "之间"),
    ("among", "之间"),
    ("above", "以上"),
    ("below", "以下"),
    ("under", "下"),
    ("over", "超过"),
    ("across", "跨"),
    ("against", "对"),
    ("including", "包括"),
    ("except", "除"),
    ("regarding", "关于"),
    ("according", "根据"),
    ("besides", "此外"),
    ("of", "的"),
    ("in", "在"),
    ("on", "在"),
    ("at", "在"),
    ("to", "到"),
    ("for", "的"),
    ("by", "由"),
    ("from", "从"),
    ("with", "使用"),
    ("into", "到"),
    ("onto", "到"),
    ("out", "出"),
    ("up", "上"),
    ("down", "下"),
    ("off", "关闭"),
    
    # Articles - remove
    ("the", ""),
    ("a", ""),
    ("an", ""),
    
    # Be-verbs - remove
    ("is", ""),
    ("are", ""),
    ("was", ""),
    ("were", ""),
    ("be", ""),
    ("been", ""),
    ("being", ""),
    ("has", ""),
    ("have", ""),
    ("had", ""),
    ("do", ""),
    ("does", ""),
    ("did", ""),
    ("done", ""),
    ("having", ""),
    ("its", ""),
    ("their", ""),
    ("your", ""),
    ("this", ""),
    ("that", ""),
    ("these", ""),
    ("those", ""),
    ("it", ""),
    ("them", ""),
    
    # Modals
    ("will", "将"),
    ("would", ""),
    ("should", "应"),
    ("could", ""),
    ("may", "可能"),
    ("might", "可能"),
    ("shall", "应"),
    ("must", "必须"),
    ("can", ""),
    ("need", "需要"),
    ("needs", "需要"),
    ("wants", "需要"),
    
    # Misc
    ("too", "过"),
    ("very", "很"),
    ("really", "确实"),
    ("quite", "相当"),
]

# ── Known proper nouns to keep as-is ──
PROPER_NOUNS = {
    'API','CPU','IP','DNS','DHCP','HTTP','HTTPS','SSH','SSL','TCP','UDP',
    'NFS','VMFS','VVol','vVol','FCD','CBT','TPM','SEV','SGX','TDX',
    'NVDIMM','PXE','EFI','VGA','ROM','AHCI','NVMe','NVME','PVSCSI',
    'SATA','SAS','FCoE','iSCSI','VXLAN','E1000','VXNET','OVF','OVA',
    'VMDK','VMX','RDMA','VIB','ESX','ESXi','VCSA','PSC','KB',
    'SMTP','KMS','JWT','JSON','XML','HTML','WWN','VC','NAS',
    'VM','PNIC','UUID','BIOS','GUID','MAC','HBA','DPU','MTU',
    'SRM','HA','DRS','EVC','SDRS','HCI','VLCM','HPP','IOPS',
    'VCF','VASA','VCHA','VCLS','CCPE','VMRP','DPP','CDRS',
    'DPM','SIOC','IORM','GSS','LWD','FT','VR','OCM','NPIV',
    'VOB','OSFS','CLOM','DOM','VAPI','VDTC','FLB','VTC',
    'VPXD','HOSTD','VPX','VIM','RDM','OVFIO',
    'NSX','DCUI','SMBIOS','PCK','TCB','ACPI',
    'PNID','CCP','VMIOP','WCP','SEV','SGX','SLOT',
    'LRO','SLA','SLO','QoS','DSCP','DVS','DVPort','VLAN',
    'PVLAN','VXLAN','Geneve','NVGRE','VMkernel','VDS',
    'NFC','VStorage','EVPN','BGP','OSPF',
    'SVGA','VMCI','VMC','CIM','SFCB','SLP','CBRC',
    'HBR','VR','vMotion','VMotion','QuickBoot',
    'NUMA','HT','TCO','UEFI','MOREF','POD','DDNS',
    'VSCSIRef','VST','OID','FSS','FSSAgent','VDF',
    'VMXNET','VMXNET3','E1000E','SVM','AVS','DMTF',
    'VNC','RDP','LDAP','REST','SOAP',
    'SVG','PDF','PNG','CSV',
    'LB','RR','I/O','IO',
    'VDTC','FLB',
    'VMCI','VMSVC',
    'VIDM','WS1','AVI','NSXT',
    'VRLI','VRNI','VRO','VRA','VROps','VRSLCM',
    'ARC','vRealize',
    'SR_IOV','PCI',
    'PNIC','VMNIC','VNIC',
    'VHBA','VSwitch','VSS',
    'TcpipStack','Vmknic',
    'DVD','CD','PSC',
    'VASA','VVol','SIOC',
    'SPBM','VSAN',
}


def parse_vmsg(filepath):
    """Parse .vmsg into {key: value} dict."""
    entries = {}
    with open(filepath, encoding='utf-8') as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith('#') or s.startswith('signature'):
                continue
            m = re.match(r'^([a-zA-Z0-9_.]+)\s*=\s*"(.+)"\s*$', s)
            if m:
                entries[m.group(1)] = m.group(2)
    return entries


def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def chinese_ratio(text):
    cleaned = re.sub(r'\{[^}]+\}|%[0-9$I64u|.a-z]+', '', text)
    if not cleaned:
        return 0.0
    cn = len(re.findall(r'[\u4e00-\u9fff]', cleaned))
    return cn / len(cleaned.strip()) if cleaned.strip() else 0.0


def protect_placeholders(text):
    """Replace {xxx} and %xx with safe markers."""
    markers = {}
    def _protect(m):
        idx = len(markers)
        marker = f'\x00PH{idx}\x00'
        markers[marker] = m.group(0)
        return marker
    result = re.sub(r'\{[^}]+\}', _protect, text)
    result = re.sub(r'%[0-9]+(?:\$[sdIu]|[$|.l]*[0-9]*[a-z])?', _protect, result)
    return result, markers


def restore_placeholders(text, markers):
    for marker, original in markers.items():
        text = text.replace(marker, original)
    return text


def fix_en_suffixes(text):
    """Remove English suffixes from Chinese words: 许可证d→许可证"""
    text = re.sub(r'([\u4e00-\u9fff]+)ing\b', r'\1', text)
    text = re.sub(r'([\u4e00-\u9fff]+)ed\b', r'\1', text)
    text = re.sub(r'([\u4e00-\u9fff]+)d\b', r'\1', text)
    text = re.sub(r'([\u4e00-\u9fff]+)s\b', r'\1', text)
    return text


def has_en_words(text):
    """Check if text has translatable English words left."""
    cleaned = re.sub(r'\{[^}]+\}|%[0-9$I64u|.a-z]+', '', text)
    words = re.findall(r'\b[a-zA-Z]{2,}\b', cleaned)
    for w in words:
        if w.upper() not in PROPER_NOUNS:
            return True
    # Also check for EN suffixes on CN words
    if re.search(r'[\u4e00-\u9fff]+[a-z]{2,}\b', text):
        return True
    return False


def translate(en_text):
    """Translate EN text to ZH by applying term dictionary with placeholder protection."""
    protected, markers = protect_placeholders(en_text)
    
    result = fix_en_suffixes(protected)
    
    # Apply dictionary (longest phrases first)
    for en_term, zh_term in TERMS:
        pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
        result = pattern.sub(zh_term, result)
    
    result = restore_placeholders(result, markers)
    
    # Clean up whitespace
    result = re.sub(r'\s+', ' ', result).strip()
    result = re.sub(r'\s+([，。；：、？）】\.!,;:?])', r'\1', result)
    result = re.sub(r'([（【])\s+', r'\1', result)
    result = re.sub(r'  +', ' ', result)
    
    return result


def main():
    print("=" * 60)
    print("locmsg.vmsg Translation Fix v4")
    print("=" * 60)
    
    # Backup
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"locmsg_{ts}.vmsg.bak")
    shutil.copy2(ZH_FILE, backup_path)
    print(f"\n[1/4] Backup: {backup_path}")
    
    # Parse
    print("\n[2/4] Parsing files...")
    en_entries = parse_vmsg(EN_FILE)
    zh_entries = parse_vmsg(ZH_FILE)
    
    with open(ZH_FILE, encoding='utf-8') as f:
        zh_content = f.read()
    original_content = zh_content
    
    print(f"  EN: {len(en_entries)} entries")
    print(f"  ZH: {len(zh_entries)} entries")
    
    # Analyze & Fix
    print("\n[3/4] Analyzing and fixing...")
    
    fixed = {}
    stats = {'good': 0, 'full': 0, 'partial': 0}
    
    for key, en_val in en_entries.items():
        if key not in zh_entries:
            continue
        
        zh_val = zh_entries[key]
        
        if not has_en_words(zh_val):
            stats['good'] += 1
            continue
        
        # Decide strategy based on how much Chinese is already present
        cn_ratio = chinese_ratio(zh_val)
        
        if cn_ratio < 0.15:
            # Mostly English → full retranslation from EN
            new_val = translate(en_val)
            stats['full'] += 1
        else:
            # Mostly Chinese → fix remaining English words
            new_val = translate(zh_val)
            stats['partial'] += 1
        
        if new_val != zh_val:
            fixed[key] = {'old': zh_val, 'new': new_val}
    
    print(f"  Already good: {stats['good']}")
    print(f"  Full retranslation: {stats['full']}")
    print(f"  Partial fix: {stats['partial']}")
    print(f"  Entries changed: {len(fixed)}")
    
    # Apply fixes
    print("\n[4/4] Applying fixes...")
    
    applied = 0
    skipped = 0
    for key, info in fixed.items():
        old_val = info['old']
        new_val = info['new']
        
        # Try no-spaces-around-= format first, then with spaces
        for fmt in [f'{key}="{old_val}"', f'{key} = "{old_val}"']:
            if fmt in zh_content:
                replacement = f'{key}="{new_val}"'
                if ' = "' in fmt:
                    replacement = f'{key} = "{new_val}"'
                zh_content = zh_content.replace(fmt, replacement, 1)
                applied += 1
                break
        else:
            skipped += 1
    
    # Fix comments too
    zh_content = zh_content.replace(
        'This extended exception must be used only 和 only in cases when',
        '此扩展异常应仅在以下情况下使用'
    )
    zh_content = zh_content.replace(
        'the session is already authorized 和 never use it in unauthorized sessions.',
        '会话已授权，切勿在未授权会话中使用。'
    )
    zh_content = re.sub(
        r'注意： sync with (bora/\S+)',
        r'注意：与 \1 同步',
        zh_content
    )
    
    # Write
    with open(ZH_FILE, 'w', encoding='utf-8') as f:
        f.write(zh_content)
    
    # Show samples
    print(f"\n  Applied: {applied}, Skipped: {skipped}")
    print(f"\n  Sample fixes (first 15):")
    for i, (key, info) in enumerate(list(fixed.items())[:15]):
        old_v = info['old']
        new_v = info['new']
        if old_v != new_v:
            print(f"\n  [{i+1}] {key}")
            print(f"    OLD: {old_v[:90]}")
            print(f"    NEW: {new_v[:90]}")
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Backup:       {backup_path}")
    print(f"  Total:        {len(en_entries)} entries")
    print(f"  Already good: {stats['good']}")
    print(f"  Fixed:        {len(fixed)}")
    print(f"  Applied:      {applied}")
    print(f"  Skipped:      {skipped}")
    print(f"  File changed: {zh_content != original_content}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
