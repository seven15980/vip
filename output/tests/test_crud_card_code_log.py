import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.card_code_log import CardCodeLog
from openapi_server.models.user import User
from openapi_server.crud.card_code_log import (
    create_card_code_log, get_card_code_log_by_id, list_card_code_logs, list_logs_by_code, list_logs_by_user, delete_card_code_log
)
import datetime

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_and_get_card_code_log():
    session = Session()
    user = User(email="loguser@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    log = create_card_code_log(session, code="LOGCODE1", user_id=user.id, action="充值本地会员一年")
    assert log.id is not None
    found = get_card_code_log_by_id(session, log.id)
    assert found.code == "LOGCODE1"
    session.close()

def test_list_logs_by_code_and_user():
    session = Session()
    user1 = User(email="loguser2@example.com", password_hash="h2")
    user2 = User(email="loguser3@example.com", password_hash="h3")
    session.add_all([user1, user2])
    session.commit()
    # 插入多条
    for i in range(5):
        create_card_code_log(session, code="CODEA", user_id=user1.id, action="A")
    for i in range(3):
        create_card_code_log(session, code="CODEB", user_id=user2.id, action="B")
    logs_a = list_logs_by_code(session, "CODEA")
    assert len(logs_a) == 5
    logs_b = list_logs_by_user(session, user2.id)
    assert len(logs_b) == 3
    session.close()

def test_list_and_delete_card_code_logs():
    session = Session()
    user = User(email="loguser4@example.com", password_hash="h4")
    session.add(user)
    session.commit()
    for i in range(7):
        create_card_code_log(session, code=f"BATCHLOG{i}", user_id=user.id, action="batch")
    logs = list_card_code_logs(session, skip=0, limit=4)
    assert len(logs) == 4
    log = logs[0]
    delete_card_code_log(session, log)
    assert get_card_code_log_by_id(session, log.id) is None
    session.close() 