from sqlalchemy.orm import Session
from typing import Optional, List
from openapi_server.models.user_notification import UserNotification
import datetime

def create_user_notification(db: Session, user_id: int, notification_id: int, is_read: bool = False, read_at: Optional[datetime.datetime] = None) -> UserNotification:
    un = UserNotification(user_id=user_id, notification_id=notification_id, is_read=is_read, read_at=read_at)
    db.add(un)
    db.commit()
    db.refresh(un)
    return un


def get_user_notification_by_id(db: Session, un_id: int) -> Optional[UserNotification]:
    return db.query(UserNotification).filter(UserNotification.id == un_id).first()


def list_user_notifications(db: Session, skip: int = 0, limit: int = 100) -> List[UserNotification]:
    return db.query(UserNotification).offset(skip).limit(limit).all()


def list_user_notifications_by_user(db: Session, user_id: int) -> List[UserNotification]:
    return db.query(UserNotification).filter(UserNotification.user_id == user_id).all()


def list_user_notifications_by_notification(db: Session, notification_id: int) -> List[UserNotification]:
    return db.query(UserNotification).filter(UserNotification.notification_id == notification_id).all()


def update_user_notification(db: Session, un: UserNotification, **kwargs) -> UserNotification:
    for k, v in kwargs.items():
        setattr(un, k, v)
    db.commit()
    db.refresh(un)
    return un


def delete_user_notification(db: Session, un: UserNotification) -> None:
    db.delete(un)
    db.commit() 