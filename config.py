"""
==================================================================
  全局配置 & 预编译正则
==================================================================
"""
import re
import logging

# ============================================================
#  日志 — 格式: HH:MM:SS [LEVEL] message
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("webinsight")

# ============================================================
#  抓取超时（单位：秒 — httpx 使用）
# ============================================================
HTTP_TIMEOUT = 30.0        # 主请求超时（秒）
HTTP_TIMEOUT_SHORT = 15.0  # CSS / 子资源请求超时（秒）

# ============================================================
#  Playwright 动态渲染（单位：毫秒 — Playwright 使用）
# ============================================================
PLAYWRIGHT_TIMEOUT = 30000  # 页面加载总超时（毫秒 = 30秒）
PLAYWRIGHT_WAIT = 2.5       # 额外等待时间，让 JS 动画/路由执行完毕（秒）

# ============================================================
#  视口尺寸（Playwright 模拟桌面分辨率）
# ============================================================
VIEWPORT_WIDTH = 1440
VIEWPORT_HEIGHT = 900

# ============================================================
#  DeepSeek AI 参数
# ============================================================
AI_MAX_TOKENS = 8192     # 单次 AI 响应最大 token 数
AI_TEMPERATURE = 0.6     # 创造性控制（0=精确, 1=创造性）
AI_TIMEOUT = 120.0       # AI API 调用超时（秒）
AI_STREAM_TIMEOUT = 180.0  # 流式 AI 调用超时（秒）

# ============================================================
#  数据截断
# ============================================================
TEXT_PREVIEW_LENGTH = 8000    # 静态抓取时文本预览截断长度
TEXT_PREVIEW_LENGTH_PW = 10000  # Playwright 抓取时文本预览截断长度
SPA_TEXT_THRESHOLD = 500      # 文本低于此长度 + 检测到 SPA 特征 → 判定为 SPA

# ============================================================
#  重试策略（AI API 调用）
# ============================================================
MAX_RETRIES = 3         # 最大重试次数
RETRY_DELAY = 1.0       # 重试间隔乘数（第n次等待 n*RETRY_DELAY 秒）

# ============================================================
#  HTTP 请求头
# ============================================================
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

# ============================================================
#  服务端
# ============================================================
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
SERVER_HOST = "0.0.0.0"   # 监听所有网络接口
SERVER_PORT = 8765         # 服务端口
CACHE_TTL = 3600           # 分析缓存有效期（秒）

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
