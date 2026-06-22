#!/usr/bin/env python3
"""
Fix Chinese translations in key_en_ja_cn.csv (v2).

Approach: Protect URLs/placeholders, then safely fix common patterns.
Only operate on strings that have MIXED Chinese+English (hybrid) content.
"""

import csv
import re
import os
import sys
import time

INPUT_FILE = os.path.join(os.path.dirname(__file__), "key_en_ja_cn.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "key_en_ja_cn_fixed.csv")

# ─── URL and placeholder protection ──────────────────────────────────
# These patterns must be preserved exactly

def protect(text):
    """Replace protected patterns with placeholders and return mapping."""
    placeholders = {}
    
    # URLs
    def _protect_url(m):
        idx = len(placeholders)
        ph = f'__URL_{idx}__'
        placeholders[ph] = m.group(0)
        return ph
    text = re.sub(r'https?://[^\s,;)]+', _protect_url, text)
    
    # Placeholders like {0}, {paramName}, {operator}, {red.value,l}
    def _protect_placeholder(m):
        idx = len(placeholders)
        ph = f'__PH_{idx}__'
        placeholders[ph] = m.group(0)
        return ph
    text = re.sub(r'\{[^}]+\}', _protect_placeholder, text)
    
    # Format placeholders like %1, %2, %1$s, %1$d
    def _protect_fmt(m):
        idx = len(placeholders)
        ph = f'__FMT_{idx}__'
        placeholders[ph] = m.group(0)
        return ph
    text = re.sub(r'%\d+(?:\$[a-zA-Z0-9|]+)?', _protect_fmt, text)
    
    # VMware KB article numbers
    def _protect_kb(m):
        idx = len(placeholders)
        ph = f'__KB_{idx}__'
        placeholders[ph] = m.group(0)
        return ph
    text = re.sub(r'kb\.vmware\.com[^\s,;)]*', _protect_kb, text)
    text = re.sub(r'knowledge\.broadcom\.com[^\s,;)]*', _protect_kb, text)
    
    # Signature value
    def _protect_sig(m):
        return m.group(0)  # Keep sIgNaTuRe as-is
    text = re.sub(r'sIgNaTuRe', _protect_sig, text)
    
    return text, placeholders

def unprotect(text, placeholders):
    """Restore protected patterns."""
    for ph, original in placeholders.items():
        text = text.replace(ph, original)
    return text


# ─── Safe replacements ───────────────────────────────────────────────
# Only for texts that have mixed Chinese+English content

# Fix English plural s appended to Chinese words
PLURAL_FIXES = [
    (r'数据存储s(?!\w)', '数据存储'),
    (r'虚拟机s(?!\w)', '虚拟机'),
    (r'主机s(?!\w)', '主机'),
    (r'服务器s(?!\w)', '服务器'),
    (r'客户端s(?!\w)', '客户端'),
    (r'数据中心s(?!\w)', '数据中心'),
    (r'文件夹s(?!\w)', '文件夹'),
    (r'磁盘s(?!\w)', '磁盘'),
    (r'网络s(?!\w)', '网络'),
    (r'端口s(?!\w)', '端口'),
    (r'证书s(?!\w)', '证书'),
    (r'值s(?!\w)', '值'),
    (r'状态s(?!\w)', '状态'),
    (r'事件s(?!\w)', '事件'),
    (r'错误s(?!\w)', '错误'),
    (r'任务s(?!\w)', '任务'),
    (r'资源s(?!\w)', '资源'),
    (r'服务s(?!\w)', '服务'),
    (r'设备s(?!\w)', '设备'),
    (r'对象s(?!\w)', '对象'),
    (r'文件s(?!\w)', '文件'),
    (r'用户s(?!\w)', '用户'),
    (r'接口s(?!\w)', '接口'),
    (r'组件s(?!\w)', '组件'),
    (r'属性s(?!\w)', '属性'),
    (r'角色s(?!\w)', '角色'),
    (r'策略s(?!\w)', '策略'),
    (r'代理s(?!\w)', '代理'),
    (r'控制器s(?!\w)', '控制器'),
    (r'处理器s(?!\w)', '处理器'),
    (r'传感器s(?!\w)', '传感器'),
    (r'许可证s(?!\w)', '许可证'),
    (r'密钥s(?!\w)', '密钥'),
    (r'键s(?!\w)', '键'),
    (r'卷s(?!\w)', '卷'),
    (r'池s(?!\w)', '池'),
    (r'分区s(?!\w)', '分区'),
    (r'适配器s(?!\w)', '适配器'),
    (r'扩展s(?!\w)', '扩展'),
    (r'权限s(?!\w)', '权限'),
    (r'特权s(?!\w)', '特权'),
    (r'间隔s(?!\w)', '间隔'),
    (r'选项卡s(?!\w)', '选项卡'),
    (r'描述s(?!\w)', '描述'),
    (r'配置s(?!\w)', '配置'),
    (r'操作s(?!\w)', '操作'),
    (r'模块s(?!\w)', '模块'),
    (r'名称s(?!\w)', '名称'),
    (r'组s(?!\w)', '组'),
    (r'信息s(?!\w)', '信息'),
    (r'连接s(?!\w)', '连接'),
    (r'备份s(?!\w)', '备份'),
    (r'日志s(?!\w)', '日志'),
    (r'规则s(?!\w)', '规则'),
    (r'标签s(?!\w)', '标签'),
    (r'路径s(?!\w)', '路径'),
    (r'类型s(?!\w)', '类型'),
    (r'值s(?!\w)', '值'),
]

# Known wrong translations and typos
TYPO_FIXES = [
    # "电流" as "current" in non-electrical context → "当前" but only in 
    # specific alarm/summary/label contexts (not in electrical terms like "电压")
    (r'电流 值', '当前值'),
    (r'电流 状态', '当前状态'),
    (r'电流 配置', '当前配置'),
    (r'电流 版本', '当前版本'),
    (r'电流 名称', '当前名称'),
    (r'电流 用户', '当前用户'),
    (r'电流 使用率', '当前使用率'),
    (r'电流 容量', '当前容量'),
    (r'电流 活动', '当前活动'),
    (r'电流 限制', '当前限制'),
    (r'电流 监控', '当前监控'),
    (r'电流 事件', '当前事件'),
    (r'电流 信息', '当前信息'),
    (r'电流 操作', '当前操作'),
    (r'电流 连接', '当前连接'),
    (r'电流ly', '当前'),
    
    # Typo fixes
    (r'连接ion', '连接'),
    (r'provIDEr', '提供程序'),
    (r'IDEntity', '标识'),
    (r'添加ress', '处理'),
    (r'at测试ation', '证明'),  # attestation
    (r'测试ing', '测试'),  # testing (in wrong context)
    (r'验证ing', '验证'),
    (r'正在ing', '正在'),
    (r'cata日志', '目录'),  # catalog
    
    # "已用" used incorrectly for "used by" / "used for"
    (r'已用 由', '由'),
    (r'已用 for', '用于'),
    (r'已用 by', '由'),
    (r'已用 in', '在'),
    (r'已用 to', '用于'),
    (r'^已用 ', '用于'),
    (r' 已用$', ''),
    
    # Wrong suffix "d" for past tense
    (r'定义d', '定义'),
    (r'限制d', '限制'),
    (r'启用d', '启用'),
    (r'禁用d', '禁用'),
    (r'配置d', '配置'),
    (r'分配d', '分配'),
    (r'注册d', '注册'),
    (r'安装d', '安装'),
    (r'更新d', '更新'),
    (r'更改d', '更改'),
    (r'设置d', '设置'),
    (r'重命名d', '重命名'),
    (r'选择d', '选择'),
    (r'隔离d', '隔离'),
    (r'组合d', '组合'),
    (r'修改d', '修改'),
    (r'组合d', '组合'),
    (r'基于d', '基于'),
    
    # "电源 on/off" patterns
    (r'电源 on\b', '打开电源'),
    (r'电源 off\b', '关闭电源'),
    (r'电源ed on\b', '已开机'),
    (r'电源ed off\b', '已关机'),
    
    # Spacing fixes for "已X" patterns
    (r'已 更新', '已更新'),
    (r'已 完成', '已完成'),
    (r'已 配置', '已配置'),
    (r'已 启用', '已启用'),
    (r'已 禁用', '已禁用'),
    (r'已 连接', '已连接'),
    (r'已 断开', '已断开'),
    (r'已 安装', '已安装'),
    (r'已 更改', '已更改'),
    (r'已 取消', '已取消'),
    (r'已 创建', '已创建'),
    (r'已 注册', '已注册'),
    (r'已 注销', '已注销'),
    (r'已 移动', '已移动'),
    (r'已 停止', '已停止'),
    (r'已 重新启动', '已重新启动'),
    (r'已 过期', '已过期'),
    (r'已 修复', '已修复'),
    (r'已 保留', '已保留'),
    (r'已 同步', '已同步'),
    (r'已 复制', '已复制'),
    (r'已 删除', '已删除'),
    (r'已 添加', '已添加'),
    (r'已 移除', '已移除'),
    (r'已 替换', '已替换'),
    (r'已 解决', '已解决'),
    (r'已 恢复', '已恢复'),
    (r'已 加密', '已加密'),
    (r'已 解密', '已解密'),
    (r'已 关闭', '已关闭'),
    (r'已 打开', '已打开'),
    (r'已 分配', '已分配'),
    (r'已 设置', '已设置'),
    (r'已 使用', '已使用'),
    (r'已 释放', '已释放'),
    (r'已 公布', '已公布'),
    (r'已 发布', '已发布'),

    # "不 X" spacing
    (r'不 兼容', '不兼容'),
    (r'不 支持', '不支持'),
    (r'不 可用', '不可用'),
    (r'不 活动', '不活动'),
    (r'不 允许', '不允许'),
    (r'不 匹配', '不匹配'),
    (r'不 正确', '不正确'),
    (r'不 一致', '不一致'),
    (r'不 充分', '不充分'),
    (r'不 合法', '不合法'),
    (r'不 相同', '不相同'),
    (r'不 稳定', '不稳定'),
    (r'不 需要', '不需要'),
    (r'不 相关', '不相关'),
    (r'不 确定', '不确定'),
    (r'不 连续', '不连续'),
    (r'不 能', '不能'),
    (r'不 存在', '不存在'),

    # "未 X" patterns
    (r'未 配置', '未配置'),
    (r'未 使用', '未使用'),
    (r'未 找到', '未找到'),
    (r'未 指定', '未指定'),
    (r'未 定义', '未定义'),
    (r'未 成功', '未成功'),
    (r'未 完成', '未完成'),
    (r'未 启用', '未启用'),
    (r'未 分配', '未分配'),
    (r'未 验证', '未验证'),
    (r'未 授权', '未授权'),
    (r'未 注册', '未注册'),
    (r'未 命名', '未命名'),
    (r'未 锁定', '未锁定'),
    (r'未 保护', '未保护'),
    (r'未 就绪', '未就绪'),
    (r'未 连接', '未连接'),
    (r'未 安装', '未安装'),
    (r'未 设置', '未设置'),
    (r'未 标记', '未标记'),

    # "可 X" spacing
    (r'可 用', '可用'),
    (r'可 配置', '可配置'),
    (r'可 选择', '可选择'),
    (r'可 访问', '可访问'),
    (r'可 管理', '可管理'),
    (r'可 移动', '可移动'),
    (r'可 执行', '可执行'),
    (r'可 预测', '可预测'),
    (r'可 传输', '可传输'),
    (r'可 操作', '可操作'),
    (r'可 授权', '可授权'),
    (r'可 信赖', '可信赖'),
]

# English articles and fillers to remove from mixed Chinese-English text
# These only apply when the text has Chinese characters
ENGLISH_FILLERS = [
    (r'\ba\b', ''),
    (r'\ban\b', ''),
    (r'\bthe\b', ''),
    (r'\bthis\b', ''),
    (r'\bthat\b', ''),
    (r'\bthese\b', ''),
    (r'\bis\b', ''),
    (r'\bare\b', ''),
    (r'\bhas\b', ''),
    (r'\bhave\b', ''),
    (r'\bbeen\b', ''),
    (r'\bwas\b', ''),
    (r'\bwere\b', ''),
    (r'\bwill\b', ''),
    (r'\bbe\b', ''),
    (r'\bfor\b', ''),
    (r'\bwith\b', ''),
    (r'\bfrom\b', ''),
    (r'\bby\b', ''),
    (r'\bto\b', ''),
    (r'\bor\b', ''),
    (r'\bin\b', ''),
    (r'\bon\b', ''),
    (r'\bat\b', ''),
    (r'\bas\b', ''),
    (r'\bof\b', ''),
    (r'\band\b', ''),
    (r'\bnot\b', ''),
    (r'\bno\b', ''),
    (r'\bany\b', ''),
    (r'\bsome\b', ''),
    (r'\ball\b', ''),
    (r'\beach\b', ''),
    (r'\bits\b', ''),
    (r'\bits\b', ''),
    (r'\bour\b', ''),
    (r'\byour\b', ''),
    (r'\btheir\b', ''),
    (r'\bthem\b', ''),
    (r'\bit\b', ''),
    (r'\bcan\b', ''),
    (r'\bmay\b', ''),
    (r'\bmust\b', ''),
    (r'\bshould\b', ''),
    (r'\bwould\b', ''),
    (r'\bcould\b', ''),
    (r'\bdoes\b', ''),
    (r'\bdo\b', ''),
    (r'\bdid\b', ''),
    (r'\bif\b', ''),
    (r'\bwhile\b', ''),
    (r'\bwhen\b', ''),
    (r'\bwhere\b', ''),
    (r'\bwhich\b', ''),
    (r'\bwho\b', ''),
    (r'\bwhom\b', ''),
    (r'\bwhat\b', ''),
    (r'\bhow\b', ''),
    (r'\bthan\b', ''),
    (r'\bthen\b', ''),
    (r'\bjust\b', ''),
    (r'\balso\b', ''),
    (r'\bvery\b', ''),
    (r'\balready\b', ''),
    (r'\babout\b', ''),
    (r'\babove\b', ''),
    (r'\bafter\b', ''),
    (r'\bagain\b', ''),
    (r'\bagainst\b', ''),
    (r'\bbeing\b', ''),
    (r'\bbelow\b', ''),
    (r'\bbetween\b', ''),
    (r'\bboth\b', ''),
    (r'\bduring\b', ''),
    (r'\beither\b', ''),
    (r'\bfurther\b', ''),
    (r'\bhere\b', ''),
    (r'\bthere\b', ''),
    (r'\bsince\b', ''),
    (r'\bstill\b', ''),
    (r'\bsuch\b', ''),
    (r'\bthrough\b', ''),
    (r'\btoo\b', ''),
    (r'\bunder\b', ''),
    (r'\buntil\b', ''),
    (r'\bup\b', ''),
    (r'\bwell\b', ''),
    (r'\byet\b', ''),
    (r'\bmore\b', ''),
    (r'\bmost\b', ''),
    (r'\bmuch\b', ''),
    (r'\bmany\b', ''),
    (r'\bsame\b', ''),
    (r'\bonly\b', ''),
    (r'\bother\b', ''),
    (r'\banother\b', ''),
    (r'\bevery\b', ''),
    (r'\bnow\b', ''),
    (r'\balways\b', ''),
    (r'\bnever\b', ''),
    (r'\boften\b', ''),
    (r'\bover\b', ''),
    (r'\bout\b', ''),
    (r'\binto\b', ''),
    (r'\bonto\b', ''),
    (r'\bupon\b', ''),
    (r'\bwithout\b', ''),
    (r'\bwithin\b', ''),
    (r'\bexcept\b', ''),
    (r'\bdown\b', ''),
    (r'\boff\b', ''),
    (r'\bvia\b', ''),
    (r'\bper\b', ''),
    (r'\bthan\b', ''),
]

REPLACE_PATTERNS = [
    # Default alarm → 默认警报
    (r'Default alarm', '默认警报'),
    (r'Default 警报', '默认警报'),
    
    # Health → 运行状况 (in alarm/service context)
    (r'Health alarm', '运行状况警报'),
    (r'Health 警报', '运行状况警报'),
    (r'Health status', '运行状况'),
    (r'Health 状态', '运行状况'),
    (r'health status', '运行状况'),
    (r'health 状态', '运行状况'),
    
    # Status → 状态
    (r'Status\b', '状态'),
    (r' status\b', ' 状态'),
    
    # "to monitor" → "监控"
    (r'to monitor', '监控'),
    
    # "is triggered" → "触发"
    (r'is triggered', '触发'),
    (r'is 触发', '触发'),
    
    # "Alarm to / Alarm that" → "警报"
    (r'Alarm to', '警报：'),
    (r'Alarm that', '警报：'),
    (r'警报 to', '警报：'),
    (r'警报 that', '警报：'),
    
    # "Please" → "请"
    (r'\bPlease\b', '请'),
    
    # "See the" → "请参阅"
    (r'See the', '请参阅'),
    (r'See 请参阅', '请参阅'),
    
    # "for more details" → ""
    (r'for more details', '以了解详细信息'),
    (r'for details', '以了解详细信息'),
    
    # "Refer to" / "refer to" → "请参阅"
    (r'Refer to\b', '请参阅'),
    (r'Refer\b(?!\s)', '请参阅'),
    
    # follow(s) → 按照
    (r'\bfollow\b', '按照'),
    (r'\bfollowing\b', '以下'),
    
    # "Failed to X" → "X失败"
    # This is complex, handle specific cases
    (r'Failed to update the', '更新'),
    (r'Failed to update', '更新'),
    (r'失败 to update', '更新'),
    (r'失败 to 更新', '更新失败'),
    (r'failed to', '失败'),
    
    # "is about to" → "即将"
    (r'is about to', '即将'),
    
    # Fix remaining known plurals
    (r'certificates', '证书'),
    (r'certificate', '证书'),
    
    # "due to" → ""
    (r'\bdue to\b', ''),
    (r' due ', ''),
    
    # Various verbs
    (r'\bConnect\b', '连接'),
    (r'\bconnect\b', '连接'),
    (r'\bConfigure\b', '配置'),
    (r'\bconfigure\b', '配置'),
    (r'\bManage\b', '管理'),
    (r'\bmanage\b', '管理'),
    (r'\bCreate\b', '创建'),
    (r'\bcreate\b', '创建'),
    (r'\bDelete\b', '删除'),
    (r'\bdelete\b', '删除'),
    (r'\bRemove\b', '移除'),
    (r'\bremove\b', '移除'),
    (r'\bUpdate\b', '更新'),
    (r'\bupdate\b', '更新'),
    (r'\bInstall\b', '安装'),
    (r'\binstall\b', '安装'),
    
    # Nouns
    (r'\bHost\b', '主机'),
    (r'\bhost\b', '主机'),
    (r'\bServer\b', '服务器'),
    (r'\bserver\b', '服务器'),
    (r'\bCluster\b', '集群'),
    (r'\bcluster\b', '集群'),
    (r'\bDatacenter\b', '数据中心'),
    (r'\bdatacenter\b', '数据中心'),
    (r'\bDatastore\b', '数据存储'),
    (r'\bdatastore\b', '数据存储'),
    (r'\bVirtual\s+machine\b', '虚拟机'),
    (r'\bvirtual\s+machine\b', '虚拟机'),
    (r'\bVirtual\s+disk\b', '虚拟磁盘'),
    (r'\bvirtual\s+disk\b', '虚拟磁盘'),
    (r'\bNetwork\b', '网络'),
    (r'\bnetwork\b', '网络'),
    (r'\bStorage\b', '存储'),
    (r'\bstorage\b', '存储'),
    (r'\bMemory\b', '内存'),
    (r'\bmemory\b', '内存'),
    (r'\bDisk\b', '磁盘'),
    (r'\bdisk\b', '磁盘'),
    (r'\bDevice\b', '设备'),
    (r'\bdevice\b', '设备'),
    (r'\bPort\b', '端口'),
    (r'\bport\b', '端口'),
    (r'\bResource\b', '资源'),
    (r'\bresource\b', '资源'),
    (r'\bService\b', '服务'),
    (r'\bservice\b', '服务'),
    (r'\bLicense\b', '许可证'),
    (r'\blicense\b', '许可证'),
    (r'\bUser\b', '用户'),
    (r'\buser\b', '用户'),
    (r'\bAgent\b', '代理'),
    (r'\bagent\b', '代理'),
    (r'\bClient\b', '客户端'),
    (r'\bclient\b', '客户端'),
    (r'\bConsole\b', '控制台'),
    (r'\bconsole\b', '控制台'),
    (r'\bFolder\b', '文件夹'),
    (r'\bfolder\b', '文件夹'),
    (r'\bFile\b', '文件'),
    (r'\bfile\b', '文件'),
    (r'\bDirectory\b', '目录'),
    (r'\bdirectory\b', '目录'),
    (r'\bDatabase\b', '数据库'),
    (r'\bdatabase\b', '数据库'),
    (r'\bConfiguration\b', '配置'),
    (r'\bconfiguration\b', '配置'),
    (r'\bConfig\b', '配置'),
    (r'\bconfig\b', '配置'),
    (r'\bOperation\b', '操作'),
    (r'\boperation\b', '操作'),
    (r'\bAction\b', '操作'),
    (r'\baction\b', '操作'),
    (r'\bEvent\b', '事件'),
    (r'\bevent\b', '事件'),
    (r'\bAlarm\b', '警报'),
    (r'\balarm\b', '警报'),
    (r'\bWarning\b', '警告'),
    (r'\bwarning\b', '警告'),
    (r'\bError\b', '错误'),
    (r'\berror\b', '错误'),
    (r'\bFailure\b', '失败'),
    (r'\bfailure\b', '失败'),
    (r'\bSuccess\b', '成功'),
    (r'\bsuccess\b', '成功'),
    (r'\bEnabled\b', '已启用'),
    (r'\benabled\b', '已启用'),
    (r'\bDisabled\b', '已禁用'),
    (r'\bdisabled\b', '已禁用'),
    (r'\bConnected\b', '已连接'),
    (r'\bconnected\b', '已连接'),
    (r'\bDisconnected\b', '已断开连接'),
    (r'\bdisconnected\b', '已断开连接'),
    (r'\bConfigured\b', '已配置'),
    (r'\bconfigured\b', '已配置'),
    (r'\bInstalled\b', '已安装'),
    (r'\binstalled\b', '已安装'),
    (r'\bFailed\b', '失败'),
    (r'\bfailed\b', '失败'),
    (r'\bUpdated\b', '已更新'),
    (r'\bupdated\b', '已更新'),
    (r'\bChanged\b', '已更改'),
    (r'\bchanged\b', '已更改'),
    (r'\bRemoved\b', '已移除'),
    (r'\bremoved\b', '已移除'),
    (r'\bCreated\b', '已创建'),
    (r'\bcreated\b', '已创建'),
    (r'\bRegistered\b', '已注册'),
    (r'\bregistered\b', '已注册'),
    (r'\bUnregistered\b', '已注销'),
    (r'\bunregistered\b', '已注销'),
    (r'\bUpgrade\b', '升级'),
    (r'\bupgrade\b', '升级'),
    (r'\bMigrate\b', '迁移'),
    (r'\bmigrate\b', '迁移'),
    (r'\bMigration\b', '迁移'),
    (r'\bmigration\b', '迁移'),
    (r'\bReplication\b', '复制'),
    (r'\breplication\b', '复制'),
    (r'\bEncryption\b', '加密'),
    (r'\bencryption\b', '加密'),
    (r'\bEncrypt\b', '加密'),
    (r'\bencrypt\b', '加密'),
    (r'\bMonitoring\b', '监控'),
    (r'\bmonitoring\b', '监控'),
    (r'\bMonitor\b', '监控'),
    (r'\bmonitor\b', '监控'),
    (r'\bManager\b', '管理器'),
    (r'\bmanager\b', '管理器'),
    (r'\bManagement\b', '管理'),
    (r'\bmanagement\b', '管理'),
    (r'\bDefault\b', '默认'),
    (r'\bdefault\b', '默认'),
    (r'\bCurrent\b', '当前'),
    (r'\bcurrent\b', '当前'),
    (r'\bValue\b', '值'),
    (r'\bvalue\b', '值'),
    (r'\bName\b', '名称'),
    (r'\bname\b', '名称'),
    (r'\bType\b', '类型'),
    (r'\btype\b', '类型'),
    (r'\bCount\b', '计数'),
    (r'\bcount\b', '计数'),
    (r'\bSupported\b', '支持'),
    (r'\bsupported\b', '支持'),
    (r'\bAvailable\b', '可用'),
    (r'\bavailable\b', '可用'),
    (r'\bTimeout\b', '超时'),
    (r'\btimeout\b', '超时'),
    (r'\bBackup\b', '备份'),
    (r'\bbackup\b', '备份'),
    (r'\bRestore\b', '恢复'),
    (r'\brestore\b', '恢复'),
    (r'\bSnapshot\b', '快照'),
    (r'\bsnapshot\b', '快照'),
    (r'\bTemplate\b', '模板'),
    (r'\btemplate\b', '模板'),
    (r'\bPolicy\b', '策略'),
    (r'\bpolicy\b', '策略'),
    (r'\bGroup\b', '组'),
    (r'\bgroup\b', '组'),
    (r'\bAccount\b', '帐户'),
    (r'\baccount\b', '帐户'),
    (r'\bSession\b', '会话'),
    (r'\bsession\b', '会话'),
    (r'\bMessage\b', '消息'),
    (r'\bmessage\b', '消息'),
    (r'\bLog\b', '日志'),
    (r'\blog\b', '日志'),
    (r'\bImage\b', '映像'),
    (r'\bimage\b', '映像'),
    (r'\bRole\b', '角色'),
    (r'\brole\b', '角色'),
    (r'\bPermission\b', '权限'),
    (r'\bpermission\b', '权限'),
    (r'\bPrivilege\b', '特权'),
    (r'\bprivilege\b', '特权'),
    (r'\bProperty\b', '属性'),
    (r'\bproperty\b', '属性'),
    (r'\bObject\b', '对象'),
    (r'\bobject\b', '对象'),
    (r'\bTask\b', '任务'),
    (r'\btask\b', '任务'),
    (r'\bProcess\b', '进程'),
    (r'\bprocess\b', '进程'),
    (r'\bApplication\b', '应用程序'),
    (r'\bapplication\b', '应用程序'),
    (r'\bApp\b', '应用'),
    (r'\bInterface\b', '接口'),
    (r'\binterface\b', '接口'),
    (r'\bMode\b', '模式'),
    (r'\bmode\b', '模式'),
    (r'\bLevel\b', '级别'),
    (r'\blevel\b', '级别'),
    (r'\bPath\b', '路径'),
    (r'\bpath\b', '路径'),
    (r'\bLabel\b', '标签'),
    (r'\blabel\b', '标签'),
    (r'\bKey\b', '键'),
    (r'\bkey\b', '键'),
    (r'\bRule\b', '规则'),
    (r'\brule\b', '规则'),
    (r'\bSource\b', '源'),
    (r'\bsource\b', '源'),
    (r'\bTarget\b', '目标'),
    (r'\btarget\b', '目标'),
    (r'\bDestination\b', '目标'),
    (r'\bdestination\b', '目标'),
    (r'\bOriginal\b', '原始'),
    (r'\boriginal\b', '原始'),
    (r'\bPhysical\b', '物理'),
    (r'\bphysical\b', '物理'),
    (r'\bLogical\b', '逻辑'),
    (r'\blogical\b', '逻辑'),
    (r'\bExternal\b', '外部'),
    (r'\bexternal\b', '外部'),
    (r'\bInternal\b', '内部'),
    (r'\binternal\b', '内部'),
    (r'\bLocal\b', '本地'),
    (r'\blocal\b', '本地'),
    (r'\bRemote\b', '远程'),
    (r'\bremote\b', '远程'),
    (r'\bActive\b', '活动'),
    (r'\bactive\b', '活动'),
    (r'\bPrimary\b', '主'),
    (r'\bprimary\b', '主'),
    (r'\bSecondary\b', '辅助'),
    (r'\bsecondary\b', '辅助'),
    (r'\bTotal\b', '总计'),
    (r'\btotal\b', '总计'),
    (r'\bAverage\b', '平均值'),
    (r'\baverage\b', '平均值'),
    (r'\bMaximum\b', '最大值'),
    (r'\bmaximum\b', '最大值'),
    (r'\bMinimum\b', '最小值'),
    (r'\bminimum\b', '最小值'),
    (r'\bUsage\b', '使用率'),
    (r'\busage\b', '使用率'),
    (r'\bCapacity\b', '容量'),
    (r'\bcapacity\b', '容量'),
    (r'\bBandwidth\b', '带宽'),
    (r'\bbandwidth\b', '带宽'),
    (r'\bLatency\b', '延迟'),
    (r'\blatency\b', '延迟'),
    (r'\bThroughput\b', '吞吐量'),
    (r'\bthroughput\b', '吞吐量'),
    (r'\bHealth\b', '运行状况'),
    (r'\bhealth\b', '运行状况'),
    (r'\bFault\b', '故障'),
    (r'\bfault\b', '故障'),
    (r'\bTolerance\b', '容错'),
    (r'\btolerance\b', '容错'),
    (r'\bFailover\b', '故障切换'),
    (r'\bfailover\b', '故障切换'),
    (r'\bStandby\b', '待机'),
    (r'\bstandby\b', '待机'),
    (r'\bMaintenance\b', '维护'),
    (r'\bmaintenance\b', '维护'),
    (r'\bProvisioning\b', '置备'),
    (r'\bprovisioning\b', '置备'),
    (r'\bAllocation\b', '分配'),
    (r'\ballocation\b', '分配'),
    (r'\bReservation\b', '预留'),
    (r'\breservation\b', '预留'),
    (r'\bThreshold\b', '阈值'),
    (r'\bthreshold\b', '阈值'),
    (r'\bNotification\b', '通知'),
    (r'\bnotification\b', '通知'),
    (r'\bResponse\b', '响应'),
    (r'\bresponse\b', '响应'),
    (r'\bRequest\b', '请求'),
    (r'\brequest\b', '请求'),
    (r'\bCompliance\b', '合规'),
    (r'\bcompliance\b', '合规'),
    (r'\bVerification\b', '验证'),
    (r'\bverification\b', '验证'),
    (r'\bAuthentication\b', '身份验证'),
    (r'\bauthentication\b', '身份验证'),
    (r'\bAuthorization\b', '授权'),
    (r'\bauthorization\b', '授权'),
    (r'\bAccess\b', '访问'),
    (r'\baccess\b', '访问'),
    (r'\bSecurity\b', '安全'),
    (r'\bsecurity\b', '安全'),
    (r'\bTrust\b', '信任'),
    (r'\btrust\b', '信任'),
    (r'\bRecovery\b', '恢复'),
    (r'\brecovery\b', '恢复'),
    (r'\bRedundancy\b', '冗余'),
    (r'\bredundancy\b', '冗余'),
    (r'\bIntegration\b', '集成'),
    (r'\bintegration\b', '集成'),
    (r'\bSolution\b', '解决方案'),
    (r'\bsolution\b', '解决方案'),
    (r'\bExtension\b', '扩展'),
    (r'\bextension\b', '扩展'),
    (r'\bProfile\b', '配置文件'),
    (r'\bprofile\b', '配置文件'),
    (r'\bComponent\b', '组件'),
    (r'\bcomponent\b', '组件'),
    (r'\bModule\b', '模块'),
    (r'\bmodule\b', '模块'),
    (r'\bPlugin\b', '插件'),
    (r'\bplugins\b', '插件'),
    (r'\bAdapter\b', '适配器'),
    (r'\badapter\b', '适配器'),
    (r'\bController\b', '控制器'),
    (r'\bcontroller\b', '控制器'),
    (r'\bSensor\b', '传感器'),
    (r'\bsensor\b', '传感器'),
    (r'\bProcessor\b', '处理器'),
    (r'\bprocessor\b', '处理器'),
    (r'\bVolume\b', '卷'),
    (r'\bvolume\b', '卷'),
    (r'\bPartition\b', '分区'),
    (r'\bpartition\b', '分区'),
    (r'\bSignature\b', '签名'),
    (r'\bsignature\b', '签名'),
    (r'\bInsufficient\b', '不足'),
    (r'\binsufficient\b', '不足'),
    (r'\bInvalid\b', '无效'),
    (r'\binvalid\b', '无效'),
    (r'\bUnknown\b', '未知'),
    (r'\bunknown\b', '未知'),
    (r'\bNormal\b', '正常'),
    (r'\bnormal\b', '正常'),
    (r'\bCritical\b', '严重'),
    (r'\bcritical\b', '严重'),
    (r'\bPending\b', '待定'),
    (r'\bpending\b', '待定'),
    (r'\bDiscovered\b', '已发现'),
    (r'\bdiscovered\b', '已发现'),
    (r'\bProvide\b', '提供'),
    (r'\bprovide\b', '提供'),
    (r'\bSelect\b', '选择'),
    (r'\bselect\b', '选择'),
    (r'\bAllow\b', '允许'),
    (r'\ballow\b', '允许'),
    (r'\bNotify\b', '通知'),
    (r'\bnotify\b', '通知'),
    (r'\bDetect\b', '检测'),
    (r'\bdetect\b', '检测'),
    (r'\bPerform\b', '执行'),
    (r'\bperform\b', '执行'),
]


def has_mixed_content(text):
    """Check if text has both Chinese characters and English words."""
    if not text:
        return False
    has_cn = bool(re.search(r'[\u4e00-\u9fff]', text))
    has_en_word = bool(re.search(r'\b[a-zA-Z]{3,}\b', text))
    return has_cn and has_en_word


def is_mostly_english(text):
    """Check if text is mostly English with just a few Chinese words."""
    if not text:
        return False
    cn_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    en_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    total_words = cn_chars + en_words
    if total_words == 0:
        return True
    return en_words / total_words > 0.6


def fix_translation(key, zh_cn):
    """Fix a single zh_CN translation string."""
    if not zh_cn or zh_cn.strip() == '':
        return zh_cn
    
    # Skip signature markers
    if key == 'signature':
        return zh_cn
    
    # Skip purely Chinese or purely English text (no mixed content)
    if not has_mixed_content(zh_cn):
        return zh_cn
    
    text = zh_cn
    
    # Protect URLs and placeholders
    text, placeholders = protect(text)
    
    # Apply typo fixes
    for pattern, replacement in TYPO_FIXES:
        text = re.sub(pattern, replacement, text)
    
    # Apply plural fixes
    for pattern, replacement in PLURAL_FIXES:
        text = re.sub(pattern, replacement, text)
    
    # Apply term replacements
    for pattern, replacement in REPLACE_PATTERNS:
        text = re.sub(pattern, replacement, text)
    
    # If text is still mostly English, also clean up filler words
    if is_mostly_english(text):
        for pattern, replacement in ENGLISH_FILLERS:
            text = re.sub(pattern, replacement, text)
    
    # Clean up: remove double spaces, trim
    text = re.sub(r'  +', ' ', text)
    # Remove leading/trailing spaces and punctuation artifacts
    text = re.sub(r'^[\s,;.]+', '', text)
    text = re.sub(r'[\s,;.]+$', '', text)
    # Fix remaining "的 的" → "的"
    text = re.sub(r'的\s+的', '的', text)
    # Clean triples
    text = re.sub(r'  +', ' ', text)
    
    # Restore protected patterns
    text = unprotect(text, placeholders)
    
    # Final cleanup
    text = re.sub(r'  +', ' ', text)
    text = text.strip()
    
    return text


def progress_bar(current, total, bar_len=40):
    """Print a simple progress bar."""
    filled = int(bar_len * current / total)
    bar = '█' * filled + '░' * (bar_len - filled)
    pct = current * 100 / total
    sys.stdout.write(f'\r  [{bar}] {pct:5.1f}% ({current}/{total})')
    sys.stdout.flush()

def main():
    rows_fixed = 0
    total_rows = 0
    hybrid_count = 0
    
    # Phase 1: count lines
    print("正在统计行数...", end='', flush=True)
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as infile:
        for _ in infile:
            total_rows += 1
    total_rows -= 1  # exclude header
    print(f" {total_rows} 行")
    
    # Phase 2: process with progress bar
    print("正在修复翻译...")
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        try:
            zh_cn_idx = header.index('zh_CN')
        except ValueError:
            print("ERROR: Could not find 'zh_CN' column in header")
            return
        
        rows = [header]
        start_time = time.time()
        
        for i, row in enumerate(reader, 1):
            if len(row) > zh_cn_idx:
                original = row[zh_cn_idx]
                key = row[0] if len(row) > 0 else ''
                if has_mixed_content(original):
                    hybrid_count += 1
                fixed = fix_translation(key, original)
                if fixed != original:
                    row[zh_cn_idx] = fixed
                    rows_fixed += 1
            rows.append(row)
            
            # Update progress every 100 rows
            if i % 100 == 0 or i == total_rows:
                progress_bar(i, total_rows)
    
    elapsed = time.time() - start_time
    print(f"\n正在写入输出文件...", end='', flush=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    
    print(" 完成!")
    print(f"\n{'='*50}")
    print(f"  总计行数:       {total_rows}")
    print(f"  混合内容行数:   {hybrid_count}")
    print(f"  已修复行数:     {rows_fixed}")
    print(f"  耗时:           {elapsed:.1f} 秒")
    print(f"  输出文件:       {OUTPUT_FILE}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()
