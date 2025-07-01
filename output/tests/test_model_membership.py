import sys
import importlib
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

# 导入 user 和 membership
user_mod = importlib.import_module("openapi_server.models.user")
User = user_mod.User
mod = importlib.import_module("openapi_server.models.membership")
Membership = mod.Membership
from openapi_server.models import Base

# 复用 user 的 Base 以保证外键一致
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def enable_foreign_keys(session):
    session.execute(text("PRAGMA foreign_keys=ON"))

def test_create_membership():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="m1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    m = Membership(user_id=user.id, type="local", expire_at=datetime.now(), storage_total=None)
    session.add(m)
    session.commit()
    assert m.id is not None
    assert m.created_at is not None
    assert m.updated_at is not None
    session.close()

def test_membership_foreign_key():
    session = Session()
    enable_foreign_keys(session)
    # user_id 不存在应报错
    m = Membership(user_id=9999, type="online", expire_at=datetime.now(), storage_total=10)
    session.add(m)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_update_membership():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="m2@example.com", password_hash="h2")
    session.add(user)
    session.commit()
    m = Membership(user_id=user.id, type="online", expire_at=datetime.now(), storage_total=10)
    session.add(m)
    session.commit()
    old_updated = m.updated_at
    m.storage_total = 20
    session.commit()
    assert m.updated_at >= old_updated
    session.close()

def test_delete_membership():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="m3@example.com", password_hash="h3")
    session.add(user)
    session.commit()
    m = Membership(user_id=user.id, type="local", expire_at=datetime.now(), storage_total=None)
    session.add(m)
    session.commit()
    mid = m.id
    session.delete(m)
    session.commit()
    m2 = session.query(Membership).filter_by(id=mid).first()
    assert m2 is None
    session.close() 