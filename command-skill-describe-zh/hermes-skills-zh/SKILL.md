---
name: describe-zh
description: Translate all installed skill descriptions to Chinese. Use when user wants to see skill descriptions in Chinese or asks to translate skills.
---

# describe-zh

Scan all installed skills and translate their descriptions to Chinese.

## Scan Paths

- `~/.hermes/skills/`
- `~/.hermes/commands/`

## Translation

Use `ANTHROPIC_API_KEY` environment variable for AI translation.
Cache translations locally to avoid repeated API calls.
