from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from openapi_server.schemas.user import RegisterRequest, LoginRequest, UserProfileResponse, ProfileUpdateRequest
from openapi_server.crud import user as crud_user
from openapi_server.core import jwt, crypto
from openapi_server.database import get_db
from openapi_server.core.response import success, error
from openapi_server.deps import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if crud_user.get_user_by_email(db, data.email):
        return error(msg="邮箱已注册", code=400)
    if len(data.password) < 6:
        return error(msg="密码长度至少6位", code=400)
    hashed = crypto.hash_password(data.password)
    user = crud_user.create_user(db, email=data.email, password_hash=hashed)
    return success({"id": user.id, "email": user.email})

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = crud_user.get_user_by_email(db, data.email)
    if not user or not crypto.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    user.last_login = datetime.utcnow()
    db.commit()
    token = jwt.create_access_token({"user_id": user.id})
    return success({"token": token})

@router.get("/profile")
def get_profile(current_user=Depends(get_current_user)):
    return success({
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
    })

@router.put("/profile")
def update_profile(data: ProfileUpdateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if data.password and len(data.password) < 6:
        return error(msg="密码长度至少6位", code=400)
    hashed = crypto.hash_password(data.password)
    crud_user.update_user(db, current_user, password_hash=hashed)
    return success() 