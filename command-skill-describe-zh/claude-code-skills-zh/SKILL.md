---
name: describe-zh
description: 将已安装 skill 的 description 改为中文。当用户想让 skill 列表显示中文描述时使用。
---

# describe-zh

将 Claude Code 中所有 skill 和 command 的描述改为中文。

## 修改范围

### Skills (`~/.claude/skills/`)

1. 读取 `~/.claude/skills/<skill-name>/SKILL.md`
2. 找到 `description:` 字段
3. 将英文描述翻译为中文
4. 写回文件

### Commands (`~/.claude/commands/`)

commands 目录结构为 `~/.claude/commands/<command>/<subcommand>.md`

1. 遍历 `~/.claude/commands/` 下每个子目录
2. 读取每个 `.md` 文件的 frontmatter
3. 找到 `description:` 字段
4. 将英文描述翻译为中文
5. 写回文件

## 翻译示例

Skills 原文：
```yaml
description: Helps users discover and install agent skills...
```

改为：
```yaml
description: 帮助用户发现和安装 agent skills。当用户问"怎么做X"时使用...
```

Commands 原文：
```yaml
---
name: my-command
description: Brief description of what this command does
---
```

改为：
```yaml
---
name: my-command
description: 这个命令的作用中文描述
---
```

## 注意事项

- 只修改 `description:` 字段，不要修改 body 内容
- 保持 YAML frontmatter 格式正确
- 翻译后重启 Claude Code 使更改生效
