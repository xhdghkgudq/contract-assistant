import requests

# 测试作废合同接口
url = "http://localhost:5000/void_contract"

# 测试数据
void_data = {
    "contract_id": 4
}

# 测试请求，不使用token
print("=== 测试作废合同（不使用token）===")
try:
    response = requests.post(url, json=void_data, headers={
        "Content-Type": "application/json",
        "Origin": "http://localhost:5173"
    })
    print("响应状态码:", response.status_code)
    print("响应头:", dict(response.headers))
    print("响应内容:", response.text)
except Exception as e:
    print("请求失败:", e)

# 模拟登录获取token
login_url = "http://localhost:5000/login"
login_data = {
    "username": "admin",
    "password": "123456"
}

print("\n=== 测试登录 ===")
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
            print("\n=== 测试作废合同（使用token）===")
            try:
                response = requests.post(url, json=void_data, headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                    "Origin": "http://localhost:5173"
                })
                print("响应状态码:", response.status_code)
                print("响应头:", dict(response.headers))
                print("响应内容:", response.text)
            except Exception as e:
                print("请求失败:", e)
        else:
            print("登录响应中没有token")
    else:
        print("登录失败，状态码:", login_response.status_code)
except Exception as e:
    print("登录请求失败:", e)
