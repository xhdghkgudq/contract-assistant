import requests
import json

# 测试登录和保存合同
print("Test login and save contract")

# 1. Login
login_url = 'http://localhost:5000/login'
headers = {'Content-Type': 'application/json'}
login_data = json.dumps({'username': 'admin', 'password': 'admin123'})
login_response = requests.post(login_url, headers=headers, data=login_data)
print('Login status:', login_response.status_code)

if login_response.status_code == 200:
    token = login_response.json().get('token')
    print('Got token:', token[:20], '...')
    
    # 2. Test save contract
    save_url = 'http://localhost:5000/save_contract'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
    }
    
    contract_data = {
        'contract_number': 'TS-2026-TEST',
        'party_a': '北京科技有限公司',
        'party_b': '上海贸易有限公司',
        'service_content': '技术咨询服务',
        'service_period': '2026-01-01至2026-12-31',
        'service_fee': '1000000元',
        'payment_method': '转账',
        'name': '测试合同',
        'content': '合同内容',
        'result': '分析结果',
        'subject_ok': True,
        'object_clear': True,
        'price_clear': True,
        'performable': True
    }
    
    try:
        save_response = requests.post(save_url, headers=headers, data=json.dumps(contract_data))
        print('Save status:', save_response.status_code)
        print('Save response:', save_response.text)
    except Exception as e:
        print('Error:', str(e))
