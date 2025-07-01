from sqlalchemy.orm import Session
from typing import Optional, List
from openapi_server.models.card_code import CardCode

def create_card_code(db: Session, code: str, value: int, type: str) -> CardCode:
    card = CardCode(code=code, value=value, type=type, is_used=False)
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


def get_card_code_by_code(db: Session, code: str) -> Optional[CardCode]:
    return db.query(CardCode).filter(CardCode.code == code).first()


def get_card_code_by_id(db: Session, card_id: int) -> Optional[CardCode]:
    return db.query(CardCode).filter(CardCode.id == card_id).first()


def list_card_codes(db: Session, skip: int = 0, limit: int = 100) -> List[CardCode]:
    return db.query(CardCode).order_by(CardCode.created_at.desc()).offset(skip).limit(limit).all()


def update_card_code(db: Session, card: CardCode, **kwargs) -> CardCode:
    for k, v in kwargs.items():
        setattr(card, k, v)
    db.commit()
    db.refresh(card)
    return card


def delete_card_code(db: Session, card: CardCode) -> None:
    db.delete(card)
    db.commit() 