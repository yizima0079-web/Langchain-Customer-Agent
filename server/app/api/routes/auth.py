"""认证路由：注册、登录、当前用户信息。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, get_db
from app.core.security import create_access_token, md5_hash, verify_password
from app.models.user import User
from app.schemas.common import Response
from app.schemas.user import LoginRequest, Token, UserCreate, UserOut

router = APIRouter(prefix="/auth", tags=["认证"])


@router.post("/register", response_model=Response[UserOut], summary="用户注册")
def register(req: UserCreate, db: Session = Depends(get_db)):
    """注册普通用户（密码 MD5 加密存储）。"""
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    user = User(
        username=req.username,
        password=md5_hash(req.password),
        nickname=req.nickname or req.username,
        phone=req.phone,
        email=req.email,
        role=0,
        status=1,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return Response(data=UserOut.model_validate(user))


@router.post("/login", response_model=Response[Token], summary="用户登录")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """校验账号密码并签发 JWT。"""
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    if user.status == 0:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    token = create_access_token(user.id)
    return Response(data=Token(access_token=token, user=user))


@router.get("/me", response_model=Response[UserOut], summary="当前用户信息")
def me(current_user: User = Depends(get_current_user)):
    """返回当前登录用户信息。"""
    return Response(data=UserOut.model_validate(current_user))
