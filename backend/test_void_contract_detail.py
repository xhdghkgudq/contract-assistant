import requests
import json

# 测试作废合同接口
url = "http://localhost:5000/void_contract"

# 模拟登录获取token
login_url = "http://localhost:5000/login"
login_data = {
    "username": "admin",
    "password": "123456"
}

print("=== 测试登录 ===")
login_response = requests.post(login_url, json=login_data)
print("登录响应状态码:", login_response.status_code)
print("登录响应内容:", login_response.json())

if "token" in login_response.json():
    token = login_response.json()["token"]
    print(f"获取到token: {token}")
    
    # 先获取合同列表，找到一个有效的合同ID
    contracts_url = "http://localhost:5000/contracts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:5173"
    }
    
    print("\n=== 测试获取合同列表 ===")
    contracts_response = requests.get(contracts_url, headers=headers)
    print("获取合同列表响应状态码:", contracts_response.status_code)
    print("获取合同列表响应内容:", contracts_response.json())
    
    if contracts_response.status_code == 200 and len(contracts_response.json()) > 0:
        # 获取第一个合同的ID
        contract_id = contracts_response.json()[0]["id"]
        print(f"\n找到合同ID: {contract_id}")
        
        # 测试作废合同
        void_data = {
            "contract_id": contract_id
        }
        
        print("\n=== 测试作废合同 ===")
        response = requests.post(url, json=void_data, headers=headers)
        print("作废合同响应状态码:", response.status_code)
        print("作废合同响应内容:", response.json())
        print("作废合同响应头:", dict(response.headers))
    else:
        print("\n没有找到合同，无法测试作废功能")
else:
    print("\n登录失败，无法测试作废功能")
