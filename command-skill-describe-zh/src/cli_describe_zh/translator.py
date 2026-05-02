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
        """Translate multiple texts in a single API call."""
        if not self.client:
            return texts  # Fallback to original texts

        # Filter out empty texts
        non_empty = [(i, t) for i, t in enumerate(texts) if t and t.strip()]
        if not non_empty:
            return texts

        # Build prompt with all texts numbered
        texts_to_translate = [t for _, t in non_empty]
        numbered_texts = "\n".join(f"{i+1}. {t}" for i, t in enumerate(texts_to_translate))

        prompt = f"""Translate each of the following English texts to {target_lang}. Output one translation per line, numbered to match.

{numbered_texts}

{target_lang.title()} (one per line, numbered 1, 2, 3...):"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            translation_lines = response.content[0].text.strip().split("\n")
            translations = [line.split(". ", 1)[-1].strip() if ". " in line else line.strip() for line in translation_lines]

            # Build result mapping original indices to translations
            result = list(texts)  # Copy original
            for idx, translation in zip([i for i, _ in non_empty], translations):
                result[idx] = translation

            return result
        except Exception:
            return texts  # Fallback on error