"""商品路由。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.common import Response
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["商品"])


@router.get("", summary="商品列表")
def list_products(
    page: int = 1,
    size: int = 10,
    category_id: int | None = None,
    keyword: str = "",
    only_online: bool = False,
    db: Session = Depends(get_db),
):
    """分页查询商品，支持分类过滤、关键字搜索、仅上架过滤。"""
    query = db.query(Product)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if keyword:
        query = query.filter(Product.name.contains(keyword))
    if only_online:
        query = query.filter(Product.status == 1)

    total = query.count()
    items = query.order_by(Product.id.desc()).offset((page - 1) * size).limit(size).all()

    # 补充分类名，方便前端展示
    result = []
    for p in items:
        out = ProductOut.model_validate(p)
        out.category_name = p.category.name if p.category else None
        result.append(out)
    return Response(data={"total": total, "items": result})


@router.get("/{product_id}", response_model=Response[ProductOut], summary="商品详情")
def get_product(product_id: int, db: Session = Depends(get_db)):
    """返回单个商品详情。"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    out = ProductOut.model_validate(product)
    out.category_name = product.category.name if product.category else None
    return Response(data=out)


@router.post("", summary="新增商品（管理员）")
def create_product(
    req: ProductCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """新增商品。"""
    product = Product(**req.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    out = ProductOut.model_validate(product)
    out.category_name = product.category.name if product.category else None
    return Response(data=out)


@router.put("/{product_id}", summary="编辑商品（管理员）")
def update_product(
    product_id: int,
    req: ProductUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """编辑商品信息。"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    data = req.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    out = ProductOut.model_validate(product)
    out.category_name = product.category.name if product.category else None
    return Response(data=out)


@router.delete("/{product_id}", summary="删除商品（管理员）")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """删除商品。"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")
    db.delete(product)
    db.commit()
    return Response(data="删除成功")
