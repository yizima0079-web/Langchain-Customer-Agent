"""安全相关工具：密码 MD5 加密、JWT 令牌签发与解析。"""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from app.core.config import settings


def md5_hash(text: str) -> str:
    """对字符串做 MD5 加密（用于用户密码存储）。

    Args:
        text: 原始字符串。

    Returns:
        MD5 十六进制小写字符串。
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def verify_password(plain: str, hashed: str) -> bool:
    """校验明文密码与 MD5 密文是否一致。"""
    return md5_hash(plain) == hashed


def create_access_token(subject: str | int, extra: dict[str, Any] | None = None) -> str:
    """签发 JWT 访问令牌。

    Args:
        subject: 令牌主体（通常为用户 ID）。
        extra: 额外声明（可选，例如角色信息）。

    Returns:
        JWT 字符串。
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload: dict[str, Any] = {"sub": str(subject), "exp": expire}
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """解析 JWT 令牌。

    Args:
        token: JWT 字符串。

    Returns:
        解析成功返回 payload 字典，失败返回 None。
    """
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None
