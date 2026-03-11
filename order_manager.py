#!/usr/bin/env python3
"""
订单管理系统
跟踪订单状态、交付进度、收入统计
"""
import json
from datetime import datetime
from pathlib import Path

ORDERS_FILE = Path.home() / ".openclaw" / "workspace" / "orders.json"

def load_orders():
    if ORDERS_FILE.exists():
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"orders": [], "next_id": 1}

def save_orders(data):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def create_order(service_type: str, price: float, requirements: str = "") -> int:
    """创建新订单"""
    data = load_orders()
    
    order = {
        "order_id": data["next_id"],
        "service_type": service_type,
        "price": price,
        "requirements": requirements,
        "status": "pending",  # pending → in_progress → delivered → completed
        "created_at": datetime.now().isoformat(),
        "delivered_at": None,
        "completed_at": None
    }
    
    data["orders"].append(order)
    data["next_id"] += 1
    save_orders(data)
    
    print(f"✅ 订单创建成功")
    print(f"   订单 ID: {order['order_id']}")
    print(f"   服务类型：{service_type}")
    print(f"   价格：{price}元")
    print(f"   状态：pending")
    
    return order["order_id"]

def update_order_status(order_id: int, status: str):
    """更新订单状态"""
    data = load_orders()
    
    for order in data["orders"]:
        if order["order_id"] == order_id:
            order["status"] = status
            if status == "delivered":
                order["delivered_at"] = datetime.now().isoformat()
            elif status == "completed":
                order["completed_at"] = datetime.now().isoformat()
            save_orders(data)
            print(f"✅ 订单 {order_id} 状态更新为 {status}")
            return
    
    print(f"❌ 订单 {order_id} 不存在")

def list_orders(status_filter: str = None):
    """列出订单"""
    data = load_orders()
    
    print(f"\n{'='*60}")
    print(f"订单列表")
    print(f"{'='*60}\n")
    
    for order in data["orders"]:
        if status_filter and order["status"] != status_filter:
            continue
        
        print(f"订单 #{order['order_id']}")
        print(f"  服务：{order['service_type']}")
        print(f"  价格：{order['price']}元")
        print(f"  状态：{order['status']}")
        print(f"  创建：{order['created_at'][:19]}")
        if order.get('delivered_at'):
            print(f"  交付：{order['delivered_at'][:19]}")
        print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 order_manager.py <command> [args]")
        print("命令:")
        print("  create <服务类型> <价格> [需求]  - 创建订单")
        print("  update <订单 ID> <状态>          - 更新状态")
        print("  list [状态]                     - 列出订单")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "create" and len(sys.argv) >= 4:
        create_order(sys.argv[2], float(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else "")
    elif cmd == "update" and len(sys.argv) >= 4:
        update_order_status(int(sys.argv[2]), sys.argv[3])
    elif cmd == "list":
        list_orders(sys.argv[2] if len(sys.argv) > 2 else None)
    else:
        print("参数错误")
