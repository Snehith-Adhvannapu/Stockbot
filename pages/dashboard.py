import streamlit as st
import pandas as pd
import time
from datetime import datetime

from agents.trading_agent import TradingAgent

def show():
    st.title("📊 Trading Dashboard")
    st.markdown("Your real-time trading overview")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    bot = st.session_state.get('trading_bot', None)
    
    if bot:
        st.markdown("### 🤖 Bot Status")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if bot.running:
                st.success("**Bot Status:** 🟢 Running")
            else:
                st.warning("**Bot Status:** 🟡 Stopped")
        
        with col2:
            st.info(f"**Strategy:** {bot.strategy_name.title()}")
        
        with col3:
            st.info(f"**Watching:** {len(bot.watchlist)} stocks")
        
        try:
            status = bot.get_status()
            account = status.get('account', {})
            
            st.markdown("---")
            st.markdown("### 💰 Account Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Portfolio Value", f"${float(account.get('portfolio_value', 0)):,.2f}")
            
            with col2:
                st.metric("Cash", f"${float(account.get('cash', 0)):,.2f}")
            
            with col3:
                st.metric("Positions", status.get('positions_count', 0))
            
            with col4:
                st.metric("Buying Power", f"${float(account.get('buying_power', 0)):,.2f}")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📋 Current Positions")
                positions = status.get('positions', [])
                
                if positions and not any('error' in p for p in positions):
                    pos_data = []
                    for pos in positions:
                        pnl = float(pos.get('unrealized_pl', 0))
                        pnl_pct = float(pos.get('unrealized_plpc', 0)) * 100
                        
                        pos_data.append({
                            'Stock': pos.get('symbol'),
                            'Shares': int(float(pos.get('qty', 0))),
                            'Value': f"${float(pos.get('market_value', 0)):,.2f}",
                            'P/L': f"${pnl:.2f} ({pnl_pct:+.1f}%)"
                        })
                    
                    df = pd.DataFrame(pos_data)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No active positions. The bot is watching for opportunities!")
            
            with col2:
                st.markdown("### 🎯 Recent Activity")
                recent_signals = status.get('recent_signals', [])
                
                if recent_signals:
                    for signal in recent_signals[:5]:
                        signal_type = signal.get('signal', 'NONE')
                        symbol = signal.get('symbol', 'N/A')
                        
                        if signal_type == 'BUY':
                            st.success(f"✅ BUY signal: {symbol}")
                        elif signal_type == 'SELL':
                            st.error(f"📤 SELL signal: {symbol}")
                        else:
                            st.info(f"👀 Watching: {symbol}")
                else:
                    st.info("No recent activity. Bot is monitoring...")
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("⚙️ Configure Bot", use_container_width=True):
                    st.session_state.selected_page = 'auto_trading'
                    st.rerun()
            
            with col2:
                if st.button("💼 View Portfolio", use_container_width=True):
                    st.session_state.selected_page = 'portfolio'
                    st.rerun()
            
            with col3:
                if st.button("📈 View Charts", use_container_width=True):
                    st.session_state.selected_page = 'charts'
                    st.rerun()
        
        except Exception as e:
            st.error(f"Error loading bot data: {str(e)}")
            st.info("💡 Tip: Make sure the bot is properly initialized")
    
    else:
        st.info("👋 Welcome to your Trading Dashboard!")
        
        st.markdown("### 🚀 Quick Start")
        
        st.markdown("""
        **You haven't set up a trading bot yet. Here's how to get started:**
        
        1. Click on "🤖 Trading Bot" in the sidebar
        2. Configure your watchlist (which stocks to monitor)
        3. Choose a trading strategy
        4. Enable Paper Trading mode (practice with fake money)
        5. Click "Start Bot"
        
        The bot will then automatically:
        - Monitor your selected stocks 24/7
        - Look for trading opportunities
        - Execute trades based on your strategy
        - Manage risk with stop-losses
        """)
        
        if st.button("🚀 Set Up Bot Now →", type="primary", use_container_width=True):
            st.session_state.selected_page = 'auto_trading'
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        try:
            trading_agent = TradingAgent()
            account = trading_agent.get_account_info()
            
            if 'error' not in account:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Account Value", f"${float(account.get('portfolio_value', 0)):,.2f}")
                
                with col2:
                    st.metric("Available Cash", f"${float(account.get('cash', 0)):,.2f}")
                
                with col3:
                    st.metric("Buying Power", f"${float(account.get('buying_power', 0)):,.2f}")
            else:
                st.warning("⚠️ Cannot connect to trading account. Check your API credentials.")
                st.info("💡 Make sure your Alpaca API keys are set correctly in the environment.")
        
        except Exception as e:
            st.warning("⚠️ Cannot load account data")
            st.info("💡 This is normal if you haven't set up your Alpaca API keys yet.")
        
        st.markdown("---")
        st.markdown("### ⚡ Other Tools")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Find Opportunities", use_container_width=True):
                st.session_state.selected_page = 'scanner'
                st.rerun()
        
        with col2:
            if st.button("📈 View Charts", use_container_width=True):
                st.session_state.selected_page = 'charts'
                st.rerun()
        
        with col3:
            if st.button("📚 Learn More", use_container_width=True):
                st.session_state.selected_page = 'help'
                st.rerun()
    
    auto_refresh = st.checkbox("🔄 Auto-refresh every 30 seconds", value=False)
    
    if auto_refresh and bot:
        st.caption("Dashboard will refresh in 30 seconds...")
        time.sleep(30)
        st.rerun()
