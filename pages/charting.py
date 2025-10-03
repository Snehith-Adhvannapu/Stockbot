import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from trading.market_monitor import MarketDataMonitor
from trading.technical_indicators import TechnicalIndicators

def show():
    from utils.ui_helpers import get_theme
    theme = get_theme()
    
    st.markdown(f"""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>📈 Advanced Charts</h1>
        <p style='color: {theme['text_secondary']}; font-size: 1.1rem;'>Professional stock charting with technical analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        symbol = st.text_input("📊 Stock Symbol", value="AAPL", max_chars=10).upper()
    
    with col2:
        timeframe = st.selectbox(
            "⏰ Timeframe",
            ["1 Day", "1 Hour", "15 Min"],
            index=0
        )
        timeframe_map = {"1 Day": "1Day", "1 Hour": "1Hour", "15 Min": "15Min"}
        actual_timeframe = timeframe_map[timeframe]
    
    with col3:
        days = st.slider("📅 History (days)", 7, 365, 90)
    
    col1, col2 = st.columns(2)
    
    with col1:
        chart_type = st.radio(
            "📊 Chart Style",
            ["Candlestick", "Line", "Area"],
            horizontal=True
        )
    
    with col2:
        indicators = st.multiselect(
            "📈 Technical Indicators",
            ["MA 20", "MA 50", "Bollinger Bands", "RSI", "MACD", "Volume"],
            default=["MA 20", "Volume"]
        )
    
    if st.button("📊 Load Chart", type="primary", use_container_width=True):
        with st.spinner(f"Loading {symbol} chart..."):
            try:
                monitor = MarketDataMonitor()
                calc = TechnicalIndicators()
                
                df = monitor.get_historical_bars(symbol, timeframe=actual_timeframe, days_back=days)
                
                if df.empty:
                    st.error(f"❌ No data found for {symbol}")
                    st.info("💡 Try a different symbol (e.g., AAPL, MSFT, GOOGL)")
                    return
                
                has_bottom = "RSI" in indicators or "MACD" in indicators or "Volume" in indicators
                rows = 2 if has_bottom else 1
                row_heights = [0.7, 0.3] if has_bottom else [1.0]
                
                fig = make_subplots(
                    rows=rows, cols=1,
                    row_heights=row_heights,
                    shared_xaxes=True,
                    vertical_spacing=0.05
                )
                
                if chart_type == "Candlestick":
                    fig.add_trace(
                        go.Candlestick(
                            x=df['timestamp'],
                            open=df['open'],
                            high=df['high'],
                            low=df['low'],
                            close=df['close'],
                            name=symbol,
                            increasing_line_color='#26a69a',
                            decreasing_line_color='#ef5350'
                        ),
                        row=1, col=1
                    )
                elif chart_type == "Line":
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=df['close'],
                            mode='lines',
                            name=symbol,
                            line=dict(color='#667eea', width=2)
                        ),
                        row=1, col=1
                    )
                else:
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=df['close'],
                            mode='lines',
                            name=symbol,
                            fill='tozeroy',
                            line=dict(color='#667eea', width=2),
                            fillcolor='rgba(102, 126, 234, 0.2)'
                        ),
                        row=1, col=1
                    )
                
                if "MA 20" in indicators:
                    sma20 = calc.calculate_sma(df['close'], 20)
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=sma20,
                            mode='lines',
                            name='MA 20',
                            line=dict(color='#FF9800', width=1.5)
                        ),
                        row=1, col=1
                    )
                
                if "MA 50" in indicators:
                    sma50 = calc.calculate_sma(df['close'], 50)
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=sma50,
                            mode='lines',
                            name='MA 50',
                            line=dict(color='#9C27B0', width=1.5)
                        ),
                        row=1, col=1
                    )
                
                if "Bollinger Bands" in indicators:
                    bb = calc.calculate_bollinger_bands(df['close'])
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=bb['upper'],
                            mode='lines',
                            name='BB Upper',
                            line=dict(color='rgba(128,128,128,0.3)', width=1)
                        ),
                        row=1, col=1
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=df['timestamp'],
                            y=bb['lower'],
                            mode='lines',
                            name='BB Lower',
                            line=dict(color='rgba(128,128,128,0.3)', width=1),
                            fill='tonexty',
                            fillcolor='rgba(128,128,128,0.1)'
                        ),
                        row=1, col=1
                    )
                
                if has_bottom:
                    if "RSI" in indicators:
                        rsi = calc.calculate_rsi(df['close'])
                        fig.add_trace(
                            go.Scatter(
                                x=df['timestamp'],
                                y=rsi,
                                mode='lines',
                                name='RSI',
                                line=dict(color='#9C27B0', width=2)
                            ),
                            row=2, col=1
                        )
                        fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=2, col=1)
                        fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=2, col=1)
                    
                    elif "MACD" in indicators:
                        macd_data = calc.calculate_macd(df['close'])
                        fig.add_trace(
                            go.Scatter(
                                x=df['timestamp'],
                                y=macd_data['macd'],
                                mode='lines',
                                name='MACD',
                                line=dict(color='#2196F3', width=2)
                            ),
                            row=2, col=1
                        )
                        fig.add_trace(
                            go.Scatter(
                                x=df['timestamp'],
                                y=macd_data['signal'],
                                mode='lines',
                                name='Signal',
                                line=dict(color='#FF9800', width=2)
                            ),
                            row=2, col=1
                        )
                    
                    else:
                        colors = ['#26a69a' if df['close'].iloc[i] >= df['open'].iloc[i] else '#ef5350' 
                                 for i in range(len(df))]
                        fig.add_trace(
                            go.Bar(
                                x=df['timestamp'],
                                y=df['volume'],
                                name='Volume',
                                marker_color=colors,
                                opacity=0.7
                            ),
                            row=2, col=1
                        )
                
                fig.update_layout(
                    title=f"{symbol} - {timeframe}",
                    xaxis_rangeslider_visible=False,
                    height=600,
                    showlegend=True,
                    hovermode='x unified',
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("### 📊 Quick Stats")
                
                col1, col2, col3 = st.columns(3)
                
                current_price = df['close'].iloc[-1]
                price_change = df['close'].iloc[-1] - df['close'].iloc[0]
                price_change_pct = (price_change / df['close'].iloc[0]) * 100
                
                with col1:
                    st.metric("Current Price", f"${current_price:.2f}")
                
                with col2:
                    st.metric(
                        "Period Change",
                        f"${price_change:.2f}",
                        f"{price_change_pct:+.2f}%"
                    )
                
                with col3:
                    volatility = calc.calculate_volatility(df['close'])
                    st.metric("Volatility", f"{volatility:.2f}%")
                
            except Exception as e:
                st.error(f"❌ Error loading chart: {str(e)}")
                st.info("💡 Try a different stock symbol or check your connection")
    
    else:
        st.info("👆 Enter a stock symbol and click 'Load Chart' to visualize price data")
        
        st.markdown("### 💡 Chart Tips")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Popular Stocks to Try:**
            - AAPL (Apple)
            - MSFT (Microsoft)
            - GOOGL (Google)
            - TSLA (Tesla)
            - AMZN (Amazon)
            """)
        
        with col2:
            st.markdown("""
            **Recommended Indicators:**
            - **MA 20, MA 50**: Trend direction
            - **Bollinger Bands**: Volatility
            - **RSI**: Overbought/Oversold
            - **MACD**: Momentum
            - **Volume**: Trading activity
            """)
