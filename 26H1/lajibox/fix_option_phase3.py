with open(r'd:\vmware\i18n\OVFTool\env\zh-CN\option.vmsg', 'r', encoding='utf-8') as f:
    content = f.read()
original = content

replacements = {
    '禁用 有效ation': '禁用验证',
    '有效ation of ': '验证 ',
    '验证 of 用': '验证用户',
    '更新 level of vCenter 服务器': 'vCenter 服务器的更新级别',
    'Long operation 客户端 超时': '长操作客户端超时',
    '日志记录 level': '日志记录级别',
    'Normal 日志记录': '正常日志记录',
    '启用 用户 retrieve 限制s': '启用用户检索限制',
    '用户 retrieve 超时': '用户检索超时',
    'Match 主机 许可证 服务器 to vCenter': '使主机许可证服务器与 vCenter 匹配',
    'Email 地址 for email 警报s (例如, 警报@company.com)': '用于电子邮件警报的电子邮件地址（例如，alarm@company.com）',
    '间隔 in 分钟 介于 each 验证 of 用户 和 组 名称. 设置 to zero to 禁用验证': '每次用户和组名称验证之间的间隔（分钟）。设为零可禁用验证',
    '间隔 in 分钟 介于 each 验证 of 用 户 和 组 名称s. 设置 to zero to 禁用验证': '每次用户和组名称验证之间的间隔（分钟）。设为零可禁用验证',
    'Number of 秒 to wait for a search for 用户 和 组 to return results': '等待用户和组搜索返回结果的秒数',
    'Maximum number of 用户 和 组 to display 在 添加 权限s 对话框': '在添加权限对话框中显示的最大用户和组数',
    'Number of 分钟 介于 each 验证 of all known 用户 和 组 - 设置 to zero to 禁用验证': '所有已知用户和组的每次验证之间的分钟数 - 设为零可禁用验证',
    '启用 验证 of 用户 和 组': '启用用户和组的验证',
    'display 在 添加 权限s 对话框 - 设置 to zero to 禁用 the 限制': '在添加权限对话框中显示 - 设为零可禁用限制',
    'Number of 秒 to wait for a search for 用户 和 组 to return results - 设置 to zero to 禁用 the 超时': '等待用户和组搜索返回结果的秒数 - 设为零可禁用超时',
    'st和by': '备用',
}

count = 0
for old, new in replacements.items():
    c = content.count(old)
    if c:
        content = content.replace(old, new)
        count += c

if content != original:
    with open(r'd:\vmware\i18n\OVFTool\env\zh-CN\option.vmsg', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Phase 3 done ✓ ({count} replacements)")
else:
    print("Phase 3: no changes")
