import pytest
from fastapi.testclient import TestClient
from openapi_server.main import app
from openapi_server.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.admin import Admin
from openapi_server.core.crypto import hash_password
import os

TEST_DB_PATH = "output/tests/test_api_admin.db"
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

def test_admin_login():
    session = TestingSessionLocal()
    admin = Admin(username="admin1", password_hash=hash_password("adminpass"))
    session.add(admin)
    session.commit()
    # 正确登录
    resp = client.post("/api/admin/login", json={"username": "admin1", "password": "adminpass"})
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    assert "token" in resp.json()["data"]
    # 错误密码
    resp2 = client.post("/api/admin/login", json={"username": "admin1", "password": "wrong"})
    assert resp2.status_code == 200
    assert resp2.json()["code"] != 0
    # 账号不存在
    resp3 = client.post("/api/admin/login", json={"username": "notexist", "password": "adminpass"})
    assert resp3.status_code == 200
    assert resp3.json()["code"] != 0
    session.close() 