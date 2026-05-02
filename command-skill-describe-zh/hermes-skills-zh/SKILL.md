---
name: describe-zh
description: 将所有已安装 Skill 的描述翻译为中文 | Translate all installed skill descriptions to Chinese
---

# describe-zh

自动将系统中所有已安装 Skill 的 description 翻译为中文。

## 功能

1. 扫描 `~/.hermes/skills/` 中的插件安装 Skill
2. 扫描 `~/.hermes/commands/` 中的自定义斜杠命令
3. 调用 AI API 将每个 Skill 的 description 翻译为中文
4. 返回翻译后的 Skill 列表

## 使用

安装后，在 Hermes 中输入 `/describe-zh` 查看翻译后的所有 Skill 描述。

## 配置

环境变量：
- `ANTHROPIC_API_KEY`: Anthropic API Key（必需）
- `DESCRIBE_ZH_CACHE_TTL`: 缓存有效期，默认 3600 秒
