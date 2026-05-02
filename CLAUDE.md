# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个跨 CLI 工具的命令和 Skill 描述中文化适配器项目。目标是为不懂英文的用户提供主流 CLI 工具（如 Claude Code、OpenCode、OpenClaw、Hermes 等）的命令描述中文翻译，帮助用户理解并选择正确的命令。

## 项目目标

1. **适配多种 CLI 工具** - 支持 Claude Code、OpenCode、OpenClaw、Hermes 等
2. **命令描述中文化** - 将各 CLI 的斜杠命令（slash commands）描述翻译为中文
3. **Skill 描述翻译** - 将 Skill/插件的功能描述翻译为中文
4. **统一翻译接口** - 提供一致的翻译 API，不影响原 CLI 功能

## 核心功能模块

- **CLI 适配层** - 识别不同 CLI 的命令格式和元数据结构
- **翻译引擎** - 基于 AI 的中英文翻译
- **缓存层** - 缓存已翻译的描述，减少 API 调用
- **CLI 集成** - 透明拦截命令描述，返回翻译后的中文

## 技术栈

- Python（主要语言）
- 支持多 CLI 工具的插件化架构

## Skill 格式规范（基于 ClawHub 官方规范）

### 核心原则

- **Skill 是一个文件夹**，`SKILL.md`（或 `skill.md`）是唯一必需文件
- **仅接受文本文件**（JSON/YAML/TOML/JS/TS/Markdown/SVG 等）
- **Bundle 大小限制**：50MB
- **Slug 格式**：`^[a-z0-9][a-z0-9-]*$`（小写、URL 安全）
- **发布后许可证**：MIT-0（可商用，无需署名）

### SKILL.md 结构

```markdown
---
name: skill-name
description: 简短描述（用于 UI 和搜索）
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:            # 必需的环境变量
        - API_KEY
      bins:           # 必需的 CLI 工具
        - curl
    primaryEnv: API_KEY
    envVars:          # 环境变量声明（含可选变量）
      - name: API_KEY
        required: true
        description: API 令牌
      - name: OPTIONAL_VAR
        required: false
        description: 可选变量
    emoji: "\u2705"
    homepage: https://...
    os: ["macos", "linux"]  # OS 限制
---
# 标题

详细描述技能功能、使用方法、注意事项等。
```

### Frontmatter 字段说明

| 字段 | 类型 | 说明 |
|-----|------|-----|
| `name` | string | 技能名称（小写、URL 安全） |
| `description` | string | 简短描述（UI/搜索用） |
| `version` | string | 语义化版本（semver） |
| `metadata.openclaw.requires.env` | string[] | 必需的环境变量 |
| `metadata.openclaw.requires.bins` | string[] | 必需的 CLI 工具 |
| `metadata.openclaw.requires.anyBins` | string[] | 至少需要一个的 CLI 工具 |
| `metadata.openclaw.primaryEnv` | string | 主要凭证环境变量 |
| `metadata.openclaw.always` | boolean | 是否始终激活（无需显式安装） |
| `metadata.openclaw.emoji` | string | UI 显示 emoji |
| `metadata.openclaw.install` | array | 依赖安装规格（brew/node/go/uv） |

### 完整示例

```yaml
---
name: todoist-cli
description: Manage Todoist tasks, projects, and labels from the command line.
version: 1.2.0
metadata:
  openclaw:
    requires:
      env:
        - TODOIST_API_KEY
      bins:
        - curl
    primaryEnv: TODOIST_API_KEY
    envVars:
      - name: TODOIST_API_KEY
        required: true
        description: Todoist API token.
      - name: TODOIST_PROJECT_ID
        required: false
        description: Optional default project ID.
    emoji: "\u2705"
    homepage: https://github.com/example/todoist-cli
---
```

## CLI 命令斜杠格式

各 CLI 工具的斜杠命令格式：

| CLI 工具 | 命令格式 | 描述位置 |
|---------|---------|---------|
| Claude Code | `/command` 或 `/skill` | 内置命令 + Skill |
| OpenClaw | `/skill-name` | ClawHub Skills |
| OpenCode | `/` 前缀 | 插件系统 |
| Hermes | `/` 前缀 | 命令系统 |

## 项目目录结构

```
command-skill-describe-Zh/
├── cli_adapters/     # CLI 适配器
│   ├── claude_code.py
│   ├── openclaw.py
│   ├── opencode.py
│   └── hermes.py
├── translators/      # 翻译引擎
├── cache/            # 缓存层
├── skills/           # 已翻译的 Skill 描述
└── main.py           # 入口文件
```
