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

        # Verify scanner can find and parse the skill
        from cli_describe_zh.scanner import SkillScanner
        from cli_describe_zh.cache import TranslationCache

        scanner = SkillScanner(CLIType.CLAUDE_CODE)
        scanner.search_paths = [skills_dir]
        skills = scanner.scan()

        assert len(skills) >= 1
        assert skills[0].name == "test-skill"
        assert "manage tasks" in skills[0].description

def test_cache_persistence():
    """Test that cache stores and retrieves translations."""
    from cli_describe_zh.cache import TranslationCache

    with tempfile.TemporaryDirectory() as tmpdir:
        cache = TranslationCache(cache_dir=Path(tmpdir))

        # Set a translation
        cache.set("test_key", "Hello", "你好")

        # Retrieve it
        result = cache.get("test_key", "Hello")
        assert result == "你好"
