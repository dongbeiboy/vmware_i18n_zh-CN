#!/usr/bin/env python3
"""
Fix task.vmsg zh-CN: EN→ZH dictionary retranslation for mixed-language entries.
Recreated after another session deleted the original.
"""

import re, datetime
from pathlib import Path

SESSION_TAG = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
ZH_CN_FILE = Path(r"d:\vmware\i18n\OVFTool\env\zh-CN\task.vmsg")
EN_FILE = Path(r"d:\vmware\OVFTool\env\en\task.vmsg")
REPORT_FILE = Path(r"d:\vmware\i18n\OVFTool\env\zh-CN\fix_task_report.md")
BACKUP_FILE = Path(r"d:\vmware\i18n\.backup\OVFTool\env\zh-CN\task_pre_v2.vmsg")

# ─── Core dictionary (short but covers most artifacts) ──────────────────
EN2ZH = {
    # Cleanup patterns
    "the ": "", "a ": "", "an ": "", "is ": "", "are ": "", "be ": "",
    "was ": "", "were ": "", "been ": "", "being ": "", "have ": "",
    "has ": "", "had ": "", "do ": "", "does ": "", "did ": "",
    "that ": "", "which ": "", "who ": "", "whom ": "", "whose ": "",
    "where ": "", "when ": "", "what ": "", "why ": "", "how ": "",
    "will ": "", "would ": "", "shall ": "", "should ": "", "can ": "",
    "could ": "", "may ": "", "might ": "", "must ": "",
    "not ": "不 ", "no ": "无 ",
    "of ": "的 ", "to ": "", "for ": "的 ",
    "by ": "由 ", "on ": "在 ", "in ": "在 ",
    "from ": "从 ", "with ": "使用 ", "and ": "和 ",
    "or ": "或 ", "this ": "此 ", "these ": "这些 ",
    "its ": "其 ", "their ": "其 ", "into ": "到 ",
    "than ": "比 ", "via ": "通过 ", "per ": "每 ",
    "than ": "比 ", "as ": "作为 ",

    # Core VMware terms
    "host": "主机", "hosts": "主机",
    "server": "服务器", "servers": "服务器",
    "client": "客户端", "clients": "客户端",
    "virtual machine": "虚拟机", "virtual machines": "虚拟机",
    "VM": "虚拟机", "VMs": "虚拟机",
    "virtual disk": "虚拟磁盘", "virtual disks": "虚拟磁盘",
    "virtual switch": "虚拟交换机", "virtual switches": "虚拟交换机",
    "datastore": "数据存储", "datastores": "数据存储",
    "cluster": "集群", "clusters": "集群",
    "resource pool": "资源池", "resource pools": "资源池",
    "datacenter": "数据中心", "datacenters": "数据中心",
    "network": "网络", "networks": "网络",
    "folder": "文件夹", "folders": "文件夹",
    "template": "模板", "templates": "模板",
    "snapshot": "快照", "snapshots": "快照",
    "domain": "域", "domains": "域",
    "user": "用户", "users": "用户",
    "group": "组", "groups": "组",
    "role": "角色", "roles": "角色",
    "permission": "权限", "permissions": "权限",
    "privilege": "特权", "privileges": "特权",
    "configuration": "配置", "config": "配置",
    "information": "信息", "info": "信息",
    "service": "服务", "services": "服务",
    "manager": "管理器",
    "system": "系统", "systems": "系统",
    "device": "设备", "devices": "设备",
    "disk": "磁盘", "disks": "磁盘",
    "memory": "内存",
    "storage": "存储",
    "policy": "策略", "policies": "策略",
    "resource": "资源", "resources": "资源",
    "port": "端口", "ports": "端口",
    "certificate": "证书", "certificates": "证书",
    "license": "许可证", "licenses": "许可证",
    "key": "密钥", "keys": "密钥",
    "file": "文件", "files": "文件",
    "directory": "目录", "directories": "目录",
    "partition": "分区", "partitions": "分区",
    "volume": "卷", "volumes": "卷",
    "session": "会话", "sessions": "会话",
    "task": "任务", "tasks": "任务",
    "event": "事件", "events": "事件",
    "alarm": "警报", "alarms": "警报",
    "extension": "扩展", "extensions": "扩展",
    "adapter": "适配器", "adapters": "适配器",
    "agent": "代理", "agents": "代理",
    "module": "模块", "modules": "模块",
    "property": "属性", "properties": "属性",
    "value": "值", "values": "值",
    "parameter": "参数", "parameters": "参数",
    "status": "状态", "state": "状态",
    "mode": "模式",
    "level": "级别", "levels": "级别",
    "name": "名称", "names": "名称",
    "type": "类型", "types": "类型",
    "version": "版本", "versions": "版本",
    "message": "消息", "messages": "消息",
    "log": "日志", "logs": "日志",
    "rule": "规则", "rules": "规则",
    "entity": "实体", "entities": "实体",
    "object": "对象", "objects": "对象",
    "list": "列表",
    "default": "默认",
    "current": "当前",
    "active": "活动",
    "available": "可用",
    "invalid": "无效",
    "valid": "有效",
    "required": "必需",
    "optional": "可选",
    "specific": "特定",
    "particular": "特定",
    "existing": "现有",
    "multiple": "多个",
    "single": "单个",
    "unique": "唯一",
    "global": "全局",
    "local": "本地",
    "remote": "远程",
    "internal": "内部",
    "external": "外部",
    "public": "公共",
    "private": "私有",
    "primary": "主要",
    "secondary": "辅助",
    "parent": "父级",
    "child": "子级", "children": "子级",
    "source": "源",
    "target": "目标",
    "destination": "目标",
    "backup": "备份",
    "recovery": "恢复",
    "compatibility": "兼容性",
    "authentication": "身份验证",
    "authorization": "授权",
    "encryption": "加密",
    "namespace": "命名空间",
    "recommendation": "建议", "recommendations": "建议",
    "operation": "操作", "operations": "操作",
    "connection": "连接", "connections": "连接",
    "content": "内容",
    "environment": "环境",
    "specification": "规范", "spec": "规范",
    "description": "描述",
    "component": "组件", "components": "组件",
    "feature": "功能", "features": "功能",
    "attribute": "属性", "attributes": "属性",
    "capability": "功能", "capabilities": "功能",
    "configuration": "配置",
    "provider": "提供程序",
    "collection": "集合",
    "reference": "参考",
    "setting": "设置", "settings": "设置",
    "option": "选项", "options": "选项",
    "interval": "间隔", "intervals": "间隔",
    "password": "密码",
    "account": "帐户",
    "image": "映像",
    "location": "位置", "locations": "位置",
    "text": "文本",
    "output": "输出",
    "input": "输入",
    "format": "格式",
    "list": "列表",
    "details": "详细信息",
    "setup": "设置",
    "status": "状态",
    "entries": "条目",
    "properties": "属性",
    "content": "内容",
    "entries": "条目",
    "profile": "配置文件", "profiles": "配置文件",
    "pool": "池",
    "database": "数据库",
    "inventory": "清单",
    "environment": "环境",
    "collection": "集合",
    "tree": "树",
    "link": "链接",
    "topology": "拓扑",
    "history": "历史记录",
    "record": "记录", "records": "记录",
    "transaction": "事务",
    "sequence": "顺序",
    "count": "计数",
    "counter": "计数器", "counters": "计数器",
    "throughput": "吞吐量",
    "resolution": "分辨率",
    "revision": "修订版",
    "priority": "优先级",
    "usage": "使用率",
    "size": "大小",
    "duration": "持续时间",
    "timestamp": "时间戳",
    "overhead": "开销",
    "capacity": "容量",
    "access": "访问",
    "mapping": "映射", "mappings": "映射",
    "progress": "进度",
    "status": "状态",

    # Nouns - general
    "action": "操作", "actions": "操作",
    "answer": "应答",
    "area": "区域", "areas": "区域",
    "array": "阵列",
    "availability": "可用性",
    "bandwidth": "带宽",
    "base": "基础",
    "block": "块", "blocks": "块",
    "bundle": "捆绑包", "bundles": "捆绑包",
    "bus": "总线",
    "capability": "功能", "capabilities": "功能",
    "catalog": "目录",
    "category": "类别",
    "checkpoint": "检查点",
    "class": "类",
    "collector": "收集器", "collectors": "收集器",
    "command": "命令",
    "compatibility": "兼容性",
    "condition": "条件",
    "constraint": "约束",
    "container": "容器",
    "context": "上下文",
    "controller": "控制器", "controllers": "控制器",
    "conversion": "转换",
    "copy": "副本",
    "credential": "凭据", "credentials": "凭据",
    "data": "数据",
    "definition": "定义", "definitions": "定义",
    "dependency": "依赖项", "dependencies": "依赖项",
    "deployment": "部署",
    "descriptor": "描述符",
    "design": "设计",
    "diagnostic": "诊断",
    "digest": "摘要",
    "discovery": "发现",
    "display": "显示",
    "distribution": "分发",
    "document": "文档",
    "drive": "驱动器",
    "dump": "转储",
    "edition": "版本",
    "element": "元素", "elements": "元素",
    "endpoint": "端点",
    "engine": "引擎",
    "error": "错误", "errors": "错误",
    "evidence": "证据",
    "exception": "异常",
    "executable": "可执行文件",
    "execution": "执行",
    "expression": "表达式",
    "extent": "扩展区",
    "extraction": "提取",
    "failure": "故障",
    "field": "字段", "fields": "字段",
    "filter": "筛选器", "filters": "筛选器",
    "fingerprint": "指纹",
    "firewall": "防火墙",
    "firmware": "固件",
    "flag": "标志", "flags": "标志",
    "framework": "框架",
    "gateway": "网关",
    "guideline": "准则", "guidelines": "准则",
    "hardware": "硬件",
    "health": "运行状况",
    "hierarchy": "层次结构",
    "identity": "身份",
    "implementation": "实现",
    "index": "索引",
    "initialization": "初始化",
    "installation": "安装",
    "installer": "安装程序",
    "instance": "实例", "instances": "实例",
    "interface": "接口",
    "issue": "问题", "issues": "问题",
    "item": "项", "items": "项",
    "job": "作业", "jobs": "作业",
    "kernel": "内核",
    "label": "标签", "labels": "标签",
    "language": "语言", "languages": "语言",
    "lease": "租约",
    "limit": "限制", "limits": "限制",
    "load": "负载",
    "locale": "区域设置", "locales": "区域设置",
    "lock": "锁", "locks": "锁",
    "logging": "日志记录",
    "logic": "逻辑",
    "management": "管理",
    "manifest": "清单文件",
    "media": "媒体",
    "medium": "介质",
    "member": "成员",
    "membership": "成员资格",
    "metadata": "元数据",
    "method": "方法", "methods": "方法",
    "metric": "指标", "metrics": "指标",
    "migration": "迁移",
    "model": "模型",
    "modification": "修改",
    "monitor": "监视器",
    "monitoring": "监视",
    "mount": "挂载点",
    "notification": "通知", "notifications": "通知",
    "number": "数量",
    "owner": "所有者",
    "package": "包",
    "packet": "数据包",
    "page": "页面", "pages": "页面",
    "pair": "对",
    "partner": "合作伙伴", "partners": "合作伙伴",
    "patch": "修补程序",
    "path": "路径", "paths": "路径",
    "peer": "对等",
    "performance": "性能",
    "phase": "阶段",
    "placement": "放置",
    "preparation": "准备",
    "principal": "主体",
    "procedure": "过程",
    "process": "进程", "processes": "进程",
    "processing": "处理",
    "product": "产品",
    "program": "程序",
    "project": "项目",
    "protection": "保护",
    "protocol": "协议",
    "provision": "置备",
    "provisioning": "置备",
    "proxy": "代理",
    "queue": "队列",
    "quorum": "仲裁",
    "range": "范围",
    "read": "读取",
    "reason": "原因",
    "receipt": "接收",
    "reconciliation": "协调",
    "reference": "参考",
    "region": "区域",
    "registry": "注册表",
    "relation": "关系",
    "relationship": "关系",
    "release": "版本",
    "reliability": "可靠性",
    "relocation": "重新定位",
    "remediation": "修正",
    "replica": "副本",
    "replication": "复制",
    "report": "报告",
    "repository": "存储库",
    "request": "请求",
    "requirement": "要求", "requirements": "要求",
    "reservation": "预留", "reservations": "预留",
    "response": "响应",
    "restriction": "限制",
    "result": "结果", "results": "结果",
    "retention": "保留",
    "retry": "重试",
    "route": "路由",
    "ruleset": "规则集",
    "runtime": "运行时",
    "scenario": "方案", "scenarios": "方案",
    "schedule": "计划",
    "schema": "架构",
    "scheme": "方案",
    "screen": "屏幕",
    "script": "脚本",
    "scroll": "滚动",
    "search": "搜索",
    "secret": "机密",
    "section": "部分",
    "sector": "扇区",
    "security": "安全性",
    "sensor": "传感器",
    "shelf": "架",
    "signature": "签名",
    "site": "站点",
    "space": "空间",
    "standard": "标准",
    "startup": "启动",
    "statement": "语句",
    "statistic": "统计信息", "statistics": "统计信息",
    "structure": "结构",
    "subnet": "子网",
    "subprofile": "子配置文件",
    "subsystem": "子系统",
    "support": "支持",
    "switch": "交换机", "switches": "交换机",
    "synchronization": "同步",
    "table": "表",
    "tag": "标签", "tags": "标签",
    "terminal": "终端",
    "termination": "终止",
    "test": "测试", "tests": "测试",
    "thread": "线程",
    "threshold": "阈值",
    "ticket": "票证",
    "time": "时间",
    "timeout": "超时",
    "timer": "计时器",
    "token": "令牌",
    "tool": "工具", "tools": "工具",
    "traffic": "流量",
    "trust": "信任",
    "uninstaller": "卸载程序",
    "unit": "单元", "units": "单元",
    "update": "更新", "updates": "更新",
    "upgrade": "升级", "upgrades": "升级",
    "validation": "验证",
    "validity": "有效性",
    "vApp": "vApp",
    "vendor": "供应商",
    "verification": "验证",
    "view": "视图", "views": "视图",
    "virtual": "虚拟",
    "visibility": "可见性",
    "warning": "警告", "warnings": "警告",
    "window": "窗口", "windows": "窗口",
    "witness": "见证",
    "workflow": "工作流", "workflows": "工作流",
    "workload": "工作负载",
    "write": "写入",

    # Modifiers
    "all": "所有",
    "any": "任何",
    "each": "每个",
    "every": "每个",
    "new": "新",
    "newest": "最新",
    "old": "旧",
    "older": "较旧",
    "more": "更多",
    "most": "大多数",
    "some": "某些",
    "no": "无",
    "none": "无",
    "both": "两者",
    "only": "仅",
    "also": "也",
    "very": "很",
    "additional": "其他",
    "advanced": "高级",
    "basic": "基本",
    "complete": "完整",
    "current": "当前",
    "custom": "自定义",
    "direct": "直接",
    "dynamic": "动态",
    "empty": "空",
    "entire": "整个",
    "exact": "确切",
    "explicit": "显式",
    "extended": "扩展",
    "external": "外部",
    "final": "最终",
    "first": "第一",
    "fixed": "固定",
    "forced": "强制",
    "free": "空闲",
    "full": "完全",
    "general": "常规",
    "immediate": "立即",
    "implicit": "隐式",
    "independent": "独立",
    "initial": "初始",
    "last": "最后",
    "latest": "最新",
    "legacy": "旧版",
    "limited": "有限",
    "logical": "逻辑",
    "manual": "手动",
    "maximum": "最大", "max": "最大",
    "minimum": "最小", "min": "最小",
    "mixed": "混合",
    "native": "本机",
    "natural": "自然",
    "necessary": "必需",
    "next": "下一个",
    "normal": "正常",
    "null": "空",
    "open": "打开",
    "original": "原始",
    "other": "其他", "others": "其他",
    "partial": "部分",
    "physical": "物理",
    "potential": "潜在",
    "previous": "上一个",
    "proper": "正确",
    "raw": "原始",
    "ready": "就绪",
    "recent": "最近",
    "recently": "最近",
    "redundant": "冗余",
    "related": "相关",
    "relative": "相对",
    "remaining": "剩余",
    "restricted": "受限",
    "root": "根",
    "same": "相同",
    "saved": "已保存",
    "scheduled": "计划",
    "separate": "单独",
    "serial": "串行",
    "serious": "严重",
    "shared": "共享",
    "simple": "简单",
    "simulated": "模拟",
    "special": "特殊",
    "stable": "稳定",
    "standard": "标准",
    "static": "静态",
    "strict": "严格",
    "strong": "强",
    "subsequent": "后续",
    "sufficient": "足够",
    "suitable": "适合",
    "temporary": "临时",
    "top": "顶部",
    "total": "总计",

    # Verbs - core
    "add": "添加", "adds": "添加",
    "remove": "移除", "removes": "移除",
    "create": "创建", "creates": "创建",
    "delete": "删除", "deletes": "删除",
    "update": "更新", "updates": "更新",
    "set": "设置", "sets": "设置",
    "get": "获取", "gets": "获取",
    "retrieve": "检索", "retrieves": "检索",
    "query": "查询", "queries": "查询",
    "configure": "配置", "configures": "配置",
    "reconfigure": "重新配置", "reconfigures": "重新配置",
    "enable": "启用", "enables": "启用",
    "disable": "禁用", "disables": "禁用",
    "start": "启动", "starts": "启动",
    "stop": "停止", "stops": "停止",
    "restart": "重新启动", "restarts": "重新启动",
    "reload": "重新加载", "reloads": "重新加载",
    "refresh": "刷新", "refreshes": "刷新",
    "rename": "重命名", "renames": "重命名",
    "move": "移动", "moves": "移动",
    "copy": "复制", "copies": "复制",
    "clone": "克隆", "clones": "克隆",
    "migrate": "迁移", "migrates": "迁移",
    "check": "检查", "checks": "检查",
    "verify": "验证", "verifies": "验证",
    "validate": "验证", "validates": "验证",
    "select": "选择", "selects": "选择",
    "assign": "分配", "assigns": "分配",
    "register": "注册", "registers": "注册",
    "unregister": "注销", "unregisters": "注销",
    "export": "导出", "exports": "导出",
    "import": "导入", "imports": "导入",
    "deploy": "部署", "deploys": "部署",
    "install": "安装", "installs": "安装",
    "uninstall": "卸载", "uninstalls": "卸载",
    "upgrade": "升级", "upgrades": "升级",
    "upload": "上传", "uploads": "上传",
    "download": "下载", "downloads": "下载",
    "notify": "通知", "notifies": "通知",
    "reset": "重置", "resets": "重置",
    "suspend": "挂起", "suspends": "挂起",
    "resume": "恢复", "resumes": "恢复",
    "initialize": "初始化",
    "execute": "执行", "executes": "执行",
    "release": "释放", "releases": "释放",
    "renew": "续订", "renews": "续订",
    "cancel": "取消", "cancels": "取消",
    "format": "格式化", "formats": "格式化",
    "generate": "生成", "generates": "生成",
    "extend": "扩展", "extends": "扩展",
    "search": "搜索", "searches": "搜索",
    "locate": "查找", "locates": "查找",
    "join": "加入", "joins": "加入",
    "leave": "离开", "leaves": "离开",
    "mount": "挂载", "mounts": "挂载",
    "unmount": "卸载", "unmounts": "卸载",
    "consolidate": "整合", "consolidates": "整合",
    "allocate": "分配", "allocates": "分配",
    "attach": "附加", "attaches": "附加",
    "detach": "分离", "detaches": "分离",
    "associate": "关联", "associates": "关联",
    "lock": "锁定", "locks": "锁定",
    "unlock": "解锁", "unlocks": "解锁",
    "customize": "自定义", "customizes": "自定义",
    "reboot": "重新启动", "reboots": "重新启动",
    "shutdown": "关机", "shuts down": "关机",
    "power on": "打开电源", "power off": "关闭电源",
    "power-on": "打开电源", "power-off": "关闭电源",
    "login": "登录", "logout": "注销",
    "failover": "故障切换",
    "evacuate": "撤离", "evacuates": "撤离",
    "revert": "还原", "reverts": "还原",
    "reconnect": "重新连接", "reconnects": "重新连接",
    "disconnect": "断开连接", "disconnects": "断开连接",
    "overwrite": "覆盖", "overwrites": "覆盖",
    "synchronize": "同步", "synchronizes": "同步",
    "acknowledge": "确认",
    "acquire": "获取", "acquires": "获取",
    "activate": "激活", "activates": "激活",
    "apply": "应用", "applies": "应用",
    "backup": "备份",
    "bind": "绑定", "binds": "绑定",
    "browse": "浏览", "browses": "浏览",
    "change": "更改", "changes": "更改",
    "clear": "清除", "clears": "清除",
    "close": "关闭",
    "commit": "提交", "commits": "提交",
    "compute": "计算",
    "convert": "转换", "converts": "转换",
    "defined": "定义",
    "destroy": "销毁", "destroys": "销毁",
    "determine": "确定", "determines": "确定",
    "diagnose": "诊断",
    "discover": "发现", "discovers": "发现",
    "display": "显示",
    "edit": "编辑", "edits": "编辑",
    "enter": "进入", "enters": "进入",
    "estimate": "估计", "estimates": "估计",
    "exit": "退出", "exits": "退出",
    "fetch": "获取", "fetches": "获取",
    "find": "查找", "finds": "查找",
    "include": "包含", "includes": "包含",
    "initiate": "发出", "initiates": "发出",
    "invoke": "调用", "invokes": "调用",
    "list": "列出", "lists": "列出",
    "make": "设置", "makes": "设置",
    "map": "映射", "maps": "映射",
    "mark": "标记", "marks": "标记",
    "merge": "合并", "merges": "合并",
    "modify": "修改", "modifies": "修改",
    "open": "打开", "opens": "打开",
    "perform": "执行", "performs": "执行",
    "post": "提交", "posts": "提交",
    "prepare": "准备", "prepares": "准备",
    "promote": "提升",
    "provide": "提供", "provides": "提供",
    "put": "放置", "puts": "放置",
    "recommend": "建议", "recommends": "建议",
    "recompile": "重新编译",
    "restore": "还原", "restores": "还原",
    "return": "返回", "returns": "返回",
    "run": "运行", "runs": "运行",
    "save": "保存", "saves": "保存",
    "scan": "扫描", "scans": "扫描",
    "send": "发送", "sends": "发送",
    "specify": "指定", "specifies": "指定",
    "supply": "提供",
    "support": "支持", "supports": "支持",
    "terminate": "终止", "terminates": "终止",
    "test": "测试", "tests": "测试",
    "track": "跟踪",
    "transfer": "传输", "transfers": "传输",
    "wait": "等待", "waits": "等待",
    "write": "写入", "writes": "写入",
}

# Sort longest first
EN2ZH_SORTED = dict(sorted(EN2ZH.items(), key=lambda x: -len(x[0])))

# ─── Regex cleaners ─────────────────────────────────────────────────────
ZH_ED_SUFFIX = re.compile(r'([\u4e00-\u9fff]+)ed\b(?!\w)')
ZH_D_SUFFIX = re.compile(r'([\u4e00-\u9fff]+)d\b(?!\w)')
ZH_S_SUFFIX = re.compile(r'([\u4e00-\u9fff]+)s\b(?!\w)')
ZH_ER_SUFFIX = re.compile(r'([\u4e00-\u9fff]+)er\b')
ZH_ING_SUFFIX = re.compile(r'([\u4e00-\u9fff]+)ing\b')
PROGRESSIVE_RE = re.compile(r'正在([\u4e00-\u9fff]+)')
YI_VERB_RE = re.compile(r'已(启用|禁用|配置|创建|删除|更新|分配|选择|加载|挂载|卸载|注册|登录|连接|安装|迁移|复制|同步|验证|锁定|解锁|预留|关闭|打开|添加|移除|关联|分配|预留|批准)')
THE_RE = re.compile(r'\bthe\s+', re.I)
SPACE_CN_PUNC = re.compile(r'\s+([，。；：、）])')
MULTI_SPACE = re.compile(r'[ \t]{2,}')


def clean_artifacts(text):
    result = text
    result = ZH_ED_SUFFIX.sub(r'\1', result)
    result = ZH_ER_SUFFIX.sub(r'\1程序', result)
    result = ZH_ING_SUFFIX.sub(r'\1', result)
    result = ZH_D_SUFFIX.sub(r'\1', result)
    result = ZH_S_SUFFIX.sub(r'\1', result)
    result = PROGRESSIVE_RE.sub(r'\1', result)
    result = YI_VERB_RE.sub(r'\1', result)
    result = THE_RE.sub('', result)
    return result.strip()


# Pre-compile all patterns once
EN2ZH_PATTERNS = [
    (re.compile(r'(?<![a-zA-Z])' + re.escape(term) + r'(?![a-zA-Z])', re.I), zh)
    for term, zh in EN2ZH_SORTED.items()
]

def translate_en(text):
    result = text
    for pattern, zh_term in EN2ZH_PATTERNS:
        result = pattern.sub(zh_term, result)
    result = MULTI_SPACE.sub(' ', result).strip()
    result = SPACE_CN_PUNC.sub(r'\1', result)
    return result


def is_mostly_en(text, threshold=0.25):
    if not text.strip():
        return False
    en = sum(1 for c in text if c.isascii() and c.isalpha())
    zh = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return en + zh > 0 and en / (en + zh) > threshold


def parse_vmsg(filepath):
    entries = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'^([A-Za-z0-9_.]+)\.(label|summary)\s*=\s*"(.+)"$', line.rstrip('\n'))
            if m:
                entries[f"{m.group(1)}.{m.group(2)}"] = m.group(3)
    return entries


def build_en_map(entries):
    en_map = {}
    for key, value in entries.items():
        parts = key.rsplit('.', 1)
        if len(parts) == 2:
            en_map.setdefault(parts[0], {})[parts[1]] = value
    return en_map


def main():
    print(f"[{SESSION_TAG}] Reading EN...")
    en_entries = parse_vmsg(EN_FILE)
    en_map = build_en_map(en_entries)
    print(f"  {len(en_entries)} entries")

    print(f"[{SESSION_TAG}] Reading ZH-CN...")
    with open(ZH_CN_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Backup
    BACKUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f"  Backup: {BACKUP_FILE}")

    output = []
    stats = {'total': 0, 'fixed': 0, 'retranslated': 0, 'unchanged': 0}
    review = []

    for line in lines:
        s = line.rstrip('\n')
        m = re.match(r'^([A-Za-z0-9_.]+)\.(label|summary)\s*=\s*"(.+)"$', s)
        if m:
            stats['total'] += 1
            full_key = f"{m.group(1)}.{m.group(2)}"
            field = m.group(2)
            zh_val = m.group(3)
            root = m.group(1)
            en_val = en_map.get(root, {}).get(field) if root in en_map else None

            # Step 1: clean artifacts
            cleaned = clean_artifacts(zh_val)

            # Step 2: if still mostly EN, retranslate
            if is_mostly_en(cleaned, 0.35):
                if en_val:
                    ret = translate_en(en_val)
                    # Compare which is better
                    en_r = sum(1 for c in ret if c.isascii() and c.isalpha())
                    zh_r = sum(1 for c in ret if '\u4e00' <= c <= '\u9fff')
                    en_c = sum(1 for c in cleaned if c.isascii() and c.isalpha())
                    zh_c = sum(1 for c in cleaned if '\u4e00' <= c <= '\u9fff')
                    ratio_r = zh_r / max(zh_r + en_r, 1)
                    ratio_c = zh_c / max(zh_c + en_c, 1)

                    if ratio_r > ratio_c and ratio_r > 0.35:
                        new_val = ret
                        stats['retranslated'] += 1
                    elif zh_c > 0:
                        new_val = cleaned
                        stats['fixed'] += 1
                    else:
                        new_val = ret
                        stats['retranslated'] += 1
                else:
                    new_val = cleaned
                    stats['fixed'] += 1
            elif cleaned != zh_val:
                new_val = cleaned
                stats['fixed'] += 1
            else:
                new_val = zh_val
                stats['unchanged'] += 1

            if new_val != zh_val:
                en_chk = sum(1 for c in new_val if c.isascii() and c.isalpha())
                zh_chk = sum(1 for c in new_val if '\u4e00' <= c <= '\u9fff')
                if en_chk + zh_chk > 0 and en_chk / max(en_chk + zh_chk, 1) > 0.35:
                    review.append((full_key, new_val, en_val))

            output.append(f'{m.group(1)}.{field} = "{new_val}"\n')
        else:
            output.append(s + '\n')

    # Write
    with open(ZH_CN_FILE, 'w', encoding='utf-8') as f:
        f.writelines(output)

    # Report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# Fix Report\nGenerated: {datetime.datetime.now()}\n\n")
        f.write(f"Total: {stats['total']}, Fixed: {stats['fixed']}, "
                f"Retranslated: {stats['retranslated']}, Unchanged: {stats['unchanged']}\n")
        if review:
            f.write(f"\n## Needs review ({len(review)})\n")
            for k, v, ev in review[:50]:
                f.write(f"- {k}: {v[:60]}\n")

    print(f"\nDone! Total: {stats['total']}, Fixed: {stats['fixed']}, "
          f"Retranslated: {stats['retranslated']}, Unchanged: {stats['unchanged']}")
    print(f"Needs review: {len(review)}")


if __name__ == '__main__':
    main()
