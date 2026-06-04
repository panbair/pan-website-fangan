"""CLI 变化检测 — 架构推断 / 指标计算 / 基线对比 / 告警策略"""
from pathlib import Path
from glob import glob


def derive_architecture_hints(data: dict) -> dict:
    """从抓取数据推断混合架构特征。"""
    source = data.get("_source", "requests")
    text_len = data.get("text_length", 0)
    modules = data.get("page_modules", []) or []
    spa_signals = 0
    total_signals = 0

    # 信号1: 来源是 Playwright 说明静态抓取内容不足
    if source == "playwright":
        spa_signals += 1
        total_signals += 1

    # 信号2: 文本过少
    if text_len < 500:
        total_signals += 1
        spa_signals += 1 if text_len < 200 else 0

    # 信号3: 模块极少
    if len(modules) < 3:
        total_signals += 1
        spa_signals += 1 if len(modules) < 2 else 0

    tech = data.get("tech_stack", {}) or {}
    frameworks = tech.get("frameworks", []) or []
    spa_frameworks = {"React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js", "Gatsby"}
    if any(f in spa_frameworks for f in frameworks):
        total_signals += 1
        spa_signals += 1

    confidence = round(spa_signals / max(1, total_signals), 3) if total_signals > 0 else 0.0
    return {
        "likely_mixed_architecture": confidence >= 0.5,
        "mixed_architecture_confidence": confidence,
        "spa_signals": spa_signals,
        "total_signals": total_signals,
    }


def build_gsap_layer_portrait(data: dict) -> dict:
    """构建 GSAP 页面分层画像（精简版）。"""
    runtime = data.get("runtime_animation", {}) or {}
    return {
        "above_fold": int(runtime.get("scrolltrigger_above_fold_count", 0) or 0),
        "mid_fold": int(runtime.get("scrolltrigger_mid_fold_count", 0) or 0),
        "deep_fold": int(runtime.get("scrolltrigger_deep_fold_count", 0) or 0),
        "total_animated": int(runtime.get("total_animated_elements", 0) or 0),
        "scrolltrigger_instances": int(runtime.get("scrolltrigger_instances", 0) or 0),
    }


def metric_page_size_kb(data: dict) -> float:
    """提取页面大小指标 (KB)"""
    return float((data.get("page_stats", {}) or {}).get("html_size_kb", 0) or 0)


def metric_module_count(data: dict) -> int:
    """提取模块数量"""
    return len(data.get("page_modules", []) or [])


def metric_anim_count(data: dict) -> int:
    """提取动画元素数量"""
    runtime = data.get("runtime_animation", {}) or {}
    return int(runtime.get("total_animated_elements", 0) or 0)


def collect_tech_flat(data: dict) -> set:
    """收集技术栈标签（用于差异对比）"""
    tech = data.get("tech_stack", {}) or {}
    tags = set()
    for key in ("build_tools", "frameworks", "libraries", "animation_libraries",
                "cms", "analytics", "cdn", "css_framework", "hosting"):
        for item in tech.get(key, []) or []:
            tags.add(f"{key}:{item}")
    return tags


def find_previous_baseline(output_dir: Path, domain: str, current_json_path: Path) -> Path | None:
    """查找上一次分析基线文件"""
    pattern = str(output_dir / f"analysis-{domain}-*.json")
    candidates = sorted(glob(pattern))
    prev = [Path(p) for p in candidates if Path(p).resolve() != current_json_path.resolve()]
    if not prev:
        return None
    prev.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return prev[0]


def build_change_summary(current: dict, baseline: dict, threshold: float) -> dict:
    """构建变化摘要并计算告警级别。"""
    cur_size = metric_page_size_kb(current)
    base_size = metric_page_size_kb(baseline)
    cur_modules = metric_module_count(current)
    base_modules = metric_module_count(baseline)
    cur_anim = metric_anim_count(current)
    base_anim = metric_anim_count(baseline)

    size_delta_pct = 0.0 if base_size == 0 else ((cur_size - base_size) / base_size)
    module_delta = cur_modules - base_modules
    anim_delta_pct = 0.0 if base_anim == 0 else ((cur_anim - base_anim) / base_anim)

    cur_tech = collect_tech_flat(current)
    base_tech = collect_tech_flat(baseline)
    added = sorted(cur_tech - base_tech)
    removed = sorted(base_tech - cur_tech)

    size_score = min(1.0, abs(size_delta_pct) / 0.5)
    module_score = min(1.0, abs(module_delta) / 8.0)
    anim_score = min(1.0, abs(anim_delta_pct) / 0.6)
    tech_score = min(1.0, (len(added) + len(removed)) / 10.0)
    change_score = round(size_score * 0.25 + module_score * 0.25 + anim_score * 0.2 + tech_score * 0.3, 3)

    if change_score >= threshold:
        severity = "high"
    elif change_score >= max(0.05, threshold * 0.5):
        severity = "medium"
    else:
        severity = "low"

    return {
        "severity": severity,
        "threshold": threshold,
        "change_score": change_score,
        "metrics": {
            "html_size_kb": {"baseline": base_size, "current": cur_size, "delta_pct": round(size_delta_pct, 4)},
            "module_count": {"baseline": base_modules, "current": cur_modules, "delta": module_delta},
            "animated_elements": {"baseline": base_anim, "current": cur_anim, "delta_pct": round(anim_delta_pct, 4)},
        },
        "tech_stack_changes": {
            "added": added,
            "removed": removed,
            "total": len(added) + len(removed),
        },
    }


def apply_alert_policy(summary: dict, policy: dict) -> str:
    """根据告警策略返回动作"""
    severity = (summary or {}).get("severity", "low")
    return (policy or {}).get(severity, "none")
