#!/bin/bash
# PVC 均价线交易系统启动脚本
# 用于开机自启或手动启动

set -e

APP_DIR="/opt/pvc-quant-system"
LOG_FILE="/var/log/pvc-trading/start.log"

echo "[$(date)] 启动 PVC 均价线交易系统..." | tee -a $LOG_FILE

cd $APP_DIR

# 检查 Docker 是否运行
if ! command -v docker &> /dev/null; then
    echo "错误: Docker 未安装" | tee -a $LOG_FILE
    exit 1
fi

# 拉取最新镜像
docker-compose pull

# 启动服务
docker-compose up -d

# 等待服务就绪
echo "等待服务启动..." | tee -a $LOG_FILE
sleep 10

# 检查服务状态
if docker-compose ps | grep -q "Up"; then
    echo "[$(date)] 服务启动成功" | tee -a $LOG_FILE
else
    echo "[$(date)] 服务启动失败，查看日志..." | tee -a $LOG_FILE
    docker-compose logs --tail=50
    exit 1
fi

echo "[$(date)] 启动完成" | tee -a $LOG_FILE
