"""CLI 工具函数 — URL 处理、文件 IO、时间戳"""
import json
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def safe_domain(url: str) -> str:
    """从 URL 提取安全域名（替换冒号等特殊字符）"""
    domain = urlparse(url).netloc or "website"
    return domain.replace(":", "_")


def now_stamp() -> str:
    """当前日期戳 YYYY-MM-DD"""
    return datetime.now().strftime("%Y-%m-%d")


def unique_path(path: Path) -> Path:
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


def load_json(path: Path) -> dict:
    """从文件读取 JSON"""
    return json.loads(path.read_text(encoding="utf-8"))
