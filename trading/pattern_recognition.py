import pandas as pd
import numpy as np
from typing import List, Dict, Optional

class PatternRecognition:
    """Identify technical analysis patterns in price data"""
    
    @staticmethod
    def detect_double_top(df: pd.DataFrame, tolerance: float = 0.02) -> Optional[Dict]:
        """Detect double top pattern"""
        if len(df) < 50:
            return None
        
        high = df['high'].rolling(window=5, center=True).max()
        
        peaks = []
        for i in range(5, len(df) - 5):
            if high.iloc[i] == df['high'].iloc[i]:
                peaks.append({'index': i, 'price': df['high'].iloc[i]})
        
        for i in range(len(peaks) - 1):
            peak1 = peaks[i]
            for j in range(i + 1, len(peaks)):
                peak2 = peaks[j]
                
                if abs(peak1['price'] - peak2['price']) / peak1['price'] <= tolerance:
                    if peak2['index'] - peak1['index'] >= 10:
                        trough_price = df['low'].iloc[peak1['index']:peak2['index']].min()
                        
                        if trough_price < peak1['price'] * 0.95:
                            return {
                                'pattern': 'double_top',
                                'signal': 'SELL',
                                'confidence': 0.7,
                                'peak1_price': peak1['price'],
                                'peak2_price': peak2['price'],
                                'neckline': trough_price
                            }
        
        return None
    
    @staticmethod
    def detect_double_bottom(df: pd.DataFrame, tolerance: float = 0.02) -> Optional[Dict]:
        """Detect double bottom pattern"""
        if len(df) < 50:
            return None
        
        low = df['low'].rolling(window=5, center=True).min()
        
        troughs = []
        for i in range(5, len(df) - 5):
            if low.iloc[i] == df['low'].iloc[i]:
                troughs.append({'index': i, 'price': df['low'].iloc[i]})
        
        for i in range(len(troughs) - 1):
            trough1 = troughs[i]
            for j in range(i + 1, len(troughs)):
                trough2 = troughs[j]
                
                if abs(trough1['price'] - trough2['price']) / trough1['price'] <= tolerance:
                    if trough2['index'] - trough1['index'] >= 10:
                        peak_price = df['high'].iloc[trough1['index']:trough2['index']].max()
                        
                        if peak_price > trough1['price'] * 1.05:
                            return {
                                'pattern': 'double_bottom',
                                'signal': 'BUY',
                                'confidence': 0.7,
                                'trough1_price': trough1['price'],
                                'trough2_price': trough2['price'],
                                'neckline': peak_price
                            }
        
        return None
    
    @staticmethod
    def detect_head_and_shoulders(df: pd.DataFrame) -> Optional[Dict]:
        """Detect head and shoulders pattern"""
        if len(df) < 60:
            return None
        
        high = df['high'].rolling(window=5, center=True).max()
        
        peaks = []
        for i in range(10, len(df) - 10):
            if high.iloc[i] == df['high'].iloc[i]:
                peaks.append({'index': i, 'price': df['high'].iloc[i]})
        
        for i in range(len(peaks) - 2):
            left_shoulder = peaks[i]
            head = peaks[i + 1]
            right_shoulder = peaks[i + 2]
            
            if (head['price'] > left_shoulder['price'] * 1.05 and
                head['price'] > right_shoulder['price'] * 1.05):
                
                shoulder_diff = abs(left_shoulder['price'] - right_shoulder['price'])
                if shoulder_diff / left_shoulder['price'] < 0.03:
                    
                    trough1 = df['low'].iloc[left_shoulder['index']:head['index']].min()
                    trough2 = df['low'].iloc[head['index']:right_shoulder['index']].min()
                    neckline = (trough1 + trough2) / 2
                    
                    return {
                        'pattern': 'head_and_shoulders',
                        'signal': 'SELL',
                        'confidence': 0.75,
                        'left_shoulder': left_shoulder['price'],
                        'head': head['price'],
                        'right_shoulder': right_shoulder['price'],
                        'neckline': neckline
                    }
        
        return None
    
    @staticmethod
    def detect_triangle(df: pd.DataFrame) -> Optional[Dict]:
        """Detect triangle patterns (ascending, descending, symmetrical)"""
        if len(df) < 30:
            return None
        
        recent_df = df.iloc[-30:]
        
        highs = []
        lows = []
        
        for i in range(5, len(recent_df) - 5):
            if recent_df['high'].iloc[i] == recent_df['high'].iloc[i-5:i+6].max():
                highs.append(recent_df['high'].iloc[i])
            
            if recent_df['low'].iloc[i] == recent_df['low'].iloc[i-5:i+6].min():
                lows.append(recent_df['low'].iloc[i])
        
        if len(highs) >= 2 and len(lows) >= 2:
            high_trend = (highs[-1] - highs[0]) / len(highs)
            low_trend = (lows[-1] - lows[0]) / len(lows)
            
            if high_trend < 0 and abs(low_trend) < abs(high_trend) * 0.3:
                return {
                    'pattern': 'descending_triangle',
                    'signal': 'SELL',
                    'confidence': 0.65
                }
            
            elif low_trend > 0 and abs(high_trend) < abs(low_trend) * 0.3:
                return {
                    'pattern': 'ascending_triangle',
                    'signal': 'BUY',
                    'confidence': 0.65
                }
            
            elif abs(high_trend) < 0.001 and abs(low_trend) < 0.001:
                return {
                    'pattern': 'symmetrical_triangle',
                    'signal': 'WATCH',
                    'confidence': 0.5
                }
        
        return None
    
    @staticmethod
    def detect_flag(df: pd.DataFrame) -> Optional[Dict]:
        """Detect bull/bear flag patterns"""
        if len(df) < 30:
            return None
        
        recent_df = df.iloc[-30:]
        prev_df = df.iloc[-60:-30]
        
        prev_trend = (prev_df['close'].iloc[-1] - prev_df['close'].iloc[0]) / prev_df['close'].iloc[0]
        
        if abs(prev_trend) < 0.1:
            return None
        
        recent_high = recent_df['high'].max()
        recent_low = recent_df['low'].min()
        recent_range = (recent_high - recent_low) / recent_low
        
        if recent_range < 0.05:
            if prev_trend > 0:
                return {
                    'pattern': 'bull_flag',
                    'signal': 'BUY',
                    'confidence': 0.65
                }
            else:
                return {
                    'pattern': 'bear_flag',
                    'signal': 'SELL',
                    'confidence': 0.65
                }
        
        return None
    
    @staticmethod
    def detect_gap(df: pd.DataFrame) -> Optional[Dict]:
        """Detect price gaps"""
        if len(df) < 5:
            return None
        
        for i in range(1, min(5, len(df))):
            prev_close = df['close'].iloc[-(i+1)]
            curr_open = df['open'].iloc[-i]
            
            gap_pct = abs(curr_open - prev_close) / prev_close
            
            if gap_pct > 0.02:
                if curr_open > prev_close:
                    return {
                        'pattern': 'gap_up',
                        'signal': 'BUY',
                        'confidence': 0.6,
                        'gap_size': gap_pct * 100
                    }
                else:
                    return {
                        'pattern': 'gap_down',
                        'signal': 'SELL',
                        'confidence': 0.6,
                        'gap_size': gap_pct * 100
                    }
        
        return None
    
    @staticmethod
    def scan_all_patterns(df: pd.DataFrame) -> List[Dict]:
        """Scan for all known patterns"""
        patterns = []
        
        double_top = PatternRecognition.detect_double_top(df)
        if double_top:
            patterns.append(double_top)
        
        double_bottom = PatternRecognition.detect_double_bottom(df)
        if double_bottom:
            patterns.append(double_bottom)
        
        h_and_s = PatternRecognition.detect_head_and_shoulders(df)
        if h_and_s:
            patterns.append(h_and_s)
        
        triangle = PatternRecognition.detect_triangle(df)
        if triangle:
            patterns.append(triangle)
        
        flag = PatternRecognition.detect_flag(df)
        if flag:
            patterns.append(flag)
        
        gap = PatternRecognition.detect_gap(df)
        if gap:
            patterns.append(gap)
        
        return patterns
