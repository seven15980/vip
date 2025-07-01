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

TEST_DB_PATH = "output/tests/test_api_admin_membership.db"
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

def test_list_memberships():
    session = TestingSessionLocal()
    admin = Admin(username="admin5", password_hash=hash_password("adminpass5"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    # 插入多条会员
    from openapi_server.models.membership import Membership
    import datetime
    for i in range(12):
        session.add(Membership(user_id=i+1, type="local", expire_at=datetime.datetime.utcnow(), storage_total=None))
    session.commit()
    # 未登录
    resp = client.get("/api/admin/memberships?page=1&page_size=5")
    assert resp.status_code == 401
    # 管理员登录，第一页
    resp2 = client.get("/api/admin/memberships?page=1&page_size=5", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert data["total"] >= 12
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["data"]) == 5
    # 第二页
    resp3 = client.get("/api/admin/memberships?page=2&page_size=5", headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    data2 = resp3.json()["data"]
    assert data2["page"] == 2
    session.close()

def test_get_membership_detail():
    session = TestingSessionLocal()
    admin = Admin(username="admin6", password_hash=hash_password("adminpass6"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    from openapi_server.models.membership import Membership
    import datetime
    # 插入local/online会员
    session.add(Membership(user_id=100, type="local", expire_at=datetime.datetime.utcnow(), storage_total=None))
    session.add(Membership(user_id=100, type="online", expire_at=datetime.datetime.utcnow(), storage_total=20))
    session.commit()
    # 未登录
    resp = client.get("/api/admin/memberships/100")
    assert resp.status_code == 401
    # 管理员登录
    resp2 = client.get("/api/admin/memberships/100", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert len(data) == 2
    types = [d["type"] for d in data]
    assert "local" in types and "online" in types
    session.close()

def test_admin_renew_membership():
    session = TestingSessionLocal()
    admin = Admin(username="admin7", password_hash=hash_password("adminpass7"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    from openapi_server.models.membership import Membership
    import datetime
    # 新建local会员
    resp = client.post("/api/admin/memberships/200/renew", json={"type": "local", "months": 2, "storage": 0}, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["type"] == "local"
    # 新建online会员
    resp2 = client.post("/api/admin/memberships/201/renew", json={"type": "online", "months": 1, "storage": 10}, headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data2 = resp2.json()["data"]
    assert data2["type"] == "online"
    assert data2["storage_total"] == 10
    # 续费叠加
    session.add(Membership(user_id=202, type="online", expire_at=datetime.datetime.utcnow(), storage_total=10))
    session.commit()
    resp3 = client.post("/api/admin/memberships/202/renew", json={"type": "online", "months": 2, "storage": 20}, headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    data3 = resp3.json()["data"]
    assert data3["storage_total"] == 30
    # 未登录
    resp4 = client.post("/api/admin/memberships/203/renew", json={"type": "local", "months": 1, "storage": 0})
    assert resp4.status_code == 401
    session.close()

def test_get_statistics():
    session = TestingSessionLocal()
    admin = Admin(username="admin8", password_hash=hash_password("adminpass8"))
    session.add(admin)
    session.commit()
    token = get_admin_token(admin.id)
    from openapi_server.models.user import User
    from openapi_server.models.membership import Membership
    from openapi_server.models.card_code import CardCode
    import datetime
    # 插入数据
    session.add(User(email="u1@a.com", password_hash="h1"))
    session.add(User(email="u2@a.com", password_hash="h2"))
    session.add(Membership(user_id=1, type="local", expire_at=datetime.datetime.utcnow(), storage_total=None))
    session.add(CardCode(code="C1", value=365, type="both", is_used=True))
    session.add(CardCode(code="C2", value=365, type="both", is_used=False))
    session.commit()
    # 未登录
    resp = client.get("/api/admin/statistics")
    assert resp.status_code == 401
    # 管理员登录
    resp2 = client.get("/api/admin/statistics", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert data["user_count"] >= 2
    assert data["membership_count"] >= 1
    assert data["card_code_used_count"] >= 1
    session.close() 