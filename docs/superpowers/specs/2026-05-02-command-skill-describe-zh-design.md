# Command Skill Describe ZH - 设计规范

## 项目概述

**项目名称**: command-skill-describe-zh
**项目目标**: 跨 CLI 工具的命令和 Skill 描述中文化适配器
**核心功能**: 自动翻译所有已安装 Skill 的 description 字段为中文

## 验收标准（Acceptance Criteria）

**最终目标**: 用户在任意支持的 CLI 中输入 `/` 后，显示的命令列表中，每个命令的一句话描述（description）显示为中文。

**示例效果**:
| 原英文 | 翻译后中文 |
|--------|-----------|
| `exit` - Exit the current session | `exit` - 退出当前会话 |
| `help` - Show help information | `help` - 显示帮助信息 |
| `undo` - Undo the last action | `undo` - 撤销上一个操作 |
| `skills` - Manage installed skills | `skills` - 管理已安装的技能 |

**验收确认**: 用户输入 `/` → 显示命令列表 → 所有 description 为中文

## 支持的 CLI 工具

| CLI 工具 | 斜杠命令来源 | 路径 |
|---------|------------|------|
| Claude Code | 内置命令 + 自定义命令 + 插件安装命令 | `~/.claude/commands/*.md` (自定义)<br>`~/.claude/skills/*/SKILL.md` (插件) |
| OpenCode | Skill 系统 | `~/.config/opencode/skills/` 或 `~/.claude/skills/` |
| OpenClaw | Skill 系统 | `./skills/` |
| Hermes | 待确认 | 待确认 |

**Claude Code 命令来源说明**：
1. **内置命令** - CLI 内置的斜杠命令
2. **自定义命令** - `~/.claude/commands/*.md` 中用户自己创建的斜杠命令
3. **插件安装命令** - 通过 `/plugin install` 安装的第三方 Skill，其描述文件位于 `~/.claude/skills/<plugin-name>/SKILL.md`

## 核心机制

### 工作原理

当用户安装 `describe-zh` Skill 后，该 Skill 会：

1. **扫描** - 扫描本机已安装的所有 Skill 的 `SKILL.md` 文件
2. **提取** - 提取每个 Skill 的 `description` 字段
3. **翻译** - 调用 AI API 将 description 翻译为中文
4. **缓存** - 存储翻译结果，避免重复翻译
5. **返回** - 在 CLI 显示 Skill 列表时，返回翻译后的中文 description

### 拦截流程

```
用户执行 /help 或查看 Skill 列表
    ↓
CLI 调用 describe-zh Skill
    ↓
describe-zh 扫描其他 Skills 的 SKILL.md
    ↓
提取 description 并翻译为中文
    ↓
返回翻译后的 Skill 列表（中文 description）
```

## 功能模块

### 1. Skill 扫描器

```python
class SkillScanner:
    def scan_skills(self, cli_type: str) -> List[SkillInfo]:
        """扫描指定 CLI 的所有已安装 Skill"""
        pass

    def extract_description(self, skill_path: str) -> str:
        """从 SKILL.md 或 .md 文件中提取 description"""
        pass

# Claude Code 需要扫描多个来源
CC_SCAN_PATHS = {
    "commands": "~/.claude/commands/",      # 自定义斜杠命令
    "skills": "~/.claude/skills/"           # 插件安装的 Skill
}
```

### 2. 翻译器

```python
class Translator:
    def translate(self, text: str, target_lang: str = "zh") -> str:
        """调用 AI API 翻译文本"""
        pass

    def batch_translate(self, texts: List[str]) -> List[str]:
        """批量翻译多个文本"""
        pass
```

### 3. 缓存层

- 本地缓存已翻译内容
- 缓存结构：`{skill_path: {description: "...", translated_at: "..."}}`
- 缓存有效期可配置

### 4. 描述翻译 Skill

每个 CLI 对应一个翻译 Skill，包结构：

```
{cli}-skills-zh/
├── SKILL.md                    # 核心描述文件
├── README.md                   # 安装说明
├── install.sh                  # 安装脚本
└── src/
    ├── scanner.py              # Skill 扫描器
    ├── translator.py           # 翻译器
    └── cache.py                # 缓存管理
```

### 5. SKILL.md 结构

```markdown
---
name: describe-zh
description: 将所有 Skill 的描述翻译为中文 | Translate all skill descriptions to Chinese
---

# describe-zh

自动将系统中所有已安装 Skill 的 description 翻译为中文。

## 功能
1. 扫描本机已安装的所有 Skill
2. 提取每个 Skill 的 description
3. 调用 AI API 翻译为中文
4. 返回翻译后的描述

## 使用
安装后，所有 Skill 列表的描述将自动显示为中文。
```

## 安装方式

```bash
# OpenClaw
clawhub install describe-zh

# Claude Code
claude skill install describe-zh

# 其他 CLI 类似
```

## 配置选项

```yaml
translator:
  api_key: $ANTHROPIC_API_KEY
  model: "claude-sonnet-4-20250514"
  cache_ttl: 3600  # 缓存时间（秒）
  target_lang: "zh"
```

## 错误处理

| 场景 | 处理方式 |
|-----|---------|
| AI API 不可用 | 返回原文英文 description |
| 网络超时 | 返回原文 + 轻量级重试提示 |
| 配额用尽 | 返回原文 + 用户通知 |
| 扫描失败 | 跳过该 Skill，返回其他翻译结果 |

## 项目目录结构

```
command-skill-describe-zh/
├── claude-code-skills-zh/
│   ├── SKILL.md
│   ├── README.md
│   ├── install.sh
│   └── src/
│       ├── scanner.py
│       ├── translator.py
│       └── cache.py
├── opencode-skills-zh/
│   ├── SKILL.md
│   ├── README.md
│   └── src/
│       └── ...
├── openclaw-skills-zh/
│   ├── SKILL.md
│   ├── README.md
│   └── src/
│       └── ...
└── hermes-skills-zh/
    ├── SKILL.md
    ├── README.md
    └── src/
        └── ...
```

## 后续步骤

1. 实现 Skill 扫描器
2. 实现翻译器模块
3. 实现缓存机制
4. 为每个 CLI 创建独立的 Skill 包
5. 编写各平台的安装脚本
6. 测试各 CLI 的集成
7. 发布到各 CLI 的市场/仓库
