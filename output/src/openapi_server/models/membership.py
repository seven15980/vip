from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from . import Base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Membership(Base):
    __tablename__ = "membership"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    type = Column(String, nullable=False)  # local/online
    expire_at = Column(DateTime, nullable=False)
    storage_total = Column(Integer, nullable=True)  # 仅online会员有
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class MembershipStatusLocal(BaseModel):
    expire_at: Optional[datetime] = Field(None, example="2023-12-31T23:59:59", description="本地会员到期时间")

class MembershipStatusOnline(BaseModel):
    expire_at: Optional[datetime] = Field(None, example="2023-12-31T23:59:59", description="线上会员到期时间")
    storage_total: int = Field(0, example=10, description="线上会员总容量（GB）")

class MembershipStatusResponse(BaseModel):
    local: MembershipStatusLocal = Field(..., description="本地会员信息")
    online: MembershipStatusOnline = Field(..., description="线上会员信息") 