"""Pydantic 数据模型"""
from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    url: str
    api_key: str
    model: str = "deepseek-chat"


class AnalyzeResponse(BaseModel):
    success: bool
    report: str = ""
    website_data: dict = {}
    error: str = ""
