"""GSAP 实现画像 — 从运行时数据构建调用模式 + ScrollTrigger 配置分布"""
import re


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
    """追加 GSAP 实现画像摘要到 AI 报告末尾。"""
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
