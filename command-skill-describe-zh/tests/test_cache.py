import tempfile
import time
from pathlib import Path
from cli_describe_zh.cache import TranslationCache

def test_cache_set_and_get():
    with tempfile.TemporaryDirectory() as tmpdir:
        cache = TranslationCache(cache_dir=Path(tmpdir))

        cache.set("test_key", "Hello", "你好")
        result = cache.get("test_key", "Hello")

        assert result == "你好"