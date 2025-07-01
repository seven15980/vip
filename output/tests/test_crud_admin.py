import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openapi_server.models import Base
from openapi_server.models.admin import Admin
from openapi_server.crud.admin import (
    create_admin, get_admin_by_id, get_admin_by_username, list_admins, update_admin, delete_admin
)

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_create_and_get_admin():
    session = Session()
    admin = create_admin(session, username="admin1", password_hash="h1")
    assert admin.id is not None
    found = get_admin_by_id(session, admin.id)
    assert found.username == "admin1"
    found2 = get_admin_by_username(session, "admin1")
    assert found2.id == admin.id
    session.close()

def test_update_admin():
    session = Session()
    admin = create_admin(session, username="admin2", password_hash="h2")
    updated = update_admin(session, admin, password_hash="h2new")
    assert updated.password_hash == "h2new"
    session.close()

def test_list_and_delete_admins():
    session = Session()
    for i in range(5):
        create_admin(session, username=f"batchadmin{i}", password_hash="h3")
    admins = list_admins(session, skip=0, limit=3)
    assert len(admins) == 3
    admin = get_admin_by_username(session, "batchadmin0")
    delete_admin(session, admin)
    assert get_admin_by_username(session, "batchadmin0") is None
    session.close() 