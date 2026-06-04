"""WebInsight CLI — 单站分析 / 竞品对比 (v2.1 模块化)"""
import argparse
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from crawler import normalize_url, fetch_website_requests, fetch_website_playwright
from ai import analyze_with_deepseek
from analyzer import build_gsap_implementation_profile

from cli_utils import safe_domain, now_stamp, unique_path, load_json
from cli_reports import build_no_ai_markdown, build_compare_markdown, build_change_markdown
from cli_change_detection import (
    build_gsap_layer_portrait,
    build_change_summary,
    apply_alert_policy,
    find_previous_baseline,
)


# ============================================================
#  抓取调度
# ============================================================
async def _fetch_with_interaction(url: str, mode: str) -> dict:
    """统一抓取入口，附加 GSAP 画像"""
    if mode == "standard":
        data = await fetch_website_playwright(url)
        data["_source"] = data.get("_source", "playwright")
    else:
        data = await fetch_website_requests(url)
        data["_source"] = data.get("_source", "requests")

    data["gsap_profile"] = build_gsap_implementation_profile(data)
    data["gsap_layer_portrait"] = build_gsap_layer_portrait(data)
    return data


# ============================================================
#  主流程
# ============================================================
async def run(args: argparse.Namespace) -> int:
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    url = normalize_url(args.url.strip())
    stamp = now_stamp()
    domain = safe_domain(url)

    website_data = await _fetch_with_interaction(url, args.mode)

    # 竞品对比模式
    if args.compare_url:
        compare_url = normalize_url(args.compare_url.strip())
        compare_data = await _fetch_with_interaction(compare_url, args.mode)
        compare_md = build_compare_markdown(website_data, compare_data)

        compare_path = unique_path(output_dir / f"compare-{safe_domain(url)}-vs-{safe_domain(compare_url)}-{stamp}.md")
        compare_path.write_text(compare_md, encoding="utf-8")

        compare_json = {
            "left": website_data,
            "right": compare_data,
            "created_at": datetime.now().isoformat(),
        }
        unique_path(output_dir / f"compare-{safe_domain(url)}-vs-{safe_domain(compare_url)}-{stamp}.json").write_text(
            json.dumps(compare_json, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        print(f"[OK] 对比报告已生成: {compare_path}")
        return 0

    # AI 分析模式
    if args.no_ai:
        report_md = build_no_ai_markdown(website_data)
    else:
        api_key = args.api_key or os.getenv("DEEPSEEK_API_KEY", "")
        if not api_key:
            print("[ERROR] 未提供 API Key。请使用 --api-key 或设置环境变量 DEEPSEEK_API_KEY")
            return 2
        report_md = await analyze_with_deepseek(website_data, api_key, args.model)

    md_path = unique_path(output_dir / f"analysis-{domain}-{stamp}.md")
    json_path = unique_path(output_dir / f"analysis-{domain}-{stamp}.json")

    md_path.write_text(report_md, encoding="utf-8")
    json_path.write_text(json.dumps(website_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 变化检测
    alert_summary = _run_change_detection(
        website_data, url, domain, stamp, output_dir, json_path, args
    )

    print(f"[OK] 分析报告已生成: {md_path}")
    print(f"[OK] 原始数据已保存: {json_path}")

    if alert_summary and alert_summary.get("selected_action") == "fail":
        print("[ALERT] 告警策略命中 fail，返回非零退出码")
        return 3
    if alert_summary and args.fail_on_alert and alert_summary.get("severity") == "high":
        print("[ALERT] 兼容参数 --fail-on-alert 命中 high，返回非零退出码")
        return 3
    return 0


def _run_change_detection(
    website_data: dict, url: str, domain: str, stamp: str,
    output_dir: Path, json_path: Path, args: argparse.Namespace,
) -> dict | None:
    """执行变化检测（基线对比 + 告警）"""
    baseline_path = Path(args.baseline_json) if args.baseline_json else None
    if not baseline_path:
        baseline_path = find_previous_baseline(output_dir, domain, json_path)

    if not baseline_path or not baseline_path.exists():
        return None

    baseline_data = load_json(baseline_path)
    alert_summary = build_change_summary(website_data, baseline_data, args.alert_threshold)
    policy = {"high": args.on_high, "medium": args.on_medium, "low": args.on_low}
    selected_action = apply_alert_policy(alert_summary, policy)
    alert_summary["policy"] = policy
    alert_summary["selected_action"] = selected_action

    diff_md = build_change_markdown(url, baseline_path, alert_summary)
    diff_path = unique_path(output_dir / f"analysis-{domain}-{stamp}-diff.md")
    diff_json_path = unique_path(output_dir / f"analysis-{domain}-{stamp}-diff.json")
    diff_path.write_text(diff_md, encoding="utf-8")
    diff_json_path.write_text(json.dumps(alert_summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 变化检测报告已生成: {diff_path}")
    print(f"[OK] 变化检测数据已保存: {diff_json_path}")

    if args.alert_file:
        Path(args.alert_file).write_text(json.dumps(alert_summary, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[OK] 告警文件已写入: {args.alert_file}")

    return alert_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WebInsight CLI: 单站分析 / 竞品对比")
    parser.add_argument("--url", required=True, help="目标网站 URL")
    parser.add_argument("--compare-url", default="", help="可选：第二个 URL，用于竞品对比")
    parser.add_argument("--mode", choices=["quick", "standard"], default="quick",
                        help="quick=requests, standard=playwright")
    parser.add_argument("--model", default="deepseek-chat", help="DeepSeek 模型名称")
    parser.add_argument("--api-key", default="", help="DeepSeek API Key")
    parser.add_argument("--enable-vision", action="store_true", help="（已移除）视觉模型功能暂未支持")
    parser.add_argument("--no-ai", action="store_true", help="仅生成规则快照，不调用 AI")
    parser.add_argument("--output-dir", default="结果", help="输出目录")
    parser.add_argument("--baseline-json", default="", help="可选：指定基线 JSON（用于变化检测）")
    parser.add_argument("--alert-threshold", type=float, default=0.35, help="变化检测阈值，默认 0.35")
    parser.add_argument("--fail-on-alert", action="store_true", help="当变化级别=high时返回非零退出码")
    parser.add_argument("--alert-file", default="", help="可选：输出告警 JSON 文件路径")
    parser.add_argument("--on-high", choices=["none", "warn", "issue", "fail"], default="issue",
                        help="high 告警动作")
    parser.add_argument("--on-medium", choices=["none", "warn", "issue", "fail"], default="warn",
                        help="medium 告警动作")
    parser.add_argument("--on-low", choices=["none", "warn", "issue", "fail"], default="none",
                        help="low 告警动作")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return asyncio.run(run(args))


if __name__ == "__main__":
    raise SystemExit(main())
