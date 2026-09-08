"""收货地址相关请求模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AddressCreate(BaseModel):
    """新增地址请求。"""

    name: str = Field(..., min_length=1, max_length=64)
    phone: str = Field(..., min_length=1, max_length=20)
    province: str | None = None
    city: str | None = None
    district: str | None = None
    detail: str = Field(..., min_length=1, max_length=255)
    is_default: int = 0


class AddressUpdate(BaseModel):
    """编辑地址请求（字段均可选）。"""

    name: str | None = None
    phone: str | None = None
    province: str | None = None
    city: str | None = None
    district: str | None = None
    detail: str | None = None
    is_default: int | None = None


class AddressOut(BaseModel):
    """地址响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    name: str
    phone: str
    province: str | None = None
    city: str | None = None
    district: str | None = None
    detail: str
    is_default: int
    created_at: datetime | None = None
