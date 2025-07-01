import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.card_code import CardCode
from openapi_server.models.user import User
from openapi_server.crud.card_code import (
    create_card_code, get_card_code_by_code, get_card_code_by_id, list_card_codes, update_card_code, delete_card_code
)
import datetime

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # 确保 user/card_code 等所有依赖表都被创建
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_and_get_card_code():
    session = Session()
    card = create_card_code(session, code="CODE123", value=365, type="local")
    assert card.id is not None
    found = get_card_code_by_code(session, "CODE123")
    assert found is not None
    found2 = get_card_code_by_id(session, card.id)
    assert found2.code == "CODE123"
    session.close()

def test_update_card_code():
    session = Session()
    # 先插入 user 以满足外键
    user = User(email="carduser@example.com", password_hash="h1")
    session.add(user)
    session.commit()
    card = create_card_code(session, code="CODE456", value=365, type="online")
    updated = update_card_code(session, card, is_used=True, used_by=user.id, used_at=datetime.datetime(2024,1,1,0,0,0))
    assert updated.is_used is True
    assert updated.used_by == user.id
    assert updated.used_at.year == 2024
    session.close()

def test_list_and_delete_card_codes():
    session = Session()
    # 批量创建
    for i in range(10):
        create_card_code(session, code=f"BATCH{i}", value=365, type="both")
    cards = list_card_codes(session, skip=0, limit=5)
    assert len(cards) == 5
    # 删除
    card = get_card_code_by_code(session, "BATCH0")
    delete_card_code(session, card)
    assert get_card_code_by_code(session, "BATCH0") is None
    session.close() 