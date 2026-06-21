# VMware vSphere 中文(简体)本地化翻译项目

> VMware vSphere / vCenter 国际化翻译 (i18n) 项目 — 日语翻译为简体中文

## 📋 项目概述

本项目旨在将 VMware vSphere 套件（包括 OVF Tool、vCenter Server 等组件）的日语（`ja`）语言资源文件翻译为简体中文（`zh-CN`）。项目包含翻译脚本、质量检查工具、翻译词典以及已翻译的语言资源文件。

### 核心目标

- 将 VMware 日语 `.vmsg` 本地化文件翻译为简体中文
- 提供翻译修复、质量检测和状态检查工具
- 维护日语→中文翻译词典，提高翻译一致性
- 支持 OVF Tool 和 vSphere 两大组件的本地化

## 📁 目录结构

```
├── README.md                       # 本文件
├── dict_ja2cn.csv                  # 日语→中文翻译词典
├── messages/                       # vSphere 消息本地化文件
│   ├── reference/                  # 参考文件（原始日文等多语言文件）
│   │   ├── vmware-ja.vmsg          # 日文版 vSphere 消息
│   │   ├── vmware-es.vmsg          # 西班牙文版（参考）
│   │   ├── vmware-fr.vmsg          # 法文版（参考）
│   │   ├── vmui-ja.dll             # vSphere UI 日文资源
│   │   └── vmappsdk-ja.dll         # vSphere SDK 日文资源
│   └── zh-CN/
│       └── vmware.vmsg             # ✅ 已翻译的简体中文 vSphere 消息文件
├── OVFTool/                        # OVF Tool 本地化
│   └── env/
│       ├── en/                     # OVF Tool 英文原文（参考）
│       ├── zh-CN/                  # ✅ 已翻译的 OVF Tool 中文文件
│       │   ├── action.vmsg         # 操作相关消息
│       │   ├── alarm.vmsg          # 告警消息
│       │   ├── auth.vmsg           # 认证消息
│       │   ├── cluster.vmsg        # 集群消息
│       │   ├── default.vmsg        # 默认消息
│       │   ├── enum.vmsg           # 枚举值
│       │   ├── evc.vmsg            # EVC (Enhanced vMotion Compatibility)
│       │   ├── event.vmsg          # 事件消息
│       │   ├── eventaux.vmsg       # 辅助事件消息
│       │   ├── fault.vmsg          # 故障消息
│       │   ├── gos.vmsg            # Guest OS 消息
│       │   ├── host.vmsg           # 主机消息
│       │   ├── locmsg.vmsg         # 本地化消息
│       │   ├── option.vmsg         # 选项消息
│       │   ├── ovftool.vmsg        # OVF Tool 主消息
│       │   ├── ovftool-warning.vmsg # OVF Tool 警告
│       │   ├── perf.vmsg           # 性能消息
│       │   ├── question.vmsg       # 问题/提示消息
│       │   ├── stask.vmsg          # 计划任务消息
│       │   ├── task.vmsg           # 任务消息
│       │   └── vm.vmsg             # 虚拟机消息
│       └── *.vlcl                  # OVF Tool 区域设置配置
├── .backup/                        # 自动备份目录
└── *.py                            # 翻译与工具脚本（详见下方）
```

## 🔧 工具脚本说明

### 翻译脚本

| 脚本 | 功能 |
|------|------|
| `translate_eventaux_v5.py` | 翻译 `eventaux.vmsg` 事件辅助消息文件 |
| `translate_ovftool_v2.py` | 翻译 OVF Tool 相关 `.vmsg` 文件 |

### 翻译修复脚本

| 脚本 | 功能 |
|------|------|
| `fix_locmsg.py` | 修复 `locmsg.vmsg` 中的翻译问题 |
| `fix_locmsg_v2.py` | 修复 `locmsg.vmsg` v2 版本 |
| `fix_locmsg_v3.py` | 修复 `locmsg.vmsg` v3 版本 |
| `fix_locmsg_v4.py` | 修复 `locmsg.vmsg` v4 版本 |
| `fix_enum_batch.py` | 批量修复枚举值翻译 |
| `fix_enum_batch2.py` | 批量修复枚举值 v2 |
| `fix_enum_batch3.py` | 批量修复枚举值 v3 |
| `fix_option_phase2.py` | 修复 `option.vmsg` 第二阶段 |
| `fix_option_phase3.py` | 修复 `option.vmsg` 第三阶段 |
| `fix_option_vmsg.py` | 修复 `option.vmsg` 翻译 |
| `fix_question_vmsg.py` | 修复 `question.vmsg` 翻译 |
| `fix_stask_vmsg.py` | 修复 `stask.vmsg` 翻译 |
| `fix_task_vmsg_v2.py` | 修复 `task.vmsg` v2 |
| `fix_task_vmsg_v3_patch.py` | 修复 `task.vmsg` v3 补丁 |
| `fix_vm_vmsg_v3.py` | 修复 `vm.vmsg` v3 |
| `fix_small.py` | 小规模修复工具 |
| `patch_eventaux.py` | 修补 `eventaux.vmsg` |

### 质量检测与调试脚本

| 脚本 | 功能 |
|------|------|
| `check_fix.py` | 检查翻译修复效果，统计中文覆盖率 |
| `check_status.py` | 检查所有 zh-CN 翻译文件的状态、键值完整度 |
| `quick_verify.py` | 快速验证翻译文件完整性 |
| `debug_locmsg.py` | 调试 `locmsg.vmsg` 翻译问题 |
| `debug_locmsg2.py` | 调试 `locmsg.vmsg` v2 |

## 📖 翻译流程

1. **词典驱动翻译**：使用 `dict_ja2cn.csv` 日语→中文词典进行子串匹配翻译
2. **增量修复**：通过多个版本的修复脚本迭代改进翻译质量
3. **质量检查**：使用检查脚本评估翻译覆盖率（统计中文字符占比）
4. **备份恢复**：`.backup/` 目录自动备份每次操作前的文件状态

### 翻译词典格式

```csv
# 日语→中文 翻译词典
# 格式: 日文原文,中文翻译
キャンセル,取消
続行,继续
再試行,重试
接続,连接
```

> ⚠️ 注意：长匹配/精确匹配词条应放在前面，替换基于子串匹配。

## ✅ 质量指标

检查脚本会从以下维度评估翻译质量：

- **键值完整度**：中英文文件的消息键数量对比
- **中文覆盖率**：值文本中中文字符占比
- **常见问题检测**：如残留日语假名、未翻译的英文术语等

## 🚀 使用方式

```bash
# 检查翻译状态
python3 check_status.py

# 运行翻译修复
python3 fix_locmsg_v4.py

# 快速验证
python3 quick_verify.py
```

## 📄 文件格式说明

`.vmsg` 文件是 VMware 自定义的消息资源文件格式，包含：

- `label` 和 `summary` 键值对：定义 UI 元素的显示文本和摘要
- `sig` 签名行：用于完整性校验
- `###` 注释行

示例：
```
AgentManager.add.label = "添加代理管理器"
AgentManager.add.summary = "向 vCenter Server 添加新的代理管理器"
```

## 🤝 贡献

欢迎通过 Issue 或 Pull Request 提交翻译改进建议！

## 📜 许可

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

> **注意**：项目中的 `.vmsg` 翻译文件是 VMware  copyrighted 作品的衍生翻译，使用时请遵守 VMware 相应的许可条款。