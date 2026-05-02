from cli_describe_zh.models import SkillInfo

def test_skill_info_creation():
    skill = SkillInfo(
        name="test-skill",
        description="Test skill description",
        path="/path/to/skill",
        cli_type="claude_code"
    )
    assert skill.name == "test-skill"
    assert skill.description == "Test skill description"
    assert skill.translated_description is None