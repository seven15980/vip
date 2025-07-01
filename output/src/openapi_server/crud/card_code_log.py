from sqlalchemy.orm import Session
from typing import Optional, List
from openapi_server.models.card_code_log import CardCodeLog
import datetime

def create_card_code_log(db: Session, code: str, user_id: int, used_at: Optional[datetime.datetime] = None, action: Optional[str] = None) -> CardCodeLog:
    log = CardCodeLog(code=code, user_id=user_id, used_at=used_at or datetime.datetime.utcnow(), action=action)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_card_code_log_by_id(db: Session, log_id: int) -> Optional[CardCodeLog]:
    return db.query(CardCodeLog).filter(CardCodeLog.id == log_id).first()


def list_card_code_logs(db: Session, skip: int = 0, limit: int = 100) -> List[CardCodeLog]:
    return db.query(CardCodeLog).offset(skip).limit(limit).all()


def list_logs_by_code(db: Session, code: str) -> List[CardCodeLog]:
    return db.query(CardCodeLog).filter(CardCodeLog.code == code).all()


def list_logs_by_user(db: Session, user_id: int) -> List[CardCodeLog]:
    return db.query(CardCodeLog).filter(CardCodeLog.user_id == user_id).all()


def delete_card_code_log(db: Session, log: CardCodeLog) -> None:
    db.delete(log)
    db.commit() 