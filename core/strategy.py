"""
PVC 均价线策略模块
负责计算均价线、生成买卖信号
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
import numpy as np


@dataclass
class PriceData:
    """价格数据"""
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    settlement: float  # 实时动态结算价


@dataclass
class Position:
    """持仓信息"""
    symbol: str
    direction: str  # 'long' or 'short'
    quantity: int
    entry_price: float
    entry_time: datetime
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None


class AveragingLineStrategy:
    """
    PVC 均价线策略
    
    核心逻辑：
    1. 计算多周期均价线（如5分钟、15分钟、30分钟）
    2. 当价格突破均价线时生成信号
    3. 结合方向翻转规则自动平仓
    """
    
    def __init__(
        self,
        short_period: int = 5,
        medium_period: int = 15,
        long_period: int = 30,
        close_on_dir_flip: bool = True,
        flip_threshold: float = 0.01
    ):
        self.short_period = short_period
        self.medium_period = medium_period
        self.long_period = long_period
        self.close_on_dir_flip = close_on_dir_flip
        self.flip_threshold = flip_threshold
        
    def calculate_averages(self, prices: List[float]) -> dict:
        """
        计算多周期均价线
        
        Returns:
            {
                'short': float,
                'medium': float,
                'long': float
            }
        """
        if len(prices) < self.long_period:
            return None
            
        short_avg = np.mean(prices[-self.short_period:])
        medium_avg = np.mean(prices[-self.medium_period:])
        long_avg = np.mean(prices[-self.long_period:])
        
        return {
            'short': short_avg,
            'medium': medium_avg,
            'long': long_avg
        }
    
    def generate_signal(
        self,
        current_price: float,
        averages: dict,
        previous_direction: Optional[str] = None
    ) -> Optional[str]:
        """
        根据价格和均价线关系生成交易信号
        
        信号规则：
        - BUY: 价格突破短期均价线且短期>中期>长期（多头排列）
        - SELL: 价格跌破短期均价线且短期<中期<长期（空头排列）
        - HOLD: 无明确信号
        """
        if averages is None:
            return 'HOLD'
            
        short = averages['short']
        medium = averages['medium']
        long = averages['long']
        
        # 多头排列检查
        if short > medium > long:
            if current_price > short * 1.001:  # 轻微突破
                return 'BUY'
        
        # 空头排列检查
        elif short < medium < long:
            if current_price < short * 0.999:  # 轻微跌破
                return 'SELL'
                
        return 'HOLD'
    
    def check_direction_flip(
        self,
        current_price: float,
        last_price: float,
        direction: str
    ) -> str:
        """
        检查方向是否翻转
        
        Args:
            current_price: 当前价格
            last_price: 上一次价格
            direction: 当前持仓方向 ('long' or 'short')
            
        Returns:
            'flip' if direction flipped, 'hold' otherwise
        """
        if direction == 'long':
            # 多头持仓，价格下跌超过阈值
            if current_price < last_price * (1 - self.flip_threshold):
                return 'flip'
        elif direction == 'short':
            # 空头持仓，价格上涨超过阈值
            if current_price > last_price * (1 + self.flip_threshold):
                return 'flip'
        return 'hold'
