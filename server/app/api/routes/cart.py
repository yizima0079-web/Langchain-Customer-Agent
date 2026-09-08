"""购物车路由。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.order import Cart
from app.models.product import Product
from app.models.user import User
from app.schemas.common import Response
from app.schemas.order import CartAdd, CartItemOut, CartUpdate

router = APIRouter(prefix="/cart", tags=["购物车"])


@router.get("", response_model=Response[list[CartItemOut]], summary="我的购物车")
def my_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """返回当前用户购物车（含商品冗余信息）。"""
    carts = db.query(Cart).filter(Cart.user_id == current_user.id).all()
    result: list[CartItemOut] = []
    for c in carts:
        product = db.query(Product).filter(Product.id == c.product_id).first()
        result.append(
            CartItemOut(
                id=c.id,
                product_id=c.product_id,
                quantity=c.quantity,
                product_name=product.name if product else None,
                product_image=product.cover_image if product else None,
                price=float(product.price) if product else None,
                stock=product.stock if product else None,
            )
        )
    return Response(data=result)


@router.post("", summary="加入购物车")
def add_cart(
    req: CartAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """加入购物车（已存在则累加数量）。"""
    product = db.query(Product).filter(Product.id == req.product_id).first()
    if not product or product.status != 1:
        raise HTTPException(status_code=400, detail="商品不存在或已下架")

    item = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id, Cart.product_id == req.product_id)
        .first()
    )
    if item:
        item.quantity += req.quantity
    else:
        db.add(Cart(user_id=current_user.id, product_id=req.product_id, quantity=req.quantity))
    db.commit()
    return Response(data="已加入购物车")


@router.put("/{cart_id}", summary="修改购物车数量")
def update_cart(
    cart_id: int,
    req: CartUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """修改购物车项数量。"""
    item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="购物车项不存在")
    item.quantity = req.quantity
    db.commit()
    return Response(data="已更新")


@router.delete("/{cart_id}", summary="删除购物车项")
def delete_cart(
    cart_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除购物车项。"""
    item = db.query(Cart).filter(Cart.id == cart_id, Cart.user_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="购物车项不存在")
    db.delete(item)
    db.commit()
    return Response(data="已删除")
