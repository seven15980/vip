import importlib
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

mod = importlib.import_module("openapi_server.models.notification")
Notification = mod.Notification
from openapi_server.models import Base

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_notification():
    session = Session()
    n = Notification(title="系统通知", content="欢迎使用", type="system")
    session.add(n)
    session.commit()
    assert n.id is not None
    assert n.created_at is not None
    session.close()

def test_update_notification():
    session = Session()
    n = Notification(title="私有通知", content="仅你可见", type="private")
    session.add(n)
    session.commit()
    n.content = "内容已修改"
    session.commit()
    assert n.content == "内容已修改"
    session.close()

def test_delete_notification():
    session = Session()
    n = Notification(title="删除测试", content="即将删除", type="system")
    session.add(n)
    session.commit()
    nid = n.id
    session.delete(n)
    session.commit()
    n2 = session.query(Notification).filter_by(id=nid).first()
    assert n2 is None
    session.close() 