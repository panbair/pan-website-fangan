"""
技术栈检测 — Wappalyzer (3000+ 规则) + 预编译正则 (动画库专项)

检测策略:
1. Wappalyzer: 框架 / CMS / 分析工具 / CDN / 服务器 / CSS框架
2. 预编译正则: 动画库 (23种, Wappalyzer 覆盖不全)
3. HTTP 响应头: Server / X-Powered-By / CF-Ray
"""
import re
from config import logger


# ============================================================
#  动画库专项正则 (Wappalyzer 对此类覆盖较弱)
# ============================================================
_ANIMATION_CHECKS: list[tuple[re.Pattern, str]] = []

def _register(patterns: list[str], name: str):
    for p in patterns:
        _ANIMATION_CHECKS.append((re.compile(p, re.I), name))

_register([r'gsap(?:\.min)?\.js', r'gsap@[\d.]+', r'gsap\.registerPlugin',
           r'ScrollTrigger', r'gsap\.to\(', r'gsap\.from\('], "GSAP")
_register([r'ScrollTrigger', r'scrollTrigger'], "GSAP ScrollTrigger")
_register([r'Observer'], "GSAP Observer")
_register([r'framer-motion', r'framerMotion'], "Framer Motion")
_register([r'anime(?:\.min)?\.js', r'animejs'], "Anime.js")
_register([r'three(?:\.min)?\.js', r'three@[\d.]+'], "Three.js")
_register([r'lottie(?:-web)?(?:\.min)?\.js', r'lottie-player', r'@lottiefiles'], "Lottie")
_register([r'@rive-app', r'rive\.wasm'], "Rive")
_register([r'motion\s+one', r'@motionone'], "Motion One")
_register([r'aos(?:\.min)?\.(?:js|css)', r'data-aos[=\\-]', r'AOS\.init'], "AOS")
_register([r'wow(?:\.min)?\.js', r'WOW\.init'], "WOW.js")
_register([r'scrollreveal', r'ScrollReveal\('], "ScrollReveal")
_register([r'locomotive-scroll', r'data-scroll-container', r'data-scroll-section'], "Locomotive Scroll")
_register([r'barba\.js', r'@barba'], "Barba.js")
_register([r'animate\.css', r'animate__\w+'], "animate.css")
_register([r'hover\.css', r'hvr-'], "Hover.css")
_register([r'magic(?:\.min)?\.css'], "Magic Animations")
_register([r'tilt(?:\.min)?\.js', r'tilt\.js'], "Tilt.js")
_register([r'parallax(?:\.min)?\.js'], "Parallax.js")
_register([r'rellax(?:\.min)?\.js'], "Rellax")
_register([r'typed(?:\.min)?\.js'], "Typed.js")
_register([r'particles(?:\.min)?\.js', r'particlesJS'], "Particles.js")
_register([r'tsparticles', r'@tsparticles'], "tsparticles")
_register([r'splitting(?:\.min)?\.js'], "Splitting.js")
_register([r'ScrollSmoother', r'Flip\.', r'SplitText', r'DrawSVG', r'MorphSVG'], "GreenSock 商业版")

del _register


# ============================================================
#  Wappalyzer 检测
# ============================================================
def _detect_with_wappalyzer(url: str, html: str, headers: dict) -> dict:
    """使用 Wappalyzer 专业规则库进行技术栈检测"""
    try:
        from Wappalyzer import Wappalyzer, WebPage

        # Wappalyzer 的 WebPage.new_from_response 需要 requests 风格的响应
        webpage = WebPage.new_from_response(
            url=url,
            html=html,
            headers=headers,
        )
        wappalyzer = Wappalyzer.latest()
        raw = wappalyzer.analyze(webpage)

        # Wappalyzer 返回 { technology_name: { "categories": [...], ... } }
        return raw
    except ImportError:
        logger.info("python-Wappalyzer 未安装，回退到纯正则检测")
        return {}
    except Exception as e:
        logger.warning(f"Wappalyzer 检测失败: {e}，回退到纯正则检测")
        return {}


# Wappalyzer category ID → 我们的分类名
_WAPPALYZER_CATEGORY_MAP = {
    1: "cms",           # CMS
    2: "server",        # Web servers
    6: "frameworks",    # JavaScript frameworks
    10: "analytics",    # Analytics
    12: "libraries",    # JavaScript libraries
    14: "hosting",      # PaaS / hosting
    22: "server",       # Web servers
    23: "fonts",        # Fonts
    25: "libraries",    # JavaScript libraries
    27: "cdn",          # CDN
    31: "cdn",          # CDN
    33: "cdn",          # CDN
    34: "css_framework",# UI frameworks
    47: "build_tools",  # Build tools
    51: "server",       # Web servers
    59: "libraries",    # JavaScript libraries
    61: "analytics",    # Analytics
    66: "css_framework",# UI frameworks
    71: "analytics",    # Analytics
    87: "build_tools",  # Build tools
}


def _classify_wappalyzer_results(raw: dict) -> dict[str, set]:
    """将 Wappalyzer 原始结果分类到我们的结构中"""
    tech: dict[str, set] = {
        "build_tools": set(),
        "frameworks": set(),
        "libraries": set(),
        "animation_libraries": set(),
        "cms": set(),
        "analytics": set(),
        "cdn": set(),
        "css_framework": set(),
        "server": set(),
        "fonts": set(),
        "hosting": set(),
    }

    for tech_name, info in raw.items():
        categories = info.get("categories", [])
        for cat in categories:
            cat_id = cat.get("id") if isinstance(cat, dict) else cat
            target = _WAPPALYZER_CATEGORY_MAP.get(cat_id)
            if target and target in tech:
                tech[target].add(tech_name)

    return tech


# ============================================================
#  主检测函数
# ============================================================
def detect_tech_stack(
    html: str, scripts: list, styles: list, headers: dict, fonts: list = None
) -> dict:
    """
    混合技术栈检测:
    1. Wappalyzer (3000+ 专业规则) → 框架/CMS/分析/CDN/主机
    2. 预编译正则 → 动画库 (Wappalyzer 覆盖不到的领域)
    3. HTTP 响应头 → Server / Powered-By / CDN
    """
    url = headers.get("_url", "")

    # Step 1: Wappalyzer
    wappa_raw = _detect_with_wappalyzer(url, html, headers)
    tech_sets = _classify_wappalyzer_results(wappa_raw)

    # Step 2: 动画库专项正则检测
    full_text = html + " " + " ".join(scripts) + " " + " ".join(styles)
    if fonts:
        full_text += " " + " ".join(fonts)

    for compiled_re, name in _ANIMATION_CHECKS:
        if compiled_re.search(full_text):
            tech_sets["animation_libraries"].add(name)

    # Step 3: HTTP 响应头补充
    server = headers.get("server") or headers.get("Server") or ""
    if server:
        tech_sets["server"].add(server)
    powered = headers.get("x-powered-by") or headers.get("X-Powered-By") or ""
    if powered:
        tech_sets["server"].add(powered)
    if headers.get("cf-ray") or headers.get("CF-Ray"):
        tech_sets["cdn"].add("Cloudflare")

    # 字体检测
    if fonts:
        for f in fonts:
            if "googleapis" in f or "gstatic" in f or "fonts.googleapis" in f:
                tech_sets["fonts"].add("Google Fonts")

    return {k: sorted(v) for k, v in tech_sets.items() if v}
