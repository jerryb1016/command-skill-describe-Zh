# command-skill-describe-zh

> 天下苦学渣久矣，本人爱折腾，无奈英语水平有限，却不想被时代抛弃。

将 CLI Skill/命令的 description 翻译为中文的工具。

## 功能

- 自动扫描已安装的 Skills 和 Commands
- 批量翻译 description 为中文
- 翻译前自动备份原文
- 支持回滚

## 使用方法

1. 将此 SKILL.md 安装到你的 CLI skills 目录
2. 运行 `/describe-zh`
3. 确认翻译结果

## 工作流程

1. **备份原文** - 在 `.describe-zh-backup/` 目录备份
2. **收集描述** - 扫描所有 SKILL.md 的 description 字段
3. **批量翻译** - AI 一次性翻译所有描述
4. **写入文件** - 修改 description 字段

## 回滚

如需恢复原文，从 `.describe-zh-backup/` 目录复制备份文件即可。
