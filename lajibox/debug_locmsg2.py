#!/usr/bin/env python3
"""Debug: test all entries to find why fixed=0"""

import sys
sys.path.insert(0, 'D:\\vmware\\i18n')
import fix_locmsg_v3

en_entries = fix_locmsg_v3.parse_vmsg(fix_locmsg_v3.EN_FILE)
zh_entries = fix_locmsg_v3.parse_vmsg(fix_locmsg_v3.ZH_FILE)

diff_count = 0
same_count = 0
tested = 0

for key, en_val in list(en_entries.items())[:50]:  # test first 50
    if key not in zh_entries:
        continue
    
    zh_val = zh_entries[key]
    remaining = fix_locmsg_v3.eng_words_remaining(zh_val)
    has_suffix = fix_locmsg_v3.has_en_suffix(zh_val)
    cn_ratio = fix_locmsg_v3.chinese_ratio(zh_val)
    
    if not remaining and not has_suffix:
        continue  # already good
    
    tested += 1
    use_full = cn_ratio < 0.2 or (cn_ratio < 0.5 and len(remaining) > 3)
    
    if use_full:
        new_val = fix_locmsg_v3.translate_text(en_val, is_full=True)
        new_val = fix_locmsg_v3.post_process(new_val)
    else:
        new_val = fix_locmsg_v3.translate_text(zh_val, is_full=False)
        new_val = fix_locmsg_v3.post_process(new_val)
    
    if new_val != zh_val:
        diff_count += 1
        if diff_count <= 5:
            print(f"\n[DIFF] {key}")
            print(f"  OLD: {zh_val[:80]}")
            print(f"  NEW: {new_val[:80]}")
    else:
        same_count += 1
        if same_count <= 5:
            print(f"\n[SAME] {key}")
            print(f"  VAL: {zh_val[:80]}")

print(f"\n\nTested: {tested}, Diff: {diff_count}, Same: {same_count}")
