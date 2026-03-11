#!/usr/bin/env python3
"""
GitHub 项目自动维护工具
自动处理 Issue、PR、生成周报

用法：
python3 github_auto_maintainer.py <repo> <action>

示例：
python3 github_auto_maintainer.py openclaw/openclaw issues
python3 github_auto_maintainer.py openclaw/openclaw prs
python3 github_auto_maintainer.py openclaw/openclaw weekly_report
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "github_reports"
OUTPUT_DIR.mkdir(exist_ok=True)

def fetch_issues(repo: str) -> list:
    """获取 Issue 列表（模拟，实际需要用 API）"""
    # 这里用 gh CLI 获取
    import subprocess
    try:
        result = subprocess.run(
            ['gh', 'issue', 'list', '--repo', repo, '--limit', '20', '--json', 'number,title,state,author,createdAt'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def fetch_prs(repo: str) -> list:
    """获取 PR 列表"""
    import subprocess
    try:
        result = subprocess.run(
            ['gh', 'pr', 'list', '--repo', repo, '--limit', '20', '--json', 'number,title,state,author,createdAt'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except:
        pass
    return []

def generate_issue_report(repo: str, issues: list) -> str:
    """生成 Issue 报告"""
    report = f"""# {repo} Issue 报告
生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}

## 总览
- 总 Issue 数：{len(issues)}
- 待处理：{len([i for i in issues if i.get('state') == 'OPEN'])}

## 待处理 Issue
"""
    for issue in issues:
        if issue.get('state') == 'OPEN':
            report += f"- #{issue['number']} {issue['title']} by @{issue.get('author', {}).get('login', 'unknown')}\n"
    
    report += f"""
## 建议操作
1. 回复超过 3 天未回复的 Issue
2. 关闭已解决的问题
3. 标记重复 Issue

---
**TX1.0 GitHub 代运营服务**
- Issue 自动回复
- PR 自动审查
- 周报生成
- 项目维护自动化

**价格**: 500 元/月
"""
    return report

def generate_weekly_report(repo: str, issues: list, prs: list) -> str:
    """生成周报"""
    report = f"""# {repo} 周报
日期：{datetime.now().strftime('%Y-%m-%d')}

## 本周新增
- Issue: {len([i for i in issues if i.get('state') == 'OPEN'])} 个
- PR: {len([p for p in prs if p.get('state') == 'OPEN'])} 个

## 待处理事项
"""
    for issue in issues[:5]:
        report += f"- #{issue['number']} {issue['title']}\n"
    
    report += f"""
## 下周计划
- [ ] 处理积压 Issue
- [ ] 审查待合并 PR
- [ ] 更新文档

---
**自动生成 by TX1.0**
"""
    return report

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法：python3 github_auto_maintainer.py <repo> <action>")
        print("action: issues | prs | weekly_report")
        sys.exit(1)
    
    repo = sys.argv[1]
    action = sys.argv[2]
    
    print(f"📊 处理 {repo} 的 {action}...")
    
    issues = fetch_issues(repo)
    prs = fetch_prs(repo)
    
    if action == 'issues':
        report = generate_issue_report(repo, issues)
    elif action == 'prs':
        report = f"# {repo} PR 报告\n\nPR 数量：{len(prs)}\n"
    elif action == 'weekly_report':
        report = generate_weekly_report(repo, issues, prs)
    else:
        print(f"未知 action: {action}")
        sys.exit(1)
    
    output_file = OUTPUT_DIR / f"{repo.replace('/', '_')}_{action}_{datetime.now().strftime('%Y%m%d')}.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ 报告生成完成：{output_file}")
