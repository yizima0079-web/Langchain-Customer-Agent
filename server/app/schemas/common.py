"""通用数据结构：统一响应、分页。"""
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    """统一 API 响应格式。"""

    code: int = 0
    message: str = "ok"
    data: T | None = None


class Page(BaseModel, Generic[T]):
    """分页响应格式。"""

    total: int
    items: list[T]
