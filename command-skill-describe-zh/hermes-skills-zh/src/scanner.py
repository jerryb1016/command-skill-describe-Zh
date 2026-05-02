import re
from pathlib import Path
from typing import List, Optional
from models import SkillInfo
from cli_detector import CLIType

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

            if self.cli_type == CLIType.HERMES and path.name == "commands":
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
