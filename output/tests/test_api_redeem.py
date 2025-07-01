import pytest
from fastapi.testclient import TestClient
from openapi_server.main import app
from openapi_server.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.user import User
from openapi_server.models.card_code import CardCode
from openapi_server.models.membership import Membership
import datetime
import os

TEST_DB_PATH = "output/tests/test_api_redeem.db"
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

def test_redeem_card():
    session = TestingSessionLocal()
    user = User(email="redeem1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    token = get_token(user.id)
    # 创建本地卡密
    card = CardCode(code="CODELOCAL1", value=365, type="local", is_used=False)
    session.add(card)
    session.commit()
    # 正常兑换
    resp = client.post("/api/redeem", json={"code": "CODELOCAL1"}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    # 重复兑换
    resp2 = client.post("/api/redeem", json={"code": "CODELOCAL1"}, headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    assert resp2.json()["code"] != 0
    # 线上卡密
    card2 = CardCode(code="CODEONLINE1", value=365, type="online", is_used=False)
    session.add(card2)
    session.commit()
    resp3 = client.post("/api/redeem", json={"code": "CODEONLINE1"}, headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    assert resp3.json()["code"] == 0
    # 叠加线上会员
    resp4 = client.post("/api/redeem", json={"code": "CODEONLINE1"}, headers={"Authorization": f"Bearer {token}"})
    assert resp4.json()["code"] != 0
    session.close() 