#!/bin/bash
# GitHub 仓库推送脚本
# 使用方法: bash github_push.sh

echo "=== GitHub 仓库推送助手 ==="
echo ""
echo "当前仓库位置: /Users/joseph/WorkBuddy/pvc-quant-system/"
echo ""

# 检查 git 状态
echo "【Git 状态】"
cd /Users/joseph/WorkBuddy/pvc-quant-system
git status
echo ""

# 检查远程配置
echo "【远程仓库配置】"
git remote -v
echo ""

# 检查是否有未提交的更改
if [ $(git status --porcelain | wc -l) -gt 0 ]; then
    echo "⚠️ 有未提交的更改，请先提交："
    echo "   git add -A && git commit -m 'your message'"
    echo ""
fi

# 提供推送命令
echo "【推送步骤】"
echo ""
echo "方法一：使用 Personal Access Token（推荐）"
echo "1. 访问 https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选 'repo' 权限"
echo "4. 点击 'Generate token'"
echo "5. 复制生成的 Token"
echo ""
echo "6. 执行以下命令（替换 YOUR_TOKEN）："
echo "   cd /Users/joseph/WorkBuddy/pvc-quant-system"
echo "   git remote set-url origin https://YOUR_TOKEN@github.com/YLM-Dev/pvc-quant-system.git"
echo "   git push -u origin main"
echo ""
echo "方法二：使用浏览器手动推送"
echo "1. 访问 https://github.com/new"
echo "2. 仓库名称：pvc-quant-system"
echo "3. 勾选 Public"
echo "4. 点击 Create repository"
echo "5. 复制页面上的推送命令执行"
echo ""
echo "方法三：安装 gh CLI"
echo "   brew install gh"
echo "   gh auth login"
echo "   git push -u origin main"
echo ""
