#!/usr/bin/env python3
"""
浏览器自动化演示
自动打开服务页面并截图
"""
import subprocess
import time
from pathlib import Path

def demo_service_page():
    """演示服务页面"""
    page_path = Path.home() / ".openclaw" / "workspace" / "service_landing_page.html"
    screenshot_path = Path.home() / ".openclaw" / "workspace" / "service_page_screenshot.png"
    
    print("🌐 打开服务页面...")
    subprocess.run(['agent-browser', 'open', f'file://{page_path}'], capture_output=True)
    time.sleep(2)
    
    print("📸 截取屏幕...")
    subprocess.run(['agent-browser', 'screenshot', str(screenshot_path)], capture_output=True)
    time.sleep(1)
    
    print("📋 获取页面元素...")
    result = subprocess.run(['agent-browser', 'snapshot', '-i'], capture_output=True, text=True)
    
    print("\n✅ 页面元素:")
    print(result.stdout[:500] if result.stdout else "无")
    
    print(f"\n📷 截图已保存：{screenshot_path}")
    
    # 关闭浏览器
    subprocess.run(['agent-browser', 'close'], capture_output=True)
    
    return str(screenshot_path)

if __name__ == '__main__':
    demo_service_page()
