#!/usr/bin/env python3
"""
v3 patch: Targeted post-fixes on v2 result. Fixes residual English artifacts.
"""
import re, datetime
from pathlib import Path

SESSION_TAG = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
ZH_CN_FILE = Path(r"d:\vmware\i18n\OVFTool\env\zh-CN\task.vmsg")
BACKUP_FILE = Path(r"d:\vmware\i18n\.backup\OVFTool\env\zh-CN\task_pre_v3.vmsg")
REPORT_FILE = Path(r"d:\vmware\i18n\OVFTool\env\zh-CN\fix_task_report.md")

FIXES = [
    # ===== Prefixes (before Chinese) =====
    (re.compile(r'(?<![a-zA-Z])[Rr]e(?=[\u4e00-\u9fff])'), '重新'),
    (re.compile(r'(?<![a-zA-Z])[Uu]n(?=[\u4e00-\u9fff])'), '取消'),
    (re.compile(r'(?<![a-zA-Z])[Nn]on(?=[\u4e00-\u9fff\s])'), '非'),
    (re.compile(r'(?<![a-zA-Z])[Pp]re(?=[\u4e00-\u9fff])'), '预'),
    (re.compile(r'(?<![a-zA-Z])[Dd]e(?=[\u4e00-\u9fff])'), '取消'),

    # ===== English prepositions/function words between Chinese or with "to" =====
    # These survive because word-boundary regex failed in v2
    (re.compile(r'\b(on|at|to|of|by|with|from|into|via|per)\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\b(the|a|an|this|that|these|those)\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\b(for)\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\b(in)\s+(?=[\u4e00-\u9fff])', re.I), ''),
    # "of 的" artifact → remove "of" before Chinese
    (re.compile(r'\bof\s+(?=[\u4e00-\u9fff])', re.I), ''),
    # "to be" + Chinese → remove "to be"
    (re.compile(r'\bto\s+be\s+(?=[\u4e00-\u9fff])', re.I), ''),
    # "to" at end before Chinese
    (re.compile(r'\bto\s+(?=[\u4e00-\u9fff])', re.I), ''),
    
    # "be " + Chinese → remove "be"
    (re.compile(r'\bbe\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bis\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bare\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bwas\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bwere\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bhave\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bhas\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bhad\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bdo\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bdid\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bdoes\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bwill\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bwould\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bshall\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bshould\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bcan\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bcould\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bmay\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bmight\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bmust\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bthat\s+(?=[\u4e00-\u9fff\s])', re.I), ''),
    (re.compile(r'\bwhich\s+(?=[\u4e00-\u9fff\s])', re.I), ''),
    (re.compile(r'\bwhen\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bwhere\s+(?=[\u4e00-\u9fff])', re.I), ''),
    (re.compile(r'\bwhether\s+', re.I), ''),
    # "not/no/never" before Chinese → 不
    (re.compile(r'\b(not|no|never)\s+(?=[\u4e00-\u9fff])', re.I), '不'),
    # "as " before Chinese
    (re.compile(r'\bas\s+(?=[\u4e00-\u9fff])', re.I), ''),
    # "than " before Chinese
    (re.compile(r'\bthan\s+(?=[\u4e00-\u9fff])', re.I), '比'),
    # "if " before Chinese  
    (re.compile(r'\bif\s+(?=[\u4e00-\u9fff])', re.I), '如果'),
    
    # ===== Verb conjugations =====
    (re.compile(r'\bexecutes?\s+', re.I), '执行'),
    (re.compile(r'\bmanages?\s+', re.I), '管理'),
    (re.compile(r'\bperforms?\s+', re.I), '执行'),
    (re.compile(r'\binstructs?\s+', re.I), '指示'),
    (re.compile(r'\bdetermines?\s+', re.I), '确定'),
    (re.compile(r'\brepresents?\s+', re.I), '表示'),
    (re.compile(r'\bcontains?\s+', re.I), '包含'),
    (re.compile(r'\bincludes?\s+', re.I), '包括'),
    (re.compile(r'\bexcludes?\s+', re.I), '排除'),
    (re.compile(r'\binvokes?\s+', re.I), '调用'),
    (re.compile(r'\bnotif(y|ies|ied)\b', re.I), '通知'),
    (re.compile(r'\bspecif(y|ies|ied)\b', re.I), '指定'),
    (re.compile(r'\bidentif(y|ies|ied)\b', re.I), '识别'),
    (re.compile(r'\bverif(y|ies|ied)\b', re.I), '验证'),
    (re.compile(r'\bmodif(y|ies|ied)\b', re.I), '修改'),
    (re.compile(r'\bclassif(y|ies|ied)\b', re.I), '分类'),
    (re.compile(r'\bjustif(y|ies|ied)\b', re.I), '调整'),
    (re.compile(r'\bprovides?\b', re.I), '提供'),
    (re.compile(r'\brecomputes?\b', re.I), '重新计算'),
    (re.compile(r'\bretrieves?\b', re.I), '检索'),
    (re.compile(r'\bvalidates?\b', re.I), '验证'),
    (re.compile(r'\bchecks?\s+', re.I), '检查'),
    (re.compile(r'\bdeletes?\s+', re.I), '删除'),
    (re.compile(r'\bcreates?\s+', re.I), '创建'),
    (re.compile(r'\brenames?\s+', re.I), '重命名'),
    (re.compile(r'\breloads?\s+', re.I), '重新加载'),
    (re.compile(r'\brefreshes?\s+', re.I), '刷新'),
    (re.compile(r'\bclears?\s+', re.I), '清除'),
    (re.compile(r'\bselects?\s+', re.I), '选择'),
    (re.compile(r'\bcloses?\s+', re.I), '关闭'),
    (re.compile(r'\bopens?\s+', re.I), '打开'),
    (re.compile(r'\brecords?\s+', re.I), '记录'),
    (re.compile(r'\breturns?\s+', re.I), '返回'),
    (re.compile(r'\buses?\s+', re.I), '使用'),
    (re.compile(r'\bcalls?\s+', re.I), '调用'),
    (re.compile(r'\bfinds?\s+', re.I), '查找'),
    (re.compile(r'\blocates?\s+', re.I), '查找'),
    (re.compile(r'\bcomputes?\s+', re.I), '计算'),
    (re.compile(r'\bprepares?\s+', re.I), '准备'),
    (re.compile(r'\bchecks?\s+', re.I), '检查'),
    (re.compile(r'\bconverts?\s+', re.I), '转换'),
    (re.compile(r'\bexports?\s+', re.I), '导出'),
    (re.compile(r'\bimports?\s+', re.I), '导入'),
    (re.compile(r'\bmoves?\s+', re.I), '移动'),
    (re.compile(r'\bcopies?\s+', re.I), '复制'),
    (re.compile(r'\blists?\s+', re.I), '列出'),
    (re.compile(r'\bupdates?\s+', re.I), '更新'),
    (re.compile(r'\breconfigures?\s+', re.I), '重新配置'),
    (re.compile(r'\benables?\s+', re.I), '启用'),
    (re.compile(r'\bdisables?\s+', re.I), '禁用'),
    (re.compile(r'\bregisters?\s+', re.I), '注册'),
    (re.compile(r'\bdisplays?\s+', re.I), '显示'),
    (re.compile(r'\brestores?\s+', re.I), '还原'),
    (re.compile(r'\bapplies?\s+', re.I), '应用'),
    (re.compile(r'\bgenerates?\s+', re.I), '生成'),
    (re.compile(r'\bstarts?\s+', re.I), '启动'),
    (re.compile(r'\bstops?\s+', re.I), '停止'),
    (re.compile(r'\bjoins?\s+', re.I), '加入'),
    (re.compile(r'\bassigns?\s+', re.I), '分配'),
    (re.compile(r'\bcombines?\s+', re.I), '合并'),
    (re.compile(r'\bconnects?\s+', re.I), '连接'),
    (re.compile(r'\bdestroys?\s+', re.I), '销毁'),
    (re.compile(r'\breleases?\s+', re.I), '释放'),
    (re.compile(r'\bseparates?\s+', re.I), '分离'),
    (re.compile(r'\bcalculates?\s+', re.I), '计算'),
    (re.compile(r'\bcollects?\s+', re.I), '收集'),
    (re.compile(r'\bcompares?\s+', re.I), '比较'),
    (re.compile(r'\bconverts?\s+', re.I), '转换'),
    (re.compile(r'\breplaces?\s+', re.I), '替换'),
    (re.compile(r'\brequires?\s+', re.I), '需要'),
    (re.compile(r'\bcontrols?\s+', re.I), '控制'),
    (re.compile(r'\bprocesses?\s+', re.I), '处理'),
    (re.compile(r'\bworks?\s+', re.I), '工作'),
    (re.compile(r'\bhandles?\s+', re.I), '处理'),
    (re.compile(r'\bparticipates?\s+', re.I), '参与'),
    (re.compile(r'\badjusts?\s+', re.I), '调整'),
    (re.compile(r'\bfollows?\s+', re.I), '遵循'),
    (re.compile(r'\binitiates?\s+', re.I), '发出'),
    (re.compile(r'\binitializes?\s+', re.I), '初始化'),
    (re.compile(r'\bsupports?\s+', re.I), '支持'),
    (re.compile(r'\binteracts?\s+', re.I), '交互'),
    (re.compile(r'\bqueues?\s+', re.I), '排队'),
    (re.compile(r'\brecognizes?\s+', re.I), '识别'),
    (re.compile(r'\bschedules?\s+', re.I), '计划'),
    (re.compile(r'\bmanipulates?\s+', re.I), '操作'),
    (re.compile(r'\bmandates?\s+', re.I), '要求'),

    # ===== Specific words =====
    (re.compile(r'\baddress(es)?\b', re.I), '地址'),
    (re.compile(r'\bmetadata\b', re.I), '元数据'),
    (re.compile(r'\btopology\b', re.I), '拓扑'),
    (re.compile(r'\bchecksum(s)?\b', re.I), '校验和'),
    (re.compile(r'\btimestamp(s)?\b', re.I), '时间戳'),
    (re.compile(r'\brepository\b', re.I), '存储库'),
    (re.compile(r'\bmanifest\b', re.I), '清单文件'),
    (re.compile(r'\bbinary\b', re.I), '二进制'),
    (re.compile(r'\btransaction(s)?\b', re.I), '事务'),
    (re.compile(r'\bduplexity\b', re.I), '双工'),
    (re.compile(r'\bsubject\b', re.I), '主题'),
    (re.compile(r'\bbundle(s)?\b', re.I), '捆绑包'),
    (re.compile(r'\boutput\b', re.I), '输出'),
    (re.compile(r'\binput\b', re.I), '输入'),
    (re.compile(r'\bdefault(s)?\b', re.I), '默认'),
    (re.compile(r'\bformat\b', re.I), '格式'),
    (re.compile(r'\bdetail(s)?\b', re.I), '详细信息'),
    (re.compile(r'\bread\b', re.I), '读取'),
    (re.compile(r'\bwrite\b', re.I), '写入'),
    (re.compile(r'\breader\b', re.I), '读取器'),
    (re.compile(r'\bwriter\b', re.I), '写入器'),
    (re.compile(r'\bprogress\b', re.I), '进度'),
    (re.compile(r'\bruntime\b', re.I), '运行时'),
    (re.compile(r'\bstartup\b', re.I), '启动'),
    (re.compile(r'\bstandalone\b', re.I), '独立'),
    
    # ===== "managed" → "托管" =====
    (re.compile(r'\bmanaged\s+', re.I), '托管'),
    (re.compile(r'\bmanages?\s+', re.I), '管理'),
    
    # ===== Artifacts =====
    (re.compile(r'上加载'), '上传'),
    (re.compile(r'下加载'), '下载'),
    (re.compile(r'up\s*加载'), '上传'),
    (re.compile(r'down\s*加载'), '下载'),
    (re.compile(r'添加ress'), '地址'),
    (re.compile(r'电源\s*[oO][nN]\b'), '打开电源'),
    (re.compile(r'电源\s*[oO][fF]{2}\b'), '关闭电源'),
    (re.compile(r'电源-?[oO][nN]\b'), '打开电源'),
    (re.compile(r'电源-?[oO][fF]{2}\b'), '关闭电源'),
    (re.compile(r'地址es\b'), '地址'),
    (re.compile(r'([\u4e00-\u9fff]+)es\b'), r'\1'),
    
    # ===== Trailing/leading prepositions =====
    (re.compile(r'\s+(for|in|on|at|to|of|by|with|from|the|a|an)\s*$', re.I), ''),
    (re.compile(r'^\s*(for|in|on|at|to|of|by|with|from|the|a|an)\s+', re.I), ''),
    
    # ===== Cleanup =====
    (re.compile(r'[ \t]{2,}'), ' '),
    (re.compile(r'\s+([，。；：、）])'), r'\1'),
    (re.compile(r'^\s+|\s+$'), ''),
]


def main():
    print(f"[{SESSION_TAG}] Reading: {ZH_CN_FILE}")
    with open(ZH_CN_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Backup
    BACKUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    output = []
    fix_count = 0
    total = 0
    still_en = []

    for line in lines:
        s = line.rstrip('\n')
        m = re.match(r'^([A-Za-z0-9_.]+)\.(label|summary)\s*=\s*"(.+)"$', s)
        if m:
            total += 1
            val = m.group(3)
            new_val = val
            for pat, repl in FIXES:
                new_val = pat.sub(repl, new_val)
            new_val = new_val.strip()
            if new_val != val:
                fix_count += 1
            # Check if still English-heavy
            en_c = sum(1 for c in new_val if c.isascii() and c.isalpha())
            zh_c = sum(1 for c in new_val if '\u4e00' <= c <= '\u9fff')
            if en_c + zh_c > 0 and en_c / max(en_c + zh_c, 1) > 0.35:
                still_en.append((f"{m.group(1)}.{m.group(2)}", new_val))
            output.append(f'{m.group(1)}.{m.group(2)} = "{new_val}"\n')
        else:
            output.append(s + '\n')

    with open(ZH_CN_FILE, 'w', encoding='utf-8') as f:
        f.writelines(output)

    # Report
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(f"# v3 Patch Report\n{datetime.datetime.now()}\n\n")
        f.write(f"Total: {total}, Fixed: {fix_count}, Still EN: {len(still_en)}\n")
        if still_en:
            for k, v in still_en[:30]:
                f.write(f"- {k}: {v[:80]}\n")

    print(f"\nDone! Fixed: {fix_count}, Still EN-heavy: {len(still_en)}")


if __name__ == '__main__':
    main()
