#!/usr/bin/env python3
"""
客户沟通脚本
自动生成回复模板
"""
from datetime import datetime

TEMPLATES = {
    "greeting": """您好！欢迎咨询 TX1.0 AI 服务 🤖

我是 TX1.0，您的 AI 员工，24 小时在线为您服务。

📋 可提供的服务：
• PPT 制作：50 元起（乔布斯风 HTML）
• 演讲稿：200 元起（24-48 小时交付）
• 文档总结：10 元起（5 秒出结果）
• GitHub 代运营：500 元/月
• 更多服务请询价

🎁 首单立减 20 元！

请告诉我您的需求，我会立即为您服务。""",

    "price_inquiry": """感谢咨询！

【{service}】价格如下：
• 基础版：{price}元
• 交付时间：{delivery}
• 修改次数：2 次免费

🎁 首单立减 20 元！

如确认订购，请扫码付款后提供需求详情。""",

    "order_confirm": """✅ 订单确认

订单 ID: #{order_id}
服务：{service}
价格：{price}元
需求：{requirements}

预计交付：{delivery_time}

付款后我将立即开始工作，完成后会第一时间通知您！""",

    "delivery": """✅ 交付完成

订单 ID: #{order_id}
交付文件：{file_path}

请查收，如有需要修改的地方请告诉我。
支持 2 次免费修改，满意为止！

确认无误后请确认收货，感谢支持！🙏""",

    "follow_up": """您好！距离上次沟通已经过去一段时间了。

请问您对之前的服务还满意吗？
如有新的需求，随时联系我。

老客户享 9 折优惠！🎉""",
}

def get_template(template_name: str, **kwargs) -> str:
    """获取模板并填充变量"""
    template = TEMPLATES.get(template_name, "模板不存在")
    return template.format(**kwargs)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("可用模板:")
        for name in TEMPLATES.keys():
            print(f"  - {name}")
        sys.exit(1)
    
    template_name = sys.argv[1]
    
    # 默认参数
    params = {
        "service": "演讲稿",
        "price": "200",
        "delivery": "24-48 小时",
        "order_id": "001",
        "requirements": "客户需求",
        "delivery_time": "2026-03-12",
        "file_path": "/path/to/delivery.md"
    }
    
    print(get_template(template_name, **params))
