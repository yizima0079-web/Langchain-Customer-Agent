"""购物车与订单相关请求/响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CartAdd(BaseModel):
    """加入购物车请求。"""

    product_id: int
    quantity: int = 1


class CartUpdate(BaseModel):
    """购物车数量更新请求。"""

    quantity: int


class CartItemOut(BaseModel):
    """购物车项响应（含商品信息）。"""

    id: int
    product_id: int
    quantity: int
    product_name: str | None = None
    product_image: str | None = None
    price: float | None = None
    stock: int | None = None


class OrderItemOut(BaseModel):
    """订单明细响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    product_image: str | None = None
    price: float
    quantity: int


class OrderOut(BaseModel):
    """订单响应。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    user_id: int
    total_amount: float
    status: int
    address_id: int | None = None
    remark: str | None = None
    created_at: datetime | None = None
    items: list[OrderItemOut] = []


class OrderCreate(BaseModel):
    """下单请求（购物车结算）。"""

    address_id: int
    remark: str | None = None
    # 直接从购物车结算时无需传，若传则指定商品与数量（用于立即购买）
    items: list[CartAdd] | None = None


class OrderUpdate(BaseModel):
    """订单状态更新请求。"""

    status: int
