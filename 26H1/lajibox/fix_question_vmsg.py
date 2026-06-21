#!/usr/bin/env python3
"""
Fix translations in zh-CN/question.vmsg by comparing with en/question.vmsg.
Safe for concurrent sessions via lock file + atomic write.
"""
import os, sys, json, socket, tempfile, shutil, time as time_module

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VMSG_DIR = os.path.join(BASE_DIR, "OVFTool", "env")
LOCK_FILE = os.path.join(VMSG_DIR, ".fix_question_vmsg.lock")
EN_FILE = os.path.join(VMSG_DIR, "en", "question.vmsg")
ZH_FILE = os.path.join(VMSG_DIR, "zh-CN", "question.vmsg")

EN_TO_ZH = {
    "Stop": "停止", "Allow": "允许", "Allow all": "全部允许",
    "Always ignore": "始终忽略", "Always keep": "始终保留",
    "Append": "追加", "Before suspending": "挂起前",
    "Browse": "浏览", "Cancel": "取消", "Commit": "提交",
    "Continue": "继续", "Debug": "调试", "Deny": "拒绝",
    "Deny all": "全部拒绝", "Device": "设备",
    "General": "常规", "Help": "帮助", "Ignore": "忽略",
    "Ignore all": "全部忽略", "Install": "安装", "Keep": "保留",
    "Miscellaneous": "其他", "No": "否", "OK": "确定",
    "Options": "选项", "Overwrite": "覆盖", "Preserve": "保留",
    "Replace": "替换", "Retry": "重试", "Save": "保存",
    "Settings": "设置", "Support": "支持", "Upgrade": "升级",
    "Yes": "是",
    "_Back": "_后退", "_Cancel": "_取消", "_Close": "_关闭",
    "_Delete": "_删除", "_Finish": "_完成", "_Next": "_下一步",
    "Independent-nonpersistent": "独立-非持久",
    "Independent-persistent": "独立-持久",
    "Nonpersistent": "非持久", "Persistent": "持久",
    "Undoable": "可撤消", "vmnet": "vmnet",
}

SPECIFIC_FIXES = {
    "Answer.Always Create": "总是创建",
    "Answer.Before powering off": "关闭电源前",
    "Answer.Current version": "当前版本",
    "Answer.Delete Team and _VMs": "删除团队和虚拟机",
    "Answer.Disable Acceleration": "禁用加速",
    "Answer.Enter Serial Number...": "输入序列号...",
    "Answer.Just Power Off": "仅关闭电源",
    "Answer.Logging level": "日志记录级别",
    "Answer.Previous version": "上一个版本",
    "Answer.Reload File": "重新加载文件",
    "Answer.Request Support": "请求支持",
    "Answer.Revert to Snapshot": "还原到快照",
    "Answer.Run with debugging information": "使用调试信息运行",
    "Answer.Save Anyway": "仍然保存",
    "Answer.Save As...": "另存为...",
    "Answer.Take a Snapshot": "拍摄快照",
    "Answer.VM > Removable Devices": "虚拟机 > 可移动设备",
    "Answer.Working Directory": "工作目录",
    "Answer.Abort": "停止",
    "Answer.Browse...": "浏览...",
}

def acquire_lock():
    content = f"{socket.gethostname()}:{os.getpid()}"
    try:
        fd = os.open(LOCK_FILE, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        with os.fdopen(fd, 'w') as f:
            f.write(content)
        return True
    except FileExistsError:
        try:
            if time_module.time() - os.path.getmtime(LOCK_FILE) > 300:
                os.remove(LOCK_FILE)
                return acquire_lock()
        except OSError:
            pass
        return False

def release_lock():
    try:
        os.remove(LOCK_FILE)
    except OSError:
        pass

def parse_vmsg(path):
    result = {}
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n').rstrip('\r')
            if line.startswith('#') or line.startswith('signature=') or line.startswith('###'):
                continue
            if '=' in line:
                k, _, v = line.partition('=')
                key = k.strip()
                val = v.strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                result[key] = val
    return result

def fix_translations(en_values, zh_values):
    fixed, changes = {}, []
    
    for key in sorted(zh_values.keys()):
        current = zh_values[key]
        en_val = en_values.get(key, "")

        # 1) Specific known fixes first
        if key in SPECIFIC_FIXES:
            target = SPECIFIC_FIXES[key]
            if current != target:
                changes.append((key, current, target, "修正中英混杂/翻译错误"))
            fixed[key] = target
            continue

        # 2) Direct EN->ZH mapping
        if en_val in EN_TO_ZH:
            target = EN_TO_ZH[en_val]
            if current != target:
                changes.append((key, current, target, "完整翻译"))
            fixed[key] = target
            continue

        # 3) Keep as-is (already correct)
        fixed[key] = current

    return fixed, changes

def main():
    if not acquire_lock():
        print("锁文件存在，其他会话可能正在运行中。")
        sys.exit(1)
    
    try:
        en = parse_vmsg(EN_FILE)
        zh = parse_vmsg(ZH_FILE)
        
        missing = [k for k in en if k not in zh]
        if missing:
            print(f"警告: zh-CN 缺少 {len(missing)} 个键")
            for k in missing:
                print(f"  {k} = \"{en[k]}\"")
            # Add missing keys
            for k in missing:
                zh[k] = en[k]
        
        fixed, changes = fix_translations(en, zh)
        
        total = len(fixed)
        n_changed = len(changes)
        print(f"总条目: {total}, 修正: {n_changed}, 正确: {total - n_changed}")
        
        if changes:
            for k, old, new, reason in changes:
                print(f"\n  [{k}]")
                print(f"    原值: \"{old}\"")
                print(f"    新值: \"{new}\"")
                print(f"    原因: {reason}")
        
        if not changes:
            print("✓ 全部翻译正确，无需修改")
            return
        
        # Atomic write
        fd, tmp = tempfile.mkstemp(suffix='.vmsg', prefix='.question_fixed_', dir=os.path.dirname(ZH_FILE))
        os.close(fd)
        
        # Write header
        with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
            f.write("# zh_CN resources\n")
            f.write('signature="sIgNaTuRe"\n')
            f.write("###\n")
            for key in sorted(fixed.keys()):
                f.write(f'{key}="{fixed[key]}"\n')
        
        shutil.move(tmp, ZH_FILE)
        print(f"\n✅ 已修正 {n_changed} 处 → {ZH_FILE}")
    finally:
        release_lock()

if __name__ == "__main__":
    main()
