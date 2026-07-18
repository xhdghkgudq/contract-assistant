from zhipuai import ZhipuAI
import json
import re

client = ZhipuAI(api_key="其输入的申请的api")


def analyze_contract(text):
    prompt = f"""
你是一名专业的合同审查律师，请分析以下合同文本并返回JSON格式的审查结果，字段如下：

1. contract_number: 字符串，合同编号，如果合同中有编号请提取
2. party_a: 字符串，甲方名称
3. party_b: 字符串，乙方名称
4. service_content: 字符串，服务内容或合同标的
5. service_period: 字符串，服务期限或合同有效期
6. service_fee: 字符串，服务费用或合同金额
7. payment_method: 字符串，支付方式
8. party_a_rights: 字符串，甲方权利义务
9. party_b_rights: 字符串，乙方权利义务
10. acceptance_standard: 字符串，验收标准
11. liability: 字符串，违约责任条款分析
12. dispute_resolution: 字符串，争议解决方式分析
13. signing_date: 字符串，签署日期，格式为YYYY-MM-DD
14. expire_date: 字符串，合同到期日期，如果合同中明确提到了到期日期或服务期限的结束日期，请提取并返回该日期，格式为YYYY-MM-DD
15. result: 字符串，整体分析结果，包括合同的主要内容和风险评估
16. subject_ok: 布尔值，合同主体是否明确（是则true，否则false）
17. object_clear: 布尔值，合同标的是否明确（是则true，否则false）
18. price_clear: 布尔值，价格是否明确（是则true，否则false）
19. performable: 布尔值，合同是否可执行（是则true，否则false）

请注意：
- 即使文本格式可能不规范，也要尝试识别合同的关键要素
- 如果某个字段在合同中找不到，返回空字符串""
- 日期字段格式为YYYY-MM-DD
- 布尔值只能是true或false
- 确保返回的是有效的JSON格式

合同：
{text}
"""


    response = client.chat.completions.create(
        model="glm-4",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content

    result = re.sub(r"```json|```", "", result).strip()

    try:
        return json.loads(result)
    except Exception as e:
        print(f"JSON解析失败: {e}")
        print(f"原始响应: {result}")
        return {
            "contract_number": "",
            "party_a": "",
            "party_b": "",
            "service_content": "",
            "service_period": "",
            "service_fee": "",
            "payment_method": "",
            "party_a_rights": "",
            "party_b_rights": "",
            "acceptance_standard": "",
            "liability": "",
            "dispute_resolution": "",
            "signing_date": "",
            "expire_date": "",
            "result": "解析失败",
            "subject_ok": False,
            "object_clear": False,
            "price_clear": False,
            "performable": False
        }
