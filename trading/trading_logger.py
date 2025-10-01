import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class TradingLogger:
    """Comprehensive logging system for trading bot"""
    
    def __init__(self, log_dir: str = "trading_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.trades_log_file = self.log_dir / "trades.jsonl"
        self.decisions_log_file = self.log_dir / "decisions.jsonl"
        self.errors_log_file = self.log_dir / "errors.jsonl"
        self.performance_log_file = self.log_dir / "performance.jsonl"
    
    def log_trade(
        self,
        symbol: str,
        action: str,
        quantity: int,
        price: float,
        order_id: str,
        strategy: str,
        confidence: float,
        **kwargs
    ):
        """Log a trade execution"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'trade',
            'symbol': symbol,
            'action': action,
            'quantity': quantity,
            'price': price,
            'total_value': quantity * price,
            'order_id': order_id,
            'strategy': strategy,
            'confidence': confidence,
            **kwargs
        }
        
        self._append_to_file(self.trades_log_file, log_entry)
    
    def log_decision(
        self,
        symbol: str,
        signal: str,
        strategy: str,
        confidence: float,
        executed: bool,
        reason: str = "",
        **kwargs
    ):
        """Log a trading decision"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'decision',
            'symbol': symbol,
            'signal': signal,
            'strategy': strategy,
            'confidence': confidence,
            'executed': executed,
            'reason': reason,
            **kwargs
        }
        
        self._append_to_file(self.decisions_log_file, log_entry)
    
    def log_error(
        self,
        error_type: str,
        message: str,
        symbol: Optional[str] = None,
        **kwargs
    ):
        """Log an error"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'error',
            'error_type': error_type,
            'message': message,
            'symbol': symbol,
            **kwargs
        }
        
        self._append_to_file(self.errors_log_file, log_entry)
    
    def log_performance(
        self,
        portfolio_value: float,
        cash: float,
        positions_count: int,
        unrealized_pnl: float,
        realized_pnl: float,
        **kwargs
    ):
        """Log performance metrics"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': 'performance',
            'portfolio_value': portfolio_value,
            'cash': cash,
            'positions_count': positions_count,
            'unrealized_pnl': unrealized_pnl,
            'realized_pnl': realized_pnl,
            **kwargs
        }
        
        self._append_to_file(self.performance_log_file, log_entry)
    
    def _append_to_file(self, file_path: Path, log_entry: Dict):
        """Append log entry to file"""
        try:
            with open(file_path, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            print(f"Error writing to log file {file_path}: {e}")
    
    def get_recent_trades(self, limit: int = 50) -> List[Dict]:
        """Get recent trades from log"""
        return self._read_log_file(self.trades_log_file, limit)
    
    def get_recent_decisions(self, limit: int = 100) -> List[Dict]:
        """Get recent decisions from log"""
        return self._read_log_file(self.decisions_log_file, limit)
    
    def get_recent_errors(self, limit: int = 50) -> List[Dict]:
        """Get recent errors from log"""
        return self._read_log_file(self.errors_log_file, limit)
    
    def get_performance_history(self, limit: int = 100) -> List[Dict]:
        """Get performance history from log"""
        return self._read_log_file(self.performance_log_file, limit)
    
    def _read_log_file(self, file_path: Path, limit: int = 100) -> List[Dict]:
        """Read entries from log file"""
        if not file_path.exists():
            return []
        
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            entries = []
            for line in lines[-limit:]:
                try:
                    entries.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
            
            return entries
        except Exception as e:
            print(f"Error reading log file {file_path}: {e}")
            return []
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics from logs"""
        trades = self.get_recent_trades(limit=1000)
        decisions = self.get_recent_decisions(limit=1000)
        errors = self.get_recent_errors(limit=1000)
        
        total_trades = len(trades)
        buy_trades = len([t for t in trades if t.get('action') == 'buy'])
        sell_trades = len([t for t in trades if t.get('action') == 'sell'])
        
        total_decisions = len(decisions)
        executed_decisions = len([d for d in decisions if d.get('executed')])
        
        return {
            'total_trades': total_trades,
            'buy_trades': buy_trades,
            'sell_trades': sell_trades,
            'total_decisions': total_decisions,
            'executed_decisions': executed_decisions,
            'execution_rate': round((executed_decisions / total_decisions * 100), 2) if total_decisions > 0 else 0,
            'total_errors': len(errors),
            'log_files': {
                'trades': str(self.trades_log_file),
                'decisions': str(self.decisions_log_file),
                'errors': str(self.errors_log_file),
                'performance': str(self.performance_log_file)
            }
        }
    
    def clear_logs(self):
        """Clear all log files"""
        for log_file in [self.trades_log_file, self.decisions_log_file, 
                        self.errors_log_file, self.performance_log_file]:
            if log_file.exists():
                log_file.unlink()
