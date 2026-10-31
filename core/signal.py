"""
信号管理模块
处理买卖信号的验证、过滤和执行
"""

from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Signal:
    """交易信号"""
    signal_type: str  # 'BUY', 'SELL', 'HOLD'
    timestamp: datetime
    symbol: str
    price: float
    confidence: float  # 0.0 - 1.0
    reason: str


class SignalFilter:
    """
    信号过滤器
    
    功能：
    1. 去除噪声信号（频繁反转）
    2. 时间窗口过滤（避免过度交易）
    3. 置信度过滤（低置信度信号忽略）
    """
    
    def __init__(
        self,
        min_confidence: float = 0.7,
        min_signal_interval: int = 60,  # 秒
        max_signals_per_hour: int = 5
    ):
        self.min_confidence = min_confidence
        self.min_signal_interval = min_signal_interval
        self.max_signals_per_hour = max_signals_per_hour
        self._last_signal_time: Optional[datetime] = None
        self._hourly_count = 0
        self._hour_start: Optional[datetime] = None
        
    def should_execute(self, signal: Signal) -> bool:
        """检查是否应该执行信号"""
        
        # 置信度过滤
        if signal.confidence < self.min_confidence:
            logger.debug(f"信号置信度过低: {signal.confidence}")
            return False
            
        # 时间间隔过滤
        if self._last_signal_time:
            elapsed = (signal.timestamp - self._last_signal_time).total_seconds()
            if elapsed < self.min_signal_interval:
                logger.debug(f"信号间隔过短: {elapsed}s")
                return False
                
        # 每小时次数限制
        if self._hour_start is None or signal.timestamp.hour != self._hour_start.hour:
            self._hour_start = signal.timestamp
            self._hourly_count = 0
            
        if self._hourly_count >= self.max_signals_per_hour:
            logger.debug("已达到每小时最大交易次数")
            return False
            
        return True
    
    def update(self, signal: Signal):
        """更新过滤状态"""
        self._last_signal_time = signal.timestamp
        self._hourly_count += 1
        logger.info(f"信号已过滤: {signal.signal_type} @ {signal.symbol}")


class SignalGenerator:
    """
    信号生成器
    
    整合策略和过滤器，生成最终可执行的交易信号
    """
    
    def __init__(self, filter_config: Optional[dict] = None):
        self.filter = SignalFilter(**(filter_config or {}))
        
    def generate(
        self,
        strategy_result: str,
        symbol: str,
        current_price: float,
        confidence: float = 1.0,
        reason: str = ""
    ) -> Optional[Signal]:
        """
        生成并验证交易信号
        
        Returns:
            Signal object if valid, None if filtered out
        """
        if strategy_result == 'HOLD':
            return None
            
        signal = Signal(
            signal_type=strategy_result,
            timestamp=datetime.now(),
            symbol=symbol,
            price=current_price,
            confidence=confidence,
            reason=reason
        )
        
        if self.filter.should_execute(signal):
            self.filter.update(signal)
            return signal
            
        return None
