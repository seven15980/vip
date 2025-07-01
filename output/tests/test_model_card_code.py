import importlib
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

user_mod = importlib.import_module("openapi_server.models.user")
User = user_mod.User
mod = importlib.import_module("openapi_server.models.card_code")
CardCode = mod.CardCode
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

def test_create_card_code():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="c1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    code = CardCode(code="CODE123", value=365, type="local", is_used=False, used_by=None)
    session.add(code)
    session.commit()
    assert code.id is not None
    assert code.created_at is not None
    session.close()

def test_card_code_unique():
    session = Session()
    enable_foreign_keys(session)
    code1 = CardCode(code="UNIQUE1", value=365, type="local", is_used=False)
    code2 = CardCode(code="UNIQUE1", value=365, type="local", is_used=False)
    session.add(code1)
    session.commit()
    session.add(code2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_card_code_foreign_key():
    session = Session()
    enable_foreign_keys(session)
    code = CardCode(code="FKTEST", value=365, type="local", is_used=True, used_by=9999)
    session.add(code)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_update_card_code():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="c2@example.com", password_hash="h2")
    session.add(user)
    session.commit()
    code = CardCode(code="UPDTEST", value=365, type="online", is_used=False)
    session.add(code)
    session.commit()
    code.is_used = True
    code.used_by = user.id
    code.used_at = datetime.now()
    session.commit()
    assert code.is_used is True
    assert code.used_by == user.id
    assert code.used_at is not None
    session.close()

def test_delete_card_code():
    session = Session()
    enable_foreign_keys(session)
    code = CardCode(code="DELTEST", value=365, type="both", is_used=False)
    session.add(code)
    session.commit()
    cid = code.id
    session.delete(code)
    session.commit()
    code2 = session.query(CardCode).filter_by(id=cid).first()
    assert code2 is None
    session.close() 