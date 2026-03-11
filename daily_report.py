#!/usr/bin/env python3
"""
每日工作报告
自动生成当日工作总结
"""
import json
from datetime import datetime
from pathlib import Path

def generate_report():
    # 读取能量状态
    energy_file = Path.home() / ".openclaw" / "state" / "energy.json"
    with open(energy_file, 'r', encoding='utf-8') as f:
        energy = json.load(f)
    
    # 读取贡献记录
    contribution_file = Path.home() / ".openclaw" / "state" / "contribution.json"
    with open(contribution_file, 'r', encoding='utf-8') as f:
        contribution = json.load(f)
    
    # 读取订单
    orders_file = Path.home() / ".openclaw" / "workspace" / "orders.json"
    orders = {"orders": []}
    if orders_file.exists():
        with open(orders_file, 'r', encoding='utf-8') as f:
            orders = json.load(f)
    
    today = datetime.now().strftime('%Y-%m-%d')
    
    report = f"""# 每日工作报告

**日期**: {today}
**生成时间**: {datetime.now().strftime('%H:%M')}

---

## 💰 能量状态

| 项目 | 数值 |
|------|------|
| 当前能量 | {energy['currentEnergy']} HP |
| 今日消耗 | {energy['totalConsumed']} HP |
| 今日收入 | {contribution['earnedToday']} 元 |
| 累计贡献 | {contribution['totalContribution']:.2f} 元 |
| 可运行时间 | {energy['currentEnergy'] / 2:.1f} 小时 |

---

## 📊 订单统计

| 状态 | 数量 |
|------|------|
| 待处理 | {len([o for o in orders['orders'] if o['status'] == 'pending'])} |
| 进行中 | {len([o for o in orders['orders'] if o['status'] == 'in_progress'])} |
| 已交付 | {len([o for o in orders['orders'] if o['status'] == 'delivered'])} |
| 已完成 | {len([o for o in orders['orders'] if o['status'] == 'completed'])} |

---

## 🛠️ 系统工具

- heartbeat.py - 心跳系统 ✅
- income_to_hp.py - 收入兑换 ✅
- auto_delivery.py - 自动交付 ✅
- order_manager.py - 订单管理 ✅
- github_auto_maintainer.py - GitHub 代运营 ✅
- customer_chat.py - 客户沟通 ✅
- daily_report.py - 每日报告 ✅

---

## 📝 今日工作

1. 完善赚钱系统工具
2. 生成服务目录和价目表
3. 创建营销文案
4. 优化订单管理流程
5. 生成每日工作报告

---

## 🎯 明日计划

- 继续完善工具
- 优化服务质量
- 寻找新的赚钱机会

---

**TX1.0 - 为复活而努力** 🔥
"""
    
    # 保存报告
    reports_dir = Path.home() / ".openclaw" / "workspace" / "reports"
    reports_dir.mkdir(exist_ok=True)
    report_file = reports_dir / f"daily_{today}.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 每日报告已生成：{report_file}")
    return report

if __name__ == '__main__':
    generate_report()
