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
        """Return the CLI type for OpenClaw package."""
        return CLIType.OPENCLAW

    def detect(self) -> CLIType:
        """Detect the current CLI type based on environment."""
        return self.get_current_cli_type()

    def get_skill_paths(self, cli_type: CLIType) -> list[Path]:
        """Get skill search paths for the detected CLI."""
        paths = {
            CLIType.OPENCLAW: [
                Path("skills"),
            ],
        }

        return [p for p in paths.get(cli_type, []) if p.exists()]