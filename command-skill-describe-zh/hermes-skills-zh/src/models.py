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
