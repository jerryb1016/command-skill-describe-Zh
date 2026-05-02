# command-skill-describe-zh

[English](./README.md) | 简体中文

> 天下苦学渣久矣，本人爱折腾，无奈英语水平有限，却不想被时代抛弃。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

让 CLI 斜杠命令的描述显示中文的小工具。

## 功能

- :mag: 自动扫描已安装的 Skills 和 Commands
- :earth_americas: 批量翻译 description 为中文
- :floppy_disk: 翻译前自动备份原文
- :arrows_counterclockwise: 支持回滚

## 支持的 CLI

- Claude Code
- OpenClaw
- OpenCode
- Hermes

## 安装

```bash
# 克隆仓库
git clone https://github.com/jerryb1016/command-skill-describe-zh.git

# 复制 SKILL.md 到你的 CLI skills 目录
cp SKILL.md ~/.claude/skills/describe-zh/SKILL.md
```

## 使用

```bash
/describe-zh
```

## 工作流程

1. **备份原文** - 在 `.describe-zh-backup/` 目录备份
2. **收集描述** - 扫描所有 SKILL.md 的 description 字段
3. **批量翻译** - AI 一次性翻译所有描述
4. **写入文件** - 修改 description 字段

## 回滚

如需恢复原文，从 `.describe-zh-backup/` 目录复制备份文件即可。

## License

MIT
