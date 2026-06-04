"""分析结果缓存 — 避免重复分析同一 URL"""
import time
import hashlib
from config import CACHE_TTL, logger


class AnalysisCache:
    """简单的内存缓存，TTL 30 分钟"""

    def __init__(self, ttl: int = 1800):
        self._store: dict[str, dict] = {}
        self._ttl = ttl
        self._url_map: dict[str, str] = {}  # hash -> url 映射，供管理接口使用

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
                self._evict(key)
        return None

    def set(self, url: str, data: dict):
        key = self._key(url)
        self._store[key] = {"data": data, "timestamp": time.time()}
        self._url_map[key] = url
        logger.info(f"缓存写入: {url}")

    def _evict(self, key: str):
        del self._store[key]
        self._url_map.pop(key, None)

    def clear(self):
        count = len(self._store)
        self._store.clear()
        self._url_map.clear()
        return count

    def stats(self) -> dict:
        """返回缓存统计信息"""
        now = time.time()
        valid_entries = 0
        urls = []
        for key, entry in list(self._store.items()):
            if now - entry["timestamp"] < self._ttl:
                valid_entries += 1
                urls.append(self._url_map.get(key, key))
            else:
                self._evict(key)
        return {"size": valid_entries, "urls": urls, "ttl_seconds": self._ttl}


# 全局单例
analysis_cache = AnalysisCache(ttl=CACHE_TTL)
