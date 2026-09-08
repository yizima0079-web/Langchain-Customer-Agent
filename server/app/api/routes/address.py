"""收货地址路由。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.models.address import Address
from app.models.user import User
from app.schemas.address import AddressCreate, AddressOut, AddressUpdate
from app.schemas.common import Response

router = APIRouter(prefix="/addresses", tags=["收货地址"])


@router.get("", summary="地址列表")
def list_address(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """返回当前用户地址（默认地址排前）。"""
    items = (
        db.query(Address)
        .filter(Address.user_id == current_user.id)
        .order_by(Address.is_default.desc(), Address.id.desc())
        .all()
    )
    return Response(data=[AddressOut.model_validate(a) for a in items])


@router.post("", summary="新增地址")
def create_address(
    req: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """新增收货地址；若设为默认，取消其他默认。"""
    if req.is_default:
        db.query(Address).filter(Address.user_id == current_user.id).update(
            {Address.is_default: 0}
        )
    address = Address(user_id=current_user.id, **req.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return Response(data=AddressOut.model_validate(address))


@router.put("/{address_id}", summary="编辑地址")
def update_address(
    address_id: int,
    req: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """编辑地址；若设为默认，取消其他默认。"""
    address = (
        db.query(Address)
        .filter(Address.id == address_id, Address.user_id == current_user.id)
        .first()
    )
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")

    data = req.model_dump(exclude_unset=True)
    if data.get("is_default"):
        db.query(Address).filter(Address.user_id == current_user.id).update(
            {Address.is_default: 0}
        )
    for field, value in data.items():
        setattr(address, field, value)
    db.commit()
    db.refresh(address)
    return Response(data=AddressOut.model_validate(address))


@router.delete("/{address_id}", summary="删除地址")
def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """删除地址。"""
    address = (
        db.query(Address)
        .filter(Address.id == address_id, Address.user_id == current_user.id)
        .first()
    )
    if not address:
        raise HTTPException(status_code=404, detail="地址不存在")
    db.delete(address)
    db.commit()
    return Response(data="已删除")
