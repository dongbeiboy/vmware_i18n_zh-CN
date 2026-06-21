#!/usr/bin/env python3
import re
from pathlib import Path

f = Path(r'D:\vmware\i18n\OVFTool\env\zh-CN\task.vmsg')
text = f.read_text(encoding='utf-8')
lines = text.split('\n')

# Show first few fixed entries
for l in lines:
    if l.startswith('AgentManager'):
        print(l[:100])
    if l.startswith('AuthorizationManager.add') and ('label' in l or 'summary' in l):
        print(l[:100])

vals = [l for l in lines if ('label=' in l or 'summary=' in l) and l[0].isalpha()]
print(f'\nTotal entries: {len(vals)}')
print(f'权限s: {"权限s" in text}, 定义d: {"定义d" in text}, 添加ress: {"添加ress" in text}')

# Count quality
good = 0
pure_en = []
mixed = []
for l in lines:
    m = re.match(r'^[A-Za-z0-9_.]+\.(label|summary)\s*=\s*"(.+)"$', l)
    if m:
        v = m.group(2)
        en = sum(1 for c in v if c.isascii() and c.isalpha())
        zh = sum(1 for c in v if '\u4e00' <= c <= '\u9fff')
        key = m.group(1) + '.' + m.group(2)
        if en > 0 and zh == 0:
            pure_en.append((key, v))
        elif en + zh > 0 and en / (en + zh) > 0.5:
            mixed.append((key, v))
        else:
            good += 1

print(f'Good (mostly CN): {good}')
print(f'Pure English: {len(pure_en)}')
print(f'Mixed (>50% EN): {len(mixed)}')
print()

if pure_en:
    print('=== Pure EN ===')
    for k, v in pure_en[:10]:
        print(f'  {k} = {v}')

if mixed:
    print('=== Mixed samples (first 15) ===')
    for k, v in mixed[:15]:
        print(f'  {k} = {v[:90]}')
