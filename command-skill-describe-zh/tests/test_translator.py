import os
from unittest.mock import patch, MagicMock
from cli_describe_zh.translator import Translator

def test_translate_text():
    with patch('anthropic.Anthropic') as mock_anthropic:
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="测试翻译")]
        )

        translator = Translator(api_key="test-key")
        result = translator.translate("Test translation")
        assert "测试翻译" in result