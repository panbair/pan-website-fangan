"""Tiny smoke harness for app-level GSAP profile paths."""
import asyncio
from app import (
    build_gsap_implementation_profile,
    detect_tech_stack,
    fetch_website_requests,
)
async def main() -> int:
    left = await fetch_website_requests("https://example.com")
    assert left.get("title")
    assert left.get("domain")
    tech = detect_tech_stack(
        html='<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/gsap.min.js"></script>'
             '<script>gsap.to(".a", {})</script>',
        scripts=["https://cdn.jsdelivr.net/npm/gsap@3.12.2/dist/gsap.min.js"],
        styles=[],
        headers={},
    )
    anim_libs = set((tech or {}).get("animation_libraries", []) or [])
    assert "GSAP" in anim_libs
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
    print("SMOKE_OK")
    return 0
if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
