import pytest
from fastapi.testclient import TestClient
from openapi_server.main import app
from openapi_server.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.user import User
from openapi_server.models.notification import Notification
from openapi_server.models.user_notification import UserNotification
import datetime
import os

TEST_DB_PATH = "output/tests/test_api_notification.db"
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

def test_notification_api():
    session = TestingSessionLocal()
    user = User(email="notify1@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    token = get_token(user.id)
    # 无通知
    resp = client.get("/api/notifications", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["data"] == []
    # 插入通知和关联
    note = Notification(title="系统通知", content="欢迎", type="system", created_at=datetime.datetime.utcnow())
    session.add(note)
    session.commit()
    un = UserNotification(user_id=user.id, notification_id=note.id, is_read=False)
    session.add(un)
    session.commit()
    # 获取通知
    resp2 = client.get("/api/notifications", headers={"Authorization": f"Bearer {token}"})
    assert resp2.status_code == 200
    data = resp2.json()["data"]
    assert len(data) == 1
    assert data[0]["is_read"] is False
    # 标记为已读
    resp3 = client.put(f"/api/notifications/{note.id}/read", headers={"Authorization": f"Bearer {token}"})
    assert resp3.status_code == 200
    # 再查已读
    resp4 = client.get("/api/notifications", headers={"Authorization": f"Bearer {token}"})
    assert resp4.json()["data"][0]["is_read"] is True
    session.close() 