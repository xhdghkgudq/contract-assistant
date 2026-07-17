from flask import Blueprint, request, jsonify
from models.user import User
import jwt, datetime

user_bp = Blueprint("user", __name__)

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"msg": "未提供认证令牌"}), 401
        try:
            if token.startswith("Bearer "):
                token = token[7:]
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = User.query.get(data["user_id"])
            if not current_user:
                return jsonify({"msg": "用户不存在"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"msg": "令牌已过期"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"msg": "无效的令牌"}), 401
        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

def admin_required(f):
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.role != "admin":
            return jsonify({"msg": "需要管理员权限"}), 403
        return f(current_user, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(username=data['username']).first()

    if user and user.password == data['password']:
        token = jwt.encode({
            "user_id": user.id,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, "secret", algorithm="HS256")

        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        })

    return jsonify({"msg": "用户名或密码错误"}), 401

@user_bp.route("/me", methods=["GET"])
@token_required
def get_current_user(current_user):
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    })