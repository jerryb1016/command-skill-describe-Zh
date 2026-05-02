import json
import time
from pathlib import Path
from typing import Optional

class TranslationCache:
    """Local cache for translations."""

    def __init__(self, cache_dir: Optional[Path] = None, ttl: int = 3600):
        self.cache_dir = cache_dir or Path.home() / ".cache" / "cli-describe-zh"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl
        self._memory_cache: dict[str, dict] = {}

    def _get_cache_path(self, key: str) -> Path:
        """Get the cache file path for a key."""
        import hashlib
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str, original: str) -> Optional[str]:
        """Get cached translation."""
        # Check memory cache first
        if key in self._memory_cache:
            entry = self._memory_cache[key]
            if time.time() - entry["cached_at"] < self.ttl:
                return entry["translation"]

        # Check disk cache
        cache_path = self._get_cache_path(key)
        if cache_path.exists():
            try:
                with open(cache_path) as f:
                    entry = json.load(f)

                if time.time() - entry["cached_at"] < self.ttl:
                    self._memory_cache[key] = entry
                    return entry["translation"]
            except (json.JSONDecodeError, KeyError):
                pass

        return None

    def set(self, key: str, original: str, translation: str) -> None:
        """Set cached translation."""
        entry = {
            "original": original,
            "translation": translation,
            "cached_at": time.time(),
        }

        # Save to memory
        self._memory_cache[key] = entry

        # Save to disk
        cache_path = self._get_cache_path(key)
        with open(cache_path, "w") as f:
            json.dump(entry, f)

    def clear(self) -> None:
        """Clear all cached translations."""
        self._memory_cache.clear()
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()