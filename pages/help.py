import streamlit as st

def show():
    st.title("📚 Help & Documentation")
    st.markdown("Learn how to use the Stock Trading Platform")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Getting Started", "Features", "FAQ", "Troubleshooting"])
    
    with tab1:
        st.markdown("### 🚀 Getting Started")
        
        st.markdown("""
        **Step 1: Choose Your Mode**
        - **AI Stock Advisor**: Get recommendations for stocks to buy or sell
        - **Autonomous Trading**: Set up an automated trading bot
        
        **Step 2: Configure Your Settings**
        - Enter stock symbols you want to monitor
        - Choose your trading strategy
        - Set risk parameters (stop loss, position size, etc.)
        
        **Step 3: Start Trading**
        - For AI Advisor: Enter a symbol and click Analyze
        - For Bot: Click "Start Bot" after configuration
        
        **Important:** Always use Paper Trading mode first to practice without real money!
        """)
    
    with tab2:
        st.markdown("### ✨ Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **AI Stock Advisor**
            - Sentiment analysis from news
            - Fundamental company analysis
            - Combined recommendation score
            - Customizable weights
            
            **Trading Bot**
            - 24/7 automated trading
            - Multiple strategy options
            - Risk management built-in
            - Real-time monitoring
            
            **Portfolio Manager**
            - Track all your positions
            - See profit/loss in real-time
            - Diversification analysis
            - Performance metrics
            """)
        
        with col2:
            st.markdown("""
            **Market Scanner**
            - Find trading opportunities
            - Multiple scan types
            - Customizable criteria
            - Export results to CSV
            
            **Charts**
            - Advanced technical analysis
            - Multiple timeframes
            - Popular indicators
            - Interactive visualization
            
            **Backtesting**
            - Test strategies on history
            - See potential performance
            - Risk-free simulation
            - Detailed trade reports
            """)
    
    with tab3:
        st.markdown("### ❓ Frequently Asked Questions")
        
        with st.expander("What is Paper Trading?"):
            st.markdown("""
            Paper trading lets you practice trading with fake money. It's completely risk-free!
            
            - Uses real market data
            - Simulates real trades
            - No real money at risk
            - Perfect for learning
            """)
        
        with st.expander("How do I switch to real trading?"):
            st.markdown("""
            **Warning:** Only switch to real trading after you're profitable in paper trading!
            
            To switch:
            1. Make sure your Alpaca account is funded
            2. Uncheck "Paper Trading Mode" in bot configuration
            3. Confirm you understand the risks
            
            **Remember:** Real trading uses real money and you can lose it!
            """)
        
        with st.expander("What's the best strategy to use?"):
            st.markdown("""
            It depends on market conditions:
            
            - **Momentum**: Works best in trending markets (stocks going up or down strongly)
            - **Mean Reversion**: Works best in ranging markets (stocks bouncing up and down)
            - **Sentiment**: Follows the news and market mood
            - **Hybrid**: Combines multiple strategies for balance
            
            Tip: Use backtesting to see which strategy works best for your stocks!
            """)
        
        with st.expander("How often should I check the bot?"):
            st.markdown("""
            The bot runs automatically, but it's good to:
            
            - Check once or twice a day
            - Review positions weekly
            - Adjust strategy if performance is poor
            - Monitor for unusual market conditions
            
            Don't obsess over every trade - let the bot work!
            """)
        
        with st.expander("What's a good stop loss percentage?"):
            st.markdown("""
            Common stop loss settings:
            
            - **Conservative**: 3-5% (less risk, may get stopped out often)
            - **Moderate**: 5-7% (balanced approach)
            - **Aggressive**: 7-10% (more risk, more room to move)
            
            Lower volatility stocks can use tighter stops. Higher volatility stocks need wider stops.
            """)
    
    with tab4:
        st.markdown("### 🔧 Troubleshooting")
        
        st.markdown("""
        **Bot won't start:**
        - Check if your Alpaca API keys are set correctly
        - Make sure you're using paper trading credentials for practice
        - Try refreshing the page
        
        **No data loading:**
        - Check your internet connection
        - Stock market may be closed
        - Symbol might be incorrect
        
        **Trades not executing:**
        - Market hours: 9:30 AM - 4:00 PM ET Monday-Friday
        - Check if you have enough buying power
        - Verify bot is actually running (green status)
        
        **Analysis shows errors:**
        - Some stocks don't have news (try major stocks like AAPL)
        - API limits may be reached (wait a few minutes)
        - Check if symbol is correct
        """)
        
        st.markdown("---")
        st.markdown("### 💬 Need More Help?")
        st.info("This is a trading simulator. Practice with paper trading until you're consistently profitable!")
