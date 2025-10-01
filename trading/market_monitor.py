import os
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading

from trading.data_provider import YFinanceDataProvider

class MarketDataMonitor:
    """Monitor live market data using YFinance for historical data and Alpaca for trading"""
    
    def __init__(self):
        self.data_provider = YFinanceDataProvider()
        
        self.watchlist = []
        self.market_data_cache = {}
        self.last_update = {}
        self.monitoring = False
        self.monitor_thread = None
    
    def add_to_watchlist(self, symbols: List[str]):
        """Add symbols to watchlist"""
        for symbol in symbols:
            if symbol not in self.watchlist:
                self.watchlist.append(symbol)
    
    def remove_from_watchlist(self, symbols: List[str]):
        """Remove symbols from watchlist"""
        for symbol in symbols:
            if symbol in self.watchlist:
                self.watchlist.remove(symbol)
    
    def get_watchlist(self) -> List[str]:
        """Get current watchlist"""
        return self.watchlist.copy()
    
    def get_historical_bars(
        self,
        symbol: str,
        timeframe: str = '1Hour',
        days_back: int = 30
    ) -> pd.DataFrame:
        """
        Get historical bar data for a symbol using YFinance
        
        Args:
            symbol: Stock ticker
            timeframe: Bar timeframe ('1Min', '5Min', '1Hour', '1Day')
            days_back: Number of days to look back
        
        Returns:
            DataFrame with columns: timestamp, open, high, low, close, volume
        """
        return self.data_provider.get_historical_bars(symbol, timeframe, days_back)
    
    def get_latest_quote(self, symbol: str) -> Optional[Dict]:
        """Get latest quote for a symbol using YFinance"""
        quote = self.data_provider.get_latest_quote(symbol)
        
        if quote and quote.get('price', 0) > 0:
            return {
                'symbol': symbol,
                'ask_price': quote['ask'],
                'bid_price': quote['bid'],
                'mid_price': quote['price'],
                'timestamp': datetime.now()
            }
        
        return None
    
    def get_batch_quotes(self, symbols: List[str]) -> List[Dict]:
        """Get latest quotes for multiple symbols"""
        return self.data_provider.get_batch_quotes(symbols)
    
    def update_market_data(self):
        """Update market data for all symbols in watchlist"""
        for symbol in self.watchlist:
            try:
                df = self.get_historical_bars(symbol, timeframe='1Hour', days_back=60)
                
                if not df.empty:
                    self.market_data_cache[symbol] = df
                    self.last_update[symbol] = datetime.now()
                
            except Exception as e:
                print(f"Error updating data for {symbol}: {e}")
    
    def get_cached_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get cached market data for a symbol"""
        return self.market_data_cache.get(symbol)
    
    def start_monitoring(self, update_interval: int = 60):
        """
        Start monitoring market data in background
        
        Args:
            update_interval: Update interval in seconds
        """
        if self.monitoring:
            print("Already monitoring market data")
            return
        
        self.monitoring = True
        
        def monitor_loop():
            while self.monitoring:
                try:
                    self.update_market_data()
                    time.sleep(update_interval)
                except Exception as e:
                    print(f"Error in monitoring loop: {e}")
                    time.sleep(update_interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"Started monitoring {len(self.watchlist)} symbols")
    
    def stop_monitoring(self):
        """Stop monitoring market data"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        print("Stopped monitoring market data")
    
    def get_market_summary(self) -> Dict:
        """Get summary of current market data"""
        summary = {
            'watchlist_size': len(self.watchlist),
            'cached_symbols': len(self.market_data_cache),
            'monitoring_active': self.monitoring,
            'last_updates': {}
        }
        
        for symbol, update_time in self.last_update.items():
            time_diff = datetime.now() - update_time
            summary['last_updates'][symbol] = {
                'timestamp': update_time.isoformat(),
                'age_seconds': int(time_diff.total_seconds())
            }
        
        return summary
    
    def calculate_volatility(self, symbol: str, period: int = 20) -> Optional[float]:
        """Calculate historical volatility for a symbol"""
        df = self.get_cached_data(symbol)
        
        if df is None or len(df) < period:
            return None
        
        returns = df['close'].pct_change().dropna()
        volatility = returns.rolling(window=period).std().iloc[-1]
        
        annualized_volatility = volatility * (252 ** 0.5) * 100
        
        return round(annualized_volatility, 2)
    
    def get_price_change(self, symbol: str, period: int = 1) -> Optional[Dict]:
        """Get price change over specified period"""
        df = self.get_cached_data(symbol)
        
        if df is None or len(df) < period + 1:
            return None
        
        current_price = df['close'].iloc[-1]
        previous_price = df['close'].iloc[-(period + 1)]
        
        change = current_price - previous_price
        change_pct = (change / previous_price) * 100
        
        return {
            'symbol': symbol,
            'current_price': round(current_price, 2),
            'previous_price': round(previous_price, 2),
            'change': round(change, 2),
            'change_pct': round(change_pct, 2),
            'period': period
        }
