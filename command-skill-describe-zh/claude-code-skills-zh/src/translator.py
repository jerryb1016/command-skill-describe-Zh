import os
from typing import Optional
import anthropic

class Translator:
    """AI-powered translator using Anthropic API."""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None

    def translate(self, text: str, target_lang: str = "zh") -> str:
        """Translate text to target language."""
        if not self.client:
            return text  # Fallback to original text

        if not text or not text.strip():
            return text

        prompt = f"""Translate the following English text to {target_lang}.
Only output the translation, nothing else.

English: {text}
{target_lang.title()}:"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )

            translation = response.content[0].text.strip()
            return translation
        except Exception:
            return text  # Fallback on error

    def batch_translate(self, texts: list[str], target_lang: str = "zh") -> list[str]:
        """Translate multiple texts."""
        return [self.translate(text, target_lang) for text in texts]