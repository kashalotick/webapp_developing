import time
from abc import ABC, abstractmethod
from typing import Any, Annotated

from fastapi import Depends

from app.deps import LoggerDep
class AbstractTTLCache(ABC):
    @abstractmethod
    def get(self, key: str) -> Any | None:
        pass
    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        pass
    @abstractmethod
    def invalidate(self, prefix: str = "") -> None:
        pass
class TTLCache(AbstractTTLCache):
    def __init__(self, logger: LoggerDep):
        self.logger = logger
        self._data: dict[str, tuple[float, Any]] = {}

    def get(self, key: str, ttl=60) -> Any | None:
        item = self._data.get(key)
        if item is None:
            return None
        expires_at, value = item
        if time.monotonic() > expires_at:
            del self._data[key]
            self.logger.info(f"Cache miss for key: {key}")
            return None

        self.logger.info(f"Cache hit for key: {key}")
        return value

    def set(self, key: str, value: Any) -> None:
        self._data[key] = (time.monotonic() + self.ttl, value)
        self.logger.info(f"Cache set for key: {key}")

    def invalidate(self, prefix: str = "") -> None:
        for key in [k for k in self._data if k.startswith(prefix)]:
            del self._data[key]


cache: AbstractTTLCache | None = None
def get_cache(logger: LoggerDep) -> AbstractTTLCache:
    global cache
    local_cache = cache
    if local_cache is None:
        local_cache = TTLCache(logger=logger)
        cache = local_cache

    return local_cache

CacheDep = Annotated[AbstractTTLCache, Depends(get_cache)]
