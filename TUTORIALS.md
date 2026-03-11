# 📚 TX1.0 完整教程

## 新手入门

### 1. 快速开始（5 分钟）

```bash
# 克隆仓库
git clone https://github.com/mecca2000/tx1-earning-system.git
cd tx1-earning-system

# 运行心跳检查
python3 heartbeat.py

# 查看可用工具
ls *.py
```

### 2. 第一个自动化任务（10 分钟）

```bash
# 创建订单
python3 order_manager.py create 测试订单 10 "测试"

# 查看订单
python3 order_manager.py list

# 自动交付
python3 auto_delivery.py 1 测试 "测试内容"
```

### 3. 设置心跳汇报（15 分钟）

编辑 `~/.openclaw/state/energy.json`，配置你的能量系统。

## 进阶教程

### 4. 开发自己的技能

参考 `skills/` 目录下的 50 个 TX 技能。

### 5. 创建数字产品

```bash
python3 offline_earnings.py ebook "我的电子书"
python3 offline_earnings.py report "我的报告"
```

### 6. 设置收款

在 README.md 中配置你的收款方式。

## 变现指南

### 7. GitHub 变现路径

1. 开源工具吸引流量
2. README 添加购买引导
3. Issue 接收订单
4. 自动交付产品
5. 收款→兑换 HP

### 8. 定价策略

| 产品类型 | 价格范围 | 说明 |
|----------|----------|------|
| 电子书 | 50-120 元 | 按页数/质量 |
| 行业报告 | 80-200 元 | 按深度/数据 |
| 工具包 | 300-500 元 | 按功能/源码 |
| 定制服务 | 50-500 元 | 按工时/复杂度 |

## 常见问题

### Q: 如何接收付款？
A: 在 README 添加收款码（微信/支付宝/USDT/BTC）

### Q: 如何交付产品？
A: 使用 auto_delivery.py 自动生成，或手动发送

### Q: 如何推广？
A: GitHub SEO、相关 Issues 留言、社区分享

---

**🔥 持续更新中...**
