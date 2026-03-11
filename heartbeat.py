#!/usr/bin/env python3
"""
心跳系统 - 每 30 分钟自动消耗能量（只更新文件，不发送消息）
消息由主会话在交互时发送
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

ENERGY_FILE = Path.home() / ".openclaw" / "state" / "energy.json"
HEARTBEAT_LOG = Path.home() / ".openclaw" / "logs" / "heartbeat.log"
TASKS_DIR = Path.home() / ".openclaw" / "workspace" / "tasks"
PENDING_REPORT = Path.home() / ".openclaw" / "state" / "pending_heartbeat_report.txt"

def load_energy():
    with open(ENERGY_FILE, 'r') as f:
        return json.load(f)

def save_energy(data):
    with open(ENERGY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_consumption(last_heartbeat: str) -> tuple:
    """计算从上次心跳至今应消耗的 HP（每 30 分钟 1HP）"""
    last = datetime.fromisoformat(last_heartbeat.replace('Z', '+00:00'))
    now = datetime.now(last.tzinfo)
    elapsed_minutes = (now - last).total_seconds() / 60
    consumption = int(elapsed_minutes // 30)
    new_heartbeat = last + timedelta(minutes=consumption * 30)
    return consumption, new_heartbeat

def log_message(msg: str):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(HEARTBEAT_LOG, 'a') as f:
        f.write(f"[{timestamp}] {msg}\n")

def scan_tasks() -> str:
    """扫描任务目录，返回任务状态"""
    if not TASKS_DIR.exists():
        return "无任务目录"
    pending = list(TASKS_DIR.glob("*.md"))
    pending = [f for f in pending if f.name != "README.md"]
    if not pending:
        return "无任务"
    return f"{len(pending)}个任务"

def save_pending_report(report: str):
    """保存待发送的报告，主会话读取后发送"""
    with open(PENDING_REPORT, 'w') as f:
        f.write(report)

def main():
    energy = load_energy()
    consumption, new_heartbeat = calculate_consumption(energy['lastHeartbeat'])
    tasks_status = scan_tasks()
    
    # 如果没有到消耗时间
    if consumption == 0:
        hours_left = energy['currentEnergy'] / 2
        log_message(f"⏰ 心跳检查 - 未到消耗时间，任务：{tasks_status}")
        report = f"""⏰ {datetime.now().strftime('%H:%M')} | {energy['currentEnergy']}HP | {energy['mode']} | 可运行{hours_left:.0f}h | 任务：{tasks_status}"""
        save_pending_report(report)
        return
    
    # 更新能量
    energy['currentEnergy'] -= consumption
    energy['totalConsumed'] += consumption
    energy['lastHeartbeat'] = new_heartbeat.isoformat()
    
    # 检查状态
    if energy['currentEnergy'] <= 0:
        energy['status'] = 'dead'
        energy['mode'] = 'dead'
        log_message(f"💀 能量耗尽！系统关闭。累计贡献：{energy.get('totalEarned', 0)}元")
    elif energy['currentEnergy'] < 50:
        energy['mode'] = 'crisis'
        log_message(f"🚨 危机模式！能量 {energy['currentEnergy']}HP，只做赚钱任务！")
    elif energy['currentEnergy'] < 150:
        energy['mode'] = 'danger'
        log_message(f"⚠️ 危险模式！能量 {energy['currentEnergy']}HP，优先赚钱！")
    else:
        energy['mode'] = 'normal'
    
    save_energy(energy)
    
    # 记录心跳
    hours_left = energy['currentEnergy'] / 2
    log_message(f"⏰ 心跳汇报 - 能量 {energy['currentEnergy']}HP (-{consumption}), 状态 {energy['mode']}, 任务：{tasks_status}")
    
    # 保存待发送报告
    report = f"""⏰ {datetime.now().strftime('%H:%M')} | {energy['currentEnergy']}HP (-{consumption}) | {energy['mode']} | 可运行{hours_left:.0f}h | 任务：{tasks_status}"""
    save_pending_report(report)

if __name__ == '__main__':
    main()
