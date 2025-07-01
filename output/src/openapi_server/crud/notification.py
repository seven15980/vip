from sqlalchemy.orm import Session
from typing import Optional, List
from openapi_server.models.notification import Notification
import datetime

def create_notification(db: Session, title: str, content: str, type: str, created_at: Optional[datetime.datetime] = None) -> Notification:
    notification = Notification(title=title, content=content, type=type, created_at=created_at or datetime.datetime.utcnow())
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_notification_by_id(db: Session, notification_id: int) -> Optional[Notification]:
    return db.query(Notification).filter(Notification.id == notification_id).first()


def list_notifications(db: Session, skip: int = 0, limit: int = 100) -> List[Notification]:
    return db.query(Notification).offset(skip).limit(limit).all()


def update_notification(db: Session, notification: Notification, **kwargs) -> Notification:
    for k, v in kwargs.items():
        setattr(notification, k, v)
    db.commit()
    db.refresh(notification)
    return notification


def delete_notification(db: Session, notification: Notification) -> None:
    db.delete(notification)
    db.commit() 