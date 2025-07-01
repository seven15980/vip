import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.notification import Notification
from openapi_server.crud.notification import (
    create_notification, get_notification_by_id, list_notifications, update_notification, delete_notification
)
import datetime

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_and_get_notification():
    session = Session()
    n = create_notification(session, title="系统通知", content="欢迎注册", type="system")
    assert n.id is not None
    found = get_notification_by_id(session, n.id)
    assert found.title == "系统通知"
    session.close()

def test_update_notification():
    session = Session()
    n = create_notification(session, title="私有通知", content="容量到期", type="private")
    updated = update_notification(session, n, content="容量已续费")
    assert updated.content == "容量已续费"
    session.close()

def test_list_and_delete_notifications():
    session = Session()
    for i in range(6):
        create_notification(session, title=f"批量{i}", content="内容", type="system")
    notes = list_notifications(session, skip=0, limit=3)
    assert len(notes) == 3
    n = notes[0]
    delete_notification(session, n)
    assert get_notification_by_id(session, n.id) is None
    session.close() 