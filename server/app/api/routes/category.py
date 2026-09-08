"""商品分类路由。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.product import Category, Product
from app.models.user import User
from app.schemas.common import Response
from app.schemas.product import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["商品分类"])


@router.get("", response_model=Response[list[CategoryOut]], summary="分类列表")
def list_categories(db: Session = Depends(get_db)):
    """返回全部分类（小程序/前端公用，按排序倒序）。"""
    items = db.query(Category).order_by(Category.sort.desc(), Category.id.asc()).all()
    data = [CategoryOut.model_validate(c) for c in items]
    return Response(data=data)


@router.post("", summary="新增分类（管理员）")
def create_category(
    req: CategoryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """新增商品分类。"""
    category = Category(name=req.name, sort=req.sort, status=req.status)
    db.add(category)
    db.commit()
    db.refresh(category)
    return Response(data=CategoryOut.model_validate(category))


@router.put("/{category_id}", summary="编辑分类（管理员）")
def update_category(
    category_id: int,
    req: CategoryUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """编辑分类信息。"""
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    data = req.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return Response(data=CategoryOut.model_validate(category))


@router.delete("/{category_id}", summary="删除分类（管理员）")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """删除分类（该分类下存在商品时禁止删除）。"""
    has_product = db.query(Product).filter(Product.category_id == category_id).first()
    if has_product:
        raise HTTPException(status_code=400, detail="该分类下存在商品，无法删除")
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    db.delete(category)
    db.commit()
    return Response(data="删除成功")
