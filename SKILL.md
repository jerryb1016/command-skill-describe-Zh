---
name: describe-zh
description: 将已安装 skill 的 description 改为中文。当用户想让 skill 列表显示中文描述时使用。
---

# describe-zh

将当前 CLI 中所有已安装 skill 的 description 改为中文。

## 路径规则

Skill 安装在哪里，就扫描那里：

- **Skills**：本 skill 所在目录的上级目录下的其他 skill 目录
- **Commands**：检查 `../commands/` 是否存在，存在则扫描

例如 skill 在 `~/.claude/skills/describe-zh/SKILL.md`：
- 扫描 `~/.claude/skills/*/SKILL.md`（跳过 describe-zh 自身）
- 扫描 `~/.claude/commands/`（如果存在）

## 工作流程

### 第一步：备份原文

1. 在上级目录创建 `.describe-zh-backup/` 目录
2. 备份所有待修改文件
3. 备份文件命名：`原相对路径.descriptions.md`

### 第二步：批量收集

1. 扫描 skills 目录，找出所有 `SKILL.md`
2. 检查 commands 目录是否存在
3. 收集所有 `description:` 字段原文
4. 展示给用户确认

### 第三步：批量翻译

1. 将所有文本一次性发送给 AI
2. AI 按编号返回翻译结果
3. 按编号匹配文件

### 第四步：批量写入

1. 修改每个文件的 `description:` 字段
2. 显示进度（如 "3/10"）
3. 完成总结

## 翻译格式示例

```
请翻译以下 description 字段：

1. Helps users discover and install agent skills...
2. Suite of tools for creating elaborate...

译文：
1. 帮助用户发现和安装 agent skills...
2. 创建复杂多组件 HTML artifact 的工具套件...
```

## 回滚方法

如需恢复原文：

1. 从 `.describe-zh-backup/` 找到备份
2. 复制回原位置
3. 重启 CLI

## 注意事项

- 只修改 `description:` 字段，不改 body
- 跳过 `describe-zh` 自身
- 保持 YAML frontmatter 格式正确
- 首次使用自动创建备份
