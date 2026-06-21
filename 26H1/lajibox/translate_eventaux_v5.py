#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Translate eventaux.vmsg - safe multi-word phrase replacement."""
import re

EN_FILE = r'd:\vmware\i18n\OVFTool\env\en\eventaux.vmsg'
ZH_FILE = r'd:\vmware\i18n\OVFTool\env\zh-CN\eventaux.vmsg'

ENAMES = {
    "HostInventoryFullEvent":"主机清单已满事件","LicenseNonComplianceEvent":"许可证不合规事件",
    "LicenseServerUnavailableEvent":"许可证服务器不可用事件","NoLicenseEvent":"无许可证事件",
    "InvalidEditionEvent":"无效版本事件","HostLicenseExpiredEvent":"主机许可证已过期事件",
    "VMotionLicenseExpiredEvent":"VMotion许可证已过期事件","LicenseRestrictedEvent":"许可证受限事件",
    "VmFailedToPowerOffEvent":"虚拟机无法关闭电源事件","VmFailedToPowerOnEvent":"虚拟机无法打开电源事件",
    "VmFailedToRebootGuestEvent":"虚拟机无法重新启动客户机事件","VmFailedToResetEvent":"虚拟机无法重置事件",
    "VmUpgradingEvent":"虚拟机正在升级事件","VmUuidAssignedEvent":"虚拟机UUID已分配事件",
    "VmInstanceUuidAssignedEvent":"虚拟机实例UUID已分配事件","VmUuidChangedEvent":"虚拟机UUID已更改事件",
    "VmInstanceUuidChangedEvent":"虚拟机实例UUID已更改事件","VmInstanceUuidConflictEvent":"虚拟机实例UUID冲突事件",
    "VmRelocateFailedEvent":"虚拟机重新定位失败事件","VmUnsupportedStartingEvent":"虚拟机不支持启动事件",
    "VmFailedToShutdownGuestEvent":"虚拟机无法关闭客户机事件","AlarmEmailFailedEvent":"警报邮件发送失败事件",
    "AlarmReconfiguredEvent":"警报已重新配置事件","AlarmScriptFailedEvent":"警报脚本失败事件",
    "AlarmSnmpFailedEvent":"警报SNMP失败事件","ScheduledTaskEmailFailedEvent":"计划任务邮件发送失败事件",
    "ScheduledTaskFailedEvent":"计划任务失败事件","DasAgentUnavailableEvent":"Das代理不可用事件",
    "DasDisabledEvent":"Das已禁用事件","DasEnabledEvent":"Das已启用事件",
    "HostDasEnablingEvent":"主机Das正在启用事件","InsufficientFailoverResourcesEvent":"故障切换资源不足事件",
    "VmDasBeingResetEvent":"虚拟机Das正在重置事件","VmDasBeingResetWithScreenshotEvent":"虚拟机Das正在带截图重置事件",
    "VmDasResetFailedEvent":"虚拟机Das重置失败事件","VmFailoverFailed":"虚拟机故障切换失败",
    "VmMaxRestartCountReached":"虚拟机达到最大重新启动次数","VmPowerOffOnIsolationEvent":"虚拟机隔离时关闭电源事件",
    "VmShutdownOnIsolationEvent":"虚拟机隔离时关机事件","VmAutoRenameEvent":"虚拟机自动重命名事件",
    "VmBeingDeployedEvent":"虚拟机正在部署事件","VmBeingHotMigratedEvent":"虚拟机正在热迁移事件",
    "DatastoreDiscoveredEvent":"数据存储已发现事件","DatastoreRenamedOnHostEvent":"数据存储已在主机上重命名事件",
    "VMFSDatastoreExtendedEvent":"VMFS数据存储已扩展事件","VMFSDatastoreExpandedEvent":"VMFS数据存储已扩容事件",
    "VmConfigMissingEvent":"虚拟机配置缺失事件","VmDeployedEvent":"虚拟机已部署事件",
    "VmMacChangedEvent":"虚拟机MAC地址已更改事件","VmMacConflictEvent":"虚拟机MAC地址冲突事件",
    "VmOrphanedEvent":"虚拟机孤立事件","VmConnectedEvent":"虚拟机已连接事件",
    "MigrationErrorEvent":"迁移错误事件","MigrationHostErrorEvent":"迁移主机错误事件",
    "VmBeingMigratedEvent":"虚拟机正在迁移事件","VmMigratedEvent":"虚拟机已迁移事件",
    "VmBeingRelocatedEvent":"虚拟机正在重新定位事件","VmRelocatedEvent":"虚拟机已重新定位事件",
    "VmCloneFailedEvent":"虚拟机克隆失败事件","MigrationHostWarningEvent":"迁移主机警告事件",
    "MigrationResourceErrorEvent":"迁移资源错误事件","MigrationResourceWarningEvent":"迁移资源警告事件",
    "VmDeployFailedEvent":"虚拟机部署失败事件","VmDiskFailedEvent":"虚拟机磁盘失败事件",
    "VmFailedMigrateEvent":"虚拟机迁移失败事件","VmFailedRelayoutOnVmfs2DatastoreEvent":"虚拟机在VMFS2数据存储上布局失败事件",
    "VmFailedRelayoutEvent":"虚拟机布局失败事件","VmAcquiredMksTicketEvent":"虚拟机已获取Mks票证事件",
    "VmWwnAssignedEvent":"虚拟机WWN已分配事件","VmWwnChangedEvent":"虚拟机WWN已更改事件",
    "VmWwnConflictEvent":"虚拟机WWN冲突事件","VmReloadFromPathFailedEvent":"虚拟机从路径重新加载失败事件",
    "CustomizationLinuxIdentityFailed":"自定义Linux标识失败","CustomizationNetworkSetupFailed":"自定义网络设置失败",
    "CustomizationSysprepFailed":"自定义Sysprep失败","CustomizationUnknownFailure":"自定义未知失败",
    "VmFailedStartingSecondaryEvent":"虚拟机启动辅助虚拟机失败事件","VmFailedUpdatingSecondaryConfig":"虚拟机更新辅助配置失败事件",
    "VmFaultToleranceStateChangedEvent":"虚拟机FaultTolerance状态已更改事件",
    "VmFaultToleranceTurnedOffEvent":"虚拟机FaultTolerance已关闭事件","VmFaultToleranceVmTerminatedEvent":"虚拟机FaultTolerance已终止事件",
    "VmMaxFTRestartCountReached":"虚拟机达到最大FT重新启动次数","VmNoCompatibleHostForSecondaryEvent":"虚拟机无兼容辅助主机事件",
    "VmSecondaryDisabledBySystemEvent":"虚拟机辅助已由系统禁用事件","VmTimedoutStartingSecondaryEvent":"虚拟机启动辅助超时事件",
    "CanceledHostOperationEvent":"已取消主机操作事件","ChangeOwnerOfFileFailedEvent":"更改文件所有者失败事件",
    "HostAddFailedEvent":"主机添加失败事件","HostAdminDisableEvent":"主机管理员禁用事件",
    "HostAdminEnableEvent":"主机管理员启用事件","HostCnxFailedAccountFailedEvent":"主机连接因帐户失败而失败事件",
    "HostCnxFailedAlreadyManagedEvent":"主机连接因已被管理而失败事件","HostCnxFailedBadCcagentEvent":"主机连接因代理故障而失败事件",
    "HostCnxFailedBadUsernameEvent":"主机连接因用户名错误而失败事件","HostCnxFailedBadVersionEvent":"主机连接因版本不兼容而失败事件",
    "HostCnxFailedCcagentUpgradeEvent":"主机连接因代理升级而失败事件","HostCnxFailedEvent":"主机连接失败事件",
    "HostCnxFailedNetworkErrorEvent":"主机连接因网络错误而失败事件","HostCnxFailedNoAccessEvent":"主机连接因无访问权限而失败事件",
    "HostCnxFailedNoConnectionEvent":"主机连接因无连接而失败事件","HostCnxFailedNoLicenseEvent":"主机连接因无许可证而失败事件",
    "HostCnxFailedNotFoundEvent":"主机连接因未找到而失败事件","HostCnxFailedTimeoutEvent":"主机连接超时失败事件",
    "HostConnectionLostEvent":"主机连接丢失事件","HostReconnectionFailedEvent":"主机重新连接失败事件",
    "TimedOutHostOperationEvent":"主机操作超时事件","AccountCreatedEvent":"帐户已创建事件",
    "AccountRemovedEvent":"帐户已移除事件","AccountUpdatedEvent":"帐户已更新事件",
    "AdminPasswordNotChangedEvent":"管理员密码未更改事件","BadUsernameSessionEvent":"用户名错误会话事件",
    "ErrorUpgradeEvent":"升级错误事件","GeneralHostErrorEvent":"常规主机错误事件",
    "GeneralHostInfoEvent":"常规主机信息事件","GeneralHostWarningEvent":"常规主机警告事件",
    "GeneralUserEvent":"常规用户事件","GeneralVmErrorEvent":"常规虚拟机错误事件",
    "GeneralVmInfoEvent":"常规虚拟机信息事件","GeneralVmWarningEvent":"常规虚拟机警告事件",
    "HostSyncFailedEvent":"主机同步失败事件","HostUpgradeFailedEvent":"主机升级失败事件",
    "NoAccessUserEvent":"无访问权限用户事件","SessionTerminatedEvent":"会话已终止事件",
    "TaskTimeoutEvent":"任务超时事件","UserUpgradeEvent":"用户升级事件",
    "VcAgentUninstalledEvent":"VC代理已卸载事件","VcAgentUninstallFailedEvent":"VC代理卸载失败事件",
    "VcAgentUpgradedEvent":"VC代理已升级事件","VcAgentUpgradeFailedEvent":"VC代理升级失败事件",
    "VimAccountPasswordChangedEvent":"Vim帐户密码已更改事件","VmMessageErrorEvent":"虚拟机消息错误事件",
    "VmMessageEvent":"虚拟机消息事件","VmMessageWarningEvent":"虚拟机消息警告事件",
    "DvsHostWentOutOfSyncEvent":"Dvs主机已失步事件","GhostDvsProxySwitchDetectedEvent":"检测到幽灵Dvs代理交换机事件",
    "IncorrectHostInformationEvent":"主机信息不正确事件","HostWwnConflictEvent":"主机WWN冲突事件",
    "HostIpChangedEvent":"主机IP已更改事件","DrsExitStandbyModeFailedEvent":"DRS退出待机模式失败事件",
    "ClusterOvercommittedEvent":"集群超量使用事件","ResourceViolatedEvent":"资源违规事件",
    "HostComplianceCheckedEvent":"主机合规性已检查事件","ClusterComplianceCheckedEvent":"集群合规性已检查事件",
    "HostNonCompliantEvent":"主机不合规事件","ClusterReconfiguredEvent":"集群已重新配置事件",
    "ClusterStatusChangedEvent":"集群状态已更改事件","DrsInvocationFailedEvent":"DRS调用失败事件",
    "DrsResourceConfigureFailedEvent":"DRS资源配置失败事件","DrsVmMigratedEvent":"DRS虚拟机已迁移事件",
    "DrsVmPoweredOnEvent":"DRS虚拟机已打开电源事件","HostOvercommittedEvent":"主机超量使用事件",
    "HostStatusChangedEvent":"主机状态已更改事件","NoMaintenanceModeDrsRecommendationForVM":"虚拟机无维护模式DRS建议",
    "NotEnoughResourcesToStartVmEvent":"资源不足无法启动虚拟机事件","ResourcePoolReconfiguredEvent":"资源池已重新配置事件",
    "DasHostIsolatedEvent":"Das主机已隔离事件","HostMissingNetworksEvent":"主机缺少网络事件",
    "HostExtraNetworksEvent":"主机额外网络事件","HostNoHAEnabledPortGroupsEvent":"主机无HA启用端口组事件",
    "HostNoAvailableNetworksEvent":"主机无可用网络事件",
    "HostIsolationIpPingFailedEvent":"主机隔离IP连通测试失败事件",
    "HostNoRedundantManagementNetworkEvent":"主机无冗余管理网络事件",
    "HostIpToShortNameFailedEvent":"主机IP转短名称失败事件","HostGetShortNameFailedEvent":"主机获取短名称失败事件",
    "HostPrimaryAgentNotShortNameEvent":"主机主代理非短名称事件","HostShortNameInconsistentEvent":"主机短名称不一致事件",
    "HostShortNameToIpFailedEvent":"主机短名称转IP失败事件",
}

SAFE = [
    ("vCenter Server-specific instance UUID","vCenter Server 特定的实例 UUID"),
    ("vCenter Server Foundation license key","vCenter Server Foundation 许可证密钥"),
    ("Summary tab for the virtual machine","虚拟机的摘要选项卡"),
    ("virtual machine remote console","虚拟机远程控制台"),
    ("guest operating system","客户机操作系统"),
    ("host isolation response","主机隔离响应"),
    ("vSphere Distributed Switch proxy switch","vSphere Distributed Switch 代理交换机"),
    ("vSphere Distributed Switch","vSphere Distributed Switch"),
    ("admission control","准入控制"),
    ("heartbeat datastores","心跳数据存储"),
    ("proxy switch","代理交换机"),
    ("host profile","主机配置文件"),
    ("cluster profile","集群配置文件"),
    ("Management Traffic","管理流量"),
    ("Maintenance Mode","维护模式"),
    ("Standby Mode","待机模式"),
    ("Lockdown Mode","锁定模式"),
    ("Service Console","服务控制台"),
    ("configuration file","配置文件"),
    ("resource pool","资源池"),
    ("license key","许可证密钥"),
    ("MAC address","MAC 地址"),
    ("IP address","IP 地址"),
    ("BIOS UUID","BIOS UUID"),
    ("instance UUID","实例 UUID"),
    ("virtual NIC","虚拟 NIC"),
    ("host name","主机名"),
    ("domain name","域名"),
    ("port group","端口组"),
    ("virtual machine","虚拟机"),
    ("virtual hardware","虚拟硬件"),
    ("Fault Tolerance","Fault Tolerance"),
    ("VMware Tools Service","VMware Tools Service"),
    ("VMware Tools","VMware Tools"),
    ("vSphere Client","vSphere Client"),
    ("vCenter Server","vCenter Server"),
    ("vSphere HA","vSphere HA"),
    ("network isolated","网络隔离"),
    ("power state","电源状态"),
    ("management network","管理网络"),
    ("default gateway","默认网关"),
    ("power on","打开电源"),
    ("power off","关闭电源"),
    ("powered on","已打开电源"),
    ("powered off","已关闭电源"),
    ("not responding","无响应"),
    ("NIC teaming","NIC 组合"),
    ("screenshot image","屏幕截图"),
    ("Active Directory","Active Directory"),
    ("Local System","本地系统"),
    ("open-vm-tools","open-vm-tools"),
]
SAFE.sort(key=lambda x: -len(x[0]))

def apply_safe(text):
    r = text
    for e, c in SAFE:
        if c != e: r = r.replace(e, c)
    return r

def fix_ids(text):
    def r(m):
        return 'id="vim.\u4e8b\u4ef6.' + ENAMES.get(m.group(1), m.group(1)) + '"'
    return re.sub(r'id="vim\.event\.([^"]+)"', r, text)

with open(EN_FILE, 'r', encoding='utf-8') as f:
    en = f.read()

zh = fix_ids(en)
zh = zh.replace('# en_US resources', '# zh_CN resources', 1)
zh = re.sub(r'(>)([^<]+?)(\s*<)', lambda m: m.group(1) + apply_safe(m.group(2)) + m.group(3), zh)

with open(ZH_FILE, 'w', encoding='utf-8') as f:
    f.write(zh)

n = len(re.findall(r'\.longDescription\s*=', en))
print(f"Done! {n} events. Output: {ZH_FILE}")
