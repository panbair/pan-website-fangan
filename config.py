"""
==================================================================
  全局配置 & 预编译正则
==================================================================
"""
import re
import logging

# ============================================================
#  日志
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("webinsight")

# ============================================================
#  超时 & 尺寸
# ============================================================
HTTP_TIMEOUT = 30.0
HTTP_TIMEOUT_SHORT = 15.0
PLAYWRIGHT_TIMEOUT = 30000
PLAYWRIGHT_WAIT = 0.8
VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900
AI_MAX_TOKENS = 8192
AI_TEMPERATURE = 0.6
TEXT_PREVIEW_LENGTH = 8000
TEXT_PREVIEW_LENGTH_PW = 10000
SPA_TEXT_THRESHOLD = 500
MODULE_MIN_WIDTH = 100
MODULE_MIN_HEIGHT = 50
MAX_RETRIES = 3
RETRY_DELAY = 1.0

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8765

# ============================================================
#  预编译正则
# ============================================================
RE_SPA_ROOT = re.compile(
    r'<div[^>]*id=["\'](?:root|app|__next|__nuxt)["\']', re.I
)
RE_MODULE_SCRIPT = re.compile(r'<script[^>]*type=["\']module["\']', re.I)

RE_TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.I | re.S)
RE_META_DESC_1 = re.compile(
    r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', re.I
)
RE_META_DESC_2 = re.compile(
    r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']description["\']', re.I
)
RE_META_KW_1 = re.compile(
    r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']*)["\']', re.I
)
RE_META_KW_2 = re.compile(
    r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*name=["\']keywords["\']', re.I
)
RE_OG_PROP = re.compile(
    r'<meta[^>]*property=["\']og:(\w+)["\'][^>]*content=["\']([^"\']*)["\']', re.I
)
RE_OG_PROP_REV = re.compile(
    r'<meta[^>]*content=["\']([^"\']*)["\'][^>]*property=["\']og:(\w+)["\']', re.I
)
RE_TWITTER = re.compile(
    r'<meta[^>]*name=["\']twitter:(\w+)["\'][^>]*content=["\']([^"\']*)["\']', re.I
)
RE_CANONICAL = re.compile(
    r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']*)["\']', re.I
)
RE_VIEWPORT = re.compile(
    r'<meta[^>]*name=["\']viewport["\'][^>]*content=["\']([^"\']*)["\']', re.I
)
RE_CHARSET = re.compile(r'<meta[^>]*charset=["\']([^"\']*)["\']', re.I)

RE_JSON_LD = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S
)

RE_LINKS = re.compile(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', re.I | re.S)
RE_IMAGES_ALT = re.compile(r'<img[^>]*alt=["\']([^"\']*)["\']', re.I)
RE_SCRIPTS_SRC = re.compile(r'<script[^>]*src=["\']([^"\']*)["\']', re.I)
RE_STYLES_HREF = re.compile(r'<link[^>]*href=["\']([^"\']*\.css[^"\']*)["\']', re.I)
RE_FONTS_GOOGLE = re.compile(r'https?://fonts\.googleapis\.com/[^"\')]+', re.I)
RE_FONTS_FILE = re.compile(r'https?://[^"\')]*font[^"\')]*\.(?:woff2?|ttf|otf)[^"\')]*', re.I)

RE_DIV = re.compile(r'<div[\s>]', re.I)
RE_SECTION = re.compile(r'<section[\s>]', re.I)
RE_IMG = re.compile(r'<img[\s>]', re.I)
RE_A = re.compile(r'<a[\s>]', re.I)
RE_FORM = re.compile(r'<form[\s>]', re.I)
RE_BUTTON = re.compile(r'<button[\s>]', re.I)
RE_VIDEO = re.compile(r'<video[\s>]', re.I)

RE_WEBP = re.compile(r'\.webp["\')]', re.I)
RE_AVIF = re.compile(r'\.avif["\')]', re.I)
RE_SVG = re.compile(r'\.svg["\')]', re.I)

RE_H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
RE_H2 = re.compile(r'<h2[^>]*>(.*?)</h2>', re.I | re.S)
RE_H3 = re.compile(r'<h3[^>]*>(.*?)</h3>', re.I | re.S)
RE_H4 = re.compile(r'<h4[^>]*>(.*?)</h4>', re.I | re.S)
RE_H5 = re.compile(r'<h5[^>]*>(.*?)</h5>', re.I | re.S)
RE_H6 = re.compile(r'<h6[^>]*>(.*?)</h6>', re.I | re.S)

RE_CLEAN_SCRIPT = re.compile(r'<script[^>]*>.*?</script>', re.I | re.S)
RE_CLEAN_STYLE = re.compile(r'<style[^>]*>.*?</style>', re.I | re.S)
RE_CLEAN_TAGS = re.compile(r'<[^>]+>')
RE_CLEAN_WS = re.compile(r'\s+')
RE_INLINE_TAG = re.compile(r'<[^>]+>')

RE_SEMANTIC_TAG = re.compile(
    r'<(header|nav|main|article|aside|footer|figure|figcaption)[\s>]', re.I
)
