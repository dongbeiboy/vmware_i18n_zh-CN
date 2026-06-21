"""Check current status of all zh-CN translation files."""
import glob, os, re

en_dir = r'D:\vmware\i18n\OVFTool\env\en'
zh_dir = r'D:\vmware\i18n\OVFTool\env\zh-CN'
main_zh = r'D:\vmware\i18n\messages\zh-CN\vmware.vmsg'

def count_keys(lines):
    return sum(1 for l in lines if '=' in l 
               and not l.strip().startswith('#') 
               and not l.strip().startswith('sig')
               and not l.strip().startswith('###'))

def count_cn(text):
    return sum(1 for c in text if '\u4e00' <= c <= '\u9fff')

# OVFTool files
results = []
print('=== OVFTool zh-CN ===')
print(f'  {"File":25s} {"Keys":12s} {"CN%":8s}')
print(f'  {"-"*25} {"-"*12} {"-"*8}')

for f in sorted(os.listdir(zh_dir)):
    if not f.endswith('.vmsg'):
        continue
    
    zh_text = open(os.path.join(zh_dir, f), encoding='utf-8').read()
    en_text = open(os.path.join(en_dir, f), encoding='utf-8').read()
    
    zh_keys = count_keys(zh_text.split('\n'))
    en_keys = count_keys(en_text.split('\n'))
    
    # Estimate CN coverage: compare CN chars in ZH vs EN (EN should have ~0 CN)
    cn_zh = count_cn(zh_text)
    cn_en = count_cn(en_text)
    
    # Rough coverage: Chinese chars in values / total value chars
    # Better: just check how many values contain Chinese
    zh_val_count = 0
    for l in zh_text.split('\n'):
        if '=' in l and not l.strip().startswith('#'):
            val = l.split('=', 1)[1]
            if any('\u4e00' <= c <= '\u9fff' for c in val):
                zh_val_count += 1
    
    total_val_count = count_keys(zh_text.split('\n'))
    coverage = zh_val_count / total_val_count * 100 if total_val_count > 0 else 0
    
    key_match = '✅' if zh_keys == en_keys else f'❌({zh_keys}/{en_keys})'
    grade = 'A' if coverage >= 85 else 'B' if coverage >= 70 else 'C' if coverage >= 50 else 'D'
    
    print(f'  {f:25s} {key_match:12s} {coverage:6.0f}% ({grade})')
    results.append((f, zh_keys, en_keys, coverage, grade))

# Main vmware.vmsg
print()
print('=== Main vmware.vmsg ===')
main_text = open(main_zh, encoding='utf-8').read()
main_keys = count_keys(main_text.split('\n'))
main_cn = count_cn(main_text)
main_size = os.path.getsize(main_zh) / 1024

# Count CN coverage in main
zh_val_count = 0
total_val_count = 0
for l in main_text.split('\n'):
    if '=' in l and not l.strip().startswith('#'):
        total_val_count += 1
        val = l.split('=', 1)[1]
        if any('\u4e00' <= c <= '\u9fff' for c in val):
            zh_val_count += 1

main_cov = zh_val_count / total_val_count * 100 if total_val_count > 0 else 0

print(f'  Keys: {main_keys}')
print(f'  Size: {main_size:.0f} KB')
print(f'  CN chars: {main_cn}')
print(f'  CN coverage: {main_cov:.0f}%')

# Encoding corruption
print()
print('=== Encoding corruption check ===')
and_bug = 0
for f in sorted(os.listdir(zh_dir)):
    if f.endswith('.vmsg'):
        content = open(os.path.join(zh_dir, f), encoding='utf-8').read()
        found = re.findall(r'c和ela|St和ard|St和alone|Ab和on', content)
        if found:
            and_bug += len(found)
            print(f'  {f}: {len(found)} instances')

# Check main vmware.vmsg too
main_content = open(main_zh, encoding='utf-8').read()
ji_count = len(re.findall(r'即', main_content))
and_count = len(re.findall(r'c和ela|St和ard|St和alone|Ab和on', main_content))
print(f'  Main vmware.vmsg: and→和={and_count}, 即={ji_count}')

print(f'  OVFTool total: {and_bug}')
if and_bug == 0:
    print('  ✅ Clean!')

# Summary
print()
print('=== Overall Summary ===')
a = sum(1 for r in results if r[4] == 'A')
b = sum(1 for r in results if r[4] == 'B')
c = sum(1 for r in results if r[4] == 'C')
d = sum(1 for r in results if r[4] == 'D')
print(f'  OVFTool: {len(results)} files, {a}A/{b}B/{c}C/{d}D')
print(f'  Main: {main_cov:.0f}% CN coverage')

# Check backup exists
backup = r'D:\vmware\i18n\.backup'
if os.path.exists(backup):
    snaps = sorted(os.listdir(backup))
    print(f'  Backups: {len(snaps)} snapshots (latest: {snaps[-1] if snaps else "none"})')
