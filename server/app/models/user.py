"""用户 ORM 模型。"""
from sqlalchemy import BigInteger, Column, DateTime, SmallInteger, String, func

from app.core.database import Base


class User(Base):
    """用户表模型，普通用户与管理员共用，通过 role 区分。"""

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="用户ID")
    username = Column(String(64), nullable=False, unique=True, comment="登录账号")
    password = Column(String(64), nullable=False, comment="密码(MD5)")
    nickname = Column(String(64), nullable=True, comment="昵称")
    avatar = Column(String(255), nullable=True, comment="头像URL")
    phone = Column(String(20), nullable=True, comment="手机号")
    email = Column(String(128), nullable=True, comment="邮箱")
    role = Column(SmallInteger, nullable=False, default=0, comment="0=普通用户 1=管理员")
    status = Column(SmallInteger, nullable=False, default=1, comment="0=禁用 1=正常")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )
