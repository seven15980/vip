import importlib
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

user_mod = importlib.import_module("openapi_server.models.user")
User = user_mod.User
notif_mod = importlib.import_module("openapi_server.models.notification")
Notification = notif_mod.Notification
mod = importlib.import_module("openapi_server.models.user_notification")
UserNotification = mod.UserNotification
from openapi_server.models import Base

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def enable_foreign_keys(session):
    session.execute(text("PRAGMA foreign_keys=ON"))

def test_create_user_notification():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="un1@example.com", password_hash="h1")
    notif = Notification(title="n1", content="c1", type="system")
    session.add(user)
    session.add(notif)
    session.commit()
    un = UserNotification(user_id=user.id, notification_id=notif.id)
    session.add(un)
    session.commit()
    assert un.id is not None
    assert un.is_read is False
    session.close()

def test_user_notification_foreign_key():
    session = Session()
    enable_foreign_keys(session)
    un = UserNotification(user_id=9999, notification_id=8888)
    session.add(un)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_update_user_notification():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="un2@example.com", password_hash="h2")
    notif = Notification(title="n2", content="c2", type="private")
    session.add(user)
    session.add(notif)
    session.commit()
    un = UserNotification(user_id=user.id, notification_id=notif.id)
    session.add(un)
    session.commit()
    un.is_read = True
    un.read_at = datetime.now()
    session.commit()
    assert un.is_read is True
    assert un.read_at is not None
    session.close()

def test_delete_user_notification():
    session = Session()
    enable_foreign_keys(session)
    user = User(email="un3@example.com", password_hash="h3")
    notif = Notification(title="n3", content="c3", type="system")
    session.add(user)
    session.add(notif)
    session.commit()
    un = UserNotification(user_id=user.id, notification_id=notif.id)
    session.add(un)
    session.commit()
    uid = un.id
    session.delete(un)
    session.commit()
    un2 = session.query(UserNotification).filter_by(id=uid).first()
    assert un2 is None
    session.close() 