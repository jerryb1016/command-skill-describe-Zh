#!/usr/bin/env python3
"""Entry point for describe-zh skill."""

import os
import sys
from typing import List

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cli_detector import CLIDetector, CLIType
from scanner import SkillScanner
from translator import Translator
from cache import TranslationCache
from models import SkillInfo


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


def main():
    """Main entry point."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    cache_ttl = int(os.environ.get("DESCRIBE_ZH_CACHE_TTL", "3600"))

    app = DescribeZH(api_key=api_key, cache_ttl=cache_ttl)
    output = app.format_skill_list()
    print(output)


if __name__ == "__main__":
    main()
