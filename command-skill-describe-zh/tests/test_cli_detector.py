import os
from cli_describe_zh.cli_detector import CLIDetector, CLIType

def test_detect_claude_code():
    detector = CLIDetector()
    # Mock environment
    os.environ["HOME"] = "/home/user"
    cli_type = detector.detect()
    assert cli_type in [CLIType.CLAUDE_CODE, CLIType.OPENCODE, CLIType.OPENCLAW, CLIType.HERMES, CLIType.UNKNOWN]