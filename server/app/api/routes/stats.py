"""数据统计路由（供管理后台首页图表使用）。"""
from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.order import Order
from app.models.product import Category, Product
from app.models.user import User
from app.schemas.common import Response

router = APIRouter(prefix="/stats", tags=["数据统计"])

# 订单状态中文映射
STATUS_MAP = {0: "待付款", 1: "待发货", 2: "待收货", 3: "已完成", 4: "已取消"}


@router.get("/overview", summary="KPI 汇总")
def overview(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """返回首页 KPI 卡片数据：用户数/商品数/订单数/销售额/今日订单。"""
    user_count = db.query(User).filter(User.role == 0).count()
    product_count = db.query(Product).filter(Product.status == 1).count()
    order_count = db.query(Order).count()
    total_sales = (
        db.query(func.sum(Order.total_amount))
        .filter(Order.status.in_([1, 2, 3]))
        .scalar()
        or 0
    )
    today = date.today()
    today_orders = db.query(Order).filter(func.date(Order.created_at) == today).count()

    return Response(
        data={
            "user_count": user_count,
            "product_count": product_count,
            "order_count": order_count,
            "total_sales": float(total_sales),
            "today_orders": today_orders,
        }
    )


@router.get("/sales-trend", summary="近7天销售趋势")
def sales_trend(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """返回近 7 天每天的销售额与订单数（用于折线图）。"""
    result = []
    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        orders = db.query(Order).filter(func.date(Order.created_at) == day).all()
        sales = sum(float(o.total_amount) for o in orders if o.status in (1, 2, 3))
        result.append({"date": day.strftime("%m-%d"), "sales": round(sales, 2), "orders": len(orders)})
    return Response(data=result)


@router.get("/order-status", summary="订单状态分布")
def order_status(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """返回各订单状态的数量分布（用于饼图）。"""
    rows = db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    result = [{"name": STATUS_MAP.get(s, str(s)), "value": c} for s, c in rows]
    return Response(data=result)


@router.get("/category", summary="分类销量占比")
def category_stats(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """返回各分类商品累计销量占比（用于柱状图）。"""
    rows = (
        db.query(Category.name, func.sum(Product.sales))
        .join(Product, Product.category_id == Category.id)
        .group_by(Category.id)
        .all()
    )
    result = [{"name": name, "value": int(v or 0)} for name, v in rows]
    return Response(data=result)
