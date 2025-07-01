from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from typing import List
from ..models.notification import (
    NotificationOut,
    NotificationMarkReadResponse,
    AdminSendNotificationRequest,
    AdminSendNotificationResponse,
    NotificationHistoryOut,
    SuccessResponse,
)
from ..deps import get_current_user, get_current_admin
from ..database import get_db
from ..crud import user_notification as crud_user_notification, notification as crud_notification
from ..crud import user as crud_user
from ..crud import membership as crud_membership
import datetime

router = APIRouter(
    prefix="/notification",
    tags=["notification"]
)

@router.get("/", response_model=List[NotificationOut])
def get_notifications(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_notes = crud_user_notification.list_user_notifications_by_user(db, current_user.id)
    result = []
    for un in user_notes:
        note = crud_notification.get_notification_by_id(db, un.notification_id)
        if note:
            result.append(NotificationOut(
                id=note.id,
                title=note.title,
                content=note.content,
                type=note.type,
                created_at=note.created_at,
                is_read=un.is_read,
                read_at=un.read_at
            ))
    return result

@router.put("/{id}/read", response_model=NotificationMarkReadResponse)
def mark_notification_read(
    id: int = Path(...),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    un_list = crud_user_notification.list_user_notifications_by_user(db, current_user.id)
    un = next((x for x in un_list if x.notification_id == id), None)
    if not un:
        return NotificationMarkReadResponse(success=False, msg="通知不存在或不属于该用户")
    if not un.is_read:
        crud_user_notification.update_user_notification(db, un, is_read=True, read_at=datetime.datetime.utcnow())
    return NotificationMarkReadResponse(success=True, msg="已标记为已读")

@router.post("/admin/send", response_model=AdminSendNotificationResponse)
def send_notification(
    data: AdminSendNotificationRequest = Body(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    if data.target == "specified" and (not data.user_ids or len(data.user_ids) == 0):
        return AdminSendNotificationResponse(success=False, msg="指定用户时user_ids不能为空", notification_id=None, user_count=0)
    if data.type not in ["info", "warning", "success"]:
        return AdminSendNotificationResponse(success=False, msg="通知类型错误", notification_id=None, user_count=0)
    if data.target not in ["all", "normal", "online", "local", "specified"]:
        return AdminSendNotificationResponse(success=False, msg="发送对象类型错误", notification_id=None, user_count=0)
    now = datetime.datetime.utcnow()
    notification = crud_notification.create_notification(db, title=data.title, content=data.content, type=data.type, created_at=now)
    user_ids = set()
    if data.target == "all":
        users = crud_user.list_all_users(db)
        user_ids = {u.id for u in users}
    elif data.target == "normal":
        users = crud_user.list_all_users(db)
        for u in users:
            memberships = crud_membership.get_membership_by_user(db, u.id)
            if not memberships:
                user_ids.add(u.id)
    elif data.target == "online":
        users = crud_user.list_all_users(db)
        for u in users:
            memberships = crud_membership.get_membership_by_user(db, u.id, type="online")
            if memberships:
                user_ids.add(u.id)
    elif data.target == "local":
        users = crud_user.list_all_users(db)
        for u in users:
            memberships = crud_membership.get_membership_by_user(db, u.id, type="local")
            if memberships:
                user_ids.add(u.id)
    elif data.target == "specified":
        user_ids = set(data.user_ids)
    if not user_ids:
        return AdminSendNotificationResponse(success=False, msg="没有符合条件的用户", notification_id=None, user_count=0)
    for uid in user_ids:
        crud_user_notification.create_user_notification(db, user_id=uid, notification_id=notification.id)
    return AdminSendNotificationResponse(
        success=True,
        msg=f"通知已发送给{len(user_ids)}个用户",
        notification_id=notification.id,
        user_count=len(user_ids)
    )

@router.get("/admin/history", response_model=List[NotificationHistoryOut])
def get_all_notifications(
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    notifications = db.query(crud_notification.Notification).order_by(crud_notification.Notification.created_at.desc()).all()
    return [NotificationHistoryOut.from_orm(n) for n in notifications] 