# VMware 中文翻译

> VMware vSphere / vCenter 翻译项目 — 为vmware添加简体中文支持

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
│       └── zh-CN/                  # ✅ 已翻译的 OVF Tool 中文文件
└── *.py                            # 翻译与工具脚本（详见下方）
```

## 🔧 工具脚本说明

### 翻译脚本

| 脚本 | 功能 |
|------|------|
| `translate_eventaux_v5.py` | 翻译 `eventaux.vmsg` 事件辅助消息文件 |
| `translate_ovftool_v2.py` | 翻译 OVF Tool 相关 `.vmsg` 文件 |

## 🚀 使用方式

```bash
未完待续
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