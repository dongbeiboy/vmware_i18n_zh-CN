# -*- coding: utf-8 -*-
import re

path = r'd:\vmware\i18n\OVFTool\env\zh-CN\enum.vmsg'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define all remaining replacements
replacements = {
    # noConfig
    'noConfig.label="The 配置 信息 的 虚拟机 不 可用"': 'noConfig.label="虚拟机的配置信息不可用"',
    'noConfig.summary="The 配置 信息 的 虚拟机 不 可用."': 'noConfig.summary="虚拟机的配置信息不可用。"',
    
    # ftSecondaryVm
    'ftSecondaryVm.label="Fault Tolerance Secondary VM"': 'ftSecondaryVm.label="Fault Tolerance 辅助 VM"',
    'ftSecondaryVm.summary="Fault Tolerance Secondary VM"': 'ftSecondaryVm.summary="Fault Tolerance 辅助 VM"',
    
    # hasLocalDisk
    'hasLocalDisk.label="The 虚拟机 has one or more 磁盘s on local (non-\u4efd\u989d) 存储"': 'hasLocalDisk.label="此虚拟机在本地（非共享）存储上有一个或多个磁盘"',
    'hasLocalDisk.summary="The 虚拟机 has one or more 磁盘s on local (non-\u4efd\u989d) 存储"': 'hasLocalDisk.summary="此虚拟机在本地（非共享）存储上有一个或多个磁盘"',
    
    # hasLinkedCloneDisk
    'hasLinkedCloneDisk.label="The 虚拟机 has 虚拟磁盘 in linked-\u514b\u9686 mode"': 'hasLinkedCloneDisk.label="此虚拟机具有链接克隆模式的虚拟磁盘"',
    'hasLinkedCloneDisk.summary="The 虚拟机 has 虚拟磁盘 in linked-\u514b\u9686 mode"': 'hasLinkedCloneDisk.summary="此虚拟机具有链接克隆模式的虚拟磁盘"',
    
    # esxAgentVm
    'esxAgentVm.label="The 虚拟机 is an ESX 代理 VM"': 'esxAgentVm.label="此虚拟机是 ESX 代理 VM"',
    'esxAgentVm.summary="The 虚拟机 is an ESX 代理 VM"': 'esxAgentVm.summary="此虚拟机是 ESX 代理 VM"',
    
    # video3dEnabled
    'video3dEnabled.label="The 虚拟机 has a video 设备 with 3D 已启用"': 'video3dEnabled.label="此虚拟机具有启用了 3D 的视频设备"',
    'video3dEnabled.summary="The 虚拟机 has a video 设备 with 3D 已启用"': 'video3dEnabled.summary="此虚拟机具有启用了 3D 的视频设备"',
    
    # hasVFlashConfiguration
    'hasVFlashConfiguration.label="The 虚拟机 has 磁盘s with vSphere Flash Read Cache 已配置"': 'hasVFlashConfiguration.label="此虚拟机的磁盘配置了 vSphere Flash Read Cache"',
    'hasVFlashConfiguration.summary="The 虚拟机 has 磁盘s with vSphere Flash Read Cache 已配置"': 'hasVFlashConfiguration.summary="此虚拟机的磁盘配置了 vSphere Flash Read Cache"',
    
    # hasUnsupportedDisk
    'hasUnsupportedDisk.label="The 虚拟机 has a 虚拟磁盘 with a backing 类型 that 不 compatible with vSphere Fault Tolerance protection"': 'hasUnsupportedDisk.label="此虚拟机的虚拟磁盘具有与 vSphere Fault Tolerance 保护不兼容的后备类型"',
    'hasUnsupportedDisk.summary="The 虚拟机 has a 虚拟磁盘 with a backing 类型 that 不 compatible with vSphere Fault Tolerance protection."': 'hasUnsupportedDisk.summary="此虚拟机的虚拟磁盘具有与 vSphere Fault Tolerance 保护不兼容的后备类型。"',
    
    # insufficientBandwidth
    'insufficientBandwidth.label="The virtual NIC 已关联 使用 主机 has insufficient 带宽 for vSphere Fault Tolerance 日志记录"': 'insufficientBandwidth.label="与主机关联的虚拟 NIC 带宽不足以支持 vSphere Fault Tolerance 日志记录"',
    'insufficientBandwidth.summary="The virtual NIC 已关联 使用 主机 has insufficient 带宽 for vSphere Fault Tolerance 日志记录."': 'insufficientBandwidth.summary="与主机关联的虚拟 NIC 带宽不足以支持 vSphere Fault Tolerance 日志记录。"',
    
    # hasNestedHVConfiguration
    'hasNestedHVConfiguration.label="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with Hardware Virtualization or Virtualizaton Based 安全性 已启用."': 'hasNestedHVConfiguration.label="主机不支持对启用了硬件虚拟化或基于虚拟化的安全性的虚拟机进行 vSphere Fault Tolerance"',
    'hasNestedHVConfiguration.summary="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with Hardware Virtualization or Virtualizaton Based 安全性 已启用."': 'hasNestedHVConfiguration.summary="主机不支持对启用了硬件虚拟化或基于虚拟化的安全性的虚拟机进行 vSphere Fault Tolerance"',
    
    # unsupportedProduct
    'unsupportedProduct.label="vSphere Fault Tolerance 不 支持 by the VMware product 已安装 在 主机"': 'unsupportedProduct.label="主机上安装的 VMware 产品不支持 vSphere Fault Tolerance"',
    'unsupportedProduct.summary="The VMware product 已安装 在 主机 does not support vSphere Fault Tolerance."': 'unsupportedProduct.summary="主机上安装的 VMware 产品不支持 vSphere Fault Tolerance。"',
    
    # cpuHvUnsupported
    'cpuHvUnsupported.label="Hardware virtualization 不 支持 by the 主机 CPU"': 'cpuHvUnsupported.label="主机 CPU 不支持硬件虚拟化"',
    'cpuHvUnsupported.summary="The 主机 system\'s CPU does not support hardware virtualization, \u2014\u2014 required for Fault Tolerance."': 'cpuHvUnsupported.summary="主机系统的 CPU 不支持硬件虚拟化，而硬件虚拟化是 Fault Tolerance 所必需的。"',
    
    # cpuHwmmuUnsupported
    'cpuHwmmuUnsupported.label="Hardware MMU virtualization 不 支持 by the 主机 CPU"': 'cpuHwmmuUnsupported.label="主机 CPU 不支持硬件 MMU 虚拟化"',
    'cpuHwmmuUnsupported.summary="The 主机 system\'s CPU does not support hardware MMU virtualization, \u2014\u2014 required for SMP Fault Tolerance."': 'cpuHwmmuUnsupported.summary="主机系统的 CPU 不支持硬件 MMU 虚拟化，而这是 SMP Fault Tolerance 所必需的。"',
    
    # cpuHvDisabled
    'cpuHvDisabled.label="Hardware virtualization is 已禁用 在 主机 BIOS"': 'cpuHvDisabled.label="硬件虚拟化已在主机 BIOS 中禁用"',
    'cpuHvDisabled.summary="The 主机 system\'s CPU is compatible with Fault Tolerance, but hardware virtualization has been 已禁用 在 BIOS."': 'cpuHvDisabled.summary="主机系统的 CPU 与 Fault Tolerance 兼容，但硬件虚拟化已在 BIOS 中禁用。"',
    
    # hasEFIFirmware
    'hasEFIFirmware.label="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with EFI firmware"': 'hasEFIFirmware.label="主机不支持对具有 EFI 固件的虚拟机进行 vSphere Fault Tolerance"',
    'hasEFIFirmware.summary="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with EFI firmware"': 'hasEFIFirmware.summary="主机不支持对具有 EFI 固件的虚拟机进行 vSphere Fault Tolerance"',
    
    # tooManyVCPUs
    'tooManyVCPUs.label="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with this many virtual CPUs"': 'tooManyVCPUs.label="主机不支持对具有这么多虚拟 CPU 的虚拟机进行 vSphere Fault Tolerance"',
    'tooManyVCPUs.summary="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with this many virtual CPUs"': 'tooManyVCPUs.summary="主机不支持对具有这么多虚拟 CPU 的虚拟机进行 vSphere Fault Tolerance"',
    
    # tooMuchMemory
    'tooMuchMemory.label="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with this much 内存"': 'tooMuchMemory.label="主机不支持对具有这么多内存的虚拟机进行 vSphere Fault Tolerance"',
    'tooMuchMemory.summary="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with this much 内存"': 'tooMuchMemory.summary="主机不支持对具有这么多内存的虚拟机进行 vSphere Fault Tolerance"',
    
    # vMotionNotLicensed
    'vMotionNotLicensed.label="No 许可证 for vMotion"': 'vMotionNotLicensed.label="没有 vMotion 许可证"',
    'vMotionNotLicensed.summary="vSphere Fault Tolerance requires the 主机 to have a 许可证 that supports vMotion"': 'vMotionNotLicensed.summary="vSphere Fault Tolerance 要求主机具有支持 vMotion 的许可证"',
    
    # ftNotLicensed
    'ftNotLicensed.label="No 许可证 for vSphere Fault Tolerance"': 'ftNotLicensed.label="没有 vSphere Fault Tolerance 许可证"',
    'ftNotLicensed.summary="To use vSphere Fault Tolerance, the 主机 must have a 许可证 that supports the vSphere Fault Tolerance feature."': 'ftNotLicensed.summary="要使用 vSphere Fault Tolerance，主机必须具有支持 vSphere Fault Tolerance 功能的许可证。"',
    
    # haAgentIssue
    'haAgentIssue.label="vSphere HA 代理 not running"': 'haAgentIssue.label="vSphere HA 代理未运行"',
    'haAgentIssue.summary="vSphere Fault Tolerance requires the vSphere HA 代理 to be running 在 主机"': 'haAgentIssue.summary="vSphere Fault Tolerance 要求 vSphere HA 代理在主机上运行"',
    
    # unsupportedSPBM
    'unsupportedSPBM.label="The 虚拟机 has 不支持 存储 policies"': 'unsupportedSPBM.label="此虚拟机具有不受支持的存储策略"',
    'unsupportedSPBM.summary="虚拟机s with Fault Tolerance support SPBM policies only when running on vSAN 数据存储s."': 'unsupportedSPBM.summary="启用 Fault Tolerance 的虚拟机仅在 vSAN 数据存储上运行时才支持 SPBM 策略。"',
    
    # unsupportedPMemHAFailOver
    'unsupportedPMemHAFailOver.label="虚拟机 with Fault Tolerance is 不支持 with PMem Failover."': 'unsupportedPMemHAFailOver.label="具有 Fault Tolerance 的虚拟机不支持 PMem 故障切换。"',
    'unsupportedPMemHAFailOver.summary="虚拟机 with Fault Tolerance 不 支持 with PMem 已启用 for Failover."': 'unsupportedPMemHAFailOver.summary="具有 Fault Tolerance 的虚拟机不支持为故障切换启用 PMem。"',
    
    # unsupportedEncryptedDisk
    'unsupportedEncryptedDisk.label="The 虚拟机 has an encrypted 虚拟磁盘 that 不 compatible with vSphere Fault Tolerance protection."': 'unsupportedEncryptedDisk.label="此虚拟机具有已加密的虚拟磁盘，这与 vSphere Fault Tolerance 保护不兼容。"',
    'unsupportedEncryptedDisk.summary="The 虚拟机 has an encrypted 虚拟磁盘 that 不 compatible with vSphere Fault Tolerance protection."': 'unsupportedEncryptedDisk.summary="此虚拟机具有已加密的虚拟磁盘，这与 vSphere Fault Tolerance 保护不兼容。"',
    
    # ftMetroClusterNotEditable
    'ftMetroClusterNotEditable.label="Cannot 启用 or 禁用 FT Metro 集群 when vSphere Fault Tolerance has been turned on 的 虚拟机."': 'ftMetroClusterNotEditable.label="当 vSphere Fault Tolerance 已为此虚拟机启用时，无法启用或禁用 FT Metro 集群。"',
    'ftMetroClusterNotEditable.summary="Cannot 启用 or 禁用 FT Metro 集群 when vSphere Fault Tolerance has been turned on 的 虚拟机."': 'ftMetroClusterNotEditable.summary="当 vSphere Fault Tolerance 已为此虚拟机启用时，无法启用或禁用 FT Metro 集群。"',
    
    # noHostGroupConfigured
    'noHostGroupConfigured.label="No 主机 组 已配置 on this FT Metro 集群 已启用 虚拟机"': 'noHostGroupConfigured.label="此已启用 FT Metro 集群的虚拟机上未配置任何主机组"',
    'noHostGroupConfigured.summary="No 主机 组 已配置 on this FT Metro 集群 已启用 虚拟机"': 'noHostGroupConfigured.summary="此已启用 FT Metro 集群的虚拟机上未配置任何主机组"',
}

count = 0
not_found = []
for old, new in replacements.items():
    # Try both with escaped quotes and without
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        not_found.append(old[:60])

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Successfully replaced: {count}')
if not_found:
    print(f'Not found ({len(not_found)}):')
    for nf in not_found:
        print(f'  - {nf}')
