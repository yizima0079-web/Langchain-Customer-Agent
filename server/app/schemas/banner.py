"""轮播图相关请求/响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BannerCreate(BaseModel):
    """新增轮播图请求。"""

    title: str | None = Field(None, max_length=128, description="标题")
    image: str = Field(..., description="图片URL")
    sort: int = 0
    status: int = 1


class BannerUpdate(BaseModel):
    """编辑轮播图请求（字段均可选）。"""

    title: str | None = None
    image: str | None = None
    sort: int | None = None
    status: int | None = None


class BannerOut(BaseModel):
    """轮播图响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str | None = None
    image: str
    sort: int
    status: int
    created_at: datetime | None = None
