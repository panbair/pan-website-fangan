"""动态网站抓取 (Playwright) — 截图、模块提取、运行时动画检测"""
import asyncio
import base64
import json
import re
from urllib.parse import urlparse

import httpx

from config import (
    USER_AGENT, HTTP_TIMEOUT_SHORT, PLAYWRIGHT_TIMEOUT, PLAYWRIGHT_WAIT,
    VIEWPORT_WIDTH, VIEWPORT_HEIGHT, TEXT_PREVIEW_LENGTH_PW,
    RE_SCRIPTS_SRC, RE_STYLES_HREF, RE_FONTS_GOOGLE, RE_FONTS_FILE,
    RE_WEBP, RE_AVIF, RE_SVG,
    logger,
)
from crawler.static import _extract_important_headers, fetch_website_requests
from analyzer.animations import extract_page_modules_playwright
from analyzer.tech_stack import detect_tech_stack


# ============================================================
#  Playwright 辅助函数
# ============================================================
async def _take_screenshot(page) -> str:
    data = await page.screenshot(full_page=True, type="jpeg", quality=75)
    return base64.b64encode(data).decode()


async def _extract_page_modules(page) -> list:
    return await extract_page_modules_playwright(page)


async def _detect_runtime_animation(page) -> dict:
    return await page.evaluate(_RUNTIME_ANIMATION_JS)


async def _extract_text_content(page) -> str:
    return await page.evaluate(_TEXT_CONTENT_JS) or ""


async def _extract_links(page) -> list:
    return await page.evaluate(_LINKS_JS)


async def _extract_images_detail(page) -> list:
    return await page.evaluate(_IMAGES_DETAIL_JS)


async def _eval_meta(page, selector: str, attr: str) -> str:
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
    return await page.evaluate(_OG_TAGS_JS)


async def _eval_twitter_tags(page) -> dict:
    return await page.evaluate(_TWITTER_TAGS_JS)


async def _eval_charset(page) -> str:
    try:
        return (await page.evaluate(_CHARSET_JS)) or ""
    except Exception:
        return ""


async def _eval_structured_data(page) -> list:
    return await page.evaluate(_STRUCTURED_DATA_JS)


async def _eval_headings(page, selector: str, limit: int) -> list:
    try:
        return await page.evaluate(
            f"""(sel, lim) => Array.from(document.querySelectorAll(sel))
                .slice(0, lim).map(h => h.innerText.trim())""",
            selector, limit
        ) or []
    except Exception:
        return []


async def _count_elements(page, selector: str) -> int:
    try:
        return await page.evaluate(f"document.querySelectorAll('{selector}').length") or 0
    except Exception:
        return 0


async def _fetch_response_headers(url: str) -> tuple[dict, str]:
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SHORT, follow_redirects=True) as client:
            resp = await client.get(url, headers={"User-Agent": USER_AGENT})
            return dict(resp.headers), str(resp.url)
    except Exception:
        return {}, url


# ============================================================
#  JS 评估代码常量
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
                try { result.scrolltrigger_instances = ScrollTrigger.getAll ? ScrollTrigger.getAll().length : 'unknown'; }
                catch(e) { result.scrolltrigger_instances = 'unknown'; }
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


# ============================================================
#  主抓取函数
# ============================================================
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

            # 并发数据提取
            (
                screenshot_b64, page_modules, runtime_animation, text_content,
                links_raw, images_detail, meta_desc, meta_keywords,
                og_tags_full, twitter_tags_full, canonical, viewport, charset,
                structured_data, h1_tags, h2_tags, h3_h6_tags,
                div_count, section_count, img_count, a_count,
                form_count, button_count, video_count, canvas_count, svg_count,
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

            modern_images = {
                "webp": len(RE_WEBP.findall(html)),
                "avif": len(RE_AVIF.findall(html)),
                "svg": len(RE_SVG.findall(html)),
            }

            scripts = RE_SCRIPTS_SRC.findall(html)
            styles = RE_STYLES_HREF.findall(html)
            fonts = RE_FONTS_GOOGLE.findall(html) + RE_FONTS_FILE.findall(html)

            resp_headers, final_url_from_headers = await _fetch_response_headers(url)
            if final_url_from_headers:
                final_url = final_url_from_headers

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

            # v2.0: Web Vitals + 动画性能测量
            from crawler.web_vitals import (
                measure_web_vitals, measure_animation_fps, audit_animation_performance
            )
            web_vitals, anim_fps, anim_audit = await asyncio.gather(
                measure_web_vitals(page),
                measure_animation_fps(page),
                audit_animation_performance(page),
                return_exceptions=True,
            )

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
                # v2.0 新增: 真实性能数据
                "web_vitals": (
                    web_vitals if not isinstance(web_vitals, Exception) else {}
                ),
                "animation_fps": (
                    anim_fps if not isinstance(anim_fps, Exception) else {}
                ),
                "animation_audit": (
                    anim_audit if not isinstance(anim_audit, Exception) else {}
                ),
            }
        finally:
            await browser.close()
