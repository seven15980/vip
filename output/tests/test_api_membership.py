import pytest
from fastapi.testclient import TestClient
from openapi_server.main import app
from openapi_server.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.user import User
from openapi_server.models.membership import Membership
import datetime
import os

TEST_DB_PATH = "output/tests/test_api_membership.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def get_token(user_id):
    from openapi_server.core.jwt import create_access_token
    return create_access_token({"user_id": user_id})

def test_membership_info():
    session = TestingSessionLocal()
    # 创建用户和会员
    user = User(email="m1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    token = get_token(user.id)
    # 无会员
    resp = client.get("/api/membership", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["data"] == {}
    # 有本地会员
    m1 = Membership(user_id=user.id, type="local", expire_at=datetime.datetime(2025,1,1,0,0,0))
    session.add(m1)
    session.commit()
    resp2 = client.get("/api/membership", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    assert "local" in resp2.json()["data"]
    # 有线上会员
    m2 = Membership(user_id=user.id, type="online", expire_at=datetime.datetime(2026,1,1,0,0,0), storage_total=20)
    session.add(m2)
    session.commit()
    resp3 = client.get("/api/membership", headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    assert "online" in resp3.json()["data"]
    session.close()

def test_smoke():
    assert True 