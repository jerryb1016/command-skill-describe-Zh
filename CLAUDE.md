# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

跨 CLI 工具的 Skill/命令 description 中文化工具。支持 Claude Code、OpenCode、OpenClaw、Hermes 等主流 CLI。

## 核心文件

- **SKILL.md** - 唯一的核心文件，包含完整的翻译工作流程。AI 直接读取并执行其中的步骤。

## 工作流程

1. **备份原文** - 在 `.describe-zh-backup/` 目录备份原始 description
2. **收集描述** - 扫描 skills 目录和 commands 目录
3. **批量翻译** - AI 一次性翻译所有 description 字段
4. **写入文件** - 修改每个 SKILL.md 的 description 字段

## 路径规则

Skill 安装在哪里，就扫描那里：
- **Skills**：本 skill 所在目录的上级目录下的其他 skill 目录
- **Commands**：检查 `../commands/` 是否存在，存在则扫描

例如 skill 在 `~/.claude/skills/describe-zh/SKILL.md`：
- 扫描 `~/.claude/skills/*/SKILL.md`（跳过 describe-zh 自身）
- 扫描 `~/.claude/commands/`（如果存在）

## 支持的 CLI

| CLI 工具 | 命令格式 | Skills 路径 | Commands 路径 |
|---------|---------|------------|--------------|
| Claude Code | `/skill` | `~/.claude/skills/` | `~/.claude/commands/` |
| OpenClaw | `/skill-name` | 同上 | 同上 |
| OpenCode | `/` 前缀 | 插件目录 | 插件目录 |
| Hermes | `/` 前缀 | 相应目录 | 相应目录 |

## 使用方式

直接运行 `/describe-zh`，AI 会按照 SKILL.md 中的步骤执行翻译。

## 注意事项

- 只修改 `description:` 字段，不改 body
- 跳过 describe-zh 自身
- 保持 YAML frontmatter 格式正确
- 翻译前自动备份
