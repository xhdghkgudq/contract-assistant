from app import app
from extensions import db
from models.user import User

with app.app_context():
    # 查询所有用户
    users = User.query.all()
    print("数据库中的用户:")
    for user in users:
        print(f"ID: {user.id}, 用户名: {user.username}, 密码: {user.password}, 角色: {user.role}")
