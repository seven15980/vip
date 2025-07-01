from fastapi import Depends, HTTPException, status, Request
from jose import JWTError
from sqlalchemy.orm import Session
from .database import get_db
from .core.jwt import JWTUtil
from .models import api_login_post200_response
from .core.exception import APIException
from .config import settings
from .models.user import User

# 假设有 User/Admin ORM 模型，后续可完善

def get_current_user(request: Request, db: Session = Depends(get_db)):
    """
    解析 JWT，获取当前用户信息。
    """
    auth: str = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未认证")
    token = auth.split(" ", 1)[1]
    try:
        payload = JWTUtil.decode_token(token)
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token无效")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="用户不存在")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token无效或已过期")

def get_current_admin(request: Request, db: Session = Depends(get_db)):
    """
    解析 JWT，获取当前管理员信息。
    """
    auth: str = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未认证")
    token = auth.split(" ", 1)[1]
    try:
        payload = JWTUtil.decode_token(token)
        admin_id = payload.get("admin_id")
        if not admin_id:
            raise HTTPException(status_code=401, detail="Token无效")
        # 这里应查询数据库获取管理员对象，简化为返回 admin_id
        return {"admin_id": admin_id}
    except JWTError:
        raise HTTPException(status_code=401, detail="Token无效或已过期") 