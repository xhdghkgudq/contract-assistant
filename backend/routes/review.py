from datetime import datetime
from extensions import db   # ✅ 改这里（核心修复）

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    # 关联合同
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)

    # AI整体结果（JSON字符串）
    result = db.Column(db.Text)

    # 各项分析字段
    subject_ok = db.Column(db.Boolean)
    object_clear = db.Column(db.Boolean)
    price_clear = db.Column(db.Boolean)
    performable = db.Column(db.Boolean)
    liability = db.Column(db.Text)
    dispute = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "result": self.result,
            "subject_ok": self.subject_ok,
            "object_clear": self.object_clear,
            "price_clear": self.price_clear,
            "performable": self.performable,
            "liability": self.liability,
            "dispute": self.dispute,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }