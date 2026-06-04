"""CLI 报告构建 — 无AI快照 / 竞品对比 / 变化检测 Markdown"""
import json
from pathlib import Path

from cli_change_detection import derive_architecture_hints


def build_no_ai_markdown(data: dict) -> str:
    """构建无 AI 的规则快照报告"""
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


def build_compare_markdown(left: dict, right: dict) -> str:
    """构建竞品对比 Markdown"""
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


def build_change_markdown(url: str, baseline_path: Path, summary: dict) -> str:
    """构建变化检测 Markdown 报告"""
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
