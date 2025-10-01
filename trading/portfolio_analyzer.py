import pandas as pd
import numpy as np
from typing import Dict, List
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class PortfolioAnalyzer:
    """Analyze portfolio performance and composition"""
    
    def __init__(self):
        pass
    
    def analyze_portfolio(self, positions: List[Dict], account_info: Dict) -> Dict:
        """Comprehensive portfolio analysis"""
        if not positions or any('error' in p for p in positions):
            return {
                'total_value': float(account_info.get('portfolio_value', 0)),
                'cash': float(account_info.get('cash', 0)),
                'positions_value': 0,
                'num_positions': 0,
                'diversification_score': 0
            }
        
        total_positions_value = sum(float(p.get('market_value', 0)) for p in positions)
        total_value = float(account_info.get('portfolio_value', 0))
        
        sector_allocation = self._calculate_sector_allocation(positions)
        concentration_risk = self._calculate_concentration_risk(positions, total_positions_value)
        performance_metrics = self._calculate_performance_metrics(positions)
        
        return {
            'total_value': total_value,
            'cash': float(account_info.get('cash', 0)),
            'positions_value': total_positions_value,
            'num_positions': len(positions),
            'sector_allocation': sector_allocation,
            'concentration_risk': concentration_risk,
            'performance_metrics': performance_metrics,
            'diversification_score': self._calculate_diversification_score(positions)
        }
    
    def _calculate_sector_allocation(self, positions: List[Dict]) -> Dict:
        """Calculate portfolio allocation by sector"""
        sector_map = {
            'AAPL': 'Technology', 'MSFT': 'Technology', 'GOOGL': 'Technology',
            'TSLA': 'Automotive', 'AMZN': 'E-commerce', 'META': 'Technology',
            'NVDA': 'Technology', 'JPM': 'Finance', 'BAC': 'Finance'
        }
        
        total_value = sum(float(p.get('market_value', 0)) for p in positions)
        
        sector_values = {}
        for pos in positions:
            symbol = pos.get('symbol')
            sector = sector_map.get(symbol, 'Other')
            value = float(pos.get('market_value', 0))
            
            if sector in sector_values:
                sector_values[sector] += value
            else:
                sector_values[sector] = value
        
        sector_percentages = {
            sector: (value / total_value * 100) if total_value > 0 else 0
            for sector, value in sector_values.items()
        }
        
        return sector_percentages
    
    def _calculate_concentration_risk(self, positions: List[Dict], total_value: float) -> Dict:
        """Calculate portfolio concentration risk"""
        if total_value == 0:
            return {'herfindahl_index': 0, 'top_3_concentration': 0}
        
        weights = [float(p.get('market_value', 0)) / total_value for p in positions]
        
        herfindahl_index = sum(w ** 2 for w in weights)
        
        sorted_weights = sorted(weights, reverse=True)
        top_3_concentration = sum(sorted_weights[:3]) * 100 if len(sorted_weights) >= 3 else sum(sorted_weights) * 100
        
        return {
            'herfindahl_index': herfindahl_index,
            'top_3_concentration': top_3_concentration
        }
    
    def _calculate_performance_metrics(self, positions: List[Dict]) -> Dict:
        """Calculate performance metrics for positions"""
        total_unrealized_pl = sum(float(p.get('unrealized_pl', 0)) for p in positions)
        total_cost_basis = sum(float(p.get('cost_basis', 0)) for p in positions)
        
        avg_return = (total_unrealized_pl / total_cost_basis * 100) if total_cost_basis > 0 else 0
        
        winners = [p for p in positions if float(p.get('unrealized_pl', 0)) > 0]
        losers = [p for p in positions if float(p.get('unrealized_pl', 0)) < 0]
        
        return {
            'total_unrealized_pl': total_unrealized_pl,
            'avg_return_pct': avg_return,
            'num_winners': len(winners),
            'num_losers': len(losers),
            'win_rate': (len(winners) / len(positions) * 100) if positions else 0
        }
    
    def _calculate_diversification_score(self, positions: List[Dict]) -> float:
        """Calculate diversification score (0-100)"""
        if not positions:
            return 0
        
        num_positions = len(positions)
        
        total_value = sum(float(p.get('market_value', 0)) for p in positions)
        weights = [float(p.get('market_value', 0)) / total_value for p in positions if total_value > 0]
        
        if not weights:
            return 0
        
        herfindahl = sum(w ** 2 for w in weights)
        
        num_score = min(num_positions / 20 * 50, 50)
        
        concentration_score = (1 - herfindahl) * 50
        
        diversification_score = num_score + concentration_score
        
        return min(diversification_score, 100)
    
    def create_allocation_chart(self, positions: List[Dict]) -> go.Figure:
        """Create portfolio allocation pie chart"""
        if not positions:
            return None
        
        symbols = [p.get('symbol') for p in positions]
        values = [float(p.get('market_value', 0)) for p in positions]
        
        fig = go.Figure(data=[go.Pie(
            labels=symbols,
            values=values,
            hole=0.4,
            marker=dict(
                colors=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336', 
                       '#00BCD4', '#FFEB3B', '#795548', '#607D8B', '#E91E63']
            )
        )])
        
        fig.update_layout(
            title='Portfolio Allocation',
            height=400,
            showlegend=True
        )
        
        return fig
    
    def create_performance_chart(self, positions: List[Dict]) -> go.Figure:
        """Create performance comparison chart"""
        if not positions:
            return None
        
        symbols = [p.get('symbol') for p in positions]
        returns = [float(p.get('unrealized_plpc', 0)) * 100 for p in positions]
        
        colors = ['#4CAF50' if r > 0 else '#F44336' for r in returns]
        
        fig = go.Figure(data=[go.Bar(
            x=symbols,
            y=returns,
            marker_color=colors,
            text=[f"{r:.1f}%" for r in returns],
            textposition='auto'
        )])
        
        fig.update_layout(
            title='Position Performance (%)',
            xaxis_title='Symbol',
            yaxis_title='Return (%)',
            height=400,
            showlegend=False
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray")
        
        return fig
