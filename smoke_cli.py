"""Tiny smoke harness for stage-3 CLI features."""

import asyncio
import os
from app import (
    _memory_rate_limit_retry_after,
    build_animation_evidence_rows,
    build_animation_evidence_summary,
    build_gsap_implementation_profile,
    build_gsap_layer_portrait,
    build_report_quality_issues,
    build_visual_scorecard,
    detect_tech_stack,
    fetch_website_requests,
    get_rate_limit_mode,
    get_history_delete_token,
    get_history_read_token,
    resolve_api_key,
)
from cli_analyze import (
    _build_compare_markdown,
    _build_no_ai_markdown,
    apply_alert_policy,
    build_change_summary,
)


async def main() -> int:
    left = await fetch_website_requests("https://example.com")
    right = await fetch_website_requests("https://example.org")

    md_single = _build_no_ai_markdown(left)
    md_compare = _build_compare_markdown(left, right)

    assert "网站快照分析" in md_single
    assert "竞品对比" in md_compare
    assert left.get("title")
    assert right.get("title")

    # 变化检测冒烟
    baseline = {
        "page_stats": {"html_size_kb": 10},
        "page_modules": [{"id": 1}],
        "runtime_animation": {"total_animated_elements": 20},
        "tech_stack": {"frameworks": ["React"]},
    }
    current = {
        "page_stats": {"html_size_kb": 25},
        "page_modules": [{"id": 1}, {"id": 2}, {"id": 3}],
        "runtime_animation": {"total_animated_elements": 90},
        "tech_stack": {"frameworks": ["React", "Next.js"]},
    }
    summary = build_change_summary(current, baseline, threshold=0.35)
    assert summary.get("severity") in {"medium", "high"}
    assert "metrics" in summary

    # 多级策略映射冒烟
    action = apply_alert_policy(summary, {"high": "issue", "medium": "warn", "low": "none"})
    assert action in {"issue", "warn", "none"}

    # 视觉评分映射冒烟
    visual_data = {
        "visual_summary": {
            "visual_scores": {
                "hierarchy": 80,
                "readability": 70,
                "cta_visibility": 65,
                "interaction_feedback": 75,
            },
            "confidence": 0.84,
            "_snapshot_count": 3,
        }
    }
    scorecard = build_visual_scorecard(visual_data)
    assert scorecard.get("available") is True
    mapped = scorecard.get("mapped_scores", {})
    assert "ui_ux" in mapped and "interaction_quality" in mapped and "conversion_visibility" in mapped

    # API Key 代理回退冒烟
    old_api_key = os.environ.get("DEEPSEEK_API_KEY")
    try:
        os.environ["DEEPSEEK_API_KEY"] = "sk-env-fallback"
        assert resolve_api_key("") == "sk-env-fallback"
        assert resolve_api_key("sk-request-key") == "sk-request-key"
    finally:
        if old_api_key is None:
            os.environ.pop("DEEPSEEK_API_KEY", None)
        else:
            os.environ["DEEPSEEK_API_KEY"] = old_api_key

    # 历史接口读写令牌回退冒烟
    old_admin = os.environ.get("WEBINSIGHT_ADMIN_TOKEN")
    old_read = os.environ.get("WEBINSIGHT_ADMIN_READ_TOKEN")
    old_delete = os.environ.get("WEBINSIGHT_ADMIN_DELETE_TOKEN")
    try:
        os.environ["WEBINSIGHT_ADMIN_TOKEN"] = "legacy-token"
        os.environ.pop("WEBINSIGHT_ADMIN_READ_TOKEN", None)
        os.environ.pop("WEBINSIGHT_ADMIN_DELETE_TOKEN", None)
        assert get_history_read_token() == "legacy-token"
        assert get_history_delete_token() == "legacy-token"

        os.environ["WEBINSIGHT_ADMIN_READ_TOKEN"] = "read-token"
        os.environ["WEBINSIGHT_ADMIN_DELETE_TOKEN"] = "delete-token"
        assert get_history_read_token() == "read-token"
        assert get_history_delete_token() == "delete-token"
    finally:
        if old_admin is None:
            os.environ.pop("WEBINSIGHT_ADMIN_TOKEN", None)
        else:
            os.environ["WEBINSIGHT_ADMIN_TOKEN"] = old_admin
        if old_read is None:
            os.environ.pop("WEBINSIGHT_ADMIN_READ_TOKEN", None)
        else:
            os.environ["WEBINSIGHT_ADMIN_READ_TOKEN"] = old_read
        if old_delete is None:
            os.environ.pop("WEBINSIGHT_ADMIN_DELETE_TOKEN", None)
        else:
            os.environ["WEBINSIGHT_ADMIN_DELETE_TOKEN"] = old_delete

    # 内存限流算法冒烟
    bucket = "test:127.0.0.1"
    now = 1000.0
    assert _memory_rate_limit_retry_after(bucket, max_count=2, window_seconds=60, now_ts=now) == 0
    assert _memory_rate_limit_retry_after(bucket, max_count=2, window_seconds=60, now_ts=now + 1) == 0
    assert _memory_rate_limit_retry_after(bucket, max_count=2, window_seconds=60, now_ts=now + 2) > 0

    # 限流模式冒烟（至少能返回受支持值）
    assert get_rate_limit_mode() in {"memory", "redis"}

    # 报告质检规则冒烟
    report_text = """
    该站检测到 1 个 h1。
    子元素动画覆盖率: 1033%。
    """
    website_data = {"h1_headings": [], "h2_headings": []}
    issues = build_report_quality_issues(report_text, website_data)
    assert len(issues) >= 2

    # 动画库识别增强冒烟
    tech = detect_tech_stack(
        html='<script src="https://cdn.jsdelivr.net/npm/lenis@1.0.0/dist/lenis.min.js"></script>'
             '<script src="https://unpkg.com/split-type"></script>'
             '<script>new ScrollMagic.Scene()</script>',
        scripts=[
            "https://cdn.jsdelivr.net/npm/lenis@1.0.0/dist/lenis.min.js",
            "https://unpkg.com/split-type",
        ],
        styles=[],
        headers={},
    )
    anim_libs = set((tech or {}).get("animation_libraries", []) or [])
    assert "Lenis" in anim_libs
    assert "SplitType" in anim_libs
    assert "ScrollMagic" in anim_libs

    # 动画证据置信度摘要冒烟
    evidence_data = {
        "tech_stack": {"animation_libraries": ["GSAP", "Lenis"]},
        "runtime_animation": {
            "gsap_version": "3.12.2",
            "lenis_detected": True,
            "scrolltrigger_instances": 5,
            "lottie_elements": 0,
        },
        "tech_detection_debug": {
            "evidence": [
                {"category": "animation_libraries", "name": "GSAP", "pattern": "gsap\\.to\\(", "source": "html/scripts/styles/fonts"},
                {"category": "animation_libraries", "name": "Lenis", "pattern": "lenis", "source": "html/scripts/styles/fonts"},
            ]
        },
        "css_keyframes_count": 2,
    }
    anim_summary = build_animation_evidence_summary(evidence_data)
    assert isinstance(anim_summary, dict)
    assert "libraries" in anim_summary
    assert "top3_high_confidence" in anim_summary
    gsap_row = next((x for x in (anim_summary.get("libraries") or []) if x.get("library") == "GSAP"), None)
    assert gsap_row is not None
    assert "evidence_paths" in gsap_row
    assert "script_hit_count" in gsap_row
    assert "false_positive_risk" in gsap_row
    detail_rows = build_animation_evidence_rows(evidence_data)
    assert isinstance(detail_rows, list)
    assert any((r.get("library") == "GSAP") for r in detail_rows)

    # GSAP 实现方案画像冒烟
    gsap_data = {
        "tech_stack": {"animation_libraries": ["GSAP", "GSAP ScrollTrigger"]},
        "runtime_animation": {
            "gsap_version": "3.12.2",
            "scrolltrigger_instances": 6,
            "scrolltrigger_scrub_count": 4,
            "scrolltrigger_pin_count": 2,
            "scrolltrigger_snap_count": 1,
            "scrolltrigger_toggle_actions_count": 3,
            "scrolltrigger_markers_count": 0,
            "scrolltrigger_scrub_pin_combo_count": 2,
            "scrolltrigger_start_top_top_count": 3,
            "scrolltrigger_start_top_bottom_count": 1,
            "scrolltrigger_start_top_center_count": 1,
            "scrolltrigger_start_other_count": 1,
            "scrolltrigger_end_plus_eq_count": 2,
            "scrolltrigger_end_bottom_top_count": 1,
            "scrolltrigger_end_other_count": 1,
            "scrolltrigger_above_fold_count": 2,
            "scrolltrigger_mid_fold_count": 3,
            "scrolltrigger_deep_fold_count": 1,
            "scrolltrigger_trigger_hotspots": [
                {"selector": "section.hero", "count": 2},
                {"selector": "section.cases", "count": 1},
            ],
        },
        "_raw_html": "<script>gsap.timeline(); gsap.to('.a',{}); gsap.fromTo('.b',{},{})</script>",
        "scripts": ["https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/gsap.min.js"],
    }
    gsap_profile = build_gsap_implementation_profile(gsap_data)
    assert gsap_profile.get("gsap_detected") is True
    assert gsap_profile.get("scrolltrigger_profile", {}).get("instances") == 6
    assert "implementation_style" in gsap_profile
    assert "scenario_profile" in gsap_profile
    assert "optimization_actions" in gsap_profile
    assert "layer_distribution" in gsap_profile
    assert "trigger_hotspots" in gsap_profile

    gsap_layer_portrait = build_gsap_layer_portrait({
        **gsap_data,
        "page_modules": [
            {"index": 1, "top": 80, "height": 900, "hasAnimation": True, "hasTransform": True, "hasTransition": True, "hasScrollAnimClass": False, "animatedChildCount": 5, "cssClasses": ["hero", "gsap-intro"], "className": "hero gsap-intro"},
            {"index": 2, "top": 1200, "height": 900, "hasAnimation": False, "hasTransform": True, "hasTransition": True, "hasScrollAnimClass": True, "animatedChildCount": 4, "cssClasses": ["story", "scrolltrigger"], "className": "story scrolltrigger"},
            {"index": 3, "top": 2400, "height": 1000, "hasAnimation": False, "hasTransform": True, "hasTransition": False, "hasScrollAnimClass": True, "animatedChildCount": 3, "cssClasses": ["pin-panel"], "className": "pin-panel"},
        ],
    })
    assert gsap_layer_portrait.get("module_count") == 3
    assert gsap_layer_portrait.get("layer_count") >= 1
    assert gsap_layer_portrait.get("dominant_layer") in {"首屏层", "中上层", "中下层", "尾屏层"}
    assert isinstance(gsap_layer_portrait.get("layer_stats"), list)

    print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))


















