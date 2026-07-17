from app import app
from extensions import db
from models.contract import Contract
from models.review import Review
from datetime import datetime

with app.app_context():
    # 获取所有合同
    contracts = Contract.query.all()
    
    print(f'共有 {len(contracts)} 份合同')
    print('=' * 100)
    
    for contract in contracts:
        review = Review.query.filter_by(contract_id=contract.id).first()
        
        print(f'合同ID: {contract.id}')
        print(f'合同名称: {contract.name}')
        print(f'创建时间: {contract.created_at}')
        print(f'到期时间: {contract.expire_date}')
        if review:
            print(f'主体明确: {review.subject_ok}')
            print(f'标的明确: {review.object_clear}')
            print(f'价格明确: {review.price_clear}')
            print(f'可执行性: {review.performable}')
            print(f'合规状态: {review.is_compliant}')
        else:
            print('暂无审查记录')
        print('-' * 100)
