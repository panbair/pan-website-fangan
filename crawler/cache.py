"""分析结果缓存 — 避免重复分析同一 URL"""
import time
import hashlib
from config import logger


class AnalysisCache:
    """简单的内存缓存，TTL 30 分钟"""

    def __init__(self, ttl: int = 1800):
        self._store: dict[str, dict] = {}
        self._ttl = ttl

    def _key(self, url: str) -> str:
        return hashlib.md5(url.strip().lower().encode()).hexdigest()

    def get(self, url: str) -> dict | None:
        key = self._key(url)
        entry = self._store.get(key)
        if entry:
            age = time.time() - entry["timestamp"]
            if age < self._ttl:
                logger.info(f"缓存命中: {url} (age={age:.0f}s)")
                return entry["data"]
            else:
                del self._store[key]
        return None

    def set(self, url: str, data: dict):
        key = self._key(url)
        self._store[key] = {"data": data, "timestamp": time.time()}
        logger.info(f"缓存写入: {url}")

    def clear(self):
        self._store.clear()


# 全局单例
analysis_cache = AnalysisCache(ttl=1800)  # 30 分钟
