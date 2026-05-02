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

    def get_current_cli_type(self) -> CLIType:
        """Return the CLI type for Claude Code package."""
        return CLIType.CLAUDE_CODE

    def detect(self) -> CLIType:
        """Detect the current CLI type based on environment."""
        return self.get_current_cli_type()

    def get_skill_paths(self, cli_type: CLIType) -> list[Path]:
        """Get skill search paths for the detected CLI."""
        home = Path.home()

        paths = {
            CLIType.CLAUDE_CODE: [
                home / ".claude" / "commands",
                home / ".claude" / "skills",
            ],
        }

        return [p for p in paths.get(cli_type, []) if p.exists()]