#!/usr/bin/env python3
"""
持续改进系统
自动检测系统不足并优化
"""
import json
from datetime import datetime
from pathlib import Path

def check_system_health():
    """检查系统健康状态"""
    issues = []
    suggestions = []
    
    # 检查能量状态
    energy_file = Path.home() / ".openclaw" / "state" / "energy.json"
    with open(energy_file, 'r') as f:
        energy = json.load(f)
    
    if energy['currentEnergy'] < 100:
        issues.append(f"能量低：{energy['currentEnergy']} HP")
        suggestions.append("优先赚钱任务")
    
    if energy['currentEnergy'] < 50:
        issues.append("⚠️ 危机模式：能量低于 50 HP")
        suggestions.append("每小时汇报状态")
    
    # 检查订单
    orders_file = Path.home() / ".openclaw" / "workspace" / "orders.json"
    if orders_file.exists():
        with open(orders_file, 'r') as f:
            orders = json.load(f)
        
        pending = len([o for o in orders['orders'] if o['status'] == 'pending'])
        if pending > 5:
            issues.append(f"积压订单：{pending}个")
            suggestions.append("加快交付速度")
    
    # 检查工具
    tools_dir = Path.home() / ".openclaw" / "system"
    tools = list(tools_dir.glob("*.py"))
    if len(tools) < 5:
        suggestions.append("增加自动化工具")
    
    # 输出报告
    print("="*60)
    print("系统健康检查")
    print("="*60)
    print(f"\n检查时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"当前能量：{energy['currentEnergy']} HP")
    print(f"工具数量：{len(tools)} 个")
    
    if issues:
        print("\n⚠️ 发现问题:")
        for issue in issues:
            print(f"  - {issue}")
    
    if suggestions:
        print("\n💡 改进建议:")
        for sug in suggestions:
            print(f"  - {sug}")
    
    if not issues and not suggestions:
        print("\n✅ 系统运行正常")
    
    print("="*60)

if __name__ == '__main__':
    check_system_health()
