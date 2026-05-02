---
name: describe-zh
description: 将已安装 skill 的 description 改为中文。当用户想让 skill 列表显示中文描述时使用。
---

# describe-zh

将 `~/.claude/skills/` 下所有 skill 的 `SKILL.md` description 字段改为中文。

## 使用方法

1. 读取 `~/.claude/skills/<skill-name>/SKILL.md`
2. 找到 `description:` 字段
3. 将英文描述翻译为中文
4. 写回文件

## 翻译示例

原文：
```yaml
description: Helps users discover and install agent skills...
```

改为：
```yaml
description: 帮助用户发现和安装 agent skills。当用户问"怎么做X"时使用...
```

## 注意事项

- 只修改 `description:` 字段，不要修改 body 内容
- 保持 YAML 格式正确
- 翻译后重启 Claude Code 使更改生效
