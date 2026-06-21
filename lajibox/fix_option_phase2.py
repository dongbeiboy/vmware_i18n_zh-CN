import re

with open(r'd:\vmware\i18n\OVFTool\env\zh-CN\option.vmsg', 'r', encoding='utf-8') as f:
    content = f.read()
original = content
changes = []

# Fix batch 1: Chinese-English plural suffixes
plural_fixes = {'用户s':'用户','组s':'组','日志s':'日志','日志gers':'记录器','日志ger':'记录器'}
for old, new in plural_fixes.items():
    p = re.compile(r'(="[^"]*?)' + re.escape(old) + r'([^"]*")')
    c = len(p.findall(content))
    if c:
        content = p.sub(r'\1' + new + r'\2', content)
        changes.append(f"{old}->{new}: {c}")

# Fix batch 2: Half-translated terms
half_fixes = {'re端口':'报告','sup端口':'支持','添加ress':'地址','ac计数ing':'累计','dia日志':'对话框','有效ation':'验证','设置tings':'设置'}
for old, new in half_fixes.items():
    p = re.compile(r'(="[^"]*?)' + re.escape(old) + r'([^"]*")')
    c = len(p.findall(content))
    if c:
        content = p.sub(r'\1' + new + r'\2', content)
        changes.append(f"{old}->{new}: {c}")

# Fix batch 3: Ordinal SNMP labels
ordinal_fixes = {
    'First SNMP 接收器 名称':'第一个 SNMP 接收器名称', 'Second SNMP 接收器 名称':'第二个 SNMP 接收器名称',
    'Third SNMP 接收器 名称':'第三个 SNMP 接收器名称', 'Fourth SNMP 接收器 名称':'第四个 SNMP 接收器名称',
    'First SNMP 接收器 端口':'第一个 SNMP 接收器端口', 'Second SNMP 接收器 端口':'第二个 SNMP 接收器端口',
    'Third SNMP 接收器 端口':'第三个 SNMP 接收器端口', 'Fourth SNMP 接收器 端口':'第四个 SNMP 接收器端口',
    'First SNMP 接收器 community':'第一个 SNMP 接收器团体字符串', 'Second SNMP 接收器 community':'第二个 SNMP 接收器团体字符串',
    'Third SNMP 接收器 community':'第三个 SNMP 接收器团体字符串', 'Fourth SNMP 接收器 community':'第四个 SNMP 接收器团体字符串',
    '启用 first SNMP 接收器':'启用第一个 SNMP 接收器', '启用 second SNMP 接收器':'启用第二个 SNMP 接收器',
    '启用 third SNMP 接收器':'启用第三个 SNMP 接收器', '启用 fourth SNMP 接收器':'启用第四个 SNMP 接收器',
}
for old, new in ordinal_fixes.items():
    c = content.count(old)
    if c:
        content = content.replace(old, new)
        changes.append(f"ordinal: {c}")

# Fix batch 4: Summary translations
summary_fixes = {
    'SNMP 接收器 端口 number. If the 端口 number 不 设置, the Windows default is 使用, —— typically 端口 162':'SNMP 接收器端口号。如果未设置端口号，则使用 Windows 默认值，通常为端口 162',
    'Email 添加ress for email 警报s (例如, 警报@company.com)':'用于电子邮件警报的电子邮件地址（例如，alarm@company.com）',
    'Community string for SNMP trap (例如, public)':'SNMP 陷阱的团体字符串（例如，public）',
    'Whether SNMP traps are sent to this SNMP 接收器':'是否将 SNMP 陷阱发送到此 SNMP 接收器',
    'SMTP 服务器 IP 地址 or DNS 名称 (例如, smtp.company.com)':'SMTP 服务器 IP 地址或 DNS 名称（例如，smtp.company.com）',
    'SMTP 服务器 端口 number. Typically, this 端口 number is 25':'SMTP 服务器端口号。通常此端口号为 25',
    'Major database 版本':'数据库主版本', 'Major database schema 版本':'数据库架构主版本',
    'Minor database 版本':'数据库次版本', 'Minor database schema 版本':'数据库架构次版本',
    'Maximum 用户s to retrieve':'要检索的最大用户数',
    'Interval in 分钟 介于 each 有效ation of 用户 和 组 名称s. 设置 to zero to 禁用 有效ation':'每次用户和组名称验证之间的间隔（分钟）。设为零可禁用验证',
    'Maximum number of 用户s 和 组s to display 在 添加 权限s dia日志':'在添加权限对话框中显示的最大用户和组数',
    'Number of 秒 to wait for a search for 用户s 和 组s to return results':'等待用户和组搜索返回结果的秒数',
    '启用 有效ation of 用户s 和 组s':'启用用户和组的验证',
}
for old, new in summary_fixes.items():
    c = content.count(old)
    if c:
        content = content.replace(old, new)
        changes.append(f"summary: {c}")

if content != original:
    with open(r'd:\vmware\i18n\OVFTool\env\zh-CN\option.vmsg', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Phase 2 done ✓")
    for c in changes:
        print(f"  {c}")
else:
    print("Phase 2: no changes")
