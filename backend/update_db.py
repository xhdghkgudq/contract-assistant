from app import app
from extensions import db
from models.contract import Contract
from models.review import Review

with app.app_context():
    # 先删除所有表
    db.drop_all()
    # 重新创建所有表
    db.create_all()
    print('数据库表结构更新成功！')
