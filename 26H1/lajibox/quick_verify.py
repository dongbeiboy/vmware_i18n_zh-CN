import re
import sys
sys.stdout.reconfigure(encoding='utf-8')
f = open(r'd:\vmware\i18n\OVFTool\env\zh-CN\option.vmsg', encoding='utf-8').read()
checks = ['接收r','有效ation','A挂载','计数ry','用户s','组s','日志gers','dia日志']
for c in checks:
    ok = 'OK' if c not in f else 'REM'
    print(f'{ok}: {c}')

# Check within quotes specifically
print()
for pat, name in [(r'="[^"]*已用[^"]*"','已用(值内)'),(r'="[^"]*已启用[^"]*"','已启用(值内)'),
                   (r'="[^"]*正在监控[^"]*"','正在监控'),(r'="[^"]*正在扫描[^"]*"','正在扫描')]:
    ok = 'OK' if not re.findall(pat, f) else 'REM'
    print(f'{ok}: {name}')

# Check if they exist in key names
for t in ['已用','已启用']:
    if t in f and t not in [x for x in ['']]:
        lines = [l.strip() for l in f.split('\n') if t in l and not l.strip().startswith('#')]
        if lines:
            print(f'\n{t} - 共{len(lines)}行包含(多在键名中):')
            for l in lines[:3]:
                print(f'  {l[:100]}')

