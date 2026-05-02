import tempfile
import os
from pathlib import Path
from cli_describe_zh.scanner import SkillScanner
from cli_describe_zh.cli_detector import CLIType

def test_scan_claude_code_commands():
    scanner = SkillScanner(CLIType.CLAUDE_CODE)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create mock command file
        cmd_dir = Path(tmpdir) / "commands"
        cmd_dir.mkdir()
        (cmd_dir / "help.md").write_text("""---
description: Show help information
---

# Help
""")
        skills_dir = Path(tmpdir) / "skills"
        skills_dir.mkdir()
        test_skill_dir = skills_dir / "test-skill"
        test_skill_dir.mkdir()
        (test_skill_dir / "SKILL.md").write_text("""---
name: test-skill
description: A test skill
---

# Test Skill
""")

        scanner.search_paths = [cmd_dir, skills_dir]
        results = scanner.scan()

        assert len(results) >= 2