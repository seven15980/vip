from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import Optional
from ..models.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserProfileUpdateRequest,
    UserRegisterResponse,
    UserLoginResponse,
    UserProfileOut,
    SuccessResponse,
)
from ..crud import user as crud_user
from ..core import jwt, crypto
from ..database import get_db
from ..deps import get_current_user
from ..schemas.user import UserProfileResponse
from typing import List
from ..models.user import UserListOut

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.post("/register", response_model=UserRegisterResponse)
def register(
    data: UserRegisterRequest = Body(...),
    db: Session = Depends(get_db)
):
    if crud_user.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="邮箱已注册")
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="密码长度至少6位")
    hashed = crypto.hash_password(data.password)
    user = crud_user.create_user(db, email=data.email, password_hash=hashed)
    return UserRegisterResponse(id=user.id, email=user.email)

@router.post("/login", response_model=UserLoginResponse)
def login(
    data: UserLoginRequest = Body(...),
    db: Session = Depends(get_db)
):
    user = crud_user.get_user_by_email(db, data.email)
    if not user or not crypto.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    user.last_login = user.last_login  # TODO: 实际应更新时间
    db.commit()
    token = jwt.create_access_token({"user_id": user.id})
    return UserLoginResponse(token=token)

@router.get("/profile", response_model=UserProfileOut)
def get_profile(current_user=Depends(get_current_user)):
    return UserProfileOut(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
    )

@router.put("/profile", response_model=SuccessResponse)
def update_profile(
    data: UserProfileUpdateRequest = Body(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if data.password and len(data.password) < 6:
        raise HTTPException(status_code=400, detail="密码长度至少6位")
    hashed = crypto.hash_password(data.password)
    crud_user.update_user(db, current_user, password_hash=hashed)
    return SuccessResponse(msg="更新成功") 
@router.get("/all", response_model=List[UserListOut])
def get_all_users(db: Session = Depends(get_db)):
    users = crud_user.get_all_users(db)
    return [UserListOut.from_orm(u) for u in users]