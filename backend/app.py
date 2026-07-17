from flask import Flask, make_response, request
from flask_cors import CORS
from extensions import db


def create_app():
    app = Flask(__name__)

    # ✅ 数据库配置（改成你的 contract_ai）
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/contract_ai'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ 初始化数据库
    db.init_app(app)

    # ✅ 全局OPTIONS处理中间件
    @app.before_request
    def handle_options():
        if request.method == 'OPTIONS':
            response = make_response()
            response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost:5173')
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = '3600'
            return response

    # ✅ 跨域配置 - 使用最简单可靠的配置
    CORS(app, resources={r"/*": {
        "origins": ["http://localhost:5173", "http://localhost:5174"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
        "supports_credentials": True,
        "max_age": 3600
    }})

    # ✅ 注册蓝图（路由）
    from routes.contract import contract_bp
    from routes.user import user_bp   # ⭐别忘了登录接口

    app.register_blueprint(contract_bp)
    app.register_blueprint(user_bp)

    # ✅ 测试接口（防止404）
    @app.route('/')
    def index():
        return {'msg': 'backend running'}

    return app


# 创建 app
app = create_app()


# ✅ 启动服务
if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # ⭐ 自动建表（非常关键）

    app.run(debug=False, host='0.0.0.0', port=5000)