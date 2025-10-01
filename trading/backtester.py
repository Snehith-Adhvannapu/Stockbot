import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from trading.strategy_engine import TradingStrategy, StrategyEngine
from trading.risk_manager import RiskManager

class Backtester:
    """Backtest trading strategies on historical data"""
    
    def __init__(
        self,
        initial_capital: float = 100000,
        commission: float = 0.001
    ):
        self.initial_capital = initial_capital
        self.commission = commission
        self.results = None
    
    def run_backtest(
        self,
        strategy: TradingStrategy,
        market_data: Dict[str, pd.DataFrame],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        risk_manager: Optional[RiskManager] = None
    ) -> Dict:
        """
        Run backtest on historical data
        
        Args:
            strategy: Trading strategy to backtest
            market_data: Dictionary of symbol -> DataFrame with OHLCV data
            start_date: Backtest start date
            end_date: Backtest end date
            risk_manager: Optional risk manager for position sizing
        
        Returns:
            Dictionary with backtest results
        """
        if risk_manager is None:
            risk_manager = RiskManager()
        
        risk_manager.set_initial_capital(self.initial_capital)
        
        portfolio = {
            'cash': self.initial_capital,
            'positions': {},
            'history': [],
            'trades': []
        }
        
        all_dates = set()
        for symbol, df in market_data.items():
            if 'timestamp' in df.columns:
                all_dates.update(df['timestamp'].tolist())
        
        sorted_dates = sorted(list(all_dates))
        
        if start_date:
            sorted_dates = [d for d in sorted_dates if d >= start_date]
        if end_date:
            sorted_dates = [d for d in sorted_dates if d <= end_date]
        
        for current_date in sorted_dates:
            self._process_day(
                current_date=current_date,
                strategy=strategy,
                market_data=market_data,
                portfolio=portfolio,
                risk_manager=risk_manager
            )
        
        final_portfolio_value = self._calculate_portfolio_value(
            portfolio, market_data, sorted_dates[-1]
        )
        
        total_return = (final_portfolio_value - self.initial_capital) / self.initial_capital
        
        self.results = self._calculate_metrics(
            portfolio=portfolio,
            final_value=final_portfolio_value,
            total_return=total_return
        )
        
        return self.results
    
    def _process_day(
        self,
        current_date: datetime,
        strategy: TradingStrategy,
        market_data: Dict[str, pd.DataFrame],
        portfolio: Dict,
        risk_manager: RiskManager
    ):
        """Process one day of trading"""
        current_positions = len(portfolio['positions'])
        portfolio_value = self._calculate_portfolio_value(
            portfolio, market_data, current_date
        )
        
        for symbol, df in market_data.items():
            df_subset = df[df['timestamp'] <= current_date].copy()
            
            if len(df_subset) < 30:
                continue
            
            try:
                signal = strategy.generate_signal(df_subset, symbol)
                confidence = strategy.get_confidence(df_subset, symbol)
            except:
                continue
            
            current_price = df_subset['close'].iloc[-1]
            
            if signal == 'BUY' and symbol not in portfolio['positions']:
                should_enter = risk_manager.should_enter_position(
                    account_value=portfolio_value,
                    current_positions=current_positions,
                    signal_confidence=confidence
                )
                
                if should_enter:
                    position_size = risk_manager.calculate_position_size(
                        account_value=portfolio_value,
                        current_price=current_price,
                        signal_confidence=confidence
                    )
                    
                    cost = position_size * current_price * (1 + self.commission)
                    
                    if cost <= portfolio['cash']:
                        portfolio['cash'] -= cost
                        portfolio['positions'][symbol] = {
                            'shares': position_size,
                            'entry_price': current_price,
                            'entry_date': current_date
                        }
                        
                        portfolio['trades'].append({
                            'date': current_date,
                            'symbol': symbol,
                            'action': 'BUY',
                            'shares': position_size,
                            'price': current_price,
                            'cost': cost,
                            'confidence': confidence
                        })
                        
                        current_positions += 1
            
            elif signal == 'SELL' and symbol in portfolio['positions']:
                position = portfolio['positions'][symbol]
                shares = position['shares']
                entry_price = position['entry_price']
                entry_date = position['entry_date']
                
                days_held = (current_date - entry_date).days
                
                exit_decision = risk_manager.should_exit_position(
                    entry_price=entry_price,
                    current_price=current_price,
                    position_age_days=days_held
                )
                
                if exit_decision['should_exit'] or signal == 'SELL':
                    revenue = shares * current_price * (1 - self.commission)
                    portfolio['cash'] += revenue
                    
                    pnl = revenue - (shares * entry_price * (1 + self.commission))
                    
                    portfolio['trades'].append({
                        'date': current_date,
                        'symbol': symbol,
                        'action': 'SELL',
                        'shares': shares,
                        'price': current_price,
                        'revenue': revenue,
                        'pnl': pnl,
                        'pnl_pct': (pnl / (shares * entry_price)) * 100,
                        'days_held': days_held,
                        'reason': exit_decision.get('reason', 'signal')
                    })
                    
                    del portfolio['positions'][symbol]
                    current_positions -= 1
        
        portfolio_value = self._calculate_portfolio_value(
            portfolio, market_data, current_date
        )
        
        portfolio['history'].append({
            'date': current_date,
            'cash': portfolio['cash'],
            'positions_value': portfolio_value - portfolio['cash'],
            'total_value': portfolio_value,
            'num_positions': len(portfolio['positions'])
        })
    
    def _calculate_portfolio_value(
        self,
        portfolio: Dict,
        market_data: Dict[str, pd.DataFrame],
        current_date: datetime
    ) -> float:
        """Calculate total portfolio value"""
        total_value = portfolio['cash']
        
        for symbol, position in portfolio['positions'].items():
            if symbol in market_data:
                df_subset = market_data[symbol][market_data[symbol]['timestamp'] <= current_date]
                
                if len(df_subset) > 0:
                    current_price = df_subset['close'].iloc[-1]
                    position_value = position['shares'] * current_price
                    total_value += position_value
        
        return total_value
    
    def _calculate_metrics(
        self,
        portfolio: Dict,
        final_value: float,
        total_return: float
    ) -> Dict:
        """Calculate comprehensive backtest metrics"""
        trades = portfolio['trades']
        history = portfolio['history']
        
        completed_trades = [t for t in trades if t['action'] == 'SELL']
        
        if not completed_trades:
            return {
                'initial_capital': self.initial_capital,
                'final_value': final_value,
                'total_return': total_return * 100,
                'total_trades': len(trades),
                'completed_trades': 0,
                'win_rate': 0,
                'message': 'No completed trades'
            }
        
        wins = [t for t in completed_trades if t['pnl'] > 0]
        losses = [t for t in completed_trades if t['pnl'] <= 0]
        
        win_rate = len(wins) / len(completed_trades) if completed_trades else 0
        avg_win = np.mean([t['pnl'] for t in wins]) if wins else 0
        avg_loss = np.mean([t['pnl'] for t in losses]) if losses else 0
        
        total_wins = sum([t['pnl'] for t in wins])
        total_losses = abs(sum([t['pnl'] for t in losses]))
        profit_factor = total_wins / total_losses if total_losses > 0 else 0
        
        daily_returns = []
        for i in range(1, len(history)):
            prev_value = history[i-1]['total_value']
            curr_value = history[i]['total_value']
            daily_return = (curr_value - prev_value) / prev_value
            daily_returns.append(daily_return)
        
        if daily_returns:
            sharpe_ratio = (np.mean(daily_returns) / np.std(daily_returns)) * np.sqrt(252) if np.std(daily_returns) > 0 else 0
        else:
            sharpe_ratio = 0
        
        peak = self.initial_capital
        max_drawdown = 0
        
        for record in history:
            value = record['total_value']
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        return {
            'initial_capital': self.initial_capital,
            'final_value': final_value,
            'total_return': total_return * 100,
            'total_trades': len(trades),
            'completed_trades': len(completed_trades),
            'winning_trades': len(wins),
            'losing_trades': len(losses),
            'win_rate': win_rate * 100,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': profit_factor,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown * 100,
            'avg_days_held': np.mean([t['days_held'] for t in completed_trades]) if completed_trades else 0,
            'trade_details': completed_trades,
            'equity_curve': history
        }
    
    def plot_results(self) -> go.Figure:
        """Create visualization of backtest results"""
        if not self.results:
            return None
        
        history = self.results['equity_curve']
        
        dates = [h['date'] for h in history]
        values = [h['total_value'] for h in history]
        
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.7, 0.3],
            subplot_titles=('Portfolio Value Over Time', 'Number of Positions'),
            vertical_spacing=0.1
        )
        
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=values,
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#4CAF50', width=2),
                fill='tozeroy',
                fillcolor='rgba(76, 175, 80, 0.1)'
            ),
            row=1, col=1
        )
        
        fig.add_hline(
            y=self.initial_capital,
            line_dash="dash",
            line_color="gray",
            annotation_text="Initial Capital",
            row=1, col=1
        )
        
        num_positions = [h['num_positions'] for h in history]
        
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=num_positions,
                mode='lines',
                name='Positions',
                line=dict(color='#2196F3', width=2),
                fill='tozeroy',
                fillcolor='rgba(33, 150, 243, 0.1)'
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            title='Backtest Results',
            showlegend=True,
            height=700,
            hovermode='x unified'
        )
        
        fig.update_xaxes(title_text="Date", row=2, col=1)
        fig.update_yaxes(title_text="Value ($)", row=1, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        
        return fig
    
    def get_summary_report(self) -> str:
        """Generate text summary of backtest results"""
        if not self.results:
            return "No backtest results available"
        
        r = self.results
        
        report = f"""
        BACKTEST SUMMARY
        ================
        
        Performance:
        - Initial Capital: ${r['initial_capital']:,.2f}
        - Final Value: ${r['final_value']:,.2f}
        - Total Return: {r['total_return']:.2f}%
        - Sharpe Ratio: {r['sharpe_ratio']:.2f}
        - Max Drawdown: {r['max_drawdown']:.2f}%
        
        Trading Activity:
        - Total Trades: {r['total_trades']}
        - Completed Trades: {r['completed_trades']}
        - Winning Trades: {r['winning_trades']}
        - Losing Trades: {r['losing_trades']}
        - Win Rate: {r['win_rate']:.1f}%
        
        Trade Economics:
        - Average Win: ${r['avg_win']:,.2f}
        - Average Loss: ${r['avg_loss']:,.2f}
        - Profit Factor: {r['profit_factor']:.2f}
        - Avg Days Held: {r['avg_days_held']:.1f}
        """
        
        return report
