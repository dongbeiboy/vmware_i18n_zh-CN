"""
生成 key_en_ja_cn.csv: 汇总所有 vmsg 文件的 key、英文、日文、中文翻译对照表
- OVFTool: en/*.vmsg ↔ zh-CN/*.vmsg 精确匹配 key（en=英文, ja=空）
- vCenter: vmware-ja.vmsg ↔ zh-CN/vmware.vmsg（en=空, ja=日文）
"""
import csv
import re
import os
import glob

PROJECT = r"e:\development\github\vmware_i18n_zh-CN\26H1"
OUTPUT = os.path.join(PROJECT, r"lajibox\key_en_ja_cn.csv")

OVF_EN = os.path.join(PROJECT, r"OVFTool\env\en")
OVF_CN = os.path.join(PROJECT, r"OVFTool\env\zh-CN")
VC_JA = os.path.join(PROJECT, r"messages\reference\vmware-ja.vmsg")
VC_CN = os.path.join(PROJECT, r"messages\zh-CN\vmware.vmsg")

# 解析 vmsg 文件为 {key: value} 字典
def parse_vmsg(path):
    d = {}
    pat = re.compile(r'^\s*([a-zA-Z0-9_.-]+)\s*=\s*"(.*)"\s*$')
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = pat.match(line)
            if m:
                d[m.group(1)] = m.group(2)
    return d

rows = []

# --- 1) OVFTool: en ↔ zh-CN (ja=空) ---
cn_files = {os.path.basename(p): p for p in glob.glob(os.path.join(OVF_CN, "*.vmsg"))}
en_files = {os.path.basename(p): p for p in glob.glob(os.path.join(OVF_EN, "*.vmsg"))}

common = sorted(set(cn_files) & set(en_files))
for fname in common:
    en_dict = parse_vmsg(en_files[fname])
    cn_dict = parse_vmsg(cn_files[fname])
    all_keys = sorted(set(en_dict) | set(cn_dict))
    for k in all_keys:
        rows.append({
            "key": k,
            "en": en_dict.get(k, ""),
            "ja": "",
            "zh_CN": cn_dict.get(k, ""),
            "source": f"ovftool/{fname}"
        })

# --- 2) vCenter: vmware-ja.vmsg ↔ vmware.vmsg (en=空) ---
ja_dict = parse_vmsg(VC_JA)
cn_dict = parse_vmsg(VC_CN)
all_keys = sorted(set(ja_dict) | set(cn_dict))
for k in all_keys:
    rows.append({
        "key": k,
        "en": "",
        "ja": ja_dict.get(k, ""),
        "zh_CN": cn_dict.get(k, ""),
        "source": "vcenter/vmware.vmsg"
    })

# --- 写入 CSV ---
with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["key", "en", "ja", "zh_CN", "source"])
    w.writeheader()
    w.writerows(rows)

print(f"Done! {len(rows)} rows -> {OUTPUT}")
print(f"  OVFTool: {sum(1 for r in rows if r['source'].startswith('ovftool'))} （en有值, ja空）")
print(f"  vCenter: {sum(1 for r in rows if r['source'].startswith('vcenter'))} （en空, ja有值）")
