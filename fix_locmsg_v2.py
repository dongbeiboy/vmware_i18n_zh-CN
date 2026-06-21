#!/usr/bin/env python3
"""
locmsg.vmsg zh-CN Translation Fix v2

Two strategies:
1. For entries that are mostly Chinese (>30% Chinese chars) with some English words:
   - Fix English suffixes, then replace known EN terms with ZH equivalents
2. For entries that are mostly English (<30% Chinese chars):
   - Apply FULL retranslation from EN source using comprehensive dictionary

Usage: python fix_locmsg_v2.py
"""

import os, re, shutil
from datetime import datetime

EN_FILE = r"D:\vmware\i18n\OVFTool\env\en\locmsg.vmsg"
ZH_FILE = r"D:\vmware\i18n\OVFTool\env\zh-CN\locmsg.vmsg"
BACKUP_DIR = r"D:\vmware\i18n\.backup"

# ============================================================
# TERM DICTIONARY
# ============================================================
TERMS = {
    # Determiners / articles
    "the": "",
    "a": "",
    "an": "",
    "this": "此",
    "these": "这些",
    "that": "该",
    "those": "那些",
    "its": "其",
    "their": "其",
    "your": "您的",
    "some": "某些",
    "any": "任何",
    "all": "所有",
    "both": "两者",
    "each": "每个",
    "every": "每个",
    "no": "无",
    "other": "其他",
    "another": "另一",
    "such": "此类",
    "multiple": "多个",
    "various": "各种",
    "certain": "特定",
    "following": "以下",
    "specified": "指定",
    "given": "给定",
    "existing": "现有",
    "current": "当前",
    "previous": "先前",
    "original": "原始",
    "additional": "额外",
    
    # Prepositions (context-dependent, handle carefully)
    "of": "的",
    "in": "在",
    "on": "在",
    "at": "在",
    "to": "到",
    "for": "对于",
    "by": "由",
    "from": "从",
    "with": "使用",
    "without": "没有",
    "through": "通过",
    "via": "通过",
    "between": "之间",
    "among": "之中",
    "within": "之内",
    "into": "到",
    "onto": "到",
    "upon": "在",
    "during": "期间",
    "since": "自",
    "until": "直到",
    "after": "之后",
    "before": "之前",
    "behind": "之后",
    "above": "以上",
    "below": "以下",
    "under": "下",
    "over": "超过",
    "across": "跨",
    "against": "针对",
    "according to": "根据",
    "based on": "基于",
    "due to": "由于",
    "except": "除",
    "including": "包括",
    "regarding": "关于",
    "as": "作为",
    "as well as": "以及",
    
    # Conjunctions
    "and": "和",
    "or": "或",
    "but": "但",
    "if": "如果",
    "then": "则",
    "else": "否则",
    "so": "因此",
    "because": "因为",
    "though": "虽然",
    "while": "同时",
    "when": "时",
    "where": "其中",
    "whether": "是否",
    "unless": "除非",
    "once": "一旦",
    "that is": "即",
    "i.e.": "即",
    
    # Common verbs - be
    "is": "",
    "are": "",
    "was": "",
    "were": "",
    "be": "",
    "been": "",
    "being": "",
    "has": "",
    "have": "",
    "had": "",
    "do": "",
    "does": "",
    "did": "",
    "done": "",
    "doing": "",
    "will": "将",
    "would": "会",
    "should": "应",
    "could": "可以",
    "may": "可能",
    "might": "可能",
    "can": "可以",
    "shall": "应",
    "must": "必须",
    "need": "需要",
    "need to": "需要",
    "needs to": "需要",
    "want": "需要",
    "used": "使用",
    "use": "使用",
    "using": "使用",
    "set": "设置",
    "setting": "正在设置",
    "sets": "设置",
    "make": "使",
    "makes": "使",
    "making": "正在使",
    "keep": "保持",
    "keeps": "保持",
    "keeping": "正在保持",
    "take": "执行",
    "takes": "执行",
    "taking": "正在执行",
    "cause": "导致",
    "causes": "导致",
    "caused": "导致",
    "causing": "导致",
    "occur": "发生",
    "occurs": "发生",
    "occurred": "发生",
    "occurring": "发生",
    "appear": "出现",
    "appears": "出现",
    "appeared": "出现",
    "exist": "存在",
    "exists": "存在",
    "existed": "存在",
    "result": "结果",
    "results": "结果",
    "resulted": "导致",
    "indicate": "表示",
    "indicates": "表示",
    "indicated": "表示",
    "contain": "包含",
    "contains": "包含",
    "containing": "包含",
    "include": "包括",
    "includes": "包括",
    "including": "包括",
    "require": "需要",
    "requires": "需要",
    "required": "需要",
    "requiring": "需要",
    "correspond": "对应",
    "corresponds": "对应",
    "corresponding": "对应",
    
    # Negatives
    "not": "不",
    "no": "无",
    "non": "非",
    "none": "无",
    "nothing": "无",
    "never": "从不",
    "neither": "也不",
    "nor": "也不",
    "cannot": "无法",
    "can not": "无法",
    "could not": "无法",
    "will not": "将不",
    "won't": "将不",
    "don't": "不",
    "doesn't": "不",
    "didn't": "未",
    "isn't": "不",
    "aren't": "不",
    "wasn't": "未",
    "weren't": "未",
    "hasn't": "未",
    "haven't": "未",
    "hadn't": "未",
    "must not": "不得",
    "should not": "不应",
    "may not": "可能不",
    "failed to": "无法",
    "fail to": "无法",
    "fails to": "无法",
    "unable to": "无法",
    
    # Question words
    "what": "什么",
    "which": "哪个",
    "who": "谁",
    "whom": "谁",
    "whose": "谁的",
    "why": "为什么",
    "how": "如何",
    "when": "何时",
    "where": "何处",
    
    # Quantifiers
    "many": "许多",
    "much": "许多",
    "few": "很少",
    "little": "很少",
    "more": "更多",
    "most": "最多",
    "less": "更少",
    "least": "最少",
    "enough": "足够",
    "plenty": "充足",
    "sufficient": "充足",
    "insufficient": "不足",
    "excessive": "过多",
    "extra": "额外",
    "additional": "额外",
    
    # VMware infrastructure
    "virtual machine": "虚拟机",
    "virtual machines": "虚拟机",
    "virtual disk": "虚拟磁盘",
    "virtual disks": "虚拟磁盘",
    "virtual device": "虚拟设备",
    "virtual switch": "虚拟交换机",
    "virtual switches": "虚拟交换机",
    "host bus adapter": "主机总线适配器",
    "network adapter": "网络适配器",
    "network adapters": "网络适配器",
    "physical network adapter": "物理网络适配器",
    "physical adapters": "物理适配器",
    "vmkernel network adapter": "VMkernel 网络适配器",
    "distributed switch": "分布式交换机",
    "distributed port group": "分布式端口组",
    "distributed port groups": "分布式端口组",
    "resource pool": "资源池",
    "resource pools": "资源池",
    "datastore": "数据存储",
    "datastores": "数据存储",
    "data store": "数据存储",
    "data stores": "数据存储",
    "storage pod": "存储 Pod",
    "content library": "内容库",
    "content library item": "内容库项目",
    "fault tolerance": "容错",
    "resource profile": "资源配置文件",
    "resource profiles": "资源配置文件",
    "vm resource profile": "VM 资源配置文件",
    "compute policy": "计算策略",
    "maintenance mode": "维护模式",
    "standby mode": "待机模式",
    "lockdown mode": "锁定模式",
    "power state": "电源状态",
    "cluster": "集群",
    "clusters": "集群",
    "host": "主机",
    "hosts": "主机",
    "server": "服务器",
    "servers": "服务器",
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
    "port": "端口",
    "ports": "端口",
    "uplink": "上行链路",
    "uplinks": "上行链路",
    "user": "用户",
    "users": "用户",
    "username": "用户名",
    "password": "密码",
    "account": "帐户",
    "certificate": "证书",
    "certificates": "证书",
    "key": "密钥",
    "keys": "密钥",
    "token": "令牌",
    "session": "会话",
    "sessions": "会话",
    "profile": "配置文件",
    "profile s": "配置文件",
    "policy": "策略",
    "policies": "策略",
    "rule": "规则",
    "folder": "文件夹",
    "folders": "文件夹",
    "file": "文件",
    "files": "文件",
    "directory": "目录",
    "directories": "目录",
    "path": "路径",
    "paths": "路径",
    "name": "名称",
    "names": "名称",
    "value": "值",
    "values": "值",
    "type": "类型",
    "state": "状态",
    "status": "状态",
    "statuses": "状态",
    "log": "日志",
    "logs": "日志",
    "event": "事件",
    "events": "事件",
    "error": "错误",
    "errors": "错误",
    "warning": "警告",
    "warnings": "警告",
    "info": "信息",
    "message": "消息",
    "messages": "消息",
    "version": "版本",
    "config": "配置",
    "configuration": "配置",
    "configurations": "配置",
    "property": "属性",
    "properties": "属性",
    "parameter": "参数",
    "parameters": "参数",
    "attribute": "属性",
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
    "privilege": "特权",
    "privileges": "特权",
    "permission": "权限",
    "permissions": "权限",
    "lockdown": "锁定",
    "encryption": "加密",
    "encrypted": "已加密",
    "namespace": "命名空间",
    "namespaces": "命名空间",
    "partition": "分区",
    "partitions": "分区",
    "partitioning": "分区",
    "volume": "卷",
    "volumes": "卷",
    "thin provision": "精简置备",
    "thin-provisioned": "已精简置备",
    "zeroed thick": "零置备厚格式",
    "zeroed-thick": "零置备厚格式",
    "file system": "文件系统",
    "filesystem": "文件系统",
    "snapshot": "快照",
    "snapshots": "快照",
    "sector": "扇区",
    "sectors": "扇区",
    "provider": "提供程序",
    "providers": "提供程序",
    "adapter": "适配器",
    "adapters": "适配器",
    "controller": "控制器",
    "port group": "端口组",
    
    # States / adjectives
    "enabled": "已启用",
    "disabled": "已禁用",
    "connected": "已连接",
    "disconnected": "已断开连接",
    "associated": "已关联",
    "registered": "已注册",
    "unregistered": "已注销",
    "initialized": "已初始化",
    "installed": "已安装",
    "licensed": "已授权",
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
    "finished": "已完成",
    "succeeded": "已成功",
    "failed": "失败",
    "successful": "成功",
    "successfully": "成功",
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
    "correct": "正确",
    "incorrect": "不正确",
    "proper": "正确",
    "maximum": "最大",
    "minimum": "最小",
    "optimal": "最佳",
    "normal": "正常",
    "abnormal": "异常",
    "active": "活动",
    "inactive": "非活动",
    "passive": "被动",
    "unused": "未使用",
    "unknown": "未知",
    "pending": "待定",
    "queued": "已排队",
    
    # Verbs
    "allow": "允许",
    "allows": "允许",
    "allowed": "允许",
    "disallow": "不允许",
    "disallowed": "不允许",
    "enable": "启用",
    "disables": "禁用",
    "disable": "禁用",
    "enables": "启用",
    "enabling": "正在启用",
    "disabling": "正在禁用",
    "process": "处理",
    "processes": "处理",
    "processed": "已处理",
    "performing": "正在执行",
    "perform": "执行",
    "performs": "执行",
    "perform ed": "执行",
    "performed": "已执行",
    "request": "请求",
    "requested": "已请求",
    "requests": "请求",
    "response": "响应",
    "respond": "响应",
    "verify": "验证",
    "verifies": "验证",
    "verified": "已验证",
    "check": "检查",
    "checks": "检查",
    "checked": "已检查",
    "ensure": "确保",
    "ensures": "确保",
    "ensured": "已确保",
    "select": "选择",
    "selects": "选择",
    "selected": "已选择",
    "specify": "指定",
    "specifies": "指定",
    "specified": "指定",
    "specifying": "正在指定",
    "provide": "提供",
    "provides": "提供",
    "provided": "提供",
    "providing": "正在提供",
    "configure": "配置",
    "configures": "配置",
    "configured": "已配置",
    "configuring": "正在配置",
    "reconfigure": "重新配置",
    "reconfigured": "已重新配置",
    "deploy": "部署",
    "deployed": "已部署",
    "deploying": "正在部署",
    "deployment": "部署",
    "migrate": "迁移",
    "migrates": "迁移",
    "migrated": "已迁移",
    "migrating": "正在迁移",
    "migration": "迁移",
    "clone": "克隆",
    "clones": "克隆",
    "cloned": "已克隆",
    "cloning": "正在克隆",
    "attach": "附加",
    "attaches": "附加",
    "attached": "已附加",
    "attaching": "正在附加",
    "detach": "分离",
    "detached": "已分离",
    "remove": "移除",
    "removes": "移除",
    "removing": "正在移除",
    "add": "添加",
    "adds": "添加",
    "adding": "正在添加",
    "update": "更新",
    "updates": "更新",
    "updating": "正在更新",
    "modify": "修改",
    "modifies": "修改",
    "modifying": "正在修改",
    "delete": "删除",
    "deletes": "删除",
    "deleting": "正在删除",
    "create": "创建",
    "creates": "创建",
    "creating": "正在创建",
    "rename": "重命名",
    "renames": "重命名",
    "renaming": "正在重命名",
    "move": "移动",
    "moves": "移动",
    "moving": "正在移动",
    "import": "导入",
    "imports": "导入",
    "export": "导出",
    "exports": "导出",
    "generate": "生成",
    "generates": "生成",
    "generated": "已生成",
    "generating": "正在生成",
    "synchronize": "同步",
    "synchronized": "已同步",
    "cleaning up": "正在清理",
    "clean up": "清理",
    "restart": "重新启动",
    "restarts": "重新启动",
    "restarting": "正在重新启动",
    "reboot": "重新引导",
    "reboots": "重新引导",
    "power on": "打开电源",
    "powered on": "已打开电源",
    "power off": "关闭电源",
    "powered off": "已关闭电源",
    "power up": "启动",
    "power down": "关闭",
    "suspend": "挂起",
    "suspended": "已挂起",
    "suspending": "正在挂起",
    "resume": "恢复",
    "resumed": "已恢复",
    
    # Time
    "timeout": "超时",
    "timed out": "超时",
    "interval": "间隔",
    "retry": "重试",
    "retries": "重试",
    "retrying": "正在重试",
    "temporary": "临时",
    "temporarily": "临时",
    "permanent": "永久",
    "permanently": "永久",
    "duration": "持续时间",
    "frequency": "频率",
    "delay": "延迟",
    "latency": "延迟",
    
    # Networking
    "ip address": "IP 地址",
    "subnet mask": "子网掩码",
    "default gateway": "默认网关",
    "mac address": "MAC 地址",
    "bandwidth": "带宽",
    "subnet": "子网",
    
    # Storage
    "nfs": "NFS",
    "vmfs": "VMFS",
    "vvol": "vVol",
    "ssd": "SSD",
    "disk space": "磁盘空间",
    "free space": "可用空间",
    "free space": "可用空间",
    
    # Common longer phrases
    "operation": "操作",
    "operations": "操作",
    "support": "支持",
    "issue": "问题",
    "issues": "问题",
    "problem": "问题",
    "problems": "问题",
    "reason": "原因",
    "reasons": "原因",
    "condition": "条件",
    "conditions": "条件",
    "context": "上下文",
    "scenario": "场景",
    "scenarios": "场景",
    "workload": "工作负载",
    "workloads": "工作负载",
    "attempt": "尝试",
    "attempts": "尝试",
    "attempted": "已尝试",
    "remediation": "补救",
    "diagnostics": "诊断",
    "details": "详细信息",
    "detail": "详细信息",
    
    # VMware products
    "vcenter server": "vCenter Server",
    "vcenter": "vCenter",
    "vsphere replication": "vSphere 复制",
    "vsphere": "vSphere",
    "vsan": "vSAN",
    "nsx": "NSX",
    "esxi": "ESXi",
    "vmware tools": "VMware Tools",
    "vcenter ha": "vCenter HA",
    
    # Misc common words
    "information": "信息",
    "description": "描述",
    "label": "标签",
    "summary": "摘要",
    "id": "ID",
    "number": "数量",
    "numbers": "数量",
    "count": "计数",
    "total": "总计",
    "amount": "数量",
    "size": "大小",
    "length": "长度",
    "limit": "限制",
    "limits": "限制",
    "limit ed": "限制",
    "threshold": "阈值",
    "level": "级别",
    "levels": "级别",
    "priority": "优先级",
    "action": "操作",
    "actions": "操作",
    "task": "任务",
    "tasks": "任务",
    "process": "进程",
    "processes": "进程",
    "thread": "线程",
    "threads": "线程",
    "method": "方法",
    "methods": "方法",
    "mode": "模式",
    "modes": "模式",
    "option": "选项",
    "options": "选项",
    "setting": "设置",
    "settings": "设置",
    "criteria": "条件",
    "format": "格式",
    "formats": "格式",
    "pattern": "模式",
    "patterns": "模式",
    "tag": "标签",
    "tags": "标签",
    "role": "角色",
    "roles": "角色",
    "entity": "实体",
    "entities": "实体",
    "object": "对象",
    "objects": "对象",
    "target": "目标",
    "source": "源",
    "destination": "目标",
    "origin": "来源",
    "input": "输入",
    "output": "输出",
    
    # Verbs related to operations
    "initialize": "初始化",
    "initializes": "初始化",
    "initializing": "正在初始化",
    "terminate": "终止",
    "terminates": "终止",
    "terminated": "已终止",
    "terminating": "正在终止",
    "abort": "中止",
    "aborted": "已中止",
    "aborting": "正在中止",
    "cancel": "取消",
    "cancels": "取消",
    "canceled": "已取消",
    "cancelled": "已取消",
    "canceling": "正在取消",
    "cancelling": "正在取消",
    "interrupt": "中断",
    "interrupted": "已中断",
    "interrupting": "正在中断",
    "pause": "暂停",
    "paused": "已暂停",
    "pausing": "正在暂停",
    "recover": "恢复",
    "recovered": "已恢复",
    "recovering": "正在恢复",
    "resolve": "解决",
    "resolved": "已解决",
    "resolving": "正在解决",
    "allocate": "分配",
    "allocated": "已分配",
    "allocating": "正在分配",
    "release": "释放",
    "released": "已释放",
    "releasing": "正在释放",
    "assign": "分配",
    "assigns": "分配",
    "assigned": "已分配",
    "assigning": "正在分配",
    "consume": "消耗",
    "consumes": "消耗",
    "consumed": "已消耗",
    "consuming": "正在消耗",
    "exceed": "超过",
    "exceeds": "超过",
    "exceeded": "已超过",
    "exceeding": "超过",
    "increase": "增加",
    "increases": "增加",
    "increased": "已增加",
    "increasing": "正在增加",
    "decrease": "减少",
    "decreases": "减少",
    "decreased": "已减少",
    "decreasing": "正在减少",
    "reduce": "减少",
    "reduces": "减少",
    "reduced": "已减少",
    "reducing": "正在减少",
    "extend": "扩展",
    "extends": "扩展",
    "extended": "已扩展",
    "extending": "正在扩展",
    "expand": "展开",
    "expands": "展开",
    "expanded": "已展开",
    "expanding": "正在展开",
    "upgrade": "升级",
    "upgrades": "升级",
    "upgraded": "已升级",
    "upgrading": "正在升级",
    "convert": "转换",
    "converts": "转换",
    "converted": "已转换",
    "converting": "正在转换",
    "transfer": "传输",
    "transfers": "传输",
    "transferred": "已传输",
    "transferring": "正在传输",
    "transform": "转换",
    "transforms": "转换",
    "transformed": "已转换",
    "transforming": "正在转换",
    "mount": "挂载",
    "mounts": "挂载",
    "mounted": "已挂载",
    "unmount": "卸载",
    "unmounts": "卸载",
    "unmounted": "已卸载",
    "load": "加载",
    "loads": "加载",
    "loaded": "已加载",
    "loading": "正在加载",
    "unload": "卸载",
    "unloads": "卸载",
    "unloaded": "已卸载",
    "unloading": "正在卸载",
    "wait": "等待",
    "waits": "等待",
    "waited": "已等待",
    "waiting": "正在等待",
    "match": "匹配",
    "matches": "匹配",
    "matched": "已匹配",
    "matching": "正在匹配",
    "compare": "比较",
    "compares": "比较",
    "compared": "已比较",
    "comparing": "正在比较",
    "detect": "检测",
    "detects": "检测",
    "detected": "已检测",
    "detecting": "正在检测",
    "identify": "标识",
    "identifies": "标识",
    "identified": "已标识",
    "identifying": "正在标识",
    "obtain": "获取",
    "obtains": "获取",
    "obtained": "已获取",
    "obtaining": "正在获取",
    "receive": "接收",
    "receives": "接收",
    "received": "已接收",
    "receiving": "正在接收",
    "send": "发送",
    "sends": "发送",
    "sent": "已发送",
    "sending": "正在发送",
    "submit": "提交",
    "submits": "提交",
    "submitted": "已提交",
    "submitting": "正在提交",
    "return": "返回",
    "returns": "返回",
    "returned": "已返回",
    "returning": "正在返回",
    "display": "显示",
    "displays": "显示",
    "displayed": "已显示",
    "displaying": "正在显示",
    "show": "显示",
    "shows": "显示",
    "showing": "正在显示",
    "hide": "隐藏",
    "hides": "隐藏",
    "hidden": "已隐藏",
    "hiding": "正在隐藏",
    "override": "覆盖",
    "overrides": "覆盖",
    "overridden": "已覆盖",
    "overriding": "正在覆盖",
    "overwrite": "覆盖",
    "overwrites": "覆盖",
    "overwritten": "已覆盖",
    "overwriting": "正在覆盖",
    "reset": "重置",
    "resets": "重置",
    "resetting": "正在重置",
    "refresh": "刷新",
    "refreshes": "刷新",
    "refreshed": "已刷新",
    "refreshing": "正在刷新",
    "clear": "清除",
    "clears": "清除",
    "cleared": "已清除",
    "clearing": "正在清除",
    "confirm": "确认",
    "confirms": "确认",
    "confirmed": "已确认",
    "confirming": "正在确认",
    "save": "保存",
    "saves": "保存",
    "saved": "已保存",
    "saving": "正在保存",
    "store": "存储",
    "stores": "存储",
    "stored": "已存储",
    "storing": "正在存储",
    "restore": "还原",
    "restores": "还原",
    "restored": "已还原",
    "restoring": "正在还原",
    "discover": "发现",
    "discovers": "发现",
    "discovered": "已发现",
    "discovering": "正在发现",
    "enumerate": "枚举",
    "enumerates": "枚举",
    "enumerated": "已枚举",
    "enumerating": "正在枚举",
    "register": "注册",
    "registers": "注册",
    "registered": "已注册",
    "registering": "正在注册",
    "unregister": "注销",
    "unregisters": "注销",
    "unregistered": "已注销",
    "unregistering": "正在注销",
    "subscribe": "订阅",
    "subscribes": "订阅",
    "subscribed": "已订阅",
    "subscribing": "正在订阅",
    "unsubscribe": "取消订阅",
    "unsubscribes": "取消订阅",
    "unsubscribed": "已取消订阅",
    "unsubscribing": "正在取消订阅",
    "publish": "发布",
    "publishes": "发布",
    "published": "已发布",
    "publishing": "正在发布",
    "install": "安装",
    "installs": "安装",
    "installed": "已安装",
    "installing": "正在安装",
    "uninstall": "卸载",
    "uninstalls": "卸载",
    "uninstalled": "已卸载",
    "uninstalling": "正在卸载",
    "apply": "应用",
    "applies": "应用",
    "applied": "已应用",
    "applying": "正在应用",
    "execute": "执行",
    "executes": "执行",
    "executed": "已执行",
    "executing": "正在执行",
    "read": "读取",
    "reads": "读取",
    "readable": "可读取",
    "write": "写入",
    "writes": "写入",
    "writable": "可写入",
    "written": "已写入",
    "writing": "正在写入",
}

# English suffixes that cling to Chinese words
EN_SUFFIX_MAP = {
    'ing': '',
    's': '',
    'd': '',
    'ed': '',
    'tion': '',
    'ment': '',
    'er': '程序',
    'or': '',
    'ity': '',
    'al': '',
    'ive': '',
    'able': '',
    'ible': '',
}

# English-only entries that are simple/short and should be fully translated
SIMPLE_EN_TRANSLATIONS = {
    "FIXED": "固定",
    "LB-RR": "LB-RR",
    "LB-IOPS": "LB-IOPS",
    "LB-BYTES": "LB-BYTES",
    "LB-Latency": "LB-延迟",
    "Preferred path": "首选路径",
    "Preferred path for I/Os.": "I/O 的首选路径。",
    "IOPS": "IOPS",
    "I/O count for path switch.": "路径切换的 I/O 计数。",
    "Bytes": "字节",
    "Byte count for path switch.": "路径切换的字节计数。",
    "Latency evaluation time": "延迟评估时间",
    "Latency evaluation interval on the paths.": "路径上的延迟评估间隔。",
    "Sampling I/Os per path": "每条路径的采样 I/O 数",
    "Sample I/Os to be issued on path to calculate latency.": "在路径上发出以计算延迟的示例 I/O。",
    "Select fixed path for I/Os.": "为 I/O 选择固定路径。",
    "Select paths in round-robin fashion for I/Os.": "以轮循方式为 I/O 选择路径。",
    "Select path having least outstanding I/Os.": "选择具有最少未完成 I/O 的路径。",
    "Select path having least outstanding bytes.": "选择具有最少未完成字节数的路径。",
    "Select path having least latency.": "选择延迟最小的路径。",
    "Unknown entity: {entity}.": "未知实体：{entity}。",
    "Invalid Token": "无效令牌",
    "Invalid Security Context": "无效安全上下文",
    "Operation not found.": "未找到操作。",
    "Invalid subject token.": "无效主题令牌。",
    "Unknown subject type": "未知主题类型",
    "Unknown grant type": "未知授权类型",
    "Unknown summary type": "未知摘要类型",
    "Unknown entitlement": "未知权利",
    "Profile not found {profile}": "未找到配置文件 {profile}",
    "Switch": "交换机",
}


def parse_vmsg(filepath):
    entries = {}
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    has_spaces = {}
    for i, line in enumerate(lines):
        s = line.strip()
        if not s or s.startswith('#') or s.startswith('signature'):
            continue
        m = re.match(r'^([a-zA-Z0-9_.]+)\s*=\s*"(.+)"\s*$', s)
        if m:
            key = m.group(1)
            val = m.group(2)
            entries[key] = val
            has_spaces[key] = ' = ' in line or line.count('=') > 0 and line.find(' = ') >= 0
    return entries, has_spaces


def has_chinese(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))


def chinese_ratio(text):
    """Calculate ratio of Chinese characters in text (excluding placeholders)"""
    cleaned = re.sub(r'\{[^}]+\}|%[0-9$I64u|.a-z]+', '', text)
    if not cleaned:
        return 0.0
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', cleaned))
    total_chars = len(cleaned.strip())
    return cn_chars / total_chars if total_chars > 0 else 0.0


def count_english_words(text):
    """Count remaining English words in mixed text"""
    cleaned = re.sub(r'\{[^}]+\}|%[0-9$I64u|.a-z]+', '', text)
    words = re.findall(r'\b[a-zA-Z]{2,}\b', cleaned)
    # Filter out known English that should stay
    keep_upper = {
        'API','CPU','IP','DNS','DHCP','HTTP','HTTPS','SSH','SSL','TCP','UDP',
        'NFS','VMFS','vSAN','vSphere','NSX','vCenter','VLAN','PCI','USB','SCSI',
        'NVMe','RDMA','HBA','NIC','MAC','UUID','BIOS','PNID','DPU','OCM','NPIV',
        'HCI','VLCM','HPP','IOPS','SRM','VR','FT','HA','DRS','EVC','SDRS','DPM',
        'SIOC','VCF','VASA','VVol','vVol','FCD','CBT','TPM','SEV','SGX','TDX',
        'NVDIMM','PXE','EFI','VGA','ROM','AHCI','NVME','PVSCSI','SATA','SAS',
        'FCoE','iSCSI','VXLAN','E1000','OVF','OVA','VMDK','VMX','VMSD','VMSN',
        'VMSS','RDM','VIB','ESX','ESXi','VCSA','PSC','VCHA','VCLS','CCPE',
        'VMRP','DPP','CDRS','VTC','FLB','VDTC','VAPI','OSFS','CLOM','DOM',
        'GSS','KB','SMTP','LWD','KMS','JWT','REST','SOAP','JSON','XML','HTML',
        'PNG','PDF','SVG','WWN','VC','VPXD','HOSTD','VPX','VIM','NAS','FQDN',
        'LB','RR','MTU','MAC','NIC','VNC','RDP','LDAP','SR_IOV','IO',
        'VM','PNIC','VMNIC','VSWITCH','DVSWITCH','DVS','VSS','DVD',
    }
    return [w for w in words if w.upper() not in keep_upper and w.upper() != w]


def fix_english_suffixes(text):
    """Fix English suffixes on Chinese words"""
    for suffix, replacement in sorted(EN_SUFFIX_MAP.items(), key=lambda x: -len(x[0])):
        text = re.sub(
            rf'([\u4e00-\u9fff]+)({suffix})\b',
            lambda m: m.group(1) + replacement,
            text
        )
    return text


def has_english_suffix_issue(text):
    return bool(re.search(r'[\u4e00-\u9fff]+[a-z]{2,}\b', text))


def retranslate_entry(en_text, zh_text):
    """
    Smart retranslation:
    - If mostly Chinese (>30% Chinese chars): fix remaining English words
    - If mostly English (<30% Chinese chars): full retranslation from EN
    """
    cn_ratio = chinese_ratio(zh_text)
    
    # Simple/short English-only entries
    trimmed_en = en_text.strip()
    if trimmed_en in SIMPLE_EN_TRANSLATIONS:
        return SIMPLE_EN_TRANSLATIONS[trimmed_en]
    
    if cn_ratio < 0.1:
        # Almost no Chinese - do full retranslation
        return translate_from_en(en_text)
    elif cn_ratio < 0.3:
        # Some Chinese but mostly English - fix aggressively
        result = fix_english_suffixes(zh_text)
        result = apply_dict_to_text(result)
        return result
    else:
        # Mostly Chinese already - just fix remaining English
        result = fix_english_suffixes(zh_text)
        result = apply_dict_to_text(result)
        return result


def translate_from_en(en_text):
    """Full retranslation of English text to Chinese"""
    result = en_text
    
    # Sort by length (longest first) to avoid partial replacements
    sorted_terms = sorted(TERMS.items(), key=lambda x: -len(x[0]))
    
    for en_term, zh_term in sorted_terms:
        if not zh_term:
            # Delete these words entirely
            pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
            result = pattern.sub('', result)
        else:
            pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
            result = pattern.sub(zh_term, result)
    
    # Clean up
    result = re.sub(r'\s+', ' ', result).strip()
    result = re.sub(r'\s+([，。；：、？）】\.])', r'\1', result)
    result = re.sub(r'([（【])\s+', r'\1', result)
    result = re.sub(r'\s+的$', '', result)
    result = re.sub(r'^\s*的\s+', '', result)
    
    return result


def apply_dict_to_text(text):
    """Apply dictionary replacements to text"""
    result = text
    
    # Sort by length (longest first)
    sorted_terms = sorted(TERMS.items(), key=lambda x: -len(x[0]))
    
    for en_term, zh_term in sorted_terms:
        if not zh_term:
            pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
            result = pattern.sub('', result)
        else:
            pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
            result = pattern.sub(zh_term, result)
    
    # Clean up
    result = re.sub(r'\s+', ' ', result).strip()
    result = re.sub(r'\s+([，。；：、？）】\.])', r'\1', result)
    result = re.sub(r'([（【])\s+', r'\1', result)
    
    return result


def main():
    print("=" * 65)
    print("locmsg.vmsg Translation Fix v2")
    print("=" * 65)
    
    # Backup
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"locmsg_{ts}.vmsg.bak")
    shutil.copy2(ZH_FILE, backup_path)
    print(f"\n[1] Backup: {backup_path}")
    
    # Parse
    print("\n[2] Parsing files...")
    en_entries, _ = parse_vmsg(EN_FILE)
    zh_entries, zh_spaces = parse_vmsg(ZH_FILE)
    
    with open(ZH_FILE, encoding='utf-8') as f:
        zh_content = f.read()
    original = zh_content
    
    print(f"  EN entries: {len(en_entries)}")
    print(f"  ZH entries: {len(zh_entries)}")
    
    # Analyze & fix
    print("\n[3] Analyzing and fixing...")
    stats = {'mostly_en': 0, 'mixed': 0, 'mostly_cn': 0, 'fixed': 0, 'unchanged': 0}
    fixes = {}
    
    for key, en_val in en_entries.items():
        if key not in zh_entries:
            print(f"  MISSING: {key}")
            continue
        
        zh_val = zh_entries[key]
        
        # Skip if already pure Chinese
        if not count_english_words(zh_val) and not has_english_suffix_issue(zh_val):
            stats['unchanged'] += 1
            continue
        
        cn_ratio = chinese_ratio(zh_val)
        if cn_ratio < 0.1:
            stats['mostly_en'] += 1
        elif cn_ratio < 0.3:
            stats['mixed'] += 1
        else:
            stats['mostly_cn'] += 1
        
        new_val = retranslate_entry(en_val, zh_val)
        
        if new_val != zh_val:
            fixes[key] = {'old': zh_val, 'new': new_val}
            stats['fixed'] += 1
    
    print(f"  Mostly English:   {stats['mostly_en']}")
    print(f"  Mixed:            {stats['mixed']}")
    print(f"  Mostly Chinese:   {stats['mostly_cn']}")
    print(f"  Fixed:            {stats['fixed']}")
    print(f"  Unchanged:        {stats['unchanged']}")
    
    # Apply
    print("\n[4] Applying fixes...")
    applied = 0
    for key, info in fixes.items():
        old_val = info['old']
        new_val = info['new']
        
        # Try both formats
        for fmt in [f'{key}="{old_val}"', f'{key} = "{old_val}"']:
            if fmt in zh_content:
                replacement = f'{key}="{new_val}"' if '="' in fmt else f'{key} = "{new_val}"'
                zh_content = zh_content.replace(fmt, replacement, 1)
                applied += 1
                break
        else:
            print(f"  CANNOT FIND: {key}")
    
    # Show first 15 fixes
    print(f"\n  Sample fixes (first 15):")
    shown = 0
    for key, info in fixes.items():
        if shown >= 15:
            break
        old_v = info['old']
        new_v = info['new']
        if old_v != new_v:
            shown += 1
            print(f"\n  [{shown}] {key}")
            print(f"    OLD: {old_v[:90]}")
            print(f"    NEW: {new_v[:90]}")
    
    # Fix comments
    zh_content = zh_content.replace(
        'This extended exception must be used only 和 only in cases when',
        '此扩展异常应仅在以下情况下使用'
    )
    zh_content = zh_content.replace(
        'the session is already authorized 和 never use it in unauthorized sessions.',
        '会话已授权，切勿在未授权会话中使用。'
    )
    for src in [
        'bora/vim/lib/esxtoken/TokenHandler.cpp',
        'bora/apps/esxtokend/vapi/messageResolver.cpp',
        'bora/apps/kmxa/vapi/messageResolver.cpp',
        'bora/apps/kmxd/vapi/messageResolver.cpp',
        'bora/apps/attestd/vapi/messageResolver.cpp',
        'bora/apps/attestd/vapi/statusImpl.cpp',
    ]:
        zh_content = zh_content.replace(f'注意： sync with {src}', f'注意：与 {src} 同步')
    
    # Write
    with open(ZH_FILE, 'w', encoding='utf-8') as f:
        f.write(zh_content)
    
    changed = zh_content != original
    print(f"\n  Applied:  {applied}")
    print(f"  Changed:  {changed}")
    
    # Summary
    print(f"\n{'='*65}")
    print("SUMMARY")
    print(f"{'='*65}")
    print(f"  Backup:   {backup_path}")
    print(f"  Output:   {ZH_FILE}")
    print(f"  Total:    {len(en_entries)} entries")
    print(f"  Fixed:    {stats['fixed']}")
    print(f"  Applied:  {applied}")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
