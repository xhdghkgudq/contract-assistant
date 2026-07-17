from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime, timedelta

# 生成近期的到期日期（7天后）
expire_date = (datetime.now() + timedelta(days=7)).strftime('%Y年%m月%d日')

def generate_contract():
    # 创建PDF文档
    doc = SimpleDocTemplate('合规测试合同.pdf', pagesize=A4)
    
    # 获取样式表
    styles = getSampleStyleSheet()
    
    # 自定义标题样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=20
    )
    
    # 自定义正文样式
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        alignment=TA_LEFT,
        fontSize=12,
        leading=20
    )
    
    # 合同内容
    story = []
    
    # 添加标题
    story.append(Paragraph('技术服务合同', title_style))
    story.append(Spacer(1, 10))
    
    # 添加合同内容
    content = f"""
合同编号：TS-2026-0331

甲方：北京科技有限公司
乙方：上海网络科技有限公司

根据《中华人民共和国合同法》及相关法律法规的规定，甲乙双方在平等、自愿、公平、诚实信用的基础上，就甲方委托乙方提供技术服务事宜，经协商一致，订立本合同。

一、服务内容
1. 甲方委托乙方提供技术服务，包括系统架构设计、代码优化、性能测试等服务。
2. 乙方应按照甲方的要求，提供专业、高效的技术服务。

二、服务期限
服务期限为2026年4月1日至{expire_date}，共计7天。

三、服务费用
1. 服务费用总计为人民币壹万元整（¥10,000.00）。
2. 支付方式：甲方应在合同签订后3个工作日内支付全部服务费用。

四、双方权利义务
1. 甲方权利义务：
   - 向乙方提供必要的技术资料和工作条件；
   - 按照合同约定支付服务费用；
   - 对乙方的服务进行监督和验收。

2. 乙方权利义务：
   - 按照合同约定提供技术服务；
   - 保证服务质量和进度；
   - 保守甲方的商业秘密和技术秘密。

五、验收标准
1. 乙方完成服务后，应向甲方提交服务成果。
2. 甲方应在收到服务成果后3个工作日内进行验收。
3. 验收合格的，甲方应签署验收确认书；验收不合格的，乙方应在3个工作日内整改完毕。

六、违约责任
1. 甲方未按照合同约定支付服务费用的，每逾期一天，应按照未支付金额的0.1%向乙方支付违约金。
2. 乙方未按照合同约定提供技术服务的，每逾期一天，应按照服务费用的0.1%向甲方支付违约金。
3. 任何一方违反合同约定的，应承担因此给对方造成的损失。

七、争议解决
本合同履行过程中发生的争议，双方应协商解决；协商不成的，任何一方均有权向合同签订地有管辖权的人民法院提起诉讼。

八、其他条款
1. 本合同自双方签字盖章之日起生效。
2. 本合同一式两份，甲乙双方各执一份，具有同等法律效力。

甲方（盖章）：北京科技有限公司
法定代表人（签字）：张三
日期：2026年3月31日

乙方（盖章）：上海网络科技有限公司
法定代表人（签字）：李四
日期：2026年3月31日
"""
    
    # 添加内容到PDF
    for line in content.strip().split('\n'):
        if line.strip():
            story.append(Paragraph(line, body_style))
        else:
            story.append(Spacer(1, 10))
    
    # 生成PDF
    doc.build(story)
    print('合同生成成功！')

if __name__ == '__main__':
    generate_contract()
