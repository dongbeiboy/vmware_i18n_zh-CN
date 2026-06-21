#!/usr/bin/env python3
"""
Enhanced OVFTool EN→CN translator.
Reads English .vmsg files, applies comprehensive phrase-level dictionary,
fixes mixed Chinese-English, and writes improved zh-CN output.
"""

import os, re, glob, json

EN_DIR = r"OVFTool\env\en"
ZH_DIR = r"OVFTool\env\zh-CN"

# ============================================================
# Comprehensive Translation Dictionary
# Key = English phrase (lowercase, stripped), Value = Chinese
# Longer phrases MUST come before shorter ones to avoid partial matches
# ============================================================

# These are exact full-value translations (matching entire "..." content)
FULL_VALUE_MAP = {
    # Power Policy
    "not supported": "不支持",
    "host power management was not detected": "未检测到主机电源管理",
    "high performance": "高性能",
    "do not use any power management features": "不使用任何电源管理功能",
    "balanced": "均衡",
    "reduce energy consumption with minimal performance compromise": "以最小性能影响降低能耗",
    "low power": "低功耗",
    "reduce energy consumption at the risk of lower performance": "降低能耗，但可能影响性能",
    "custom": "自定义",
    "user-defined power management policy": "用户定义的电源管理策略",
    
    # Nvdimm health
    "normal": "正常",
    "n/a": "无",
    "maintenance needed": "需要维护",
    "maintenance required but no data loss": "需要维护，但不会丢失数据",
    "performance degraded": "性能降级",
    "all data loss": "全部数据丢失",
    "unknown": "未知",
    "health status cannot be obtained or is currently unavailable": "无法获取运行状况状态，或当前不可用",
    
    # Time
    "less than a minute": "不到 1 分钟",
    "less than an hour": "不到 1 小时",
    "less than a day": "不到 1 天",
    "less than a week": "不到 1 周",
    "less than a month": "不到 1 个月",
    "less than a year": "不到 1 年",
    "more than a year": "超过 1 年",
    
    # Event categories
    "info": "信息",
    "error": "错误",
    "warning": "警告",
    "user name": "用户名",
    "user name creating the event": "创建事件的用户名",
    "data center id": "数据中心 ID",
    "event data center id": "事件数据中心 ID",
    "data center name": "数据中心名称",
    "compute resource id for the event": "事件的计算资源 ID",
    "compute-resource id": "计算资源 ID",
    "compute-resource name": "计算资源名称",
    "host id": "主机 ID",
    "host name": "主机名称",
    "user id": "用户 ID",
    "user id for the event": "事件的用户 ID",
    "event detail": "事件详细信息",
    "full formatted message for the event": "事件的完整格式化消息",
    "system account": "系统帐户",
    "date and time when the event occurred": "事件发生的日期和时间",
    "event key": "事件键值",
    "chain id": "链 ID",
    "key for an event chain": "事件链的键值",
    "alarm task": "警报任务",
    "task started by an alarm": "由警报启动的任务",
    "scheduled task": "计划任务",
    "task started by a scheduled task": "由计划任务启动的任务",
    "system task": "系统任务",
    "task started by the server": "由服务器启动的任务",
    "user task": "用户任务",
    "task started by a specific user": "由特定用户启动的任务",
    "<event>": "<Event>",
    "<internal>": "<internal>",
    
    # Performance counter
    "absolute": "绝对值",
    "absolute value": "绝对值",
    "delta": "增量",
    "delta value": "增量值",
    "rate": "速率",
    "rate value": "速率值",
    "fraction": "比率",
    "fraction value": "比率值",
    "raw": "原始值",
    "raw value": "原始值",
    "logn": "对数",
    "logn value": "对数值",
    "average": "平均值",
    "maximum": "最大值",
    "minimum": "最小值",
    "median": "中位数",
    "latest": "最新值",
    "first": "初始值",
    "none": "无",
    "past day": "过去一天",
    "past hour": "过去一小时",
    "past month": "过去一个月",
    "past week": "过去一周",
    "past year": "过去一年",
    "statistics over the past day": "过去一天的统计信息",
    "statistics over the past hour": "过去一小时的统计信息",
    "statistics over the past month": "过去一个月的统计信息",
    "statistics over the past week": "过去一周的统计信息",
    "statistics over the past year": "过去一年的统计信息",
    
    # Permission / auth
    "folder.create": "创建文件夹",
    "folder.delete": "删除文件夹",
    "folder.move": "移动文件夹",
    "folder.rename": "重命名文件夹",
    "datacenter.create": "创建数据中心",
    "datacenter.delete": "删除数据中心",
    "datacenter.move": "移动数据中心",
    "datacenter.rename": "重命名数据中心",
    "host.cim.agent": "CIM Agent",
    "host.cim.ciminteraction": "CIM 交互",
    "host.connection": "连接",
    "host.create": "创建",
    "host.delete": "删除",
    "host.deletehost": "删除主机",
    "host.esxagentmanager": "ESX Agent Manager",
    "host.fibrechannel": "Fibre Channel",
    "host.fibrechannel.hba": "Fibre Channel HBA",
    "host.fibrechannel.hba.configure": "配置",
    
    # License messages
    "evaluation period is over": "评估期已结束",
    "license expired": "许可证已过期",
    "please install a valid license to use this product": "请安装有效许可证以使用此产品",
    
    # Common task messages
    "create": "创建",
    "update": "更新",
    "delete": "删除",
    "remove": "移除",
    "rename": "重命名",
    "migrate": "迁移",
    "clone": "克隆",
    "power on": "打开电源",
    "power off": "关闭电源",
    "suspend": "挂起",
    "reset": "重置",
    "shutdown guest": "关闭客户机",
    "reboot guest": "重新启动客户机",
    "standby guest": "客户机待机",
    "reconfigure": "重新配置",
    "register": "注册",
    "unregister": "注销",
    "reload": "重新加载",
    "refresh": "刷新",
    "connect": "连接",
    "disconnect": "断开连接",
    
    # ovftool specific
    "source": "源",
    "destination": "目标",
    "source type": "源类型",
    "destination type": "目标类型",
    "source location": "源位置",
    "destination location": "目标位置",
    "transfer failed": "传输失败",
    "authentication failed": "身份验证失败",
    "connection refused": "连接被拒绝",
    "connection timeout": "连接超时",
    "file not found": "文件未找到",
    "access denied": "访问被拒绝",
    "operation completed successfully": "操作成功完成",
    "operation failed": "操作失败",
    "invalid parameter": "无效参数",
    "unsupported protocol": "不支持的协议",
    "network error": "网络错误",
    "disk space full": "磁盘空间已满",
    "ssl certificate error": "SSL 证书错误",
    "unknown error": "未知错误",
    "unsupported version": "不支持的版本",
    "already exists": "已存在",
    "not found": "未找到",
    "invalid configuration": "无效配置",
    "validation failed": "验证失败",
    "deployment completed": "部署完成",
    "deployment failed": "部署失败",
    "import completed": "导入完成",
    "export completed": "导出完成",
    "download completed": "下载完成",
    "upload completed": "上传完成",
    "initializing transfer": "正在初始化传输",
    "validating source": "正在验证源",
    "validating destination": "正在验证目标",
    "transferring data": "正在传输数据",
    "completed": "已完成",
    "in progress": "进行中",
    "cancelled": "已取消",
    "failed with error": "失败",
    "successful": "成功",

    # Event descriptions - task lifecycle
    "task started": "任务已启动",
    "task completed": "任务已完成",
    "task failed": "任务失败",
    "task queued": "任务已排队",
    "task timeout": "任务超时",
    "task cancelled": "任务已取消",
    "scheduled task completed": "计划任务已完成",
    "scheduled task created": "计划任务已创建",
    "scheduled task removed": "计划任务已移除",
    "alarm created": "警报已创建",
    "alarm removed": "警报已移除",
    "alarm reconfigured": "警报已重新配置",
    "alarm status": "警报状态",
    "alarm acked": "警报已确认",
    "alarm email completed": "警报电子邮件已发送",
    "alarm email failed": "警报电子邮件发送失败",
    "alarm snmp completed": "警报 SNMP 已完成",
    "alarm snmp failed": "警报 SNMP 失败",
    "alarm action triggered": "警报操作已触发",
    "alarm action": "警报操作",

    # Event descriptions - VM lifecycle
    "vm created": "虚拟机已创建",
    "vm deleted": "虚拟机已删除",
    "vm reconfigured": "虚拟机已重新配置",
    "vm renamed": "虚拟机已重命名",
    "vm migrated": "虚拟机已迁移",
    "vm relocated": "虚拟机已重新定位",
    "vm cloned": "虚拟机已克隆",
    "vm deployed": "虚拟机已部署",
    "vm powered on": "虚拟机已打开电源",
    "vm powered off": "虚拟机已关闭电源",
    "vm suspended": "虚拟机已挂起",
    "vm resumed": "虚拟机已恢复",
    "vm reset": "虚拟机已重置",
    "vm shutdown": "虚拟机关机",
    "vm rebooted": "虚拟机已重新启动",
    "vm message": "虚拟机消息",
    "vm message error": "虚拟机消息错误",
    "vm message warning": "虚拟机消息警告",
    "vm mac assigned": "虚拟机 MAC 地址已分配",
    "vm mac changed": "虚拟机 MAC 地址已更改",
    "vm uuid assigned": "虚拟机 UUID 已分配",
    "vm uuid changed": "虚拟机 UUID 已更改",
    "vm das reset failed": "虚拟机 DAS 重置失败",
    "vm failover failed": "虚拟机故障切换失败",
    "vm being created": "正在创建虚拟机",
    "vm being deleted": "正在删除虚拟机",
    "vm being cloned": "正在克隆虚拟机",
    "vm being hot migrated": "正在热迁移虚拟机",
    "vm being relocated": "正在重新定位虚拟机",
    "vm upgraded": "虚拟机已升级",
    "vm folder added": "虚拟机文件夹已添加",
    "vm folder moved": "虚拟机文件夹已移动",
    "vm max restart count reached": "虚拟机已达到最大重新启动次数",
    "vm config missing": "虚拟机配置缺失",
    "vm date rolled back": "虚拟机日期已回滚",
    "vm das being reset with screenshot": "虚拟机 DAS 正在带截图重置",

    # Event descriptions - Host lifecycle
    "host connected": "主机已连接",
    "host disconnected": "主机已断开连接",
    "host added": "主机已添加",
    "host removed": "主机已移除",
    "host moved": "主机已移动",
    "host reconfigured": "主机已重新配置",
    "host shutdown": "主机关机",
    "host rebooted": "主机已重新启动",
    "host entered maintenance mode": "主机已进入维护模式",
    "host exited maintenance mode": "主机已退出维护模式",
    "host entered standby mode": "主机已进入待机模式",
    "host exited standby mode": "主机已退出待机模式",
    "host error": "主机错误",
    "host warning": "主机警告",
    "host ssl certificate warning": "主机 SSL 证书警告",
    "host profile applied": "主机配置文件已应用",
    "host profile compliance": "主机配置文件合规性",
    "host tpm attestation": "主机 TPM 证明",
    "host tpm attestation failed": "主机 TPM 证明失败",

    # Event descriptions - Datastore
    "datastore created": "数据存储已创建",
    "datastore removed": "数据存储已移除",
    "datastore renamed": "数据存储已重命名",
    "datastore capacity increased": "数据存储容量已增加",
    "datastore file uploaded": "数据存储文件已上传",
    "datastore file downloaded": "数据存储文件已下载",
    "datastore file moved": "数据存储文件已移动",
    "datastore file deleted": "数据存储文件已删除",
    "datastore inaccessible": "数据存储不可访问",
    "datastore ip changed": "数据存储 IP 已更改",
    "datastore principal removed": "数据存储主体已移除",

    # Event format strings with placeholders
    "cannot complete vm clone": "无法完成虚拟机克隆",
    "cannot complete customization sysprep": "无法完成 Sysprep 自定义",
    "cannot migrate vm": "无法迁移虚拟机",
    "cannot complete vm relayout.": "无法完成虚拟机重新布局。",
    "migrating {vm.name} from {host.name}": "正在从 {host.name} 迁移 {vm.name}",
    "relocating {vm.name} from {host.name}": "正在从 {host.name} 重新定位 {vm.name}",
    "being cloned to {destName}": "正在克隆到 {destName}",
    "an upgrade for vsphere distributed switch {dvs.name} is in progress.": "vSphere Distributed Switch {dvs.name} 的升级正在进行中。",
    "an upgrade for vsphere distributed switch {dvs.name} was rejected.": "vSphere Distributed Switch {dvs.name} 的升级已被拒绝。",
    "bi oid ({uuid}) conflicts with that of {conflictedvm.name}": "BIOS ID ({uuid}) 与 {conflictedVm.name} 的 BIOS ID 冲突",
    "cannot connect {host.name}": "无法连接 {host.name}",
    "cannot connect: already managed by {servername}": "无法连接：已被 {serverName} 管理",
    "cannot migrate to {desthost.name}, {destdatastore.name}": "无法迁移到 {destHost.name}、{destDatastore.name}",
    "cannot migrate {vm.name}": "无法迁移 {vm.name}",
    "assign a new instance uuid": "分配新实例 UUID",
    "assigned new bios uuid": "已分配新 BIOS UUID",
    "started by {user.name}": "由 {user.name} 启动",
    "started by {user.name} on {host.name}": "由 {user.name} 在 {host.name} 上启动",
    "completed on {host.name}": "已在 {host.name} 上完成",
    "failed on {host.name}": "在 {host.name} 上失败",
    "completed for {vm.name}": "已完成对 {vm.name} 的操作",
    "failed for {vm.name} on {host.name}": "{vm.name} 在 {host.name} 上的操作失败",
    "on {host.name} in {datacenter.name}": "在 {datacenter.name} 的 {host.name} 上",
    "in {datacenter.name}": "位于 {datacenter.name}",
    "in cluster {cluster.name}": "位于集群 {cluster.name}",
    "by {user.name} on behalf of {proxyuser.name}": "由 {user.name} 代表 {proxyUser.name} 操作",
    "by {user.name} on behalf of {proxyuser.name} on {host.name}": "由 {user.name} 代表 {proxyUser.name} 在 {host.name} 上操作",
    "by {user.name} on host {host.name}": "由 {user.name} 在主机 {host.name} 上操作",
    "by {user.name} in {datacenter.name}": "由 {user.name} 在 {datacenter.name} 中操作",
    "no access": "无访问权限",
    "no permission": "无权限",
    "access denied": "访问被拒绝",
    "authentication required": "需要身份验证",
    "operation not allowed": "不允许的操作",
    "operation not supported": "不支持的操作",
    "operation not available": "操作不可用",
    "feature not available": "功能不可用",
    "feature not licensed": "功能未获得许可",
    "not licensed": "未获得许可",
    "temporarily unavailable": "暂时不可用",
    "permanently unavailable": "永久不可用",
    "pending": "待定",
    "in progress": "进行中",
    "succeeded": "已成功",
    "failed": "失败",
    "timed out": "超时",
    "aborted": "已中止",
    "skipped": "已跳过",
    "completed with errors": "已完成，但有错误",
    "partially completed": "部分完成",
    "status unknown": "状态未知",

    # Event descriptions - DRS / Cluster
    "drs enabled": "DRS 已启用",
    "drs disabled": "DRS 已禁用",
    "drs vm migrated": "DRS 虚拟机已迁移",
    "drs vm powered on": "DRS 虚拟机已打开电源",
    "drs rule created": "DRS 规则已创建",
    "drs rule removed": "DRS 规则已移除",
    "drs rule updated": "DRS 规则已更新",
    "cluster created": "集群已创建",
    "cluster destroyed": "集群已销毁",
    "cluster added": "集群已添加",
    "cluster removed": "集群已移除",
    "cluster reconfigured": "集群已重新配置",
    "cluster resource added": "集群资源已添加",
    "cluster resource removed": "集群资源已移除",

    # Event descriptions - User / Permission
    "user login": "用户登录",
    "user logout": "用户注销",
    "user session terminated": "用户会话已终止",
    "permission added": "权限已添加",
    "permission removed": "权限已移除",
    "permission updated": "权限已更新",
    "role created": "角色已创建",
    "role removed": "角色已移除",
    "role updated": "角色已更新",
    "custom field defined": "自定义字段已定义",
    "custom field renamed": "自定义字段已重命名",
    "custom field removed": "自定义字段已移除",

    # Event descriptions - vSAN
    "vsan cluster configured": "vSAN 集群已配置",
    "vsan cluster deconfigured": "vSAN 集群已取消配置",
    "vsan disk added": "vSAN 磁盘已添加",
    "vsan disk removed": "vSAN 磁盘已移除",
    "vsan disk error": "vSAN 磁盘错误",
    "vsan health check": "vSAN 运行状况检查",
    "vsan resync": "vSAN 重新同步",
    "vsan update": "vSAN 更新",
    "vsan fault": "vSAN 故障",

    # Event descriptions - Network
    "dvs created": "分布式虚拟交换机已创建",
    "dvs removed": "分布式虚拟交换机已移除",
    "dvs reconfigured": "分布式虚拟交换机已重新配置",
    "dvs upgraded": "分布式虚拟交换机已升级",
    "dvs host added": "分布式虚拟交换机主机已添加",
    "dvs host removed": "分布式虚拟交换机主机已移除",
    "dvs port created": "分布式虚拟交换机端口已创建",
    "dvs port removed": "分布式虚拟交换机端口已移除",
    "dvs portgroup created": "分布式虚拟交换机端口组已创建",
    "dvs portgroup removed": "分布式虚拟交换机端口组已移除",
    "dvs portgroup reconfigured": "分布式虚拟交换机端口组已重新配置",
    "network added": "网络已添加",
    "network removed": "网络已移除",
    "network renamed": "网络已重命名",
    "port group created": "端口组已创建",
    "port group removed": "端口组已移除",
    "port group reconfigured": "端口组已重新配置",

    # Event descriptions - Miscellaneous common
    "resource pool created": "资源池已创建",
    "resource pool removed": "资源池已移除",
    "resource pool renamed": "资源池已重命名",
    "resource pool updated": "资源池已更新",
    "storage drs configured": "Storage DRS 已配置",
    "storage drs disabled": "Storage DRS 已禁用",
    "storage drs enabled": "Storage DRS 已启用",
    "license key added": "许可证密钥已添加",
    "license key removed": "许可证密钥已移除",
    "license assignment changed": "许可证分配已更改",
    "profile created": "配置文件已创建",
    "profile removed": "配置文件已移除",
    "profile updated": "配置文件已更新",
    "profile associated": "配置文件已关联",
    "profile dissociated": "配置文件已取消关联",
    "certificate issued": "证书已颁发",
    "certificate revoked": "证书已吊销",
    "certificate renewed": "证书已续订",
    "ca added": "CA 已添加",
    "ca removed": "CA 已移除",
    "tag created": "标签已创建",
    "tag removed": "标签已移除",
    "tag updated": "标签已更新",
    "tag assigned": "标签已分配",
    "tag unassigned": "标签已取消分配",
    "content library created": "内容库已创建",
    "content library removed": "内容库已移除",
    "content library updated": "内容库已更新",
    "content library deployed": "内容库已部署",
    "content library sync": "内容库同步",
    "replication configured": "复制已配置",
    "replication removed": "复制已移除",
    "replication state changed": "复制状态已更改",
    "namespace created": "命名空间已创建",
    "namespace removed": "命名空间已移除",
    "namespace updated": "命名空间已更新",
    "encryption enabled": "加密已启用",
    "encryption disabled": "加密已禁用",
    "encryption rotated": "加密已轮换",
    "crypto key added": "加密密钥已添加",
    "crypto key removed": "加密密钥已移除",

    # Fault descriptions
    "host not reachable": "主机不可达",
    "host connection lost": "主机连接已丢失",
    "host cpu stuck": "主机 CPU 卡住",
    "storage api error": "存储 API 错误",
    "network uplink error": "网络上行链路错误",
    "vm failure": "虚拟机故障",
    "vm error": "虚拟机错误",
    "file system error": "文件系统错误",
    "disk error": "磁盘错误",
    "memory error": "内存错误",
    "fault tolerance error": "Fault Tolerance 错误",
    "invalid state": "状态无效",
    "invalid argument": "参数无效",
    "not supported": "不支持",
    "not implemented": "未实现",
    "timeout": "超时",
    "resource busy": "资源忙",
    "resource exhausted": "资源耗尽",
    "resource in use": "资源使用中",
    "duplicate name": "名称重复",
    "invalid name": "名称无效",
    "insufficient resources": "资源不足",
    "insufficient memory": "内存不足",
    "insufficient disk space": "磁盘空间不足",
    "insufficient cpu": "CPU 不足",
    "already exists": "已存在",
    "not found": "未找到",
    "access denied": "访问被拒绝",
    "authentication failure": "身份验证失败",
    "license error": "许可证错误",
    "license restriction": "许可证限制",
    "concurrent access": "并发访问",
    "file locked": "文件已锁定",
    "file already exists": "文件已存在",
    "directory not empty": "目录非空",
    "io error": "I/O 错误",
    "device error": "设备错误",
    "protocol error": "协议错误",
    "ssl error": "SSL 错误",
    "security error": "安全错误",
    "integrity error": "完整性错误",
    "checksum error": "校验和错误",
    "config error": "配置错误",
    "runtime error": "运行时错误",
    "internal error": "内部错误",
    "fatal error": "致命错误",

    # perf.vmsg counter group descriptions
    "cpu usage": "CPU 使用率",
    "cpu usage in megahertz": "CPU 使用率（以 MHz 为单位）",
    "cpu usage in percentage": "CPU 使用率百分比",
    "memory usage": "内存使用率",
    "memory usage in megabytes": "内存使用率（以 MB 为单位）",
    "disk usage": "磁盘使用率",
    "disk usage in kilobytes": "磁盘使用率（以 KB 为单位）",
    "disk read rate": "磁盘读取速率",
    "disk write rate": "磁盘写入速率",
    "disk read latency": "磁盘读取延迟",
    "disk write latency": "磁盘写入延迟",
    "network usage": "网络使用率",
    "network usage in kilobytes per second": "网络使用率（以 KB/s 为单位）",
    "network received": "网络接收",
    "network transmitted": "网络发送",
    "network packets received": "网络数据包接收",
    "network packets transmitted": "网络数据包发送",
    "network packets dropped": "网络数据包丢弃",
    "datastore usage": "数据存储使用率",
    "datastore read rate": "数据存储读取速率",
    "datastore write rate": "数据存储写入速率",
    "datastore read latency": "数据存储读取延迟",
    "datastore write latency": "数据存储写入延迟",
    "system uptime": "系统运行时间",
    "system resource usage": "系统资源使用率",
    "power consumption": "功耗",
    "power temperature": "电源温度",
    "fan speed": "风扇转速",
    "heartbeat": "心跳",
    "green energy saving": "绿色节能",
    "cluster services cpu": "集群服务 CPU",
    "cluster services memory": "集群服务内存",
    "hbr server": "HBR 服务器",
    "hbr received": "HBR 接收",
    "hbr transmitted": "HBR 发送",
    "vflash module": "VFlash 模块",
    "vflash cache": "VFlash 缓存",
    "vsan dom object": "vSAN DOM 对象",
    "vsan dom component": "vSAN DOM 组件",
    "vsan throughput": "vSAN 吞吐量",
    "vsan iops": "vSAN IOPS",
    "vsan latency": "vSAN 延迟",
    "vsan congestion": "vSAN 拥塞",
    "vvol usage": "vVol 使用率",
    "vvol latency": "vVol 延迟",
    "vvol throughput": "vVol 吞吐量",
}

# Word/phrase replacement (applied within values, preserving surrounding text)
WORD_MAP = {
    # Common terms - these should REMAIN English in most contexts
    # (brand names, tech terms used as proper names)
    # (empty - brand names should stay English)
    
    # Words to translate within sentences
    "user name": "用户名",
    "password": "密码",
    "server": "服务器",
    "client": "客户端",
    "agent": "代理",
    "service": "服务",
    "daemon": "守护进程",
    "manager": "管理器",
    "driver": "驱动程序",
    "device": "设备",
    "network": "网络",
    "storage": "存储",
    "memory": "内存",
    "cpu": "CPU",
    "virtual machine": "虚拟机",
    "virtual disk": "虚拟磁盘",
    "host": "主机",
    "cluster": "集群",
    "datacenter": "数据中心",
    "datastore": "数据存储",
    "folder": "文件夹",
    "resource pool": "资源池",
    "template": "模板",
    "snapshot": "快照",
    "backup": "备份",
    "restore": "恢复",
    "replication": "复制",
    "migration": "迁移",
    "v motion": "vMotion",
    "storage v motion": "Storage vMotion",
    "fault tolerance": "Fault Tolerance",
    "high availability": "高可用性",
    "distributed resource scheduler": "分布式资源调度",
    "drs": "DRS",
    "v sphere": "vSphere",
    "v center": "vCenter",
    "v san": "vSAN",
    "v vol": "vVol",
    "n v d i m m": "NVDIMM",
    "configuration": "配置",
    "provisioning": "置备",
    "allocation": "分配",
    "capacity": "容量",
    "performance": "性能",
    "availability": "可用性",
    "reliability": "可靠性",
    "scalability": "可扩展性",
    "security": "安全性",
    "compliance": "合规性",
    "monitoring": "监控",
    "threshold": "阈值",
    "alert": "警报",
    "notification": "通知",
    "event": "事件",
    "task": "任务",
    "alarm": "警报",
    "permission": "权限",
    "privilege": "特权",
    "role": "角色",
    "user": "用户",
    "group": "组",
    "domain": "域",
    "authentication": "身份验证",
    "authorization": "授权",
    "certificate": "证书",
    "license": "许可证",
    
    # Verbs - past tense
    "created": "已创建",
    "deleted": "已删除",
    "updated": "已更新",
    "modified": "已修改",
    "renamed": "已重命名",
    "changed": "已更改",
    "added": "已添加",
    "removed": "已移除",
    "moved": "已移动",
    "configured": "已配置",
    "enabled": "已启用",
    "disabled": "已禁用",
    "assigned": "已分配",
    "cancelled": "已取消",
    "canceled": "已取消",
    "completed": "已完成",
    "failed": "失败",
    "started": "已启动",
    "stopped": "已停止",
    "connected": "已连接",
    "disconnected": "已断开连接",
    "entered": "已进入",
    "exited": "已退出",
    "registered": "已注册",
    "unregistered": "已注销",
    "upgraded": "已升级",
    "associated": "已关联",
    "dissociated": "已取消关联",
    "issued": "已颁发",
    "revoked": "已吊销",
    "renewed": "已续订",
    "rotated": "已轮换",
    "queued": "已排队",
    "synchronized": "已同步",
    "allocated": "已分配",
    "deallocated": "已取消分配",
    "initialized": "已初始化",
    "installed": "已安装",
    "uninstalled": "已卸载",
    "mounted": "已挂载",
    "unmounted": "已卸载",
    "reconfigured": "已重新配置",
    "resumed": "已恢复",
    "suspended": "已挂起",
    "acknowledged": "已确认",
    "rejected": "已拒绝",
    "approved": "已批准",
    "destroyed": "已销毁",

    # Verbs - present/active
    "creating": "正在创建",
    "deleting": "正在删除",
    "updating": "正在更新",
    "modifying": "正在修改",
    "renaming": "正在重命名",
    "changing": "正在更改",
    "adding": "正在添加",
    "removing": "正在移除",
    "moving": "正在移动",
    "configuring": "正在配置",
    "enabling": "正在启用",
    "disabling": "正在禁用",
    "assigning": "正在分配",
    "transferring": "正在传输",
    "initializing": "正在初始化",
    "validating": "正在验证",
    "migrating": "正在迁移",
    "cloning": "正在克隆",
    "deploying": "正在部署",
    "installing": "正在安装",
    "reconfiguring": "正在重新配置",
    "synchronizing": "正在同步",
    "processing": "正在处理",
    "scanning": "正在扫描",
    "monitoring": "正在监控",

    # Verbs - base form
    "create": "创建",
    "delete": "删除",
    "update": "更新",
    "modify": "修改",
    "rename": "重命名",
    "change": "更改",
    "add": "添加",
    "remove": "移除",
    "move": "移动",
    "configure": "配置",
    "enable": "启用",
    "disable": "禁用",
    "assign": "分配",
    "select": "选择",
    "specify": "指定",
    "define": "定义",
    "set": "设置",
    "reset": "重置",
    "clear": "清除",
    "apply": "应用",
    "cancel": "取消",
    "confirm": "确认",
    "save": "保存",
    "load": "加载",
    "reload": "重新加载",
    "refresh": "刷新",
    "release": "释放",
    "acquire": "获取",
    "generate": "生成",
    "validate": "验证",
    "verify": "验证",
    "test": "测试",
    "restart": "重新启动",
    "shutdown": "关机",
    "power": "电源",
    "login": "登录",
    "logout": "注销",
    "connect": "连接",
    "disconnect": "断开连接",
    "mount": "挂载",
    "unmount": "卸载",
    "install": "安装",
    "uninstall": "卸载",
    "register": "注册",
    "unregister": "注销",
    "upgrade": "升级",
    "downgrade": "降级",
    "import": "导入",
    "export": "导出",
    "deploy": "部署",
    "migrate": "迁移",
    "clone": "克隆",
    "backup": "备份",
    "restore": "恢复",
    "replicate": "复制",
    "sync": "同步",
    "merge": "合并",
    "split": "拆分",
    "attach": "附加",
    "detach": "分离",
    "lock": "锁定",
    "unlock": "解锁",
    
    # Technical terms (translate)
    "port": "端口",
    "port group": "端口组",
    "vlan": "VLAN",
    "ip address": "IP 地址",
    "mac address": "MAC 地址",
    "subnet": "子网",
    "gateway": "网关",
    "dns": "DNS",
    "dhcp": "DHCP",
    "ntp": "NTP",
    "snmp": "SNMP",
    "smb": "SMB",
    "nfs": "NFS",
    "iscsi": "iSCSI",
    "fibre channel": "Fibre Channel",
    "fcoe": "FCoE",
    "raid": "RAID",
    "disk": "磁盘",
    "partition": "分区",
    "volume": "卷",
    "file system": "文件系统",
    "log": "日志",
    "logging": "日志记录",
    "audit": "审核",
    "debug": "调试",
    "error": "错误",
    "warning": "警告",
    "critical": "严重",
    "information": "信息",
    "verbose": "详细",
    
    # Descriptions
    "description": "描述",
    "summary": "摘要",
    "label": "标签",
    "name": "名称",
    "status": "状态",
    "state": "状态",
    "type": "类型",
    "category": "类别",
    "value": "值",
    "key": "键",
    "id": "ID",
    "version": "版本",
    "size": "大小",
    "total": "总计",
    "free": "空闲",
    "used": "已用",
    "available": "可用",
    "percentage": "百分比",
    "count": "计数",
    "enabled": "已启用",
    "disabled": "已禁用",
    "enable": "启用",
    "disable": "禁用",
    "active": "活动",
    "inactive": "非活动",
    "valid": "有效",
    "invalid": "无效",
    "read only": "只读",
    "read write": "读写",
    "supported": "支持",
    "unsupported": "不支持",
    "configured": "已配置",
    "unconfigured": "未配置",

    # Time-related
    "seconds": "秒",
    "minutes": "分钟",
    "hours": "小时",
    "days": "天",
    "weeks": "周",
    "months": "月",
    "years": "年",
    "current": "当前",
    "previous": "上一个",
    "next": "下一个",
    "interval": "间隔",
    "frequency": "频率",
    "duration": "持续时间",
    "timeout": "超时",
    "delay": "延迟",
    "retry": "重试",

    # Resources
    "resource": "资源",
    "resources": "资源",
    "allocation": "分配",
    "reservation": "预留",
    "limit": "限制",
    "share": "份额",
    "shares": "份额",
    "overhead": "开销",
    "consumed": "已消耗",
    "reserved": "已预留",
    "unreserved": "未预留",
    "provisioned": "已置备",
    "usage": "使用率",
    "utilization": "利用率",
    "demand": "需求",
    "entitlement": " entitlement ",
    "overhead": "开销",
    "latency": "延迟",
    "throughput": "吞吐量",
    "iops": "IOPS",

    # Power management
    "power": "电源",
    "energy": "能耗",
    "consumption": "消耗",
    "battery": "电池",
    "temperature": "温度",
    "voltage": "电压",
    "current": "电流",
    "fan": "风扇",
    "cooling": "散热",
    "acoustic": "噪音",

    # Network
    "bandwidth": "带宽",
    "throughput": "吞吐量",
    "packet": "数据包",
    "packets": "数据包",
    "dropped": "丢弃",
    "errors": "错误",
    "broadcast": "广播",
    "multicast": "组播",
    "unicast": "单播",
    "transmit": "发送",
    "receive": "接收",
    "transmitted": "已发送",
    "received": "已接收",
    "pnic": "物理网卡",
    "vnic": "虚拟网卡",
    "uplink": "上行链路",
    "downlink": "下行链路",
    "vlan": "VLAN",
    "mtu": "MTU",
    "jumbo": "巨型帧",

    # Virtual hardware
    "vcpu": "vCPU",
    "vmemory": "vMemory",
    "vdisk": "虚拟磁盘",
    "vnic": "虚拟网卡",
    "vhba": "虚拟 HBA",
    "scsi": "SCSI",
    "sata": "SATA",
    "ide": "IDE",
    "nvme": "NVMe",
    "usb": "USB",
    "sound": "声卡",
    "serial": "串口",
    "parallel": "并口",
    "floppy": "软驱",
    "cdrom": "光驱",
    "numa": "NUMA",
    "numa node": "NUMA 节点",

    # Storage
    "lun": "LUN",
    "volume": "卷",
    "partition": "分区",
    "filesystem": "文件系统",
    "filesystem": "文件系统",
    "format": "格式",
    "block": "块",
    "block size": "块大小",
    "sector": "扇区",
    "strip": "条带",
    "raid": "RAID",
    "mirror": "镜像",
    "snapshot": "快照",
    "thin provisioning": "精简置备",
    "thick provisioning": "厚置备",
    "deduplication": "去重",
    "compression": "压缩",
    "encryption": "加密",
    "checksum": "校验和",
    "vvol": "vVol",
    "vvols": "vVol",
}


def translate_value(val):
    """Translate an English value string to Chinese."""
    if not val:
        return val
    
    # Strip quotes if present
    stripped = val.strip()
    had_quotes = False
    if stripped.startswith('"') and stripped.endswith('"'):
        val = stripped[1:-1]
        had_quotes = True
    
    if not val:
        return ('"' + val + '"') if had_quotes else val
    
    # Check full-value match first (case-insensitive)
    val_lower = val.lower().strip()
    if val_lower in FULL_VALUE_MAP:
        result = FULL_VALUE_MAP[val_lower]
        return ('"' + result + '"') if had_quotes else result
    
    # preserve-only patterns - values that should stay in English
    preserve_patterns = [
        r'^<\w+>$',  # <Event>, <internal>
        r'^[\w\-]+$',  # single word identifiers like "strong", "weak"
        r'^[A-Z][a-z]+(\.[A-Z][a-z]+)+$',  # CamelCase.Identifiers
        r'^(Linked Mode|Workflow Orchestration Engine|Stretched Cluster)$',
    ]
    for pat in preserve_patterns:
        if re.match(pat, val):
            return ('"' + val + '"') if had_quotes else val
    
    # Check if value contains placeholders - if so, translate around them
    # OVFTool uses {placeholder} syntax
    parts = re.split(r'(\{[^}]+\})', val)
    if len(parts) > 1:
        translated_parts = []
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                translated_parts.append(part)  # Keep placeholder
            else:
                translated_parts.append(apply_word_map(part))
        result = ''.join(translated_parts)
    else:
        result = apply_word_map(val)
    
    return ('"' + result + '"') if had_quotes else result


def apply_word_map(text):
    """Apply word-level dictionary replacements to a text string."""
    if not text.strip():
        return text
    
    # Sort by length (longest first) to avoid partial matches
    sorted_words = sorted(WORD_MAP.items(), key=lambda x: -len(x[0]))
    
    result = text
    for eng, chn in sorted_words:
        # Case-insensitive replace, but only whole words
        pattern = re.compile(re.escape(eng), re.IGNORECASE)
        result = pattern.sub(chn, result)
    
    return result


def fix_mixed_english(text):
    """Post-process to fix mixed Chinese-English patterns."""
    # Fix patterns like "用户 name" → "用户名" (Chinese + English word)
    # These happen when the dictionary partially translated
    result = text
    fixes = [
        (r'用户\s+name', '用户名'),
        (r'用户\s+Name', '用户名'),
        (r'警报\s+task', '警报任务'),
        (r'警报\s+Task', '警报任务'),
        (r'虚拟机ware', 'VMware'),
        (r'活动\s+目录', 'Active Directory'),
        (r'高\s+Availability', '高可用性'),
        (r'高\s+可用性', '高可用性'),
        (r'打开\s+Manage', 'OpenManage'),
        (r'网络\s+Login', '网络登录'),
        (r'网络\s+Backup', '网络备份'),
        (r'本地\s+Security', '本地安全'),
        (r'身份验证\s+服务器', '认证服务器'),
        (r'备份\s+Exec', 'Backup Exec'),
        (r'Net\s+备份', 'NetBackup'),
        (r'备份\s+Agent', 'Backup Agent'),
        (r'更新\s+管理器', 'Update Manager'),
        (r'集群ing', '集群'),
        (r'集群\s+ing', '集群'),
        (r'数据\s+center', 'Data Center'),
        (r'电源\s+management', '电源管理'),
        (r'性能\s+degraded', '性能降级'),
        (r'运行状况\s+status', '运行状况状态'),
        (r'全部\s+data', '全部数据'),
        (r'序列\s+port', '串口'),
        (r'串口\s+port', '串口'),
        (r'Direct\s+控制台', 'Direct Console'),
        (r'写入s', '写入'),
        (r'读取\s+and/or', '读取和/或'),
        (r'写入\s+persistency', '写入持久性'),
        (r'查询\s+服务', '查询服务'),
        (r'服务\s+Provider', '服务提供商'),
        (r'配置\s+Manager', '配置管理器'),
        (r'配置\s+manager', '配置管理器'),
        (r'存储\s+管理器', 'Storage Manager'),
        (r'存储\s+管理', '存储管理'),
        (r'文件\s+管理器', '文件管理器'),
        (r'设备\s+Manager', 'Device Manager'),
        (r'令牌\s+服务', '令牌服务'),
        (r'时间\s+服务', '时间服务'),
        (r'活动\s+Directory', 'Active Directory'),
        (r'许可证\s+Client', 'License Client'),
        (r'net\s+backup', 'NetBackup'),
        (r'备份\s+Manager', 'Backup Manager'),
        (r'管理\s+Agent', 'Manager Agent'),
        (r'代理\s+Agent', '代理'),
        (r'服务\s+Service', '服务'),
        (r'客户\s+端', '客户端'),
        (r'连接ed', '连接'),
        (r'启动ed', '启动'),
        (r'完成ed', '完成'),
        (r'删除ed', '删除'),
        (r'配置d', '配置'),
        (r'创建ed', '创建'),
        (r'移动ed', '移动'),
        (r'更改ed', '更改'),
        (r'迁移ed', '迁移'),
        (r'克隆ed', '克隆'),
        (r'更新ed', '更新'),
        (r'禁用d', '禁用'),
        (r'启用d', '启用'),
        (r'中断ed', '中断'),
        (r'重新启动ed', '重新启动'),
        (r'失败ed', '失败'),
        (r'注销ed', '注销'),
        (r'注册ed', '注册'),
        (r'挂起ed', '挂起'),
        (r'恢复ed', '恢复'),
        (r'重置ed', '重置'),
        (r'降级d', '降级'),
        (r'重命名ed', '重命名'),
        (r'重新配置d', '重新配置'),
        (r'重新加载ed', '重新加载'),
        (r'刷新ed', '刷新'),
        (r'打开ed', '打开'),
        (r'关闭ed', '关闭'),
        (r'分配ed', '分配'),
        (r'取消分配ed', '取消分配'),
        (r'关联ed', '关联'),
        (r'取消关联ed', '取消关联'),
        (r'导出ed', '导出'),
        (r'导入ed', '导入'),
        (r'部署ed', '部署'),
        (r'上传ed', '上传'),
        (r'下载ed', '下载'),
        (r'发布ed', '发布'),
        (r'吊销ed', '吊销'),
        (r'续订ed', '续订'),
        (r'轮换ed', '轮换'),
        (r'同步ed', '同步'),
        (r'格式化ed', '格式化'),
        (r'隔离ed', '隔离'),
        (r'vm 的', 'VM 的'),
        (r'的 vm', '的 VM'),
        (r'对于 the', '的'),
        (r'in the', '在'),
        (r'of the', '的'),
        (r'to the', '到'),
        (r'for the', '的'),
        (r'by a', '由'),
        (r'by an', '由'),
        (r'on the', '在'),
        (r'is not', '不'),
        (r'is the', '是'),
        (r'The number of', '数量'),
        (r'The maximum number of', '最大数量'),
        (r'The minimum number of', '最小数量'),
        (r'The total amount of', '总量'),
        (r'This is the', '这是'),
        (r'This represents the', '这表示'),
        (r'This specifies the', '这指定'),
        (r'This defines the', '这定义'),
        (r'This indicates the', '这指示'),
        (r'This determines the', '这决定'),
        (r'This controls the', '这控制'),
        (r'This sets the', '这设置'),
        (r'This enables', '这启用'),
        (r'This disables', '这禁用'),
        (r'This option', '此选项'),
        (r'This parameter', '此参数'),
        (r'This value', '此值'),
        (r'This setting', '此设置'),
        (r'This field', '此字段'),
        (r'This flag', '此标志'),
        (r'The value of', '值'),
        (r'The name of', '名称'),
        (r'The path of', '路径'),
        (r'The size of', '大小'),
        (r'The state of', '状态'),
        (r'The status of', '状态'),
        (r'The type of', '类型'),
        (r'The location of', '位置'),
        (r'The interval', '间隔'),
        (r'The duration', '持续时间'),
        (r'The timeout', '超时'),
        (r'The threshold', '阈值'),
        (r'The limit', '限制'),
        (r'The policy', '策略'),
        (r'The priority', '优先级'),
        (r'with the', '使用'),
        (r'from the', '从'),
        (r'不能 be', '不能'),
        (r'可以 be', '可以'),
        (r'应该 be', '应该'),
        (r'必须 be', '必须'),
        (r'将 be', '将'),
        (r'已 be', '已'),
        (r'正在 be', '正在'),
        (r'which is', '——'),
        (r'which are', '——'),
        (r'which has', '具有'),
        (r'which have', '具有'),
        (r'that is', '——'),
        (r'that are', '——'),
        (r'that has', '具有'),
        (r'per second', '每秒'),
        (r'per minute', '每分钟'),
        (r'per hour', '每小时'),
        (r'per day', '每天'),
        (r'per vm', '每台虚拟机'),
        (r'per host', '每台主机'),
        (r'per datastore', '每个数据存储'),
        (r'per cluster', '每个集群'),
        (r'in milliseconds', '（毫秒）'),
        (r'in seconds', '（秒）'),
        (r'in minutes', '（分钟）'),
        (r'in hours', '（小时）'),
        (r'in days', '（天）'),
        (r'in megabytes', '（MB）'),
        (r'in kilobytes', '（KB）'),
        (r'in gigabytes', '（GB）'),
        (r'in bytes', '（字节）'),
        (r'in hertz', '（Hz）'),
        (r'in percentage', '百分比'),
        (r'in percent', '百分比'),
        (r'If set to true', '如果设置为 true'),
        (r'If set to false', '如果设置为 false'),
        (r'If enabled', '如果启用'),
        (r'If disabled', '如果禁用'),
        (r'If true', '如果为 true'),
        (r'If false', '如果为 false'),
        (r'Default value', '默认值'),
        (r'Default is', '默认为'),
        (r'Defaults to', '默认为'),
        (r'no default', '无默认值'),
        (r'Range:', '范围：'),
        (r'between', '介于'),
        (r'\band\b', '和'),
        (r'through', '到'),
        (r'via', '通过'),
        (r'using', '使用'),
        (r'based on', '基于'),
        (r'according to', '根据'),
        (r'depending on', '取决于'),
        (r'regardless of', '无论'),
        (r'in addition to', '除...之外'),
        (r'as well as', '以及'),
        (r'such as', '例如'),
        (r'for example', '例如'),
        (r'e\.g\.', '例如'),
        (r'Un限制ed\s+virtual\s+SMP', '无限制虚拟 SMP'),
        (r'Un限制ed', '无限制的'),
        (r'Stretched\s+集群', '拉伸集群'),
        (r'i\.e\.', '即'),
        (r'etc\.', '等'),
        (r'Note:', '注意：'),
        (r'NOTE:', '注意：'),
    ]
    for pattern, replacement in fixes:
        result = re.sub(pattern, replacement, result)
    return result


def process_file(filename):
    """Process a single .vmsg file."""
    if filename in SKIP_FILES:
        print(f"  SKIPPED: {filename} (in skip list)")
        return None
    
    en_path = os.path.join(EN_DIR, filename)
    zh_path = os.path.join(ZH_DIR, filename)
    
    if not os.path.exists(en_path):
        return None
    
    with open(en_path, 'r', encoding='utf-8') as f:
        en_lines = f.readlines()
    
    # Read existing zh-CN if available (to preserve header)
    zh_lines = []
    if os.path.exists(zh_path):
        with open(zh_path, 'r', encoding='utf-8') as f:
            zh_lines = f.readlines()
    
    translated = []
    stats = {'total': 0, 'translated': 0, 'kept': 0}
    
    for i, line in enumerate(en_lines):
        stripped = line.rstrip('\n')
        
        # Preserve header lines, comments, separators
        if not stripped or stripped.startswith('#') or stripped.startswith('sig') or stripped.startswith('###') or stripped.startswith('##'):
            # Check if zh-CN has a corresponding line with Chinese in header
            if i < len(zh_lines) and zh_lines[i].strip().startswith('#') and 'zh_CN' in zh_lines[i]:
                translated.append(zh_lines[i].rstrip('\n'))
            elif re.match(r'^#\s*en_\w*\s*resources$', stripped.strip()):
                translated.append('# zh_CN resources')
            else:
                translated.append(stripped)
            continue
        
        # Process key=value lines
        if '=' in stripped:
            parts = stripped.split('=', 1)
            key = parts[0].rstrip()
            val = parts[1]
            
            # Check if this key's value should be translated
            stats['total'] += 1
            
            # Check if it's a proper name service label (keep English for many)
            # Service labels, firewall labels, vendor product names → keep mostly English
            # But check if current zh-CN already has a good translation
            
            # Apply translation
            new_val = translate_value(val)
            
            translated.append(key + '=' + new_val)
            if new_val != val:
                stats['translated'] += 1
            else:
                stats['kept'] += 1
        else:
            translated.append(stripped)
    
    # Write output
    output = '\n'.join(translated)
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    # Fix mixed Chinese-English patterns
    output = fix_mixed_english(output)
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(output)
    
    return stats


SKIP_FILES = {
    "eventaux.vmsg",  # XML event descriptions - translated manually via subagent
    "evc.vmsg",       # EVC mode descriptions - translated manually via subagent
}

def main():
    files_to_process = [  # all 21 files
        "event.vmsg", "option.vmsg", "task.vmsg", "perf.vmsg",
        "locmsg.vmsg", "enum.vmsg",
        "auth.vmsg", "fault.vmsg", "vm.vmsg", "alarm.vmsg",
        "default.vmsg", "host.vmsg", "ovftool.vmsg",
        "action.vmsg", "cluster.vmsg",
        "ovftool-warning.vmsg", "question.vmsg", "stask.vmsg",
        "gos.vmsg",  # OS names - keep mostly English
    ]
    
    print("Processing OVFTool files with enhanced dictionary translation...")
    print(f"{'File':<20} {'Total':<8} {'Translated':<12} {'Kept':<8}")
    print("-" * 50)
    
    total_stats = {'total': 0, 'translated': 0, 'kept': 0}
    for fname in files_to_process:
        stats = process_file(fname)
        if stats:
            print(f"{fname:<20} {stats['total']:<8} {stats['translated']:<12} {stats['kept']:<8}")
            for k in total_stats:
                total_stats[k] += stats[k]
    
    print("-" * 50)
    print(f"{'TOTAL':<20} {total_stats['total']:<8} {total_stats['translated']:<12} {total_stats['kept']:<8}")
    print(f"\nDictionary coverage: {total_stats['translated']*100//max(total_stats['total'],1)}%")
    
    # Also fix mixed Chinese-English in all files as a final pass
    print("\nRunning mixed Chinese-English fix pass...")
    for fname in files_to_process:
        zh_path = os.path.join(ZH_DIR, fname)
        if os.path.exists(zh_path):
            with open(zh_path, 'r', encoding='utf-8') as f:
                content = f.read()
            fixed = fix_mixed_english(content)
            with open(zh_path, 'w', encoding='utf-8') as f:
                f.write(fixed)
    
    print("Done!")

if __name__ == '__main__':
    main()
