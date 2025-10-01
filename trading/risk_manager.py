import numpy as np
from typing import Dict, Optional
from datetime import datetime

class RiskManager:
    """Risk management system for trading bot"""
    
    def __init__(
        self,
        max_position_size: float = 0.1,
        max_portfolio_risk: float = 0.02,
        stop_loss_pct: float = 0.05,
        take_profit_pct: float = 0.10,
        max_drawdown_pct: float = 0.15,
        max_positions: int = 10
    ):
        self.max_position_size = max_position_size
        self.max_portfolio_risk = max_portfolio_risk
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.max_drawdown_pct = max_drawdown_pct
        self.max_positions = max_positions
        
        self.initial_capital = None
        self.peak_value = None
    
    def set_initial_capital(self, capital: float):
        """Set initial capital"""
        self.initial_capital = capital
        self.peak_value = capital
    
    def calculate_position_size(
        self,
        account_value: float,
        current_price: float,
        signal_confidence: float
    ) -> int:
        """
        Calculate appropriate position size based on risk parameters
        
        Args:
            account_value: Current account value
            current_price: Current stock price
            signal_confidence: Confidence score (0.0 to 1.0)
        
        Returns:
            Number of shares to buy
        """
        max_dollar_amount = account_value * self.max_position_size
        
        confidence_adjusted_amount = max_dollar_amount * signal_confidence
        
        shares = int(confidence_adjusted_amount / current_price)
        
        return max(shares, 1)
    
    def should_enter_position(
        self,
        account_value: float,
        current_positions: int,
        signal_confidence: float
    ) -> bool:
        """
        Determine if we should enter a new position
        
        Args:
            account_value: Current account value
            current_positions: Number of current positions
            signal_confidence: Signal confidence score
        
        Returns:
            True if position should be entered
        """
        if current_positions >= self.max_positions:
            return False
        
        if signal_confidence < 0.5:
            return False
        
        if self.initial_capital and account_value < self.initial_capital * (1 - self.max_drawdown_pct):
            return False
        
        return True
    
    def should_exit_position(
        self,
        entry_price: float,
        current_price: float,
        position_age_days: int
    ) -> Dict:
        """
        Determine if we should exit a position
        
        Args:
            entry_price: Price at which position was entered
            current_price: Current market price
            position_age_days: How many days position has been held
        
        Returns:
            Dictionary with exit decision and reason
        """
        price_change = (current_price - entry_price) / entry_price
        
        if price_change <= -self.stop_loss_pct:
            return {
                'should_exit': True,
                'reason': 'stop_loss',
                'pnl_pct': price_change * 100
            }
        
        if price_change >= self.take_profit_pct:
            return {
                'should_exit': True,
                'reason': 'take_profit',
                'pnl_pct': price_change * 100
            }
        
        if position_age_days > 30:
            return {
                'should_exit': True,
                'reason': 'max_hold_period',
                'pnl_pct': price_change * 100
            }
        
        return {
            'should_exit': False,
            'reason': 'hold',
            'pnl_pct': price_change * 100
        }
    
    def check_drawdown(self, current_value: float) -> Dict:
        """
        Check if maximum drawdown has been exceeded
        
        Args:
            current_value: Current portfolio value
        
        Returns:
            Dictionary with drawdown status
        """
        if self.initial_capital is None:
            return {
                'exceeded': False,
                'current_drawdown': 0.0,
                'max_drawdown': self.max_drawdown_pct
            }
        
        if current_value > self.peak_value:
            self.peak_value = current_value
        
        drawdown = (self.peak_value - current_value) / self.peak_value
        
        return {
            'exceeded': drawdown > self.max_drawdown_pct,
            'current_drawdown': drawdown * 100,
            'max_drawdown': self.max_drawdown_pct * 100,
            'peak_value': self.peak_value,
            'current_value': current_value
        }
    
    def calculate_risk_metrics(self, trades_history: list) -> Dict:
        """
        Calculate risk metrics from trade history
        
        Args:
            trades_history: List of completed trades
        
        Returns:
            Dictionary with risk metrics
        """
        if not trades_history:
            return {
                'sharpe_ratio': 0.0,
                'win_rate': 0.0,
                'avg_win': 0.0,
                'avg_loss': 0.0,
                'profit_factor': 0.0,
                'max_consecutive_losses': 0
            }
        
        pnl_values = [trade.get('pnl', 0) for trade in trades_history]
        
        wins = [pnl for pnl in pnl_values if pnl > 0]
        losses = [pnl for pnl in pnl_values if pnl < 0]
        
        win_rate = len(wins) / len(pnl_values) if pnl_values else 0.0
        avg_win = np.mean(wins) if wins else 0.0
        avg_loss = abs(np.mean(losses)) if losses else 0.0
        
        total_wins = sum(wins)
        total_losses = abs(sum(losses))
        profit_factor = total_wins / total_losses if total_losses > 0 else 0.0
        
        max_consecutive_losses = 0
        current_consecutive = 0
        for pnl in pnl_values:
            if pnl < 0:
                current_consecutive += 1
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive)
            else:
                current_consecutive = 0
        
        if len(pnl_values) > 1:
            returns = np.array(pnl_values)
            sharpe_ratio = (np.mean(returns) / np.std(returns)) * np.sqrt(252) if np.std(returns) > 0 else 0.0
        else:
            sharpe_ratio = 0.0
        
        return {
            'sharpe_ratio': round(sharpe_ratio, 2),
            'win_rate': round(win_rate * 100, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'max_consecutive_losses': max_consecutive_losses,
            'total_trades': len(pnl_values),
            'winning_trades': len(wins),
            'losing_trades': len(losses)
        }
    
    def get_risk_summary(self) -> Dict:
        """Get current risk management parameters"""
        return {
            'max_position_size': f"{self.max_position_size * 100}%",
            'max_portfolio_risk': f"{self.max_portfolio_risk * 100}%",
            'stop_loss': f"{self.stop_loss_pct * 100}%",
            'take_profit': f"{self.take_profit_pct * 100}%",
            'max_drawdown': f"{self.max_drawdown_pct * 100}%",
            'max_positions': self.max_positions
        }
