import importlib
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.user import User
from openapi_server.crud.user import (
    create_user, get_user_by_email, get_user_by_id, update_user_password, delete_user
)

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_and_get_user():
    session = Session()
    user = create_user(session, email="crud1@example.com", password_hash="h1")
    assert user.id is not None
    found = get_user_by_email(session, "crud1@example.com")
    assert found is not None
    assert found.id == user.id
    found2 = get_user_by_id(session, user.id)
    assert found2.email == "crud1@example.com"
    session.close()

def test_update_user_password():
    session = Session()
    user = create_user(session, email="crud2@example.com", password_hash="h2")
    updated = update_user_password(session, user, "h2new")
    assert updated.password_hash == "h2new"
    session.close()

def test_delete_user():
    session = Session()
    user = create_user(session, email="crud3@example.com", password_hash="h3")
    uid = user.id
    delete_user(session, user)
    found = get_user_by_id(session, uid)
    assert found is None
    session.close() 