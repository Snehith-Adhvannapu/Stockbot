import os
from typing import Dict, List, Optional
from datetime import datetime
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

class TradingAgent:
    """Agent responsible for paper trading using Alpaca API"""
    
    def __init__(self):
        self.api_key = os.getenv("ALPACA_API_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET_KEY")
        
        if not self.api_key or not self.secret_key:
            raise ValueError("Alpaca API credentials not found in environment variables")
        
        self.trading_client = TradingClient(
            self.api_key, 
            self.secret_key, 
            paper=True
        )
        
        self.data_client = StockHistoricalDataClient(
            self.api_key,
            self.secret_key
        )
    
    def get_account_info(self) -> Dict:
        """Get current account information"""
        try:
            account = self.trading_client.get_account()
            return {
                'account_number': account.account_number,
                'status': account.status,
                'buying_power': float(account.buying_power),
                'cash': float(account.cash),
                'portfolio_value': float(account.portfolio_value),
                'equity': float(account.equity),
                'last_equity': float(account.last_equity),
                'currency': account.currency,
                'pattern_day_trader': account.pattern_day_trader,
                'trading_blocked': account.trading_blocked,
                'transfers_blocked': account.transfers_blocked,
                'account_blocked': account.account_blocked,
                'created_at': account.created_at.isoformat() if account.created_at else None,
                'daytrade_count': account.daytrade_count,
            }
        except Exception as e:
            return {
                'error': f"Failed to get account info: {str(e)}"
            }
    
    def get_positions(self) -> List[Dict]:
        """Get all current positions"""
        try:
            positions = self.trading_client.get_all_positions()
            return [
                {
                    'symbol': pos.symbol,
                    'qty': float(pos.qty),
                    'avg_entry_price': float(pos.avg_entry_price),
                    'current_price': float(pos.current_price),
                    'market_value': float(pos.market_value),
                    'cost_basis': float(pos.cost_basis),
                    'unrealized_pl': float(pos.unrealized_pl),
                    'unrealized_plpc': float(pos.unrealized_plpc),
                    'side': pos.side,
                    'exchange': pos.exchange,
                }
                for pos in positions
            ]
        except Exception as e:
            return [{'error': f"Failed to get positions: {str(e)}"}]
    
    def get_open_orders(self) -> List[Dict]:
        """Get all open orders"""
        try:
            orders = self.trading_client.get_orders()
            return [
                {
                    'id': str(order.id),
                    'symbol': order.symbol,
                    'qty': float(order.qty) if order.qty else None,
                    'side': order.side.value,
                    'type': order.type.value,
                    'status': order.status.value,
                    'created_at': order.created_at.isoformat() if order.created_at else None,
                    'filled_qty': float(order.filled_qty) if order.filled_qty else 0,
                    'filled_avg_price': float(order.filled_avg_price) if order.filled_avg_price else None,
                }
                for order in orders
            ]
        except Exception as e:
            return [{'error': f"Failed to get orders: {str(e)}"}]
    
    def place_market_order(self, symbol: str, qty: float, side: str) -> Dict:
        """
        Place a market order
        
        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            qty: Number of shares
            side: 'buy' or 'sell'
        """
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL
            
            market_order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.DAY
            )
            
            order = self.trading_client.submit_order(order_data=market_order_data)
            
            return {
                'success': True,
                'order_id': str(order.id),
                'symbol': order.symbol,
                'qty': float(order.qty) if order.qty else None,
                'side': order.side.value,
                'type': order.type.value,
                'status': order.status.value,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'message': f"Market {side} order placed successfully"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to place order: {str(e)}"
            }
    
    def place_limit_order(self, symbol: str, qty: float, side: str, limit_price: float) -> Dict:
        """
        Place a limit order
        
        Args:
            symbol: Stock ticker (e.g., 'AAPL')
            qty: Number of shares
            side: 'buy' or 'sell'
            limit_price: Limit price for the order
        """
        try:
            order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL
            
            limit_order_data = LimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.DAY,
                limit_price=limit_price
            )
            
            order = self.trading_client.submit_order(order_data=limit_order_data)
            
            return {
                'success': True,
                'order_id': str(order.id),
                'symbol': order.symbol,
                'qty': float(order.qty) if order.qty else None,
                'side': order.side.value,
                'type': order.type.value,
                'limit_price': limit_price,
                'status': order.status.value,
                'created_at': order.created_at.isoformat() if order.created_at else None,
                'message': f"Limit {side} order placed successfully"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to place limit order: {str(e)}"
            }
    
    def cancel_order(self, order_id: str) -> Dict:
        """Cancel an open order"""
        try:
            self.trading_client.cancel_order_by_id(order_id)
            return {
                'success': True,
                'message': f"Order {order_id} cancelled successfully"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to cancel order: {str(e)}"
            }
    
    def cancel_all_orders(self) -> Dict:
        """Cancel all open orders"""
        try:
            cancelled = self.trading_client.cancel_orders()
            return {
                'success': True,
                'cancelled_count': len(cancelled),
                'message': f"Cancelled {len(cancelled)} orders"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to cancel orders: {str(e)}"
            }
    
    def close_position(self, symbol: str) -> Dict:
        """Close a specific position"""
        try:
            self.trading_client.close_position(symbol)
            return {
                'success': True,
                'message': f"Position {symbol} closed successfully"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to close position: {str(e)}"
            }
    
    def close_all_positions(self) -> Dict:
        """Close all positions"""
        try:
            closed = self.trading_client.close_all_positions(cancel_orders=True)
            return {
                'success': True,
                'closed_count': len(closed),
                'message': f"Closed {len(closed)} positions"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to close all positions: {str(e)}"
            }
    
    def get_latest_quote(self, symbol: str) -> Dict:
        """Get latest quote for a symbol"""
        try:
            request_params = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quotes = self.data_client.get_stock_latest_quote(request_params)
            
            if symbol in quotes:
                quote = quotes[symbol]
                return {
                    'symbol': symbol,
                    'ask_price': float(quote.ask_price),
                    'ask_size': float(quote.ask_size),
                    'bid_price': float(quote.bid_price),
                    'bid_size': float(quote.bid_size),
                    'timestamp': quote.timestamp.isoformat() if quote.timestamp else None,
                }
            else:
                return {'error': f"No quote data found for {symbol}"}
        except Exception as e:
            return {'error': f"Failed to get quote: {str(e)}"}
    
    def execute_trade_from_recommendation(self, ticker: str, recommendation: str, qty: float = 1) -> Dict:
        """
        Execute a trade based on AI recommendation
        
        Args:
            ticker: Stock ticker symbol
            recommendation: 'BUY', 'SELL', or 'HOLD'
            qty: Number of shares to trade
        """
        if recommendation == 'HOLD':
            return {
                'success': True,
                'action': 'no_trade',
                'message': f"Recommendation is HOLD for {ticker}, no trade executed"
            }
        
        if recommendation == 'BUY':
            return self.place_market_order(ticker, qty, 'buy')
        elif recommendation == 'SELL':
            positions = self.get_positions()
            has_position = any(pos.get('symbol') == ticker for pos in positions)
            
            if has_position:
                return self.close_position(ticker)
            else:
                return {
                    'success': False,
                    'message': f"Cannot sell {ticker}: no position held"
                }
        else:
            return {
                'success': False,
                'error': f"Invalid recommendation: {recommendation}"
            }
