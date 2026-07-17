from extensions import db   # ✅ 必须这样

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(255))
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=db.func.now())