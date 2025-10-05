import streamlit as st
import pandas as pd
from datetime import datetime

from trading.market_monitor import MarketDataMonitor
from trading.technical_indicators import TechnicalIndicators

def show():
    from utils.ui_helpers import get_theme
    theme = get_theme()
    
    st.markdown(f"""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>🔍 Market Scanner</h1>
        <p style='color: {theme['text_secondary']}; font-size: 1.1rem;'>Discover trading opportunities in real-time</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎯 What kind of opportunities are you looking for?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scan_options = {
            "Momentum Breakout": {
                "emoji": "🚀",
                "desc": "Strong upward movement with high volume"
            },
            "Oversold Stocks": {
                "emoji": "📉",
                "desc": "Stocks that may bounce back up"
            },
            "Overbought Stocks": {
                "emoji": "📈",
                "desc": "Stocks that may pull back down"
            },
            "Volume Spike": {
                "emoji": "📊",
                "desc": "Unusual trading activity"
            },
            "Moving Average Cross": {
                "emoji": "✂️",
                "desc": "Trend change signals"
            }
        }
        
        selected_scan = st.selectbox(
            "Scan Type",
            options=list(scan_options.keys()),
            format_func=lambda x: f"{scan_options[x]['emoji']} {x}"
        )
        
        st.info(f"**Looking for:** {scan_options[selected_scan]['desc']}")
    
    with col2:
        st.markdown("**Stocks to scan**")
        watchlist_input = st.text_area(
            "Enter symbols (one per line):",
            value="",
            height=150,
            placeholder="AAPL\nMSFT\nGOOGL\nTSLA"
        )
        
        symbols = [s.strip().upper() for s in watchlist_input.split('\n') if s.strip()]
        st.caption(f"✓ Will scan {len(symbols)} stocks")
    
    if st.button("🔍 Scan Now", type="primary", use_container_width=True):
        with st.spinner(f"Scanning {len(symbols)} stocks..."):
            monitor = MarketDataMonitor()
            calc = TechnicalIndicators()
            
            scan_type_map = {
                "Momentum Breakout": "Momentum Breakout",
                "Oversold Stocks": "Oversold (RSI)",
                "Overbought Stocks": "Overbought (RSI)",
                "Volume Spike": "Volume Spike",
                "Moving Average Cross": "Moving Average Crossover"
            }
            
            actual_scan = scan_type_map[selected_scan]
            
            results = []
            progress_bar = st.progress(0)
            
            for i, symbol in enumerate(symbols):
                try:
                    df = monitor.get_historical_bars(symbol, timeframe='1Day', days_back=60)
                    
                    if df.empty or len(df) < 30:
                        continue
                    
                    close = df['close']
                    high = df['high']
                    low = df['low']
                    volume = df['volume']
                    
                    try:
                        rsi = calc.calculate_rsi(close)
                        current_rsi = rsi.iloc[-1] if not rsi.empty else 50
                    except:
                        current_rsi = 50
                    
                    sma_20 = calc.calculate_sma(close, 20)
                    sma_50 = calc.calculate_sma(close, 50)
                    
                    current_price = close.iloc[-1]
                    prev_price = close.iloc[-2]
                    price_change = ((current_price - prev_price) / prev_price) * 100
                    
                    current_volume = volume.iloc[-1]
                    avg_volume = volume.rolling(20).mean().iloc[-1]
                    volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
                    
                    signal = None
                    score = 0
                    
                    if actual_scan == "Momentum Breakout":
                        if current_rsi > 60 and price_change > 2 and volume_ratio > 1.5:
                            signal = "BUY"
                            score = min(current_rsi + (price_change * 5) + (volume_ratio * 10), 100)
                    
                    elif actual_scan == "Oversold (RSI)":
                        if current_rsi < 35:
                            signal = "BUY"
                            score = 100 - current_rsi
                    
                    elif actual_scan == "Overbought (RSI)":
                        if current_rsi > 65:
                            signal = "SELL"
                            score = current_rsi
                    
                    elif actual_scan == "Volume Spike":
                        if volume_ratio > 2.0:
                            signal = "WATCH"
                            score = volume_ratio * 20
                    
                    elif actual_scan == "Moving Average Crossover":
                        if len(sma_20) > 1 and len(sma_50) > 1:
                            if sma_20.iloc[-1] > sma_50.iloc[-1] and sma_20.iloc[-2] <= sma_50.iloc[-2]:
                                signal = "BUY"
                                score = 75
                            elif sma_20.iloc[-1] < sma_50.iloc[-1] and sma_20.iloc[-2] >= sma_50.iloc[-2]:
                                signal = "SELL"
                                score = 75
                    
                    if signal:
                        results.append({
                            'Stock': symbol,
                            'Signal': signal,
                            'Strength': f"{round(score, 0)}/100",
                            'Price': f"${current_price:.2f}",
                            'Change': f"{price_change:+.1f}%",
                            'RSI': round(current_rsi, 0),
                            'Volume': f"{volume_ratio:.1f}x"
                        })
                
                except Exception as e:
                    print(f"Error scanning {symbol}: {e}")
                
                progress_bar.progress((i + 1) / len(symbols))
            
            progress_bar.empty()
            
            st.session_state.scan_results = results
            st.session_state.scan_timestamp = datetime.now()
    
    if 'scan_results' in st.session_state and st.session_state.scan_results:
        results = st.session_state.scan_results
        timestamp = st.session_state.scan_timestamp
        
        st.markdown("---")
        st.markdown(f"### 🎯 Found {len(results)} Opportunities")
        st.caption(f"Scanned: {timestamp.strftime('%I:%M %p')}")
        
        if results:
            col1, col2, col3 = st.columns(3)
            
            buy_count = len([r for r in results if r['Signal'] == 'BUY'])
            sell_count = len([r for r in results if r['Signal'] == 'SELL'])
            watch_count = len([r for r in results if r['Signal'] == 'WATCH'])
            
            with col1:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #4CAF50, #45a049); 
                           padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>{buy_count}</h2>
                    <p style='margin: 0;'>BUY Signals</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f44336, #d32f2f); 
                           padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>{sell_count}</h2>
                    <p style='margin: 0;'>SELL Signals</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #FF9800, #f57c00); 
                           padding: 1rem; border-radius: 10px; text-align: center; color: white;'>
                    <h2 style='margin: 0;'>{watch_count}</h2>
                    <p style='margin: 0;'>WATCH Signals</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            df = pd.DataFrame(results)
            
            for result in results:
                signal = result['Signal']
                if signal == 'BUY':
                    bg_color = "#e8f5e9"
                    border_color = "#4CAF50"
                    icon = "🟢"
                elif signal == 'SELL':
                    bg_color = "#ffebee"
                    border_color = "#f44336"
                    icon = "🔴"
                else:
                    bg_color = "#fff3e0"
                    border_color = "#FF9800"
                    icon = "🟡"
                
                st.markdown(f"""
                <div style='background: {bg_color}; 
                           border: 3px solid {border_color}; 
                           padding: 1.5rem; 
                           margin: 1rem 0; 
                           border-radius: 12px;
                           box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;'>
                        <div style='flex: 1; min-width: 150px;'>
                            <h2 style='margin: 0; font-size: 2rem; font-weight: bold; color: #1a1a1a;'>{icon} {result['Stock']}</h2>
                            <p style='margin: 0.5rem 0; color: #1a1a1a; font-size: 1.1rem;'>Signal: <strong>{result['Signal']}</strong></p>
                        </div>
                        <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                            <p style='margin: 0; color: #1a1a1a; font-size: 1rem; font-weight: 600;'>Price</p>
                            <p style='margin: 0.5rem 0; font-size: 1.5rem; font-weight: bold; color: #1a1a1a;'>{result['Price']}</p>
                            <p style='margin: 0; color: {"#2e7d32" if "+" in result['Change'] else "#c62828"}; font-weight: bold; font-size: 1.1rem;'>{result['Change']}</p>
                        </div>
                        <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                            <p style='margin: 0; color: #1a1a1a; font-size: 1rem; font-weight: 600;'>Strength</p>
                            <p style='margin: 0.5rem 0; font-size: 1.5rem; font-weight: bold; color: #1a1a1a;'>{result['Strength']}</p>
                        </div>
                        <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                            <p style='margin: 0; color: #1a1a1a; font-size: 1rem; font-weight: 600;'>RSI</p>
                            <p style='margin: 0.5rem 0; font-size: 1.5rem; font-weight: bold; color: #1a1a1a;'>{result['RSI']}</p>
                        </div>
                        <div style='flex: 1; min-width: 120px; text-align: center; background: white; padding: 1rem; border-radius: 8px;'>
                            <p style='margin: 0; color: #1a1a1a; font-size: 1rem; font-weight: 600;'>Volume</p>
                            <p style='margin: 0.5rem 0; font-size: 1.5rem; font-weight: bold; color: #1a1a1a;'>{result['Volume']}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📥 Export Results", use_container_width=True):
                    csv = df.to_csv(index=False)
                    st.download_button(
                        "Download CSV",
                        csv,
                        f"scan_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        "text/csv",
                        use_container_width=True
                    )
            
            with col2:
                if st.button("🔄 Scan Again", use_container_width=True):
                    st.rerun()
        else:
            st.info("😔 No opportunities found with current settings")
            st.markdown("**Try:**")
            st.markdown("- Adding more stocks")
            st.markdown("- Using a different scan type")
            st.markdown("- Checking again later")
    
    elif 'scan_results' in st.session_state:
        st.info("👆 Click 'Scan Now' to find opportunities")
