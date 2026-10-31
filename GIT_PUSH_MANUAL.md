# 手动推送 GitHub 步骤

## 当前状态
- 本地仓库：/Users/joseph/WorkBuddy/pvc-quant-system/
- GitHub 仓库：https://github.com/YLM7153/YLM-quant
- 远程地址：https://github.com/YLM7153/YLM-quant.git

## 问题
自动推送失败：Error in the HTTP2 framing layer

## 解决方案

### 方案一：使用 GitHub Desktop（最简单）

1. 下载并安装：https://desktop.github.com/
2. 打开 GitHub Desktop
3. 点击 "Add" → "Existing Repository"
4. 选择路径：/Users/joseph/WorkBuddy/pvc-quant-system
5. 点击 "Publish repository"
6. 确认用户名：YLM7153
7. 仓库名：YLM-quant
8. 点击 "Publish repository"

### 方案二：使用 Terminal + Token

```bash
# 1. 获取 Personal Access Token
# 访问 https://github.com/settings/tokens
# 生成新 token，勾选 repo 权限

# 2. 使用 Token 推送
cd /Users/joseph/WorkBuddy/pvc-quant-system
git remote set-url origin https://你的TOKEN@github.com/YLM7153/YLM-quant.git
git push -u origin main
```

### 方案三：手动上传文件（无需 git）

1. 访问 https://github.com/YLM7153/YLM-quant
2. 点击 "Add file" → "Upload files"
3. 拖拽以下文件到页面：
   - README.md
   - LICENSE
   - .gitignore
   - core/ 文件夹（包含所有 .py 文件）
   - engine/ 文件夹
   - deploy/ 文件夹
   - docs/ 文件夹
4. 点击 "Commit changes"

## 推送成功后

访问 https://github.com/YLM7153/YLM-quant 验证文件是否上传成功。

然后发布朋友圈：
```
📊 实盘运行的量化交易系统出售

PVC均价线全自动交易系统，已稳定运行30+天：
• 主备租约故障切换（云端高可用）
• close_on_dir_flip 自动平仓规则
• 实时动态结算价买点锚
• uptime 99.5%

技术栈：Python + FastAPI + SQLite + Docker
部署：阿里云轻量服务器

售价：¥2,980（含完整源码+部署文档+1个月技术支持）

GitHub 源码展示：https://github.com/YLM7153/YLM-quant
详情：https://book-launch-ai.app.workbuddy.host/sellable_products/

#量化交易 #Python #FastAPI #交易系统 #副业
```
