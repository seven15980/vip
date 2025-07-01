import pytest
import requests

BASE = "http://localhost:8000"

@pytest.fixture(scope="module")
def admin_token():
    resp = requests.post(f"{BASE}/api/admin/login", json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    return resp.json()["data"]["token"]

@pytest.fixture(scope="module")
def user_token():
    # 注册新用户
    email = "pytest_user@test.com"
    password = "pytest123"
    requests.post(f"{BASE}/api/register", json={"email": email, "password": password})
    resp = requests.post(f"{BASE}/api/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    return resp.json()["data"]["token"]

def test_user_profile(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = requests.get(f"{BASE}/api/profile", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0

def test_membership_info(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = requests.get(f"{BASE}/api/membership", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0

def test_redeem(user_token, admin_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    # 获取一个未用卡密
    resp = requests.get(f"{BASE}/api/admin/card-codes?page=1&page_size=10", headers={"Authorization": f"Bearer {admin_token}"})
    code = next((c["code"] for c in resp.json()["data"]["data"] if not c["is_used"]), None)
    assert code
    resp2 = requests.post(f"{BASE}/api/redeem", json={"code": code}, headers=headers)
    assert resp2.status_code == 200

def test_notifications(user_token):
    headers = {"Authorization": f"Bearer {user_token}"}
    resp = requests.get(f"{BASE}/api/notifications", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0
    if resp.json()["data"]:
        note_id = resp.json()["data"][0]["id"]
        resp2 = requests.put(f"{BASE}/api/notifications/{note_id}/read", headers=headers)
        assert resp2.status_code == 200

def test_admin_membership_list(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = requests.get(f"{BASE}/api/admin/memberships?page=1&page_size=5", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0

def test_admin_statistics(admin_token):
    headers = {"Authorization": f"Bearer {admin_token}"}
    resp = requests.get(f"{BASE}/api/admin/statistics", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["code"] == 0 