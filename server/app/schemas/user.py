"""用户相关请求/响应模型。"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    """登录请求。"""

    username: str = Field(..., min_length=1, description="账号")
    password: str = Field(..., min_length=1, description="密码")


class UserCreate(BaseModel):
    """注册请求。"""

    username: str = Field(..., min_length=2, max_length=64)
    password: str = Field(..., min_length=6, max_length=64)
    nickname: str | None = None
    phone: str | None = None
    email: str | None = None


class UserUpdate(BaseModel):
    """用户资料编辑请求。"""

    nickname: str | None = None
    avatar: str | None = None
    phone: str | None = None
    email: str | None = None
    status: int | None = None
    role: int | None = None


class UserOut(BaseModel):
    """用户信息响应（不含密码）。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nickname: str | None = None
    avatar: str | None = None
    phone: str | None = None
    email: str | None = None
    role: int
    status: int
    created_at: datetime | None = None


class Token(BaseModel):
    """登录令牌响应。"""

    access_token: str
    token_type: str = "bearer"
    user: UserOut
