"""静态网站抓取 (httpx)"""
import json
import re
from urllib.parse import urlparse

import httpx

from config import (
    USER_AGENT, HTTP_TIMEOUT, TEXT_PREVIEW_LENGTH,
    RE_TITLE, RE_META_DESC_1, RE_META_DESC_2,
    RE_META_KW_1, RE_META_KW_2,
    RE_OG_PROP, RE_OG_PROP_REV, RE_TWITTER,
    RE_CANONICAL, RE_VIEWPORT, RE_CHARSET, RE_JSON_LD,
    RE_LINKS, RE_IMAGES_ALT, RE_SCRIPTS_SRC, RE_STYLES_HREF,
    RE_FONTS_GOOGLE, RE_FONTS_FILE,
    RE_DIV, RE_SECTION, RE_IMG, RE_A, RE_FORM, RE_BUTTON, RE_VIDEO,
    RE_WEBP, RE_AVIF, RE_SVG,
    RE_H1, RE_H2, RE_H3, RE_H4, RE_H5, RE_H6,
    RE_CLEAN_SCRIPT, RE_CLEAN_STYLE, RE_CLEAN_TAGS, RE_CLEAN_WS,
    RE_INLINE_TAG, RE_SEMANTIC_TAG,
    logger,
)
from analyzer.tech_stack import detect_tech_stack


def _extract_important_headers(resp_headers: dict) -> dict:
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

    # ---- 提取关键信息 ----
    title_match = RE_TITLE.search(html)
    title = title_match.group(1).strip() if title_match else ""

    meta_desc = ""
    for pattern in (RE_META_DESC_1, RE_META_DESC_2):
        m = pattern.search(html)
        if m:
            meta_desc = m.group(1)
            break

    meta_keywords = ""
    for pattern in (RE_META_KW_1, RE_META_KW_2):
        m = pattern.search(html)
        if m:
            meta_keywords = m.group(1)
            break

    og_tags = dict(RE_OG_PROP.findall(html))
    if not og_tags:
        og_tags = {v: k for k, v in RE_OG_PROP_REV.findall(html)}

    twitter_tags = dict(RE_TWITTER.findall(html))

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

    structured_data = []
    for m in RE_JSON_LD.finditer(html):
        try:
            structured_data.append(json.loads(m.group(1)))
        except (json.JSONDecodeError, ValueError):
            structured_data.append(m.group(1)[:200] + "...")

    link_list = []
    for href, text in RE_LINKS.findall(html)[:50]:
        text_clean = RE_INLINE_TAG.sub('', text).strip()
        if text_clean:
            link_list.append(f"{text_clean} → {href}")

    images = [alt for alt in RE_IMAGES_ALT.findall(html)[:30] if alt.strip()]
    scripts = RE_SCRIPTS_SRC.findall(html)
    styles = RE_STYLES_HREF.findall(html)
    fonts = RE_FONTS_GOOGLE.findall(html) + RE_FONTS_FILE.findall(html)

    # 清理文本
    text_clean = RE_CLEAN_SCRIPT.sub('', html)
    text_clean = RE_CLEAN_STYLE.sub('', text_clean)
    text_clean = RE_CLEAN_TAGS.sub(' ', text_clean)
    text_clean = RE_CLEAN_WS.sub(' ', text_clean).strip()
    text_preview = text_clean[:TEXT_PREVIEW_LENGTH]

    # 技术栈检测
    tech_stack = detect_tech_stack(html, scripts, styles, resp_headers, fonts)

    # 标题
    h1_raw = [RE_INLINE_TAG.sub('', h).strip() for h in RE_H1.findall(html)[:10]]
    h2_raw = [RE_INLINE_TAG.sub('', h).strip() for h in RE_H2.findall(html)[:15]]
    h3_h6_raw = []
    for pattern in (RE_H3, RE_H4, RE_H5, RE_H6):
        h3_h6_raw.extend(
            RE_INLINE_TAG.sub('', h).strip() for h in pattern.findall(html)[:5]
        )

    # 元素统计
    element_counts = {
        "div_count": len(RE_DIV.findall(html)),
        "section_count": len(RE_SECTION.findall(html)),
        "image_count": len(RE_IMG.findall(html)),
        "link_count": len(RE_A.findall(html)),
        "form_count": len(RE_FORM.findall(html)),
        "button_count": len(RE_BUTTON.findall(html)),
        "video_count": len(RE_VIDEO.findall(html)),
    }

    # 语义化标签
    semantic_tags = {}
    for m in RE_SEMANTIC_TAG.finditer(html):
        tag = m.group(1)
        semantic_tags[tag] = semantic_tags.get(tag, 0) + 1

    important_headers = _extract_important_headers(resp_headers)

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
        "fonts": fonts,
        "tech_stack": tech_stack,
        "response_headers_summary": json.dumps(important_headers, ensure_ascii=False, indent=2),
        "page_stats": {
            **element_counts,
            "html_size_kb": round(len(html) / 1024, 1),
            "semantic_tags_used": semantic_tags,
            "modern_image_formats": modern_images,
        }
    }
