import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    changes = []

    # 1. "已" prefix abuse
    for old in ["已更新","已启用","已禁用","已创建","已添加","已分配","已消耗","已更改","已修改","已注册","已升级","已过期","已删除","已移除"]:
        new = old[1:]
        p = re.compile(r'(="[^"]*?)' + re.escape(old) + r'([^"]*")')
        c = len(p.findall(content))
        if c:
            content = p.sub(r'\1' + new + r'\2', content)
            changes.append(f"{old}->{new}: {c}")

    # 2. "已用" -> "使用"
    p = re.compile(r'(="[^"]*?)已用([^"]*")')
    c = len(p.findall(content))
    if c:
        content = p.sub(r'\1使用\2', content)
        changes.append(f"已用->使用: {c}")

    # 3. "A挂载" -> "量"
    p = re.compile(r'(="[^"]*?)A挂载([^"]*")')
    c = len(p.findall(content))
    if c:
        content = p.sub(r'\1量\2', content)
        changes.append(f"A挂载->量: {c}")

    # 4. "接收r" -> "接收器"
    p = re.compile(r'(="[^"]*?)接收r([^"]*")')
    c = len(p.findall(content))
    if c:
        content = p.sub(r'\1接收器\2', content)
        changes.append(f"接收r->接收器: {c}")

    # 5. "计数ry" -> "国家"
    p = re.compile(r'(="[^"]*?)计数ry([^"]*")')
    c = len(p.findall(content))
    if c:
        content = p.sub(r'\1国家\2', content)
        changes.append(f"计数ry->国家: {c}")

    # 6. "正在X" -> "X"
    for old in ["正在监控","正在添加","正在扫描","正在运行","正在克隆","正在使用","正在注册","正在生成","正在处理","正在加载","正在等待","正在执行"]:
        new = old[2:]
        p = re.compile(r'(="[^"]*?)' + re.escape(old) + r'([^"]*")')
        c = len(p.findall(content))
        if c:
            content = p.sub(r'\1' + new + r'\2', content)
            changes.append(f"{old}->{new}: {c}")

    # 7. Remove leading "The "/"the "
    for prefix in ["The ", "the "]:
        p = re.compile(r'(=")' + re.escape(prefix) + r'([^"]*")')
        c = len(p.findall(content))
        if c:
            content = p.sub(r'\1\2', content)
            changes.append(f"remove '{prefix}': {c}")

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Phase 1 done ✓")
    else:
        print("Phase 1: no changes")

    for c in changes:
        print(f"  {c}")

if __name__ == '__main__':
    fix_file(r'd:\vmware\i18n\OVFTool\env\zh-CN\option.vmsg')
