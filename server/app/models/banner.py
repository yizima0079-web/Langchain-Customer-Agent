"""首页轮播图 ORM 模型。"""
from sqlalchemy import BigInteger, Column, DateTime, Integer, SmallInteger, String, func

from app.core.database import Base


class Banner(Base):
    """首页轮播图表模型。

    小程序首页顶部轮播展示，由管理后台维护图片与启停状态。
    """

    __tablename__ = "banner"

    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="轮播图ID")
    title = Column(String(128), nullable=True, comment="标题")
    image = Column(String(255), nullable=False, comment="图片URL")
    sort = Column(Integer, nullable=False, default=0, comment="排序(越大越靠前)")
    status = Column(SmallInteger, nullable=False, default=1, comment="0=停用 1=启用")
    created_at = Column(DateTime, nullable=False, default=func.now(), comment="创建时间")
