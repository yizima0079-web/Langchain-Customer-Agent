"""Pydantic 模型包（请求/响应数据结构）。"""
from app.schemas.address import AddressCreate, AddressUpdate
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.common import Page, Response
from app.schemas.knowledge import KnowledgeFileOut
from app.schemas.order import (
    CartAdd,
    CartItemOut,
    CartUpdate,
    OrderCreate,
    OrderItemOut,
    OrderOut,
    OrderUpdate,
)
from app.schemas.product import (
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    ProductCreate,
    ProductOut,
    ProductUpdate,
)
from app.schemas.user import LoginRequest, Token, UserCreate, UserOut, UserUpdate

__all__ = [
    "Response",
    "Page",
    "AddressCreate",
    "AddressUpdate",
    "LoginRequest",
    "Token",
    "UserCreate",
    "UserUpdate",
    "UserOut",
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryOut",
    "ProductCreate",
    "ProductUpdate",
    "ProductOut",
    "CartAdd",
    "CartUpdate",
    "CartItemOut",
    "OrderCreate",
    "OrderUpdate",
    "OrderItemOut",
    "OrderOut",
    "KnowledgeFileOut",
    "ChatRequest",
    "ChatResponse",
]
