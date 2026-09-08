"""收货地址 ORM 模型。"""
from sqlalchemy import BigInteger, Column, DateTime, SmallInteger, String, func

from app.core.database import Base


class Address(Base):
    """收货地址表模型。"""

    __tablename__ = "address"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="地址ID")
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    name = Column(String(64), nullable=False, comment="收货人姓名")
    phone = Column(String(20), nullable=False, comment="收货人电话")
    province = Column(String(64), nullable=True, comment="省")
    city = Column(String(64), nullable=True, comment="市")
    district = Column(String(64), nullable=True, comment="区")
    detail = Column(String(255), nullable=False, comment="详细地址")
    is_default = Column(SmallInteger, nullable=False, default=0, comment="0=否 1=是")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
