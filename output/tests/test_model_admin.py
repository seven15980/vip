import importlib
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime

mod = importlib.import_module("openapi_server.models.admin")
Admin = mod.Admin
from openapi_server.models import Base

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_admin():
    session = Session()
    admin = Admin(username="admin1", password_hash="h1")
    session.add(admin)
    session.commit()
    assert admin.id is not None
    assert admin.created_at is not None
    session.close()

def test_admin_unique_username():
    session = Session()
    admin1 = Admin(username="uniqueadmin", password_hash="h1")
    admin2 = Admin(username="uniqueadmin", password_hash="h2")
    session.add(admin1)
    session.commit()
    session.add(admin2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()
    session.close()

def test_update_admin():
    session = Session()
    admin = Admin(username="updateadmin", password_hash="h1")
    session.add(admin)
    session.commit()
    admin.password_hash = "h2"
    session.commit()
    assert admin.password_hash == "h2"
    session.close()

def test_delete_admin():
    session = Session()
    admin = Admin(username="deladmin", password_hash="h1")
    session.add(admin)
    session.commit()
    aid = admin.id
    session.delete(admin)
    session.commit()
    admin2 = session.query(Admin).filter_by(id=aid).first()
    assert admin2 is None
    session.close() 