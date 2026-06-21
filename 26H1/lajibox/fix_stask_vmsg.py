"""
fix_stask_vmsg.py - 完善 stask.vmsg 翻译
对比 en 原文，修复 zh-CN 中的未翻译/半翻译项。

多会话安全: 备份 + 原子写入 + 幂等
"""
import os
import re
import shutil
import tempfile
from datetime import datetime

TARGET = os.path.join(os.path.dirname(__file__),
                      "OVFTool", "env", "zh-CN", "stask.vmsg")
BACKUP_DIR = os.path.join(os.path.dirname(__file__), ".backup")


def backup(filepath):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    bak_path = os.path.join(BACKUP_DIR, f"stask.vmsg.{ts}.bak")
    shutil.copy2(filepath, bak_path)
    print(f"[备份] -> {bak_path}")


def atomic_write(filepath, content):
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(filepath),
                               prefix=".stask_tmp_", suffix=".vmsg")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        os.replace(tmp, filepath)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def fix_translations(text):
    replacements = [
        # labels
        ('scheduler.DailyTaskScheduler.label="Daily"', 'scheduler.DailyTaskScheduler.label="每天"'),
        ('scheduler.OnceTaskScheduler.label="Once"', 'scheduler.OnceTaskScheduler.label="一次"'),
        ('scheduler.MonthlyByDayTaskScheduler.label="Monthly (by day)"', 'scheduler.MonthlyByDayTaskScheduler.label="每月（按日期）"'),
        ('scheduler.MonthlyByWeekdayTaskScheduler.label="Monthly (by weekday)"', 'scheduler.MonthlyByWeekdayTaskScheduler.label="每月（按工作日）"'),
        ('scheduler.MonthlyTaskScheduler.label="Monthly"', 'scheduler.MonthlyTaskScheduler.label="每月"'),
        ('scheduler.HourlyTaskScheduler.label="Hourly"', 'scheduler.HourlyTaskScheduler.label="每小时"'),
        ('scheduler.WeeklyTaskScheduler.label="Weekly"', 'scheduler.WeeklyTaskScheduler.label="每周"'),
        ('scheduler.AfterStartupTaskScheduler.label="After startup"', 'scheduler.AfterStartupTaskScheduler.label="启动后"'),

        # frequencies
        ('scheduler.DailyTaskScheduler.frequency="Hour"', 'scheduler.DailyTaskScheduler.frequency="小时"'),
        ('scheduler.OnceTaskScheduler.frequency="Time"', 'scheduler.OnceTaskScheduler.frequency="时间"'),
        ('scheduler.MonthlyByDayTaskScheduler.frequency="Day"', 'scheduler.MonthlyByDayTaskScheduler.frequency="日期"'),
        ('scheduler.MonthlyByWeekdayTaskScheduler.frequency="Weekday within off设置 week"', 'scheduler.MonthlyByWeekdayTaskScheduler.frequency="偏移周内的工作日"'),
        ('scheduler.MonthlyTaskScheduler.frequency="Day"', 'scheduler.MonthlyTaskScheduler.frequency="日期"'),
        ('scheduler.HourlyTaskScheduler.frequency="Minute"', 'scheduler.HourlyTaskScheduler.frequency="分钟"'),
        ('scheduler.WeeklyTaskScheduler.frequency="Weekday"', 'scheduler.WeeklyTaskScheduler.frequency="工作日"'),
        ('scheduler.AfterStartupTaskScheduler.frequency="延迟 分钟"', 'scheduler.AfterStartupTaskScheduler.frequency="延迟（分钟）"'),

        # summaries
        ('scheduler.DailyTaskScheduler.summary="Scheduled 任务 will be triggered every day at a specific hour"',
         'scheduler.DailyTaskScheduler.summary="计划任务将在每天的特定小时触发"'),
        ('scheduler.OnceTaskScheduler.summary="Scheduled 任务 will be triggered once at a specific time"',
         'scheduler.OnceTaskScheduler.summary="计划任务将在特定时间触发一次"'),
        ('scheduler.MonthlyByDayTaskScheduler.summary="Scheduled 任务 will be triggered monthly on a specific day"',
         'scheduler.MonthlyByDayTaskScheduler.summary="计划任务将在每月的特定日期触发"'),
        ('scheduler.MonthlyByWeekdayTaskScheduler.summary="Scheduled 任务 will be triggered on a specific weekday of an off设置 week 的 month"',
         'scheduler.MonthlyByWeekdayTaskScheduler.summary="计划任务将在每月的偏移周的特定工作日触发"'),
        ('scheduler.MonthlyTaskScheduler.summary="Scheduled 任务 will be triggered every month on a specific day"',
         'scheduler.MonthlyTaskScheduler.summary="计划任务将在每月的特定日期触发"'),
        ('scheduler.HourlyTaskScheduler.summary="Scheduled 任务 will be triggered at a specific minute every hour"',
         'scheduler.HourlyTaskScheduler.summary="计划任务将在每小时的特定分钟触发"'),
        ('scheduler.WeeklyTaskScheduler.summary="Scheduled 任务 will be triggered on a specific weekday every week"',
         'scheduler.WeeklyTaskScheduler.summary="计划任务将在每周的特定工作日触发"'),
        ('scheduler.AfterStartupTaskScheduler.summary="Scheduled 任务 will be triggered a specific number of 分钟 after vCenter 服务器 has 已启动"',
         'scheduler.AfterStartupTaskScheduler.summary="计划任务将在 vCenter 服务器启动后的特定分钟数触发"'),

        # email alarms
        ('Email.statefulAlarm.subject="[VMware vCenter - 警报 {alarmName}] {alarmName} 已更改 状态 from {oldStatus} to {newStatus}"',
         'Email.statefulAlarm.subject="[VMware vCenter - 警报 {alarmName}] {alarmName} 已将状态从 {oldStatus} 更改为 {newStatus}"'),
        ('Email.statefulAlarm.body="Target: {targetName}\\n上一个 状态: {oldStatus}\\nNew 状态: {newStatus}\\n\\n警报 Definition:\\n{declaringSummary}\\n\\n{alarmValue}:\\n {triggeringSummary}\\n\\n描述:\\n{eventDescription}"',
         'Email.statefulAlarm.body="目标: {targetName}\\n上一个状态: {oldStatus}\\n新状态: {newStatus}\\n\\n警报定义:\\n{declaringSummary}\\n\\n{alarmValue}:\\n {triggeringSummary}\\n\\n描述:\\n{eventDescription}"'),
        ('Email.statefulEventAlarm.body="Target: {targetName}\\n上一个 状态: {oldStatus}\\nNew 状态: {newStatus}\\n\\n警报 Definition:\\n{declaringSummary}\\n\\n{alarmValue}:\\n {eventDescription}"',
         'Email.statefulEventAlarm.body="目标: {targetName}\\n上一个状态: {oldStatus}\\n新状态: {newStatus}\\n\\n警报定义:\\n{declaringSummary}\\n\\n{alarmValue}:\\n {eventDescription}"'),
        ('Email.statelessEventAlarm.body="Target: {targetName}\\n状态less 事件 警报\\n\\n警报 Definition:\\n{declaringSummary}\\n\\n{alarmValue}:\\n{eventDescription}"',
         'Email.statelessEventAlarm.body="目标: {targetName}\\n无状态事件警报\\n\\n警报定义:\\n{declaringSummary}\\n\\n{alarmValue}:\\n{eventDescription}"'),

        # event labels
        ('event.Event.label="Event"', 'event.Event.label="事件"'),
        ('event.Date.label="Date"', 'event.Date.label="日期"'),
        ('event.Vm.label="VM"', 'event.Vm.label="虚拟机"'),
        ('event.Host.label="Host"', 'event.Host.label="主机"'),
        ('event.Datacenter.label="Data center"', 'event.Datacenter.label="数据中心"'),
        ('event.Datastore.label="Datastore"', 'event.Datastore.label="数据存储"'),
        ('event.Network.label="Network"', 'event.Network.label="网络"'),
        ('event.DVS.label="vSphere Distributed Switch"', 'event.DVS.label="vSphere 分布式交换机"'),
        ('event.Arguments.label="Arguments"', 'event.Arguments.label="参数"'),
        ('event.Summary.label="Summary"', 'event.Summary.label="摘要"'),
    ]

    for old, new in replacements:
        if old in text:
            text = text.replace(old, new)
            print(f"  [修复] {old.split('=')[0]}")
        elif new in text:
            print(f"  [跳过] {old.split('=')[0]} (已修复)")
        else:
            print(f"  [警告] 未匹配: {old.split('=')[0]}")

    return text


def main():
    if not os.path.exists(TARGET):
        print(f"[错误] 找不到: {TARGET}")
        return 1

    print("=" * 50)
    print("stask.vmsg 翻译完善 (重建运行)")
    print("=" * 50)

    backup(TARGET)

    with open(TARGET, "r", encoding="utf-8") as f:
        original = f.read()

    print("\n--- 修复项 ---")
    fixed = fix_translations(original)

    if fixed == original:
        print("\n[结果] 无需修改。")
    else:
        atomic_write(TARGET, fixed)
        count = sum(1 for o, f in zip(original.splitlines(), fixed.splitlines()) if o != f)
        print(f"\n[结果] 翻译完善完成！共 {count} 处修改。")

    return 0


if __name__ == "__main__":
    exit(main())
