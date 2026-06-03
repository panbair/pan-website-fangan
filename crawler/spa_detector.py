"""SPA / 动态网站检测 — 判断是否需要 Playwright 渲染"""
import re
from config import RE_SPA_ROOT, RE_MODULE_SCRIPT, SPA_TEXT_THRESHOLD

# Astro / 动画驱动网站的检测特征
RE_ASTRO_ISLAND = re.compile(r'<astro-island[>\s]', re.I)
RE_ASTRO_STATIC = re.compile(r'/_astro/', re.I)
RE_GSAP_REF = re.compile(r'gsap|ScrollTrigger|framer-motion|motion\.one', re.I)
RE_ANIMATION_CLASS = re.compile(
    r'data-aos|data-wow|data-scroll|data-reveal|data-parallax|data-animate',
    re.I
)
DYNAMIC_SCRIPT_THRESHOLD = 5  # 超过此数量的脚本 → 可能是动态网站


def is_spa_page(website_data: dict) -> bool:
    """检测是否需要 Playwright 动态渲染"""
    html = website_data.get("_raw_html", "")
    if not html:
        return False

    # 条件1: 传统 SPA 挂载点 (React/Vue/Angular/Next/Nuxt)
    has_spa_root = bool(RE_SPA_ROOT.search(html))
    text_len = website_data.get("text_length", 0)
    script_count = len(website_data.get("scripts", []))
    has_low_text = text_len < SPA_TEXT_THRESHOLD and script_count > 0
    has_module_script = bool(RE_MODULE_SCRIPT.search(html))

    # 传统 SPA 检测
    if has_spa_root and (has_low_text or has_module_script):
        return True

    # 条件2: Astro Island Architecture (有内容但动态组件多)
    if bool(RE_ASTRO_ISLAND.search(html)) or bool(RE_ASTRO_STATIC.search(html)):
        return True

    # 条件3: 动画密集型网站 (GSAP/ScrollTrigger/Framer Motion 等)
    if RE_GSAP_REF.search(html):
        return True

    # 条件4: 使用了滚动动画库的 data 属性
    if RE_ANIMATION_CLASS.search(html):
        return True

    # 条件5: 脚本数量多 + 有 module script (Vite/esbuild 构建的轻量 SPA)
    if script_count >= DYNAMIC_SCRIPT_THRESHOLD and has_module_script:
        return True

    return False
