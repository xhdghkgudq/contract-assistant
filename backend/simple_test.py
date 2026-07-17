# -*- coding: utf-8 -*-
import requests
import json

def main():
    print("Testing backend API...")
    
    # 1. Login
    print("\n1. Testing login...")
    login_url = "http://localhost:5000/login"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps({'username': 'admin', 'password': 'admin123'})
    
    response = requests.post(login_url, headers=headers, data=data)
    print("   Status:", response.status_code)
    
    if response.status_code == 200:
        token = response.json().get('token')
        print("   Token received:", token[:20], "...")
    else:
        print("   Login failed:", response.text)
        return
    
    # 2. Test OPTIONS
    print("\n2. Testing OPTIONS request...")
    save_url = "http://localhost:5000/save_contract"
    headers = {'Origin': 'http://localhost:5173'}
    
    response = requests.options(save_url, headers=headers)
    print("   Status:", response.status_code)
    print("   CORS headers:")
    for key, value in response.headers.items():
        if 'Access-Control' in key:
            print("     ", key, ":", value)
    
    # 3. Test save contract
    print("\n3. Testing save_contract...")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Origin': 'http://localhost:5173'
    }
    
    contract_data = {
        'contract_number': 'TEST-SIMPLE-001',
        'party_a': 'Jia Fang',
        'party_b': 'Yi Fang',
        'service_content': 'Service content',
        'service_period': '2024-01-01 to 2024-12-31',
        'service_fee': '100000',
        'payment_method': 'Transfer',
        'name': 'Test Contract',
        'content': 'Contract content',
        'result': 'Analysis result',
        'subject_ok': True,
        'object_clear': True,
        'price_clear': True,
        'performable': True
    }
    
    response = requests.post(save_url, headers=headers, data=json.dumps(contract_data))
    print("   Status:", response.status_code)
    print("   Response:", response.text)

if __name__ == '__main__':
    main()
