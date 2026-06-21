# -*- coding: utf-8 -*-
import re

with open(r'd:\vmware\i18n\OVFTool\env\zh-CN\enum.vmsg', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'verifySSLCertificateFlagNotSet.summary="\\"Check 主机 证书s\\" flag not 设置 for vCenter 服务器"': 'verifySSLCertificateFlagNotSet.summary="未为 vCenter 服务器设置\\"检查主机证书\\"标志"',
    
    'hasSnapshots.label="The 虚拟机 has one or more 快照s or 磁盘s that need consolIDation that make it incompatible for vSphere Fault Tolerance protection"': 'hasSnapshots.label="此虚拟机具有一个或多个需要整合的快照或磁盘，因此与 vSphere Fault Tolerance 保护不兼容"',
    'hasSnapshots.summary="The 虚拟机 has one or more 快照s or 磁盘s that need consolIDation that make it incompatible for vSphere Fault Tolerance protection"': 'hasSnapshots.summary="此虚拟机具有一个或多个需要整合的快照或磁盘，因此与 vSphere Fault Tolerance 保护不兼容"',
    
    'noConfig.label="The 配置 信息 的 虚拟机 不 可用"': 'noConfig.label="虚拟机的配置信息不可用"',
    'noConfig.summary="The 配置 信息 的 虚拟机 不 可用."': 'noConfig.summary="虚拟机的配置信息不可用。"',
    
    'ftSecondaryVm.label="Fault Tolerance Secondary VM"': 'ftSecondaryVm.label="Fault Tolerance 辅助 VM"',
    'ftSecondaryVm.summary="Fault Tolerance Secondary VM"': 'ftSecondaryVm.summary="Fault Tolerance 辅助 VM"',
    
    'hasLocalDisk.label="The 虚拟机 has one or more 磁盘s on local (non-份额d) 存储"': 'hasLocalDisk.label="此虚拟机在本地（非共享）存储上有一个或多个磁盘"',
    'hasLocalDisk.summary="The 虚拟机 has one or more 磁盘s on local (non-份额d) 存储"': 'hasLocalDisk.summary="此虚拟机在本地（非共享）存储上有一个或多个磁盘"',
    
    'hasLinkedCloneDisk.label="The 虚拟机 has 虚拟磁盘 in linked-克隆 mode"': 'hasLinkedCloneDisk.label="此虚拟机具有链接克隆模式的虚拟磁盘"',
    'hasLinkedCloneDisk.summary="The 虚拟机 has 虚拟磁盘 in linked-克隆 mode"': 'hasLinkedCloneDisk.summary="此虚拟机具有链接克隆模式的虚拟磁盘"',
    
    'esxAgentVm.label="The 虚拟机 is an ESX 代理 VM"': 'esxAgentVm.label="此虚拟机是 ESX 代理 VM"',
    'esxAgentVm.summary="The 虚拟机 is an ESX 代理 VM"': 'esxAgentVm.summary="此虚拟机是 ESX 代理 VM"',
    
    'video3dEnabled.label="The 虚拟机 has a vIDEo 设备 with 3D 已启用"': 'video3dEnabled.label="此虚拟机具有启用了 3D 的视频设备"',
    'video3dEnabled.summary="The 虚拟机 has a vIDEo 设备 with 3D 已启用"': 'video3dEnabled.summary="此虚拟机具有启用了 3D 的视频设备"',
    
    'hasVFlashConfiguration.label="The 虚拟机 has 磁盘s with vSphere Flash Read Cache 已配置"': 'hasVFlashConfiguration.label="此虚拟机的磁盘配置了 vSphere Flash Read Cache"',
    'hasVFlashConfiguration.summary="The 虚拟机 has 磁盘s with vSphere Flash Read Cache 已配置"': 'hasVFlashConfiguration.summary="此虚拟机的磁盘配置了 vSphere Flash Read Cache"',
}

count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"  Replaced: {old[:50]}...")
    else:
        print(f"  NOT FOUND: {old[:50]}...")

with open(r'd:\vmware\i18n\OVFTool\env\zh-CN\enum.vmsg', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal replacements: {count}')
