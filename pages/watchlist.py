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
        st.session_state.watchlist = []
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### Your Watchlist")
    
    with col2:
        if st.button("🔄 Refresh Prices", use_container_width=True):
            st.rerun()
    
    st.markdown("### Quick Add Stocks")
    
    popular_stocks = {
        "🇺🇸 Tech": ["AAPL", "MSFT", "GOOGL", "META", "NVDA", "TSLA", "AMZN", "NFLX", "AMD", "INTC"],
        "🇺🇸 Banking": ["JPM", "BAC", "WFC", "C", "GS", "MS"],
        "🇺🇸 Healthcare": ["JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK"],
        "🇺🇸 Consumer": ["WMT", "HD", "NKE", "SBUX", "MCD", "DIS"],
        "🇮🇳 Tech": ["TCS.NS", "INFY.NS", "HCLTECH.NS", "WIPRO.NS", "TECHM.NS"],
        "🇮🇳 Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS", "KOTAKBANK.NS", "AXISBANK.NS"],
        "🇮🇳 Auto": ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS"],
        "🇮🇳 Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS", "BIOCON.NS"]
    }
    
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        selected_category = st.selectbox(
            "Select Category:",
            options=list(popular_stocks.keys())
        )
    
    with col2:
        selected_stock = st.selectbox(
            "Select Stock:",
            options=popular_stocks[selected_category]
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add", use_container_width=True, key="add_preset"):
            if selected_stock not in st.session_state.watchlist:
                st.session_state.watchlist.append(selected_stock)
                st.success(f"Added {selected_stock}")
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning(f"{selected_stock} already in watchlist")
    
    st.markdown("### Or Add Custom Stock")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        new_symbol = st.text_input(
            "Enter stock symbol:",
            placeholder="e.g., AAPL or RELIANCE.NS",
            max_chars=20
        ).upper()
        
        if st.button("➕ Add Custom Stock", use_container_width=True):
            if new_symbol and new_symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_symbol)
                st.success(f"Added {new_symbol}")
                time.sleep(0.5)
                st.rerun()
            elif new_symbol in st.session_state.watchlist:
                st.warning(f"{new_symbol} is already in your watchlist")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear All", use_container_width=True):
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
                        close_series = pd.Series(df['close'])
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
            
            st.markdown("### Stock Performance")
            
            for stock_data in watchlist_data:
                if stock_data['Price'] != 'Error':
                    change_pct = float(stock_data['Change %'].replace('%', '').replace('+', ''))
                    if change_pct >= 0:
                        bg_color = "#e8f5e9"
                        border_color = "#4CAF50"
                        icon = "📈"
                    else:
                        bg_color = "#ffebee"
                        border_color = "#f44336"
                        icon = "📉"
                    
                    rsi_val = float(stock_data['RSI'])
                    if rsi_val < 30:
                        rsi_status = "Oversold"
                        rsi_color = "#4CAF50"
                    elif rsi_val > 70:
                        rsi_status = "Overbought"
                        rsi_color = "#f44336"
                    else:
                        rsi_status = "Neutral"
                        rsi_color = "#666"
                    
                    st.markdown(f"""
                    <div style='background: {bg_color}; 
                               border: 3px solid {border_color}; 
                               padding: 1.5rem; 
                               margin: 1rem 0; 
                               border-radius: 12px;
                               box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
                            <div style='flex: 1; min-width: 150px;'>
                                <h2 style='margin: 0; font-size: 2rem; font-weight: bold;'>{icon} {stock_data['Symbol']}</h2>
                            </div>
                            <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                                <p style='margin: 0; color: #0d47a1; font-size: 1rem; font-weight: 600;'>Price</p>
                                <p style='margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold; color: #1a237e;'>{stock_data['Price']}</p>
                                <p style='margin: 0; color: {border_color}; font-weight: bold; font-size: 1.2rem;'>{stock_data['Change %']}</p>
                            </div>
                            <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                                <p style='margin: 0; color: #0d47a1; font-size: 1rem; font-weight: 600;'>High / Low</p>
                                <p style='margin: 0.25rem 0; font-size: 1.3rem; font-weight: 600; color: #1a237e;'>{stock_data['High']}</p>
                                <p style='margin: 0; font-size: 1.3rem; font-weight: 600; color: #1a237e;'>{stock_data['Low']}</p>
                            </div>
                            <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                                <p style='margin: 0; color: #0d47a1; font-size: 1rem; font-weight: 600;'>Volume</p>
                                <p style='margin: 0.5rem 0; font-size: 1.3rem; font-weight: 600; color: #1a237e;'>{stock_data['Volume']}</p>
                            </div>
                            <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                                <p style='margin: 0; color: #0d47a1; font-size: 1rem; font-weight: 600;'>RSI</p>
                                <p style='margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold; color: {rsi_color};'>{stock_data['RSI']}</p>
                                <p style='margin: 0; font-size: 1rem; font-weight: 600; color: {rsi_color};'>{rsi_status}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: #fafafa; 
                               border-left: 4px solid #999; 
                               padding: 1rem; 
                               margin: 0.5rem 0; 
                               border-radius: 8px;'>
                        <h3 style='margin: 0; font-size: 1.5rem;'>⚠️ {stock_data['Symbol']}</h3>
                        <p style='margin: 0.25rem 0; color: #666;'>Unable to fetch data for this symbol</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
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
