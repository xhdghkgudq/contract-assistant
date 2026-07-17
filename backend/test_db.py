from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/contract_ai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 测试连接和表结构
with app.app_context():
    try:
        # 测试连接
        db.engine.connect()
        print("✅ 数据库连接成功")
        
        # 检查表是否存在
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        if 'contracts' in inspector.get_table_names():
            print("✅ contracts表存在")
            
            # 获取表结构
            columns = inspector.get_columns('contracts')
            print("\n=== contracts表字段 ===")
            for col in columns:
                print(f"  {col['name']}: {col['type']}")
                
            # 检查是否有缺失的字段
            required_fields = [
                'contract_number', 'party_a', 'party_b', 'service_content',
                'service_period', 'service_fee', 'payment_method',
                'party_a_rights', 'party_b_rights', 'acceptance_standard',
                'liability', 'dispute_resolution', 'signing_date',
                'result', 'subject_ok', 'object_clear', 'price_clear',
                'performable', 'is_compliant', 'is_void'
            ]
            
            existing_fields = [col['name'] for col in columns]
            missing_fields = [f for f in required_fields if f not in existing_fields]
            
            if missing_fields:
                print(f"\n❌ 缺失字段: {missing_fields}")
                print("\n请运行以下SQL添加缺失字段:")
                for field in missing_fields:
                    sql_type = "VARCHAR(255)" if field not in ['service_content', 'party_a_rights', 'party_b_rights', 'acceptance_standard', 'liability', 'dispute_resolution', 'result'] else "TEXT"
                    if field in ['signing_date', 'expire_date']:
                        sql_type = "DATETIME"
                    if field in ['subject_ok', 'object_clear', 'price_clear', 'performable', 'is_compliant', 'is_void']:
                        sql_type = "TINYINT(1) DEFAULT 0"
                    print(f"ALTER TABLE contracts ADD COLUMN {field} {sql_type};")
            else:
                print("\n✅ 所有字段都存在")
                
        else:
            print("❌ contracts表不存在")
            
    except Exception as e:
        print(f"❌ 数据库错误: {e}")
        import traceback
        traceback.print_exc()
