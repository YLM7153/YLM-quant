"""
实盘执行引擎
负责接收信号、执行交易、管理持仓
"""

import logging
from typing import Optional, List
from datetime import datetime
import asyncio

from core.strategy import AveragingLineStrategy, PriceData
from core.signal import SignalGenerator, Signal
from core.risk import RiskManager, Position
from core.lease import LeaseManager

logger = logging.getLogger(__name__)


class LiveEngine:
    """
    实盘执行引擎
    
    流程：
    1. 订阅行情数据
    2. 计算策略信号
    3. 执行交易
    4. 管理持仓和风险
    """
    
    def __init__(
        self,
        symbols: List[str],
        strategy_config: dict,
        risk_config: dict,
        lease_config: dict
    ):
        self.symbols = symbols
        self.strategy = AveragingLineStrategy(**strategy_config)
        self.risk_manager = RiskManager(**risk_config)
        self.signal_generator = SignalGenerator()
        self.lease_manager = LeaseManager(**lease_config)
        
        self._price_history: dict = {sym: [] for sym in symbols}
        self._running = False
        
    async def start(self):
        """启动引擎"""
        self._running = True
        logger.info("实盘引擎启动")
        
        # 启动租约管理
        asyncio.create_task(self.lease_manager.start())
        
        # 启动主循环
        await self._main_loop()
        
    async def _main_loop(self):
        """主循环"""
        while self._running:
            try:
                for symbol in self.symbols:
                    await self._process_symbol(symbol)
                await asyncio.sleep(1)  # 每秒检查一次
            except Exception as e:
                logger.error(f"主循环错误: {e}")
                await asyncio.sleep(5)
                
    async def _process_symbol(self, symbol: str):
        """处理单个交易品种"""
        # 1. 获取最新价格（实际中从API获取）
        latest_price = await self._get_latest_price(symbol)
        if latest_price is None:
            return
            
        # 2. 更新价格历史
        self._price_history[symbol].append(latest_price)
        if len(self._price_history[symbol]) > 100:
            self._price_history[symbol] = self._price_history[symbol][-100:]
            
        # 3. 计算策略信号
        prices = [p.close_price for p in self._price_history[symbol]]
        averages = self.strategy.calculate_averages(prices)
        strategy_result = self.strategy.generate_signal(
            latest_price.close_price,
            averages
        )
        
        # 4. 检查方向翻转
        if strategy_result == 'HOLD' and self.risk_manager._positions:
            for position in self.risk_manager._positions:
                if position.symbol == symbol:
                    flip_result = self.strategy.check_direction_flip(
                        latest_price.close_price,
                        self._price_history[symbol][-2].close_price if len(self._price_history[symbol]) > 1 else latest_price.close_price,
                        position.direction
                    )
                    if flip_result == 'flip' and self.strategy.close_on_dir_flip:
                        logger.info(f"方向翻转，平掉 {symbol} 持仓")
                        self.risk_manager.close_position(symbol, latest_price.close_price)
                        return
                        
        # 5. 生成可执行信号
        if strategy_result != 'HOLD':
            signal = self.signal_generator.generate(
                strategy_result,
                symbol,
                latest_price.close_price,
                confidence=0.8,
                reason=f"均价线信号: {strategy_result}"
            )
            
            if signal:
                await self._execute_signal(signal)
                
    async def _get_latest_price(self, symbol: str) -> Optional[PriceData]:
        """
        获取最新价格（实际中调用数据源API）
        这里返回模拟数据
        """
        # 模拟数据生成
        import random
        base_price = 5000.0
        return PriceData(
            timestamp=datetime.now(),
            open_price=base_price,
            high_price=base_price + 10,
            low_price=base_price - 10,
            close_price=base_price + random.uniform(-5, 5),
            volume=random.uniform(1000, 5000),
            settlement=base_price + random.uniform(-3, 3)
        )
        
    async def _execute_signal(self, signal: Signal):
        """执行交易信号"""
        logger.info(f"执行信号: {signal.signal_type} {signal.symbol} @ {signal.price}")
        
        # 这里应该调用 brokerage API 执行实际交易
        # 例如：broker.place_order(signal)
        
        # 更新持仓
        if signal.signal_type == 'BUY':
            position = Position(
                symbol=signal.symbol,
                direction='long',
                quantity=10,  # 示例数量
                entry_price=signal.price,
                stop_loss=self.risk_manager.calculate_stop_loss(signal.price, 'long'),
                take_profit=self.risk_manager.calculate_take_profit(signal.price, 'long'),
                entry_time=datetime.now().isoformat()
            )
            self.risk_manager.add_position(position)
            
        elif signal.signal_type == 'SELL':
            # 空头开仓或平多
            position = Position(
                symbol=signal.symbol,
                direction='short',
                quantity=10,
                entry_price=signal.price,
                stop_loss=self.risk_manager.calculate_stop_loss(signal.price, 'short'),
                take_profit=self.risk_manager.calculate_take_profit(signal.price, 'short'),
                entry_time=datetime.now().isoformat()
            )
            self.risk_manager.add_position(position)
            
    def get_status(self) -> dict:
        """获取引擎状态"""
        return {
            "symbols": self.symbols,
            "positions": [
                {
                    "symbol": p.symbol,
                    "direction": p.direction,
                    "quantity": p.quantity,
                    "entry_price": p.entry_price
                }
                for p in self.risk_manager._positions
            ],
            "daily_pnl": self.risk_manager.get_daily_pnl(),
            "lease_status": self.lease_manager.get_status()
        }
