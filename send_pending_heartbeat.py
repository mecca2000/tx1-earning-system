#!/usr/bin/env python3
"""
检查并发送待发送的心跳报告（主会话在交互时调用）
"""
import subprocess
from pathlib import Path

PENDING_REPORT = Path.home() / ".openclaw" / "state" / "pending_heartbeat_report.txt"
TARGET_USER = "ou_6411571988fd02748bc696e0f01a489e"

def main():
    if not PENDING_REPORT.exists():
        return  # 没有待发送的报告
    
    report = PENDING_REPORT.read_text().strip()
    if not report:
        return
    
    # 发送飞书消息
    try:
        result = subprocess.run(
            ['openclaw', 'message', 'send', '--channel', 'feishu', '--target', f'user:{TARGET_USER}', '-m', report],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            # 发送成功后删除文件
            PENDING_REPORT.unlink()
    except Exception:
        pass  # 发送失败，保留文件下次再试

if __name__ == '__main__':
    main()
