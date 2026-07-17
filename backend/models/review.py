from datetime import datetime
from extensions import db

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=False)

    result = db.Column(db.Text)

    subject_ok = db.Column(db.Boolean, default=False)
    object_clear = db.Column(db.Boolean, default=False)
    price_clear = db.Column(db.Boolean, default=False)
    performable = db.Column(db.Boolean, default=False)
    is_compliant = db.Column(db.Boolean, default=False)  # 是否合规
    liability = db.Column(db.Text)
    dispute = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)