---
name: describe-zh
description: 将已安装 skill 的 description 改为中文。当用户想让 skill 列表显示中文描述时使用。
---

# describe-zh

将 Claude Code 中所有 skill 和 command 的描述改为中文。

## 工作流程

### 第一步：备份原文

在修改任何文件之前，先备份所有原文：

1. 创建 `~/.claude/.describe-zh-backup/` 目录
2. 对每个要翻译的文件，复制一份到备份目录
3. 备份文件命名：`原路径.descriptions.md`（如 `skills/find-skills.descriptions.md`）

### 第二步：批量收集待翻译内容

1. 扫描 `~/.claude/skills/` 下所有 `SKILL.md`
2. 扫描 `~/.claude/commands/` 下所有 `.md` 文件
3. 收集所有 `description:` 字段的原文
4. 一次性展示给用户确认

### 第三步：批量翻译

1. 将所有待翻译文本一次性发送给 AI
2. 要求 AI 按编号输出翻译结果
3. 收到翻译结果后，按编号匹配文件

### 第四步：批量写入

1. 按顺序修改每个文件的 `description:` 字段
2. 显示修改进度（如 "3/10"）
3. 完成后显示总结

## 修改范围

### Skills (`~/.claude/skills/`)

```
~/.claude/skills/<skill-name>/SKILL.md
```

### Commands (`~/.claude/commands/`)

```
~/.claude/commands/<command>/<subcommand>.md
```

## 翻译示例

批量翻译格式（第二阶段输出给 AI）：

```
请翻译以下 description 字段，输出格式为 "编号. 原文 → 译文"：

1. Helps users discover and install agent skills when they ask...
2. Suite of tools for creating elaborate, multi-component...
3. Review UI code for Web Interface Guidelines compliance...

译文：
1. 帮助用户发现和安装 agent skills。当用户问"怎么做X"时使用...
2. 创建复杂多组件 claude.ai HTML artifact 的工具套件...
3. 审查 UI 代码是否符合网页界面设计规范...
```

## 回滚方法

如需恢复原文：

1. 从 `~/.claude/.describe-zh-backup/` 找到对应备份
2. 将备份内容复制回原文件
3. 重启 Claude Code

## 注意事项

- 只修改 `description:` 字段，不要修改 body 内容
- 保持 YAML frontmatter 格式正确
- 翻译后重启 Claude Code 使更改生效
- 首次使用会自动创建备份目录
