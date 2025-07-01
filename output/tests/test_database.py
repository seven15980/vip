import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session
import sys
import importlib

# 动态导入 database.py
if "openapi_server.database" in sys.modules:
    del sys.modules["openapi_server.database"]
dbmod = importlib.import_module("openapi_server.database")

Base = dbmod.Base
engine = dbmod.engine
SessionLocal = dbmod.SessionLocal

def setup_module(module):
    # 定义临时表
    class User(Base):
        __tablename__ = "test_user"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)
    module.User = User
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

def test_session_crud():
    # 测试Session获取和基本CRUD
    session: Session = SessionLocal()
    # 插入
    user = User(name="testuser")
    session.add(user)
    session.commit()
    session.refresh(user)
    assert user.id is not None
    # 查询
    user2 = session.query(User).filter_by(name="testuser").first()
    assert user2 is not None
    assert user2.name == "testuser"
    # 删除
    session.delete(user2)
    session.commit()
    user3 = session.query(User).filter_by(name="testuser").first()
    assert user3 is None
    session.close()

def test_get_db():
    # 测试 get_db 依赖生成Session
    gen = dbmod.get_db()
    session = next(gen)
    assert isinstance(session, Session)
    # 关闭
    try:
        next(gen)
    except StopIteration:
        pass 