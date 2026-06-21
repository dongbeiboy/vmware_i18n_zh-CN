#!/usr/bin/env python3
"""Debug locmsg translation fix."""

import sys, re
sys.path.insert(0, 'D:\\vmware\\i18n')
import fix_locmsg_v3

# Test a few entries
test_cases = [
    # (en_val, zh_val)
    ("Feature '{feature}' not licensed, requires {need} have {have}", 
     "Feature '{feature}' not 许可证d, requires {need} have {have}"),
    ("The virtual disk size is too small.",
     "The 虚拟磁盘 大小 is too small."),
    ("The file name is too long.",
     "The file 名称 is too long."),
    ("License Expired, {info}",
     "许可证 Expired, {info}"),
]

for en, zh in test_cases:
    print(f"EN: {en}")
    print(f"ZH: {zh}")
    
    remaining = fix_locmsg_v3.eng_words_remaining(zh)
    has_suffix = fix_locmsg_v3.has_en_suffix(zh)
    cn_ratio = fix_locmsg_v3.chinese_ratio(zh)
    
    print(f"  remaining: {remaining}")
    print(f"  has_suffix: {has_suffix}")
    print(f"  cn_ratio: {cn_ratio:.3f}")
    
    use_full = cn_ratio < 0.2 or (cn_ratio < 0.5 and len(remaining) > 3)
    print(f"  use_full: {use_full}")
    
    if use_full:
        new_val = fix_locmsg_v3.translate_text(en, is_full=True)
        new_val = fix_locmsg_v3.post_process(new_val)
    else:
        new_val = fix_locmsg_v3.translate_text(zh, is_full=False)
        new_val = fix_locmsg_v3.post_process(new_val)
    
    print(f"  NEW: {new_val}")
    print(f"  SAME: {new_val == zh}")
    print()
