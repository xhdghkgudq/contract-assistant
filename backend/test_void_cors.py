import requests

# 测试作废合同接口
url = "http://localhost:5000/void_contract"

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
    print("登录响应内容:", login_response.text)
    
    if login_response.status_code == 200:
        import json
        login_json = login_response.json()
        if "token" in login_json:
            token = login_json["token"]
            print(f"获取到token: {token}")
            
            # 测试作废合同，使用token
            print("\n=== 测试作废合同 ===")
            try:
                # 先获取合同列表，确保有合同可以作废
                contracts_url = "http://localhost:5000/contracts"
                contracts_response = requests.get(contracts_url, headers={
                    "Authorization": f"Bearer {token}",
                    "Origin": "http://localhost:5173"
                })
                print("获取合同列表响应状态码:", contracts_response.status_code)
                print("获取合同列表响应内容:", contracts_response.text)
                
                # 提取第一个合同的ID
                contracts = contracts_response.json()
                if contracts:
                    contract_id = contracts[0]["id"]
                    print(f"要作废的合同ID: {contract_id}")
                    
                    # 测试作废合同
                    void_data = {
                        "contract_id": contract_id
                    }
                    
                    response = requests.post(url, json=void_data, headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                        "Origin": "http://localhost:5173"
                    })
                    print("作废合同响应状态码:", response.status_code)
                    print("作废合同响应头:", dict(response.headers))
                    print("作废合同响应内容:", response.text)
                else:
                    print("没有合同可以作废")
            except Exception as e:
                print("请求失败:", e)
        else:
            print("登录响应中没有token")
    else:
        print("登录失败，状态码:", login_response.status_code)
except Exception as e:
    print("登录请求失败:", e)
