#!/usr/bin/env python3
"""
Fix Chinese translations in key_en_ja_cn.csv.

Replaces common English words/phrases left untranslated in the zh_CN column.
"""

import csv
import re
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "key_en_ja_cn.csv")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "key_en_ja_cn_fixed.csv")

# ─── Terminology replacements ────────────────────────────────────────
# Ordered by length (longer first) to avoid partial replacements

TERM_MAP = {
    # VMware specific terms that should stay - do NOT touch
    # vMotion, DRS, vSAN, vSphere, vCenter, ESXi, ESX, vApps, vApp, etc

    # High-frequency replacements - labels/summaries
    r'\ba\b': '',
    r'\ban\b': '',
    r'\bthe\b': '',
    r'\bthis\b': '',
    r'\bthat\b': '',
    r'\bThese\b': '',
    r'\bthese\b': '',
    r'\bis\b': '',
    r'\bare\b': '',
    r'\bhas\b': '',
    r'\bhave\b': '',
    r'\bbeen\b': '',
    r'\bwas\b': '',
    r'\bwere\b': '',
    r'\bwill\b': '',
    r'\bbe\b': '',
    r'\bfor\b': '',
    r'\bwith\b': '',
    r'\bfrom\b': '',
    r'\bby\b': '',
    r'\bto\b': '',
    r'\bor\b': '',
    r'\bin\b': '',
    r'\bon\b': '',
    r'\bat\b': '',
    r'\bas\b': '',
    r'\bof\b': '',
}

# Word-level replacements (case-insensitive in context)
# These are for mixed-language strings where English words appear in Chinese context
WORD_REPLACEMENTS = [
    # Technology terms (lowercase & capitalized variants)
    (r'\b(?:Host|host)\b', '主机'),
    (r'\b(?:Server|server)\b', '服务器'),
    (r'\b(?:Cluster|cluster)\b', '集群'),
    (r'\b(?:Datacenter|datacenter)\b', '数据中心'),
    (r'\b(?:Datastore|datastore)\b', '数据存储'),
    (r'\b(?:Virtual\s+machine|virtual\s+machine|VM|vm)\b', '虚拟机'),
    (r'\b(?:Virtual\s+disk|virtual\s+disk)\b', '虚拟磁盘'),
    (r'\b(?:Network|network)\b', '网络'),
    (r'\b(?:Storage|storage)\b', '存储'),
    (r'\b(?:Memory|memory|RAM)\b', '内存'),
    (r'\b(?:Disk|disk)\b', '磁盘'),
    (r'\b(?:CPU|cpu)\b', 'CPU'),
    (r'\b(?:Status|status)\b', '状态'),
    (r'\b(?:State|state)\b', '状态'),
    (r'\b(?:Power|power)\b', '电源'),
    (r'\b(?:Device|device)\b', '设备'),
    (r'\b(?:Driver|driver)\b', '驱动程序'),
    (r'\b(?:Port|port)\b', '端口'),
    (r'\b(?:Protocol|protocol)\b', '协议'),
    (r'\b(?:Resource|resource)\b', '资源'),
    (r'\b(?:Service|service)\b', '服务'),
    (r'\b(?:License|license)\b', '许可证'),
    (r'\b(?:User|user)\b', '用户'),
    (r'\b(?:Password|password)\b', '密码'),
    (r'\b(?:Certificate|certificate)\b', '证书'),
    (r'\b(?:Agent|agent)\b', '代理'),
    (r'\b(?:Client|client)\b', '客户端'),
    (r'\b(?:Console|console)\b', '控制台'),
    (r'\b(?:Folder|folder)\b', '文件夹'),
    (r'\b(?:File|file)\b', '文件'),
    (r'\b(?:Directory|directory)\b', '目录'),
    (r'\b(?:Database|database|DB|db)\b', '数据库'),
    (r'\b(?:Version|version)\b', '版本'),
    (r'\b(?:Configuration|configuration|Config|config)\b', '配置'),
    (r'\b(?:Operation|operation)\b', '操作'),
    (r'\b(?:Action|action)\b', '操作'),
    (r'\b(?:Event|event)\b', '事件'),
    (r'\b(?:Alarm|alarm)\b', '警报'),
    (r'\b(?:Warning|warning)\b', '警告'),
    (r'\b(?:Error|error)\b', '错误'),
    (r'\b(?:Failure|failure)\b', '失败'),
    (r'\b(?:Success|success)\b', '成功'),
    (r'\b(?:Enabled?|enabled?)\b', '已启用'),
    (r'\b(?:Disabled?|disabled?)\b', '已禁用'),
    (r'\b(?:Connected|connected)\b', '已连接'),
    (r'\b(?:Disconnected|disconnected)\b', '已断开连接'),
    (r'\b(?:Configured|configured)\b', '已配置'),
    (r'\b(?:Installed|installed)\b', '已安装'),
    (r'\b(?:Failed|failed)\b', '失败'),
    (r'\b(?:Updated|updated)\b', '已更新'),
    (r'\b(?:Changed|changed)\b', '已更改'),
    (r'\b(?:Removed|removed)\b', '已移除'),
    (r'\b(?:Created|created)\b', '已创建'),
    (r'\b(?:Registered|registered)\b', '已注册'),
    (r'\b(?:Unregistered|unregistered)\b', '已注销'),
    (r'\b(?:Upgrade|upgrade)\b', '升级'),
    (r'\b(?:Install|install)\b', '安装'),
    (r'\b(?:Update|update)\b', '更新'),
    (r'\b(?:Delete|delete|Remove|remove)\b', '删除'),
    (r'\b(?:Create|create)\b', '创建'),
    (r'\b(?:Migrate|migrate|Migration|migration)\b', '迁移'),
    (r'\b(?:Replicate|replicate|Replication|replication)\b', '复制'),
    (r'\b(?:Encrypt|encrypt|Encryption|encryption)\b', '加密'),
    (r'\b(?:Monitor|monitor|Monitoring|monitoring)\b', '监控'),
    (r'\b(?:Manager|manager)\b', '管理器'),
    (r'\b(?:Management|management)\b', '管理'),
    (r'\b(?:Default|default)\b', '默认'),
    (r'\b(?:Current|current)\b(?!\s*value)', '当前'),
    (r'\b(?:Value|value)\b', '值'),
    (r'\b(?:Name|name)\b', '名称'),
    (r'\b(?:Type|type)\b', '类型'),
    (r'\b(?:ID|Id|id)\b', 'ID'),
    (r'\b(?:Number|number|Count|count)\b', '数量'),
    (r'\b(?:Supported?|supported?)\b', '支持'),
    (r'\b(?:Available?|available?)\b', '可用'),
    (r'\b(?:Timeout|timeout)\b', '超时'),
    (r'\b(?:Backup|backup)\b', '备份'),
    (r'\b(?:Restore|restore)\b', '恢复'),
    (r'\b(?:Snapshot|snapshot)\b', '快照'),
    (r'\b(?:Template|template)\b', '模板'),
    (r'\b(?:Policy|policy)\b', '策略'),
    (r'\b(?:Group|group)\b', '组'),
    (r'\b(?:Account|account)\b', '帐户'),
    (r'\b(?:Session|session)\b', '会话'),
    (r'\b(?:Message|message)\b', '消息'),
    (r'\b(?:Log|log)\b', '日志'),
    (r'\b(?:Image|image)\b', '映像'),
    (r'\b(?:Role|role)\b', '角色'),
    (r'\b(?:Permission|permission)\b', '权限'),
    (r'\b(?:Privilege|privilege)\b', '特权'),
    (r'\b(?:Property|property)\b', '属性'),
    (r'\b(?:Attribute|attribute)\b', '属性'),
    (r'\b(?:Object|object)\b', '对象'),
    (r'\b(?:Task|task)\b', '任务'),
    (r'\b(?:Process|process)\b', '进程'),
    (r'\b(?:Application|application|App|app)\b', '应用程序'),
    (r'\b(?:Interface|interface)\b', '接口'),
    (r'\b(?:Mode|mode)\b', '模式'),
    (r'\b(?:Level|level)\b', '级别'),
    (r'\b(?:Path|path)\b', '路径'),
    (r'\b(?:Label|label)\b', '标签'),
    (r'\b(?:Key|key)\b', '键'),
    (r'\b(?:Rule|rule)\b', '规则'),
    (r'\b(?:Parent|parent)\b', '父项'),
    (r'\b(?:Child|child)\b', '子项'),
    (r'\b(?:Source|source)\b', '源'),
    (r'\b(?:Target|target)\b', '目标'),
    (r'\b(?:Destination|destination)\b', '目标'),
    (r'\b(?:Original|original)\b', '原始'),
    (r'\b(?:Physical|physical)\b', '物理'),
    (r'\b(?:Logical|logical)\b', '逻辑'),
    (r'\b(?:External|external)\b', '外部'),
    (r'\b(?:Internal|internal)\b', '内部'),
    (r'\b(?:Local|local)\b', '本地'),
    (r'\b(?:Remote|remote)\b', '远程'),
    (r'\b(?:Active|active)\b', '活动'),
    (r'\b(?:Inactive|inactive)\b', '非活动'),
    (r'\b(?:Primary|primary)\b', '主'),
    (r'\b(?:Secondary|secondary)\b', '辅助'),
    (r'\b(?:Total|total)\b', '总计'),
    (r'\b(?:Average|average|Avg|avg)\b', '平均'),
    (r'\b(?:Maximum|maximum|Max|max)\b', '最大'),
    (r'\b(?:Minimum|minimum|Min|min)\b', '最小'),
    (r'\b(?:Usage|usage)\b', '使用率'),
    (r'\b(?:Utilization|utilization)\b', '利用率'),
    (r'\b(?:Capacity|capacity)\b', '容量'),
    (r'\b(?:Bandwidth|bandwidth)\b', '带宽'),
    (r'\b(?:Latency|latency)\b', '延迟'),
    (r'\b(?:Throughput|throughput)\b', '吞吐量'),
    (r'\b(?:Health|health)\b', '运行状况'),
    (r'\b(?:Fault|fault)\b', '故障'),
    (r'\b(?:Tolerance|tolerance)\b', '容错'),
    (r'\b(?:Failover|failover)\b', '故障切换'),
    (r'\b(?:Standby|standby)\b', '待机'),
    (r'\b(?:Maintenance|maintenance)\b', '维护'),
    (r'\b(?:Provisioning|provisioning)\b', '置备'),
    (r'\b(?:Allocation|allocation)\b', '分配'),
    (r'\b(?:Reservation|reservation)\b', '预留'),
    (r'\b(?:Threshold|threshold)\b', '阈值'),
    (r'\b(?:Notification|notification)\b', '通知'),
    (r'\b(?:Response|response)\b', '响应'),
    (r'\b(?:Request|request)\b', '请求'),
    (r'\b(?:Discovery|discovery)\b', '发现'),
    (r'\b(?:Compliance|compliance)\b', '合规'),
    (r'\b(?:Verification|verification|Verify|verify)\b', '验证'),
    (r'\b(?:Authentication|authentication)\b', '身份验证'),
    (r'\b(?:Authorization|authorization)\b', '授权'),
    (r'\b(?:Access|access)\b', '访问'),
    (r'\b(?:Security|security)\b', '安全'),
    (r'\b(?:Trust|trust)\b', '信任'),
    (r'\b(?:Recovery|recovery)\b', '恢复'),
    (r'\b(?:Redundancy|redundancy)\b', '冗余'),
    (r'\b(?:Integration|integration)\b', '集成'),
    (r'\b(?:Solution|solution)\b', '解决方案'),
    (r'\b(?:Extension|extension)\b', '扩展'),
    (r'\b(?:Profile|profile)\b', '配置文件'),
    (r'\b(?:Component|component)\b', '组件'),
    (r'\b(?:Module|module)\b', '模块'),
    (r'\b(?:Plugin|plugin)\b', '插件'),
    (r'\b(?:Adapter|adapter)\b', '适配器'),
    (r'\b(?:(?:Controller|controller))\b', '控制器'),
    (r'\b(?:Sensor|sensor)\b', '传感器'),
    (r'\b(?:Processor|processor)\b', '处理器'),
    (r'\b(?:Volume|volume)\b', '卷'),
    (r'\b(?:Partition|partition)\b', '分区'),
    (r'\b(?:Signature|signature)\b', '签名'),
    (r'\b(?:Insufficient|insufficient)\b', '不足'),
    (r'\b(?:Invalid|invalid)\b', '无效'),
    (r'\b(?:Unknown|unknown)\b', '未知'),
    (r'\b(?:Normal|normal)\b', '正常'),
    (r'\b(?:Critical|critical)\b', '严重'),
    (r'\b(?:Pending|pending)\b', '待定'),

    # Verbs and verb phrases in mixed context
    (r'\b(?:to\s+)?monitor\b', '监控'),
    (r'\b(?:to\s+)?indicate\b', '指示'),
    (r'\btriggered\b', '触发'),
    (r'\bnotify\b', '通知'),
    (r'\bdetected\b', '检测到'),
    (r'\bexceeded\b', '超出'),
    (r'\busing\b', '使用'),
    (r'\bbased\s+on\b', '基于'),
    (r'\bdue\s+to\b', '由于'),
    (r'\baccording\s+to\b', '根据'),

    # Common summary patterns
    (r'Default alarm to monitor', '默认警报：监控'),
    (r'Default alarm that monitors', '默认警报：监控'),
    (r'Default alarm that is triggered', '默认警报：触发'),
    (r'Default alarm for', '默认警报：'),
    (r'Default alarm to alert', '默认警报：'),
    (r'Alarm to indicate', '警报：指示'),
    (r'Alarm to notify', '警报：通知'),
    (r'Alarm to monitor', '警报：监控'),
    (r'Alarm that monitors', '警报：监控'),
    (r'Alarm that indicates', '警报：指示'),
    (r'is triggered', '触发'),
    (r'is used', '用于'),
    (r'is equal to', '等于'),
    (r'is about to', '即将'),
    (r'has been', '已'),
    (r'have been', '已'),
    (r'not been', '未'),
    (r'cannot be', '无法'),
    (r'Configure', '配置'),
    (r'Manage', '管理'),
    (r'Please', '请'),
    (r'See the', '请参阅'),
    (r'for more details', '以了解详细信息'),
    (r'for details', '以了解详细信息'),
    (r'follow', '按照'),
    (r'following', '以下'),
    (r'refer to', '请参阅'),
    (r'Refer ', '请参阅'),
    (r'Please address', '请处理'),
    (r'by following', '按照'),
    (r'provided in', '参见'),
]

# Complex phrase patterns that need specific handling
PHRASE_FIXES = [
    # "Failed to X" → "X 失败"
    (r'失败 to (\S+)', r'\1 失败'),
    # "the Xs" → "X" (English plural on Chinese words)
    (r'证书s', '证书'),
    (r'警报s', '警报'),
    (r'状态s', '状态'),
    (r'值s', '值'),
    (r'事件s', '事件'),
    (r'错误s', '错误'),
    (r'任务s', '任务'),
    (r'连接s', '连接'),
    (r'资源s', '资源'),
    (r'服务s', '服务'),
    (r'设备s', '设备'),
    (r'对象s', '对象'),
    (r'文件s', '文件'),
    (r'用户s', '用户'),
    (r'接口s', '接口'),
    (r'组件s', '组件'),
    (r'属性s', '属性'),
    (r'角色s', '角色'),
    (r'策略s', '策略'),
    (r'代理s', '代理'),
    (r'扩展s', '扩展'),
    (r'分区s', '分区'),
    (r'适配器s', '适配器'),
    (r'控制器s', '控制器'),
    (r'处理器s', '处理器'),
    (r'传感器s', '传感器'),
    (r'数据存储s', '数据存储'),
    (r'虚拟机s', '虚拟机'),
    (r'数据中心s', '数据中心'),
    (r'文件夹s', '文件夹'),
    (r'选项卡s', '选项卡'),
    (r'许可证s', '许可证'),
    (r'间隔s', '间隔'),
    (r'端口s', '端口'),
    (r'网络s', '网络'),
    (r'磁盘s', '磁盘'),
    (r'主机s', '主机'),
    (r'服务器s', '服务器'),
    (r'客户端s', '客户端'),
    (r'卷s', '卷'),
    (r'描述s', '描述'),
    (r'配置s', '配置'),
    (r'操作s', '操作'),
    (r'权限s', '权限'),
    (r'特权s', '特权'),
    (r'密钥s', '密钥'),
    (r'键s', '键'),
    (r'模块s', '模块'),
    (r'池s', '池'),
    (r'名称空间s', '名称空间'),

    # "in the X" → "在 X 中"
    # Already mostly handled

    # "的 Xs" → "的 X" (fix remaining plurals)
    (r'的(\w+)s\b', r'的\1'),

    # Fix duplicate spaces
    (r'  +', ' '),

    # Fix "电流" → "当前" when it means "current" (not electrical)
    (r'电流', '当前'),

    # Fix "连接ion" typo
    (r'连接ion', '连接'),

    # Fix "已用" misused for "used"
    (r'\b已用\b', '用于'),

    # Fix "基于d" 
    (r'基于d', '基于'),
    (r'定义d', '定义'),
    (r'限制d', '限制'),
    (r'启用d', '启用'),
    (r'禁用d', '禁用'),
    (r'配置d', '配置'),
    (r'安装d', '安装'),
    (r'分配d', '分配'),
    (r'注册d', '注册'),

    # Fix "的 的" pattern
    (r'的 的', '的'),

    # Fix "——" → "，" in summaries (dash used as comma)
    (r'警报 —— triggered', '警报 triggered'),

    # Fix "provIDEr" → "provider"
    (r'provIDEr', '提供程序'),
    (r'provIDErs', '提供程序'),
    (r'IDEntity', '标识'),
    (r'添加ress', '处理'),

    # Fix "电源 on" / "电源 off"
    (r'电源 on\b', '打开电源'),
    (r'电源 off\b', '关闭电源'),
    (r'电源ed on\b', '已开机'),
    (r'电源ed off\b', '已关机'),

    # Fix "已用 by" → "由...使用"
    (r'已用 由', '由'),
    (r'已用 for', '用于'),

    # Fix "的 在" → "在...的"
    # Hard to do automatically

    # Fix "current value" context - keep "电流" for "electrical current"
    # But in most contexts it's wrong. Let me be more specific.
    # Actually let me revert: in "CurrentValue.label" the 电流 might be wrong
    # But the key has "Current values for metric/state" → 当前值
    # Leave "电流" as is for electrical contexts only
    
    # Fix "来 monitoring" 
    (r'\bmonitoring\b', '监控'),
    (r'\bmonitor\b', '监控'),

    # Fix timestamp-like format
    (r'已 使用', '使用'),
    (r'已 配置', '已配置'),
    (r'已 启用', '已启用'),
    (r'已 禁用', '已禁用'),
    (r'已 连接', '已连接'),
    (r'已 断开连接', '已断开连接'),
    (r'已 安装', '已安装'),
    (r'已 更新', '已更新'),
    (r'已 更改', '已更改'),
    (r'已 取消', '已取消'),
    (r'已 创建', '已创建'),
    (r'已 注册', '已注册'),
    (r'已 注销', '已注销'),
    (r'已 移动', '已移动'),
    (r'已 停止', '已停止'),
    (r'已 重新启动', '已重新启动'),
    (r'不 已配置', '未配置'),
    (r'不 兼容', '不兼容'),
    (r'不 支持', '不支持'),
    (r'不 可用', '不可用'),
    (r'不 活动', '不活动'),
]

# Entries that should be left as-is (mostly labels/summaries with formatting)
SKIP_KEYS = {
    'signature',  # Signature markers
}


def fix_translation(key, zh_cn):
    """Fix a single zh_CN translation string."""
    if not zh_cn or zh_cn.strip() == '':
        return zh_cn
    
    # Skip signature markers
    if key in SKIP_KEYS:
        return zh_cn
    
    text = zh_cn
    
    # Apply phrase fixes first (more specific)
    for pattern, replacement in PHRASE_FIXES:
        text = re.sub(pattern, replacement, text)
    
    # Apply word replacements (only in contexts where Chinese already mixed)
    # Only apply if the text contains at least some Chinese characters
    has_chinese = bool(re.search(r'[\u4e00-\u9fff]', text))
    if has_chinese:
        for pattern, replacement in WORD_REPLACEMENTS:
            # Only replace in mixed-language context
            text = re.sub(pattern, replacement, text)
    
    # Clean up: remove leading/trailing spaces, fix double spaces
    text = re.sub(r'  +', ' ', text)
    text = text.strip()
    
    # Fix remaining English articles and common words that got through
    if has_chinese and re.search(r'[\u4e00-\u9fff]', text):
        # Remove standalone English articles in Chinese context
        for eng_pattern, replacement in TERM_MAP.items():
            text = re.sub(eng_pattern, replacement, text)
        text = re.sub(r'  +', ' ', text)
        text = text.strip()
    
    return text


def main():
    rows_fixed = 0
    total_rows = 0
    
    with open(INPUT_FILE, 'r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        
        # Find the zh_CN column index
        try:
            zh_cn_idx = header.index('zh_CN')
        except ValueError:
            print("ERROR: Could not find 'zh_CN' column in header")
            return
        
        rows = []
        rows.append(header)
        
        for row in reader:
            total_rows += 1
            if len(row) > zh_cn_idx:
                original = row[zh_cn_idx]
                key = row[0] if len(row) > 0 else ''
                fixed = fix_translation(key, original)
                if fixed != original:
                    row[zh_cn_idx] = fixed
                    rows_fixed += 1
            rows.append(row)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)
    
    print(f"Total rows processed: {total_rows}")
    print(f"Rows fixed: {rows_fixed}")
    print(f"Output written to: {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
