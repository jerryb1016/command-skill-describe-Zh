---
name: describe-zh
description: 将所有已安装 Skill 的描述翻译为中文 | Translate all installed skill descriptions to Chinese
---

# describe-zh

自动将系统中所有已安装 Skill 的 description 翻译为中文。

## 功能

1. 扫描 `~/.config/opencode/skills/` 中的 Skill
2. 扫描 `~/.claude/skills/` 中的 Skill
3. 调用 AI API 将每个 Skill 的 description 翻译为中文
4. 返回翻译后的 Skill 列表

## 使用

安装后，在 OpenCode 中输入 `/describe-zh` 查看翻译后的所有 Skill 描述。

## 配置

环境变量：
- `ANTHROPIC_API_KEY`: Anthropic API Key（必需）