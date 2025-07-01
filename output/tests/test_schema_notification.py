import pytest
from pydantic import ValidationError
from openapi_server.schemas.notification import (
    NotificationInfo, UserNotificationInfo, NotificationListResponse, UserNotificationListResponse
)

def test_notification_info():
    n = NotificationInfo(id=1, title="t", content="c", type="system", created_at="2024-01-01T00:00:00Z")
    assert n.type == "system"
    with pytest.raises(ValidationError):
        NotificationInfo(id=1, title="t", content="c", type="system")  # 缺 created_at

def test_user_notification_info():
    n = NotificationInfo(id=2, title="t2", content="c2", type="private", created_at="2024-01-01T00:00:00Z")
    un = UserNotificationInfo(id=1, user_id=10, notification_id=2, is_read=False, read_at=None, notification=n)
    assert un.notification.id == 2
    assert un.is_read is False

def test_notification_list_response():
    resp = NotificationListResponse(notifications=[
        {"id": 1, "title": "t", "content": "c", "type": "system", "created_at": "2024-01-01T00:00:00Z"}
    ])
    assert len(resp.notifications) == 1
    assert resp.notifications[0].id == 1

def test_user_notification_list_response():
    n = {"id": 2, "title": "t2", "content": "c2", "type": "private", "created_at": "2024-01-01T00:00:00Z"}
    resp = UserNotificationListResponse(user_notifications=[
        {"id": 1, "user_id": 10, "notification_id": 2, "is_read": True, "read_at": "2024-01-02T00:00:00Z", "notification": n}
    ])
    assert len(resp.user_notifications) == 1
    assert resp.user_notifications[0].is_read is True 