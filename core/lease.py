"""
主备租约管理器
实现云端高可用的故障切换机制
"""

import time
import logging
import asyncio
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class Node:
    """节点类"""
    
    def __init__(self, url: str):
        self.url = url
        self.is_alive = False
        self.last_heartbeat: Optional[datetime] = None
        
    async def check_health(self) -> bool:
        """检查节点健康状态"""
        # 实际实现中这里会发送HTTP请求
        # 这里简化为模拟
        try:
            # await asyncio.sleep(0.1)  # 模拟网络延迟
            self.is_alive = True
            self.last_heartbeat = datetime.now()
            return True
        except Exception as e:
            self.is_alive = False
            logger.error(f"节点健康检查失败: {e}")
            return False


class LeaseManager:
    """
    主备租约管理器
    
    功能：
    1. 监控主节点心跳
    2. 主节点失效时自动切换到备节点
    3. 通知运维人员
    """
    
    def __init__(
        self,
        primary_url: str,
        backup_url: str,
        heartbeat_interval: int = 10
    ):
        self.primary = Node(primary_url)
        self.backup = Node(backup_url)
        self.heartbeat_interval = heartbeat_interval
        self.current_active = self.primary
        self._running = False
        
    async def start(self):
        """启动租约管理器"""
        self._running = True
        logger.info("租约管理器启动")
        await self._heartbeat_loop()
        
    async def _heartbeat_loop(self):
        """心跳监控循环"""
        while self._running:
            try:
                await self.check_heartbeat()
                await asyncio.sleep(self.heartbeat_interval)
            except Exception as e:
                logger.error(f"心跳循环错误: {e}")
                await asyncio.sleep(self.heartbeat_interval)
                
    async def check_heartbeat(self):
        """检查心跳并决定是否切换"""
        primary_alive = await self.primary.check_health()
        
        if primary_alive:
            if self.current_active != self.primary:
                logger.info("主节点恢复，切换回主节点")
                await self._switch_to(self.primary)
        else:
            logger.warning("主节点无响应，准备切换")
            backup_alive = await self.backup.check_health()
            if backup_alive:
                await self._switch_to(self.backup)
                self.notify_ops("主节点失效，备节点已接管")
            else:
                logger.error("主备节点均不可用！")
                
    async def _switch_to(self, node: Node):
        """切换到指定节点"""
        logger.info(f"切换到节点: {node.url}")
        self.current_active = node
        # 这里可以添加实际的连接切换逻辑
        
    def notify_ops(self, message: str):
        """通知运维人员"""
        logger.critical(f"[ALERT] {message}")
        # 实际实现中可以发送邮件、短信或钉钉通知
        # send_notification(message)
        
    def get_status(self) -> dict:
        """获取当前状态"""
        return {
            "current_active": self.current_active.url,
            "primary_alive": self.primary.is_alive,
            "backup_alive": self.backup.is_alive,
            "last_heartbeat": self.current_active.last_heartbeat.isoformat() if self.current_active.last_heartbeat else None
        }
