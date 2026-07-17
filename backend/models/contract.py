from extensions import db
from datetime import datetime

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    contract_number = db.Column(db.String(100), comment='合同编号')
    party_a = db.Column(db.String(255), comment='甲方')
    party_b = db.Column(db.String(255), comment='乙方')
    service_content = db.Column(db.Text, comment='服务内容')
    service_period = db.Column(db.String(255), comment='服务期限')
    service_fee = db.Column(db.String(100), comment='服务费用')
    payment_method = db.Column(db.String(255), comment='支付方式')
    party_a_rights = db.Column(db.Text, comment='甲方权利义务')
    party_b_rights = db.Column(db.Text, comment='乙方权利义务')
    acceptance_standard = db.Column(db.Text, comment='验收标准')
    liability = db.Column(db.Text, comment='违约责任')
    dispute_resolution = db.Column(db.Text, comment='争议解决')
    signing_date = db.Column(db.DateTime, comment='签署日期')
    content = db.Column(db.Text)
    name = db.Column(db.String(255), comment='合同名称')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_date = db.Column(db.DateTime, nullable=True)
    result = db.Column(db.Text)
    subject_ok = db.Column(db.Boolean, default=False)
    object_clear = db.Column(db.Boolean, default=False)
    price_clear = db.Column(db.Boolean, default=False)
    performable = db.Column(db.Boolean, default=False)
    is_compliant = db.Column(db.Boolean, default=False)
    is_void = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='pending', comment='审核状态: pending, approved, rejected')
    reject_reason = db.Column(db.Text, comment='审核不通过理由')
