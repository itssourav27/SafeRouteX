"""
Lightweight in-memory cache utilities
"""

from typing import Any, Dict, Tuple


class SimpleCache:
    def __init__(self):
        self._store: Dict[Any, Any] = {}

    def get(self, key):
        return self._store.get(key)

    def set(self, key, value):
        self._store[key] = value

    def exists(self, key) -> bool:
        return key in self._store

    def clear(self):
        self._store.clear()


# Shared caches (intentionally simple for v1)
coord_cache = SimpleCache()
weather_cache = SimpleCache()
earthquake_cache = SimpleCache()
safehouse_cache = SimpleCache()
