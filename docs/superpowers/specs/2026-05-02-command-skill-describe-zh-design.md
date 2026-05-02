# Command Skill Describe ZH - 设计规范

## 项目概述

**项目名称**: command-skill-describe-zh
**项目目标**: 跨 CLI 工具的命令和 Skill 描述中文化适配器
**核心功能**: 为不懂英文的用户提供主流 CLI 工具的命令描述中文翻译

## 支持的 CLI 工具

| CLI 工具 | 安装路径 | 命令格式 |
|---------|---------|---------|
| Claude Code | `~/.claude/skills/` | `/command` |
| OpenCode | `~/.config/opencode/skills/` 或 `~/.claude/skills/` | `/command` |
| OpenClaw | `./skills/` | `/skill-name` |
| Hermes | 待确认 | `/command` |

## 架构设计

### 整体架构

每个 CLI 有独立的翻译 Skill 包，安装到对应 CLI 后，透明替换原版命令描述为中文。

```
项目仓库
├── claude-code-skills-zh/    # Claude Code 翻译包
├── opencode-skills-zh/        # OpenCode 翻译包
├── openclaw-skills-zh/        # OpenClaw 翻译包
└── hermes-skills-zh/          # Hermes 翻译包
```

### 核心组件

1. **翻译 Skill** - 各 CLI 的翻译覆盖层
2. **翻译器** - 调用 AI API 进行实时翻译
3. **缓存层** - 管理已翻译内容的缓存
4. **配置管理** - 用户配置（API Key、缓存策略等）

### 工作流程

```
用户输入 /help → CLI 拦截 → Skill 触发 → 调用 AI API 翻译 → 返回中文描述
```

## 功能模块

### 1. 翻译 Skill

每个 CLI 对应一个翻译 Skill，包结构：

```
{cli}-skills-zh/
├── SKILL.md                    # 核心描述文件
├── README.md                   # 安装说明
├── install.sh                  # 安装脚本
└── translator.py               # 翻译模块（可选内嵌）
```

### 2. SKILL.md 结构

```markdown
---
name: describe-zh
description: 将命令描述翻译为中文 | Translate command descriptions to Chinese
---

# describe-zh

自动将所有命令和 Skill 的描述翻译为中文。

## 触发条件
当用户执行任何 `/` 开头的命令时，自动翻译其描述。

## 翻译流程
1. 拦截命令描述请求
2. 调用 AI API 翻译为中文
3. 返回翻译后的描述
```

### 3. 翻译器模块

```python
class Translator:
    def translate(self, text: str, target_lang: str = "zh") -> str:
        """调用 AI API 翻译文本"""
        pass

    def translate_with_cache(self, text: str) -> str:
        """带缓存的翻译"""
        pass
```

### 4. 缓存机制

- 本地缓存已翻译内容，减少 API 调用
- 缓存结构：`{text_hash: {zh: "...", en: "...", cached_at: "..."}}`
- 缓存有效期可配置

### 5. 配置管理

```yaml
translator:
  api_key: $ANTHROPIC_API_KEY  # 使用环境变量
  model: "claude-sonnet-4-20250514"
  cache_ttl: 3600  # 缓存时间（秒）
  target_lang: "zh"
```

## 用户交互

### 安装方式

```bash
# OpenClaw
clawhub install describe-zh

# Claude Code
claude skill install describe-zh

# 其他 CLI 类似
```

### 使用命令

- `/describe-zh on` - 启用中文描述
- `/describe-zh off` - 切换回英文描述
- `/describe-zh reload` - 重新加载配置

## 错误处理

| 场景 | 处理方式 |
|-----|---------|
| AI API 不可用 | 显示原文英文描述 |
| 网络超时 | 显示原文 + 重试提示 |
| 配额用尽 | 显示原文 + 用户通知 |

## 项目目录结构

```
command-skill-describe-zh/
├── claude-code-skills-zh/
│   ├── SKILL.md
│   ├── README.md
│   └── install.sh
├── opencode-skills-zh/
│   ├── SKILL.md
│   ├── README.md
│   └── install.sh
├── openclaw-skills-zh/
│   ├── SKILL.md
│   ├── README.md
│   └── install.sh
└── hermes-skills-zh/
    ├── SKILL.md
    ├── README.md
    └── install.sh
```

## 后续步骤

1. 实现核心翻译模块
2. 为每个 CLI 创建独立的 Skill 包
3. 编写各平台的安装脚本
4. 测试各 CLI 的集成
5. 发布到各 CLI 的市场/仓库
