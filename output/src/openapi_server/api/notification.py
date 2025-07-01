from fastapi import APIRouter, Depends, Path, Body
from sqlalchemy.orm import Session
from openapi_server.deps import get_current_user, get_current_admin
from openapi_server.database import get_db
from openapi_server.crud import user_notification as crud_user_notification, notification as crud_notification
from openapi_server.crud import user as crud_user
from openapi_server.crud import membership as crud_membership
from openapi_server.core.response import success, error
from openapi_server.schemas.notification import AdminSendNotificationRequest
import datetime

router = APIRouter()

@router.get("/notifications")
def get_notifications(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # 联查 user_notification + notification
    user_notes = crud_user_notification.list_user_notifications_by_user(db, current_user.id)
    result = []
    for un in user_notes:
        note = crud_notification.get_notification_by_id(db, un.notification_id)
        if note:
            result.append({
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "type": note.type,
                "created_at": note.created_at.isoformat(),
                "is_read": un.is_read,
                "read_at": un.read_at.isoformat() if un.read_at else None
            })
    return success(result)

@router.put("/notifications/{id}/read")
def mark_notification_read(id: int = Path(...), current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    un_list = crud_user_notification.list_user_notifications_by_user(db, current_user.id)
    un = next((x for x in un_list if x.notification_id == id), None)
    if not un:
        return error("通知不存在或不属于该用户", code=404)
    if not un.is_read:
        crud_user_notification.update_user_notification(db, un, is_read=True, read_at=datetime.datetime.utcnow())
    return success()

@router.post("/admin/notifications")
def send_notification(
    data: AdminSendNotificationRequest = Body(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    # 参数校验
    if data.target == "specified" and (not data.user_ids or len(data.user_ids) == 0):
        return error("指定用户时user_ids不能为空", code=400)
    if data.type not in ["info", "warning", "success"]:
        return error("通知类型错误", code=400)
    if data.target not in ["all", "normal", "online", "local", "specified"]:
        return error("发送对象类型错误", code=400)

    # 1. 写入通知表
    now = datetime.datetime.utcnow()
    notification = crud_notification.create_notification(db, title=data.title, content=data.content, type=data.type, created_at=now)

    # 2. 获取目标用户
    user_ids = set()
    if data.target == "all":
        users = crud_user.list_all_users(db)
        user_ids = {u.id for u in users}
    elif data.target == "normal":
        users = crud_user.list_all_users(db)
        # 普通用户：没有任何会员资格的用户
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
        return error("没有符合条件的用户", code=400)

    # 3. 写入用户通知关联表
    for uid in user_ids:
        crud_user_notification.create_user_notification(db, user_id=uid, notification_id=notification.id)

    return success({
        "msg": f"通知已发送给{len(user_ids)}个用户",
        "notification_id": notification.id,
        "user_count": len(user_ids)
    })

@router.get("/admin/notifications/history")
def get_all_notifications(current_admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    notifications = db.query(crud_notification.Notification).order_by(crud_notification.Notification.created_at.desc()).all()
    result = []
    for n in notifications:
        result.append({
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "type": n.type,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        })
    return success(result) 