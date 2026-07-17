from flask import Blueprint, request, jsonify, make_response, g
import json
import os
import pdfplumber
from extensions import db
from models import Contract, Review, User   # ✅ 统一入口（关键！）
from services.ai import analyze_contract
from datetime import datetime
from utils.auth import verify_token

contract_bp = Blueprint("contract", __name__)


def _safe_text(val, default=""):
    """AI 或前端偶发传入 dict/list 时写入 MySQL 会报错，统一转成可存库的字符串。"""
    if val is None:
        return default
    if isinstance(val, (dict, list)):
        return json.dumps(val, ensure_ascii=False)
    return str(val)

# 认证中间件
from functools import wraps
def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # OPTIONS请求直接返回200 OK和正确的CORS头
        if request.method == 'OPTIONS':
            response = make_response()
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost:5173')
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
        
        token = request.headers.get('Authorization')
        if token:
            # 移除Bearer前缀
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_info = verify_token(token)
            if not user_info:
                return jsonify({"msg": "无效的认证令牌"}), 401
            
            # 获取用户信息并存入g对象
            user = User.query.get(user_info.get('user_id'))
            if user:
                g.user = user
            else:
                return jsonify({"msg": "用户不存在"}), 401
        else:
            return jsonify({"msg": "未提供认证令牌"}), 401
        
        return f(*args, **kwargs)
    return wrapper

# 管理员权限检查装饰器
def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # OPTIONS请求直接返回200 OK和正确的CORS头
        if request.method == 'OPTIONS':
            response = make_response()
            response.status_code = 200
            response.headers['Access-Control-Allow-Origin'] = request.headers.get('Origin', 'http://localhost:5173')
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With, Accept, Origin'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            return response
        
        token = request.headers.get('Authorization')
        if token:
            # 移除Bearer前缀
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_info = verify_token(token)
            if not user_info:
                return jsonify({"msg": "无效的认证令牌"}), 401
            
            # 获取用户信息
            user = User.query.get(user_info.get('user_id'))
            if not user:
                return jsonify({"msg": "用户不存在"}), 401
            
            # 检查是否为管理员
            if user.role != 'admin':
                return jsonify({"msg": "需要管理员权限"}), 403
            
            g.user = user
        else:
            return jsonify({"msg": "未提供认证令牌"}), 401
        
        return f(*args, **kwargs)
    return wrapper

# ======================
# 上传接口
# ======================
@contract_bp.route("/upload", methods=["POST", "OPTIONS"])
@auth_required
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"msg": "未上传文件"}), 400

    upload_path = "uploads"
    os.makedirs(upload_path, exist_ok=True)
    
    # 保存为固定文件名，确保分析时使用的是刚上传的文件
    fixed_filename = "current_contract.pdf"
    filepath = os.path.join(upload_path, fixed_filename)
    file.save(filepath)

    return jsonify({"msg": "上传成功", "filename": fixed_filename})

# ======================
# AI 审查接口（上传文件分析）
# ======================
@contract_bp.route("/review", methods=["GET", "OPTIONS"])
@auth_required
def review():
    upload_path = "uploads"
    fixed_filename = "current_contract.pdf"
    filepath = os.path.join(upload_path, fixed_filename)
    
    if not os.path.exists(filepath):
        return jsonify({"msg": "没有文件"}), 400

    text = ""
    if filepath.endswith(".pdf"):
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        except Exception as e:
            # 尝试使用大模型来读取文件
            text = "正在使用大模型分析文件内容..."
            # 这里可以添加大模型调用逻辑
    elif filepath.endswith(".txt"):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        text = "暂不支持该文件格式"

    try:
        result = analyze_contract(text)  # AI分析
    except Exception as e:
        result = f"AI分析失败：{str(e)}"

    return jsonify({"text": text, "analysis": result})

# ======================
# AI 审查接口（根据合同ID分析）
# ======================
@contract_bp.route("/review/analyze", methods=["POST", "OPTIONS"])
def review_analyze():
    try:
        data = request.json
        contract_id = data.get('contract_id')
        
        if not contract_id:
            return jsonify({"msg": "请提供合同ID"}), 400

        # 从数据库获取合同信息
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"msg": "合同不存在"}), 404

        # 获取合同文本内容进行分析
        text = contract.content or contract.service_content or "暂无内容"
        
        try:
            result = analyze_contract(text)  # AI分析
        except Exception as e:
            result = {
                "contract_number": "",
                "party_a": "",
                "party_b": "",
                "service_content": "",
                "service_period": "",
                "service_fee": "",
                "payment_method": "",
                "party_a_rights": "",
                "party_b_rights": "",
                "acceptance_standard": "",
                "liability": "",
                "dispute_resolution": "",
                "signing_date": "",
                "expire_date": "",
                "result": "AI分析失败，使用数据库已有数据",
                "subject_ok": False,
                "object_clear": False,
                "price_clear": False,
                "performable": False
            }

        # 使用数据库中已有的值填充空字段
        if not result.get('contract_number'):
            result['contract_number'] = contract.contract_number or '未识别'
        if not result.get('party_a'):
            result['party_a'] = contract.party_a or '未识别'
        if not result.get('party_b'):
            result['party_b'] = contract.party_b or '未识别'
        if not result.get('service_content'):
            result['service_content'] = contract.service_content or '未识别'
        if not result.get('service_period'):
            result['service_period'] = contract.service_period or '未识别'
        if not result.get('service_fee'):
            result['service_fee'] = contract.service_fee or '未识别'
        if not result.get('payment_method'):
            result['payment_method'] = contract.payment_method or '未识别'
        if not result.get('party_a_rights'):
            result['party_a_rights'] = contract.party_a_rights or '未识别'
        if not result.get('party_b_rights'):
            result['party_b_rights'] = contract.party_b_rights or '未识别'
        if not result.get('acceptance_standard'):
            result['acceptance_standard'] = contract.acceptance_standard or '未识别'
        if not result.get('liability'):
            result['liability'] = contract.liability or '未识别'
        if not result.get('dispute_resolution'):
            result['dispute_resolution'] = contract.dispute_resolution or '未识别'
        if not result.get('signing_date'):
            result['signing_date'] = str(contract.signing_date) if contract.signing_date else '未识别'
        if not result.get('expire_date'):
            result['expire_date'] = str(contract.expire_date) if contract.expire_date else '未识别'
        if not result.get('result') or result['result'] == '解析失败':
            result['result'] = contract.result or '未识别'
        
        # 使用数据库中的合规检查结果
        if contract.subject_ok is not None:
            result['subject_ok'] = contract.subject_ok
        if contract.object_clear is not None:
            result['object_clear'] = contract.object_clear
        if contract.price_clear is not None:
            result['price_clear'] = contract.price_clear
        if contract.performable is not None:
            result['performable'] = contract.performable

        return jsonify({"text": text, "analysis": result})
    
    except Exception as e:
        return jsonify({"msg": "review/analyze接口错误", "error": str(e)}), 500

# ======================
# 保存合同到数据库
# ======================
@contract_bp.route("/save_contract", methods=["POST", "OPTIONS"])
@auth_required
def save_contract():
    try:
        data = request.json
        
        if not data:
            return jsonify({"msg": "请求数据为空"}), 400

        # 计算是否合规
        def to_bool(value):
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() == "true"
            return False
        
        is_compliant = (
            to_bool(data.get("subject_ok")) and 
            to_bool(data.get("object_clear")) and 
            to_bool(data.get("price_clear")) and 
            to_bool(data.get("performable"))
        )

        # 处理到期日期
        expire_date = data.get("expire_date")
        if expire_date:
            try:
                # 尝试多种日期格式解析
                expire_date = expire_date.replace('Z', '+00:00')
                expire_date = datetime.fromisoformat(expire_date)
            except Exception as e:
                expire_date = None
        
        # 处理签署日期
        signing_date = data.get("signing_date")
        if signing_date:
            try:
                # 尝试多种日期格式解析
                signing_date = signing_date.replace('Z', '+00:00')
                signing_date = datetime.fromisoformat(signing_date)
            except Exception as e:
                signing_date = None
        
        # 创建合同对象，只包含数据库中存在的字段
        contract = Contract(
            contract_number=_safe_text(data.get("contract_number"), ""),
            party_a=_safe_text(data.get("party_a"), ""),
            party_b=_safe_text(data.get("party_b"), ""),
            service_content=_safe_text(data.get("service_content"), ""),
            service_period=_safe_text(data.get("service_period"), ""),
            service_fee=_safe_text(data.get("service_fee"), ""),
            payment_method=_safe_text(data.get("payment_method"), ""),
            party_a_rights=_safe_text(data.get("party_a_rights"), ""),
            party_b_rights=_safe_text(data.get("party_b_rights"), ""),
            acceptance_standard=_safe_text(data.get("acceptance_standard"), ""),
            liability=_safe_text(data.get("liability"), ""),
            dispute_resolution=_safe_text(data.get("dispute_resolution"), ""),
            signing_date=signing_date,
            name=_safe_text(data.get("name"), "") or "合同_" + str(int(datetime.now().timestamp())),
            content=_safe_text(data.get("content"), ""),
            expire_date=expire_date,
            result=_safe_text(data.get("result"), ""),
            subject_ok=to_bool(data.get("subject_ok")),
            object_clear=to_bool(data.get("object_clear")),
            price_clear=to_bool(data.get("price_clear")),
            performable=to_bool(data.get("performable")),
            is_compliant=is_compliant
        )
        
        db.session.add(contract)
        db.session.commit()

        return jsonify({
            "msg": "保存成功",
            "is_compliant": is_compliant,
            "contract_id": contract.id
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "保存失败", "error": str(e)}), 500

# ======================
# 作废合同（软删除）- 仅管理员可用
# ======================
@contract_bp.route("/void_contract", methods=["POST", "OPTIONS"])
@admin_required
def void_contract():
    try:
        data = request.json
        if not data:
            return jsonify({"msg": "请求数据为空"}), 400

        contract_id = data.get("contract_id")
        if not contract_id:
            return jsonify({"msg": "缺少合同ID"}), 400

        # 查找合同
        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"msg": "合同不存在"}), 404

        # 软删除：设置is_void标记为True
        contract.is_void = True
        db.session.commit()

        return jsonify({"msg": "合同已作废"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "作废合同失败", "error": str(e)}), 500

# ======================
# 获取合同列表
# ======================
@contract_bp.route("/contracts", methods=["GET", "OPTIONS"])
def get_contracts():
    try:
        # 获取筛选参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # 构建查询，排除已作废的合同
        query = Contract.query.filter((Contract.is_void == False) | (Contract.is_void == None))
        
        # 应用日期筛选
        if start_date:
            from datetime import datetime
            try:
                start = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(Contract.expire_date >= start)
            except:
                pass
        
        if end_date:
            from datetime import datetime
            try:
                end = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(Contract.expire_date <= end)
            except:
                pass
        
        contracts = query.all()
        result = []

        for c in contracts:
            result.append({
                "id": c.id,
                "contract_number": c.contract_number,
                "party_a": c.party_a,
                "party_b": c.party_b,
                "service_content": c.service_content,
                "service_period": c.service_period,
                "service_fee": c.service_fee,
                "payment_method": c.payment_method,
                "party_a_rights": c.party_a_rights,
                "party_b_rights": c.party_b_rights,
                "acceptance_standard": c.acceptance_standard,
                "liability": c.liability,
                "dispute_resolution": c.dispute_resolution,
                "signing_date": str(c.signing_date) if c.signing_date else None,
                "name": c.name,
                "created_at": str(c.created_at),
                "expire_date": str(c.expire_date) if c.expire_date else None,
                "result": c.result,
                "subject_ok": c.subject_ok if c.subject_ok is not None else False,
                "object_clear": c.object_clear if c.object_clear is not None else False,
                "price_clear": c.price_clear if c.price_clear is not None else False,
                "performable": c.performable if c.performable is not None else False,
                "is_compliant": c.is_compliant if c.is_compliant is not None else False,
                "status": getattr(c, 'status', 'pending'),
                "reject_reason": getattr(c, 'reject_reason', None)
            })

        return jsonify(result)

    except Exception as e:
        import traceback
        error_info = traceback.format_exc()
        print("contracts接口错误:", str(e))
        print("错误详情:", error_info)
        return jsonify({"msg": "contracts接口错误", "error": str(e)}), 500

# ======================
# 查看合同内容
# ======================
@contract_bp.route("/contract/content", methods=["GET", "OPTIONS"])
@auth_required
def get_contract_content():
    try:
        upload_path = "uploads"
        fixed_filename = "current_contract.pdf"
        filepath = os.path.join(upload_path, fixed_filename)
        
        if not os.path.exists(filepath):
            return jsonify({"msg": "没有文件"}), 400

        content = ""
        if filepath.endswith(".txt"):
            # 文本文件
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        elif filepath.endswith(".pdf"):
            # PDF文件
            try:
                import pdfplumber
                with pdfplumber.open(filepath) as pdf:
                    for page in pdf.pages:
                        content += page.extract_text() or ""
            except Exception as e:
                # 尝试使用大模型来读取文件
                content = "正在使用大模型分析文件内容..."
                # 这里可以添加大模型调用逻辑
        else:
            content = "不支持的文件格式"

        return jsonify({"content": content, "filename": fixed_filename})

    except Exception as e:
        return jsonify({"msg": "contract/content接口错误", "error": str(e)}), 500

# ======================
# 审核合同
# ======================
@contract_bp.route("/contract/approve", methods=["POST", "OPTIONS"])
def approve_contract():
    try:
        data = request.json
        contract_id = data.get('contract_id')
        status = data.get('status')
        reason = data.get('reason', '')

        contract = Contract.query.get(contract_id)
        if not contract:
            return jsonify({"msg": "合同不存在"}), 400

        if status == 'approved':
            contract.status = 'approved'
            contract.reject_reason = None
        elif status == 'rejected':
            contract.status = 'rejected'
            contract.reject_reason = reason

        db.session.commit()
        return jsonify({"msg": "操作成功"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "审核接口错误", "error": str(e)}), 500

# ======================
# 获取合同统计数据
# ======================
@contract_bp.route("/stats", methods=["GET", "OPTIONS"])
@auth_required
def get_stats():
    try:
        # 获取所有未作废的合同
        contracts = Contract.query.filter((Contract.is_void == False) | (Contract.is_void == None)).all()
        
        # 当前合同数量
        current_count = len(contracts)
        
        # 进行中合同数量（假设expire_date大于当前日期的为进行中）
        today = datetime.now().date()
        in_progress_count = 0
        
        # 应收金额总和
        receivable_amount = 0
        
        # 应付金额总和（假设为应收的80%作为模拟）
        payable_amount = 0
        
        # 按月份统计应收金额
        monthly_receivable = [0] * 12
        # 按月份统计应付金额
        monthly_payable = [0] * 12
        
        for c in contracts:
            # 计算进行中合同
            if c.expire_date:
                expire_date = c.expire_date.date() if hasattr(c.expire_date, 'date') else c.expire_date
                if expire_date > today:
                    in_progress_count += 1
            
            # 计算金额
            if c.service_fee:
                try:
                    # 提取数字金额
                    fee_str = ''.join(filter(lambda x: x.isdigit() or x == '.', str(c.service_fee)))
                    if fee_str:
                        fee = float(fee_str)
                        receivable_amount += fee
                        payable_amount += fee * 0.8  # 假设应付为应收的80%
                        
                        # 按月份统计（根据签署日期）
                        if c.signing_date:
                            month = c.signing_date.month - 1  # 转换为0索引
                            if 0 <= month < 12:
                                monthly_receivable[month] += fee
                                monthly_payable[month] += fee * 0.8
                except:
                    pass
        
        # 计算应收账款统计（模拟数据）
        received_amount = receivable_amount * 0.2767  # 实收约27.67%
        unreceived_amount = receivable_amount - received_amount
        receivable_rate = round((received_amount / receivable_amount * 100) if receivable_amount > 0 else 0, 2)
        
        # 计算应付账款统计（模拟数据）
        paid_amount = payable_amount * 0.385  # 实付约38.5%
        unpaid_amount = payable_amount - paid_amount
        payable_rate = round((paid_amount / payable_amount * 100) if payable_amount > 0 else 0, 2)
        
        return jsonify({
            "current_contracts": current_count,
            "in_progress_contracts": in_progress_count,
            "receivable_amount": round(receivable_amount, 2),
            "payable_amount": round(payable_amount, 2),
            "monthly_receivable": [round(v, 2) for v in monthly_receivable],
            "monthly_payable": [round(v, 2) for v in monthly_payable],
            "received_amount": round(received_amount, 2),
            "unreceived_amount": round(unreceived_amount, 2),
            "receivable_rate": receivable_rate,
            "paid_amount": round(paid_amount, 2),
            "unpaid_amount": round(unpaid_amount, 2),
            "payable_rate": payable_rate
        })

    except Exception as e:
        return jsonify({"msg": "stats接口错误", "error": str(e)}), 500

# ======================
# 测试接口
# ======================
@contract_bp.route("/test", methods=["POST", "OPTIONS"])
def test():
    try:
        # 验证token
        # 开发环境跳过认证检查（临时解决方案）
        token = request.headers.get('Authorization')
        if token:
            # 移除Bearer前缀
            if token.startswith('Bearer '):
                token = token[7:]
            
            user_info = verify_token(token)
            if not user_info:
                return jsonify({"msg": "无效的认证令牌"}), 401
        # 如果没有token，在开发环境中允许访问

        return jsonify({"msg": "测试成功", "data": request.json})

    except Exception as e:
        return jsonify({"msg": "test接口错误", "error": str(e)}), 500