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
import os
import time
from urllib.parse import urlparse

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from config import SERVER_HOST, SERVER_PORT, logger
from models import AnalyzeRequest, AnalyzeResponse, HealthResponse, CacheInfo, CacheClearResponse, PlanGenerateRequest

from crawler import fetch_website_requests, fetch_website_playwright, is_spa_page, normalize_url
from crawler.cache import analysis_cache
from analyzer.css_parser import extract_keyframes_from_css, merge_keyframes_to_modules
from analyzer.performance import run_lighthouse_audit
from ai import analyze_with_deepseek, plan_generate_with_deepseek, plan_generate_stream
from ai.deepseek import analyze_stream
from analyzer.gsap_profile import append_gsap_implementation_brief

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
    url = normalize_url(url)
    parsed = urlparse(url)
    if not parsed.netloc:
        raise HTTPException(status_code=400, detail="请输入有效的网站 URL")
    return url


def _resolve_api_key(api_key: str = "") -> str:
    """解析 API Key: 优先使用用户提供的，否则回退到环境变量 DEEPSEEK_API_KEY"""
    key = (api_key or "").strip()
    if not key:
        key = os.getenv("DEEPSEEK_API_KEY", "")
    if not key:
        raise HTTPException(
            status_code=400,
            detail="未提供 API Key，请在输入框中填写 API Key 或设置环境变量 DEEPSEEK_API_KEY",
        )
    return key


# ============================================================
#  简易历史记录存储 (内存, 服务重启后清空)
# ============================================================
_history_store: list[dict] = []
_history_counter: int = 0


async def _crawl_website(url: str) -> dict:
    """并行抓取: 静态 + Playwright 同时启动，选最优结果"""
    # 启动静态抓取（快速获得基础数据）
    static_task = asyncio.create_task(fetch_website_requests(url))

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
        logger.warning(f"Playwright 失败 ({type(e).__name__}): {e}")

    # 回退到静态数据
    if not static_data.get("title") and not static_data.get("text_preview"):
        raise HTTPException(status_code=400, detail="无法读取网站内容，请确认 URL 是否正确")

    return static_data


def _build_frontend_data(website_data: dict) -> dict:
    """构建前端展示数据"""
    from ai.prompts import _compute_data_quality_tier
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
        # v2.2 新增字段
        "data_quality": _compute_data_quality_tier(website_data),
        "architecture_hints": website_data.get("architecture_hints"),
        "gsap_profile": website_data.get("gsap_profile"),
        "alert_summary": website_data.get("alert_summary"),
        "visual_scorecard": website_data.get("visual_scorecard"),
        "animation_evidence": website_data.get("animation_evidence"),
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


async def _gather_optional(*coros) -> list:
    """并行执行，任一失败返回空字典（不中断其他任务）"""
    results = await asyncio.gather(*coros, return_exceptions=True)
    return [r if not isinstance(r, BaseException) else {} for r in results]


# ============================================================
#  API 路由
# ============================================================
@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze_website(request: AnalyzeRequest):
    """网站深度分析主接口"""
    url = _validate_url(request.url)
    api_key = _resolve_api_key(request.api_key)
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

        report = await analyze_with_deepseek(website_data, api_key, request.model)
        report = append_gsap_implementation_brief(report, website_data)

        elapsed = time.time() - start_time
        logger.info(f"分析完成: {url} ({elapsed:.1f}s, {len(report)} 字符)")

        frontend_data = _build_frontend_data(website_data)
        response = AnalyzeResponse(success=True, report=report, website_data=frontend_data)

        # 写入缓存
        analysis_cache.set(url, {"report": report, "website_data": frontend_data})

        # 写入历史记录
        _save_to_history(url, report, frontend_data)

        return response

    except HTTPException:
        raise
    except httpx.ConnectError as e:
        logger.error(f"连接失败: {url} -> {e}")
        raise HTTPException(status_code=400, detail="无法连接到网站，请确认 URL 是否正确")
    except httpx.TimeoutException as e:
        logger.error(f"请求超时: {url} -> {e}")
        raise HTTPException(status_code=400, detail="网站请求超时（30秒），请检查 URL 是否可访问")
    except httpx.HTTPError as e:
        logger.error(f"HTTP错误: {url} -> {e}")
        raise HTTPException(status_code=400, detail="网站访问失败，请确认 URL 是否正确")
    except Exception:
        logger.exception(f"分析异常: {url}")
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


# ============================================================
#  SSE 流式分析 (v2.0)
# ============================================================
@app.post("/api/analyze/stream")
async def analyze_website_stream(request: AnalyzeRequest):
    """流式分析 — SSE 实时返回 AI 分析结果"""
    url = _validate_url(request.url)
    api_key = _resolve_api_key(request.api_key)
    logger.info(f"开始流式分析: {url}")

    website_data = await _crawl_website(url)
    await _enrich_website_data(website_data, url)
    website_data.pop("screenshot_base64", None)
    website_data.pop("_raw_html", None)

    frontend_data = _build_frontend_data(website_data)

    async def event_generator():
        yield f"event: meta\ndata: {json.dumps(frontend_data, ensure_ascii=False)}\n\n"

        try:
            async for chunk in analyze_stream(website_data, api_key, request.model):
                yield f"event: text\ndata: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.exception("SSE 流式分析异常")
            err_msg = str(e)
            if "401" in err_msg or "403" in err_msg:
                err_msg = "API Key 无效或已过期，请检查后重试"
            elif "429" in err_msg:
                err_msg = "API 调用过于频繁，请稍后重试"
            elif "timeout" in err_msg.lower():
                err_msg = "AI 分析超时，请稍后重试"
            else:
                err_msg = "AI 分析服务暂时不可用，请稍后重试"
            yield f"event: error\ndata: {json.dumps({'error': err_msg}, ensure_ascii=False)}\n\n"

        yield "event: done\ndata: {}\n\n"

    # 流式完成后保存历史
    _save_to_history(url, "", frontend_data)

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
#  缓存管理
# ============================================================
@app.get("/api/cache/info", response_model=CacheInfo)
async def cache_info():
    """查看当前缓存信息"""
    stats = analysis_cache.stats()
    return CacheInfo(size=stats["size"], keys=stats["urls"])


@app.post("/api/cache/clear", response_model=CacheClearResponse)
async def clear_cache():
    """清除所有分析缓存"""
    count = analysis_cache.clear()
    logger.info(f"清除缓存: {count} 条")
    return CacheClearResponse(success=True, cleared=count, message=f"已清除 {count} 条缓存")


# ============================================================
#  历史记录存储辅助
# ============================================================
def _save_to_history(url: str, report: str, website_data: dict) -> None:
    """保存分析记录到历史（内存存储，服务重启后清空）"""
    global _history_counter
    _history_counter += 1
    tech_stack = website_data.get("tech_stack", {}) if website_data else {}
    _history_store.append({
        "id": _history_counter,
        "url": url,
        "domain": website_data.get("domain", "") if website_data else "",
        "title": website_data.get("title", "") if website_data else "",
        "tech_stack": tech_stack,
        "summary": (report or "")[:200],
        "report": report,
        "website_data": website_data,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    })
    # 只保留最近 100 条
    while len(_history_store) > 100:
        _history_store.pop(0)


# ============================================================
#  调试端点 — 返回原始抓取数据（不含 AI 分析）
# ============================================================
@app.post("/api/analyze/debug")
async def analyze_debug(request: AnalyzeRequest):
    """调试分析 — 返回原始检测数据供 Debug 面板使用"""
    url = _validate_url(request.url)
    logger.info(f"开始调试分析: {url}")

    website_data = await _crawl_website(url)
    await _enrich_website_data(website_data, url)
    website_data.pop("screenshot_base64", None)

    # 构建 debug 数据结构
    runtime_animation = website_data.get("runtime_animation", {}) or {}
    tech_stack = website_data.get("tech_stack", {}) or {}

    return {
        "url": url,
        "title": website_data.get("title", ""),
        "domain": website_data.get("domain", ""),
        "source": website_data.get("_source", "requests"),
        "page_stats": website_data.get("page_stats", {}),
        "tech_stack": tech_stack,
        "runtime_animation": runtime_animation,
        "page_modules": website_data.get("page_modules", []),
        "css_keyframes": website_data.get("css_keyframes", {}),
        "performance": website_data.get("performance", {}),
        "web_vitals": website_data.get("web_vitals", {}),
        "animation_fps": website_data.get("animation_fps", {}),
        "animation_audit": website_data.get("animation_audit", {}),
        "architecture_hints": website_data.get("architecture_hints", {}),
        "gsap_profile": website_data.get("gsap_profile", {}),
        # Debug 面板需要的字段（从现有数据映射）
        "tech_detection_debug": {
            "raw_tech_stack": tech_stack,
            "tech_stack": tech_stack,
            "evidence": [],
            "suppressions": [],
        },
        "evidence_rows": [],
        "animation_evidence": {"libraries": []},
        "animation_evidence_rows": [],
    }


# ============================================================
#  综合方案生成 API
# ============================================================
@app.post("/api/plan/generate")
async def generate_plan(request: PlanGenerateRequest):
    """综合方案生成 — 基于多份分析报告生成优化方案（批量模式）"""
    if not request.reports:
        raise HTTPException(status_code=400, detail="请至少选择一份分析报告")
    api_key = _resolve_api_key(request.api_key)
    logger.info(f"开始方案生成: {len(request.reports)} 份报告")

    reports_dicts = [r.model_dump() for r in request.reports]

    try:
        plan = await plan_generate_with_deepseek(reports_dicts, api_key, request.model)
        return {"success": True, "plan": plan}
    except HTTPException:
        raise
    except Exception:
        logger.exception("方案生成异常")
        raise HTTPException(status_code=500, detail="方案生成失败，请稍后重试")


@app.post("/api/plan/generate/stream")
async def generate_plan_stream(request: PlanGenerateRequest):
    """综合方案生成 — SSE 流式返回"""
    if not request.reports:
        raise HTTPException(status_code=400, detail="请至少选择一份分析报告")
    api_key = _resolve_api_key(request.api_key)
    logger.info(f"开始流式方案生成: {len(request.reports)} 份报告")

    reports_dicts = [r.model_dump() for r in request.reports]

    async def event_generator():
        try:
            async for chunk in plan_generate_stream(reports_dicts, api_key, request.model):
                yield f"event: text\ndata: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.exception("SSE 方案生成异常")
            err_msg = str(e)
            if "401" in err_msg or "403" in err_msg:
                err_msg = "API Key 无效或已过期，请检查后重试"
            elif "429" in err_msg:
                err_msg = "API 调用过于频繁，请稍后重试"
            elif "timeout" in err_msg.lower():
                err_msg = "方案生成超时，请稍后重试"
            else:
                err_msg = "AI 方案生成服务暂时不可用，请稍后重试"
            yield f"event: error\ndata: {json.dumps({'error': err_msg}, ensure_ascii=False)}\n\n"

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
#  历史记录 API
# ============================================================
@app.get("/api/history")
async def list_history(limit: int = 15):
    """获取分析历史记录列表"""
    items = _history_store[-limit:]
    items.reverse()
    return [
        {
            "id": item["id"],
            "url": item["url"],
            "domain": item["domain"],
            "title": item["title"],
            "tech_stack": item["tech_stack"],
            "summary": item["summary"],
            "created_at": item["created_at"],
        }
        for item in items
    ]


@app.get("/api/history/{item_id}")
async def get_history_item(item_id: int):
    """获取单条历史记录详情"""
    for item in _history_store:
        if item["id"] == item_id:
            return {
                "id": item["id"],
                "url": item["url"],
                "domain": item["domain"],
                "report": item["report"],
                "website_data": item["website_data"],
                "created_at": item["created_at"],
            }
    raise HTTPException(status_code=404, detail="历史记录不存在")


@app.delete("/api/history/{item_id}")
async def delete_history_item(item_id: int):
    """删除单条历史记录"""
    for i, item in enumerate(_history_store):
        if item["id"] == item_id:
            _history_store.pop(i)
            logger.info(f"删除历史记录: id={item_id}")
            return {"success": True, "message": "已删除"}
    raise HTTPException(status_code=404, detail="历史记录不存在")


# ============================================================
#  健康检查
# ============================================================
def _check_lighthouse() -> bool:
    """检测 Lighthouse sidecar 是否可用 (Node.js + lighthouse npm 包)"""
    import subprocess
    try:
        result = subprocess.run(
            ["node", "-e", 'require("lighthouse"); console.log("ok")'],
            capture_output=True, text=True, timeout=10,
        )
        return "ok" in result.stdout
    except Exception:
        return False


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return {
        "status": "ok",
        "version": "2.2.0",
        "modules": {
            "wappalyzer": _check_import("Wappalyzer"),
            "playwright": _check_import("playwright"),
            "lighthouse": _check_lighthouse(),
            "csstree": False,     # 需要 Node.js sidecar
            "playwright_browser": _check_playwright_browser(),
        }
    }


def _check_import(module_name: str) -> bool:
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def _check_playwright_browser() -> bool:
    """检测 Playwright 浏览器是否已安装"""
    import os as _os
    pw_dir = _os.path.expanduser("~/AppData/Local/ms-playwright")
    if _os.path.exists(pw_dir):
        for item in _os.listdir(pw_dir):
            if "chromium" in item.lower():
                return True
    return False


# ============================================================
#  静态文件 & 首页
# ============================================================
# 只暴露 index.html, 不暴露源码
@app.get("/")
async def root():
    return FileResponse("index.html")


@app.get("/favicon.ico")
async def favicon():
    """返回一个简单的 SVG favicon，避免 404"""
    from fastapi.responses import Response
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="16" fill="#6366f1"/>'
        '<text x="32" y="44" font-size="36" text-anchor="middle" fill="#fff">🔍</text>'
        '</svg>'
    )
    return Response(content=svg, media_type="image/svg+xml")


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
    logger.info("  [WebInsight v2.2] 网站深度分析工具")
    logger.info(f"  访问: http://localhost:{SERVER_PORT}")
    logger.info(f"  健康检查: http://localhost:{SERVER_PORT}/health")
    logger.info("  模块: Wappalyzer + csstree + Lighthouse + DeepSeek AI")
    logger.info("=" * 60)
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT, timeout_keep_alive=120)
