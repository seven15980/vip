from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from . import Base
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False) 
    last_login = Column(DateTime, nullable=True) 

class UserRegisterRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", alias="email")
    password: str = Field(..., min_length=6, example="123456", description="用户密码")

    class Config:
        allow_population_by_field_name = True

class UserRegisterResponse(BaseModel):
    id: int = Field(..., example=1, description="用户ID")
    email: EmailStr = Field(..., example="user@example.com", alias="email")

    class Config:
        allow_population_by_field_name = True

class UserLoginRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", alias="email")
    password: str = Field(..., example="123456", description="用户密码")

    class Config:
        allow_population_by_field_name = True

class UserLoginResponse(BaseModel):
    token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", description="JWT 令牌")

class UserProfileOut(BaseModel):
    id: int = Field(..., example=1, description="用户ID")
    email: EmailStr = Field(..., example="user@example.com", alias="email")
    is_active: bool = Field(..., example=True, description="是否激活")
    created_at: Optional[datetime] = Field(None, example="2023-01-01T00:00:00", description="创建时间")
    last_login: Optional[datetime] = Field(None, example="2023-01-02T00:00:00", description="最后登录时间")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True

class UserProfileUpdateRequest(BaseModel):
    password: str = Field(..., min_length=6, example="123456", description="新密码")

class SuccessResponse(BaseModel):
    msg: str = Field(..., example="操作成功", description="返回信息") 

class UserListOut(BaseModel):
    id: int = Field(..., example=1, description="用户ID")
    email: EmailStr = Field(..., example="user@example.com", alias="email")
    is_active: bool = Field(..., example=True, description="是否激活")

    class Config:
        from_attributes = True
        allow_population_by_field_name = True