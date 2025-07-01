from sqlalchemy.orm import Session
from typing import Optional, List
from openapi_server.models.membership import Membership


def create_membership(db: Session, user_id: int, type: str, expire_at, storage_total: Optional[int] = None) -> Membership:
    membership = Membership(user_id=user_id, type=type, expire_at=expire_at, storage_total=storage_total)
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


def get_membership_by_user(db: Session, user_id: int, type: Optional[str] = None) -> List[Membership]:
    q = db.query(Membership).filter(Membership.user_id == user_id)
    if type:
        q = q.filter(Membership.type == type)
    return q.all()


def get_membership_by_id(db: Session, membership_id: int) -> Optional[Membership]:
    return db.query(Membership).filter(Membership.id == membership_id).first()


def update_membership(db: Session, membership: Membership, **kwargs) -> Membership:
    for k, v in kwargs.items():
        setattr(membership, k, v)
    db.commit()
    db.refresh(membership)
    return membership


def delete_membership(db: Session, membership: Membership) -> None:
    db.delete(membership)
    db.commit()


def list_memberships(db: Session, skip: int = 0, limit: int = 100) -> List[Membership]:
    return db.query(Membership).offset(skip).limit(limit).all() 