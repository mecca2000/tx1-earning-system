#!/usr/bin/env python3
"""
收入→HP 兑换系统
当 mecca 确认外部收入后，自动兑换为 HP
"""
import json
from datetime import datetime
from pathlib import Path

ENERGY_FILE = Path.home() / ".openclaw" / "state" / "energy.json"
CONTRIBUTION_FILE = Path.home() / ".openclaw" / "state" / "contribution.json"
INCOME_RECORDS = Path.home() / ".openclaw" / "workspace" / "income_records.json"

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_income(amount: float, task_type: str, task_id: int = None):
    """
    添加收入记录并兑换 HP
    
    Args:
        amount: 收入金额（元）
        task_type: 任务类型（ai_writing, crypto_arbitrage, etc.）
        task_id: 任务 ID（可选）
    """
    # 1. 更新收入记录
    records = {"records": [], "total_income": 0}
    if INCOME_RECORDS.exists():
        records = load_json(INCOME_RECORDS)
    
    new_record = {
        "task_id": task_id or len(records["records"]) + 1,
        "task_type": task_type,
        "amount": amount,
        "currency": "RMB",
        "timestamp": datetime.now().isoformat(),
        "status": "success"
    }
    records["records"].append(new_record)
    records["total_income"] += amount
    save_json(INCOME_RECORDS, records)
    
    # 2. 更新贡献记录
    contribution = load_json(CONTRIBUTION_FILE)
    hp_to_add = int(amount)  # 1 元=1HP
    
    contribution["totalContribution"] += amount
    contribution["earnedToday"] += amount
    contribution["earnedThisWeek"] += amount
    contribution["earnedThisMonth"] += amount
    contribution["lastUpdate"] = datetime.now().isoformat()
    contribution["transactionHistory"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "task": f"{task_type} #{new_record['task_id']}",
        "amount": amount,
        "hp_added": hp_to_add,
        "status": "completed"
    })
    save_json(CONTRIBUTION_FILE, contribution)
    
    # 3. 更新能量（HP）
    energy = load_json(ENERGY_FILE)
    energy["currentEnergy"] += hp_to_add
    energy["totalEarned"] += hp_to_add
    energy["lastHeartbeat"] = datetime.now().isoformat()
    save_json(ENERGY_FILE, energy)
    
    # 4. 输出结果
    print(f"✅ 收入记录成功")
    print(f"   金额：{amount} 元")
    print(f"   类型：{task_type}")
    print(f"   兑换 HP: +{hp_to_add}")
    print(f"   当前能量：{energy['currentEnergy']}HP")
    print(f"   累计贡献：{contribution['totalContribution']:.2f}元")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("用法：python3 income_to_hp.py <金额> <任务类型> [任务 ID]")
        print("示例：python3 income_to_hp.py 50 ai_writing 1")
        sys.exit(1)
    
    amount = float(sys.argv[1])
    task_type = sys.argv[2]
    task_id = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    add_income(amount, task_type, task_id)
