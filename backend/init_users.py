from app import app
from extensions import db
from models.user import User

with app.app_context():
    # 检查是否已有用户
    existing_user = User.query.first()
    if not existing_user:
        # 创建默认用户
        user = User(
            username='admin',
            password='123456'
        )
        db.session.add(user)
        db.session.commit()
        print('默认用户创建成功！')
        print('用户名: admin')
        print('密码: 123456')
    else:
        print('用户已存在，跳过初始化。')
