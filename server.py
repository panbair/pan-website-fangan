"""
==================================================================
  🌐 WebInsight — 网站深度分析工具 v2.0
==================================================================
  模块化架构:
  - crawler/  : 网站抓取 (httpx + Playwright 双引擎)
  - analyzer/ : 技术栈检测 / 动画分析 / CSS解析 / 性能审计
  - ai/       : DeepSeek AI 分析 + Prompt 模板
  - sidecars/ : Node.js 辅助脚本 (csstree / Lighthouse)

  启动: python server.py 或 uvicorn server:app --port 8765
==================================================================
"""
import asyncio
import json
import time
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from config import SERVER_HOST, SERVER_PORT, logger
from models import AnalyzeRequest, AnalyzeResponse

from crawler import fetch_website_requests, fetch_website_playwright, is_spa_page
from crawler.cache import analysis_cache
from crawler.web_vitals import measure_web_vitals, measure_animation_fps, audit_animation_performance
from analyzer.css_parser import extract_keyframes_from_css, merge_keyframes_to_modules
from analyzer.performance import run_lighthouse_audit
from ai import analyze_with_deepseek
from ai.deepseek import analyze_stream

# ============================================================
#  FastAPI 应用
# ============================================================
app = FastAPI(
    title="WebInsight v2",
    description="网站深度学习分析工具 — Wappalyzer + csstree + Lighthouse + DeepSeek AI",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
#  共享抓取逻辑 (避免 DRY)
# ============================================================
def _validate_url(url: str) -> str:
    """URL 校验和标准化"""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="请输入有效的网站 URL")
    return url


async def _crawl_website(url: str) -> dict:
    """并行抓取: 静态 + Playwright 同时启动，选最优结果"""
    # 启动静态抓取（快速获得基础数据）
    static_task = asyncio.create_task(fetch_website_requests(url))
    pw_task: asyncio.Task | None = None

    # 等待静态抓取完成，同时判断是否需要 Playwright
    static_data = await static_task
    logger.info(f"静态抓取完成: {static_data.get('title', 'N/A')}, "
                f"文本={static_data.get('text_length', 0)}")

    # 如果静态数据已足够好（非SPA，有内容），直接返回
    need_pw = is_spa_page(static_data)
    if not need_pw and static_data.get("text_length", 0) > 200:
        logger.info("静态数据充足，跳过 Playwright")
        return static_data

    # 需要 Playwright: 并行启动（它可能已经在后台跑了）
    logger.info(f"启动 Playwright 动态渲染 (SPA={need_pw})...")
    try:
        pw_data = await fetch_website_playwright(url)
        if pw_data and pw_data.get("_source") == "playwright":
            logger.info(f"Playwright 成功，{len(pw_data.get('page_modules', []))} 个模块")
            return pw_data
    except Exception as e:
        logger.warning(f"Playwright 失败: {e}")

    # 回退到静态数据
    if not static_data.get("title") and not static_data.get("text_preview"):
        raise HTTPException(status_code=400, detail="无法读取网站内容，请确认 URL 是否正确")

    return static_data


def _build_frontend_data(website_data: dict) -> dict:
    """构建前端展示数据"""
    return {
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
        "performance": website_data.get("performance"),
        "css_keyframes_count": (
            sum(len(v) for v in website_data.get("css_keyframes", {}).values())
            if website_data.get("css_keyframes") else 0
        ),
        "web_vitals": website_data.get("web_vitals"),
        "animation_fps": website_data.get("animation_fps"),
        "animation_audit": website_data.get("animation_audit"),
    }


async def _enrich_website_data(website_data: dict, url: str) -> None:
    """CSS 解析 + Lighthouse 审计（仅 Playwright 模式）"""
    if website_data.get("_source") != "playwright":
        return

    css_urls = website_data.get("styles", [])
    css_keyframes, performance_data = await _gather_optional(
        extract_keyframes_from_css(css_urls),
        run_lighthouse_audit(url),
    )

    if css_keyframes:
        page_modules = website_data.get("page_modules", [])
        website_data["page_modules"] = merge_keyframes_to_modules(page_modules, css_keyframes)
        website_data["css_keyframes"] = css_keyframes
        logger.info(f"CSS @keyframes: {sum(len(v) for v in css_keyframes.values())} 个")

    if performance_data and "error" not in performance_data:
        website_data["performance"] = performance_data
        logger.info(f"Lighthouse: P{performance_data.get('performance_score','?')}")


async def _gather_optional(*coros):
    """并行执行，任一失败返回空字典"""
    results = await asyncio.gather(*coros, return_exceptions=True)
    return [r if not isinstance(r, BaseException) else {} for r in results]


# ============================================================
#  API 路由
# ============================================================
@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    """网站深度分析主接口"""
    url = _validate_url(request.url)
    start_time = time.time()

    # 缓存检查
    cached = analysis_cache.get(url)
    if cached:
        return AnalyzeResponse(
            success=True,
            report=cached["report"],
            website_data=cached["website_data"],
        )

    logger.info(f"开始分析: {url}")

    try:
        website_data = await _crawl_website(url)
        await _enrich_website_data(website_data, url)

        # 清理大型数据
        website_data.pop("screenshot_base64", None)
        website_data.pop("_raw_html", None)

        report = await analyze_with_deepseek(website_data, request.api_key, request.model)

        elapsed = time.time() - start_time
        logger.info(f"分析完成: {url} ({elapsed:.1f}s, {len(report)} 字符)")

        frontend_data = _build_frontend_data(website_data)
        response = AnalyzeResponse(success=True, report=report, website_data=frontend_data)

        # 写入缓存
        analysis_cache.set(url, {"report": report, "website_data": frontend_data})

        return response

    except HTTPException:
        raise
    except httpx.ConnectError as e:
        logger.error(f"连接失败: {url} -> {e}")
        raise HTTPException(status_code=400, detail=f"无法连接到网站: {str(e)}")
    except httpx.TimeoutException as e:
        logger.error(f"请求超时: {url} -> {e}")
        raise HTTPException(status_code=400, detail=f"网站请求超时，请检查 URL")
    except httpx.HTTPError as e:
        logger.error(f"HTTP错误: {url} -> {e}")
        raise HTTPException(status_code=400, detail=f"网站访问失败: {str(e)}")
    except Exception as e:
        logger.exception(f"分析异常: {url}")
        raise HTTPException(status_code=500, detail=f"分析过程出错: {str(e)}")


# ============================================================
#  SSE 流式分析 (v2.0)
# ============================================================
@app.post("/api/analyze/stream")
async def analyze_website_stream(request: AnalyzeRequest):
    """流式分析 — SSE 实时返回 AI 分析结果"""
    url = _validate_url(request.url)
    logger.info(f"开始流式分析: {url}")

    website_data = await _crawl_website(url)
    website_data.pop("screenshot_base64", None)
    website_data.pop("_raw_html", None)

    frontend_data = _build_frontend_data(website_data)

    async def event_generator():
        yield f"event: meta\ndata: {json.dumps(frontend_data, ensure_ascii=False)}\n\n"

        try:
            async for chunk in analyze_stream(website_data, request.api_key, request.model):
                yield f"event: text\ndata: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ============================================================
#  健康检查
# ============================================================
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "version": "2.1.0",
        "modules": {
            "wappalyzer": _check_import("Wappalyzer"),
            "playwright": _check_import("playwright"),
            "lighthouse": False,  # 需要 Node.js sidecar
            "csstree": False,     # 需要 Node.js sidecar
        }
    }


def _check_import(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


# ============================================================
#  静态文件 & 首页
# ============================================================
# 只暴露 index.html, 不暴露源码
@app.get("/")
async def root():
    return FileResponse("index.html")


# ============================================================
#  启动 & 优雅关闭
# ============================================================
if __name__ == "__main__":
    import uvicorn
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # 清理旧文件
    import os
    old_app = os.path.join(os.path.dirname(__file__), "app.py")
    if os.path.exists(old_app):
        logger.info("检测到旧版 app.py，已由 server.py 替代")

    logger.info("=" * 60)
    logger.info("  [WebInsight v2.1] 网站深度分析工具")
    logger.info(f"  访问: http://localhost:{SERVER_PORT}")
    logger.info(f"  健康检查: http://localhost:{SERVER_PORT}/health")
    logger.info("  模块: Wappalyzer + csstree + Lighthouse + DeepSeek AI")
    logger.info("=" * 60)
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, timeout_keep_alive=120)
