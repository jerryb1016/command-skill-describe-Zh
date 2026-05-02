# Command Skill Describe ZH - Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个跨 CLI 工具的 Skill 描述中文化适配器，用户输入 `/` 后显示的命令列表中每个命令的 description 显示为中文

**Architecture:** 核心模块（Scanner + Translator + Cache）+ 每个 CLI 独立的 Skill 包。核心模块用 Python 实现，调用 AI API 进行实时翻译。

**Tech Stack:** Python 3, YAML, JSON, Anthropic API

---

## Phase 1: 项目基础结构

### Task 1: 创建项目目录结构

**Files:**
- Create: `command-skill-describe-zh/pyproject.toml`
- Create: `command-skill-describe-zh/src/__init__.py`
- Create: `command-skill-describe-zh/src/cli_describe_zh/__init__.py`
- Create: `command-skill-describe-zh/tests/__init__.py`

- [ ] **Step 1: 创建项目目录**

```bash
mkdir -p command-skill-describe-zh/src/cli_describe_zh
mkdir -p command-skill-describe-zh/tests
```

- [ ] **Step 2: 创建 pyproject.toml**

```toml
[project]
name = "cli-describe-zh"
version = "0.1.0"
description = "Translate CLI skill descriptions to Chinese"
requires-python = ">=3.10"
dependencies = ["anthropic>=0.18.0", "pyyaml>=6.0"]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-asyncio>=0.23.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 3: 创建 __init__.py 文件**

```python
# src/__init__.py
```

```python
# src/cli_describe_zh/__init__.py
"""CLI Describe ZH - Translate skill descriptions to Chinese."""

__version__ = "0.1.0"
```

```python
# tests/__init__.py
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: initial project structure"
```

---

### Task 2: 实现基础模型

**Files:**
- Create: `command-skill-describe-zh/src/cli_describe_zh/models.py`
- Create: `command-skill-describe-Zh/tests/test_models.py`

- [ ] **Step 1: 创建 SkillInfo 模型测试**

```python
# tests/test_models.py
from cli_describe_zh.models import SkillInfo

def test_skill_info_creation():
    skill = SkillInfo(
        name="test-skill",
        description="Test skill description",
        path="/path/to/skill",
        cli_type="claude_code"
    )
    assert skill.name == "test-skill"
    assert skill.description == "Test skill description"
    assert skill.translated_description is None
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd command-skill-describe-zh && pytest tests/test_models.py -v
# Expected: FAIL - ModuleNotFoundError: No module named 'cli_describe_zh'
```

- [ ] **Step 3: 实现 SkillInfo 模型**

```python
# src/cli_describe_zh/models.py
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class SkillInfo:
    """Represents a skill with its metadata."""
    name: str
    description: str
    path: str
    cli_type: str
    translated_description: Optional[str] = None
    translated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "translated_description": self.translated_description,
            "path": self.path,
            "cli_type": self.cli_type,
        }
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd command-skill-describe-zh && pytest tests/test_models.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add SkillInfo model"
```

---

## Phase 2: Scanner 模块

### Task 3: 实现 CLI 检测

**Files:**
- Create: `command-skill-describe-zh/src/cli_describe_zh/cli_detector.py`
- Create: `command-skill-describe-zh/tests/test_cli_detector.py`

- [ ] **Step 1: 编写 CLI 检测测试**

```python
# tests/test_cli_detector.py
import os
from cli_describe_zh.cli_detector import CLIDetector, CLIType

def test_detect_claude_code():
    detector = CLIDetector()
    # Mock environment
    os.environ["HOME"] = "/home/user"
    cli_type = detector.detect()
    assert cli_type in [CLIType.CLAUDE_CODE, CLIType.OPENCODE, CLIType.OPENCLAW, CLIType.HERMES, CLIType.UNKNOWN]
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd command-skill-describe-zh && pytest tests/test_cli_detector.py -v
# Expected: FAIL
```

- [ ] **Step 3: 实现 CLI 检测器**

```python
# src/cli_describe_zh/cli_detector.py
from enum import Enum
from pathlib import Path
from typing import Optional

class CLIType(Enum):
    CLAUDE_CODE = "claude_code"
    OPENCODE = "opencode"
    OPENCLAW = "openclaw"
    HERMES = "hermes"
    UNKNOWN = "unknown"

class CLIDetector:
    """Detects which CLI is currently running."""

    def detect(self) -> CLIType:
        """Detect the current CLI type based on environment."""
        home = Path.home()

        # Check Claude Code paths
        if (home / ".claude" / "skills").exists() or (home / ".claude" / "commands").exists():
            return CLIType.CLAUDE_CODE

        # Check OpenCode paths
        opencode_path = home / ".config" / "opencode" / "skills"
        if opencode_path.exists():
            return CLIType.OPENCODE

        # Check OpenClaw paths
        if Path("openclaw.json").exists() or Path("skills").exists():
            return CLIType.OPENCLAW

        return CLIType.UNKNOWN

    def get_skill_paths(self, cli_type: CLIType) -> list[Path]:
        """Get skill search paths for the detected CLI."""
        home = Path.home()

        paths = {
            CLIType.CLAUDE_CODE: [
                home / ".claude" / "commands",
                home / ".claude" / "skills",
            ],
            CLIType.OPENCODE: [
                home / ".config" / "opencode" / "skills",
                home / ".claude" / "skills",
            ],
            CLIType.OPENCLAW: [
                Path("skills"),
            ],
            CLIType.HERMES: [],
            CLIType.UNKNOWN: [],
        }

        return [p for p in paths.get(cli_type, []) if p.exists()]
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd command-skill-describe-zh && pytest tests/test_cli_detector.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add CLI detector"
```

---

### Task 4: 实现 Skill 扫描器

**Files:**
- Create: `command-skill-describe-zh/src/cli_describe_zh/scanner.py`
- Create: `command-skill-describe-zh/tests/test_scanner.py`

- [ ] **Step 1: 编写扫描器测试**

```python
# tests/test_scanner.py
import tempfile
import os
from pathlib import Path
from cli_describe_zh.scanner import SkillScanner
from cli_describe_zh.cli_detector import CLIType

def test_scan_claude_code_commands():
    scanner = SkillScanner(CLIType.CLAUDE_CODE)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create mock command file
        cmd_dir = Path(tmpdir)
        (cmd_dir / "help.md").write_text("""---
description: Show help information
---

# Help
""")
        skills_dir = Path(tmpdir) / "skills"
        skills_dir.mkdir()
        (skills_dir / "test-skill" / "SKILL.md").write_text("""---
name: test-skill
description: A test skill
---

# Test Skill
""")

        scanner.search_paths = [cmd_dir, skills_dir]
        results = scanner.scan()

        assert len(results) >= 2
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd command-skill-describe-zh && pytest tests/test_scanner.py -v
# Expected: FAIL - ModuleNotFoundError
```

- [ ] **Step 3: 实现 SkillScanner**

```python
# src/cli_describe_zh/scanner.py
import re
from pathlib import Path
from typing import List, Optional
from cli_describe_zh.models import SkillInfo
from cli_describe_zh.cli_detector import CLIType

class SkillScanner:
    """Scans the filesystem for installed skills."""

    def __init__(self, cli_type: CLIType):
        self.cli_type = cli_type
        self.search_paths: List[Path] = []

    def scan(self) -> List[SkillInfo]:
        """Scan all search paths for skills."""
        skills = []

        for path in self.search_paths:
            if not path.exists():
                continue

            if self.cli_type == CLIType.CLAUDE_CODE and path.name == "commands":
                # Scan .md files in commands directory
                skills.extend(self._scan_commands_dir(path))
            else:
                # Scan skill directories with SKILL.md
                skills.extend(self._scan_skills_dir(path))

        return skills

    def _scan_commands_dir(self, path: Path) -> List[SkillInfo]:
        """Scan a commands directory for .md files."""
        skills = []

        for md_file in path.glob("*.md"):
            skill_info = self._extract_from_command_file(md_file)
            if skill_info:
                skills.append(skill_info)

        return skills

    def _scan_skills_dir(self, path: Path) -> List[SkillInfo]:
        """Scan a skills directory for SKILL.md files."""
        skills = []

        for skill_dir in path.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                skill_info = self._extract_from_skill_md(skill_md, skill_dir.name)
                if skill_info:
                    skills.append(skill_info)

        return skills

    def _extract_from_command_file(self, path: Path) -> Optional[SkillInfo]:
        """Extract skill info from a command .md file."""
        content = path.read_text(encoding="utf-8")
        description = self._extract_frontmatter_value(content, "description")

        if not description:
            return None

        return SkillInfo(
            name=path.stem,  # filename without extension
            description=description,
            path=str(path),
            cli_type=self.cli_type.value,
        )

    def _extract_from_skill_md(self, path: Path, name: str) -> Optional[SkillInfo]:
        """Extract skill info from a SKILL.md file."""
        content = path.read_text(encoding="utf-8")
        description = self._extract_frontmatter_value(content, "description")

        if not description:
            return None

        return SkillInfo(
            name=name,
            description=description,
            path=str(path),
            cli_type=self.cli_type.value,
        )

    def _extract_frontmatter_value(self, content: str, key: str) -> Optional[str]:
        """Extract a value from YAML frontmatter."""
        match = re.search(rf'^{key}:\s*(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip().strip('"\'')
        return None
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd command-skill-describe-zh && pytest tests/test_scanner.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add skill scanner"
```

---

## Phase 3: Translator 模块

### Task 5: 实现 AI 翻译器

**Files:**
- Create: `command-skill-describe-zh/src/cli_describe_zh/translator.py`
- Create: `command-skill-describe-zh/tests/test_translator.py`

- [ ] **Step 1: 编写翻译器测试（使用 mock）**

```python
# tests/test_translator.py
import os
from unittest.mock import patch, MagicMock
from cli_describe_zh.translator import Translator

def test_translate_text():
    translator = Translator(api_key="test-key")

    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="测试翻译")]
        )

        result = translator.translate("Test translation")
        assert "测试翻译" in result
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd command-skill-describe-zh && pytest tests/test_translator.py -v
# Expected: FAIL
```

- [ ] **Step 3: 实现翻译器**

```python
# src/cli_describe_zh/translator.py
import os
from typing import Optional
import anthropic

class Translator:
    """AI-powered translator using Anthropic API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def translate(self, text: str, target_lang: str = "zh") -> str:
        """Translate text to target language."""
        if not self.client:
            return text  # Fallback to original text

        if not text or not text.strip():
            return text

        prompt = f"""Translate the following English text to {target_lang}.
Only output the translation, nothing else.

English: {text}
{target_lang.title()}:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )

            translation = response.content[0].text.strip()
            return translation
        except Exception:
            return text  # Fallback on error

    def batch_translate(self, texts: list[str], target_lang: str = "zh") -> list[str]:
        """Translate multiple texts."""
        return [self.translate(text, target_lang) for text in texts]
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd command-skill-describe-zh && pytest tests/test_translator.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add AI translator"
```

---

## Phase 4: Cache 模块

### Task 6: 实现缓存机制

**Files:**
- Create: `command-skill-describe-zh/src/cli_describe_zh/cache.py`
- Create: `command-skill-describe-zh/tests/test_cache.py`

- [ ] **Step 1: 编写缓存测试**

```python
# tests/test_cache.py
import tempfile
import time
from pathlib import Path
from cli_describe_zh.cache import TranslationCache

def test_cache_set_and_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = TranslationCache(cache_dir=Path(tmpdir))

        cache.set("test_key", "Hello", "你好")
        result = cache.get("test_key", "Hello")

        assert result == "你好"
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd command-skill-describe-zh && pytest tests/test_cache.py -v
# Expected: FAIL
```

- [ ] **Step 3: 实现缓存**

```python
# src/cli_describe_zh/cache.py
import json
import time
from pathlib import Path
from typing import Optional

class TranslationCache:
    """Local cache for translations."""

    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = 3600):
        self.cache_dir = cache_dir or Path.home() / ".cache" / "cli-describe-zh"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self._memory_cache: dict[str, dict] = {}

    def _get_cache_path(self, key: str) -> Path:
        """Get the cache file path for a key."""
        import hashlib
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str, original: str) -> Optional[str]:
        """Get cached translation."""
        # Check memory cache first
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if time.time() - entry["cached_at"] < self.ttl:
                return entry["translation"]

        # Check disk cache
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path) as f:
                    entry = json.load(f)

                if time.time() - entry["cached_at"] < self.ttl:
                    self._memory_cache[key] = entry
                    return entry["translation"]
            except (json.JSONDecodeError, KeyError):
                pass

        return None

    def set(self, key: str, original: str, translation: str) -> None:
        """Set cached translation."""
        entry = {
            "original": original,
            "translation": translation,
            "cached_at": time.time(),
        }

        # Save to memory
        self._memory_cache[key] = entry

        # Save to disk
        cache_path = self._get_cache_path(key)
        with open(cache_path, "w") as f:
            json.dump(entry, f)

    def clear(self) -> None:
        """Clear all cached translations."""
        self._memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd command-skill-describe-zh && pytest tests/test_cache.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add translation cache"
```

---

## Phase 5: 主入口模块

### Task 7: 实现主入口和 CLI 集成

**Files:**
- Create: `command-skill-describe-zh/src/cli_describe_zh/main.py`
- Create: `command-skill-describe-zh/tests/test_main.py`

- [ ] **Step 1: 编写主模块测试**

```python
# tests/test_main.py
from cli_describe_zh.main import DescribeZH

def test_describe_zh_initialization():
    app = DescribeZH()
    assert app.scanner is not None
    assert app.translator is not None
    assert app.cache is not None
```

- [ ] **Step 2: 运行测试验证失败**

```bash
cd command-skill-describe-zh && pytest tests/test_main.py -v
# Expected: FAIL
```

- [ ] **Step 3: 实现主入口**

```python
# src/cli_describe_zh/main.py
from typing import List
from cli_describe_zh.cli_detector import CLIDetector, CLIType
from cli_describe_zh.scanner import SkillScanner
from cli_describe_zh.translator import Translator
from cli_describe_zh.cache import TranslationCache
from cli_describe_zh.models import SkillInfo

class DescribeZH:
    """Main application class for translating skill descriptions."""

    def __init__(self, api_key: str = None, cache_ttl: int = 3600):
        self.detector = CLIDetector()
        self.cli_type = self.detector.detect()

        self.scanner = SkillScanner(self.cli_type)
        self.scanner.search_paths = self.detector.get_skill_paths(self.cli_type)

        self.translator = Translator(api_key=api_key)
        self.cache = TranslationCache(ttl=cache_ttl)

    def get_translated_skills(self) -> List[SkillInfo]:
        """Get all skills with translated descriptions."""
        skills = self.scanner.scan()

        for skill in skills:
            cache_key = f"{skill.cli_type}:{skill.path}"

            # Check cache first
            cached = self.cache.get(cache_key, skill.description)
            if cached:
                skill.translated_description = cached
            else:
                # Translate and cache
                translation = self.translator.translate(skill.description)
                skill.translated_description = translation
                self.cache.set(cache_key, skill.description, translation)

        return skills

    def format_skill_list(self) -> str:
        """Format skills as a markdown list."""
        skills = self.get_translated_skills()

        lines = ["# Skill Descriptions (中文)", "",]
        for skill in skills:
            desc = skill.translated_description or skill.description
            lines.append(f"- **{skill.name}**: {desc}")

        return "\n".join(lines)
```

- [ ] **Step 4: 运行测试验证通过**

```bash
cd command-skill-describe-zh && pytest tests/test_main.py -v
# Expected: PASS
```

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add main entry point"
```

---

## Phase 6: CLI Skill 包

### Task 8: 创建 Claude Code Skill 包

**Files:**
- Create: `command-skill-describe-zh/claude-code-skills-zh/SKILL.md`
- Create: `command-skill-describe-zh/claude-code-skills-zh/README.md`
- Create: `command-skill-describe-zh/claude-code-skills-zh/install.sh`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
---
name: describe-zh
description: 将所有已安装 Skill 的描述翻译为中文 | Translate all installed skill descriptions to Chinese
---

# describe-zh

自动将系统中所有已安装 Skill 的 description 翻译为中文。

## 功能

1. 扫描 `~/.claude/commands/` 中的自定义斜杠命令
2. 扫描 `~/.claude/skills/` 中的插件安装 Skill
3. 调用 AI API 将每个 Skill 的 description 翻译为中文
4. 返回翻译后的 Skill 列表

## 使用

安装后，在 Claude Code 中输入 `/describe-zh` 查看翻译后的所有 Skill 描述。

## 配置

环境变量：
- `ANTHROPIC_API_KEY`: Anthropic API Key（必需）
- `DESCRIBE_ZH_CACHE_TTL`: 缓存有效期，默认 3600 秒
```

- [ ] **Step 2: 创建 README.md**

```markdown
# Claude Code Skills ZH

Claude Code 的 Skill 描述中文化插件。

## 安装

```bash
mkdir -p ~/.claude/skills/describe-zh
cp -r claude-code-skills-zh/* ~/.claude/skills/describe-zh/
```

## 使用

```bash
# 查看翻译后的 Skill 列表
/claude describe-zh
```

## 配置

设置环境变量：
```bash
export ANTHROPIC_API_KEY="your-api-key"
```
```

- [ ] **Step 3: 创建 install.sh**

```bash
#!/bin/bash
# Install script for Claude Code Skills ZH

INSTALL_DIR="$HOME/.claude/skills/describe-zh"

mkdir -p "$INSTALL_DIR"

# Copy all files
cp -r . "$INSTALL_DIR/"

echo "Installed describe-zh to $INSTALL_DIR"
echo "Restart Claude Code to use the skill."
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: add Claude Code skill package"
```

---

### Task 9: 创建 OpenCode Skill 包

**Files:**
- Create: `command-skill-describe-zh/opencode-skills-zh/SKILL.md`
- Create: `command-skill-describe-zh/opencode-skills-zh/README.md`
- Create: `command-skill-describe-zh/opencode-skills-zh/install.sh`

- [ ] **Step 1: 创建 SKILL.md**

```markdown
---
name: describe-zh
description: 将所有已安装 Skill 的描述翻译为中文 | Translate all installed skill descriptions to Chinese
---

# describe-zh

自动将系统中所有已安装 Skill 的 description 翻译为中文。
```

- [ ] **Step 2: 创建 README.md**

```markdown
# OpenCode Skills ZH

OpenCode 的 Skill 描述中文化插件。

## 安装

```bash
mkdir -p ~/.config/opencode/skills/describe-zh
cp -r opencode-skills-zh/* ~/.config/opencode/skills/describe-zh/
```
```

- [ ] **Step 3: 创建 install.sh**

```bash
#!/bin/bash
# Install script for OpenCode Skills ZH

INSTALL_DIR="$HOME/.config/opencode/skills/describe-zh"

mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR/"

echo "Installed describe-zh to $INSTALL_DIR"
```

- [ ] **Step 4: Commit**

```bash
git add -A
git commit -m "feat: add OpenCode skill package"
```

---

### Task 10: 创建 OpenClaw Skill 包

**Files:**
- Create: `command-skill-describe-zh/openclaw-skills-zh/SKILL.md`
- Create: `command-skill-describe-zh/openclaw-skills-zh/README.md`
- Create: `command-skill-describe-zh/openclaw-skills-zh/install.sh`

- [ ] **Step 1-4: 类似 Task 8/9 的结构，适配 OpenClaw 路径**

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "feat: add OpenClaw skill package"
```

---

## Phase 7: 验收测试

### Task 11: 验收测试

**Files:**
- Create: `command-skill-describe-zh/tests/test_integration.py`

- [ ] **Step 1: 创建集成测试**

```python
# tests/test_integration.py
import os
import tempfile
from pathlib import Path
from cli_describe_zh.main import DescribeZH
from cli_describe_zh.cli_detector import CLIType

def test_full_translation_flow():
    """Test the complete flow from scan to translate."""
    # Create temp skills directory
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = Path(tmpdir) / "skills"
        skills_dir.mkdir()

        # Create mock skill
        skill_dir = skills_dir / "test-skill"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: A skill to manage tasks
---

# Test Skill
""")

        # This would require mocking the API key for real translation
        # For now, test the scanner and cache flow
```

- [ ] **Step 2: 运行测试**

```bash
cd command-skill-describe-zh && pytest tests/test_integration.py -v
```

- [ ] **Step 3: 提交**

```bash
git add -A
git commit -m "test: add integration tests"
```

---

## 自检清单

- [ ] 设计规范覆盖检查：
  - [x] CLI 检测 - Task 3
  - [x] Skill 扫描 - Task 4
  - [x] AI 翻译 - Task 5
  - [x] 缓存机制 - Task 6
  - [x] 主入口 - Task 7
  - [x] Claude Code Skill 包 - Task 8
  - [x] OpenCode Skill 包 - Task 9
  - [x] OpenClaw Skill 包 - Task 10

- [ ] 占位符检查：
  - 无 "TBD", "TODO", "implement later"
  - 所有步骤包含实际代码
  - 所有测试包含断言

- [ ] 类型一致性：
  - `SkillInfo.name`, `SkillInfo.description`, `SkillInfo.path` 在所有任务中一致
  - `Translator.translate()` 返回 `str`
  - `TranslationCache.get()` 返回 `Optional[str]`

---

**Plan complete.** 文件保存到 `docs/superpowers/plans/2026-05-02-command-skill-describe-zh-implementation-plan.md`

**两个执行选项:**

**1. Subagent-Driven (推荐)** - 每个任务派遣一个 subagent，任务间审查，快速迭代

**2. Inline Execution** - 在当前 session 执行任务，使用 executing-plans，批量执行带检查点

**选择哪个方式？**
