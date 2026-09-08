"""商品分类与商品相关请求/响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    """分类创建请求。"""

    name: str = Field(..., min_length=1, max_length=64)
    sort: int = 0
    status: int = 1


class CategoryUpdate(BaseModel):
    """分类更新请求。"""

    name: str | None = None
    sort: int | None = None
    status: int | None = None


class CategoryOut(BaseModel):
    """分类响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sort: int
    status: int
    created_at: datetime | None = None


class ProductCreate(BaseModel):
    """商品创建请求。"""

    category_id: int
    name: str = Field(..., min_length=1, max_length=128)
    description: str | None = None
    price: float = 0
    original_price: float | None = None
    stock: int = 0
    cover_image: str | None = None
    images: str | None = None
    status: int = 1


class ProductUpdate(BaseModel):
    """商品更新请求。"""

    category_id: int | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    original_price: float | None = None
    stock: int | None = None
    cover_image: str | None = None
    images: str | None = None
    status: int | None = None


class ProductOut(BaseModel):
    """商品响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    description: str | None = None
    price: float
    original_price: float | None = None
    stock: int
    sales: int
    cover_image: str | None = None
    images: str | None = None
    status: int
    created_at: datetime | None = None
    category_name: str | None = None  # 冗余返回分类名，便于前端展示
