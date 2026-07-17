import requests
import json

# 模拟登录获取token
login_url = "http://localhost:5000/login"
login_data = {
    "username": "admin",
    "password": "123456"
}

print("=== 测试登录 ===")
login_response = requests.post(login_url, json=login_data)
print("登录响应状态码:", login_response.status_code)
login_json = login_response.json()
token = login_json["token"]
print(f"获取到token")

# 获取合同列表
print("\n=== 获取合同列表 ===")
contracts_url = "http://localhost:5000/contracts"
contracts_response = requests.get(contracts_url, headers={
    "Authorization": f"Bearer {token}"
})
print("合同列表响应状态码:", contracts_response.status_code)
print("合同列表响应内容:", contracts_response.text)

# 解析合同列表
try:
    contracts_data = contracts_response.json()
    print("合同列表数据类型:", type(contracts_data))
    
    if isinstance(contracts_data, list):
        contracts = contracts_data
    elif isinstance(contracts_data, dict):
        contracts = contracts_data.get("contracts", [])
    else:
        contracts = []
    
    print(f"找到 {len(contracts)} 个合同")
    
    if contracts:
        # 使用第一个合同的ID来测试作废
        first_contract = contracts[0]
        print("第一个合同:", first_contract)
        contract_id = first_contract.get("id") if isinstance(first_contract, dict) else first_contract[0] if isinstance(first_contract, (list, tuple)) else None
        print(f"使用合同ID: {contract_id}")
        
        # 测试作废合同
        print("\n=== 测试作废合同 ===")
        void_url = "http://localhost:5000/void_contract"
        void_data = {
            "contract_id": contract_id
        }
        response = requests.post(void_url, json=void_data, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        print("作废合同响应状态码:", response.status_code)
        print("作废合同响应内容:", response.text)
    else:
        print("没有合同可以作废")
except Exception as e:
    print("解析合同列表失败:", e)
    import traceback
    traceback.print_exc()
