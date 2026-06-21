#!/usr/bin/env python3
"""
Fix locmsg.vmsg zh-CN translation:
1. Backup original to .backup/
2. Parse EN and ZH files
3. Fix mixed Chinese-English translations using dictionary-based retranslation
4. Write fixed output to i18n/OVFTool/env/zh-CN/locmsg.vmsg

Usage: python fix_locmsg.py
"""

import os, re, sys, shutil
from datetime import datetime

EN_FILE = r"D:\vmware\i18n\OVFTool\env\en\locmsg.vmsg"
ZH_FILE = r"D:\vmware\i18n\OVFTool\env\zh-CN\locmsg.vmsg"
BACKUP_DIR = r"D:\vmware\i18n\.backup"

# ============================================================
# Comprehensive EN→ZH dictionary for common VMware terms
# ============================================================

TERM_DICT = {
    # Infrastructure
    "virtual machine": "虚拟机",
    "virtual machines": "虚拟机",
    "virtual disk": "虚拟磁盘",
    "virtual disks": "虚拟磁盘",
    "virtual device": "虚拟设备",
    "virtual switch": "虚拟交换机",
    "host bus adapter": "主机总线适配器",
    "network adapter": "网络适配器",
    "physical network adapter": "物理网络适配器",
    "vmkernel network adapter": "VMkernel 网络适配器",
    "distributed switch": "分布式交换机",
    "distributed port group": "分布式端口组",
    "resource pool": "资源池",
    "datastore": "数据存储",
    "datastores": "数据存储",
    "storage pod": "存储 Pod",
    "content library": "内容库",
    "content library item": "内容库项目",
    "fault tolerance": "容错",
    "resource profile": "资源配置文件",
    "directpath profile": "DirectPath 配置文件",
    "compute policy": "计算策略",
    "maintenance mode": "维护模式",
    "partial maintenance mode": "部分维护模式",
    "standby mode": "待机模式",
    "lockdown mode": "锁定模式",
    "power state": "电源状态",
    
    # Operations
    "power on": "打开电源",
    "powered on": "已打开电源",
    "power off": "关闭电源",
    "powered off": "已关闭电源",
    "power up": "启动",
    "power down": "关闭",
    "suspend": "挂起",
    "suspended": "已挂起",
    "suspend to memory": "挂起到内存",
    "resume": "恢复",
    "migrate": "迁移",
    "migrating": "正在迁移",
    "migrated": "已迁移",
    "migration": "迁移",
    "clone": "克隆",
    "cloned": "已克隆",
    "cloning": "正在克隆",
    "configure": "配置",
    "configured": "已配置",
    "configuring": "正在配置",
    "reconfigure": "重新配置",
    "reconfigured": "已重新配置",
    "deploy": "部署",
    "deployment": "部署",
    "deployed": "已部署",
    "attach": "附加",
    "attached": "已附加",
    "detach": "分离",
    "unbind": "解除绑定",
    "evacuate": "疏散",
    "evacuated": "已疏散",
    "evacuation": "疏散",
    "promote": "提升",
    "promoting": "正在提升",
    
    # States
    "enabled": "已启用",
    "disabled": "已禁用",
    "connected": "已连接",
    "disconnected": "已断开连接",
    "associated": "已关联",
    "registered": "已注册",
    "initialized": "已初始化",
    "installed": "已安装",
    "licensed": "已授权",
    "unlicensed": "未授权",
    "expired": "已过期",
    "reserved": "已预留",
    "removed": "已移除",
    "deleted": "已删除",
    "created": "已创建",
    "modified": "已修改",
    "updated": "已更新",
    "locked": "已锁定",
    "unlocked": "已解锁",
    "stopped": "已停止",
    "started": "已启动",
    "completed": "已完成",
    "failed": "失败",
    "valid": "有效",
    "invalid": "无效",
    "available": "可用",
    "unavailable": "不可用",
    "accessible": "可访问",
    "inaccessible": "不可访问",
    "supported": "支持",
    "unsupported": "不支持",
    "compatible": "兼容",
    "incompatible": "不兼容",
    "sufficient": "充足",
    "insufficient": "不足",
    
    # Nouns
    "host": "主机",
    "hosts": "主机",
    "cluster": "集群",
    "clusters": "集群",
    "server": "服务器",
    "service": "服务",
    "services": "服务",
    "device": "设备",
    "devices": "设备",
    "disk": "磁盘",
    "disks": "磁盘",
    "disk group": "磁盘组",
    "storage": "存储",
    "memory": "内存",
    "network": "网络",
    "networks": "网络",
    "adapter": "适配器",
    "adapters": "适配器",
    "controller": "控制器",
    "driver": "驱动程序",
    "driver s": "驱动程序",
    "port": "端口",
    "ports": "端口",
    "uplink": "上行链路",
    "uplinks": "上行链路",
    "switch": "交换机",
    "user": "用户",
    "users": "用户",
    "password": "密码",
    "account": "帐户",
    "certificate": "证书",
    "certificates": "证书",
    "key": "密钥",
    "keys": "密钥",
    "token": "令牌",
    "session": "会话",
    "profile": "配置文件",
    "profile s": "配置文件",
    "policy": "策略",
    "policies": "策略",
    "rule": "规则",
    "rules": "规则",
    "group": "组",
    "groups": "组",
    "folder": "文件夹",
    "folders": "文件夹",
    "file": "文件",
    "files": "文件",
    "directory": "目录",
    "path": "路径",
    "name": "名称",
    "names": "名称",
    "value": "值",
    "values": "值",
    "type": "类型",
    "types": "类型",
    "state": "状态",
    "status": "状态",
    "event": "事件",
    "log": "日志",
    "logs": "日志",
    "error": "错误",
    "errors": "错误",
    "warning": "警告",
    "warnings": "警告",
    "info": "信息",
    "message": "消息",
    "messages": "消息",
    "version": "版本",
    "level": "级别",
    "id": "ID",
    "id s": "ID",
    "label": "标签",
    "summary": "摘要",
    "description": "描述",
    "information": "信息",
    "configuration": "配置",
    "config": "配置",
    "property": "属性",
    "properties": "属性",
    "parameter": "参数",
    "parameters": "参数",
    "attribute": "属性",
    "attributes": "属性",
    "component": "组件",
    "components": "组件",
    "feature": "功能",
    "features": "功能",
    "function": "函数",
    "functionality": "功能",
    "capability": "能力",
    "capabilities": "能力",
    "capacity": "容量",
    "resource": "资源",
    "resources": "资源",
    "entitlement": "权利",
    "entitlements": "权利",
    "privilege": "特权",
    "privileges": "特权",
    "permission": "权限",
    "permissions": "权限",
    "authorization": "授权",
    "authentication": "身份验证",
    "security": "安全性",
    "encryption": "加密",
    "encrypted": "已加密",
    "certificate chain": "证书链",
    "namespace": "命名空间",
    "namespaces": "命名空间",
    
    # Time
    "timeout": "超时",
    "interval": "间隔",
    "retry": "重试",
    "temporary": "临时",
    "permanent": "永久",
    "current": "当前",
    "previous": "先前",
    "initial": "初始",
    "active": "活动",
    "inactive": "非活动",
    "passive": "被动",
    "witness": "见证",
    
    # Networking
    "ip address": "IP 地址",
    "ip addresses": "IP 地址",
    "subnet mask": "子网掩码",
    "default gateway": "默认网关",
    "mac address": "MAC 地址",
    "dns": "DNS",
    "dhcp": "DHCP",
    "mtu": "MTU",
    "port group": "端口组",
    "port groups": "端口组",
    "vmkernel": "VMkernel",
    "vmnic": "vmnic",
    "bandwidth": "带宽",
    "subnet": "子网",
    "subnets": "子网",
    "vlan": "VLAN",
    
    # Storage
    "partition": "分区",
    "partitions": "分区",
    "partitioning": "分区",
    "volume": "卷",
    "volumes": "卷",
    "thin provision": "精简置备",
    "thin-provisioned": "已精简置备",
    "zeroed thick": "零置备厚格式",
    "zeroed-thick": "零置备厚格式",
    "eager zeroed thick": "厚置备快速清零格式",
    "file system": "文件系统",
    "filesystem": "文件系统",
    "nfs": "NFS",
    "vmfs": "VMFS",
    "vvol": "vVol",
    "ssd": "SSD",
    "hdd": "HDD",
    "snapshot": "快照",
    "snapshots": "快照",
    "sector": "扇区",
    "sectors": "扇区",
    
    # Common verbs
    "cannot": "无法",
    "can not": "无法",
    "could not": "无法",
    "failed to": "无法",
    "unable to": "无法",
    "verify": "验证",
    "check": "检查",
    "ensure": "确保",
    "select": "选择",
    "specify": "指定",
    "specified": "已指定",
    "specifying": "正在指定",
    "provide": "提供",
    "provided": "已提供",
    "providing": "正在提供",
    "allow": "允许",
    "allowed": "允许",
    "disallow": "不允许",
    "disallowed": "不允许",
    "enable": "启用",
    "disable": "禁用",
    "process": "处理",
    "processing": "正在处理",
    "perform": "执行",
    "operation": "操作",
    "operations": "操作",
    "request": "请求",
    "requests": "请求",
    "response": "响应",
    
    # Attributes
    "maximum": "最大",
    "minimum": "最小",
    "required": "必需",
    "optional": "可选",
    "default": "默认",
    "correct": "正确",
    "incorrect": "不正确",
    "proper": "正确",
    "successful": "成功",
    "successfully": "成功",
    "generic": "一般",
    "specific": "特定",
    "duplicate": "重复",
    "conflict": "冲突",
    "conflicting": "冲突",
    "missing": "缺失",
    "empty": "为空",
    "null": "Null",
    
    # Prepositions/conjunctions
    "because": "因为",
    "between": "之间",
    "during": "期间",
    "within": "之内",
    "without": "没有",
    "through": "通过",
    "using": "使用",
    "after": "之后",
    "before": "之前",
    "according to": "根据",
    "due to": "由于",
    "as well as": "以及",
    "and/or": "和/或",
    "by": "由",
    "from": "从",
    "into": "到",
    "onto": "到",
    "with": "使用",
    "without": "没有",
    "on behalf of": "代表",
    "corresponding to": "对应",
    "based on": "基于",
    
    # VMware products
    "vcenter": "vCenter",
    "vcenter server": "vCenter Server",
    "vsphere": "vSphere",
    "vsphere replication": "vSphere Replication",
    "vsan": "vSAN",
    "nsx": "NSX",
    "vrealize": "vRealize",
    "vrealize automation": "vRealize Automation",
    "vrealize operations": "vRealize Operations",
    "vrealize orchestrator": "vRealize Orchestrator",
    "vrealize log insight": "vRealize Log Insight",
    "vrealize network insight": "vRealize Network Insight",
    "vsphere lifecycle manager": "vSphere Lifecycle Manager",
    "workspace one": "Workspace ONE",
    "vmware tools": "VMware Tools",
    "vcenter ha": "vCenter HA",
    
    # Misc
    "loading": "正在加载",
    "load": "负载",
    "overload": "过载",
    "overloaded": "过载",
    "threshold": "阈值",
    "percentage": "百分比",
    "percent": "百分比",
    "entire": "整个",
    "partial": "部分",
    "full": "完全",
    "complete": "完整",
    "incomplete": "不完整",
    "pending": "待定",
    "queued": "已排队",
    "idle": "空闲",
    "busy": "忙碌",
    "healthy": "正常",
    "unhealthy": "不正常",
    "latency": "延迟",
    "throughput": "吞吐量",
    "utilization": "利用率",
    "consumption": "消耗",
    "overhead": "开销",
    "allocation": "分配",
    "assignment": "分配",
    "corresponding": "相应的",
}

# Placeholder pattern
PLACEHOLDER_RE = re.compile(r'\{[^}]+\}|%[0-9]+(?:\$[sdIu]|[\$.|]*[0-9]*[a-z])?')

# Pattern for mixed Chinese-English (contains both Chinese chars and untranslated English words)
HAS_CHINESE = re.compile(r'[\u4e00-\u9fff]')

# Pattern to detect English suffixes on Chinese words: 许可证d, 已禁用ed, etc.
EN_SUFFIX_RE = re.compile(r'([\u4e00-\u9fff]+)([a-z]{1,4})\b', re.IGNORECASE)

# Pattern to detect "English(Chinese)English" mixing within words
MIXED_WORD_RE = re.compile(r'(\b[a-zA-Z]{2,}\s*)([\u4e00-\u9fff]+\s*[a-zA-Z]{2,})')


def parse_vmsg(filepath):
    """Parse a .vmsg file into a dict of key->value and preserve comments/blank lines."""
    entries = {}
    lines = []
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines but preserve structure
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        # Skip comments, blank lines, and signature line
        if not line_stripped or line_stripped.startswith('#') or line_stripped.startswith('signature'):
            continue
        
        # Parse key = "value"
        # Handle both formats: key = "value" and key="value"
        m = re.match(r'^([a-zA-Z0-9_.]+)\s*=\s*"(.+)"\s*$', line_stripped)
        if m:
            key = m.group(1)
            value = m.group(2)
            entries[key] = {
                'value': value,
                'line_idx': i,
                'raw_line': line
            }
    
    return entries, lines


def has_untranslated_english(text):
    """Check if text has untranslated English words mixed with Chinese."""
    if not HAS_CHINESE.search(text):
        return False
    
    # Remove placeholders
    cleaned = PLACEHOLDER_RE.sub('', text)
    
    # Remove common English fragments that should remain (protocols, product names, technical terms)
    # Check for standalone English words mixed with Chinese
    eng_words = re.findall(r'\b[a-zA-Z]{3,}\b', cleaned)
    if not eng_words:
        return False
    
    # Filter out known proper nouns / abbreviations that should stay English
    keep_english = {
        'API', 'CPU', 'RAM', 'IP', 'DNS', 'DHCP', 'HTTP', 'HTTPS', 'SSH', 'SSL',
        'TCP', 'UDP', 'NFS', 'VMFS', 'vSAN', 'vSphere', 'NSX', 'vCenter', 'VLAN',
        'PCI', 'USB', 'SCSI', 'NVMe', 'RDMA', 'HBA', 'NIC', 'MAC', 'UUID', 'BIOS',
        'GUID', 'PNID', 'PNIC', 'VMKernel', 'VMkernel', 'VMIOP', 'DVS', 'DVSwitch',
        'DPU', 'OCM', 'NPIV', 'VOB', 'HCI', 'VLCM', 'HPP', 'IOPS', 'SRM', 'VR',
        'FT', 'HA', 'DRS', 'EVC', 'SDRS', 'DPM', 'IORM', 'SIOC', 'VCF', 'VASA',
        'VVol', 'vVol', 'FCD', 'CBT', 'TPM', 'SEV', 'SGX', 'TDX', 'NVDIMM',
        'PXE', 'EFI', 'VGA', 'ROM', 'AHCI', 'NVME', 'NVMe', 'PVSCSI',
        'SATA', 'SAS', 'FCoE', 'iSCSI', 'VXLAN', 'VXNET', 'E1000',
        'OVF', 'OVA', 'VMDK', 'VMX', 'VMSD', 'VMSN', 'VMSS',
        'RDM', 'RDMA', 'VIB', 'ESX', 'ESXi', 'VCSA', 'PSC',
        'VCHA', 'VCLS', 'CCPE', 'VMRP', 'DPP', 'CDRS', 'VTC', 'FLB',
        'VDTC', 'VAPI', 'VAPI', 'OSFS', 'CLOM', 'DOM', 'VOB',
        'GSS', 'KB', 'DB', 'SMTP', 'LWD', 'VMIOP', 'SR_IOV',
        'VNC', 'RDP', 'LDAP', 'KMS', 'JWT', 'REST', 'SOAP',
        'JSON', 'XML', 'HTML', 'PNG', 'PDF', 'SVG', 'WWN',
        'SLOT', 'VC', 'VPXD', 'HOSTD', 'VPX', 'VIM',
        'FIXED', 'RR', 'LB', 'NAS',
        'VM', 'VMs', 'FQDN', 'IO', 'I/O',
    }
    
    filtered = [w for w in eng_words if w.upper() not in keep_english]
    
    return len(filtered) > 0


def fix_english_suffixes(text):
    """Fix English suffixes attached to Chinese words: 许可证d -> 许可证, 已启用ing -> 已启用"""
    # Common suffix mappings
    suffix_fixes = {
        'd': '',       # past tense: 许可证d -> 许可证
        'ed': '',      # past tense: 配置ed -> 配置
        'ing': '',     # progressive: 正在处理ing -> 正在处理
        's': '',       # plural: 用户s -> 用户
        'er': '程序',   # agent noun: 管理er -> 管理器
        'ion': '',     # 分区ion -> 分区 (already has Chinese)
        'ment': '',    # 部署ment -> 部署
        'tion': '',    # 操作tion -> 操作
        'or': '',      # 编辑or -> 编辑器
    }
    
    # First pass: remove known English suffixes from Chinese words
    for suffix, replacement in sorted(suffix_fixes.items(), key=lambda x: -len(x[0])):
        text = re.sub(
            rf'([\u4e00-\u9fff]+)({suffix})\b',
            lambda m: m.group(1) + replacement,
            text
        )
    
    return text


def retranslate_value(en_value, zh_value):
    """
    Attempt to retranslate a mixed Chinese-English value into proper Chinese.
    1. Fix English suffixes
    2. Replace known EN terms with ZH equivalents
    3. Fix remaining English words
    """
    # Step 1: Fix English suffixes
    result = fix_english_suffixes(zh_value)
    
    # Step 2: For terms that are still mixed, apply dictionary replacement
    # We need to be careful not to break placeholders
    if has_untranslated_english(result):
        # Split into parts: text and placeholders
        parts = PLACEHOLDER_RE.split(result)
        placeholders = PLACEHOLDER_RE.findall(result)
        
        new_parts = []
        for part in parts:
            if HAS_CHINESE.search(part) or part.strip():
                # Apply dictionary to this part (case-insensitive)
                new_part = part
                # Build a regex pattern from dictionary (longest first)
                for en_term, zh_term in sorted(TERM_DICT.items(), key=lambda x: -len(x[0])):
                    # Word boundary matching
                    pattern = re.compile(
                        r'\b' + re.escape(en_term) + r'\b',
                        re.IGNORECASE
                    )
                    new_part = pattern.sub(zh_term, new_part)
                new_parts.append(new_part)
            else:
                new_parts.append(part)
        
        # Reassemble with placeholders
        result = ''
        for i, part in enumerate(new_parts):
            result += part
            if i < len(placeholders):
                result += placeholders[i]
    
    # Step 3: Clean up extra spaces
    result = re.sub(r'\s+', ' ', result)
    result = result.strip()
    
    # Step 4: Fix common issues
    # Remove spaces before Chinese punctuation
    result = re.sub(r'\s+([，。；：？、）】])', r'\1', result)
    result = re.sub(r'([（【])\s+', r'\1', result)
    
    # Fix double spaces
    result = re.sub(r'  ', ' ', result)
    
    return result


def main():
    print("=" * 60)
    print("locmsg.vmsg Translation Fix Script")
    print("=" * 60)
    
    # === Step 1: Backup ===
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"locmsg_{timestamp}.vmsg.bak")
    shutil.copy2(ZH_FILE, backup_file)
    print(f"\n[1/4] Backup created: {backup_file}")
    
    # === Step 2: Parse files ===
    print("\n[2/4] Parsing EN and ZH files...")
    en_entries, en_lines = parse_vmsg(EN_FILE)
    zh_entries, zh_lines = parse_vmsg(ZH_FILE)
    
    print(f"  EN entries: {len(en_entries)}")
    print(f"  ZH entries: {len(zh_entries)}")
    
    # === Step 3: Analyze and fix ===
    print("\n[3/4] Analyzing and fixing translations...")
    
    fixes = {}
    mixed_count = 0
    suffix_fix_count = 0
    total_fixed = 0
    
    # Read the full ZH file content
    with open(ZH_FILE, encoding='utf-8') as f:
        zh_content = f.read()
    
    original_content = zh_content
    
    # Process each entry
    for key, en_info in en_entries.items():
        en_value = en_info['value']
        
        if key not in zh_entries:
            print(f"  MISSING in ZH: {key}")
            continue
        
        zh_value = zh_entries[key]['value']
        
        # Skip entries that are already proper Chinese (no English words)
        if not has_untranslated_english(zh_value):
            continue
        
        mixed_count += 1
        
        # Retranslate
        new_value = retranslate_value(en_value, zh_value)
        
        if new_value and new_value != zh_value:
            fixes[key] = {
                'old': zh_value,
                'new': new_value
            }
            total_fixed += 1
    
    print(f"\n  Entries with mixed EN/ZH: {mixed_count}")
    print(f"  Entries fixed: {total_fixed}")
    
    # === Step 4: Apply fixes ===
    print("\n[4/4] Applying fixes...")
    
    fixed_count = 0
    for key, fix_info in fixes.items():
        old_value = fix_info['old']
        new_value = fix_info['new']
        
        # Find the exact line in the ZH file
        # Need to handle both formats: key="value" and key = "value"
        # The ZH file uses format: key="value"
        old_pattern = f'{key}="{old_value}"'
        new_pattern = f'{key}="{new_value}"'
        
        if old_pattern in zh_content:
            zh_content = zh_content.replace(old_pattern, new_pattern, 1)
            fixed_count += 1
            if fixed_count <= 10:
                print(f"  [{fixed_count}] {key}")
                print(f"    OLD: {old_value[:80]}...")
                print(f"    NEW: {new_value[:80]}...")
        else:
            # Try with spaces around =
            old_pattern2 = f'{key} = "{old_value}"'
            new_pattern2 = f'{key} = "{new_value}"'
            if old_pattern2 in zh_content:
                zh_content = zh_content.replace(old_pattern2, new_pattern2, 1)
                fixed_count += 1
            else:
                print(f"  CANNOT FIND: {key}")
    
    # === Also fix comments in Chinese ===
    # Fix "注意：" comments that still have English
    zh_content = zh_content.replace(
        'This extended exception must be used only 和 only in cases when',
        '此扩展异常应仅在以下情况下使用'
    )
    zh_content = zh_content.replace(
        'the session is already authorized 和 never use it in unauthorized sessions.',
        '会话已授权，切勿在未授权会话中使用。'
    )
    
    # Fix NOTE comments
    zh_content = zh_content.replace(
        '注意： sync with bora/vim/lib/esxtoken/TokenHandler.cpp',
        '注意：与 bora/vim/lib/esxtoken/TokenHandler.cpp 同步'
    )
    zh_content = zh_content.replace(
        '注意： sync with bora/apps/esxtokend/vapi/messageResolver.cpp',
        '注意：与 bora/apps/esxtokend/vapi/messageResolver.cpp 同步'
    )
    zh_content = zh_content.replace(
        '注意： sync with bora/apps/kmxa/vapi/messageResolver.cpp',
        '注意：与 bora/apps/kmxa/vapi/messageResolver.cpp 同步'
    )
    zh_content = zh_content.replace(
        '注意： sync with bora/apps/kmxd/vapi/messageResolver.cpp',
        '注意：与 bora/apps/kmxd/vapi/messageResolver.cpp 同步'
    )
    zh_content = zh_content.replace(
        '注意： sync with bora/apps/attestd/vapi/messageResolver.cpp',
        '注意：与 bora/apps/attestd/vapi/messageResolver.cpp 同步'
    )
    zh_content = zh_content.replace(
        '注意： sync with bora/apps/attestd/vapi/statusImpl.cpp',
        '注意：与 bora/apps/attestd/vapi/statusImpl.cpp 同步'
    )
    
    # Write fixed content
    with open(ZH_FILE, 'w', encoding='utf-8') as f:
        f.write(zh_content)
    
    changes = zh_content != original_content
    print(f"\n  Total replacements made: {fixed_count}")
    print(f"  Content changed: {changes}")
    
    # === Summary ===
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Backup:      {backup_file}")
    print(f"  Output:      {ZH_FILE}")
    print(f"  Mixed EN/ZH: {mixed_count}")
    print(f"  Fixed:       {total_fixed}")
    print(f"  Applied:     {fixed_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
