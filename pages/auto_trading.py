import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time

from trading.autonomous_bot import AutonomousTradingBot
from trading.strategy_engine import StrategyEngine

@st.cache_resource
def get_trading_bot():
    """Initialize or get existing trading bot"""
    if 'trading_bot_initialized' not in st.session_state:
        return None
    return st.session_state.get('trading_bot')

def show():
    st.markdown("""
    <style>
    .auto-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .auto-header h1 {
        color: white;
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
    }
    
    .auto-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .status-card {
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .metric-box {
        text-align: center;
        padding: 1.2rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 0.3rem;
    }
    
    .metric-box h3 {
        margin: 0;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    .metric-box p {
        margin: 0.3rem 0 0 0;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='auto-header'>
        <h1>🤖 Autonomous Trading Bot</h1>
        <p>AI-powered algorithmic trading on autopilot</p>
    </div>
    """, unsafe_allow_html=True)
    
    if 'trading_bot_initialized' not in st.session_state:
        st.session_state.trading_bot_initialized = False
    
    bot = get_trading_bot()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⚙️ Bot Configuration")
    
    with col2:
        if bot and bot.running:
            st.markdown("**Status:** 🟢 **RUNNING**")
        elif bot and not bot.running:
            st.markdown("**Status:** 🟡 **STOPPED**")
        else:
            st.markdown("**Status:** ⚪ **NOT INITIALIZED**")
    
    with st.expander("📋 Configuration Settings", expanded=not st.session_state.trading_bot_initialized):
        col1, col2 = st.columns(2)
        
        with col1:
            watchlist_input = st.text_area(
                "Watchlist (one symbol per line)",
                value="AAPL\nMSFT\nGOOGL\nTSLA\nAMZN",
                height=150,
                help="Enter stock symbols to monitor, one per line"
            )
            
            watchlist = [s.strip() for s in watchlist_input.split('\n') if s.strip()]
            
            strategy_engine = StrategyEngine()
            available_strategies = strategy_engine.get_available_strategies()
            
            selected_strategy = st.selectbox(
                "Trading Strategy",
                options=available_strategies,
                index=available_strategies.index('hybrid') if 'hybrid' in available_strategies else 0,
                help="Select the trading strategy to use"
            )
        
        with col2:
            update_interval = st.slider(
                "Update Interval (seconds)",
                min_value=60,
                max_value=600,
                value=300,
                step=60,
                help="How often to check for trading opportunities"
            )
            
            paper_mode = st.checkbox(
                "Paper Trading Mode",
                value=True,
                help="Enable paper trading (no real money)"
            )
            
            if not paper_mode:
                st.warning("⚠️ Real trading mode will execute real trades with real money!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Initialize Bot", use_container_width=True, type="primary"):
                try:
                    bot = AutonomousTradingBot(
                        watchlist=watchlist,
                        strategy_name=selected_strategy,
                        paper_mode=paper_mode,
                        update_interval=update_interval
                    )
                    st.session_state.trading_bot = bot
                    st.session_state.trading_bot_initialized = True
                    st.success("✅ Bot initialized successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Failed to initialize bot: {str(e)}")
        
        with col2:
            if st.button("🔄 Reset Configuration", use_container_width=True):
                if 'trading_bot' in st.session_state:
                    if st.session_state.trading_bot.running:
                        st.session_state.trading_bot.stop()
                    del st.session_state.trading_bot
                st.session_state.trading_bot_initialized = False
                st.rerun()
    
    if not bot:
        st.info("👆 Configure and initialize the bot above to get started")
        
        st.markdown("### 📚 Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🎯 Multiple Strategies**
            - Momentum trading
            - Mean reversion
            - Sentiment-based
            - Hybrid approach
            """)
        
        with col2:
            st.markdown("""
            **🛡️ Risk Management**
            - Position sizing
            - Stop-loss orders
            - Take-profit targets
            - Drawdown protection
            """)
        
        with col3:
            st.markdown("""
            **📊 Real-time Monitoring**
            - Live market data
            - Performance tracking
            - Trade logging
            - Error handling
            """)
        
        return
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not bot.running:
            if st.button("▶️ Start Bot", use_container_width=True, type="primary"):
                bot.start()
                st.success("Bot started!")
                time.sleep(1)
                st.rerun()
        else:
            if st.button("⏸️ Stop Bot", use_container_width=True, type="secondary"):
                bot.stop()
                st.warning("Bot stopped")
                time.sleep(1)
                st.rerun()
    
    with col2:
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.rerun()
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh (30s)", value=False)
    
    if auto_refresh:
        time.sleep(30)
        st.rerun()
    
    st.markdown("### 📊 Performance Dashboard")
    
    status = bot.get_status()
    account = status.get('account', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='metric-box' style='background: linear-gradient(135deg, #4CAF50, #45a049);'>
            <h3>${float(account.get('portfolio_value', 0)):,.2f}</h3>
            <p>Portfolio Value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='metric-box' style='background: linear-gradient(135deg, #2196F3, #1976d2);'>
            <h3>${float(account.get('cash', 0)):,.2f}</h3>
            <p>Cash Available</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='metric-box' style='background: linear-gradient(135deg, #FF9800, #f57c00);'>
            <h3>{status.get('positions_count', 0)}</h3>
            <p>Active Positions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        buying_power = float(account.get('buying_power', 0))
        st.markdown(f"""
        <div class='metric-box' style='background: linear-gradient(135deg, #9C27B0, #7b1fa2);'>
            <h3>${buying_power:,.2f}</h3>
            <p>Buying Power</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💼 Current Positions")
        positions = status.get('positions', [])
        
        if positions and not any('error' in p for p in positions):
            positions_data = []
            for pos in positions:
                positions_data.append({
                    'Symbol': pos.get('symbol'),
                    'Quantity': int(float(pos.get('qty', 0))),
                    'Avg Price': f"${float(pos.get('avg_entry_price', 0)):.2f}",
                    'Current': f"${float(pos.get('current_price', 0)):.2f}",
                    'P/L': f"${float(pos.get('unrealized_pl', 0)):.2f}",
                    'P/L %': f"{float(pos.get('unrealized_plpc', 0)) * 100:.2f}%"
                })
            
            df_positions = pd.DataFrame(positions_data)
            st.dataframe(df_positions, use_container_width=True, hide_index=True)
        else:
            st.info("No active positions")
    
    with col2:
        st.markdown("#### 📈 Watchlist Status")
        watchlist_data = []
        
        for symbol in bot.watchlist:
            market_data = bot.market_monitor.get_cached_data(symbol)
            if market_data is not None and len(market_data) > 0:
                latest_price = market_data['close'].iloc[-1]
                price_change = bot.market_monitor.get_price_change(symbol, period=1)
                
                watchlist_data.append({
                    'Symbol': symbol,
                    'Price': f"${latest_price:.2f}",
                    'Change': f"{price_change.get('change_pct', 0):.2f}%" if price_change else "N/A",
                    'Status': '✅ Active'
                })
        
        if watchlist_data:
            df_watchlist = pd.DataFrame(watchlist_data)
            st.dataframe(df_watchlist, use_container_width=True, hide_index=True)
        else:
            st.info("Loading market data...")
    
    st.markdown("#### 📊 Performance Metrics")
    
    try:
        performance = bot.get_performance_metrics()
        risk_metrics = performance.get('risk_metrics', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Win Rate", f"{risk_metrics.get('win_rate', 0):.1f}%")
            st.metric("Total Trades", risk_metrics.get('total_trades', 0))
        
        with col2:
            st.metric("Sharpe Ratio", f"{risk_metrics.get('sharpe_ratio', 0):.2f}")
            st.metric("Profit Factor", f"{risk_metrics.get('profit_factor', 0):.2f}")
        
        with col3:
            st.metric("Avg Win", f"${risk_metrics.get('avg_win', 0):.2f}")
            st.metric("Avg Loss", f"${risk_metrics.get('avg_loss', 0):.2f}")
        
        with col4:
            drawdown = performance.get('drawdown', {})
            st.metric("Current Drawdown", f"{drawdown.get('current_drawdown', 0):.2f}%")
            st.metric("Max Drawdown", f"{drawdown.get('max_drawdown', 0):.1f}%")
    
    except Exception as e:
        st.warning(f"Performance metrics unavailable: {str(e)}")
    
    with st.expander("📜 Recent Trade History"):
        trades = bot.logger.get_recent_trades(limit=20)
        
        if trades:
            trades_data = []
            for trade in reversed(trades):
                trades_data.append({
                    'Time': datetime.fromisoformat(trade['timestamp']).strftime('%Y-%m-%d %H:%M'),
                    'Symbol': trade.get('symbol'),
                    'Action': trade.get('action', '').upper(),
                    'Qty': trade.get('quantity'),
                    'Price': f"${trade.get('price', 0):.2f}",
                    'Value': f"${trade.get('total_value', 0):.2f}",
                    'Strategy': trade.get('strategy'),
                    'Confidence': f"{trade.get('confidence', 0):.1%}"
                })
            
            df_trades = pd.DataFrame(trades_data)
            st.dataframe(df_trades, use_container_width=True, hide_index=True)
        else:
            st.info("No trades yet")
    
    with st.expander("📝 Recent Decisions Log"):
        decisions = bot.logger.get_recent_decisions(limit=30)
        
        if decisions:
            decisions_data = []
            for decision in reversed(decisions):
                decisions_data.append({
                    'Time': datetime.fromisoformat(decision['timestamp']).strftime('%Y-%m-%d %H:%M'),
                    'Symbol': decision.get('symbol'),
                    'Signal': decision.get('signal'),
                    'Strategy': decision.get('strategy'),
                    'Confidence': f"{decision.get('confidence', 0):.1%}",
                    'Executed': '✅' if decision.get('executed') else '❌',
                    'Reason': decision.get('reason', '')
                })
            
            df_decisions = pd.DataFrame(decisions_data)
            st.dataframe(df_decisions, use_container_width=True, hide_index=True)
        else:
            st.info("No decisions logged yet")
    
    st.markdown("---")
    st.caption("⚠️ Trading involves risk. Past performance does not guarantee future results. Always monitor your bot and manage risk appropriately.")
