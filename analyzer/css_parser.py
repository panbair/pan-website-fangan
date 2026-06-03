"""
CSS @keyframes 提取 — 通过 csstree (Node.js sidecar) 解析外部 CSS

解决痛点: 原有系统只读 computed style，无法发现 CSS 文件中定义的 @keyframes
"""
import asyncio
import json
import os
import subprocess

import httpx

from config import HTTP_TIMEOUT_SHORT, logger

SIDECAR_DIR = os.path.join(os.path.dirname(__file__), "..", "sidecars")
SIDECAR_SCRIPT = os.path.join(SIDECAR_DIR, "css-parser.mjs")


async def extract_keyframes_from_css(css_urls: list[str]) -> dict:
    """
    下载外部 CSS 文件 → csstree 解析 → 提取所有 @keyframes 定义

    Returns:
        { "https://example.com/style.css": [
            {"name": "fadeIn", "steps": [{"selector": "from", "properties": {...}}, ...]},
            ...
        ]}
    """
    results = {}

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_SHORT) as client:
        for css_url in css_urls[:15]:  # 限制 15 个文件
            try:
                resp = await client.get(css_url, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; WebInsight/1.0)"
                })
                css_text = resp.text

                # 使用子进程调用 Node.js csstree 解析器
                try:
                    proc = await asyncio.create_subprocess_exec(
                        "node", SIDECAR_SCRIPT,
                        stdin=asyncio.subprocess.PIPE,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    stdout, stderr = await proc.communicate(
                        input=css_text.encode('utf-8')
                    )

                    if proc.returncode == 0:
                        keyframes = json.loads(stdout.decode('utf-8'))
                        if keyframes:
                            results[css_url] = keyframes
                    else:
                        logger.debug(f"csstree 解析失败: {css_url}: {stderr.decode()}")

                except FileNotFoundError:
                    logger.debug("Node.js 未安装，跳过 CSS 解析")
                    break
                except Exception as e:
                    logger.debug(f"CSS 解析异常: {css_url}: {e}")

            except httpx.HTTPError as e:
                logger.debug(f"下载 CSS 失败: {css_url}: {e}")
            except Exception as e:
                logger.debug(f"处理 CSS 异常: {css_url}: {e}")

    return results


def merge_keyframes_to_modules(page_modules: list, css_keyframes: dict) -> list:
    """
    将 CSS 文件中的 @keyframes 定义与页面模块关联

    逻辑: 如果某个模块的 animationDetail 中的 name 与某个 @keyframes 名称匹配，
    则将完整的 @keyframes 定义注入到该模块的数据中
    """
    # 构建 name → definition 的映射
    all_keyframes = {}
    for css_url, definitions in css_keyframes.items():
        for kf in definitions:
            name = kf.get("name", "")
            if name:
                all_keyframes[name] = {
                    "source": css_url,
                    "definition": kf,
                }

    for mod in page_modules:
        anim_detail = mod.get("animationDetail") or []
        for anim in anim_detail:
            anim_name = anim.get("name", "")
            if anim_name in all_keyframes:
                anim["keyframe_definition"] = all_keyframes[anim_name]["definition"]
                anim["keyframe_source"] = all_keyframes[anim_name]["source"]

    return page_modules
