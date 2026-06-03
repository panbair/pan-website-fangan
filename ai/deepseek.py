"""DeepSeek AI 分析 — 带重试 + 流式输出"""
import asyncio
import json
from datetime import datetime
from typing import AsyncGenerator

from fastapi import HTTPException
from openai import OpenAI

from config import (
    DEEPSEEK_BASE_URL, AI_MAX_TOKENS, AI_TEMPERATURE,
    MAX_RETRIES, RETRY_DELAY, logger,
)
from ai.prompts import ANALYSIS_PROMPT, build_data_summary


async def analyze_with_deepseek(website_data: dict, api_key: str, model: str = "deepseek-chat") -> str:
    """使用 DeepSeek API 进行深度分析（带重试）"""
    now = datetime.now()
    capture_time = now.strftime("%Y-%m-%d %H:%M:%S")
    capture_date = now.strftime("%Y年%m月%d日")

    data_summary = build_data_summary(website_data, capture_time, capture_date)
    prompt = ANALYSIS_PROMPT + data_summary

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client = OpenAI(
                api_key=api_key,
                base_url=DEEPSEEK_BASE_URL,
            )

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"你是世界顶级的网站分析师兼资深全栈工程师。"
                            f"当前真实日期是 {capture_date}，分析报告中的日期必须使用此日期。"
                            f"分析必须专业、深入、基于实际数据，明确区分'检测到的'和'推测的'。"
                            f"对空白页/极简页面如实说明，不要编造内容。输出使用 Markdown 格式。"
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=AI_TEMPERATURE,
                max_tokens=AI_MAX_TOKENS,
                stream=False,
                timeout=120.0,
            )

            report = response.choices[0].message.content
            logger.info(f"AI 分析完成，报告长度: {len(report)} 字符")
            return report

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * attempt
                logger.warning(f"API 调用失败 (尝试 {attempt}/{MAX_RETRIES}): {e}，{wait}s 后重试...")
                await asyncio.sleep(wait)
            else:
                logger.error(f"API 调用最终失败: {e}")

    raise HTTPException(
        status_code=500,
        detail=f"DeepSeek API 调用失败（已重试 {MAX_RETRIES} 次）: {str(last_error)}"
    )


async def analyze_stream(website_data: dict, api_key: str, model: str = "deepseek-chat") -> AsyncGenerator[str, None]:
    """流式 AI 分析 — 通过 SSE 逐步返回结果"""
    now = datetime.now()
    capture_date = now.strftime("%Y年%m月%d日")

    data_summary = build_data_summary(
        website_data,
        now.strftime("%Y-%m-%d %H:%M:%S"),
        capture_date,
    )
    prompt = ANALYSIS_PROMPT + data_summary

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    f"你是世界顶级的网站分析师兼资深全栈工程师。"
                    f"当前真实日期是 {capture_date}。"
                    f"分析必须专业、深入、基于实际数据。输出使用 Markdown 格式。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=AI_TEMPERATURE,
        max_tokens=AI_MAX_TOKENS,
        stream=True,
        timeout=180.0,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
