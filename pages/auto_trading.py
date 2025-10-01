import streamlit as st
import pandas as pd
import time

from trading.autonomous_bot import AutonomousTradingBot
from trading.strategy_engine import StrategyEngine

def show():
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>Autonomous Trading Bot</h1>
        <p style='color: #666; font-size: 1.1rem;'>Let AI trade for you automatically</p>
    </div>
    """, unsafe_allow_html=True)
    
    bot = st.session_state.get('trading_bot', None)
    
    if bot:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if bot.running:
                st.success("Bot is RUNNING - Watching the market for you")
            else:
                st.warning("Bot is SET UP but STOPPED - Click 'Start Trading' below")
        
        with col2:
            if st.button("Refresh", use_container_width=True):
                st.rerun()
    else:
        st.info("Welcome! Let's set up your trading bot in 3 easy steps")
    
    st.markdown("---")
    
    if not bot:
        st.markdown("## Step 1: Pick Your Stocks")
        st.markdown("Choose 3-10 stocks you want the bot to watch and trade automatically.")
        
        watchlist_input = st.text_area(
            "Type stock symbols here (one per line):",
            value="AAPL\nMSFT\nGOOGL\nTSLA\nAMZN",
            height=140,
            help="Popular stocks: AAPL (Apple), MSFT (Microsoft), TSLA (Tesla)"
        )
        
        watchlist = [s.strip().upper() for s in watchlist_input.split('\n') if s.strip()]
        
        if len(watchlist) >= 3:
            st.success(f"Great! You selected {len(watchlist)} stocks")
        else:
            st.warning(f"Add at least 3 stocks (you have {len(watchlist)})")
        
        st.markdown("---")
        st.markdown("## Step 2: Choose Trading Style")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Pick a Strategy")
            
            strategy_choice = st.radio(
                "How should the bot trade?",
                [
                    "Hybrid (RECOMMENDED)",
                    "Momentum (Buy stocks going up)",
                    "Mean Reversion (Buy dips, sell rallies)"
                ],
                index=0
            )
            
            strategy_map = {
                "Hybrid (RECOMMENDED)": "hybrid",
                "Momentum (Buy stocks going up)": "momentum",
                "Mean Reversion (Buy dips, sell rallies)": "mean_reversion"
            }
            
            selected_strategy = strategy_map[strategy_choice]
            
            if "RECOMMENDED" in strategy_choice:
                st.info("Hybrid combines multiple strategies - Perfect for beginners")
        
        with col2:
            st.markdown("### Update Frequency")
            
            update_minutes = st.select_slider(
                "How often should it check the market?",
                options=[1, 5, 10, 15, 30, 60],
                value=5,
                help="The bot will look for trading opportunities at this interval"
            )
            
            st.success(f"Will check every {update_minutes} minute(s)")
        
        st.markdown("---")
        st.markdown("## Step 3: Safety Settings")
        
        paper_mode = st.checkbox(
            "Use PAPER TRADING (Practice with fake money - RECOMMENDED)",
            value=True,
            help="Keep this ON until you're ready for real money!"
        )
        
        if paper_mode:
            st.success("SAFE MODE - You're using practice money. No risk!")
        else:
            st.error("DANGER - This will use REAL MONEY. Only for experts!")
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            if st.button("CREATE & START BOT", type="primary", use_container_width=True):
                if len(watchlist) < 3:
                    st.error("Please add at least 3 stocks!")
                else:
                    with st.spinner("Creating your bot..."):
                        try:
                            bot = AutonomousTradingBot(
                                watchlist=watchlist,
                                strategy_name=selected_strategy,
                                paper_mode=paper_mode,
                                update_interval=update_minutes * 60
                            )
                            st.session_state.trading_bot = bot
                            bot.start()
                            
                            st.success("SUCCESS! Your bot is created and running!")
                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"Oops! Something went wrong: {str(e)}")
                            st.markdown("""
                            **Common fixes:**
                            - Make sure your Alpaca API keys are set up
                            - Try refreshing the page
                            - Check your internet connection
                            """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("New to trading? Read this first"):
            st.markdown("""
            ### What is a Trading Bot?
            
            A trading bot is like a robot assistant that:
            - Watches stock prices 24/7
            - Buys stocks when they look good
            - Sells stocks to make profit
            - Does everything automatically while you sleep
            
            ### Is it safe?
            
            **YES!** When you use Paper Trading mode (which we recommend):
            - Uses FAKE money only
            - You can practice without risk
            - Learn how it works before using real money
            
            ### What should I pick?
            
            **Stocks:** Start with big companies like Apple (AAPL), Microsoft (MSFT)
            
            **Strategy:** Choose Hybrid - it's the safest for beginners
            
            **Frequency:** 5 minutes is perfect - not too fast, not too slow
            
            **Safety:** ALWAYS use Paper Trading when you're learning!
            """)
        
        return
    
    st.markdown("## Bot Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if not bot.running:
            if st.button("START TRADING", use_container_width=True, type="primary"):
                try:
                    bot.start()
                    st.success("Bot is now running!")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            if st.button("STOP TRADING", use_container_width=True):
                try:
                    bot.stop()
                    st.warning("Bot stopped")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("VIEW DASHBOARD", use_container_width=True):
            st.session_state.selected_page = 'dashboard'
            st.rerun()
    
    with col3:
        if st.button("START OVER", use_container_width=True):
            if st.session_state.get('confirm_reset'):
                if bot.running:
                    bot.stop()
                del st.session_state.trading_bot
                st.session_state.confirm_reset = False
                st.success("Reset complete!")
                time.sleep(1)
                st.rerun()
            else:
                st.session_state.confirm_reset = True
                st.warning("Click again to confirm")
    
    st.markdown("---")
    st.markdown("## Your Account")
    
    try:
        status = bot.get_status()
        account = status.get('account', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Value", f"${float(account.get('portfolio_value', 0)):,.2f}")
        
        with col2:
            st.metric("Cash", f"${float(account.get('cash', 0)):,.2f}")
        
        with col3:
            st.metric("Trades", status.get('positions_count', 0))
        
        with col4:
            st.metric("Can Invest", f"${float(account.get('buying_power', 0)):,.2f}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Trading Now")
            positions = status.get('positions', [])
            
            if positions and not any('error' in p for p in positions):
                for pos in positions:
                    pnl = float(pos.get('unrealized_pl', 0))
                    pnl_pct = float(pos.get('unrealized_plpc', 0)) * 100
                    symbol = pos.get('symbol')
                    
                    if pnl > 0:
                        st.success(f"{symbol}: +${pnl:.2f} (+{pnl_pct:.1f}%)")
                    elif pnl < 0:
                        st.error(f"{symbol}: ${pnl:.2f} ({pnl_pct:.1f}%)")
                    else:
                        st.info(f"{symbol}: ${pnl:.2f} (0%)")
            else:
                st.info("No trades yet - The bot is watching for good opportunities")
        
        with col2:
            st.markdown("### Recent Activity")
            recent_signals = status.get('recent_signals', [])
            
            if recent_signals:
                for signal in recent_signals[:5]:
                    sig_type = signal.get('signal', 'NONE')
                    symbol = signal.get('symbol', 'N/A')
                    
                    if sig_type == 'BUY':
                        st.success(f"Bought {symbol}")
                    elif sig_type == 'SELL':
                        st.error(f"Sold {symbol}")
                    else:
                        st.info(f"Watching {symbol}")
            else:
                st.info("Bot is watching the market...")
        
        with st.expander("Your Bot Settings"):
            st.write(f"**Strategy:** {bot.strategy_name.title()}")
            st.write(f"**Stocks:** {', '.join(bot.watchlist)}")
            st.write(f"**Check Every:** {bot.update_interval//60} minutes")
            st.write(f"**Mode:** {'Paper (Practice)' if bot.paper_mode else 'Real Money'}")
            st.write(f"**Status:** {'Running' if bot.running else 'Stopped'}")
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Try clicking the Refresh button above")
