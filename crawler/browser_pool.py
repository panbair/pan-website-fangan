"""
Playwright 浏览器池 — 复用浏览器实例，避免每次请求启动新浏览器

性能提升: 首次启动 ~2s → 复用后 ~0.1s
"""
import asyncio
from contextlib import asynccontextmanager

from config import VIEWPORT_WIDTH, VIEWPORT_HEIGHT, USER_AGENT, logger


class BrowserPool:
    """单例浏览器池，维护一个常驻 Chromium 实例"""

    def __init__(self):
        self._playwright = None
        self._browser = None
        self._lock = asyncio.Lock()
        self._refcount = 0

    async def _ensure_browser(self):
        """确保浏览器已启动"""
        if self._browser is None or not self._browser.is_connected():
            try:
                from playwright.async_api import async_playwright
            except ImportError:
                return None

            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )
            logger.info("浏览器池: Chromium 已启动")

    async def acquire(self):
        """获取一个浏览器上下文（线程安全的页面）"""
        async with self._lock:
            await self._ensure_browser()
            if self._browser is None:
                return None
            self._refcount += 1

        context = await self._browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent=USER_AGENT,
        )
        page = await context.new_page()
        return BrowserHandle(page, context, self)

    async def release(self, context):
        """释放浏览器上下文"""
        try:
            await context.close()
        except Exception:
            pass

        async with self._lock:
            self._refcount -= 1
            # 空闲时关闭浏览器 (5 分钟无请求)
            if self._refcount <= 0:
                await self._schedule_cleanup()

    async def _schedule_cleanup(self):
        """延迟清理浏览器实例"""
        await asyncio.sleep(300)  # 5 分钟
        async with self._lock:
            if self._refcount <= 0 and self._browser:
                try:
                    await self._browser.close()
                    await self._playwright.stop()
                    self._browser = None
                    self._playwright = None
                    logger.info("浏览器池: Chromium 已关闭 (空闲)")
                except Exception:
                    pass


class BrowserHandle:
    """浏览器页面句柄，支持 async with"""

    def __init__(self, page, context, pool: BrowserPool):
        self.page = page
        self._context = context
        self._pool = pool

    async def __aenter__(self):
        return self.page

    async def __aexit__(self, *args):
        await self._pool.release(self._context)


# 全局单例
_browser_pool: BrowserPool | None = None


def get_browser_pool() -> BrowserPool:
    global _browser_pool
    if _browser_pool is None:
        _browser_pool = BrowserPool()
    return _browser_pool
