"""Fix known small issues in auth.vmsg"""
import re

with open(r'D:\vmware\i18n\OVFTool\env\zh-CN\auth.vmsg', encoding='utf-8') as f:
    text = f.read()

fixes = {
    'privilege.Host.label="Host"': 'privilege.Host.label="主机"',
    'privilege.Host.summary="Host"': 'privilege.Host.summary="主机"',
    'privilege.Host.Tpm.Read.label="Read"': 'privilege.Host.Tpm.Read.label="读取"',
    'privilege.Host.Entropy.Read.label="Read"': 'privilege.Host.Entropy.Read.label="读取"',
    'privilege.DVSwitch.Move.label="Move"': 'privilege.DVSwitch.Move.label="移动"',
    'privilege.VirtualMachine.Inventory.Move.label="Move"': 'privilege.VirtualMachine.Inventory.Move.label="移动"',
    'privilege.Alarm.Create.label="创建 警报"': 'privilege.Alarm.Create.label="创建警报"',
}

count = 0
for old, new in fixes.items():
    if old in text:
        text = text.replace(old, new)
        count += 1
        print(f"  FIXED: {old.split('=')[0]}")
    else:
        # Check if key exists but value differs
        key = old.split('=')[0]
        idx = text.find(key)
        if idx >= 0:
            line_end = text.find('\n', idx)
            print(f"  SKIP (value differs): {text[idx:line_end][:80]}")
        else:
            print(f"  NOT FOUND: {key}")

# Fix ScheduledTask.Run.summary (may have different exact text)
st_key = 'privilege.ScheduledTask.Run.summary'
st_idx = text.find(st_key)
if st_idx >= 0:
    line_end = text.find('\n', st_idx)
    text = text[:st_idx] + f'{st_key}="立即运行计划任务"' + text[line_end:]
    print(f"  FIXED: {st_key}")
    count += 1

# Fix RevertToSnapshot.summary (may have different exact text)
rt_key = 'privilege.VirtualMachine.State.RevertToSnapshot.summary'
rt_idx = text.find(rt_key)
if rt_idx >= 0:
    line_end = text.find('\n', rt_idx)
    text = text[:rt_idx] + f'{rt_key}="将快照设为当前值"' + text[line_end:]
    print(f"  FIXED: {rt_key}")
    count += 1

with open(r'D:\vmware\i18n\OVFTool\env\zh-CN\auth.vmsg', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"\nTotal fixes: {count}")
