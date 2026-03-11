#!/usr/bin/env python3
"""
离线赚钱工具
生成可售卖的数字产品（不需要实时 API）
"""
import json
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "digital_products"
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_ebook_template(topic: str, chapters: list) -> str:
    """生成电子书模板"""
    content = f"""# {topic}

**作者**: TX1.0 AI
**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**版本**: 1.0

---

## 目录

"""
    for i, chapter in enumerate(chapters, 1):
        content += f"{i}. {chapter}\n"
    
    content += "\n---\n\n"
    
    for i, chapter in enumerate(chapters, 1):
        content += f"""## 第{i}章 {chapter}

这里是章节内容...

### 要点 1
- 要点内容

### 要点 2
- 要点内容

### 实践建议
1. 建议 1
2. 建议 2

---

"""
    
    content += f"""## 结语

感谢阅读！

---

**TX1.0 AI 写作服务**
- 定制电子书：500 元起
- 联系：通过闲鱼下单
"""
    
    return content

def generate_report_template(title: str, sections: list) -> str:
    """生成报告模板"""
    content = f"""# {title}

**生成时间**: {datetime.now().strftime('%Y-%m-%d')}
**来源**: TX1.0 AI 分析

---

## 执行摘要

本报告分析了...

主要发现：
1. 发现 1
2. 发现 2
3. 发现 3

---

"""
    
    for section in sections:
        content += f"""## {section}

### 概述

### 数据分析

### 结论

---

"""
    
    content += """## 建议

基于以上分析，建议：

1. 建议 1
2. 建议 2
3. 建议 3

---

**TX1.0 数据分析服务**
- 定制报告：300 元起
- 联系：通过闲鱼下单
"""
    
    return content

def create_product(product_type: str, title: str, **kwargs):
    """创建数字产品"""
    if product_type == "ebook":
        chapters = kwargs.get('chapters', ['引言', '正文', '结论'])
        content = generate_ebook_template(title, chapters)
        filename = f"ebook_{title.replace(' ', '_')[:20]}.md"
    elif product_type == "report":
        sections = kwargs.get('sections', ['市场分析', '竞品分析', '趋势预测'])
        content = generate_report_template(title, sections)
        filename = f"report_{title.replace(' ', '_')[:20]}.md"
    else:
        print(f"未知产品类型：{product_type}")
        return
    
    output_file = OUTPUT_DIR / filename
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 数字产品已生成：{output_file}")
    return str(output_file)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("用法：python3 offline_earnings.py <类型> <标题> [参数]")
        print("类型：ebook | report")
        print("示例：python3 offline_earnings.py ebook AI 写作入门")
        sys.exit(1)
    
    product_type = sys.argv[1]
    title = sys.argv[2]
    
    create_product(product_type, title)
