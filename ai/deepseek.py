"""DeepSeek AI 分析 — 带重试 + 流式输出"""
import asyncio
from datetime import datetime
from typing import AsyncGenerator

from fastapi import HTTPException
from openai import OpenAI

from config import (
    DEEPSEEK_BASE_URL, AI_MAX_TOKENS, AI_TEMPERATURE,
    AI_TIMEOUT, AI_STREAM_TIMEOUT,
    MAX_RETRIES, RETRY_DELAY, logger,
)
from ai.prompts import ANALYSIS_PROMPT, build_data_summary, PLAN_GENERATION_PROMPT, build_plan_data_summary


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
                timeout=AI_TIMEOUT,
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

    # 根据错误类型返回安全的消息
    err_msg = str(last_error)
    if "401" in err_msg or "403" in err_msg or "Unauthorized" in err_msg:
        detail = "API Key 无效或已过期，请检查后重试"
    elif "429" in err_msg or "rate" in err_msg.lower():
        detail = "API 调用过于频繁，请稍后重试"
    elif "timeout" in err_msg.lower():
        detail = "AI 分析超时，请稍后重试"
    else:
        detail = "AI 分析服务暂时不可用，请稍后重试"
    raise HTTPException(status_code=500, detail=detail)


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
        timeout=AI_STREAM_TIMEOUT,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# 方案生成专用参数 — 创意方案需要极度详细 + 创意多样性
_PLAN_MAX_TOKENS = 32768  # 32K tokens — 惊艳时刻 + 逐section动画代码需要大篇幅
_PLAN_TEMPERATURE = 0.85  # 高创意温度 — 避免套路化动画

_PLAN_SYSTEM_PROMPT = """你是创意总监 + 故事叙述者 + GSAP 动画大师。

最重要的铁律：用户看完第一段必须知道这是什么网站。
方案开头必须用一句话说清楚：品牌是什么、提供什么价值、给谁用。

你设计网站像导演拍电影，但每个"场景"同时服务于两个目标：
- 🎭 故事目标：用户感受到什么情绪
- 💼 商业目标：用户学到了什么产品信息

禁止写完整篇方案都不说清楚产品/服务是什么。
内容越丰富越好，总字数 5000+。GSAP 代码零 bug。"""


async def plan_generate_with_deepseek(reports: list[dict], api_key: str, model: str = "deepseek-chat") -> str:
    """使用 DeepSeek API 基于多份报告生成综合优化方案（带重试）"""
    data_summary = build_plan_data_summary(reports)
    prompt = PLAN_GENERATION_PROMPT + data_summary

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": _PLAN_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=_PLAN_TEMPERATURE,
                max_tokens=_PLAN_MAX_TOKENS,
                stream=False,
                timeout=AI_TIMEOUT,
            )

            plan = response.choices[0].message.content
            logger.info(f"方案生成完成，长度: {len(plan)} 字符")
            return plan

        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                wait = RETRY_DELAY * attempt
                logger.warning(f"方案生成API调用失败 (尝试 {attempt}/{MAX_RETRIES}): {e}，{wait}s 后重试...")
                await asyncio.sleep(wait)
            else:
                logger.error(f"方案生成API调用最终失败: {e}")

    err_msg = str(last_error)
    if "401" in err_msg or "403" in err_msg or "Unauthorized" in err_msg:
        detail = "API Key 无效或已过期，请检查后重试"
    elif "429" in err_msg or "rate" in err_msg.lower():
        detail = "API 调用过于频繁，请稍后重试"
    elif "timeout" in err_msg.lower():
        detail = "方案生成超时，请稍后重试"
    else:
        detail = "AI 方案生成服务暂时不可用，请稍后重试"
    raise HTTPException(status_code=500, detail=detail)


async def plan_generate_stream(reports: list[dict], api_key: str, model: str = "deepseek-chat") -> AsyncGenerator[str, None]:
    """流式方案生成 — 通过 SSE 逐步返回结果"""
    data_summary = build_plan_data_summary(reports)
    prompt = PLAN_GENERATION_PROMPT + data_summary

    client = OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)

    stream = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _PLAN_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=_PLAN_TEMPERATURE,
        max_tokens=_PLAN_MAX_TOKENS,
        stream=True,
        timeout=AI_STREAM_TIMEOUT,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
