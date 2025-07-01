from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey, func
from . import Base

class UserNotification(Base):
    __tablename__ = "user_notification"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    notification_id = Column(Integer, ForeignKey("notification.id"), nullable=False, index=True)
    is_read = Column(Boolean, default=False, nullable=False)
    read_at = Column(DateTime, nullable=True) 