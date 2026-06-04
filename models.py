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


class HealthResponse(BaseModel):
    status: str
    version: str
    modules: dict[str, bool]


class CacheInfo(BaseModel):
    size: int
    keys: list[str]


class CacheClearResponse(BaseModel):
    success: bool
    cleared: int
    message: str


class PlanReportItem(BaseModel):
    title: str = ""
    domain: str = ""
    report: str = ""


class PlanGenerateRequest(BaseModel):
    reports: list[PlanReportItem]
    api_key: str = ""
    model: str = "deepseek-chat"
