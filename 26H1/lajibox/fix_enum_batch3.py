# -*- coding: utf-8 -*-
"""Comprehensive fix for remaining enum.vmsg translation issues."""
import re

path = r'd:\vmware\i18n\OVFTool\env\zh-CN\enum.vmsg'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Read the file and fix remaining issues
# Fix specific strings that still have mixed Chinese-English
fixes = [
    # === VmFaultToleranceConfigIssue ===
    ('hasLocalDisk.label="The 虚拟机 has one or more 磁盘s on local (non-\u4efd\u989d) 存储"', 
     'hasLocalDisk.label="此虚拟机在本地（非共享）存储上有一个或多个磁盘"'),
    ('hasLocalDisk.summary="The 虚拟机 has one or more 磁盘s on local (non-\u4efd\u989d) 存储"', 
     'hasLocalDisk.summary="此虚拟机在本地（非共享）存储上有一个或多个磁盘"'),
    
    ('hasNestedHVConfiguration.label="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with Hardware Virtualization or Virtualizaton Based \u5b89\u5168\u6027 \u5df2\u542f\u7528."', 
     'hasNestedHVConfiguration.label="主机不支持对启用了硬件虚拟化或基于虚拟化的安全性的虚拟机进行 vSphere Fault Tolerance"'),
    ('hasNestedHVConfiguration.summary="The 主机 does not support vSphere Fault Tolerance on 虚拟机s with Hardware Virtualization or Virtualizaton Based \u5b89\u5168\u6027 \u5df2\u542f\u7528."', 
     'hasNestedHVConfiguration.summary="主机不支持对启用了硬件虚拟化或基于虚拟化的安全性的虚拟机进行 vSphere Fault Tolerance"'),
    
    ('unsupportedProduct.summary="The VMware product \u5df2\u5b89\u88c5 \u5728 \u4e3b\u673a does not support vSphere Fault Tolerance."', 
     'unsupportedProduct.summary="主机上安装的 VMware 产品不支持 vSphere Fault Tolerance。"'),
    
    ('cpuHvUnsupported.summary="The \u4e3b\u673a system\'s CPU does not support hardware virtualization, \u2014\u2014 required for Fault Tolerance."',
     'cpuHvUnsupported.summary="主机系统的 CPU 不支持硬件虚拟化，而硬件虚拟化是 Fault Tolerance 所必需的。"'),
    
    ('cpuHwmmuUnsupported.summary="The \u4e3b\u673a system\'s CPU does not support hardware MMU virtualization, \u2014\u2014 required for SMP Fault Tolerance."',
     'cpuHwmmuUnsupported.summary="主机系统的 CPU 不支持硬件 MMU 虚拟化，而这是 SMP Fault Tolerance 所必需的。"'),
    
    ('hasEFIFirmware.label="The \u4e3b\u673a does not support vSphere Fault Tolerance on \u865a\u62df\u673as with EFI firmware"',
     'hasEFIFirmware.label="主机不支持对具有 EFI 固件的虚拟机进行 vSphere Fault Tolerance"'),
    ('hasEFIFirmware.summary="The \u4e3b\u673a does not support vSphere Fault Tolerance on \u865a\u62df\u673as with EFI firmware"',
     'hasEFIFirmware.summary="主机不支持对具有 EFI 固件的虚拟机进行 vSphere Fault Tolerance"'),
    
    ('tooManyVCPUs.label="The \u4e3b\u673a does not support vSphere Fault Tolerance on \u865a\u62df\u673as with this many virtual CPUs"',
     'tooManyVCPUs.label="主机不支持对具有这么多虚拟 CPU 的虚拟机进行 vSphere Fault Tolerance"'),
    ('tooManyVCPUs.summary="The \u4e3b\u673a does not support vSphere Fault Tolerance on \u865a\u62df\u673as with this many virtual CPUs"',
     'tooManyVCPUs.summary="主机不支持对具有这么多虚拟 CPU 的虚拟机进行 vSphere Fault Tolerance"'),
    
    ('tooMuchMemory.label="The \u4e3b\u673a does not support vSphere Fault Tolerance on \u865a\u62df\u673as with this much \u5185\u5b58"',
     'tooMuchMemory.label="主机不支持对具有这么多内存的虚拟机进行 vSphere Fault Tolerance"'),
    ('tooMuchMemory.summary="The \u4e3b\u673a does not support vSphere Fault Tolerance on \u865a\u62df\u673as with this much \u5185\u5b58"',
     'tooMuchMemory.summary="主机不支持对具有这么多内存的虚拟机进行 vSphere Fault Tolerance"'),
    
    ('vMotionNotLicensed.summary="vSphere Fault Tolerance requires the \u4e3b\u673a to have a \u8bb8\u53ef\u8bc1 that supports vMotion"',
     'vMotionNotLicensed.summary="vSphere Fault Tolerance 要求主机具有支持 vMotion 的许可证"'),
    
    ('ftNotLicensed.summary="To use vSphere Fault Tolerance, the \u4e3b\u673a must have a \u8bb8\u53ef\u8bc1 that supports the vSphere Fault Tolerance feature."',
     'ftNotLicensed.summary="要使用 vSphere Fault Tolerance，主机必须具有支持 vSphere Fault Tolerance 功能的许可证。"'),
    
    ('unsupportedSPBM.summary="\u865a\u62df\u673as with Fault Tolerance support SPBM policies only when running on vSAN \u6570\u636e\u5b58\u50a8s."',
     'unsupportedSPBM.summary="启用 Fault Tolerance 的虚拟机仅在 vSAN 数据存储上运行时才支持 SPBM 策略。"'),
    
    # === VmFaultToleranceInvalidFileBacking ===
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualFloppy.label="Virtual \u8f6f\u9a71"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualFloppy.label="虚拟软驱"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualFloppy.summary="Virtual \u8f6f\u9a71"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualFloppy.summary="虚拟软驱"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualCdrom.label="Virtual CD-ROM"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualCdrom.label="虚拟 CD-ROM"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualCdrom.summary="Virtual CD-ROM"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualCdrom.summary="虚拟 CD-ROM"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualSerialPort.label="Virtual \u4e32\u53e3 \u7aef\u53e3"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualSerialPort.label="虚拟串口"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualSerialPort.summary="Virtual \u4e32\u53e3 \u7aef\u53e3"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualSerialPort.summary="虚拟串口"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualParallelPort.label="Virtual \u5e76\u53e3 \u7aef\u53e3"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualParallelPort.label="虚拟并口"'),
    ('VmFaultToleranceInvalidFileBacking.DeviceType.virtualParallelPort.summary="Virtual \u5e76\u53e3 \u7aef\u53e3"',
     'VmFaultToleranceInvalidFileBacking.DeviceType.virtualParallelPort.summary="虚拟并口"'),
    
    # === NotSupportedDeviceForFT ===
    ('NotSupportedDeviceForFT.DeviceType.virtualVmxnet3.label="Vmxnet3 virtual ethernet adapter"',
     'NotSupportedDeviceForFT.DeviceType.virtualVmxnet3.label="Vmxnet3 虚拟以太网适配器"'),
    ('NotSupportedDeviceForFT.DeviceType.virtualVmxnet3.summary="Vmxnet3 virtual ethernet adapter"',
     'NotSupportedDeviceForFT.DeviceType.virtualVmxnet3.summary="Vmxnet3 虚拟以太网适配器"'),
    ('NotSupportedDeviceForFT.DeviceType.paraVirtualSCSIController.label="Paravirtualized SCSI controller"',
     'NotSupportedDeviceForFT.DeviceType.paraVirtualSCSIController.label="准虚拟化 SCSI 控制器"'),
    ('NotSupportedDeviceForFT.DeviceType.paraVirtualSCSIController.summary="Paravirtualized SCSI controller"',
     'NotSupportedDeviceForFT.DeviceType.paraVirtualSCSIController.summary="准虚拟化 SCSI 控制器"'),
    
    # === CannotMoveFaultToleranceVm ===
    ('CannotMoveFaultToleranceVm.MoveType.cluster.label="Cluster"',
     'CannotMoveFaultToleranceVm.MoveType.cluster.label="集群"'),
    ('CannotMoveFaultToleranceVm.MoveType.cluster.summary="Cluster"',
     'CannotMoveFaultToleranceVm.MoveType.cluster.summary="集群"'),
    
    # === FtIssuesOnHost ===
    ('FtIssuesOnHost.user.label="User"', 'FtIssuesOnHost.user.label="用户"'),
]

count = 0
not_found = []
for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        # Try to find partial match
        key = old.split('"')[0] + '"' if old.count('"') >= 2 else old[:40]
        not_found.append(key)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Fixed: {count}')
if not_found:
    print(f'Not found ({len(not_found)}):')
    for nf in not_found:
        print(f'  {nf}')
