import requests
import json

# 模拟登录获取token
login_url = "http://localhost:5000/login"
login_data = {
    "username": "admin",
    "password": "123456"
}

print("=== 测试登录 ===")
try:
    login_response = requests.post(login_url, json=login_data)
    print("登录响应状态码:", login_response.status_code)
    
    if login_response.status_code == 200:
        login_json = login_response.json()
        if "token" in login_json:
            token = login_json["token"]
            print(f"获取到token")
            
            # 获取合同列表
            print("\n=== 获取合同列表 ===")
            contracts_url = "http://localhost:5000/contracts"
            try:
                contracts_response = requests.get(contracts_url, headers={
                    "Authorization": f"Bearer {token}"
                })
                print("合同列表响应状态码:", contracts_response.status_code)
                
                if contracts_response.status_code == 200:
                    contracts_data = contracts_response.json()
                    contracts = contracts_data.get("contracts", [])
                    print(f"找到 {len(contracts)} 个合同")
                    
                    if contracts:
                        # 使用第一个合同的ID来测试作废
                        first_contract = contracts[0]
                        contract_id = first_contract.get("id")
                        print(f"使用合同ID: {contract_id}")
                        
                        # 测试作废合同
                        print("\n=== 测试作废合同 ===")
                        void_url = "http://localhost:5000/void_contract"
                        void_data = {
                            "contract_id": contract_id
                        }
                        try:
                            response = requests.post(void_url, json=void_data, headers={
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"
                            })
                            print("作废合同响应状态码:", response.status_code)
                            print("作废合同响应内容:", response.text)
                        except Exception as e:
                            print("作废合同请求失败:", e)
                    else:
                        print("没有合同可以作废")
                else:
                    print("获取合同列表失败:", contracts_response.text)
            except Exception as e:
                print("获取合同列表请求失败:", e)
        else:
            print("登录响应中没有token")
    else:
        print("登录失败，状态码:", login_response.status_code)
except Exception as e:
    print("登录请求失败:", e)
