"""
性能审计 — Lighthouse 集成

获取: Performance / SEO / Accessibility / Best Practices 评分
+ Core Web Vitals (LCP / CLS / TBT)
+ 非合成动画检测 (non-composited-animations)
"""
import asyncio
import json
import os

from config import logger

SIDECAR_DIR = os.path.join(os.path.dirname(__file__), "..", "sidecars")
LIGHTHOUSE_SCRIPT = os.path.join(SIDECAR_DIR, "lighthouse.mjs")


async def run_lighthouse_audit(url: str, timeout: int = 90) -> dict:
    """
    运行 Lighthouse 审计

    Returns:
        {
            "performance_score": 85,
            "seo_score": 92,
            "accessibility_score": 78,
            "best_practices_score": 90,
            "lcp": 2500.0,         # ms
            "cls": 0.05,
            "tbt": 150.0,          # ms
            "non_composited_animations": [...],
            "diagnostics": {...},
        }
    """
    try:
        proc = await asyncio.create_subprocess_exec(
            "node", LIGHTHOUSE_SCRIPT, url,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(), timeout=timeout
        )

        if proc.returncode == 0:
            lhr = json.loads(stdout.decode('utf-8'))

            return {
                "performance_score": round(
                    lhr.get("categories", {}).get("performance", {}).get("score", 0) * 100
                ),
                "seo_score": round(
                    lhr.get("categories", {}).get("seo", {}).get("score", 0) * 100
                ),
                "accessibility_score": round(
                    lhr.get("categories", {}).get("accessibility", {}).get("score", 0) * 100
                ),
                "best_practices_score": round(
                    lhr.get("categories", {}).get("best-practices", {}).get("score", 0) * 100
                ),
                # Core Web Vitals
                "lcp": lhr.get("audits", {}).get("largest-contentful-paint", {}).get("numericValue"),
                "cls": lhr.get("audits", {}).get("cumulative-layout-shift", {}).get("numericValue"),
                "tbt": lhr.get("audits", {}).get("total-blocking-time", {}).get("numericValue"),
                # 动画相关审计
                "non_composited_animations": _extract_animation_audits(lhr),
            }
        else:
            logger.debug(f"Lighthouse 失败: {stderr.decode()[:200]}")
            return {"error": f"Lighthouse 执行失败: {stderr.decode()[:200]}"}

    except FileNotFoundError:
        logger.info("Node.js 未安装，跳过 Lighthouse 审计")
        return {"error": "Node.js 未安装"}
    except asyncio.TimeoutError:
        logger.warning(f"Lighthouse 审计超时 ({timeout}s)")
        return {"error": f"Lighthouse 审计超时 ({timeout}s)"}
    except Exception as e:
        logger.warning(f"Lighthouse 审计异常: {e}")
        return {"error": str(e)}


def _extract_animation_audits(lhr: dict) -> list:
    """提取与动画相关的审计项"""
    findings = []

    # 非合成动画检测
    audit = lhr.get("audits", {}).get("non-composited-animations")
    if audit and audit.get("details", {}).get("items"):
        for item in audit["details"]["items"]:
            findings.append({
                "type": "non_composited",
                "node": item.get("node", {}).get("snippet", "")[:200],
                "failure_reason": item.get("failureReason", ""),
            })

    # 避免大尺寸的 layout shifts
    cls_audit = lhr.get("audits", {}).get("layout-shifts")
    if cls_audit and cls_audit.get("details", {}).get("items"):
        for item in cls_audit["details"]["items"][:5]:
            if item.get("score", 0) < 0.9:
                findings.append({
                    "type": "layout_shift",
                    "node": item.get("node", {}).get("snippet", "")[:200],
                    "score": item.get("score"),
                })

    return findings
