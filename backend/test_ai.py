from services.ai import analyze_contract

# 测试合同文本
contract_text = """技术服务合同

甲方：北京科技有限公司
乙方：上海软件技术有限公司

一、服务内容
甲方委托乙方提供系统架构设计、代码优化、性能测试等技术服务。

二、服务期限
服务期限为2026年4月1日至2026年4月7日。

三、服务费用
服务费用为人民币壹万元整。

四、付款方式
甲方应在服务完成后7个工作日内支付全部服务费用。

五、违约责任
任何一方违反本合同约定，应向对方支付违约金。

六、争议解决
本合同履行过程中发生的争议，双方应协商解决；协商不成的，任何一方均有权向合同签订地有管辖权的人民法院提起诉讼。

甲方（盖章）：北京科技有限公司
乙方（盖章）：上海软件技术有限公司
签订日期：2026年3月31日
"""

# 测试AI分析
result = analyze_contract(contract_text)
print("AI分析结果：")
print(result)
print("\n类型：")
print(type(result))
print("\n字段类型：")
if isinstance(result, dict):
    for key, value in result.items():
        print(f"{key}: {type(value)}")
