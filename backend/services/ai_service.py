import requests

def analyze_contract(text):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "Bearer YOUR_API_KEY"
    }

    data = {
        "model": "glm-4",
        "messages": [
            {"role": "user", "content": f"请分析合同风险：{text[:1500]}"}
        ]
    }

    res = requests.post(url, json=data, headers=headers)
    return res.json()