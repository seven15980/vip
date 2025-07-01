from sqlalchemy.orm import Session
from typing import Optional, List
from openapi_server.models.admin import Admin

def create_admin(db: Session, username: str, password_hash: str) -> Admin:
    admin = Admin(username=username, password_hash=password_hash)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def get_admin_by_id(db: Session, admin_id: int) -> Optional[Admin]:
    return db.query(Admin).filter(Admin.id == admin_id).first()


def get_admin_by_username(db: Session, username: str) -> Optional[Admin]:
    return db.query(Admin).filter(Admin.username == username).first()


def list_admins(db: Session, skip: int = 0, limit: int = 100) -> List[Admin]:
    return db.query(Admin).offset(skip).limit(limit).all()


def update_admin(db: Session, admin: Admin, **kwargs) -> Admin:
    for k, v in kwargs.items():
        setattr(admin, k, v)
    db.commit()
    db.refresh(admin)
    return admin


def delete_admin(db: Session, admin: Admin) -> None:
    db.delete(admin)
    db.commit() 