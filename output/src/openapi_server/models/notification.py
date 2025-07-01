from sqlalchemy import Column, Integer, String, DateTime, func
from . import Base
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Notification(Base):
    __tablename__ = "notification"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)  # system/private
    created_at = Column(DateTime, default=func.now(), nullable=False)

class NotificationOut(BaseModel):
    id: int = Field(..., example=1, description="通知ID")
    title: str = Field(..., example="系统通知", description="通知标题")
    content: str = Field(..., example="内容", description="通知内容")
    type: str = Field(..., example="info", description="通知类型")
    created_at: datetime = Field(..., example="2023-01-01T00:00:00", description="创建时间")
    is_read: bool = Field(..., example=False, description="是否已读")
    read_at: Optional[datetime] = Field(None, example="2023-01-02T00:00:00", description="已读时间")
    class Config:
        orm_mode = True

class NotificationMarkReadResponse(BaseModel):
    success: bool = Field(..., example=True, description="是否成功")
    msg: str = Field(..., example="已标记为已读", description="返回信息")

class AdminSendNotificationRequest(BaseModel):
    title: str = Field(..., example="系统通知", description="通知标题")
    content: str = Field(..., example="内容", description="通知内容")
    type: str = Field(..., example="info", description="通知类型")
    target: str = Field(..., example="all", description="发送对象类型")
    user_ids: Optional[List[int]] = Field(None, example=[1,2], description="指定用户ID列表，仅target为specified时需要")

class AdminSendNotificationResponse(BaseModel):
    success: bool = Field(..., example=True, description="是否成功")
    msg: str = Field(..., example="通知已发送", description="返回信息")
    notification_id: Optional[int] = Field(None, example=1, description="通知ID")
    user_count: int = Field(..., example=10, description="发送用户数")

class NotificationHistoryOut(BaseModel):
    id: int = Field(..., example=1, description="通知ID")
    title: str = Field(..., example="系统通知", description="通知标题")
    content: str = Field(..., example="内容", description="通知内容")
    type: str = Field(..., example="info", description="通知类型")
    created_at: Optional[datetime] = Field(None, example="2023-01-01T00:00:00", description="创建时间")
    class Config:
        orm_mode = True

class SuccessResponse(BaseModel):
    msg: str = Field(..., example="操作成功", description="返回信息") 