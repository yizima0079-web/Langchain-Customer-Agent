"""订单、订单明细、购物车 ORM 模型。"""
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Order(Base):
    """订单表模型（order 为 MySQL 保留字，需加引号）。"""

    __tablename__ = "order"
    __table_args__ = {"quote": True}

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="订单ID")
    order_no = Column(String(64), nullable=False, unique=True, comment="订单号")
    user_id = Column(BigInteger, nullable=False, comment="下单用户ID")
    total_amount = Column(Numeric(10, 2), nullable=False, default=0, comment="订单总金额")
    status = Column(
        SmallInteger,
        nullable=False,
        default=0,
        comment="0=待付款 1=待发货 2=待收货 3=已完成 4=已取消",
    )
    address_id = Column(BigInteger, nullable=True, comment="收货地址ID")
    remark = Column(String(255), nullable=True, comment="买家备注")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="下单时间")
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间"
    )

    # 订单明细
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """订单明细表模型，冗余商品快照信息。"""

    __tablename__ = "order_item"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="明细ID")
    order_id = Column(
        BigInteger, ForeignKey("order.id", ondelete="CASCADE"), nullable=False, comment="订单ID"
    )
    product_id = Column(BigInteger, nullable=False, comment="商品ID")
    product_name = Column(String(128), nullable=False, comment="商品名称(快照)")
    product_image = Column(String(255), nullable=True, comment="商品图片(快照)")
    price = Column(Numeric(10, 2), nullable=False, default=0, comment="成交单价")
    quantity = Column(Integer, nullable=False, default=1, comment="购买数量")

    order = relationship("Order", back_populates="items")


class Cart(Base):
    """购物车表模型。"""

    __tablename__ = "cart"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uk_user_product"),)

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="购物车项ID")
    user_id = Column(BigInteger, nullable=False, comment="用户ID")
    product_id = Column(BigInteger, nullable=False, comment="商品ID")
    quantity = Column(Integer, nullable=False, default=1, comment="数量")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment="更新时间"
    )
