import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..", "src")))
import importlib
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

mod = importlib.import_module("openapi_server.models.user")
User = mod.User
from openapi_server.models import Base

# 使用内存数据库做测试
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_user():
    session = Session()
    user = User(email="test@example.com", password_hash="hash")
    session.add(user)
    session.commit()
    assert user.id is not None
    assert user.is_active is True
    assert user.created_at is not None
    assert user.updated_at is not None
    session.close()

def test_unique_email():
    session = Session()
    user1 = User(email="unique@example.com", password_hash="h1")
    user2 = User(email="unique@example.com", password_hash="h2")
    session.add(user1)
    session.commit()
    session.add(user2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_update_user():
    session = Session()
    user = User(email="update@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    old_updated = user.updated_at
    user.password_hash = "h2"
    session.commit()
    assert user.updated_at >= old_updated
    session.close()

def test_delete_user():
    session = Session()
    user = User(email="delete@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    uid = user.id
    session.delete(user)
    session.commit()
    user2 = session.query(User).filter_by(id=uid).first()
    assert user2 is None
    session.close() 