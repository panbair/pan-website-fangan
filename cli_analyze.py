import argparse
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from glob import glob

from app import (
    analyze_with_deepseek,
    build_gsap_implementation_profile,
    build_gsap_layer_portrait,
    derive_architecture_hints,
    fetch_website_playwright,
    fetch_website_requests,
    normalize_url,
)


def _safe_domain(url: str) -> str:
    domain = urlparse(url).netloc or "website"
    return domain.replace(":", "_")


def _now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _unique_path(path: Path) -> Path:
    """若目标文件已存在，自动追加序号避免覆盖。"""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    for i in range(1, 1000):
        candidate = path.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"Cannot allocate unique path for {path}")


def _build_no_ai_markdown(data: dict) -> str:
    hints = derive_architecture_hints(data)
    tech = data.get("tech_stack", {}) or {}
    page_stats = data.get("page_stats", {}) or {}
    gsap_profile = data.get("gsap_profile", {}) or {}
    gsap_layer_portrait = data.get("gsap_layer_portrait", {}) or {}

    lines = [
        f"## 网站快照分析：{data.get('domain', 'unknown')}",
        "",
        f"- 抓取来源：`{data.get('_source', 'requests')}`",
        f"- 页面标题：`{data.get('title') or '（无）'}`",
        f"- 模块数量：`{len(data.get('page_modules', []) or [])}`",
        f"- HTML 体积：`{page_stats.get('html_size_kb', 0)} KB`",
        f"- 混合架构推断：`{hints.get('likely_mixed_architecture')}`（置信度 `{hints.get('mixed_architecture_confidence')}`）",
        "",
        "### 技术栈",
        "```json",
        json.dumps(tech, ensure_ascii=False, indent=2),
        "```",
        "",
        "### 页面统计",
        "```json",
        json.dumps(page_stats, ensure_ascii=False, indent=2),
        "```",
        "",
        "### GSAP 实现方案画像",
        "```json",
        json.dumps(gsap_profile, ensure_ascii=False, indent=2),
        "```",
        "",
        "### GSAP 页面分层画像",
        "```json",
        json.dumps(gsap_layer_portrait, ensure_ascii=False, indent=2),
        "```",
    ]
    return "\n".join(lines)


def _build_compare_markdown(left: dict, right: dict) -> str:
    l_name = left.get("domain") or left.get("url")
    r_name = right.get("domain") or right.get("url")

    l_tech = left.get("tech_stack", {}) or {}
    r_tech = right.get("tech_stack", {}) or {}

    def as_set(d: dict, key: str) -> set:
        return set(d.get(key, []) or [])

    l_frameworks = as_set(l_tech, "frameworks")
    r_frameworks = as_set(r_tech, "frameworks")

    l_anim = as_set(l_tech, "animation_libraries")
    r_anim = as_set(r_tech, "animation_libraries")

    l_stats = left.get("page_stats", {}) or {}
    r_stats = right.get("page_stats", {}) or {}

    lines = [
        f"## 竞品对比：{l_name} vs {r_name}",
        "",
        "| 维度 | 左侧 | 右侧 |",
        "|---|---|---|",
        f"| 标题 | {left.get('title') or '（无）'} | {right.get('title') or '（无）'} |",
        f"| 抓取来源 | {left.get('_source', 'requests')} | {right.get('_source', 'requests')} |",
        f"| HTML 体积(KB) | {l_stats.get('html_size_kb', 0)} | {r_stats.get('html_size_kb', 0)} |",
        f"| 图片数 | {l_stats.get('image_count', l_stats.get('img_count', 0))} | {r_stats.get('image_count', r_stats.get('img_count', 0))} |",
        f"| 链接数 | {l_stats.get('link_count', l_stats.get('a_count', 0))} | {r_stats.get('link_count', r_stats.get('a_count', 0))} |",
        "",
        "### 前端框架差异",
        f"- 左侧独有：{', '.join(sorted(l_frameworks - r_frameworks)) or '无'}",
        f"- 右侧独有：{', '.join(sorted(r_frameworks - l_frameworks)) or '无'}",
        "",
        "### 动画库差异",
        f"- 左侧独有：{', '.join(sorted(l_anim - r_anim)) or '无'}",
        f"- 右侧独有：{', '.join(sorted(r_anim - l_anim)) or '无'}",
    ]
    return "\n".join(lines)


def _metric_page_size_kb(data: dict) -> float:
    return float((data.get("page_stats", {}) or {}).get("html_size_kb", 0) or 0)


def _metric_module_count(data: dict) -> int:
    return len(data.get("page_modules", []) or [])


def _metric_anim_count(data: dict) -> int:
    runtime = data.get("runtime_animation", {}) or {}
    return int(runtime.get("total_animated_elements", 0) or 0)


def _collect_tech_flat(data: dict) -> set:
    tech = data.get("tech_stack", {}) or {}
    tags = set()
    for key in ("build_tools", "frameworks", "libraries", "animation_libraries", "cms", "analytics", "cdn", "css_framework", "hosting"):
        for item in tech.get(key, []) or []:
            tags.add(f"{key}:{item}")
    return tags


def _find_previous_baseline(output_dir: Path, domain: str, current_json_path: Path) -> Path | None:
    pattern = str(output_dir / f"analysis-{domain}-*.json")
    candidates = sorted(glob(pattern))
    prev = [Path(p) for p in candidates if Path(p).resolve() != current_json_path.resolve()]
    if not prev:
        return None
    prev.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return prev[0]


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_change_summary(current: dict, baseline: dict, threshold: float) -> dict:
    """构建变化摘要并计算告警级别。"""
    cur_size = _metric_page_size_kb(current)
    base_size = _metric_page_size_kb(baseline)
    cur_modules = _metric_module_count(current)
    base_modules = _metric_module_count(baseline)
    cur_anim = _metric_anim_count(current)
    base_anim = _metric_anim_count(baseline)

    size_delta_pct = 0.0 if base_size == 0 else ((cur_size - base_size) / base_size)
    module_delta = cur_modules - base_modules
    anim_delta_pct = 0.0 if base_anim == 0 else ((cur_anim - base_anim) / base_anim)

    cur_tech = _collect_tech_flat(current)
    base_tech = _collect_tech_flat(baseline)
    added = sorted(cur_tech - base_tech)
    removed = sorted(base_tech - cur_tech)

    # 简单可解释评分：越大说明变化越显著
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


def build_change_markdown(url: str, baseline_path: Path, summary: dict) -> str:
    m = summary.get("metrics", {})
    t = summary.get("tech_stack_changes", {})
    return "\n".join([
        f"## 变化检测：{url}",
        "",
        f"- 基线文件：`{baseline_path.name}`",
        f"- 告警级别：`{summary.get('severity')}`",
        f"- 变化分数：`{summary.get('change_score')}`（阈值 `{summary.get('threshold')}`）",
        "",
        "| 指标 | 基线 | 当前 | 变化 |",
        "|---|---:|---:|---:|",
        f"| HTML体积(KB) | {m.get('html_size_kb', {}).get('baseline', 0)} | {m.get('html_size_kb', {}).get('current', 0)} | {m.get('html_size_kb', {}).get('delta_pct', 0)} |",
        f"| 模块数量 | {m.get('module_count', {}).get('baseline', 0)} | {m.get('module_count', {}).get('current', 0)} | {m.get('module_count', {}).get('delta', 0)} |",
        f"| 动画元素 | {m.get('animated_elements', {}).get('baseline', 0)} | {m.get('animated_elements', {}).get('current', 0)} | {m.get('animated_elements', {}).get('delta_pct', 0)} |",
        "",
        "### 技术栈变化",
        f"- 新增：{', '.join(t.get('added', [])) or '无'}",
        f"- 移除：{', '.join(t.get('removed', [])) or '无'}",
    ])


def apply_alert_policy(summary: dict, policy: dict) -> str:
    """根据 severity 和策略映射选择动作。"""
    severity = (summary or {}).get("severity", "low")
    return (policy or {}).get(severity, "none")


async def _fetch(url: str, mode: str) -> dict:
    return await _fetch_with_interaction(url, mode, "standard", True)


async def _fetch_with_interaction(url: str, mode: str, interaction_level: str, click_whitelist: bool) -> dict:
    if mode == "standard":
        data = await fetch_website_playwright(
            url,
            interaction_level=interaction_level,
            click_whitelist=click_whitelist,
        )
        data["_source"] = data.get("_source", "playwright")
        data["gsap_profile"] = build_gsap_implementation_profile(data)
        data["gsap_layer_portrait"] = build_gsap_layer_portrait(data)
        return data
    data = await fetch_website_requests(url)
    data["_source"] = data.get("_source", "requests")
    data["gsap_profile"] = build_gsap_implementation_profile(data)
    data["gsap_layer_portrait"] = build_gsap_layer_portrait(data)
    return data


async def run(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    url = normalize_url(args.url.strip())
    stamp = _now_stamp()
    domain = _safe_domain(url)

    website_data = await _fetch_with_interaction(url, args.mode, args.interaction_level, args.click_whitelist)

    if args.compare_url:
        compare_url = normalize_url(args.compare_url.strip())
        compare_data = await _fetch_with_interaction(compare_url, args.mode, args.interaction_level, args.click_whitelist)
        compare_md = _build_compare_markdown(website_data, compare_data)

        compare_path = _unique_path(output_dir / f"compare-{_safe_domain(url)}-vs-{_safe_domain(compare_url)}-{stamp}.md")
        compare_path.write_text(compare_md, encoding="utf-8")

        compare_json = {
            "left": website_data,
            "right": compare_data,
            "created_at": datetime.now().isoformat(),
        }
        _unique_path(output_dir / f"compare-{_safe_domain(url)}-vs-{_safe_domain(compare_url)}-{stamp}.json").write_text(
            json.dumps(compare_json, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(f"[OK] 对比报告已生成: {compare_path}")
        return 0

    report_md: str
    if args.no_ai:
        report_md = _build_no_ai_markdown(website_data)
    else:
        api_key = args.api_key or os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            print("[ERROR] 未提供 API Key。请使用 --api-key 或设置环境变量 DEEPSEEK_API_KEY")
            return 2
        report_md = await analyze_with_deepseek(
            website_data,
            api_key,
            args.model,
            enable_vision=args.enable_vision,
            vision_max_images=args.vision_max_images,
        )

    md_path = _unique_path(output_dir / f"analysis-{domain}-{stamp}.md")
    json_path = _unique_path(output_dir / f"analysis-{domain}-{stamp}.json")

    md_path.write_text(report_md, encoding="utf-8")
    json_path.write_text(json.dumps(website_data, ensure_ascii=False, indent=2), encoding="utf-8")

    alert_summary = None
    baseline_path = Path(args.baseline_json) if args.baseline_json else None
    if not baseline_path:
        baseline_path = _find_previous_baseline(output_dir, domain, json_path)

    if baseline_path and baseline_path.exists():
        baseline_data = _load_json(baseline_path)
        alert_summary = build_change_summary(website_data, baseline_data, args.alert_threshold)
        policy = {
            "high": args.on_high,
            "medium": args.on_medium,
            "low": args.on_low,
        }
        selected_action = apply_alert_policy(alert_summary, policy)
        alert_summary["policy"] = policy
        alert_summary["selected_action"] = selected_action
        diff_markdown = build_change_markdown(url, baseline_path, alert_summary)
        diff_path = output_dir / f"analysis-{domain}-{stamp}-diff.md"
        diff_json_path = output_dir / f"analysis-{domain}-{stamp}-diff.json"
        diff_path = _unique_path(diff_path)
        diff_json_path = _unique_path(diff_json_path)
        diff_path.write_text(diff_markdown, encoding="utf-8")
        diff_json_path.write_text(json.dumps(alert_summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] 变化检测报告已生成: {diff_path}")
        print(f"[OK] 变化检测数据已保存: {diff_json_path}")

        if args.alert_file:
            Path(args.alert_file).write_text(json.dumps(alert_summary, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[OK] 告警文件已写入: {args.alert_file}")

    print(f"[OK] 分析报告已生成: {md_path}")
    print(f"[OK] 原始数据已保存: {json_path}")
    if alert_summary and alert_summary.get("selected_action") == "fail":
        print("[ALERT] 告警策略命中 fail，返回非零退出码")
        return 3
    if alert_summary and args.fail_on_alert and alert_summary.get("severity") == "high":
        print("[ALERT] 兼容参数 --fail-on-alert 命中 high，返回非零退出码")
        return 3
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WebInsight CLI: 单站分析 / 竞品对比")
    parser.add_argument("--url", required=True, help="目标网站 URL")
    parser.add_argument("--compare-url", default="", help="可选：第二个 URL，用于竞品对比")
    parser.add_argument("--mode", choices=["quick", "standard"], default="quick", help="quick=requests, standard=playwright")
    parser.add_argument("--model", default="deepseek-chat", help="DeepSeek 模型名称")
    parser.add_argument("--api-key", default="", help="DeepSeek API Key")
    parser.add_argument("--enable-vision", action="store_true", help="启用视觉模型（截图分析）")
    parser.add_argument("--interaction-level", choices=["off", "basic", "standard"], default="standard", help="交互模拟级别")
    parser.add_argument("--vision-max-images", type=int, default=3, help="视觉模型最多使用截图数量（1-8）")
    parser.add_argument("--click-whitelist", action="store_true", default=True, help="仅点击白名单目标（CTA/导航）")
    parser.add_argument("--no-click-whitelist", action="store_false", dest="click_whitelist", help="关闭点击白名单")
    parser.add_argument("--no-ai", action="store_true", help="仅生成规则快照，不调用 AI")
    parser.add_argument("--output-dir", default="结果", help="输出目录")
    parser.add_argument("--baseline-json", default="", help="可选：指定基线 JSON（用于变化检测）")
    parser.add_argument("--alert-threshold", type=float, default=0.35, help="变化检测阈值，默认 0.35")
    parser.add_argument("--fail-on-alert", action="store_true", help="当变化级别=high时返回非零退出码")
    parser.add_argument("--alert-file", default="", help="可选：输出告警 JSON 文件路径")
    parser.add_argument("--on-high", choices=["none", "warn", "issue", "fail"], default="issue", help="high 告警动作")
    parser.add_argument("--on-medium", choices=["none", "warn", "issue", "fail"], default="warn", help="medium 告警动作")
    parser.add_argument("--on-low", choices=["none", "warn", "issue", "fail"], default="none", help="low 告警动作")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())








