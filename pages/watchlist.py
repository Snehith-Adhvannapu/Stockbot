import streamlit as st
import pandas as pd
from datetime import datetime
import time

from trading.market_monitor import MarketDataMonitor
from trading.technical_indicators import TechnicalIndicators

def show():
    st.title("👀 Stock Watchlist")
    st.markdown("Track your favorite stocks in real-time")
    
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Your Watchlist")
    
    with col2:
        if st.button("🔄 Refresh Prices", use_container_width=True):
            st.rerun()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_symbol = st.text_input(
            "Add a stock:",
            placeholder="Enter symbol (e.g., AAPL)",
            max_chars=10
        ).upper()
        
        if st.button("➕ Add to Watchlist", use_container_width=True):
            if new_symbol and new_symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_symbol)
                st.success(f"Added {new_symbol}")
                time.sleep(0.5)
                st.rerun()
            elif new_symbol in st.session_state.watchlist:
                st.warning(f"{new_symbol} is already in your watchlist")
    
    with col2:
        if st.button("🗑️ Clear Watchlist", use_container_width=True):
            if st.session_state.get('confirm_clear'):
                st.session_state.watchlist = []
                st.session_state.confirm_clear = False
                st.success("Watchlist cleared")
                time.sleep(0.5)
                st.rerun()
            else:
                st.session_state.confirm_clear = True
                st.warning("Click again to confirm")
    
    if not st.session_state.watchlist:
        st.info("Your watchlist is empty. Add some stocks above!")
        return
    
    st.markdown("---")
    
    try:
        monitor = MarketDataMonitor()
        calc = TechnicalIndicators()
        
        watchlist_data = []
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, symbol in enumerate(st.session_state.watchlist):
            status_text.text(f"Loading {symbol}...")
            
            try:
                df = monitor.get_historical_bars(symbol, timeframe='1Day', days_back=5)
                
                if not df.empty and len(df) >= 2:
                    current_price = df['close'].iloc[-1]
                    prev_price = df['close'].iloc[-2]
                    change = current_price - prev_price
                    change_pct = (change / prev_price) * 100
                    
                    day_high = df['high'].iloc[-1]
                    day_low = df['low'].iloc[-1]
                    volume = df['volume'].iloc[-1]
                    
                    try:
                        close_series = df['close']
                        rsi = calc.calculate_rsi(close_series)
                        current_rsi = rsi.iloc[-1] if len(rsi) > 0 else 50
                    except:
                        current_rsi = 50
                    
                    watchlist_data.append({
                        'Symbol': symbol,
                        'Price': f"${current_price:.2f}",
                        'Change': f"{change:+.2f}",
                        'Change %': f"{change_pct:+.2f}%",
                        'High': f"${day_high:.2f}",
                        'Low': f"${day_low:.2f}",
                        'Volume': f"{volume:,.0f}",
                        'RSI': f"{current_rsi:.1f}",
                        'Remove': symbol
                    })
            except Exception as e:
                watchlist_data.append({
                    'Symbol': symbol,
                    'Price': 'Error',
                    'Change': '-',
                    'Change %': '-',
                    'High': '-',
                    'Low': '-',
                    'Volume': '-',
                    'RSI': '-',
                    'Remove': symbol
                })
            
            progress_bar.progress((i + 1) / len(st.session_state.watchlist))
        
        progress_bar.empty()
        status_text.empty()
        
        if watchlist_data:
            df = pd.DataFrame(watchlist_data)
            
            st.dataframe(
                df[['Symbol', 'Price', 'Change', 'Change %', 'High', 'Low', 'Volume', 'RSI']],
                use_container_width=True,
                hide_index=True
            )
            
            st.markdown("### Quick Actions")
            
            cols = st.columns(len(st.session_state.watchlist))
            
            for i, symbol in enumerate(st.session_state.watchlist):
                with cols[i]:
                    if st.button(f"❌ {symbol}", use_container_width=True, key=f"remove_{symbol}"):
                        st.session_state.watchlist.remove(symbol)
                        st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Price Alerts")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            alert_symbol = st.selectbox("Stock:", st.session_state.watchlist)
        
        with col2:
            alert_price = st.number_input("Target Price:", min_value=0.01, value=100.0, step=1.0)
        
        with col3:
            alert_condition = st.selectbox("When price:", ["goes above", "goes below"])
        
        if st.button("🔔 Set Alert", use_container_width=True):
            if 'price_alerts' not in st.session_state:
                st.session_state.price_alerts = []
            
            st.session_state.price_alerts.append({
                'symbol': alert_symbol,
                'price': alert_price,
                'condition': alert_condition,
                'created': datetime.now()
            })
            
            st.success(f"Alert set: {alert_symbol} {alert_condition} ${alert_price:.2f}")
        
        if 'price_alerts' in st.session_state and st.session_state.price_alerts:
            st.markdown("**Active Alerts:**")
            for alert in st.session_state.price_alerts:
                st.info(f"{alert['symbol']} {alert['condition']} ${alert['price']:.2f}")
        
        auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds", value=False)
        
        if auto_refresh:
            st.caption("Auto-refreshing...")
            time.sleep(30)
            st.rerun()
    
    except Exception as e:
        st.error(f"Error loading watchlist: {str(e)}")
        st.exception(e)
