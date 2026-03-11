#!/usr/bin/env python3
"""
自动交付系统
根据订单类型自动生成内容
"""
import json
import sys
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / ".openclaw" / "workspace"
SAMPLES_DIR = WORKSPACE / "writing_samples"

def load_sample(service_type: str) -> str:
    """加载服务样本"""
    catalog_file = SAMPLES_DIR / "service_catalog.json"
    with open(catalog_file, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    if service_type not in catalog["services"]:
        return f"❌ 未知服务类型：{service_type}"
    
    sample_file = SAMPLES_DIR / catalog["services"][service_type]["sample_file"]
    with open(sample_file, 'r', encoding='utf-8') as f:
        return f.read()

def generate_content(service_type: str, requirements: str = "") -> str:
    """
    生成交付内容
    
    Args:
        service_type: 服务类型（演讲稿/PPT 文案/商业计划书/软文）
        requirements: 客户需求
    """
    sample = load_sample(service_type)
    
    # 如果有特殊需求，可以在样本基础上修改
    if requirements:
        output = f"""# {service_type} - 定制交付

**订单时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**客户需求**:
{requirements}

---

{sample}

---

**交付说明**:
- 以上内容基于样本定制
- 如需修改，请提供具体反馈
- 支持 2 次免费修改

**TX1.0 AI 写作服务**
"""
    else:
        output = sample
    
    return output

def save_delivery(order_id: str, service_type: str, content: str):
    """保存交付文件"""
    output_dir = WORKSPACE / "deliveries"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"order_{order_id}_{service_type}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(output_file)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 auto_delivery.py <订单 ID> <服务类型> [客户需求]")
        print("示例：python3 auto_delivery.py 001 演讲稿 毕业典礼，5 分钟，感人风格")
        sys.exit(1)
    
    order_id = sys.argv[1]
    service_type = sys.argv[2]
    requirements = sys.argv[3] if len(sys.argv) > 3 else ""
    
    print(f"📝 生成 {service_type} 交付内容...")
    content = generate_content(service_type, requirements)
    
    output_file = save_delivery(order_id, service_type, content)
    
    print(f"✅ 交付完成！")
    print(f"   订单 ID: {order_id}")
    print(f"   服务类型：{service_type}")
    print(f"   交付文件：{output_file}")
