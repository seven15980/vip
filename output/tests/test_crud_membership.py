import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.user import User
from openapi_server.models.membership import Membership
from openapi_server.crud.membership import (
    create_membership, get_membership_by_user, get_membership_by_id, update_membership, delete_membership
)
import datetime

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def enable_foreign_keys(session):
    session.execute(text("PRAGMA foreign_keys=ON"))

def test_create_and_get_membership():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="mcrud1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    expire_at = datetime.datetime(2025, 1, 1, 0, 0, 0)
    m = create_membership(session, user_id=user.id, type="local", expire_at=expire_at)
    assert m.id is not None
    found = get_membership_by_user(session, user.id)
    assert len(found) == 1
    found2 = get_membership_by_id(session, m.id)
    assert found2.user_id == user.id
    session.close()

def test_update_membership():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="mcrud2@example.com", password_hash="h2")
    session.add(user)
    session.commit()
    expire_at = datetime.datetime(2025, 1, 1, 0, 0, 0)
    m = create_membership(session, user_id=user.id, type="online", expire_at=expire_at, storage_total=10)
    updated = update_membership(session, m, storage_total=20)
    assert updated.storage_total == 20
    session.close()

def test_delete_membership():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="mcrud3@example.com", password_hash="h3")
    session.add(user)
    session.commit()
    expire_at = datetime.datetime(2025, 1, 1, 0, 0, 0)
    m = create_membership(session, user_id=user.id, type="local", expire_at=expire_at)
    mid = m.id
    delete_membership(session, m)
    found = get_membership_by_id(session, mid)
    assert found is None
    session.close() 