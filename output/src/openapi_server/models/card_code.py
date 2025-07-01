from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from . import Base

class CardCode(Base):
    __tablename__ = "card_code"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String, unique=True, nullable=False, index=True)
    value = Column(Integer, nullable=False)
    type = Column(String, nullable=False)  # local/online/both
    is_used = Column(Boolean, default=False, nullable=False)
    used_by = Column(Integer, ForeignKey("user.id"), nullable=True)
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=False) 