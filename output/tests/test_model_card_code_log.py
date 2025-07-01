import importlib
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

user_mod = importlib.import_module("openapi_server.models.user")
User = user_mod.User
mod = importlib.import_module("openapi_server.models.card_code_log")
CardCodeLog = mod.CardCodeLog
from openapi_server.models import Base

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def enable_foreign_keys(session):
    session.execute(text("PRAGMA foreign_keys=ON"))

def test_create_card_code_log():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="log1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    log = CardCodeLog(code="LOGCODE1", user_id=user.id, action="充值本地会员一年")
    session.add(log)
    session.commit()
    assert log.id is not None
    assert log.used_at is not None
    session.close()

def test_card_code_log_foreign_key():
    session = Session()
    enable_foreign_keys(session)
    log = CardCodeLog(code="LOGCODE2", user_id=9999, action="充值线上会员")
    session.add(log)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_update_card_code_log():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="log2@example.com", password_hash="h2")
    session.add(user)
    session.commit()
    log = CardCodeLog(code="LOGCODE3", user_id=user.id, action="初始")
    session.add(log)
    session.commit()
    log.action = "后台续费"
    session.commit()
    assert log.action == "后台续费"
    session.close()

def test_delete_card_code_log():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="log3@example.com", password_hash="h3")
    session.add(user)
    session.commit()
    log = CardCodeLog(code="LOGCODE4", user_id=user.id, action="删除测试")
    session.add(log)
    session.commit()
    lid = log.id
    session.delete(log)
    session.commit()
    log2 = session.query(CardCodeLog).filter_by(id=lid).first()
    assert log2 is None
    session.close() 