from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from . import Base

class CardCodeLog(Base):
    __tablename__ = "card_code_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    used_at = Column(DateTime, default=func.now(), nullable=False)
    action = Column(String, nullable=True) 