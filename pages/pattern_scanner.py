import streamlit as st
import pandas as pd
from datetime import datetime

from trading.market_monitor import MarketDataMonitor
from trading.pattern_recognition import PatternRecognition

def show():
    st.title("🔎 Pattern Scanner")
    st.markdown("Detect technical chart patterns that often lead to big price moves")
    
    st.markdown("### Which stocks should we scan?")
    
    watchlist_input = st.text_area(
        "Enter symbols (one per line):",
        value="AAPL\nMSFT\nGOOGL\nAMZN\nTSLA\nMETA\nNVDA",
        height=120
    )
    
    symbols = [s.strip().upper() for s in watchlist_input.split('\n') if s.strip()]
    st.caption(f"✓ Will scan {len(symbols)} stocks for patterns")
    
    with st.expander("📚 What patterns will we look for?"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Reversal Patterns:**
            - 🔺 Double Top (bearish)
            - 🔻 Double Bottom (bullish)
            - 👤 Head & Shoulders (bearish)
            """)
        
        with col2:
            st.markdown("""
            **Continuation Patterns:**
            - 📐 Triangles (breakout coming)
            - 🚩 Flags (trend continues)
            - ⬆️ Price Gaps (strong momentum)
            """)
    
    if st.button("🔍 Scan for Patterns", type="primary", use_container_width=True):
        with st.spinner(f"Scanning {len(symbols)} stocks..."):
            monitor = MarketDataMonitor()
            detector = PatternRecognition()
            
            all_results = []
            progress_bar = st.progress(0)
            
            for i, symbol in enumerate(symbols):
                try:
                    df = monitor.get_historical_bars(symbol, timeframe='1Day', days_back=90)
                    
                    if df.empty or len(df) < 30:
                        continue
                    
                    patterns = detector.scan_all_patterns(df)
                    
                    for pattern in patterns:
                        pattern_name = pattern['pattern'].replace('_', ' ').title()
                        all_results.append({
                            'Stock': symbol,
                            'Pattern': pattern_name,
                            'Signal': pattern['signal'],
                            'Confidence': f"{pattern['confidence']:.0%}"
                        })
                
                except Exception as e:
                    print(f"Error scanning {symbol}: {e}")
                
                progress_bar.progress((i + 1) / len(symbols))
            
            progress_bar.empty()
            
            st.session_state.pattern_results = all_results
            st.session_state.pattern_timestamp = datetime.now()
    
    if 'pattern_results' in st.session_state and st.session_state.pattern_results:
        results = st.session_state.pattern_results
        timestamp = st.session_state.pattern_timestamp
        
        st.markdown("---")
        st.markdown(f"### 🎯 Found {len(results)} Patterns")
        st.caption(f"Scanned at: {timestamp.strftime('%I:%M %p')}")
        
        if results:
            col1, col2, col3 = st.columns(3)
            
            buy_count = len([r for r in results if r['Signal'] == 'BUY'])
            sell_count = len([r for r in results if r['Signal'] == 'SELL'])
            watch_count = len([r for r in results if r['Signal'] == 'WATCH'])
            
            with col1:
                st.metric("Bullish Patterns", buy_count)
            with col2:
                st.metric("Bearish Patterns", sell_count)
            with col3:
                st.metric("Neutral Patterns", watch_count)
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            if st.button("📥 Export Results", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    f"patterns_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv"
                )
        else:
            st.info("No patterns detected. Try scanning more stocks or wait for better setups.")
    
    elif 'pattern_results' in st.session_state:
        st.info("👆 Click 'Scan for Patterns' to analyze the stocks")
