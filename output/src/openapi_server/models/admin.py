from sqlalchemy import Column, Integer, String, DateTime, func
from . import Base
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

class AdminLoginRequest(BaseModel):
    username: str = Field(..., example="admin", alias="userName", description="管理员用户名")
    password: str = Field(..., example="123456", description="管理员密码")
    class Config:
        allow_population_by_field_name = True

class AdminLoginResponse(BaseModel):
    token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", description="JWT 令牌")
    admin_id: int = Field(..., example=1, description="管理员ID")

class CardCodeCreateRequest(BaseModel):
    count: int = Field(..., example=10, description="生成卡密数量")
    value: int = Field(..., example=30, description="卡密面值（月数/容量等）")
    type: str = Field(..., example="online", description="卡密类型（online/local/both）")

class CardCodeOut(BaseModel):
    code: str = Field(..., example="ABC123", description="卡密")
    value: int = Field(..., example=30, description="面值")
    type: str = Field(..., example="online", description="类型")
    is_used: bool = Field(..., example=False, description="是否已使用")
    used_by: Optional[int] = Field(None, example=2, description="使用者ID")
    used_at: Optional[datetime] = Field(None, example="2023-01-01T00:00:00", description="使用时间")
    created_at: Optional[datetime] = Field(None, example="2023-01-01T00:00:00", description="创建时间")
    class Config:
        orm_mode = True

class CardCodeLogOut(BaseModel):
    code: str = Field(..., example="ABC123", description="卡密")
    user_id: int = Field(..., example=1, description="用户ID")
    used_at: Optional[datetime] = Field(None, example="2023-01-01T00:00:00", description="使用时间")
    action: str = Field(..., example="兑换", description="操作类型")
    class Config:
        orm_mode = True

class MembershipOut(BaseModel):
    id: int = Field(..., example=1, description="会员ID")
    user_id: int = Field(..., example=1, description="用户ID")
    type: str = Field(..., example="online", description="会员类型")
    expire_at: Optional[datetime] = Field(None, example="2023-12-31T23:59:59", description="到期时间")
    storage_total: Optional[int] = Field(None, example=10, description="总容量（仅online类型有）")
    created_at: Optional[datetime] = Field(None, example="2023-01-01T00:00:00", description="创建时间")
    updated_at: Optional[datetime] = Field(None, example="2023-01-02T00:00:00", description="更新时间")
    class Config:
        orm_mode = True

class MembershipRenewRequest(BaseModel):
    type: str = Field(..., example="online", description="会员类型")
    months: int = Field(..., example=3, description="续费月数")
    storage: Optional[int] = Field(None, example=10, description="增加容量，仅online类型需要")

class MembershipRenewResponse(BaseModel):
    id: int = Field(..., example=1, description="会员ID")
    user_id: int = Field(..., example=1, description="用户ID")
    type: str = Field(..., example="online", description="会员类型")
    expire_at: Optional[datetime] = Field(None, example="2023-12-31T23:59:59", description="到期时间")
    storage_total: Optional[int] = Field(None, example=10, description="总容量")

class StatisticsResponse(BaseModel):
    user_count: int = Field(..., example=100, description="用户总数")
    membership_count: int = Field(..., example=50, description="会员总数")
    card_code_used_count: int = Field(..., example=30, description="已用卡密数")

class SuccessResponse(BaseModel):
    msg: str = Field(..., example="操作成功", description="返回信息") 