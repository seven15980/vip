from pydantic import BaseModel, Field
from typing import Optional, List

class NotificationInfo(BaseModel):
    id: int
    title: str
    content: str
    type: str  # system/private
    created_at: str

class UserNotificationInfo(BaseModel):
    id: int
    user_id: int
    notification_id: int
    is_read: bool
    read_at: Optional[str]
    notification: NotificationInfo

class NotificationListResponse(BaseModel):
    notifications: List[NotificationInfo]

class UserNotificationListResponse(BaseModel):
    user_notifications: List[UserNotificationInfo]

class AdminSendNotificationRequest(BaseModel):
    title: str = Field(..., description="通知标题")
    type: str = Field(..., description="通知类型：info/warning/success")
    target: str = Field(..., description="发送对象：all/normal/online/local/specified")
    user_ids: Optional[List[int]] = Field(None, description="指定用户ID列表，仅target=specified时必填")
    content: str = Field(..., description="通知内容") 