"""用户管理路由（管理员）。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.deps import get_current_admin, get_db
from app.models.user import User
from app.schemas.common import Response
from app.schemas.user import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["用户管理"])


@router.get("", summary="用户列表")
def list_users(
    page: int = 1,
    size: int = 10,
    keyword: str = "",
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """分页查询用户列表，支持按账号/昵称关键字搜索。"""
    query = db.query(User)
    if keyword:
        query = query.filter(
            or_(User.username.contains(keyword), User.nickname.contains(keyword))
        )
    total = query.count()
    items = query.order_by(User.id.desc()).offset((page - 1) * size).limit(size).all()
    # ORM 对象需转换为响应模型（排除密码等敏感字段）
    data = {"total": total, "items": [UserOut.model_validate(u) for u in items]}
    return Response(data=data)


@router.put("/{user_id}", summary="编辑用户")
def update_user(
    user_id: int,
    req: UserUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    """更新用户资料/状态/角色。"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    data = req.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return Response(data=UserOut.model_validate(user))


@router.delete("/{user_id}", summary="删除用户")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
):
    """删除用户（不能删除自己）。"""
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="不能删除自己")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return Response(data="删除成功")
