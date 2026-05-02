---
name: describe-zh
description: 将已安装 skill 的 description 改为中文。当用户想让 skill 列表显示中文描述时使用。
---

# describe-zh

将 Hermes 中所有 skill 的描述改为中文。

## 工作流程

### 第一步：备份原文

在修改任何文件之前，先备份所有原文：

1. 创建 `~/.hermes/.describe-zh-backup/` 目录
2. 对每个要翻译的文件，复制一份到备份目录

### 第二步：批量收集待翻译内容

1. 扫描 `~/.hermes/skills/` 下所有 `SKILL.md`
2. 收集所有 `description:` 字段的原文
3. 一次性展示给用户确认

### 第三步：批量翻译

1. 将所有待翻译文本一次性发送给 AI
2. 要求 AI 按编号输出翻译结果
3. 收到翻译结果后，按编号匹配文件

### 第四步：批量写入

1. 按顺序修改每个文件的 `description:` 字段
2. 显示修改进度
3. 完成后显示总结

## 修改范围

- `~/.hermes/skills/<skill-name>/SKILL.md`

## 回滚方法

如需恢复原文：

1. 从 `~/.hermes/.describe-zh-backup/` 找到对应备份
2. 将备份内容复制回原文件
3. 重启 Hermes

## 注意事项

- 只修改 `description:` 字段
- 保持 YAML frontmatter 格式正确
- 翻译后重启使更改生效
