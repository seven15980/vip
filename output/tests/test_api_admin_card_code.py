import pytest
from fastapi.testclient import TestClient
from openapi_server.main import app
from openapi_server.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.admin import Admin
from openapi_server.core.crypto import hash_password
from openapi_server.core.jwt import create_access_token
import os

TEST_DB_PATH = "output/tests/test_api_admin_card_code.db"
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

def get_admin_token(admin_id):
    return create_access_token({"admin_id": admin_id})

def test_batch_create_card_codes():
    session = TestingSessionLocal()
    admin = Admin(username="admin2", password_hash=hash_password("adminpass2"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    # 未登录
    resp = client.post("/api/admin/card-codes", json={"count": 3, "type": "both", "value": 365})
    assert resp.status_code == 401
    # 管理员登录
    resp2 = client.post("/api/admin/card-codes", json={"count": 3, "type": "both", "value": 365}, headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert len(data) == 3
    for item in data:
        assert item["value"] == 365
        assert item["type"] == "both"
        assert len(item["code"]) >= 12
        assert "created_at" in item
    session.close()

def test_list_card_codes():
    session = TestingSessionLocal()
    admin = Admin(username="admin3", password_hash=hash_password("adminpass3"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    # 插入多条卡密
    from openapi_server.models.card_code import CardCode
    for i in range(15):
        session.add(CardCode(code=f"CODE{i}", value=365, type="both", is_used=False))
    session.commit()
    # 未登录
    resp = client.get("/api/admin/card-codes?page=1&page_size=5")
    assert resp.status_code == 401
    # 管理员登录，第一页
    resp2 = client.get("/api/admin/card-codes?page=1&page_size=5", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert data["total"] >= 15
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["data"]) == 5
    # 第二页
    resp3 = client.get("/api/admin/card-codes?page=2&page_size=5", headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    data2 = resp3.json()["data"]
    assert data2["page"] == 2
    session.close()

def test_get_card_code_logs():
    session = TestingSessionLocal()
    admin = Admin(username="admin4", password_hash=hash_password("adminpass4"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    # 插入卡密和日志
    from openapi_server.models.card_code import CardCode
    from openapi_server.models.card_code_log import CardCodeLog
    card = CardCode(code="LOGTEST1", value=365, type="both", is_used=True)
    session.add(card)
    session.commit()
    # 无记录
    resp = client.get(f"/api/admin/card-codes/LOGTEST1/logs", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["data"] == []
    # 插入日志
    log1 = CardCodeLog(code="LOGTEST1", user_id=1, used_at=None, action="充值")
    log2 = CardCodeLog(code="LOGTEST1", user_id=2, used_at=None, action="续费")
    session.add_all([log1, log2])
    session.commit()
    resp2 = client.get(f"/api/admin/card-codes/LOGTEST1/logs", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert len(data) == 2
    actions = [d["action"] for d in data]
    assert "充值" in actions and "续费" in actions
    # 未登录
    resp3 = client.get(f"/api/admin/card-codes/LOGTEST1/logs")
    assert resp3.status_code == 401
    session.close() 