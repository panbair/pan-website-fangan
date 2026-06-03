"""网站抓取模块 — 静态(httpx) + 动态(Playwright) 双引擎"""
from .static import fetch_website_requests
from .playwright import fetch_website_playwright
from .spa_detector import is_spa_page

__all__ = ["fetch_website_requests", "fetch_website_playwright", "is_spa_page"]
