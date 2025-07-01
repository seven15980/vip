import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.user import User
from openapi_server.models.notification import Notification
from openapi_server.models.user_notification import UserNotification
from openapi_server.crud.user_notification import (
    create_user_notification, get_user_notification_by_id, list_user_notifications, list_user_notifications_by_user, list_user_notifications_by_notification, update_user_notification, delete_user_notification
)
import datetime

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_and_get_user_notification():
    session = Session()
    user = User(email="unuser@example.com", password_hash="h1")
    note = Notification(title="n1", content="c1", type="system")
    session.add_all([user, note])
    session.commit()
    un = create_user_notification(session, user_id=user.id, notification_id=note.id)
    assert un.id is not None
    found = get_user_notification_by_id(session, un.id)
    assert found.user_id == user.id
    assert found.notification_id == note.id
    session.close()

def test_list_by_user_and_notification():
    session = Session()
    user1 = User(email="unuser2@example.com", password_hash="h2")
    user2 = User(email="unuser3@example.com", password_hash="h3")
    note1 = Notification(title="n2", content="c2", type="system")
    note2 = Notification(title="n3", content="c3", type="private")
    session.add_all([user1, user2, note1, note2])
    session.commit()
    # 插入多条
    for i in range(4):
        create_user_notification(session, user_id=user1.id, notification_id=note1.id)
    for i in range(2):
        create_user_notification(session, user_id=user2.id, notification_id=note2.id)
    uns1 = list_user_notifications_by_user(session, user1.id)
    assert len(uns1) == 4
    uns2 = list_user_notifications_by_notification(session, note2.id)
    assert len(uns2) == 2
    session.close()

def test_update_and_delete_user_notification():
    session = Session()
    user = User(email="unuser4@example.com", password_hash="h4")
    note = Notification(title="n4", content="c4", type="system")
    session.add_all([user, note])
    session.commit()
    un = create_user_notification(session, user_id=user.id, notification_id=note.id)
    updated = update_user_notification(session, un, is_read=True, read_at=datetime.datetime(2024,1,1,0,0,0))
    assert updated.is_read is True
    assert updated.read_at.year == 2024
    delete_user_notification(session, updated)
    assert get_user_notification_by_id(session, updated.id) is None
    session.close()

def test_list_user_notifications():
    session = Session()
    user = User(email="unuser5@example.com", password_hash="h5")
    note = Notification(title="n5", content="c5", type="system")
    session.add_all([user, note])
    session.commit()
    for i in range(6):
        create_user_notification(session, user_id=user.id, notification_id=note.id)
    uns = list_user_notifications(session, skip=0, limit=3)
    assert len(uns) == 3
    session.close() 