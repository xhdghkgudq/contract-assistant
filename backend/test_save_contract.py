import requests
import json

# 测试保存合同接口
def test_save_contract():
    url = "http://localhost:5000/save_contract"
    
    # 测试数据
    test_data = {
        "contract_number": "TEST-2026-001",
        "party_a": "测试甲方",
        "party_b": "测试乙方",
        "service_content": "测试服务内容",
        "service_period": "2026-01-01 至 2026-12-31",
        "service_fee": "10000元",
        "payment_method": "银行转账",
        "party_a_rights": "甲方权利义务",
        "party_b_rights": "乙方权利义务",
        "acceptance_standard": "验收标准",
        "liability": "违约责任",
        "dispute_resolution": "协商解决",
        "signing_date": None,
        "name": "测试合同",
        "content": "合同内容",
        "expire_date": "2026-12-31T00:00:00.000Z",
        "result": "测试分析结果",
        "subject_ok": True,
        "object_clear": True,
        "price_clear": True,
        "performable": True
    }
    
    try:
        response = requests.post(url, json=test_data, headers={"Content-Type": "application/json"})
        print(f"状态码: {response.status_code}")
        print(f"响应: {response.text}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    test_save_contract()
