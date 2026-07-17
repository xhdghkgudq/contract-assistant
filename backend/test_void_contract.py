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

login_response = requests.post(login_url, json=login_data)
print("登录响应:", login_response.json())

if "token" in login_response.json():
    token = login_response.json()["token"]
    
    # 测试作废合同
    void_data = {
        "contract_id": 1  # 替换为实际的合同ID
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "http://localhost:5173"
    }
    
    response = requests.post(url, json=void_data, headers=headers)
    print("作废合同响应:", response.status_code)
    print("响应内容:", response.json())
    print("响应头:", dict(response.headers))
else:
    print("登录失败")
