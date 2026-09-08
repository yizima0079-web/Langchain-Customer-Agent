"""轮播图路由：列表（公开）+ 增删改（管理员）。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.banner import Banner
from app.models.user import User
from app.schemas.banner import BannerCreate, BannerOut, BannerUpdate
from app.schemas.common import Response

router = APIRouter(prefix="/banners", tags=["轮播图"])


@router.get("", response_model=Response[list[BannerOut]], summary="轮播图列表")
def list_banners(only_active: bool = False, db: Session = Depends(get_db)):
    """返回轮播图列表。

    小程序首页传 only_active=true 仅取启用项；
    管理后台不传取全部（含停用）。
    """
    query = db.query(Banner)
    if only_active:
        query = query.filter(Banner.status == 1)
    items = query.order_by(Banner.sort.desc(), Banner.id.asc()).all()
    return Response(data=[BannerOut.model_validate(b) for b in items])


@router.post("", summary="新增轮播图（管理员）")
def create_banner(
    req: BannerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """新增轮播图。"""
    banner = Banner(**req.model_dump())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return Response(data=BannerOut.model_validate(banner))


@router.put("/{banner_id}", summary="编辑轮播图（管理员）")
def update_banner(
    banner_id: int,
    req: BannerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """编辑轮播图信息。"""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="轮播图不存在")
    data = req.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(banner, field, value)
    db.commit()
    db.refresh(banner)
    return Response(data=BannerOut.model_validate(banner))


@router.delete("/{banner_id}", summary="删除轮播图（管理员）")
def delete_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """删除轮播图。"""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="轮播图不存在")
    db.delete(banner)
    db.commit()
    return Response(data="已删除")
