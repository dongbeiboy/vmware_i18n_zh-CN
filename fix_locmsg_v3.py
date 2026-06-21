#!/usr/bin/env python3
"""
locmsg.vmsg zh-CN Translation Fix v3

Core improvements over v2:
1. PROTECT placeholders BEFORE any text processing
2. Handle "the/a/an/is/are/be" etc by removing them entirely (not translating)
3. Better EN→ZH dictionary with more terms
4. Protect proper nouns (product names, acronyms)
5. Clean up extra spaces after removal

Usage: python fix_locmsg_v3.py
"""

import os, re, shutil
from datetime import datetime

EN_FILE = r"D:\vmware\i18n\OVFTool\env\en\locmsg.vmsg"
ZH_FILE = r"D:\vmware\i18n\OVFTool\env\zh-CN\locmsg.vmsg"
BACKUP_DIR = r"D:\vmware\i18n\.backup"

# ============================================================
# TERM DICTIONARY - sorted by length (longest first for patterns)
# ============================================================

# These are strings where the EN value should be fully replaced
FULL_TRANSLATIONS = {
    # HPP Policy
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
    "Offset": "偏移量",
}

# Term replacement dictionary (EN -> ZH)
TERMS = {
    # Core infrastructure
    "virtual machine": "虚拟机",
    "virtual disk": "虚拟磁盘",
    "virtual device": "虚拟设备",
    "virtual switch": "虚拟交换机",
    "host bus adapter": "主机总线适配器",
    "network adapter": "网络适配器",
    "physical network adapter": "物理网络适配器",
    "vmkernel network adapter": "VMkernel 网络适配器",
    "distributed switch": "分布式交换机",
    "distributed port group": "分布式端口组",
    "resource pool": "资源池",
    "content library item": "内容库项目",
    "content library": "内容库",
    "fault tolerance": "容错",
    "resource profile": "资源配置文件",
    "maintenance mode": "维护模式",
    "standby mode": "待机模式",
    "lockdown mode": "锁定模式",
    "power state": "电源状态",
    "powered on": "已打开电源",
    "powered off": "已关闭电源",
    "power on": "打开电源",
    "power off": "关闭电源",
    "power up": "启动",
    "power down": "关闭",
    "thin provisioned": "已精简置备",
    "thin-provisioned": "已精简置备",
    "zeroed thick": "零置备厚格式",
    "zeroed-thick": "零置备厚格式",
    "port group": "端口组",
    "file system": "文件系统",
    "default gateway": "默认网关",
    "ip address": "IP 地址",
    "mac address": "MAC 地址",
    "subnet mask": "子网掩码",
    "disk group": "磁盘组",
    "support": "支持",
    "supported": "支持",
    "support s": "支持",
    "unsupported": "不支持",
    "snapshot": "快照",
    "sector": "扇区",
    "storage": "存储",
    "memory": "内存",
    "network": "网络",
    "networking": "联网",
    "cluster": "集群",
    "host": "主机",
    "server": "服务器",
    "subsystem": "子系统",
    "service": "服务",
    "device": "设备",
    "disk": "磁盘",
    "port": "端口",
    "uplink": "上行链路",
    "user": "用户",
    "username": "用户名",
    "password": "密码",
    "account": "帐户",
    "certificate": "证书",
    "token": "令牌",
    "session": "会话",
    "profile": "配置文件",
    "policy": "策略",
    "rule": "规则",
    "folder": "文件夹",
    "file": "文件",
    "directory": "目录",
    "path": "路径",
    "name": "名称",
    "type": "类型",
    "state": "状态",
    "status": "状态",
    "stateful": "有状态",
    "stateless": "无状态",
    "log": "日志",
    "event": "事件",
    "error": "错误",
    "warning": "警告",
    "message": "消息",
    "version": "版本",
    "config": "配置",
    "configuration": "配置",
    "property": "属性",
    "parameter": "参数",
    "attribute": "属性",
    "component": "组件",
    "feature": "功能",
    "function": "函数",
    "functionality": "功能",
    "capability": "能力",
    "capacity": "容量",
    "resource": "资源",
    "privilege": "特权",
    "permission": "权限",
    "authorization": "授权",
    "authentication": "身份验证",
    "security": "安全性",
    "encryption": "加密",
    "encrypted": "已加密",
    "namespace": "命名空间",
    "partition": "分区",
    "volume": "卷",
    "provider": "提供程序",
    "adapter": "适配器",
    "controller": "控制器",
    "workload": "工作负载",
    "operation": "操作",
    "information": "信息",
    "description": "描述",
    "label": "标签",
    "summary": "摘要",
    "number": "数量",
    "count": "计数",
    "total": "总计",
    "amount": "数量",
    "size": "大小",
    "length": "长度",
    "limit": "限制",
    "threshold": "阈值",
    "level": "级别",
    "priority": "优先级",
    "action": "操作",
    "task": "任务",
    "thread": "线程",
    "method": "方法",
    "mode": "模式",
    "option": "选项",
    "setting": "设置",
    "format": "格式",
    "pattern": "模式",
    "tag": "标签",
    "role": "角色",
    "entity": "实体",
    "object": "对象",
    "target": "目标",
    "source": "源",
    "destination": "目标",
    "input": "输入",
    "output": "输出",
    "value": "值",
    "values": "值",
    "reason": "原因",
    "condition": "条件",
    "context": "上下文",
    "scenario": "场景",
    "attempt": "尝试",
    "diagnostics": "诊断",
    "detail": "详细信息",
    "details": "详细信息",
    "type": "类型",
    "instance": "实例",
    "instance s": "实例",
    "configuration": "配置",
    "feature": "功能",
    "features": "功能",
    "edition": "版本",
    "subsystem": "子系统",
    "specification": "规范",
    "specifications": "规范",
    "parent": "父",
    "child": "子",
    "base": "基本",
    "beyond": "超出",
    "mark": "标记",
    "marked": "已标记",
    "finish": "完成",
    "finishing": "正在完成",
    
    # States
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
    "compatible": "兼容",
    "incompatible": "不兼容",
    "unknown": "未知",
    "pending": "待定",
    "queued": "已排队",
    "active": "活动",
    "inactive": "非活动",
    "passive": "被动",
    "standalone": "独立",
    "normal": "正常",
    "abnormal": "异常",
    "expanded": "已扩展",
    "expanding": "正在扩展",
    "configured": "已配置",
    "suspended": "已挂起",
    "synchronized": "已同步",
    "evacuated": "已疏散",
    "unconfigured": "未配置",
    
    # Verbs
    "allow": "允许",
    "disallow": "不允许",
    "enable": "启用",
    "disable": "禁用",
    "process": "处理",
    "perform": "执行",
    "request": "请求",
    "respond": "响应",
    "verify": "验证",
    "check": "检查",
    "ensure": "确保",
    "select": "选择",
    "specify": "指定",
    "provide": "提供",
    "configure": "配置",
    "reconfigure": "重新配置",
    "deploy": "部署",
    "deployed": "已部署",
    "deployment": "部署",
    "migrate": "迁移",
    "migrated": "已迁移",
    "migration": "迁移",
    "migrating": "正在迁移",
    "clone": "克隆",
    "cloned": "已克隆",
    "cloning": "正在克隆",
    "attach": "附加",
    "attached": "已附加",
    "detach": "分离",
    "detached": "已分离",
    "remove": "移除",
    "removing": "正在移除",
    "add": "添加",
    "adding": "正在添加",
    "update": "更新",
    "updating": "正在更新",
    "modify": "修改",
    "delete": "删除",
    "deleting": "正在删除",
    "create": "创建",
    "creating": "正在创建",
    "rename": "重命名",
    "move": "移动",
    "moving": "正在移动",
    "import": "导入",
    "export": "导出",
    "generate": "生成",
    "generated": "已生成",
    "synchronize": "同步",
    "synchronization": "同步",
    "clean up": "清理",
    "restart": "重新启动",
    "reboot": "重新引导",
    "suspend": "挂起",
    "resume": "恢复",
    "resolve": "解决",
    "recover": "恢复",
    "recovery": "恢复",
    "allocate": "分配",
    "allocate d": "分配",
    "release": "释放",
    "assign": "分配",
    "consume": "消耗",
    "consumed": "已消耗",
    "exceed": "超过",
    "exceeded": "超过",
    "increase": "增加",
    "decrease": "减少",
    "reduce": "减少",
    "extend": "扩展",
    "extending": "正在扩展",
    "expand": "展开",
    "upgrade": "升级",
    "upgraded": "已升级",
    "convert": "转换",
    "conversion": "转换",
    "transfer": "传输",
    "transferring": "正在传输",
    "transform": "转换",
    "mount": "挂载",
    "mounted": "已挂载",
    "unmount": "卸载",
    "unmounted": "已卸载",
    "load": "加载",
    "loaded": "已加载",
    "loading": "正在加载",
    "unload": "卸载",
    "wait": "等待",
    "waiting": "正在等待",
    "match": "匹配",
    "matched": "已匹配",
    "detect": "检测",
    "detected": "已检测",
    "identify": "标识",
    "identifying": "正在标识",
    "obtain": "获取",
    "receive": "接收",
    "received": "已接收",
    "send": "发送",
    "submit": "提交",
    "return": "返回",
    "display": "显示",
    "show": "显示",
    "hide": "隐藏",
    "override": "覆盖",
    "overwrite": "覆盖",
    "reset": "重置",
    "refresh": "刷新",
    "clear": "清除",
    "confirm": "确认",
    "save": "保存",
    "store": "存储",
    "stored": "已存储",
    "restore": "还原",
    "discover": "发现",
    "enumerate": "枚举",
    "register": "注册",
    "unregister": "注销",
    "install": "安装",
    "uninstall": "卸载",
    "apply": "应用",
    "applied": "已应用",
    "applying": "正在应用",
    "execute": "执行",
    "execution": "执行",
    "read": "读取",
    "write": "写入",
    "written": "已写入",
    "writing": "正在写入",
    "occurs": "发生",
    "occured": "发生",
    "occurred": "发生",
    "occurring": "正在发生",
    "indicates": "表示",
    "indicated": "表示",
    "contains": "包含",
    "contain": "包含",
    "containing": "包含",
    "include": "包括",
    "includes": "包括",
    "including": "包括",
    "requires": "需要",
    "require": "需要",
    "requiring": "需要",
    "correspond": "对应",
    "corresponds": "对应",
    "corresponding": "对应",
    "represents": "表示",
    "represent": "表示",
    "prevent": "阻止",
    "prevents": "阻止",
    "protect": "保护",
    "protects": "保护",
    "protected": "已保护",
    "retry": "重试",
    "retries": "重试",
    "retrying": "正在重试",
    "recommend": "建议",
    "recommended": "建议",
    "recommendation": "建议",
    "remediate": "修复",
    "remediation": "修复",
    "fails": "失败",
    "failure": "失败",
    "failover": "故障切换",
    "initiate": "启动",
    "initiated": "已启动",
    "initiates": "启动",
    "implement": "实现",
    "implemented": "已实现",
    "implementation": "实现",
    "integrate": "集成",
    "integrated": "已集成",
    "integration": "集成",
    "interact": "交互",
    "interaction": "交互",
    "isolate": "隔离",
    "isolated": "已隔离",
    "maintain": "维护",
    "maintenance": "维护",
    "manage": "管理",
    "management": "管理",
    "managed": "已管理",
    "managing": "正在管理",
    "monitor": "监视",
    "monitored": "已监视",
    "monitoring": "正在监视",
    "negotiate": "协商",
    "negotiated": "已协商",
    "negotiation": "协商",
    "notify": "通知",
    "notification": "通知",
    "notified": "已通知",
    "operate": "操作",
    "operates": "操作",
    "operating": "正在操作",
    "organize": "组织",
    "organized": "已组织",
    "preserve": "保留",
    "preserves": "保留",
    "preserved": "已保留",
    "publish": "发布",
    "published": "已发布",
    "publishing": "正在发布",
    "qualify": "限定",
    "qualified": "已限定",
    "reclaim": "回收",
    "reclaimed": "已回收",
    "reconcile": "协调",
    "reconciled": "已协调",
    "reconnect": "重新连接",
    "reconnected": "已重新连接",
    "redirect": "重定向",
    "redirected": "已重定向",
    "redirecting": "正在重定向",
    "reload": "重新加载",
    "reloaded": "已重新加载",
    "replace": "替换",
    "replaced": "已替换",
    "replacing": "正在替换",
    "replicate": "复制",
    "replication": "复制",
    "replicated": "已复制",
    "report": "报告",
    "reported": "已报告",
    "reporting": "正在报告",
    "represent": "表示",
    "requesting": "正在请求",
    "require": "需要",
    "requires": "需要",
    "requiring": "需要",
    "reserve": "预留",
    "reserved": "已预留",
    "reserving": "正在预留",
    "resolve": "解析",
    "resolved": "已解析",
    "resolving": "正在解析",
    "respond": "响应",
    "response": "响应",
    "restrict": "限制",
    "restricted": "已限制",
    "restriction": "限制",
    "resume": "恢复",
    "resumed": "已恢复",
    "resuming": "正在恢复",
    "retain": "保留",
    "retained": "已保留",
    "retry": "重试",
    "retrying": "正在重试",
    "reuse": "重用",
    "reused": "已重用",
    "reverting": "正在还原",
    "revert": "还原",
    "reverted": "已还原",
    "revoke": "撤销",
    "revoked": "已撤销",
    "rolling back": "正在回滚",
    "roll back": "回滚",
    "rolled back": "已回滚",
    "route": "路由",
    "routed": "已路由",
    "satisfy": "满足",
    "satisfies": "满足",
    "satisfied": "已满足",
    "schedule": "计划",
    "scheduled": "已计划",
    "scheduling": "正在计划",
    "search": "搜索",
    "searching": "正在搜索",
    "searches": "搜索",
    "terminate": "终止",
    "terminated": "已终止",
    "terminating": "正在终止",
    "abort": "中止",
    "aborted": "已中止",
    "cancel": "取消",
    "canceled": "已取消",
    "cancelled": "已取消",
    "canceling": "正在取消",
    "cancelling": "正在取消",
    
    # Prepositions / conjunctions (context-dependent)
    "of": "的",
    "in": "在",
    "on": "在",
    "at": "在",
    "to": "到",
    "for": "的",
    "by": "由",
    "from": "从",
    "with": "",
    "without": "没有",
    "through": "通过",
    "via": "通过",
    "between": "之间",
    "among": "之间",
    "within": "内",
    "into": "到",
    "during": "期间",
    "since": "自",
    "until": "直到",
    "after": "后",
    "before": "前",
    "above": "以上",
    "below": "以下",
    "under": "下",
    "over": "超过",
    "across": "跨",
    "against": "对",
    "except": "除",
    "including": "包括",
    "regarding": "关于",
    "regardless of": "无论",
    "as": "",
    "as well as": "及",
    "according to": "根据",
    "based on": "基于",
    "due to": "由于",
    "instead of": "而不是",
    "in order to": "以",
    
    # Articles - remove entirely
    "the": "",
    "a": "",
    "an": "",
    
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
    "once": "一",
    "both": "两者",
    "either": "任一",
    "neither": "均不",
    "also": "也",
    "only": "仅",
    "just": "仅",
    "even": "甚至",
    "still": "仍",
    "already": "已",
    
    # "be" verbs - remove (Chinese doesn't need them)
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
    "having": "",
    "having been": "",
    
    # Modal verbs
    "can": "",
    "cannot": "无法",
    "can not": "无法",
    "could": "",
    "will": "",
    "would": "",
    "should": "应",
    "may": "可能",
    "might": "可能",
    "shall": "应",
    "must": "必须",
    "need": "需要",
    "needs": "需要",
    "need to": "需要",
    "needs to": "需要",
    "has to": "必须",
    "have to": "必须",
    "able to": "",
    "unable to": "无法",
    "failed to": "无法",
    "fail to": "无法",
    "fails to": "无法",
    
    # Determiners
    "this": "此",
    "these": "这些",
    "that": "",
    "those": "那些",
    "its": "",
    "their": "",
    "your": "",
    "some": "某些",
    "any": "任何",
    "all": "所有",
    "every": "每个",
    "each": "每个",
    "no": "无",
    "none": "无",
    "other": "其他",
    "another": "另一个",
    "such": "此类",
    "same": "相同",
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
    "individual": "单个",
    "separate": "单独",
    
    # Quantifiers
    "many": "许多",
    "much": "很多",
    "few": "很少",
    "fewer": "更少",
    "little": "少量",
    "more": "更多",
    "most": "最多",
    "less": "更少",
    "least": "最少",
    "enough": "足够",
    "sufficient": "足够",
    "insufficient": "不足",
    "excessive": "过多",
    "extra": "额外",
    
    # Common adjectives
    "maximum": "最大",
    "minimum": "最小",
    "optimal": "最佳",
    "correct": "正确",
    "incorrect": "不正确",
    "proper": "正确",
    "properly": "正确",
    "generic": "常规",
    "specific": "特定",
    "duplicate": "重复",
    "conflict": "冲突",
    "conflicting": "冲突",
    "missing": "缺失",
    "empty": "空",
    "null": "空",
    "true": "真",
    "false": "假",
    "major": "主要",
    "minor": "次要",
    "critical": "严重",
    "severe": "严重",
    "fatal": "致命",
    "partial": "部分",
    "full": "完全",
    "complete": "完全",
    "incomplete": "不完全",
    "entire": "整个",
    "absolute": "绝对",
    "relative": "相对",
    "primary": "主要",
    "primary": "主要",
    "secondary": "辅助",
    "temporary": "临时",
    "temporarily": "临时",
    "permanent": "永久",
    "permanently": "永久",
    "automatic": "自动",
    "automatically": "自动",
    "manual": "手动",
    "manually": "手动",
    "explicit": "显式",
    "explicitly": "显式",
    "implicit": "隐式",
    "implicitly": "隐式",
    "initial": "初始",
    "subsequent": "后续",
    "final": "最终",
    "potential": "潜在",
    
    # Nouns
    "entity": "实体",
    "object": "对象",
    "target": "目标",
    "source": "源",
    "destination": "目标",
    "origin": "来源",
    "input": "输入",
    "output": "输出",
    "start": "开始",
    "end": "结束",
    "beginning": "开始",
    "middle": "中间",
    "top": "顶部",
    "bottom": "底部",
    "front": "前端",
    "back": "后端",
    "left": "左",
    "right": "右",
    "center": "中心",
    "local": "本地",
    "remote": "远程",
    "internal": "内部",
    "external": "外部",
    "public": "公共",
    "private": "私有",
    "virtual": "虚拟",
    "physical": "物理",
    "logical": "逻辑",
    "dynamic": "动态",
    "static": "静态",
    "digital": "数字",
    "encrypted": "已加密",
    "unencrypted": "未加密",
    "metadata": "元数据",
    "offline": "离线",
    "online": "在线",
    "real": "实时",
    "realtime": "实时",
    "synthetic": "合成",
    "raw": "原始",
    "legacy": "旧版",
    "advanced": "高级",
    "basic": "基本",
    "simple": "简单",
    "complex": "复杂",
    "consistent": "一致",
    "inconsistent": "不一致",
    "reliable": "可靠",
    "unreliable": "不可靠",
    "stable": "稳定",
    "unstable": "不稳定",
    "efficient": "高效",
    "inefficient": "低效",
    "frequent": "频繁",
    "infrequent": "不频繁",
    "immediate": "立即",
    "immediately": "立即",
    "instant": "即时",
    "instant": "即时",
    
    # VMware products and proper nouns (keep as-is or use standard CN name)
    "vcenter server": "vCenter Server",
    "vcenter": "vCenter",
    "vsphere replication": "vSphere 复制",
    "vsphere": "vSphere",
    "vsan": "vSAN",
    "nsx": "NSX",
    "esxi": "ESXi",
    "vmware tools": "VMware Tools",
    "vcenter ha": "vCenter HA",
    "esx": "ESX",
    
    # Connectives / sentence structure
    "that is": "即",
    "i.e.": "即",
    "for example": "例如",
    "e.g.": "例如",
    "such as": "例如",
    "in other words": "换言之",
    "as follows": "如下",
    "the following": "以下",
    "as a result": "因此",
    "as shown": "如图所示",
    "in addition": "此外",
}


def parse_vmsg(filepath):
    entries = {}
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    for i, line in enumerate(lines):
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
    total = len(cleaned.strip())
    return cn / total if total > 0 else 0.0


def protect_placeholders(text):
    """Replace placeholders with safe markers before text processing."""
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


def fix_english_suffixes(text):
    """Fix English suffixes attached to Chinese words."""
    text = re.sub(r'([\u4e00-\u9fff]+)ing\b', r'\1', text)
    text = re.sub(r'([\u4e00-\u9fff]+)ed\b', r'\1', text)
    text = re.sub(r'([\u4e00-\u9fff]+)d\b', r'\1', text)
    text = re.sub(r'([\u4e00-\u9fff]+)s\b', r'\1', text)
    return text


def has_en_suffix(text):
    return bool(re.search(r'[\u4e00-\u9fff]+[a-z]{2,}\b', text))


def eng_words_remaining(text):
    """Count remaining English words (excluding known proper nouns)."""
    cleaned = re.sub(r'\{[^}]+\}|%[0-9$I64u|.a-z]+', '', text)
    words = re.findall(r'\b[a-zA-Z]{2,}\b', cleaned)
    keep = {
        'API','CPU','IP','DNS','DHCP','HTTP','HTTPS','SSH','SSL','TCP','UDP',
        'NFS','VMFS','VVol','vVol','FCD','CBT','TPM','SEV','SGX','TDX',
        'NVDIMM','PXE','EFI','VGA','ROM','AHCI','NVMe','NVME','PVSCSI',
        'SATA','SAS','FCoE','iSCSI','VXLAN','E1000','VXNET','OVF','OVA',
        'VMDK','VMX','RDMA','VIB','ESX','ESXi','VCSA','PSC','KB','ID',
        'SMTP','KMS','JWT','JSON','XML','HTML','WWN','VC','NAS',
        'VM','PNIC','UUID','BIOS','GUID','MAC','HBA','DPU','MTU',
        'SRM','HA','DRS','EVC','SDRS','HCI','VLCM','HPP','IOPS',
        'VCF','VASA','VCHA','VCLS','CCPE','VMRP','DPP','CDRS',
        'DPM','SIOC','IORM','GSS','LWD','FT','VR','OCM','NPIV',
        'VOB','OSFS','CLOM','DOM','VAPI','VDTC','FLB','VTC',
        'VPXD','HOSTD','VPX','VIM','RDM','OVFIO',
        'FIXED','RR','LB','IO',
        'NSX','vSAN','vSphere','vCenter',
        'DCUI','SMBIOS','PCK','TCB','ACPI',
        'PNID','NIC1','NIC0','NIC',
        'CCP','VMIOP','SR_IOV','PCI',
        'VNC','RDP','LDAP','REST','SOAP',
        'SVG','PDF','PNG','CSV',
        'TcpipStack','Vmknic','VMSVC',
        'WCP','DPU','SEV','SGX',
        'LRO','SLA','SLO','QoS','DSCP',
        'DVS','DVPort','VLAN','PVLAN',
        'VXLAN','Geneve','NVGRE',
        'VMkernel','Uplink','VDS',
        'NFC','VStorage','VASA',
        'EVPN','BGP','OSPF',
        'VRealize','VROps','VRA','VRO','VRSLCM',
        'VRLI','ARC','VRNI','VIDM','WS1',
        'AVI','NSXT',
        'SVGA','VMCI','VMC',
        'VI','VIX','VDDK',
        'CIM','SFCB','SLP','CBRC',
        'HBR','VR','FT',
        'VMCI','vSock','vSocket',
        'vMotion','VMotion',
        'QuickBoot',
        'NIC','PNIC','VMNIC','VNIC',
        'HBA','vHBA',
        'PCIe','QPI',
        'NUMA','HT',
        'TCO','TCOff',
        'BIOS','UEFI',
        'MOREF','MOR',
        'POD',
        'CoS','ToS',
        'DDNS',
        'ESXTOP','VSCSIRef',
        'VST','VSTa',
        'UUID','GUID',
        'OID','DN',
        'DCUI',
        'DumpMem','CoreDump',
        'FSS','FSSAgent',
        'vProbe',
        'VDF',
        'VGA','SVGA',
        'VMCI','VSock',
        'vService',
        'VST','VSTa',
        'CMM','CMMDS',
        'VMXNET','VMXNET3','E1000E',
        'SVM','AVS',
        'DMTF','DMI',
        'SMBIOS',
    }
    return [w for w in words if w.upper() not in keep and len(w) > 1]


def translate_text(text, is_full=True):
    """
    Core translation logic with placeholder protection.
    is_full=True: full retranslation (remove articles, be-verbs, etc.)
    is_full=False: just replace known EN terms (for mostly-CN text)
    """
    # Step 1: Protect placeholders
    protected, markers = protect_placeholders(text)
    
    # Step 2: Fix English suffixes on Chinese words
    result = fix_english_suffixes(protected)
    
    # Step 3: Apply dictionary - longest first
    sorted_terms = sorted(TERMS.items(), key=lambda x: -len(x[0]))
    for en_term, zh_term in sorted_terms:
        if not zh_term:
            if is_full:
                # Only remove "the/a/an/is/are" etc in full retranslation mode
                pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
                result = pattern.sub('', result)
        else:
            pattern = re.compile(r'\b' + re.escape(en_term) + r'\b', re.IGNORECASE)
            result = pattern.sub(zh_term, result)
    
    # Step 4: Restore placeholders
    result = restore_placeholders(result, markers)
    
    # Step 5: Clean up whitespace
    result = re.sub(r'\s+', ' ', result).strip()
    result = re.sub(r'\s+([，。；：、？）】\.!,;:?])', r'\1', result)
    result = re.sub(r'([（【])\s+', r'\1', result)
    result = re.sub(r'\s+的\b', '', result)
    result = re.sub(r'\b的\s+', '', result)
    # Remove consecutive spaces
    result = re.sub(r'  +', ' ', result)
    # Fix word boundary artifacts
    result = result.replace('  ', ' ')
    
    return result


POST_FIXES = {
    # Specific pattern fixes for remaining English words in ZH text
    r'\bnot\b': '未',
    r'\bNot\b': '未',
    r'\btoo\b': '过',
    r'\bsmall\b': '小',
    r'\blarge\b': '大',
    r'\blong\b': '长',
    r'\bshort\b': '短',
    r'\bto\b': '',
    r'\bongoing\b': '正在进行的',
    r'\bcurrent\b': '当前',
    r'\bcurrently\b': '当前',
    r'\bhave\b': '',
    r'\bhas\b': '',
    r'\bhaving\b': '',
    r'\bdoes\b': '',
    r'\bdo\b': '',
    r'\bdid\b': '',
    r'\bwould\b': '',
    r'\bshould\b': '应',
    r'\bmust\b': '必须',
    r'\bmay\b': '',
    r'\bmight\b': '',
    r'\bwill\b': '将',
    r'\bcould\b': '',
    r'\bcannot\b': '无法',
    r'\bcan\b': '',
    r'\buse\b': '使用',
    r'\bused\b': '使用',
    r'\busing\b': '使用',
    r'\bneed\b': '需要',
    r'\bneeds\b': '需要',
    r'\brequire\b': '需要',
    r'\brequires\b': '需要',
    r'\brequired\b': '需要',
    r'\bwant\b': '需要',
    r'\bchoose\b': '选择',
    r'\bchosen\b': '已选择',
    r'\bfind\b': '查找',
    r'\bfound\b': '已找到',
    r'\bset\b': '设置',
    r'\bsetting\b': '设置',
    r'\bmark\b': '标记',
    r'\bmarked\b': '已标记',
    r'\bbase\b': '基本',
    r'\bbasic\b': '基本',
    r'\bbased\b': '基于',
    r'\bbegin\b': '开始',
    r'\bstart\b': '开始',
    r'\bend\b': '结束',
    r'\bfinish\b': '完成',
    r'\bstop\b': '停止',
    r'\bcontinue\b': '继续',
    r'\bexist\b': '存在',
    r'\bexists\b': '存在',
    r'\bexisted\b': '已存在',
    r'\bcause\b': '导致',
    r'\bcaused\b': '导致',
    r'\bcauses\b': '导致',
    r'\bchange\b': '更改',
    r'\bchanged\b': '已更改',
    r'\bchanges\b': '更改',
    r'\bcorrect\b': '正确',
    r'\bcorrectly\b': '正确',
    r'\bwrong\b': '错误',
    r'\bcontain\b': '包含',
    r'\bcontains\b': '包含',
    r'\bcontaining\b': '包含',
    r'\bhold\b': '保持',
    r'\bkeep\b': '保持',
    r'\bkeeps\b': '保持',
    r'\bmaintain\b': '维护',
    r'\bmaintains\b': '维护',
    r'\bprevent\b': '防止',
    r'\bprevents\b': '防止',
    r'\bprotect\b': '保护',
    r'\bprotects\b': '保护',
    r'\bprovide\b': '提供',
    r'\bprovides\b': '提供',
    r'\bprovided\b': '提供',
    r'\bproviding\b': '正在提供',
    r'\breceive\b': '接收',
    r'\breceives\b': '接收',
    r'\breceived\b': '已接收',
    r'\bsend\b': '发送',
    r'\bsends\b': '发送',
    r'\bsent\b': '已发送',
    r'\breturn\b': '返回',
    r'\breturns\b': '返回',
    r'\breturned\b': '已返回',
    r'\bbring\b': '引入',
    r'\bbrings\b': '引入',
    r'\bbringing\b': '正在引入',
    r'\bplace\b': '放置',
    r'\bplaced\b': '已放置',
    r'\bput\b': '放置',
    r'\btake\b': '执行',
    r'\btakes\b': '执行',
    r'\btaking\b': '正在执行',
    r'\bwork\b': '工作',
    r'\bworks\b': '工作',
    r'\bworking\b': '工作',
    r'\bbuild\b': '构建',
    r'\bbuilt\b': '已构建',
    r'\bbuilding\b': '正在构建',
    r'\bfollow\b': '遵循',
    r'\bfollows\b': '遵循',
    r'\bfollowing\b': '以下',
    r'\bmeaning\b': '含义',
    r'\bfunction\b': '函数',
    r'\bfunctionality\b': '功能',
    r'\bcapability\b': '能力',
    r'\bcapabilities\b': '能力',
    r'\bcapacity\b': '容量',
    r'\bnumber\b': '数量',
    r'\bnumbers\b': '数量',
    r'\bvalue\b': '值',
    r'\bvalues\b': '值',
    r'\bproperty\b': '属性',
    r'\bproperties\b': '属性',
    r'\bparameter\b': '参数',
    r'\bparameters\b': '参数',
    r'\battribute\b': '属性',
    r'\battributes\b': '属性',
    r'\bcomponent\b': '组件',
    r'\bcomponents\b': '组件',
    r'\bobject\b': '对象',
    r'\bobjects\b': '对象',
    r'\btarget\b': '目标',
    r'\bsource\b': '源',
    r'\bdestination\b': '目标',
    r'\borigin\b': '来源',
    r'\binput\b': '输入',
    r'\boutput\b': '输出',
    r'\bstart\b': '开始',
    r'\bstarts\b': '开始',
    r'\bstarted\b': '已启动',
    r'\bstop\b': '停止',
    r'\bstops\b': '停止',
    r'\bstopped\b': '已停止',
    r'\bfail\b': '失败',
    r'\bfails\b': '失败',
    r'\bfailed\b': '失败',
    r'\bfailure\b': '失败',
    r'\bfailures\b': '失败',
    r'\bsucceed\b': '成功',
    r'\bsucceeds\b': '成功',
    r'\bsucceeded\b': '已成功',
    r'\bsuccess\b': '成功',
    r'\bsuccessful\b': '成功',
    r'\bsuccessfully\b': '成功',
    r'\bversion\b': '版本',
    r'\bversions\b': '版本',
    r'\blevel\b': '级别',
    r'\blevels\b': '级别',
    r'\bstatus\b': '状态',
    r'\bstate\b': '状态',
    r'\btype\b': '类型',
    r'\btypes\b': '类型',
    r'\bmode\b': '模式',
    r'\bmodes\b': '模式',
    r'\bactive\b': '活动',
    r'\binactive\b': '非活动',
    r'\bpassive\b': '被动',
    r'\bprimary\b': '主要',
    r'\bsecondary\b': '辅助',
    r'\bboth\b': '两者',
    r'\beither\b': '任一',
    r'\bneither\b': '两者均不',
    r'\bhere\b': '',
    r'\bthere\b': '',
    r'\bit\b': '',
    r'\bits\b': '',
    r'\bthem\b': '',
    r'\btheir\b': '',
    r'\bthis\b': '此',
    r'\bthat\b': '',
    r'\bthese\b': '这些',
    r'\bthose\b': '那些',
    r'\bother\b': '其他',
    r'\banother\b': '另一个',
    r'\beach\b': '每个',
    r'\bevery\b': '每个',
    r'\bany\b': '任何',
    r'\bno\b': '',
    r'\bsome\b': '某些',
    r'\ball\b': '所有',
    r'\bthrough\b': '通过',
    r'\bby\b': '由',
    r'\bwithin\b': '内',
    r'\bwithout\b': '没有',
    r'\bincluding\b': '包括',
    r'\bexcept\b': '除',
    r'\bbetween\b': '之间',
    r'\bamong\b': '之间',
    r'\bunder\b': '下',
    r'\bover\b': '超过',
    r'\babove\b': '以上',
    r'\bbelow\b': '以下',
    r'\bbefore\b': '前',
    r'\bafter\b': '后',
    r'\bduring\b': '期间',
    r'\bsince\b': '自',
    r'\buntil\b': '直到',
    r'\bagain\b': '再次',
    r'\bmore\b': '更多',
    r'\bmost\b': '最多',
    r'\bless\b': '更少',
    r'\bleast\b': '最少',
    r'\bgreater\b': '更大',
    r'\bgreater than\b': '大于',
    r'\bless than\b': '小于',
    r'\brather than\b': '而不是',
    r'\binstead\b': '而不是',
    r'\binstead of\b': '而不是',
    r'\bthe same\b': '相同',
    r'\bsame\b': '相同',
    r'\bdifferent\b': '不同',
    r'\bdifferently\b': '不同',
    r'\bdifferent than\b': '不同于',
    r'\balso\b': '也',
    r'\beven\b': '甚至',
    r'\bonly\b': '仅',
    r'\bjust\b': '仅',
    r'\balready\b': '已',
    r'\bmoreover\b': '此外',
    r'\bfurthermore\b': '此外',
    r'\bhowever\b': '但是',
    r'\botherwise\b': '否则',
    r'\btherefore\b': '因此',
    r'\bthus\b': '因此',
    r'\bhence\b': '因此',
    r'\bconsequently\b': '因此',
    r'\bnonetheless\b': '尽管如此',
    r'\bnevertheless\b': '尽管如此',
    r'\bmeanwhile\b': '同时',
    r'\bwhether\b': '是否',
    r'\bwhere\b': '其中',
    r'\bwhereas\b': '而',
    r'\bwhile\b': '同时',
    r'\bwhen\b': '时',
    r'\bwhenever\b': '每当',
    r'\bwhy\b': '为何',
    r'\bhow\b': '如何',
    r'\bwhat\b': '什么',
    r'\bwhich\b': '哪个',
    r'\bwho\b': '谁',
    r'\bconsist\b': '包含',
    r'\bconsists\b': '包含',
    r'\bdepend\b': '依赖',
    r'\bdepends\b': '依赖',
    r'\bdepending\b': '根据',
    r'\bdetermine\b': '确定',
    r'\bdetermines\b': '确定',
    r'\bdetermined\b': '已确定',
    r'\bdetermining\b': '正在确定',
    r'\breserve\b': '预留',
    r'\breserves\b': '预留',
    r'\breserved\b': '已预留',
    r'\breserving\b': '正在预留',
    r'\bcompute\b': '计算',
    r'\bcomputes\b': '计算',
    r'\bcomputing\b': '计算',
    r'\bconnect\b': '连接',
    r'\bconnects\b': '连接',
    r'\bconnected\b': '已连接',
    r'\bconnecting\b': '正在连接',
    r'\bdisconnect\b': '断开连接',
    r'\bdisconnected\b': '已断开连接',
    r'\breconnect\b': '重新连接',
    r'\breconnected\b': '已重新连接',
    r'\binterrupt\b': '中断',
    r'\binterrupted\b': '已中断',
    r'\bpause\b': '暂停',
    r'\bpaused\b': '已暂停',
    r'\bpower\b': '电源',
    r'\bpowered\b': '已通电',
    r'\breset\b': '重置',
    r'\bresets\b': '重置',
    r'\bresetting\b': '正在重置',
    r'\bconvert\b': '转换',
    r'\bconverts\b': '转换',
    r'\bconverted\b': '已转换',
    r'\bconversion\b': '转换',
    r'\btransfer\b': '传输',
    r'\btransfers\b': '传输',
    r'\btransferred\b': '已传输',
    r'\btransferring\b': '正在传输',
    r'\bmove\b': '移动',
    r'\bmoves\b': '移动',
    r'\bmoved\b': '已移动',
    r'\bmoving\b': '正在移动',
    r'\bopen\b': '打开',
    r'\bopens\b': '打开',
    r'\bopened\b': '已打开',
    r'\bopening\b': '正在打开',
    r'\bclose\b': '关闭',
    r'\bcloses\b': '关闭',
    r'\bclosed\b': '已关闭',
    r'\bclosing\b': '正在关闭',
    r'\benter\b': '进入',
    r'\benters\b': '进入',
    r'\bentered\b': '已进入',
    r'\bentering\b': '正在进入',
    r'\bleave\b': '离开',
    r'\bleaves\b': '离开',
    r'\bleaving\b': '正在离开',
    r'\bexit\b': '退出',
    r'\bexits\b': '退出',
    r'\bexited\b': '已退出',
    r'\bexiting\b': '正在退出',
    r'\bjoin\b': '加入',
    r'\bjoins\b': '加入',
    r'\bjoined\b': '已加入',
    r'\bjoining\b': '正在加入',
    r'\bsubscribe\b': '订阅',
    r'\bsubscribes\b': '订阅',
    r'\bsubscribed\b': '已订阅',
    r'\bunsubscribe\b': '取消订阅',
    r'\bunsubscribes\b': '取消订阅',
    r'\bunsubscribed\b': '已取消订阅',
    r'\bcall\b': '调用',
    r'\bcalls\b': '调用',
    r'\bcalled\b': '已调用',
    r'\bcalling\b': '正在调用',
    r'\bspecify\b': '指定',
    r'\bspecifies\b': '指定',
    r'\bspecified\b': '指定',
    r'\bspecifying\b': '正在指定',
    r'\bspec\b': '规范',
    r'\bspecs\b': '规范',
    r'\bhost\b': '主机',
    r'\bhosts\b': '主机',
    r'\bserver\b': '服务器',
    r'\bservice\b': '服务',
    r'\bservices\b': '服务',
    r'\bdevice\b': '设备',
    r'\bdevices\b': '设备',
    r'\bdisk\b': '磁盘',
    r'\bdisks\b': '磁盘',
    r'\bhosted\b': '托管',
    r'\bhosting\b': '托管',
    r'\bcluster\b': '集群',
    r'\bclusters\b': '集群',
    r'\bnode\b': '节点',
    r'\bnodes\b': '节点',
    r'\bpath\b': '路径',
    r'\bpaths\b': '路径',
    r'\bfile\b': '文件',
    r'\bfiles\b': '文件',
    r'\bdirectory\b': '目录',
    r'\bdirectories\b': '目录',
    r'\bfolder\b': '文件夹',
    r'\bfolders\b': '文件夹',
    r'\bname\b': '名称',
    r'\bnames\b': '名称',
    r'\buser\b': '用户',
    r'\buser name\b': '用户名',
    r'\busername\b': '用户名',
    r'\bpassword\b': '密码',
    r'\baccount\b': '帐户',
    r'\bconfig\b': '配置',
    r'\bconfiguring\b': '正在配置',
    r'\bconfigure\b': '配置',
    r'\bconfigures\b': '配置',
    r'\bconfigured\b': '已配置',
    r'\bwithout\b': '没有',
    r'\bpermit\b': '允许',
    r'\bpermits\b': '允许',
    r'\bpermitted\b': '允许',
    r'\brefer\b': '参考',
    r'\brefers\b': '参考',
    r'\breferring\b': '参考',
    r'\breference\b': '引用',
    r'\breferences\b': '引用',
    r'\breferenced\b': '已引用',
    r'\bunderstand\b': '了解',
    r'\bunderstands\b': '了解',
    r'\bwritable\b': '可写入',
    r'\breadable\b': '可读取',
    r'\breach\b': '达到',
    r'\breaches\b': '达到',
    r'\breached\b': '已达到',
}


def post_process(text):
    """Apply post-fix patterns to clean up remaining English words."""
    for pattern_str, replacement in POST_FIXES.items():
        text = re.sub(pattern_str, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'\s+([，。；：、？）】\.!,;:?])', r'\1', text)
    text = re.sub(r'([（【])\s+', r'\1', text)
    return text


def main():
    print("=" * 65)
    print("locmsg.vmsg Translation Fix v3")
    print("=" * 65)
    
    # Backup
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"locmsg_{ts}.vmsg.bak")
    shutil.copy2(ZH_FILE, backup_path)
    print(f"\n[1] Backup: {backup_path}")
    
    # Parse
    print("\n[2] Parsing files...")
    en_entries = parse_vmsg(EN_FILE)
    zh_entries = parse_vmsg(ZH_FILE)
    
    with open(ZH_FILE, encoding='utf-8') as f:
        zh_content = f.read()
    original = zh_content
    
    print(f"  EN entries: {len(en_entries)}")
    print(f"  ZH entries: {len(zh_entries)}")
    
    # Analysis
    print("\n[3] Analyzing and fixing...")
    
    stats = {'fixable': 0, 'already_good': 0, 'full_tr': 0, 'suffix_fix': 0}
    fixes = {}
    
    for key, en_val in en_entries.items():
        if key not in zh_entries:
            continue
        
        zh_val = zh_entries[key]
        
        # Check for remaining English issues
        remaining = eng_words_remaining(zh_val)
        has_suffix = has_en_suffix(zh_val)
        
        if not remaining and not has_suffix:
            stats['already_good'] += 1
            continue
        
        stats['fixable'] += 1
        cn_ratio = chinese_ratio(zh_val)
        
        # Check if full translation from EN is needed
        use_full = cn_ratio < 0.2 or (cn_ratio < 0.5 and len(remaining) > 3)
        
        if use_full:
            stats['full_tr'] += 1
            new_val = translate_text(en_val, is_full=True)
        new_val = post_process(new_val)
    else:
        stats['suffix_fix'] += 1
        new_val = translate_text(zh_val, is_full=False)
        new_val = post_process(new_val)
    
    print(f"  Already good:     {stats['already_good']}")
    print(f"  Fixable:          {stats['fixable']}")
    print(f"  Full translation: {stats['full_tr']}")
    print(f"  Suffix/word fix:  {stats['suffix_fix']}")
    print(f"  Fixed:            {len(fixes)}")
    
    # Apply fixes
    print("\n[4] Applying fixes...")
    applied = 0
    for key, info in fixes.items():
        old_val = info['old']
        new_val = info['new']
        
        for fmt in [f'{key}="{old_val}"', f'{key} = "{old_val}"']:
            if fmt in zh_content:
                replacement = f'{key}="{new_val}"' if '="' in fmt else f'{key} = "{new_val}"'
                zh_content = zh_content.replace(fmt, replacement, 1)
                applied += 1
                break
        else:
            # Partial match - might have been partially fixed already
            pass
    
    # Show samples
    print(f"\n  Samples (first 20):")
    shown = 0
    for key, info in fixes.items():
        if shown >= 20:
            break
        if info['old'] != info['new']:
            shown += 1
            print(f"\n  [{shown}] {key}")
            old_v = info['old'][:80]
            new_v = info['new'][:80]
            if old_v != new_v:
                print(f"    OLD: {old_v}")
                print(f"    NEW: {new_v}")
    
    # Fix comments
    comment_fixes = {
        'This extended exception must be used only 和 only in cases when': '此扩展异常应仅在以下情况下使用',
        'the session is already authorized 和 never use it in unauthorized sessions.': '会话已授权，切勿在未授权会话中使用。',
    }
    for old_c, new_c in comment_fixes.items():
        if old_c in zh_content:
            zh_content = zh_content.replace(old_c, new_c)
    
    # Fix "注意： sync with" comments
    zh_content = re.sub(
        r'注意： sync with (bora/\S+)',
        r'注意：与 \1 同步',
        zh_content
    )
    
    # Write
    with open(ZH_FILE, 'w', encoding='utf-8') as f:
        f.write(zh_content)
    
    changed = zh_content != original
    
    print(f"\n  Applied:   {applied}")
    print(f"  Changed:   {changed}")
    
    # Summary
    print(f"\n{'='*65}")
    print("SUMMARY")
    print(f"{'='*65}")
    print(f"  Backup:    {backup_path}")
    print(f"  Output:    {ZH_FILE}")
    print(f"  Total:     {len(en_entries)} entries")
    print(f"  Fixed:     {len(fixes)}")
    print(f"  Applied:   {applied}")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()
