"""安全相关工具：密码哈希（bcrypt）、JWT 令牌签发与解析。"""
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from app.core.config import settings


def md5_hash(text: str) -> str:
    """对字符串做 MD5 加密（仅用于兼容历史 MD5 密码，新密码一律 bcrypt）。

    Args:
        text: 原始字符串。

    Returns:
        MD5 十六进制小写字符串。
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def hash_password(plain: str) -> str:
    """使用 bcrypt 对明文密码做加盐哈希。

    Args:
        plain: 原始明文密码。

    Returns:
        bcrypt 哈希串（以 $2b$ 开头）。
    """
    return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _is_md5(hashed: str) -> bool:
    """判断哈希串是否为历史 MD5 格式（32 位十六进制）。"""
    return len(hashed) == 32 and all(c in "0123456789abcdef" for c in hashed.lower())


def verify_password(plain: str, hashed: str) -> bool:
    """校验明文密码与哈希是否一致，兼容历史 MD5 与 bcrypt 两种格式。"""
    if _is_md5(hashed):
        return md5_hash(plain) == hashed
    try:
        return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def needs_rehash(hashed: str) -> bool:
    """判断密码哈希是否需要从历史 MD5 升级为 bcrypt。"""
    return _is_md5(hashed)


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
