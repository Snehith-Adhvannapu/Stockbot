import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import pytz

class YFinanceDataProvider:
    """Market data provider using yfinance for free historical and real-time data"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = 60
    
    def get_historical_bars(self, symbol, timeframe='1Day', days_back=30):
        """
        Get historical OHLCV data
        
        Returns DataFrame with columns: timestamp, open, high, low, close, volume
        """
        try:
            interval_map = {
                '1Min': '1m',
                '5Min': '5m',
                '15Min': '15m',
                '1Hour': '1h',
                '1Day': '1d'
            }
            
            period_map = {
                '1Min': min(days_back, 7),
                '5Min': min(days_back, 60),
                '15Min': min(days_back, 60),
                '1Hour': min(days_back, 730),
                '1Day': days_back
            }
            
            interval = interval_map.get(timeframe, '1d')
            actual_days = period_map.get(timeframe, days_back)
            
            ticker = yf.Ticker(symbol)
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=actual_days)
            
            df = ticker.history(
                start=start_date,
                end=end_date,
                interval=interval,
                auto_adjust=False
            )
            
            if df.empty:
                return pd.DataFrame()
            
            df = df.reset_index()
            
            if 'Date' in df.columns:
                df['timestamp'] = pd.to_datetime(df['Date'])
            elif 'Datetime' in df.columns:
                df['timestamp'] = pd.to_datetime(df['Datetime'])
            else:
                df['timestamp'] = df.index
            
            df['open'] = df['Open']
            df['high'] = df['High']
            df['low'] = df['Low']
            df['close'] = df['Close']
            df['volume'] = df['Volume']
            
            df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
            
            df = df.dropna()
            
            return df
        
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_latest_quote(self, symbol):
        """
        Get latest quote for a symbol
        
        Returns dict with: symbol, price, change, change_percent
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            prev_close = info.get('previousClose', current_price)
            
            change = current_price - prev_close
            change_pct = (change / prev_close * 100) if prev_close > 0 else 0
            
            return {
                'symbol': symbol,
                'price': current_price,
                'change': change,
                'change_percent': change_pct,
                'volume': info.get('volume', 0),
                'bid': info.get('bid', current_price),
                'ask': info.get('ask', current_price)
            }
        
        except Exception as e:
            print(f"Error fetching quote for {symbol}: {e}")
            return {
                'symbol': symbol,
                'price': 0,
                'change': 0,
                'change_percent': 0,
                'volume': 0
            }
    
    def get_batch_quotes(self, symbols):
        """Get latest quotes for multiple symbols"""
        quotes = []
        
        for symbol in symbols:
            quote = self.get_latest_quote(symbol)
            quotes.append(quote)
        
        return quotes
    
    def get_stock_info(self, symbol):
        """Get detailed stock information"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 0),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow', 0)
            }
        
        except Exception as e:
            print(f"Error fetching info for {symbol}: {e}")
            return {'symbol': symbol, 'name': symbol}
