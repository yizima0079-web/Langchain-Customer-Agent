"""商品分类与商品 ORM 模型。"""
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    """商品分类表模型。"""

    __tablename__ = "category"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="分类ID")
    name = Column(String(64), nullable=False, comment="分类名称")
    sort = Column(Integer, nullable=False, default=0, comment="排序(越大越靠前)")
    status = Column(SmallInteger, nullable=False, default=1, comment="0=停用 1=启用")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")

    # 分类下的商品列表
    products = relationship("Product", back_populates="category")


class Product(Base):
    """商品表模型。"""

    __tablename__ = "product"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="商品ID")
    category_id = Column(
        BigInteger, ForeignKey("category.id"), nullable=False, comment="所属分类ID"
    )
    name = Column(String(128), nullable=False, comment="商品名称")
    description = Column(Text, nullable=True, comment="商品描述")
    price = Column(Numeric(10, 2), nullable=False, default=0, comment="售价")
    original_price = Column(Numeric(10, 2), nullable=True, comment="原价")
    stock = Column(Integer, nullable=False, default=0, comment="库存")
    sales = Column(Integer, nullable=False, default=0, comment="销量")
    cover_image = Column(String(255), nullable=True, comment="封面图URL")
    images = Column(Text, nullable=True, comment="轮播图URL列表(JSON字符串)")
    status = Column(SmallInteger, nullable=False, default=1, comment="0=下架 1=上架")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 所属分类
    category = relationship("Category", back_populates="products")
