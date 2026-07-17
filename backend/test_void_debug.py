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
try:
    login_response = requests.post(login_url, json=login_data)
    print("登录响应状态码:", login_response.status_code)
    print("登录响应内容:", login_response.text)
    
    if login_response.status_code == 200:
        # 提取token
        login_json = login_response.json()
        if "token" in login_json:
            token = login_json["token"]
            print(f"获取到token: {token}")
            
            # 测试作废合同
            void_data = {
                "contract_id": 3
            }
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Origin": "http://localhost:5173"
            }
            
            print("\n=== 测试作废合同 ===")
            try:
                response = requests.post(url, json=void_data, headers=headers, timeout=10)
                print("作废合同响应状态码:", response.status_code)
                print("作废合同响应头:", dict(response.headers))
                try:
                    print("作废合同响应内容:", response.json())
                except Exception as e:
                    print("解析JSON失败:", e)
                    print("原始响应内容:", response.text)
            except Exception as e:
                print("发送请求失败:", e)
        else:
            print("登录响应中没有token")
    else:
        print("登录失败，状态码:", login_response.status_code)
except Exception as e:
    print("登录请求失败:", e)
