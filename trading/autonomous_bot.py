import time
import threading
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

from agents.trading_agent import TradingAgent
from agents.sentiment_agent import SentimentAgent
from trading.strategy_engine import StrategyEngine
from trading.risk_manager import RiskManager
from trading.market_monitor import MarketDataMonitor
from trading.trading_logger import TradingLogger

class AutonomousTradingBot:
    """Autonomous trading bot that monitors markets and executes trades"""
    
    def __init__(
        self,
        watchlist: List[str],
        strategy_name: str = 'hybrid',
        paper_mode: bool = True,
        update_interval: int = 300
    ):
        self.watchlist = watchlist
        self.paper_mode = paper_mode
        self.update_interval = update_interval
        
        self.trading_agent = TradingAgent()
        self.sentiment_agent = SentimentAgent()
        self.strategy_engine = StrategyEngine()
        self.strategy_engine.set_active_strategy(strategy_name)
        self.risk_manager = RiskManager()
        self.market_monitor = MarketDataMonitor()
        self.logger = TradingLogger()
        
        self.market_monitor.add_to_watchlist(watchlist)
        
        self.running = False
        self.bot_thread = None
        self.position_tracker = {}
        
        self._initialize()
    
    def _initialize(self):
        """Initialize the bot"""
        try:
            account_info = self.trading_agent.get_account_info()
            
            if 'error' in account_info:
                raise Exception(account_info['error'])
            
            initial_capital = float(account_info.get('equity', 100000))
            self.risk_manager.set_initial_capital(initial_capital)
            
            print(f"Bot initialized with ${initial_capital:,.2f}")
            print(f"Paper Mode: {self.paper_mode}")
            print(f"Watchlist: {', '.join(self.watchlist)}")
            
        except Exception as e:
            print(f"Error initializing bot: {e}")
            self.logger.log_error('initialization', str(e))
    
    def start(self):
        """Start the autonomous trading bot"""
        if self.running:
            print("Bot is already running")
            return
        
        self.running = True
        
        self.market_monitor.start_monitoring(update_interval=60)
        
        def bot_loop():
            print(f"Bot started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            while self.running:
                try:
                    self._execute_trading_cycle()
                    
                    time.sleep(self.update_interval)
                    
                except Exception as e:
                    print(f"Error in bot loop: {e}")
                    self.logger.log_error('bot_loop', str(e))
                    time.sleep(self.update_interval)
        
        self.bot_thread = threading.Thread(target=bot_loop, daemon=True)
        self.bot_thread.start()
        
        print("Autonomous trading bot started")
    
    def stop(self):
        """Stop the autonomous trading bot"""
        self.running = False
        self.market_monitor.stop_monitoring()
        
        if self.bot_thread:
            self.bot_thread.join(timeout=10)
        
        print("Autonomous trading bot stopped")
    
    def _execute_trading_cycle(self):
        """Execute one trading cycle"""
        print(f"\n{'='*60}")
        print(f"Trading Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")
        
        account_info = self.trading_agent.get_account_info()
        
        if 'error' in account_info:
            print(f"Error getting account info: {account_info['error']}")
            return
        
        portfolio_value = float(account_info.get('portfolio_value', 0))
        cash = float(account_info.get('cash', 0))
        
        positions = self.trading_agent.get_positions()
        
        self._check_exit_conditions(positions)
        
        self._check_entry_opportunities(portfolio_value, len(positions))
        
        unrealized_pnl = sum(float(pos.get('unrealized_pl', 0)) for pos in positions if 'error' not in pos)
        
        self.logger.log_performance(
            portfolio_value=portfolio_value,
            cash=cash,
            positions_count=len(positions),
            unrealized_pnl=unrealized_pnl,
            realized_pnl=0.0
        )
        
        print(f"Portfolio Value: ${portfolio_value:,.2f}")
        print(f"Cash: ${cash:,.2f}")
        print(f"Positions: {len(positions)}")
        print(f"Unrealized P/L: ${unrealized_pnl:,.2f}")
    
    def _check_exit_conditions(self, positions: List[Dict]):
        """Check if any positions should be exited"""
        for position in positions:
            if 'error' in position:
                continue
            
            symbol = position.get('symbol')
            if not symbol:
                continue
                
            qty = float(position.get('qty', 0))
            entry_price = float(position.get('avg_entry_price', 0))
            current_price = float(position.get('current_price', 0))
            
            if symbol not in self.position_tracker:
                self.position_tracker[symbol] = {
                    'entry_date': datetime.now(),
                    'entry_price': entry_price
                }
            
            position_age = (datetime.now() - self.position_tracker[symbol]['entry_date']).days
            
            exit_decision = self.risk_manager.should_exit_position(
                entry_price=entry_price,
                current_price=current_price,
                position_age_days=position_age
            )
            
            if exit_decision['should_exit']:
                print(f"\n🔴 EXIT SIGNAL: {symbol}")
                print(f"   Reason: {exit_decision['reason']}")
                print(f"   P/L: {exit_decision['pnl_pct']:.2f}%")
                
                result = self.trading_agent.close_position(symbol)
                
                if result.get('success'):
                    print(f"   ✅ Position closed successfully")
                    
                    self.logger.log_trade(
                        symbol=symbol,
                        action='sell',
                        quantity=int(qty),
                        price=current_price,
                        order_id='exit_' + symbol,
                        strategy='risk_management',
                        confidence=1.0,
                        exit_reason=exit_decision['reason'],
                        pnl_pct=exit_decision['pnl_pct']
                    )
                    
                    if symbol in self.position_tracker:
                        del self.position_tracker[symbol]
                else:
                    print(f"   ❌ Failed to close position: {result.get('error')}")
                    self.logger.log_error('exit_position', result.get('error', 'Unknown'), symbol=symbol)
    
    def _check_entry_opportunities(self, portfolio_value: float, current_positions: int):
        """Check for entry opportunities"""
        for symbol in self.watchlist:
            if symbol in self.position_tracker:
                continue
            
            market_data = self.market_monitor.get_cached_data(symbol)
            
            if market_data is None or len(market_data) < 30:
                continue
            
            try:
                sentiment_data = self.sentiment_agent.analyze_sentiment(symbol, symbol)
                sentiment_score = sentiment_data.get('avg_sentiment', 0.0)
            except:
                sentiment_score = 0.0
            
            strategy_result = self.strategy_engine.execute_strategy(
                market_data=market_data,
                symbol=symbol,
                sentiment_score=sentiment_score
            )
            
            signal = strategy_result['signal']
            confidence = strategy_result['confidence']
            
            self.logger.log_decision(
                symbol=symbol,
                signal=signal,
                strategy=strategy_result['strategy'],
                confidence=confidence,
                executed=False,
                reason='evaluating'
            )
            
            if signal == 'BUY':
                should_enter = self.risk_manager.should_enter_position(
                    account_value=portfolio_value,
                    current_positions=current_positions,
                    signal_confidence=confidence
                )
                
                if should_enter:
                    latest_quote = self.market_monitor.get_latest_quote(symbol)
                    
                    if latest_quote is None:
                        continue
                    
                    current_price = latest_quote['mid_price']
                    
                    position_size = self.risk_manager.calculate_position_size(
                        account_value=portfolio_value,
                        current_price=current_price,
                        signal_confidence=confidence
                    )
                    
                    if position_size > 0:
                        print(f"\n🟢 BUY SIGNAL: {symbol}")
                        print(f"   Strategy: {strategy_result['strategy']}")
                        print(f"   Confidence: {confidence:.2%}")
                        print(f"   Price: ${current_price:.2f}")
                        print(f"   Quantity: {position_size} shares")
                        print(f"   Value: ${current_price * position_size:,.2f}")
                        
                        result = self.trading_agent.place_market_order(
                            symbol=symbol,
                            qty=position_size,
                            side='buy'
                        )
                        
                        if result.get('success'):
                            print(f"   ✅ Order placed successfully")
                            
                            self.position_tracker[symbol] = {
                                'entry_date': datetime.now(),
                                'entry_price': current_price
                            }
                            
                            self.logger.log_trade(
                                symbol=symbol,
                                action='buy',
                                quantity=position_size,
                                price=current_price,
                                order_id=result.get('order_id', ''),
                                strategy=strategy_result['strategy'],
                                confidence=confidence
                            )
                            
                            self.logger.log_decision(
                                symbol=symbol,
                                signal=signal,
                                strategy=strategy_result['strategy'],
                                confidence=confidence,
                                executed=True,
                                reason='signal_and_risk_passed'
                            )
                        else:
                            print(f"   ❌ Order failed: {result.get('error')}")
                            self.logger.log_error('place_order', result.get('error', 'Unknown'), symbol=symbol)
    
    def get_status(self) -> Dict:
        """Get current bot status"""
        account_info = self.trading_agent.get_account_info()
        positions = self.trading_agent.get_positions()
        market_summary = self.market_monitor.get_market_summary()
        log_stats = self.logger.get_summary_stats()
        
        return {
            'running': self.running,
            'paper_mode': self.paper_mode,
            'watchlist': self.watchlist,
            'update_interval': self.update_interval,
            'account': account_info,
            'positions_count': len(positions),
            'positions': positions,
            'market_data': market_summary,
            'logs': log_stats,
            'active_strategy': self.strategy_engine.active_strategy.name if self.strategy_engine.active_strategy else None
        }
    
    def get_performance_metrics(self) -> Dict:
        """Get comprehensive performance metrics"""
        trades = self.logger.get_recent_trades(limit=1000)
        
        risk_metrics = self.risk_manager.calculate_risk_metrics(trades)
        
        account_info = self.trading_agent.get_account_info()
        portfolio_value = float(account_info.get('portfolio_value', 0))
        
        drawdown_check = self.risk_manager.check_drawdown(portfolio_value)
        
        return {
            'risk_metrics': risk_metrics,
            'drawdown': drawdown_check,
            'total_trades': len(trades),
            'current_portfolio_value': portfolio_value
        }
