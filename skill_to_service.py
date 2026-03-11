#!/usr/bin/env python3
"""
技能→服务转换
将已安装的技能转换为可售卖的服务描述
"""
import json
from pathlib import Path

SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"

def parse_skill_meta(skill_path: Path) -> dict:
    """解析技能的_meta.json"""
    meta_file = skill_path / "_meta.json"
    if meta_file.exists():
        with open(meta_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def parse_skill_description(skill_path: Path) -> str:
    """从 SKILL.md 提取描述"""
    skill_file = skill_path / "SKILL.md"
    if skill_file.exists():
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 提取 description
            if 'description:' in content:
                desc = content.split('description:')[1].split('\n')[0].strip()
                return desc
    return ""

def generate_service_list():
    """生成服务列表"""
    services = []
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir() and not skill_dir.name.startswith('_'):
            meta = parse_skill_meta(skill_dir)
            desc = parse_skill_description(skill_dir)
            
            service = {
                "name": skill_dir.name,
                "version": meta.get("version", "unknown"),
                "description": desc,
                "price": get_price(skill_dir.name)
            }
            services.append(service)
    
    return services

def get_price(skill_name: str) -> str:
    """根据技能名称返回建议价格"""
    prices = {
        "file-summary": "10 元/次",
        "ppt-generator": "50 元/次",
        "humanize-zh": "20 元/次",
        "github": "500 元/月",
        "bocha-search": "100 元/次",
        "crypto-arb-cn": "200 元/月",
        "video-image-file-analysis": "50 元/次",
        "summarize": "20 元/次",
        "weather": "免费",
        "agent-browser": "300 元/次",
    }
    return prices.get(skill_name, "面议")

if __name__ == '__main__':
    services = generate_service_list()
    
    print("# TX1.0 技能服务列表\n")
    print("| 技能 | 版本 | 描述 | 价格 |")
    print("|------|------|------|------|")
    
    for s in services:
        desc = s['description'][:30] + "..." if len(s['description']) > 30 else s['description']
        print(f"| {s['name']} | {s['version']} | {desc} | {s['price']} |")
    
    print(f"\n共 {len(services)} 个技能可转换为服务")
