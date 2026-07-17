import requests
import json
import traceback

def test_all_endpoints():
    print("="*60)
    print("          完整测试脚本 - 诊断问题")
    print("="*60)
    
    base_url = "http://localhost:5000"
    token = None
    
    # 1. 测试登录
    print("\n[1/5] 测试登录接口...")
    try:
        login_url = f"{base_url}/login"
        headers = {'Content-Type': 'application/json', 'Origin': 'http://localhost:5173'}
        data = json.dumps({'username': 'admin', 'password': 'admin123'})
        
        print(f"   请求URL: {login_url}")
        print(f"   请求数据: {data}")
        
        response = requests.post(login_url, headers=headers, data=data)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        
        if response.status_code == 200:
            token = response.json().get('token')
            print(f"   ✅ 登录成功，获取到token: {token[:20]}...")
        else:
            print(f"   ❌ 登录失败")
            return False
            
    except Exception as e:
        print(f"   ❌ 登录异常: {e}")
        traceback.print_exc()
        return False
    
    # 2. 测试OPTIONS请求（CORS）
    print("\n[2/5] 测试OPTIONS请求（CORS）...")
    try:
        save_url = f"{base_url}/save_contract"
        headers = {
            'Origin': 'http://localhost:5173',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type, Authorization'
        }
        
        print(f"   请求URL: {save_url}")
        response = requests.options(save_url, headers=headers)
        print(f"   状态码: {response.status_code}")
        print(f"   CORS头:")
        for key, value in response.headers.items():
            if 'Access-Control' in key:
                print(f"     {key}: {value}")
        
        if response.status_code == 200:
            print("   ✅ OPTIONS请求成功")
        else:
            print(f"   ❌ OPTIONS请求失败")
            
    except Exception as e:
        print(f"   ❌ OPTIONS请求异常: {e}")
        traceback.print_exc()
    
    # 3. 测试保存合同接口
    print("\n[3/5] 测试保存合同接口...")
    try:
        save_url = f"{base_url}/save_contract"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
            'Origin': 'http://localhost:5173'
        }
        
        contract_data = {
            'contract_number': 'TEST-DEBUG-001',
            'party_a': '测试甲方公司',
            'party_b': '测试乙方公司',
            'service_content': '技术咨询服务',
            'service_period': '2024-01-01至2024-12-31',
            'service_fee': '100000元',
            'payment_method': '银行转账',
            'name': '测试合同',
            'content': '这是合同内容',
            'result': 'AI分析结果',
            'subject_ok': True,
            'object_clear': True,
            'price_clear': True,
            'performable': True
        }
        
        print(f"   请求URL: {save_url}")
        print(f"   请求数据长度: {len(json.dumps(contract_data))} 字符")
        
        response = requests.post(save_url, headers=headers, data=json.dumps(contract_data))
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ 保存合同成功")
        else:
            print(f"   ❌ 保存合同失败")
            
    except Exception as e:
        print(f"   ❌ 保存合同异常: {e}")
        traceback.print_exc()
    
    # 4. 测试上传接口
    print("\n[4/5] 测试上传接口...")
    try:
        upload_url = f"{base_url}/upload"
        headers = {
            'Authorization': f'Bearer {token}',
            'Origin': 'http://localhost:5173'
        }
        
        # 创建一个简单的测试文件
        test_content = "这是一个测试合同内容"
        
        print(f"   请求URL: {upload_url}")
        
        response = requests.post(upload_url, headers=headers, files={'file': ('test.txt', test_content)})
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ 上传成功")
        else:
            print(f"   ❌ 上传失败")
            
    except Exception as e:
        print(f"   ❌ 上传异常: {e}")
        traceback.print_exc()
    
    # 5. 测试AI分析接口
    print("\n[5/5] 测试AI分析接口...")
    try:
        review_url = f"{base_url}/review"
        headers = {
            'Authorization': f'Bearer {token}',
            'Origin': 'http://localhost:5173'
        }
        
        print(f"   请求URL: {review_url}")
        
        response = requests.get(review_url, headers=headers)
        print(f"   状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   响应数据: {json.dumps(data, ensure_ascii=False)[:200]}...")
            print("   ✅ AI分析成功")
        else:
            print(f"   ❌ AI分析失败: {response.text}")
            
    except Exception as e:
        print(f"   ❌ AI分析异常: {e}")
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("              测试完成")
    print("="*60)

if __name__ == '__main__':
    test_all_endpoints()
