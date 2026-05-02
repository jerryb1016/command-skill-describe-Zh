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
