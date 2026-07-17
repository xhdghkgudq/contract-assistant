from app import app
from extensions import db
from models.contract import Contract
from models.review import Review
from datetime import datetime, timedelta

with app.app_context():
    # 计算两天前的日期
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    
    # 删除两天前的合同和相关的审查记录
    old_contracts = Contract.query.filter(Contract.created_at < two_days_ago).all()
    
    deleted_count = 0
    for contract in old_contracts:
        # 删除相关的审查记录
        review = Review.query.filter_by(contract_id=contract.id).first()
        if review:
            db.session.delete(review)
        
        # 删除合同
        db.session.delete(contract)
        deleted_count += 1
    
    db.session.commit()
    print(f'删除了 {deleted_count} 条两天前的合同数据')
