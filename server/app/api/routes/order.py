"""订单路由。"""
import random
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.order import Cart, Order, OrderItem
from app.models.address import Address
from app.models.product import Product
from app.models.user import User
from app.schemas.common import Response
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate

router = APIRouter(prefix="/orders", tags=["订单"])


def _generate_order_no() -> str:
    """生成订单号：时间戳 + 4 位随机数。"""
    return datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))


@router.post("", response_model=Response[OrderOut], summary="创建订单")
def create_order(
    req: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """下单：支持购物车结算或指定商品立即购买。"""
    address = (
        db.query(Address)
        .filter(Address.id == req.address_id, Address.user_id == current_user.id)
        .first()
    )
    if not address:
        raise HTTPException(status_code=400, detail="收货地址不存在")

    items: list[tuple[Product, int]] = []

    if req.items:
        # 立即购买：按指定商品与数量
        candidates = [(it.product_id, it.quantity) for it in req.items]
        from_cart = False
    else:
        # 购物车结算
        carts = db.query(Cart).filter(Cart.user_id == current_user.id).all()
        if not carts:
            raise HTTPException(status_code=400, detail="购物车为空")
        candidates = [(c.product_id, c.quantity) for c in carts]
        from_cart = True

    if not candidates:
        raise HTTPException(status_code=400, detail="没有可结算的商品")

    # 按商品 id 排序后一次性加行锁，锁定顺序一致（避免死锁）并防止并发超卖
    product_ids = sorted({pid for pid, _ in candidates})
    locked = (
        db.query(Product)
        .filter(Product.id.in_(product_ids))
        .with_for_update()
        .all()
    )
    product_map = {p.id: p for p in locked}

    for pid, qty in candidates:
        product = product_map.get(pid)
        if not product or product.status != 1:
            if from_cart:
                continue  # 购物车结算：跳过已下架/失效商品
            raise HTTPException(status_code=400, detail=f"商品 {pid} 不存在或已下架")
        if product.stock < qty:
            raise HTTPException(status_code=400, detail=f"商品「{product.name}」库存不足")
        items.append((product, qty))

    if not items:
        raise HTTPException(status_code=400, detail="没有可结算的商品")

    # 购物车结算成功后清空购物车
    if from_cart:
        db.query(Cart).filter(Cart.user_id == current_user.id).delete()

    total = sum(float(p.price) * q for p, q in items)
    order = Order(
        order_no=_generate_order_no(),
        user_id=current_user.id,
        total_amount=total,
        status=0,
        address_id=req.address_id,
        remark=req.remark,
    )
    db.add(order)
    db.flush()  # 先拿到订单主键

    # 写明细 + 扣库存 + 加销量
    for product, qty in items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                product_image=product.cover_image,
                price=product.price,
                quantity=qty,
            )
        )
        product.stock -= qty
        product.sales += qty

    db.commit()
    db.refresh(order)
    # ORM → 响应模型（items 关系懒加载，需在会话内取）
    return Response(data=OrderOut.model_validate(order))


@router.get("", summary="订单列表")
def list_orders(
    page: int = 1,
    size: int = 10,
    status: int | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """订单列表：普通用户查看自己的订单，管理员查看全部。"""
    page = max(page, 1)
    size = min(max(size, 1), 100)  # 限制单页条数，防止一次拉取全表
    query = db.query(Order)
    if current_user.role != 1:
        query = query.filter(Order.user_id == current_user.id)
    if status is not None:
        query = query.filter(Order.status == status)

    total = query.count()
    items = query.order_by(Order.id.desc()).offset((page - 1) * size).limit(size).all()
    data = {"total": total, "items": [OrderOut.model_validate(o) for o in items]}
    return Response(data=data)


@router.put("/{order_id}/status", summary="更新订单状态")
def update_status(
    order_id: int,
    req: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新订单状态：普通用户仅能取消自己的订单，管理员可任意修改。"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if current_user.role != 1 and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作该订单")

    # 普通用户只能取消待付款订单；取消时释放已预扣的库存和销量。
    if current_user.role != 1 and req.status == 4:
        if order.status != 0:
            raise HTTPException(status_code=400, detail="只有待付款订单可以取消")
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity
                product.sales = max(0, product.sales - item.quantity)

    order.status = req.status
    db.commit()
    db.refresh(order)
    return Response(data=OrderOut.model_validate(order))
