"""
风险控制模块
管理仓位、止损、风控规则
"""

from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Position:
    """持仓"""
    symbol: str
    direction: str  # 'long' or 'short'
    quantity: int
    entry_price: float
    stop_loss: Optional[float]
    take_profit: Optional[float]
    entry_time: Optional[str] = None


class RiskManager:
    """
    风险管理器
    
    功能：
    1. 仓位控制（最大持仓、单笔风险）
    2. 止损止盈管理
    3. 每日亏损限额
    """
    
    def __init__(
        self,
        max_position_size: int = 100,
        max_daily_loss_pct: float = 0.05,  # 5%
        max_open_positions: int = 5,
        default_stop_loss_pct: float = 0.02,
        default_take_profit_pct: float = 0.04
    ):
        self.max_position_size = max_position_size
        self.max_daily_loss_pct = max_daily_loss_pct
        self.max_open_positions = max_open_positions
        self.default_stop_loss_pct = default_stop_loss_pct
        self.default_take_profit_pct = default_take_profit_pct
        
        self._daily_pnl = 0.0
        self._positions: list = []
        
    def calculate_stop_loss(self, entry_price: float, direction: str) -> float:
        """计算默认止损价"""
        if direction == 'long':
            return entry_price * (1 - self.default_stop_loss_pct)
        else:
            return entry_price * (1 + self.default_stop_loss_pct)
    
    def calculate_take_profit(self, entry_price: float, direction: str) -> float:
        """计算默认止盈价"""
        if direction == 'long':
            return entry_price * (1 + self.default_take_profit_pct)
        else:
            return entry_price * (1 - self.default_take_profit_pct)
    
    def can_open_position(self) -> bool:
        """检查是否可以开新仓位"""
        if len(self._positions) >= self.max_open_positions:
            logger.warning(f"已达到最大持仓数: {len(self._positions)}")
            return False
        return True
    
    def check_stop_loss(self, position: Position, current_price: float) -> Optional[str]:
        """
        检查是否触发止损/止盈
        
        Returns:
            'stop_loss', 'take_profit', or None
        """
        if position.direction == 'long':
            if position.stop_loss and current_price <= position.stop_loss:
                logger.warning(f"触发止损: {position.symbol}")
                return 'stop_loss'
            if position.take_profit and current_price >= position.take_profit:
                logger.info(f"触发止盈: {position.symbol}")
                return 'take_profit'
        else:  # short
            if position.stop_loss and current_price >= position.stop_loss:
                logger.warning(f"触发止损: {position.symbol}")
                return 'stop_loss'
            if position.take_profit and current_price <= position.take_profit:
                logger.info(f"触发止盈: {position.symbol}")
                return 'take_profit'
        return None
    
    def add_position(self, position: Position):
        """添加持仓"""
        self._positions.append(position)
        logger.info(f"新开持仓: {position.symbol} {position.direction}")
    
    def close_position(self, symbol: str, exit_price: float) -> float:
        """
        平仓并计算盈亏
        
        Returns:
            盈亏金额
        """
        for i, pos in enumerate(self._positions):
            if pos.symbol == symbol:
                if pos.direction == 'long':
                    pnl = (exit_price - pos.entry_price) * pos.quantity
                else:
                    pnl = (pos.entry_price - exit_price) * pos.quantity
                    
                self._positions.pop(i)
                self._daily_pnl += pnl
                logger.info(f"平仓 {symbol}, PnL: {pnl:.2f}")
                return pnl
                
        return 0.0
    
    def get_daily_pnl(self) -> float:
        """获取当日盈亏"""
        return self._daily_pnl
    
    def check_daily_limit(self) -> bool:
        """检查是否触发每日亏损限额"""
        # 这里需要初始资金来计算百分比
        # 简化实现：直接检查绝对值
        return abs(self._daily_pnl) < 10000  # 示例阈值
