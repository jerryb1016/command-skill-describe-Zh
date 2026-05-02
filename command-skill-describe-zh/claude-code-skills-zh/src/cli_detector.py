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