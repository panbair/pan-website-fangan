"""
==================================================================
  🌐 网站深度分析工具 - DeepSeek AI 驱动
==================================================================
  技术栈: FastAPI + Playwright/Requests + DeepSeek API
  功能: 输入URL → 智能抓取 → AI多维度分析 → 生成专业报告
==================================================================
"""
import asyncio
import base64
import logging
import re
import json
import time
from datetime import datetime
from functools import lru_cache, wraps
from urllib.parse import urlparse
from typing import Optional, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
from openai import OpenAI

# ============================================================
#  日志配置
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("webinsight")

# ============================================================
#  配置常量
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

# ============================================================
#  预编译正则模式
# ============================================================
# --- SPA 检测 ---
RE_SPA_ROOT = re.compile(
    r'<div[^>]*id=["\'](?:root|app|__next|__nuxt)["\']', re.I
)
RE_MODULE_SCRIPT = re.compile(r'<script[^>]*type=["\']module["\']', re.I)

# --- 页面元数据提取 ---
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

# --- 结构化数据 ---
RE_JSON_LD = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', re.I | re.S
)

# --- 资源提取 ---
RE_LINKS = re.compile(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', re.I | re.S)
RE_IMAGES_ALT = re.compile(r'<img[^>]*alt=["\']([^"\']*)["\']', re.I)
RE_SCRIPTS_SRC = re.compile(r'<script[^>]*src=["\']([^"\']*)["\']', re.I)
RE_STYLES_HREF = re.compile(r'<link[^>]*href=["\']([^"\']*\.css[^"\']*)["\']', re.I)
RE_FONTS_GOOGLE = re.compile(r'https?://fonts\.googleapis\.com/[^"\')]+', re.I)
RE_FONTS_FILE = re.compile(r'https?://[^"\')]*font[^"\')]*\.(?:woff2?|ttf|otf)[^"\')]*', re.I)

# --- 标签计数 ---
RE_DIV = re.compile(r'<div[\s>]', re.I)
RE_SECTION = re.compile(r'<section[\s>]', re.I)
RE_IMG = re.compile(r'<img[\s>]', re.I)
RE_A = re.compile(r'<a[\s>]', re.I)
RE_FORM = re.compile(r'<form[\s>]', re.I)
RE_BUTTON = re.compile(r'<button[\s>]', re.I)
RE_VIDEO = re.compile(r'<video[\s>]', re.I)

# --- 现代图片格式 ---
RE_WEBP = re.compile(r'\.webp["\')]', re.I)
RE_AVIF = re.compile(r'\.avif["\')]', re.I)
RE_SVG = re.compile(r'\.svg["\')]', re.I)

# --- 标题提取 ---
RE_H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.I | re.S)
RE_H2 = re.compile(r'<h2[^>]*>(.*?)</h2>', re.I | re.S)
RE_H3 = re.compile(r'<h3[^>]*>(.*?)</h3>', re.I | re.S)
RE_H4 = re.compile(r'<h4[^>]*>(.*?)</h4>', re.I | re.S)
RE_H5 = re.compile(r'<h5[^>]*>(.*?)</h5>', re.I | re.S)
RE_H6 = re.compile(r'<h6[^>]*>(.*?)</h6>', re.I | re.S)

# --- 文本清洗 ---
RE_CLEAN_SCRIPT = re.compile(r'<script[^>]*>.*?</script>', re.I | re.S)
RE_CLEAN_STYLE = re.compile(r'<style[^>]*>.*?</style>', re.I | re.S)
RE_CLEAN_TAGS = re.compile(r'<[^>]+>')
RE_CLEAN_WS = re.compile(r'\s+')
RE_INLINE_TAG = re.compile(r'<[^>]+>')

# ============================================================
#  FastAPI 应用
# ============================================================
app = FastAPI(title="Website Analyzer", description="DeepSeek AI 网站分析工具")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    url: str
    api_key: str
    model: str = "deepseek-chat"


class AnalyzeResponse(BaseModel):
    success: bool
    report: str = ""
    website_data: dict = {}
    error: str = ""


# ============================================================
#  SPA 检测 & 模块提取
# ============================================================
def is_spa_page(website_data: dict) -> bool:
    """检测是否为 SPA 单页应用（需要 Playwright 才能获取真实内容）"""
    html = website_data.get("_raw_html", "")
    if not html:
        return False

    # 1. 查找 SPA 挂载点 (root / app / __next / __nuxt)
    has_spa_root = bool(RE_SPA_ROOT.search(html))

    # 2. 检查是否有大量 JS 但极少文本内容
    text_len = website_data.get("text_length", 0)
    script_count = len(website_data.get("scripts", []))
    has_low_text = text_len < SPA_TEXT_THRESHOLD and script_count > 0

    # 3. 检查是否有 type="module" 脚本（Vite 特征）
    has_module_script = bool(RE_MODULE_SCRIPT.search(html))

    return has_spa_root and (has_low_text or has_module_script)


# ============================================================
#  Playwright 辅助函数
# ============================================================
async def _take_screenshot(page) -> str:
    """截取全页截图并返回 base64"""
    data = await page.screenshot(full_page=True, type="jpeg", quality=75)
    return base64.b64encode(data).decode()


async def _extract_page_modules(page) -> list:
    """提取页面模块"""
    return await extract_page_modules_playwright(page)


async def _detect_runtime_animation(page) -> dict:
    """检测运行时动画库"""
    return await page.evaluate(_RUNTIME_ANIMATION_JS)


async def _extract_text_content(page) -> str:
    """提取页面纯净文本"""
    return await page.evaluate(_TEXT_CONTENT_JS) or ""


async def _extract_links(page) -> list:
    """提取页面链接"""
    return await page.evaluate(_LINKS_JS)


async def _extract_images_detail(page) -> list:
    """提取图片详细信息"""
    return await page.evaluate(_IMAGES_DETAIL_JS)


async def _eval_meta(page, selector: str, attr: str) -> str:
    """提取单个 meta 属性"""
    try:
        return (await page.evaluate(
            f"""(selector, attr) => {{
                const el = document.querySelector(selector);
                return el ? el.getAttribute(attr) || '' : '';
            }}""",
            selector, attr
        )) or ""
    except Exception:
        return ""


async def _eval_attr(page, selector: str, attr: str) -> str:
    """提取单个元素的属性"""
    try:
        return (await page.evaluate(
            f"""(sel, a) => {{
                const el = document.querySelector(sel);
                return el ? el.getAttribute(a) || '' : '';
            }}""",
            selector, attr
        )) or ""
    except Exception:
        return ""


async def _eval_og_tags(page) -> dict:
    """提取 Open Graph 标签"""
    return await page.evaluate(_OG_TAGS_JS)


async def _eval_twitter_tags(page) -> dict:
    """提取 Twitter Card 标签"""
    return await page.evaluate(_TWITTER_TAGS_JS)


async def _eval_charset(page) -> str:
    """提取字符集"""
    try:
        return (await page.evaluate(_CHARSET_JS)) or ""
    except Exception:
        return ""


async def _eval_structured_data(page) -> list:
    """提取 JSON-LD 结构化数据"""
    return await page.evaluate(_STRUCTURED_DATA_JS)


async def _eval_headings(page, selector: str, limit: int) -> list:
    """提取标题文本"""
    try:
        return await page.evaluate(
            f"""(sel, lim) => Array.from(document.querySelectorAll(sel))
                .slice(0, lim).map(h => h.innerText.trim())""",
            selector, limit
        ) or []
    except Exception:
        return []


async def _count_elements(page, selector: str) -> int:
    """计数元素"""
    try:
        return await page.evaluate(f"document.querySelectorAll('{selector}').length") or 0
    except Exception:
        return 0


# ============================================================
#  页面 JavaScript 代码常量（模块提取 & 动画检测）
# ============================================================
_RUNTIME_ANIMATION_JS = """() => {
    const result = {};
    try {
        if (typeof gsap !== 'undefined') {
            result.gsap_version = gsap.version || 'unknown';
            result.timelines = typeof gsap.timeline === 'function' ? 'available' : 'no';
            result.plugins = [];
            if (typeof ScrollTrigger !== 'undefined') {
                result.plugins.push('ScrollTrigger');
                try {
                    const all = ScrollTrigger.getAll ? ScrollTrigger.getAll() : [];
                    result.scrolltrigger_instances = all.length;
                    let scrub = 0, pin = 0, snap = 0, toggleActions = 0, markers = 0;
                    let scrubPinCombo = 0;
                    let startTopTop = 0, startTopBottom = 0, startTopCenter = 0, startOther = 0;
                    let endPlusEq = 0, endBottomTop = 0, endOther = 0;
                    let aboveFold = 0, midFold = 0, deepFold = 0;
                    const triggerMap = {};
                    const viewportH = Math.max(window.innerHeight || 0, 1);

                    const selectorOf = (el) => {
                        if (!el || !el.tagName) return 'unknown';
                        const tag = String(el.tagName || '').toLowerCase();
                        const id = el.id ? ('#' + el.id) : '';
                        let cls = '';
                        try {
                            if (el.classList && el.classList.length) {
                                cls = '.' + Array.from(el.classList).slice(0, 2).join('.');
                            }
                        } catch(e) {}
                        return (tag + id + cls).slice(0, 80);
                    };

                    all.forEach(st => {
                        const v = (st && st.vars) ? st.vars : {};
                        if (v.scrub) scrub++;
                        if (v.pin) pin++;
                        if (v.snap) snap++;
                        if (v.toggleActions) toggleActions++;
                        if (v.markers) markers++;
                        if (v.scrub && v.pin) scrubPinCombo++;

                        const startStr = String(v.start || '').toLowerCase();
                        if (startStr.includes('top top')) startTopTop++;
                        else if (startStr.includes('top bottom')) startTopBottom++;
                        else if (startStr.includes('top center')) startTopCenter++;
                        else if (startStr) startOther++;

                        const endStr = String(v.end || '').toLowerCase();
                        if (endStr.includes('+=')) endPlusEq++;
                        else if (endStr.includes('bottom top')) endBottomTop++;
                        else if (endStr) endOther++;

                        const triggerEl = st && st.trigger ? st.trigger : (v.trigger || null);
                        try {
                            if (triggerEl && triggerEl.getBoundingClientRect) {
                                const rect = triggerEl.getBoundingClientRect();
                                const top = rect.top + (window.scrollY || 0);
                                if (top <= viewportH * 1.2) aboveFold++;
                                else if (top <= viewportH * 3.0) midFold++;
                                else deepFold++;

                                const key = selectorOf(triggerEl);
                                triggerMap[key] = (triggerMap[key] || 0) + 1;
                            } else {
                                deepFold++;
                            }
                        } catch(e) {
                            deepFold++;
                        }
                    });

                    result.scrolltrigger_scrub_count = scrub;
                    result.scrolltrigger_pin_count = pin;
                    result.scrolltrigger_snap_count = snap;
                    result.scrolltrigger_toggle_actions_count = toggleActions;
                    result.scrolltrigger_markers_count = markers;
                    result.scrolltrigger_scrub_pin_combo_count = scrubPinCombo;
                    result.scrolltrigger_start_top_top_count = startTopTop;
                    result.scrolltrigger_start_top_bottom_count = startTopBottom;
                    result.scrolltrigger_start_top_center_count = startTopCenter;
                    result.scrolltrigger_start_other_count = startOther;
                    result.scrolltrigger_end_plus_eq_count = endPlusEq;
                    result.scrolltrigger_end_bottom_top_count = endBottomTop;
                    result.scrolltrigger_end_other_count = endOther;
                    result.scrolltrigger_above_fold_count = aboveFold;
                    result.scrolltrigger_mid_fold_count = midFold;
                    result.scrolltrigger_deep_fold_count = deepFold;
                    result.scrolltrigger_trigger_hotspots = Object.entries(triggerMap)
                        .sort((a, b) => b[1] - a[1])
                        .slice(0, 10)
                        .map(([selector, count]) => ({ selector, count }));
                } catch(e) {
                    result.scrolltrigger_instances = 'unknown';
                }
            }
            if (typeof ScrollSmoother !== 'undefined') result.plugins.push('ScrollSmoother');
            if (typeof SplitText !== 'undefined') result.plugins.push('SplitText');
            if (typeof Flip !== 'undefined') result.plugins.push('Flip');
            if (typeof DrawSVG !== 'undefined') result.plugins.push('DrawSVG');
            if (typeof MorphSVG !== 'undefined') result.plugins.push('MorphSVG');
            if (typeof Observer !== 'undefined') result.plugins.push('Observer');
            if (typeof ScrollTo !== 'undefined') result.plugins.push('ScrollToPlugin');
            if (typeof CustomEase !== 'undefined') result.plugins.push('CustomEase');
        }
    } catch(e) { result.gsap_error = 'not available'; }
    try {
        if (typeof bodymovin !== 'undefined') result.lottie = 'bodymovin';
        else if (typeof lottie !== 'undefined') result.lottie = 'lottie-web';
    } catch(e) {}
    try {
        if (typeof THREE !== 'undefined') result.three_version = THREE.REVISION || 'unknown';
    } catch(e) {}
    try {
        result.smooth_scroll = window.getComputedStyle(document.documentElement).scrollBehavior === 'smooth';
    } catch(e) {}
    try {
        let totalAnimated = 0, totalTransform = 0, willChangeCount = 0;
        document.querySelectorAll('body *').forEach(el => {
            const cs = window.getComputedStyle(el);
            if (cs.animation !== 'none' && cs.animation !== '') totalAnimated++;
            if (cs.transform !== 'none') totalTransform++;
            if (cs.willChange !== 'auto' && cs.willChange !== '') willChangeCount++;
        });
        result.total_animated_elements = totalAnimated;
        result.total_transform_elements = totalTransform;
        result.total_will_change_elements = willChangeCount;
    } catch(e) {}
    return result;
}"""

_TEXT_CONTENT_JS = """() => {
    const clone = document.body.cloneNode(true);
    clone.querySelectorAll('script, style, noscript, svg').forEach(s => s.remove());
    return clone.innerText;
}"""

_LINKS_JS = """() => {
    return Array.from(document.querySelectorAll('a[href]')).slice(0, 80).map(a => ({
        text: a.innerText.trim().substring(0, 100),
        href: a.href,
        isExternal: !a.href.includes(window.location.hostname)
    }));
}"""

_IMAGES_DETAIL_JS = """() => {
    return Array.from(document.querySelectorAll('img')).slice(0, 40).map(img => ({
        alt: img.alt || '',
        src: (img.src || '').substring(0, 150),
        width: img.naturalWidth,
        height: img.naturalHeight,
        loading: img.loading || 'auto',
    }));
}"""

_OG_TAGS_JS = """() => {
    const tags = {};
    document.querySelectorAll('meta[property^="og:"]').forEach(el => {
        tags[el.getAttribute('property').replace('og:', '')] = el.getAttribute('content') || '';
    });
    return tags;
}"""

_TWITTER_TAGS_JS = """() => {
    const tags = {};
    document.querySelectorAll('meta[name^="twitter:"]').forEach(el => {
        tags[el.getAttribute('name').replace('twitter:', '')] = el.getAttribute('content') || '';
    });
    return tags;
}"""

_CHARSET_JS = """() => {
    const el = document.querySelector('meta[charset]');
    return el ? el.getAttribute('charset') : (document.characterSet || '');
}"""

_STRUCTURED_DATA_JS = """() => {
    const items = [];
    document.querySelectorAll('script[type="application/ld+json"]').forEach(el => {
        try { items.push(JSON.parse(el.textContent)); }
        catch(e) { items.push(el.textContent.substring(0, 200)); }
    });
    return items;
}"""


async def extract_page_modules_playwright(page) -> list:
    """使用 Playwright 提取页面每个模块/区块的详细信息"""
    modules = await page.evaluate("""() => {
        const result = [];

        // 查找所有可能的模块容器
        const selectors = [
            'section', '[class*="section"]', '[class*="module"]',
            '[class*="block"]', '[class*="panel"]', '[class*="hero"]',
            '[class*="feature"]', '[class*="banner"]', '[class*="card"]',
            'header[class]', 'footer[class]',
            // 主要布局的直接子元素
            'main > div', '#root > div > div', '#app > div > div',
            'body > div[id]', 'body > div[class*="wrapper"] > div',
        ];

        const foundElements = new Set();

        // 按选择器优先级查找
        for (const sel of selectors) {
            try {
                const els = document.querySelectorAll(sel);
                els.forEach(el => {
                    // 跳过太小的元素（可能是图标或装饰）
                    const rect = el.getBoundingClientRect();
                    const isVisible = rect.width > 100 && rect.height > 50 &&
                                      rect.bottom > -200 && rect.top < window.innerHeight + 500;
                    if (isVisible) {
                        foundElements.add(el);
                    }
                });
            } catch(e) {}
            if (foundElements.size >= 3) break; // 找到足够多就停止
        }

        // 如果没找到，回退到 body 的直接子 div
        if (foundElements.size === 0) {
            document.querySelectorAll('body > div > div > div').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 200 && rect.height > 100) {
                    foundElements.add(el);
                }
            });
        }

        // 收集每个模块的详细信息
        Array.from(foundElements).forEach((el, index) => {
            const rect = el.getBoundingClientRect();
            if (rect.width < 100 || rect.height < 50) return; // 跳过太小的

            // 获取计算样式
            const style = window.getComputedStyle(el);

            // 获取 HTML 结构摘要
            const tagNames = {};
            el.querySelectorAll('*').forEach(child => {
                const tag = child.tagName.toLowerCase();
                tagNames[tag] = (tagNames[tag] || 0) + 1;
            });

            // 获取所有 CSS 类名
            const classList = [];
            el.querySelectorAll('[class]').forEach(child => {
                child.classList.forEach(cls => {
                    if (classList.length < 30 && !classList.includes(cls)) {
                        classList.push(cls);
                    }
                });
            });

            // 获取内联样式关键字
            const inlineStyles = el.getAttribute('style') || '';

            // 提取文本内容
            const text = el.innerText ? el.innerText.trim().substring(0, 500) : '';

            // 子元素摘要
            const childSummary = [];
            const directChildren = el.children;
            for (let i = 0; i < Math.min(directChildren.length, 15); i++) {
                const child = directChildren[i];
                const childTag = child.tagName.toLowerCase();
                const childClass = child.className ? (typeof child.className === 'string' ? child.className.substring(0, 60) : '') : '';
                const childText = child.innerText ? child.innerText.trim().substring(0, 80) : '';
                childSummary.push({
                    tag: childTag,
                    class: childClass,
                    text: childText,
                    childCount: child.children.length
                });
            }

            result.push({
                index: index + 1,
                tag: el.tagName.toLowerCase(),
                id: el.id || '',
                className: (typeof el.className === 'string' ? el.className : '').substring(0, 150),
                width: Math.round(rect.width),
                height: Math.round(rect.height),
                top: Math.round(rect.top + window.scrollY),
                display: style.display,
                position: style.position,
                flexDirection: style.flexDirection,
                gridTemplateColumns: style.gridTemplateColumns || '',
                backgroundColor: style.backgroundColor,
                backgroundImage: style.backgroundImage ? style.backgroundImage.substring(0, 120) : '',
                padding: style.padding,
                margin: style.margin,
                border: style.border,
                borderRadius: style.borderRadius,
                boxShadow: style.boxShadow,
                textContent: text,
                textLength: (el.innerText || '').length,
                childCount: el.children.length,
                tagStats: tagNames,
                cssClasses: classList.slice(0, 30),
                inlineStyle: inlineStyles.substring(0, 200),
                childElements: childSummary,
                // 检测关键属性
                hasAnimation: style.animation !== 'none' && style.animation !== '',
                hasTransform: style.transform !== 'none',
                hasTransition: style.transition !== 'none' && style.transition !== 'all 0s ease 0s',
                hasGradient: style.backgroundImage.includes('gradient'),
                hasVideo: el.querySelectorAll('video').length > 0,
                hasForm: el.querySelectorAll('form, input, textarea').length > 0,
                hasCanvas: el.querySelectorAll('canvas').length > 0,
                hasSVG: el.querySelectorAll('svg').length > 0,
                imgCount: el.querySelectorAll('img').length,
                buttonCount: el.querySelectorAll('button').length,
                linkCount: el.querySelectorAll('a').length,

                // ---- 动画详细参数 ----
                animationDetail: (function() {
                    if (style.animation === 'none' || !style.animation) return null;
                    const parts = style.animation.split(',').map(a => a.trim());
                    return parts.slice(0, 4).map(a => {
                        // 解析 animation 简写: name duration easing delay iteration direction fill
                        const tokens = a.split(/\\s+/);
                        return {
                            full: a.substring(0, 120),
                            name: tokens[0] || '',
                            duration: tokens[1] || '',
                            easing: tokens[2] || '',
                            delay: tokens[3] || '',
                            iteration: tokens[4] || '',
                        };
                    });
                })(),
                transitionDetail: (function() {
                    if (style.transition === 'none' || !style.transition || style.transition === 'all 0s ease 0s') return null;
                    const parts = style.transition.split(',').map(t => t.trim());
                    return parts.slice(0, 4).map(t => ({
                        full: t.substring(0, 120),
                        prop: t.split(/\\s+/)[0] || '',
                        duration: t.split(/\\s+/)[1] || '',
                        easing: t.split(/\\s+/)[2] || '',
                        delay: t.split(/\\s+/)[3] || '',
                    }));
                })(),
                transformDetail: style.transform !== 'none' ? style.transform.substring(0, 200) : '',
                willChange: style.willChange !== 'auto' ? style.willChange : '',
                // 是否有滚动驱动的动画类名
                hasScrollAnimClass: /scroll|reveal|aos|wow|parallax|tilt|magnetic/i.test((typeof el.className === 'string' ? el.className : '') + ' ' + Array.from(el.querySelectorAll('[class]')).map(c => c.className).join(' ').substring(0, 500)),
                // 统计有动画的子元素数量
                animatedChildCount: (function() {
                    let count = 0;
                    el.querySelectorAll('*').forEach(child => {
                        const cs = window.getComputedStyle(child);
                        if ((cs.animation !== 'none' && cs.animation !== '') ||
                            (cs.transition !== 'none' && cs.transition !== '' && cs.transition !== 'all 0s ease 0s') ||
                            cs.transform !== 'none') {
                            count++;
                        }
                    });
                    return count;
                })(),
            });
        });

        return result;
    }""")

    return modules


# ============================================================
#  网站抓取模块
# ============================================================
async def fetch_website_requests(url: str) -> dict:
    """使用 httpx 抓取网站数据（轻量方案，无需浏览器）"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        html = response.text
        final_url = str(response.url)
        resp_headers = dict(response.headers)

    parsed = urlparse(final_url)
    domain = parsed.netloc

    # ---- 提取关键信息（使用预编译正则）----
    title_match = RE_TITLE.search(html)
    title = title_match.group(1).strip() if title_match else ""

    # Meta description（多种格式）
    meta_desc = ""
    for pattern in (RE_META_DESC_1, RE_META_DESC_2):
        m = pattern.search(html)
        if m:
            meta_desc = m.group(1)
            break

    # Meta keywords
    meta_keywords = ""
    for pattern in (RE_META_KW_1, RE_META_KW_2):
        m = pattern.search(html)
        if m:
            meta_keywords = m.group(1)
            break

    # Open Graph 标签
    og_tags = dict(RE_OG_PROP.findall(html))
    if not og_tags:
        og_tags = {v: k for k, v in RE_OG_PROP_REV.findall(html)}

    # Twitter Card 标签
    twitter_tags = dict(RE_TWITTER.findall(html))

    # Canonical URL / Viewport / Charset
    canonical = ""
    m = RE_CANONICAL.search(html)
    if m:
        canonical = m.group(1)

    viewport = ""
    m = RE_VIEWPORT.search(html)
    if m:
        viewport = m.group(1)

    charset = ""
    m = RE_CHARSET.search(html)
    if m:
        charset = m.group(1)

    # Structured Data (JSON-LD)
    structured_data = []
    for m in RE_JSON_LD.finditer(html):
        try:
            structured_data.append(json.loads(m.group(1)))
        except (json.JSONDecodeError, ValueError):
            structured_data.append(m.group(1)[:200] + "...")

    # 提取所有链接
    link_list = []
    for href, text in RE_LINKS.findall(html)[:50]:
        text_clean = RE_INLINE_TAG.sub('', text).strip()
        if text_clean:
            link_list.append(f"{text_clean} → {href}")

    # 提取图片 alt 文本
    images = [alt for alt in RE_IMAGES_ALT.findall(html)[:30] if alt.strip()]

    # 提取脚本 src / 样式 href / 字体
    scripts = RE_SCRIPTS_SRC.findall(html)
    styles = RE_STYLES_HREF.findall(html)
    fonts = RE_FONTS_GOOGLE.findall(html) + RE_FONTS_FILE.findall(html)

    # 清理文本内容
    text_clean = RE_CLEAN_SCRIPT.sub('', html)
    text_clean = RE_CLEAN_STYLE.sub('', text_clean)
    text_clean = RE_CLEAN_TAGS.sub(' ', text_clean)
    text_clean = RE_CLEAN_WS.sub(' ', text_clean).strip()

    # 截取前 N 字符给 AI
    text_preview = text_clean[:TEXT_PREVIEW_LENGTH]

    # ---- 技术栈检测 ----
    tech_stack = detect_tech_stack(html, scripts, styles, resp_headers, fonts)

    # ---- 页面结构分析 ----
    h1_raw = [RE_INLINE_TAG.sub('', h).strip() for h in RE_H1.findall(html)[:10]]
    h2_raw = [RE_INLINE_TAG.sub('', h).strip() for h in RE_H2.findall(html)[:15]]

    h3_h6_raw = []
    for pattern in (RE_H3, RE_H4, RE_H5, RE_H6):
        h3_h6_raw.extend(
            RE_INLINE_TAG.sub('', h).strip() for h in pattern.findall(html)[:5]
        )

    # 统计元素数量
    element_counts = {
        "div_count": len(RE_DIV.findall(html)),
        "section_count": len(RE_SECTION.findall(html)),
        "img_count": len(RE_IMG.findall(html)),
        "a_count": len(RE_A.findall(html)),
        "form_count": len(RE_FORM.findall(html)),
        "button_count": len(RE_BUTTON.findall(html)),
        "video_count": len(RE_VIDEO.findall(html)),
    }

    # 语义化标签检测
    semantic_tags = {}
    for tag in ('header', 'nav', 'main', 'article', 'aside', 'footer', 'figure', 'figcaption'):
        count = len(re.findall(rf'<{tag}[\s>]', html, re.I))
        if count > 0:
            semantic_tags[tag] = count

    # HTTP 响应头摘要
    important_headers = _extract_important_headers(resp_headers)

    # 检测现代图片格式
    modern_images = {
        "webp": len(RE_WEBP.findall(html)),
        "avif": len(RE_AVIF.findall(html)),
        "svg": len(RE_SVG.findall(html)),
    }

    return {
        "url": url,
        "final_url": final_url,
        "domain": domain,
        "_raw_html": html,
        "title": title,
        "meta_description": meta_desc,
        "meta_keywords": meta_keywords,
        "og_tags": og_tags,
        "twitter_tags": twitter_tags,
        "canonical": canonical,
        "viewport": viewport,
        "charset": charset,
        "structured_data": structured_data,
        "h1_headings": h1_raw,
        "h2_headings": h2_raw,
        "h3_h6_headings": h3_h6_raw[:10],
        "text_preview": text_preview,
        "text_length": len(text_clean),
        "links": link_list,
        "images_alt": images,
        "scripts": scripts[:30],
        "styles": styles[:20],
        "tech_stack": tech_stack,
        "response_headers_summary": json.dumps(important_headers, ensure_ascii=False, indent=2),
        "page_stats": {
            **element_counts,
            "html_size_kb": round(len(html) / 1024, 1),
            "semantic_tags_used": semantic_tags,
            "modern_image_formats": modern_images,
        }
    }


def _extract_important_headers(resp_headers: dict) -> dict:
    """从响应头中提取关键信息"""
    important_keys = [
        'server', 'x-powered-by', 'content-type', 'cache-control', 'content-encoding',
        'x-cache', 'cf-ray', 'x-frame-options', 'strict-transport-security',
        'content-security-policy', 'x-content-type-options', 'referrer-policy',
        'permissions-policy', 'set-cookie', 'x-request-id',
    ]
    result = {}
    for key in important_keys:
        val = resp_headers.get(key) or resp_headers.get(key.lower())
        if val:
            result[key] = val
    return result


async def _fetch_response_headers(url: str) -> dict:
    """单独获取 HTTP 响应头"""
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SHORT, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": USER_AGENT})
            return dict(resp.headers), str(resp.url)
    except Exception:
        return {}, url


async def fetch_website_playwright(url: str) -> dict:
    """使用 Playwright 抓取网站数据（支持动态渲染、截图、模块提取）"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.warning("Playwright 未安装，回退到 requests 模式")
        return await fetch_website_requests(url)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": VIEWPORT_HEIGHT},
            user_agent=USER_AGENT,
        )
        page = await context.new_page()

        # 监听网络请求
        network_requests = []
        page.on("request", lambda req: network_requests.append({
            "url": req.url[:200],
            "type": req.resource_type,
            "method": req.method,
        }))

        try:
            await page.goto(url, wait_until="networkidle", timeout=PLAYWRIGHT_TIMEOUT)
            await asyncio.sleep(PLAYWRIGHT_WAIT)

            final_url = page.url
            title = await page.title()
            html = await page.content()

            # 并发执行多个数据提取任务
            (
                screenshot_b64,
                page_modules,
                runtime_animation,
                text_content,
                links_raw,
                images_detail,
                meta_desc,
                meta_keywords,
                og_tags_full,
                twitter_tags_full,
                canonical,
                viewport,
                charset,
                structured_data,
                h1_tags,
                h2_tags,
                h3_h6_tags,
                div_count, section_count, img_count, a_count,
                form_count, button_count, video_count,
                canvas_count, svg_count,
            ) = await asyncio.gather(
                _take_screenshot(page),
                _extract_page_modules(page),
                _detect_runtime_animation(page),
                _extract_text_content(page),
                _extract_links(page),
                _extract_images_detail(page),
                _eval_meta(page, 'meta[name="description"]', 'content'),
                _eval_meta(page, 'meta[name="keywords"]', 'content'),
                _eval_og_tags(page),
                _eval_twitter_tags(page),
                _eval_attr(page, 'link[rel="canonical"]', 'href'),
                _eval_attr(page, 'meta[name="viewport"]', 'content'),
                _eval_charset(page),
                _eval_structured_data(page),
                _eval_headings(page, 'h1', 10),
                _eval_headings(page, 'h2', 20),
                _eval_headings(page, 'h3, h4, h5, h6', 15),
                _count_elements(page, 'div'),
                _count_elements(page, 'section'),
                _count_elements(page, 'img'),
                _count_elements(page, 'a'),
                _count_elements(page, 'form'),
                _count_elements(page, 'button'),
                _count_elements(page, 'video'),
                _count_elements(page, 'canvas'),
                _count_elements(page, 'svg'),
            )

            # 语义化标签
            semantic_tags = {}
            for tag in ('header', 'nav', 'main', 'article', 'aside', 'footer', 'figure', 'figcaption'):
                count = await _count_elements(page, tag)
                if count > 0:
                    semantic_tags[tag] = count

            # 现代图片格式
            modern_images = {
                "webp": len(RE_WEBP.findall(html)),
                "avif": len(RE_AVIF.findall(html)),
                "svg": len(RE_SVG.findall(html)),
            }

            # 脚本和样式
            scripts = RE_SCRIPTS_SRC.findall(html)
            styles = RE_STYLES_HREF.findall(html)
            fonts = RE_FONTS_GOOGLE.findall(html) + RE_FONTS_FILE.findall(html)

            # HTTP 响应头
            resp_headers, final_url_from_headers = await _fetch_response_headers(url)
            if final_url_from_headers:
                final_url = final_url_from_headers

            # 技术栈检测
            tech_stack = detect_tech_stack(html, scripts, styles, resp_headers, fonts)

            # 网络请求汇总
            api_requests = [r for r in network_requests if r['type'] in ('fetch', 'xhr')][:20]
            third_party_domains = set()
            parsed_final = urlparse(final_url)
            for r in network_requests:
                try:
                    dom = urlparse(r['url']).netloc
                    if dom and dom != parsed_final.netloc:
                        third_party_domains.add(dom)
                except Exception:
                    pass

            important_headers = _extract_important_headers(resp_headers)

            images_alt = [img['alt'] for img in images_detail if img.get('alt')]
            text_preview = (text_content or "")[:TEXT_PREVIEW_LENGTH_PW]
            link_list = [f"{l['text']} → {l['href']}" for l in links_raw if l.get('text')]

            return {
                "url": url,
                "final_url": final_url,
                "domain": parsed_final.netloc,
                "_raw_html": html,
                "_source": "playwright",
                "title": title,
                "meta_description": meta_desc or "",
                "meta_keywords": meta_keywords or "",
                "og_tags": og_tags_full,
                "twitter_tags": twitter_tags_full,
                "canonical": canonical or "",
                "viewport": viewport or "",
                "charset": charset or "",
                "structured_data": structured_data,
                "h1_headings": h1_tags,
                "h2_headings": h2_tags,
                "h3_h6_headings": h3_h6_tags,
                "text_preview": text_preview,
                "text_length": len(text_content) if text_content else 0,
                "links": link_list,
                "images_alt": images_alt,
                "images_detail": images_detail[:20],
                "scripts": scripts[:30],
                "styles": styles[:20],
                "fonts": fonts[:10],
                "tech_stack": tech_stack,
                "screenshot_base64": screenshot_b64,
                "response_headers_summary": json.dumps(important_headers, ensure_ascii=False, indent=2),
                "page_stats": {
                    "div_count": div_count,
                    "section_count": section_count,
                    "image_count": img_count,
                    "link_count": a_count,
                    "form_count": form_count,
                    "button_count": button_count,
                    "video_count": video_count,
                    "canvas_count": canvas_count,
                    "svg_count": svg_count,
                    "html_size_kb": round(len(html) / 1024, 1),
                    "semantic_tags_used": semantic_tags,
                    "modern_image_formats": modern_images,
                },
                "page_modules": page_modules,
                "network_summary": {
                    "total_requests": len(network_requests),
                    "api_requests": api_requests,
                    "third_party_domains": list(third_party_domains)[:20],
                },
                "runtime_animation": runtime_animation,
            }
        finally:
            await browser.close()


# ============================================================
#  技术栈检测 — 预编译正则模式
# ============================================================
# 结构: [(compiled_pattern, category, name), ...]
# 每个 category-name 组合只需命中一个 pattern 即被确认
_TECH_CHECKS: list[tuple[re.Pattern, str, str]] = []

def _register(category: str, name: str, patterns: list[str]):
    """注册技术栈检测规则"""
    for p in patterns:
        _TECH_CHECKS.append((re.compile(p, re.I), category, name))

# --- 构建工具 ---
_register("build_tools", "Vite", [r'/assets/[a-zA-Z0-9_-]+\.(?:js|css)', r'vite', r'type="module"'])
_register("build_tools", "Webpack", [r'webpack', r'script src="[^"]*bundle[^"]*\.js'])
_register("build_tools", "Rollup", [r'rollup'])
_register("build_tools", "esbuild", [r'esbuild'])
_register("build_tools", "Turbopack", [r'turbopack'])

# --- 前端框架 ---
_register("frameworks", "React", [r'react(?:\.min)?\.js', r'react-dom', r'__REACT', r'_reactRoot', r'react@[\d.]+'])
_register("frameworks", "Vue.js 3", [r'vue@3', r'vue\.runtime\.esm'])
_register("frameworks", "Vue.js", [r'vue(?:\.min)?\.js', r'vue\.runtime', r'__VUE__', r'data-v-[\da-f]'])
_register("frameworks", "Angular", [r'angular(?:\.min)?\.js', r'ng-version', r'_angular_'])
_register("frameworks", "Next.js", [r'__NEXT', r'_next/static', r'next-', r'__next'])
_register("frameworks", "Nuxt.js", [r'__NUXT__', r'_nuxt/', r'nuxt-'])
_register("frameworks", "Svelte", [r'svelte', r'__SVELTE__'])
_register("frameworks", "jQuery", [r'jquery(?:\.min)?\.js', r'jQuery'])
_register("frameworks", "Alpine.js", [r'alpine(?:\.min)?\.js', r'x-data'])
_register("frameworks", "HTMX", [r'htmx', r'hx-get', r'hx-post'])

# --- JS 库 ---
_register("libraries", "Lodash", [r'lodash', r'_\.(?:map|filter|reduce|debounce)'])
_register("libraries", "Axios", [r'axios(?:\.min)?\.js', r'axios@[\d.]+'])
_register("libraries", "ECharts", [r'echarts(?:\.min)?\.js', r'echarts@[\d.]+'])
_register("libraries", "Chart.js", [r'chart\.js', r'chartjs', r'Chart\.'])
_register("libraries", "D3.js", [r'd3(?:\.min)?\.js', r'd3@[\d.]+'])
_register("libraries", "Swiper", [r'swiper(?:\.min)?\.js', r'swiper-bundle'])
_register("libraries", "Day.js", [r'dayjs(?:\.min)?\.js'])
_register("libraries", "Moment.js", [r'moment(?:\.min)?\.js', r'moment@'])
_register("libraries", "Immer", [r'immer'])
_register("libraries", "Zustand", [r'zustand'])
_register("libraries", "Pinia", [r'pinia'])

# --- 动画库（专项检测）---
_register("animation_libraries", "GSAP", [r'gsap(?:\.min)?\.js', r'gsap@[\d.]+', r'gsap\.registerPlugin', r'ScrollTrigger', r'gsap\.to\(', r'gsap\.from\('])
_register("animation_libraries", "GSAP ScrollTrigger", [r'ScrollTrigger', r'scrollTrigger'])
_register("animation_libraries", "GSAP Observer", [r'Observer'])
_register("animation_libraries", "Framer Motion", [r'framer-motion', r'framerMotion'])
_register("animation_libraries", "Anime.js", [r'anime(?:\.min)?\.js', r'animejs'])
_register("animation_libraries", "Three.js", [r'three(?:\.min)?\.js', r'three@[\d.]+'])
_register("animation_libraries", "Lottie", [r'lottie(?:-web)?(?:\.min)?\.js', r'lottie-player', r'@lottiefiles'])
_register("animation_libraries", "Rive", [r'@rive-app', r'rive\.wasm'])
_register("animation_libraries", "Motion One", [r'motion\s+one', r'@motionone'])
_register("animation_libraries", "AOS (动画滚动库)", [r'aos(?:\.min)?\.(?:js|css)', r'data-aos[=\\-]', r'AOS\.init'])
_register("animation_libraries", "WOW.js", [r'wow(?:\.min)?\.js', r'WOW\.init'])
_register("animation_libraries", "ScrollReveal", [r'scrollreveal', r'ScrollReveal\('])
_register("animation_libraries", "Locomotive Scroll", [r'locomotive-scroll', r'data-scroll-container', r'data-scroll-section'])
_register("animation_libraries", "Barba.js", [r'barba\.js', r'@barba'])
_register("animation_libraries", "animate.css", [r'animate\.css', r'animate__\w+'])
_register("animation_libraries", "Hover.css", [r'hover\.css', r'hvr-'])
_register("animation_libraries", "Magic Animations", [r'magic(?:\.min)?\.css'])
_register("animation_libraries", "Tilt.js", [r'tilt(?:\.min)?\.js', r'tilt\.js'])
_register("animation_libraries", "Parallax.js", [r'parallax(?:\.min)?\.js'])
_register("animation_libraries", "Rellax", [r'rellax(?:\.min)?\.js'])
_register("animation_libraries", "Typed.js", [r'typed(?:\.min)?\.js'])
_register("animation_libraries", "Particles.js", [r'particles(?:\.min)?\.js', r'particlesJS'])
_register("animation_libraries", "tsparticles", [r'tsparticles', r'@tsparticles'])
_register("animation_libraries", "Splitting.js", [r'splitting(?:\.min)?\.js'])
_register("animation_libraries", "GreenSock (商业版)", [r'ScrollSmoother', r'Flip\.', r'SplitText', r'DrawSVG', r'MorphSVG'])

# --- CSS 框架 ---
_register("css_framework", "Tailwind CSS", [r'tailwindcss', r'tailwind', r'class="[^"]*(?:flex |grid |p-\d|m-\d)'])
_register("css_framework", "Bootstrap 5", [r'bootstrap@5', r'bootstrap/dist/css/bootstrap\.min\.css'])
_register("css_framework", "Bootstrap", [r'bootstrap(?:\.min)?\.css', r'bootstrap(?:\.min)?\.js'])
_register("css_framework", "Ant Design", [r'antd', r'ant-design', r'anticon'])
_register("css_framework", "Element Plus", [r'element-plus', r'ElButton', r'ElInput'])
_register("css_framework", "Element UI", [r'element-ui', r'el-'])
_register("css_framework", "Material UI", [r'@mui', r'@material-ui', r'MuiButton', r'Mui'])
_register("css_framework", "UnoCSS", [r'unocss', r'uno-'])
_register("css_framework", "WindiCSS", [r'windicss', r'windi-'])
_register("css_framework", "Bulma", [r'bulma(?:\.min)?\.css'])

# --- CMS ---
_register("cms", "WordPress", [r'wp-content', r'wordpress', r'wp-json', r'wp-includes'])
_register("cms", "Shopify", [r'shopify', r'myshopify'])
_register("cms", "Wix", [r'wix', r'_wix'])
_register("cms", "Squarespace", [r'squarespace', r'static1\.squarespace'])
_register("cms", "Webflow", [r'webflow', r'data-wf-'])

# --- 分析工具 ---
_register("analytics", "Google Analytics 4", [r'gtag', r'googletagmanager', r'G-[A-Z0-9]+'])
_register("analytics", "Google Analytics UA", [r'google-analytics', r'ga\.js', r'UA-\d+'])
_register("analytics", "百度统计", [r'baidu.*tongji', r'hm\.baidu', r'hmt'])
_register("analytics", "Google Tag Manager", [r'googletagmanager\.com/gtm'])
_register("analytics", "Facebook Pixel", [r'facebook\.net', r'fbq\('])
_register("analytics", "Microsoft Clarity", [r'clarity\.ms'])
_register("analytics", "Hotjar", [r'hotjar'])

# --- CDN ---
_register("cdn", "Cloudflare", [r'cloudflare', r'cdn-cgi'])
_register("cdn", "CDNJS", [r'cdnjs\.cloudflare'])
_register("cdn", "jsDelivr", [r'jsdelivr\.net'])
_register("cdn", "UNPKG", [r'unpkg\.com'])
_register("cdn", "esm.sh", [r'esm\.sh'])
_register("cdn", "Skypack", [r'skypack\.dev'])

# --- 托管平台 ---
_register("hosting", "Vercel", [r'vercel', r'x-vercel', r'__vercel'])
_register("hosting", "Netlify", [r'netlify', r'x-nf-'])
_register("hosting", "GitHub Pages", [r'github\.io', r'githubusercontent'])
_register("hosting", "阿里云/腾讯云", [r'aliyuncs\.com', r'myqcloud\.com', r'qcloud'])

# 清除辅助函数，避免污染模块命名空间
del _register


def detect_tech_stack(html: str, scripts: list, styles: list, headers: dict, fonts: list = None) -> dict:
    """从 HTML/脚本/样式/响应头中检测技术栈（使用预编译正则，高性能）"""
    # 初始化结果字典（用 set 去重）
    tech_sets: dict[str, set] = {
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

    # 构建搜索文本
    full = html + " " + " ".join(scripts) + " " + " ".join(styles)
    if fonts:
        full += " " + " ".join(fonts)

    # 使用预编译正则批量匹配（单次遍历）
    for compiled_re, category, name in _TECH_CHECKS:
        if name in tech_sets[category]:
            continue  # 已命中，跳过
        if compiled_re.search(full):
            tech_sets[category].add(name)

    # 服务端检测（响应头）
    server = headers.get("server") or headers.get("Server") or ""
    if server:
        tech_sets["server"].add(server)
    powered = headers.get("x-powered-by") or headers.get("X-Powered-By") or ""
    if powered:
        tech_sets["server"].add(powered)

    # CDN/代理检测（响应头）
    if headers.get("cf-ray") or headers.get("CF-Ray"):
        tech_sets["cdn"].add("Cloudflare")

    # 字体检测
    if fonts:
        for f in fonts:
            if "googleapis" in f or "gstatic" in f or "fonts.googleapis" in f:
                tech_sets["fonts"].add("Google Fonts")

    # 转换 set → list，清理空分类
    return {k: sorted(v) for k, v in tech_sets.items() if v}


def _count_re(pattern: str, text: str) -> int:
    try:
        return len(re.findall(pattern, text or "", re.I))
    except Exception:
        return 0


def build_gsap_implementation_profile(website_data: dict) -> dict:
    """构建 GSAP 实现画像（调用模式 + ScrollTrigger 配置分布 + 页面分层）。"""
    runtime = website_data.get("runtime_animation", {}) or {}
    tech = website_data.get("tech_stack", {}) or {}
    html = website_data.get("_raw_html", "") or ""
    scripts = "\n".join(website_data.get("scripts", []) or [])
    corpus = f"{html}\n{scripts}"

    has_gsap = bool(runtime.get("gsap_version")) or ("GSAP" in ((tech.get("animation_libraries", []) or [])))
    counts = {
        "gsap_to": _count_re(r"gsap\s*\.\s*to\s*\(", corpus),
        "gsap_from": _count_re(r"gsap\s*\.\s*from\s*\(", corpus),
        "gsap_fromto": _count_re(r"gsap\s*\.\s*fromTo\s*\(", corpus),
        "gsap_timeline": _count_re(r"gsap\s*\.\s*timeline\s*\(", corpus),
        "gsap_set": _count_re(r"gsap\s*\.\s*set\s*\(", corpus),
        "gsap_register_plugin": _count_re(r"gsap\s*\.\s*registerPlugin\s*\(", corpus),
        "gsap_match_media": _count_re(r"gsap\s*\.\s*matchMedia\s*\(", corpus),
        "gsap_context": _count_re(r"gsap\s*\.\s*context\s*\(", corpus),
    }

    st = {
        "instances": int(runtime.get("scrolltrigger_instances", 0) or 0),
        "with_scrub": int(runtime.get("scrolltrigger_scrub_count", 0) or 0),
        "with_pin": int(runtime.get("scrolltrigger_pin_count", 0) or 0),
        "with_snap": int(runtime.get("scrolltrigger_snap_count", 0) or 0),
        "with_toggle_actions": int(runtime.get("scrolltrigger_toggle_actions_count", 0) or 0),
        "with_markers": int(runtime.get("scrolltrigger_markers_count", 0) or 0),
        "scrub_pin_combo": int(runtime.get("scrolltrigger_scrub_pin_combo_count", 0) or 0),
        "start_top_top": int(runtime.get("scrolltrigger_start_top_top_count", 0) or 0),
        "start_top_bottom": int(runtime.get("scrolltrigger_start_top_bottom_count", 0) or 0),
        "start_top_center": int(runtime.get("scrolltrigger_start_top_center_count", 0) or 0),
        "start_other": int(runtime.get("scrolltrigger_start_other_count", 0) or 0),
        "end_plus_eq": int(runtime.get("scrolltrigger_end_plus_eq_count", 0) or 0),
        "end_bottom_top": int(runtime.get("scrolltrigger_end_bottom_top_count", 0) or 0),
        "end_other": int(runtime.get("scrolltrigger_end_other_count", 0) or 0),
        "above_fold": int(runtime.get("scrolltrigger_above_fold_count", 0) or 0),
        "mid_fold": int(runtime.get("scrolltrigger_mid_fold_count", 0) or 0),
        "deep_fold": int(runtime.get("scrolltrigger_deep_fold_count", 0) or 0),
    }
    hotspots = runtime.get("scrolltrigger_trigger_hotspots", []) or []

    total_tweens = counts["gsap_to"] + counts["gsap_from"] + counts["gsap_fromto"]
    if total_tweens > 0:
        mix = {
            "to_ratio": round(counts["gsap_to"] / total_tweens, 3),
            "from_ratio": round(counts["gsap_from"] / total_tweens, 3),
            "fromto_ratio": round(counts["gsap_fromto"] / total_tweens, 3),
        }
    else:
        mix = {"to_ratio": 0.0, "from_ratio": 0.0, "fromto_ratio": 0.0}

    style = "unknown"
    if counts["gsap_timeline"] >= max(3, total_tweens // 3):
        style = "timeline-driven"
    elif st["instances"] > 0 and st["with_scrub"] >= max(1, st["instances"] // 3):
        style = "scroll-driven"
    elif total_tweens > 0:
        style = "tween-driven"

    scenario = "balanced"
    if st["instances"] > 0:
        scrub_ratio = st["with_scrub"] / max(1, st["instances"])
        pin_ratio = st["with_pin"] / max(1, st["instances"])
        combo_ratio = st["scrub_pin_combo"] / max(1, st["instances"])
        if combo_ratio >= 0.35 and scrub_ratio >= 0.6:
            scenario = "storytelling-scrollytelling"
        elif scrub_ratio >= 0.6:
            scenario = "scroll-scrub-heavy"
        elif pin_ratio >= 0.4:
            scenario = "pin-section-heavy"
        elif st["with_snap"] >= max(2, st["instances"] // 3):
            scenario = "snap-navigation"

    actions = []
    if st["instances"] > 0 and st["with_markers"] > 0:
        actions.append("上线前关闭 ScrollTrigger markers，避免调试标记进入生产环境")
    if st["instances"] > 0 and st["scrub_pin_combo"] >= max(4, st["instances"] // 2):
        actions.append("scrub+pin 组合占比高，建议检查低端设备滚动卡顿并分段初始化")
    if counts["gsap_timeline"] == 0 and total_tweens >= 12:
        actions.append("Tween 调用较分散，建议用 timeline 分组管理以降低维护成本")
    if st["instances"] > 0 and st["with_toggle_actions"] == 0 and st["with_scrub"] < st["instances"]:
        actions.append("部分 ScrollTrigger 缺少 toggleActions/scrub，建议统一进入/离开行为策略")
    if st["instances"] > 0 and st["above_fold"] >= max(3, st["instances"] // 2):
        actions.append("首屏 ScrollTrigger 密度偏高，建议合并首屏动画时间线，减少首屏并发触发")
    if st["instances"] > 0 and st["deep_fold"] >= max(4, st["instances"] // 2):
        actions.append("深层区段 ScrollTrigger 较多，建议在进入视口前惰性初始化以降低主线程负担")

    total_layers = max(1, st["above_fold"] + st["mid_fold"] + st["deep_fold"])
    layer_distribution = {
        "above_fold_ratio": round(st["above_fold"] / total_layers, 3),
        "mid_fold_ratio": round(st["mid_fold"] / total_layers, 3),
        "deep_fold_ratio": round(st["deep_fold"] / total_layers, 3),
    }

    return {
        "gsap_detected": has_gsap,
        "gsap_version": runtime.get("gsap_version", ""),
        "call_counts": counts,
        "scrolltrigger_profile": st,
        "tween_mix": mix,
        "implementation_style": style,
        "scenario_profile": scenario,
        "layer_distribution": layer_distribution,
        "trigger_hotspots": hotspots[:5],
        "optimization_actions": actions,
    }


def append_gsap_implementation_brief(report: str, website_data: dict) -> str:
    """追加 GSAP 实现画像摘要。"""
    profile = build_gsap_implementation_profile(website_data)
    if not profile.get("gsap_detected"):
        return report

    st = profile.get("scrolltrigger_profile", {}) or {}
    counts = profile.get("call_counts", {}) or {}
    mix = profile.get("tween_mix", {}) or {}
    lines = [
        "\n\n## 🧭 GSAP 实现方案画像（系统自动生成）",
        "",
        f"- 实现风格: `{profile.get('implementation_style', 'unknown')}`",
        f"- 场景画像: `{profile.get('scenario_profile', 'balanced')}`",
        f"- GSAP 版本: `{profile.get('gsap_version', 'unknown')}`",
        f"- Tween 调用统计: `to={counts.get('gsap_to', 0)}` / `from={counts.get('gsap_from', 0)}` / `fromTo={counts.get('gsap_fromto', 0)}` / `timeline={counts.get('gsap_timeline', 0)}`",
        f"- Tween 结构占比: `to={mix.get('to_ratio', 0):.3f}` / `from={mix.get('from_ratio', 0):.3f}` / `fromTo={mix.get('fromto_ratio', 0):.3f}`",
        f"- ScrollTrigger 画像: `instances={st.get('instances', 0)}` / `scrub={st.get('with_scrub', 0)}` / `pin={st.get('with_pin', 0)}` / `scrub+pin={st.get('scrub_pin_combo', 0)}` / `snap={st.get('with_snap', 0)}` / `toggleActions={st.get('with_toggle_actions', 0)}`",
        f"- Start 分布: `top-top={st.get('start_top_top', 0)}` / `top-bottom={st.get('start_top_bottom', 0)}` / `top-center={st.get('start_top_center', 0)}` / `other={st.get('start_other', 0)}`",
        f"- End 分布: `+=x={st.get('end_plus_eq', 0)}` / `bottom-top={st.get('end_bottom_top', 0)}` / `other={st.get('end_other', 0)}`",
        f"- 页面分层: `首屏={st.get('above_fold', 0)}` / `中段={st.get('mid_fold', 0)}` / `深层={st.get('deep_fold', 0)}`",
    ]
    hotspots = profile.get("trigger_hotspots", []) or []
    if hotspots:
        hs = " / ".join([f"{h.get('selector', 'unknown')}×{h.get('count', 0)}" for h in hotspots[:3]])
        lines.append(f"- 高频触发点: {hs}")

    actions = profile.get("optimization_actions", []) or []
    if actions:
        lines.append("- 建议动作:")
        lines.extend([f"  - {a}" for a in actions[:4]])
    return report.rstrip() + "\n" + "\n".join(lines) + "\n"


# ============================================================
#  DeepSeek AI 分析模块
# ============================================================
ANALYSIS_PROMPT = """你是一位世界顶级的网站分析师兼资深全栈工程师，拥有10年以上 Web 开发经验。请对以下网站数据进行深度专业分析。

## ⚠️ 重要原则
- **只分析实际存在的数据**，不要编造不存在的功能或内容
- **基于抓取到的 HTML、脚本名、样式名、链接结构进行推断**，明确区分"检测到"和"推测"
- 如果网站是极简页面/空白页，如实说明其现状，**不要强行夸赞**
- 所有日期、数字必须来自实际数据，**绝对禁止编造日期**
- **如果提供了"页面模块数据"，必须逐个模块深入分析其技术实现**

## 🎯 分析核心：请特别深入分析以下四个维度

### 【核心维度0】🔬 页面模块级技术剖析（最高优先级！）

**这是最重要的维度**。如果数据中包含 page_modules，请对每个模块进行逐项深度分析：

对于每个模块，输出以下内容：
- **模块名称/编号**：如 "模块1: Hero 首屏区"
- **功能定位**：该模块在页面中承担什么角色？
- **HTML 结构分析**：使用什么标签？层级结构如何？语义化程度？
- **CSS 技术**：
  - 布局方案（Flex/Grid/绝对定位/浮动）——从 flexDirection/gridTemplateColumns 字段判断
  - 背景方案（纯色/渐变/图片/视频）——从 backgroundColor/backgroundImage/hasGradient 字段判断
  - 装饰效果（阴影/圆角/边框/滤镜）——从 boxShadow/borderRadius/border 字段判断
  - CSS 类名命名规范（BEM/Atomic/Utility-first/随意命名）——从 cssClasses 字段分析
- **🎬 动画专项分析（重要！）**：
  - 是否有 CSS Animation？→ 从 animationDetail 字段读取 name/duration/easing/iteration 等具体参数
  - 是否有 CSS Transition？→ 从 transitionDetail 字段读取过渡属性和时长
  - 是否有 CSS Transform？→ 从 transformDetail 字段读取具体变换(rotate/scale/translate/skew)
  - 是否使用了 will-change 优化？→ 从 willChange 字段判断性能意识
  - 是否有滚动驱动动画的类名特征？→ hasScrollAnimClass 字段
  - 子元素动画覆盖率 → animatedChildCount 字段（占子元素总数比例）
  - 综合判断动画类型（入场/悬停/持续/滚动触发/视差/粒子）
- **内容元素**：
  - 包含哪些内容类型（图片/视频/Canvas/SVG/表单/按钮/链接）？
  - 文本长度和密度分析
- **响应式适配**：布局方案的响应式友好度
- **技术打分**：该模块的实现质量（0-10分）

### 【核心维度0.5】🎬 全站动画体系深度剖析（最高优先级！）

**这是新增的核心维度**。综合分析以下数据源，给出动画体系的完整评估：

1. **动画库检测**：从 tech_stack.animation_libraries 中查看检测到的动画库
   - GSAP 系列：GSAP/ScrollTrigger/Observer/ScrollSmoother/SplitText/Flip 等
   - CSS 动画库：animate.css/Hover.css/Magic Animations
   - 滚动动画库：AOS/WOW.js/ScrollReveal/Locomotive Scroll
   - Canvas/WebGL 动画：Three.js/Particles.js/tsparticles/Lottie/Rive
   - 其他：Framer Motion/Anime.js/Motion One/Tilt.js/Rellax/Typed.js
2. **运行时动画数据**：从 runtime_animation 字段分析
   - GSAP 版本与可用功能
   - ScrollTrigger 实例数量（如果可用）
   - ScrollTrigger 场景分布（start/end 模式、scrub+pin 组合占比）
   - 页面分层分布（首屏/中段/深层触发比例）与高频触发点
   - GSAP 商业版插件使用情况
   - 全站动画元素总数、transform 元素数、will-change 元素数
   - Lottie/Three.js/Bodymovin 运行时检测
3. **动画实施质量评估**：
   - 动画库选择的合理性（是否杀鸡用牛刀？）
   - 动画实现的专业度（缓动函数使用、性能优化）
   - 动画与品牌调性的一致性
   - 是否过度动画（动画元素占比过高？）
   - will-change 使用是否恰当（滥用 vs 精准使用）
4. **动画性能评估**：
   - 是否仅使用 GPU 加速属性（transform/opacity）？
   - 是否存在 layout-triggering 动画风险（width/height/top/left 等属性的 animation）
   - 滚动动画的性能策略（passive listener、requestAnimationFrame）
   - Canvas/WebGL 动画的性能优化迹象
5. **动画技术总结**：列出确切使用的动画技术栈组合，评价其是否专业

### 【核心维度1】🛠️ 网站开发技术与架构
- **前端构建工具链**：根据打包文件名特征（如 index-xxxxx.js）推断 Vite/Rollup/Webpack/esbuild/Turbopack
- **前端框架/库**：精确识别 React/Vue/Angular/Svelte/jQuery 及其版本线索
- **CSS 方案**：Tailwind CSS/Bootstrap/Ant Design/Element UI/Material UI/UnoCSS/WindiCSS/Styled-components
- **JS 库生态**：Lodash/Axios/Day.js/Three.js/GSAP/Chart.js/ECharts/D3.js/Swiper 等
- **后端技术**：从 Server 头、X-Powered-By、路由格式、API 路径推断 Node.js/Python/Java/Go/PHP/Nginx/Tengine/Apache
- **部署与云服务**：CDN 域名分析、Cloudflare/Vercel/Netlify/AWS/阿里云/腾讯云
- **第三方集成**：Google Analytics/百度统计/Google Tag Manager/Facebook Pixel/客服系统/支付 SDK/地图 API
- **API 调用分析**：从 network_summary 分析数据交互
- **技术架构评价**：优势、缺陷、可扩展性、可维护性、安全性评分

### 【核心维度2】👥 面向客户与目标用户
- **核心定位与业态**：品牌官网/电商/SaaS/内容平台/社区/工具/落地页
- **目标用户画像**：具体行业、职位角色、年龄段、使用场景、核心痛点
- **价值主张分析**：用户进入页面后能得到什么？解决了什么实际问题？
- **商业模式推断**：B2B/B2C/C2C、订阅制/一次性付费/广告/免费增值
- **用户转化路径**：是否有清晰的 CTA？用户下一步应该做什么？
- **信任建设**：案例展示、客户 logo、资质证明、数据背书、用户评价

### 【核心维度3】✨ 网站亮点与差异化
- **设计亮点**：配色/动效/排版/交互中有哪些眼前一亮的设计？
- **技术亮点**：有哪些技术实现方式让人印象深刻？
- **功能亮点**：哪些功能是同类网站少见的？
- **内容亮点**：独特的数据、观点或呈现方式
- **品牌辨识度**：视觉符号、品牌元素、独特调性

## 其他分析维度

### 4. 🎨 UI/UX 设计深度评估
- 整体设计风格和视觉语言一致性
- 色彩体系分析（从模块的 backgroundColor 字段推断）
- 排版系统（字体选择、字号层级、行距、字距）
- 布局模式（网格/弹性/Flex/绝对定位）
- 交互设计质量（悬停/点击/过渡动画、微交互细节）
- 信息架构（导航逻辑、面包屑、搜索、筛选）
- 可访问性（a11y：ARIA标签、键盘导航、色彩对比度）

### 5. 📝 内容与文案策略
- 内容质量与专业度
- 信息传递效率（3秒内能否理解网站是做什么的？）
- 多媒体运用（图片质量、视频、图表、动画、3D）
- 文案水平（用户语言 vs 自嗨语言、说服力、行动号召力）
- 内容组织结构

### 6. 🚀 SEO 与技术性能
- 基础 SEO：Title/Meta Description/Keywords/H1-H6层级/Canonical/Open Graph/Twitter Card/Structured Data
- 语义化 HTML：header/main/footer/article/section/nav/aside 使用情况
- 性能评估：HTML体积/资源数量/图片格式(WebP/AVIF)/是否懒加载/代码压缩
- Core Web Vitals 预判：LCP/FID(INP)/CLS
- 移动端适配：viewport meta、媒体查询、触摸友好性
- 网络请求分析：请求总数、API 请求、第三方域名

### 7. 🔒 安全与合规
- HTTPS 部署质量（证书、HSTS、混合内容）
- 第三方资源安全（CSP 策略）
- 隐私合规（Cookie 使用、隐私政策链接、GDPR/CCPA 合规迹象）
- 表单安全

### 8. 📊 综合评分与行动建议
- **分维度评分表**（每项0-100分）：定位/技术/设计/动画/内容/SEO/性能/安全/亮点/模块实现
- **核心竞争力总结**（3-5条，实事求是不夸大）
- **按优先级排列的改进建议**（每条标注：紧急/高/中/低，预估工作量，技术难度）
- **可选的技术实施路线**（如果重建/升级，推荐的技术栈组合及理由）

## 📐 输出格式要求
- 使用 Markdown 格式，结构清晰、排版精美
- 适当使用 emoji、表格、代码块、分级标题
- 报告开头必须有 **一句话总览**
- **模块分析部分**：每个模块用独立的二级标题，包含 HTML 结构、CSS 技术、🎬动画分析、打分
- **动画体系专章**：报告中必须包含 "🎬 动画体系深度剖析" 二级标题，完整分析全站动画技术栈
- **表格中数据必须来自实际抓取结果**，不能编造
- 评分部分使用表格呈现各维度得分（新增"动画"评分维度）

---

以下是目标网站的真实数据，请开始你的专业分析。**注意：报告日期以数据中的"抓取时间"为准。**

"""


def format_modules_for_prompt(modules: list) -> str:
    """将模块数据格式化为 AI 友好的文本"""
    if not modules:
        return "（无模块数据 — 页面可能为极简页面或 SPA 空壳，内容由 JS 动态渲染）"

    lines = []
    for mod in modules:
        idx = mod.get('index', '?')
        tag = mod.get('tag', 'div')
        cls = mod.get('className', '')[:120]
        mod_id = mod.get('id', '')
        id_str = f' id="{mod_id}"' if mod_id else ''

        lines.append(f"""
### 模块 {idx}: `<{tag}{id_str} class="{cls}">`

| 属性 | 值 |
|------|-----|
| **尺寸** | {mod.get('width', '?')}×{mod.get('height', '?')}px |
| **垂直位置** | 距顶部 {mod.get('top', '?')}px |
| **display** | `{mod.get('display', '?')}` |
| **position** | `{mod.get('position', '?')}` |
| **flexDirection** | `{mod.get('flexDirection', '?')}` |
| **gridTemplateColumns** | `{mod.get('gridTemplateColumns') or '无'}` |
| **backgroundColor** | `{mod.get('backgroundColor', '?')}` |
| **backgroundImage** | `{mod.get('backgroundImage') or '无'}` |
| **padding** | `{mod.get('padding', '?')}` |
| **borderRadius** | `{mod.get('borderRadius', '?')}` |
| **boxShadow** | `{mod.get('boxShadow') or '无'}` |
| **hasGradient** | {'是' if mod.get('hasGradient') else '否'} |
| **hasAnimation** | {'是' if mod.get('hasAnimation') else '否'} |
| **hasTransform** | {'是' if mod.get('hasTransform') else '否'} |
| **hasTransition** | {'是' if mod.get('hasTransition') else '否'} |
| **willChange** | `{mod.get('willChange') or '无'}` |
| **hasScrollAnimClass** | {'是' if mod.get('hasScrollAnimClass') else '否'} |
| **动画子元素数** | {mod.get('animatedChildCount', 0)} 个 |
| **子元素数** | {mod.get('childCount', 0)} |
| **文本长度** | {mod.get('textLength', 0)} 字符 |
| **图片** | {mod.get('imgCount', 0)} 个 |
| **按钮** | {mod.get('buttonCount', 0)} 个 |
| **链接** | {mod.get('linkCount', 0)} 个 |
| **Canvas** | {mod.get('hasCanvas', False)} |
| **SVG** | {mod.get('hasSVG', False)} |
| **Video** | {mod.get('hasVideo', False)} |
| **表单** | {mod.get('hasForm', False)} |

**🎬 动画详细参数**:
""")
        # 展开 animationDetail
        anim_detail = mod.get('animationDetail')
        if anim_detail and len(anim_detail) > 0:
            for a in anim_detail[:4]:
                lines.append(f"- 动画 `{a.get('name', '?')}`: 时长={a.get('duration', '?')}, 缓动={a.get('easing', '?')}, 延迟={a.get('delay', '?')}, 重复={a.get('iteration', '?')}")
        else:
            lines.append("- （无 CSS Animation）")
        # 展开 transitionDetail
        tran_detail = mod.get('transitionDetail')
        if tran_detail and len(tran_detail) > 0:
            for t in tran_detail[:4]:
                lines.append(f"- 过渡 `{t.get('prop', '?')}`: 时长={t.get('duration', '?')}, 缓动={t.get('easing', '?')}, 延迟={t.get('delay', '?')}")
        else:
            lines.append("- （无 CSS Transition）")
        # transform
        tf = mod.get('transformDetail', '')
        if tf:
            lines.append(f"- Transform: `{tf}`")

        lines.append(f"""
**CSS 类名**: {', '.join(['`' + c + '`' for c in mod.get('cssClasses', [])[:20]]) if mod.get('cssClasses') else '（无）'}

**元素标签统计**: {json.dumps(mod.get('tagStats', {}), ensure_ascii=False)}

**内联样式**: `{mod.get('inlineStyle', '无')}`

**文本内容**: {mod.get('textContent', '（无文本）')[:600]}

**直接子元素结构**:
""")
        for child in mod.get('childElements', [])[:15]:
            lines.append(f"- `<{child['tag']}>` class=\"{child['class'][:80]}\" → {child['text'][:100]} (内含 {child['childCount']} 个子元素)")

        lines.append("")

    return "\n".join(lines)


async def analyze_with_deepseek(website_data: dict, api_key: str, model: str = "deepseek-chat") -> str:
    """使用 DeepSeek API 进行深度分析"""
    now = datetime.now()
    capture_time = now.strftime("%Y-%m-%d %H:%M:%S")
    capture_date = now.strftime("%Y年%m月%d日")

    # 构建给 AI 的数据摘要
    data_summary = f"""
## 📋 抓取元信息
- **抓取时间（真实时间，报告中必须使用此时间）**: {capture_time}
- **抓取日期**: {capture_date}
- **目标 URL**: {website_data.get('url')}
- **最终跳转 URL**: {website_data.get('final_url')}
- **域名**: {website_data.get('domain')}
- **数据来源**: {website_data.get('_source', 'requests')}（{'Playwright动态渲染' if website_data.get('_source') == 'playwright' else '静态抓取'}）
- **页面标题 `<title>`**: {website_data.get('title') or '（无标题）'}

## 🔍 SEO 与 Meta 数据
- **Meta Description**: {website_data.get('meta_description', '（缺失！严重 SEO 问题）')}
- **Meta Keywords**: {website_data.get('meta_keywords', '（缺失）')}
- **Open Graph 标签**: {json.dumps(website_data.get('og_tags', {}), ensure_ascii=False)}
- **Twitter Card 标签**: {json.dumps(website_data.get('twitter_tags', {}), ensure_ascii=False)}
- **Canonical URL**: {website_data.get('canonical', '（未设置）')}
- **Viewport**: {website_data.get('viewport', '（缺失，移动端适配未知）')}
- **Charset**: {website_data.get('charset', '（未声明）')}
- **Structured Data (JSON-LD)**: {json.dumps(website_data.get('structured_data', []), ensure_ascii=False) if website_data.get('structured_data') else '（无）'}

## 📐 页面结构
- **H1 标题** ({len(website_data.get('h1_headings', []))}个): {json.dumps(website_data.get('h1_headings', []), ensure_ascii=False) if website_data.get('h1_headings') else '（无 H1，严重 SEO 问题！）'}
- **H2 标题** ({len(website_data.get('h2_headings', []))}个): {json.dumps(website_data.get('h2_headings', []), ensure_ascii=False) if website_data.get('h2_headings') else '（无 H2）'}
- **H3-H6 标题**: {json.dumps(website_data.get('h3_h6_headings', []), ensure_ascii=False) if website_data.get('h3_h6_headings') else '（无）'}

## 📊 页面统计
```json
{json.dumps(website_data.get('page_stats', {}), ensure_ascii=False, indent=2)}
```

## 🛠️ 自动检测的技术栈
```json
{json.dumps(website_data.get('tech_stack', {}), ensure_ascii=False, indent=2)}
```

## 🎬 运行时动画检测数据
```json
{json.dumps(website_data.get('runtime_animation', {}), ensure_ascii=False, indent=2) if website_data.get('runtime_animation') else '（无运行时数据 — 可能为非 Playwright 渲染）'}
```

## 📦 JS 脚本资源（用于精确技术栈推断）
{chr(10).join(['- ' + s for s in website_data.get('scripts', [])[:15]]) if website_data.get('scripts') else '（无外部脚本）'}

## 🎨 CSS 样式资源
{chr(10).join(['- ' + s for s in website_data.get('styles', [])[:10]]) if website_data.get('styles') else '（无外部样式）'}

## 🔤 字体资源
{chr(10).join(['- ' + f for f in website_data.get('fonts', [])[:10]]) if website_data.get('fonts') else '（未检测到）'}

## 🔗 页面链接与导航结构
{chr(10).join(['- ' + l for l in website_data.get('links', [])[:30]]) if website_data.get('links') else '（页面无任何链接！用户无法导航！）'}

## 🖼 图片 Alt 文本
{chr(10).join(['- ' + img for img in website_data.get('images_alt', [])[:15]]) if website_data.get('images_alt') else '（无图片或无 Alt 文本）'}

## 🖼 图片详细信息（含尺寸、懒加载）
```json
{json.dumps(website_data.get('images_detail', [])[:15], ensure_ascii=False, indent=2)}
```

## 🌐 HTTP 响应头（服务端线索）
```
{website_data.get('response_headers_summary', '（未捕获）')}
```

## 🌍 网络请求摘要
```json
{json.dumps(website_data.get('network_summary', {}), ensure_ascii=False, indent=2) if website_data.get('network_summary') else '（无网络请求数据）'}
```

## 📝 页面文本内容（前 10000 字符，供内容分析）
{website_data.get('text_preview', '（页面无文本内容！）')}

---

## 🔬 【核心数据】页面模块逐项详情

**说明**：以下是通过浏览器渲染后提取的每个页面模块的技术细节。请对每个模块进行深度技术剖析。
**如果此部分为空，说明页面是极简页面/空白页，请如实说明。**

{format_modules_for_prompt(website_data.get('page_modules', []))}

---

**请基于以上真实数据输出完整的分析报告。报告中的日期必须使用 {capture_date}，不要编造任何其他日期。如 page_modules 不为空，报告必须包含"模块级技术剖析"章节。**
"""

    prompt = ANALYSIS_PROMPT + data_summary

    # 带重试的 API 调用
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com"
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"你是世界顶级的网站分析师兼资深全栈工程师。当前真实日期是 {capture_date}，分析报告中的日期必须使用此日期。分析必须专业、深入、基于实际数据，明确区分'检测到的'和'推测的'。对空白页/极简页面如实说明，不要编造内容。输出使用 Markdown 格式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=AI_TEMPERATURE,
                max_tokens=AI_MAX_TOKENS,
                stream=False,
                timeout=120.0,
            )

            report = response.choices[0].message.content
            report = append_gsap_implementation_brief(report, website_data)
            logger.info(f"AI 分析完成，报告长度: {len(report)} 字符")
            return report

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * attempt
                logger.warning(f"API 调用失败 (尝试 {attempt}/{MAX_RETRIES}): {e}，{wait}s 后重试...")
                await asyncio.sleep(wait)
            else:
                logger.error(f"API 调用最终失败: {e}")

    raise HTTPException(status_code=500, detail=f"DeepSeek API 调用失败（已重试 {MAX_RETRIES} 次）: {str(last_error)}")


# ============================================================
#  API 路由
# ============================================================
@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    """分析网站的主接口"""
    url = request.url.strip()
    start_time = time.time()

    # URL 格式校验
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        result = urlparse(url)
        if not result.netloc:
            raise ValueError("无效的 URL 格式")
    except Exception:
        raise HTTPException(status_code=400, detail="请输入有效的网站 URL")

    logger.info(f"开始分析: {url}")

    try:
        # 1. 先用 requests 快速抓取
        website_data = await fetch_website_requests(url)

        # 2. 检测是否为 SPA（需要动态渲染）
        if is_spa_page(website_data):
            logger.info("检测到 SPA 页面，切换到 Playwright 动态渲染")
            try:
                pw_data = await fetch_website_playwright(url)
                if pw_data and pw_data.get("_source") == "playwright":
                    website_data = pw_data
                    logger.info(f"Playwright 渲染成功，提取到 {len(pw_data.get('page_modules', []))} 个模块")
                else:
                    logger.warning("Playwright 回退到 requests 模式")
            except Exception as e:
                logger.warning(f"Playwright 启动失败: {e}，使用 requests 数据")

        if not website_data.get("title") and not website_data.get("text_preview"):
            raise HTTPException(
                status_code=400,
                detail="无法读取网站内容，请确认 URL 是否正确，或网站是否需要特殊访问方式"
            )

        # 移除大型二进制数据
        website_data.pop("screenshot_base64", None)
        website_data.pop("_raw_html", None)

        # 3. AI 分析
        report = await analyze_with_deepseek(website_data, request.api_key, request.model)

        # 4. 构建返回给前端的网站摘要数据
        gsap_profile = build_gsap_implementation_profile(website_data)
        frontend_data = {
            "title": website_data.get("title"),
            "domain": website_data.get("domain"),
            "tech_stack": website_data.get("tech_stack"),
            "page_stats": website_data.get("page_stats"),
            "meta_description": website_data.get("meta_description"),
            "og_title": website_data.get("og_tags", {}).get("title", ""),
            "og_image": website_data.get("og_tags", {}).get("image", ""),
            "response_headers": website_data.get("response_headers_summary", ""),
            "module_count": len(website_data.get("page_modules", [])),
            "source": website_data.get("_source", "requests"),
            "runtime_animation": website_data.get("runtime_animation"),
            "gsap_profile": gsap_profile,
        }

        elapsed = time.time() - start_time
        logger.info(f"分析完成: {url}，耗时 {elapsed:.1f}s，报告 {len(report)} 字符")

        return AnalyzeResponse(
            success=True,
            report=report,
            website_data=frontend_data
        )

    except HTTPException:
        raise
    except httpx.ConnectError as e:
        logger.error(f"连接失败: {url} -> {e}")
        raise HTTPException(status_code=400, detail=f"无法连接到网站: {str(e)}")
    except httpx.TimeoutException as e:
        logger.error(f"请求超时: {url} -> {e}")
        raise HTTPException(status_code=400, detail=f"网站请求超时，请检查 URL 是否正确")
    except httpx.HTTPError as e:
        logger.error(f"HTTP错误: {url} -> {e}")
        raise HTTPException(status_code=400, detail=f"网站访问失败: {str(e)}")
    except Exception as e:
        logger.exception(f"分析过程出错: {url}")
        raise HTTPException(status_code=500, detail=f"分析过程出错: {str(e)}")


# 静态文件服务
app.mount("/static", StaticFiles(directory="."), name="static")


@app.get("/")
async def root():
    return FileResponse("index.html")


# ============================================================
#  启动入口
# ============================================================
if __name__ == "__main__":
    import uvicorn
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    logger.info("=" * 60)
    logger.info("  [WebInsight] 网站深度分析工具 - DeepSeek AI")
    logger.info("  访问地址: http://localhost:8765")
    logger.info("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8765)
