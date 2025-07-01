import pytest
from fastapi.testclient import TestClient
from openapi_server.main import app
from openapi_server.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
import os

TEST_DB_PATH = "output/tests/test_api_user.db"
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

def test_register_and_login():
    # 注册
    resp = client.post("/api/register", json={"email": "apiuser@example.com", "password": "pass1234"})
    print("register resp:", resp.status_code, resp.text)
    assert resp.status_code == 200
    # 重复注册
    resp2 = client.post("/api/register", json={"email": "apiuser@example.com", "password": "pass1234"})
    print("register again resp:", resp2.status_code, resp2.text)
    assert resp2.status_code == 200
    assert resp2.json()["code"] != 0
    # 登录
    resp3 = client.post("/api/login", json={"email": "apiuser@example.com", "password": "pass1234"})
    print("login resp:", resp3.status_code, resp3.text)
    assert resp3.status_code == 200
    token = resp3.json()["data"]["token"]
    assert token
    return token

def test_profile_and_update():
    token = test_register_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    # 获取个人信息
    resp = client.get("/api/profile", headers=headers)
    print("profile resp:", resp.status_code, resp.text)
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == "apiuser@example.com"
    # 修改密码
    resp2 = client.put("/api/profile", json={"password": "newpass123"}, headers=headers)
    print("update profile resp:", resp2.status_code, resp2.text)
    assert resp2.status_code == 200
    # 用新密码登录
    resp3 = client.post("/api/login", json={"email": "apiuser@example.com", "password": "newpass123"})
    print("login with new password resp:", resp3.status_code, resp3.text)
    assert resp3.status_code == 200 