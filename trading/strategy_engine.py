import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

class TradingStrategy(ABC):
    """Base class for all trading strategies"""
    
    def __init__(self, name: str):
        self.name = name
        self.parameters = {}
    
    @abstractmethod
    def generate_signal(self, market_data: pd.DataFrame, symbol: str) -> str:
        """
        Generate trading signal based on market data
        Returns: 'BUY', 'SELL', or 'HOLD'
        """
        pass
    
    @abstractmethod
    def get_confidence(self, market_data: pd.DataFrame, symbol: str) -> float:
        """
        Get confidence score for the signal (0.0 to 1.0)
        """
        pass

class MomentumStrategy(TradingStrategy):
    """Momentum-based trading strategy using RSI and MACD"""
    
    def __init__(self, rsi_period: int = 14, rsi_oversold: int = 30, rsi_overbought: int = 70):
        super().__init__("Momentum Strategy")
        self.rsi_period = rsi_period
        self.rsi_oversold = rsi_oversold
        self.rsi_overbought = rsi_overbought
    
    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate Relative Strength Index"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD indicators"""
        exp1 = prices.ewm(span=fast, adjust=False).mean()
        exp2 = prices.ewm(span=slow, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        histogram = macd - signal_line
        
        return {
            'macd': macd,
            'signal': signal_line,
            'histogram': histogram
        }
    
    def generate_signal(self, market_data: pd.DataFrame, symbol: str) -> str:
        """Generate trading signal based on RSI and MACD"""
        if len(market_data) < 30:
            return 'HOLD'
        
        prices = market_data['close']
        rsi = self.calculate_rsi(prices, self.rsi_period)
        macd_data = self.calculate_macd(prices)
        
        current_rsi = rsi.iloc[-1]
        current_macd = macd_data['macd'].iloc[-1]
        current_signal = macd_data['signal'].iloc[-1]
        prev_macd = macd_data['macd'].iloc[-2]
        prev_signal = macd_data['signal'].iloc[-2]
        
        if current_rsi < self.rsi_oversold and current_macd > current_signal and prev_macd <= prev_signal:
            return 'BUY'
        elif current_rsi > self.rsi_overbought and current_macd < current_signal and prev_macd >= prev_signal:
            return 'SELL'
        else:
            return 'HOLD'
    
    def get_confidence(self, market_data: pd.DataFrame, symbol: str) -> float:
        """Calculate confidence based on indicator strength"""
        if len(market_data) < 30:
            return 0.0
        
        prices = market_data['close']
        rsi = self.calculate_rsi(prices, self.rsi_period)
        current_rsi = rsi.iloc[-1]
        
        if current_rsi < self.rsi_oversold:
            confidence = (self.rsi_oversold - current_rsi) / self.rsi_oversold
        elif current_rsi > self.rsi_overbought:
            confidence = (current_rsi - self.rsi_overbought) / (100 - self.rsi_overbought)
        else:
            confidence = 0.3
        
        return min(confidence, 1.0)

class MeanReversionStrategy(TradingStrategy):
    """Mean reversion strategy using Bollinger Bands"""
    
    def __init__(self, period: int = 20, std_dev: float = 2.0):
        super().__init__("Mean Reversion Strategy")
        self.period = period
        self.std_dev = std_dev
    
    def calculate_bollinger_bands(self, prices: pd.Series) -> Dict:
        """Calculate Bollinger Bands"""
        sma = prices.rolling(window=self.period).mean()
        std = prices.rolling(window=self.period).std()
        
        upper_band = sma + (std * self.std_dev)
        lower_band = sma - (std * self.std_dev)
        
        return {
            'upper': upper_band,
            'middle': sma,
            'lower': lower_band
        }
    
    def generate_signal(self, market_data: pd.DataFrame, symbol: str) -> str:
        """Generate signal based on Bollinger Bands"""
        if len(market_data) < self.period + 5:
            return 'HOLD'
        
        prices = market_data['close']
        bands = self.calculate_bollinger_bands(prices)
        
        current_price = prices.iloc[-1]
        upper_band = bands['upper'].iloc[-1]
        lower_band = bands['lower'].iloc[-1]
        middle_band = bands['middle'].iloc[-1]
        
        if current_price <= lower_band:
            return 'BUY'
        elif current_price >= upper_band:
            return 'SELL'
        else:
            return 'HOLD'
    
    def get_confidence(self, market_data: pd.DataFrame, symbol: str) -> float:
        """Calculate confidence based on distance from bands"""
        if len(market_data) < self.period + 5:
            return 0.0
        
        prices = market_data['close']
        bands = self.calculate_bollinger_bands(prices)
        
        current_price = prices.iloc[-1]
        upper_band = bands['upper'].iloc[-1]
        lower_band = bands['lower'].iloc[-1]
        middle_band = bands['middle'].iloc[-1]
        
        band_width = upper_band - lower_band
        
        if current_price <= lower_band:
            distance = abs(current_price - lower_band)
            confidence = min(distance / (band_width * 0.5), 1.0)
        elif current_price >= upper_band:
            distance = abs(current_price - upper_band)
            confidence = min(distance / (band_width * 0.5), 1.0)
        else:
            confidence = 0.2
        
        return confidence

class SentimentBasedStrategy(TradingStrategy):
    """Trading strategy based on news sentiment analysis"""
    
    def __init__(self, sentiment_threshold: float = 0.1):
        super().__init__("Sentiment-Based Strategy")
        self.sentiment_threshold = sentiment_threshold
    
    def generate_signal(self, market_data: pd.DataFrame, symbol: str, sentiment_score: Optional[float] = None) -> str:
        """Generate signal based on sentiment score"""
        if sentiment_score is None:
            return 'HOLD'
        
        if sentiment_score > self.sentiment_threshold:
            return 'BUY'
        elif sentiment_score < -self.sentiment_threshold:
            return 'SELL'
        else:
            return 'HOLD'
    
    def get_confidence(self, market_data: pd.DataFrame, symbol: str, sentiment_score: Optional[float] = None) -> float:
        """Calculate confidence based on sentiment strength"""
        if sentiment_score is None:
            return 0.0
        
        confidence = min(abs(sentiment_score), 1.0)
        return confidence

class HybridStrategy(TradingStrategy):
    """Hybrid strategy combining multiple strategies"""
    
    def __init__(self, strategies: List[TradingStrategy], weights: Optional[List[float]] = None):
        super().__init__("Hybrid Strategy")
        self.strategies = strategies
        
        if weights is None:
            self.weights = [1.0 / len(strategies)] * len(strategies)
        else:
            self.weights = weights
    
    def generate_signal(self, market_data: pd.DataFrame, symbol: str, **kwargs) -> str:
        """Generate signal by combining multiple strategies"""
        signals = []
        confidences = []
        
        for strategy, weight in zip(self.strategies, self.weights):
            if isinstance(strategy, SentimentBasedStrategy):
                signal = strategy.generate_signal(market_data, symbol, kwargs.get('sentiment_score'))
                confidence = strategy.get_confidence(market_data, symbol, kwargs.get('sentiment_score'))
            else:
                signal = strategy.generate_signal(market_data, symbol)
                confidence = strategy.get_confidence(market_data, symbol)
            
            signals.append(signal)
            confidences.append(confidence * weight)
        
        buy_score = sum(c for s, c in zip(signals, confidences) if s == 'BUY')
        sell_score = sum(c for s, c in zip(signals, confidences) if s == 'SELL')
        
        threshold = 0.3
        
        if buy_score > threshold and buy_score > sell_score:
            return 'BUY'
        elif sell_score > threshold and sell_score > buy_score:
            return 'SELL'
        else:
            return 'HOLD'
    
    def get_confidence(self, market_data: pd.DataFrame, symbol: str, **kwargs) -> float:
        """Calculate overall confidence"""
        confidences = []
        
        for strategy, weight in zip(self.strategies, self.weights):
            if isinstance(strategy, SentimentBasedStrategy):
                confidence = strategy.get_confidence(market_data, symbol, kwargs.get('sentiment_score'))
            else:
                confidence = strategy.get_confidence(market_data, symbol)
            
            confidences.append(confidence * weight)
        
        return sum(confidences) / len(confidences)

class StrategyEngine:
    """Engine for managing and executing trading strategies"""
    
    def __init__(self):
        self.strategies = {}
        self.active_strategy = None
        self._init_default_strategies()
    
    def _init_default_strategies(self):
        """Initialize default strategies"""
        self.add_strategy('momentum', MomentumStrategy())
        self.add_strategy('mean_reversion', MeanReversionStrategy())
        self.add_strategy('sentiment', SentimentBasedStrategy())
        
        hybrid = HybridStrategy([
            MomentumStrategy(),
            MeanReversionStrategy(),
            SentimentBasedStrategy()
        ], weights=[0.4, 0.3, 0.3])
        
        self.add_strategy('hybrid', hybrid)
        self.set_active_strategy('hybrid')
    
    def add_strategy(self, name: str, strategy: TradingStrategy):
        """Add a new strategy"""
        self.strategies[name] = strategy
    
    def set_active_strategy(self, name: str):
        """Set the active strategy"""
        if name in self.strategies:
            self.active_strategy = self.strategies[name]
        else:
            raise ValueError(f"Strategy '{name}' not found")
    
    def execute_strategy(self, market_data: pd.DataFrame, symbol: str, **kwargs) -> Dict:
        """Execute the active strategy"""
        if self.active_strategy is None:
            raise ValueError("No active strategy set")
        
        signal = self.active_strategy.generate_signal(market_data, symbol, **kwargs)
        confidence = self.active_strategy.get_confidence(market_data, symbol, **kwargs)
        
        return {
            'symbol': symbol,
            'strategy': self.active_strategy.name,
            'signal': signal,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_available_strategies(self) -> List[str]:
        """Get list of available strategies"""
        return list(self.strategies.keys())
