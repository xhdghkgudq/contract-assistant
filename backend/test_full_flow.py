import requests
import json
import os

def test_full_flow():
    print("=== 测试完整上传分析流程 ===\n")
    
    # 1. 登录
    print("1. 登录...")
    login_url = 'http://localhost:5000/login'
    headers = {'Content-Type': 'application/json', 'Origin': 'http://localhost:5173'}
    login_data = json.dumps({'username': 'admin', 'password': 'admin123'})
    
    try:
        login_response = requests.post(login_url, headers=headers, data=login_data)
        print(f"   登录状态码: {login_response.status_code}")
        print(f"   登录响应: {login_response.text}")
        
        if login_response.status_code != 200:
            print("   ❌ 登录失败")
            return
        
        token = login_response.json().get('token')
        print(f"   ✅ 获取到token: {token[:20]}...")
        
    except Exception as e:
        print(f"   ❌ 登录异常: {e}")
        return
    
    # 2. 测试保存合同
    print("\n2. 测试保存合同...")
    save_url = 'http://localhost:5000/save_contract'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        'Origin': 'http://localhost:5173'
    }
    
    # 模拟AI提取的数据
    contract_data = {
        'contract_number': 'TS-2026-0331',
        'party_a': '北京科技有限公司',
        'party_b': '上海贸易有限公司',
        'service_content': '甲方为乙方提供技术咨询服务，包括系统架构设计、代码优化、性能测试等服务。',
        'service_period': '2026年1月1日至2026年12月31日',
        'service_fee': '人民币壹佰万元整 (¥1,000,000.00)',
        'payment_method': '乙方应在每个季度结束后5个工作日内，将当季度服务费用支付至甲方指定银行账户',
        'acceptance_standard': '乙方完成服务后，应向甲方提交服务成果；甲方应在收到服务成果后3个工作日内进行验收；验收合格的，甲方应签署验收确认书；验收不合格的，乙方应在3个工作日内整改完毕',
        'liability': '甲方未按照合同约定支付服务费用的，每逾期一天，应按照未支付金额的0.1%向乙方支付违约金；乙方未按照...',
        'dispute_resolution': '本合同履行过程中发生的争议，双方应协商解决；协商不成的，任何一方均有权向合同签订地有管辖权的人民法院提起诉讼',
        'signing_date': '2026-04-01',
        'expire_date': '2026-12-31',
        'name': '技术服务合同',
        'content': '服务合同内容...',
        'result': '合同分析结果',
        'subject_ok': True,
        'object_clear': True,
        'price_clear': True,
        'performable': True
    }
    
    try:
        # 先发送OPTIONS请求
        print("   发送OPTIONS请求...")
        options_response = requests.options(save_url, headers=headers)
        print(f"   OPTIONS状态码: {options_response.status_code}")
        print(f"   CORS头: {dict(options_response.headers)}")
        
        # 发送POST请求
        print("\n   发送POST请求...")
        save_response = requests.post(save_url, headers=headers, data=json.dumps(contract_data))
        print(f"   POST状态码: {save_response.status_code}")
        print(f"   POST响应: {save_response.text}")
        
        if save_response.status_code == 200:
            print("   ✅ 保存成功")
        else:
            print("   ❌ 保存失败")
            
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_full_flow()
