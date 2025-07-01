import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from sqlalchemy.orm import Session
from openapi_server.database import SessionLocal, engine
from openapi_server.models.user import User
from openapi_server.models.membership import Membership
from openapi_server.models.card_code import CardCode
from openapi_server.models.admin import Admin
from openapi_server.models.notification import Notification
from openapi_server.models.user_notification import UserNotification
from openapi_server.core.crypto import hash_password
from openapi_server.models import Base
import datetime

# 初始化数据库会话
Session = SessionLocal()

# 自动建表
Base.metadata.create_all(bind=engine)

# 批量用户
for i in range(1, 21):
    user = User(email=f"user{i}@test.com", password_hash=hash_password("test123"))
    Session.add(user)
Session.commit()

# 批量会员
for i in range(1, 21):
    Session.add(Membership(user_id=i, type="local", expire_at=datetime.datetime.utcnow() + datetime.timedelta(days=365)))
    Session.add(Membership(user_id=i, type="online", expire_at=datetime.datetime.utcnow() + datetime.timedelta(days=365), storage_total=10*i))
Session.commit()

# 批量卡密
for i in range(1, 51):
    Session.add(CardCode(code=f"CODE{i:04d}", value=365, type="both", is_used=(i%3==0), used_by=(i if i%3==0 else None)))
Session.commit()

# 批量通知
for i in range(1, 6):
    note = Notification(title=f"系统通知{i}", content=f"内容{i}", type="system", created_at=datetime.datetime.utcnow())
    Session.add(note)
Session.commit()

# 用户通知关联
for i in range(1, 21):
    for note_id in range(1, 6):
        Session.add(UserNotification(user_id=i, notification_id=note_id, is_read=(note_id%2==0)))
Session.commit()

# 管理员
if not Session.query(Admin).filter_by(username="admin").first():
    Session.add(Admin(username="admin", password_hash=hash_password("admin123")))
    Session.commit()
# 新增 admin123 管理员
if not Session.query(Admin).filter_by(username="admin123").first():
    Session.add(Admin(username="admin123", password_hash=hash_password("admin123")))
    Session.commit()

Session.close()
print("测试数据已生成") 