import streamlit as st
import pandas as pd
from datetime import datetime

from trading.backtester import Backtester
from trading.strategy_engine import MomentumStrategy, MeanReversionStrategy, SentimentBasedStrategy, HybridStrategy
from trading.risk_manager import RiskManager
from trading.market_monitor import MarketDataMonitor

def show():
    st.title("📊 Strategy Backtesting")
    st.markdown("Test your trading strategies on historical data before risking real money")
    
    st.markdown("### Step 1: Choose Your Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Which stocks to test?**")
        symbols_input = st.text_area(
            "Enter stock symbols (one per line):",
            value="AAPL\nMSFT\nGOOGL\nTSLA",
            height=100
        )
        symbols = [s.strip().upper() for s in symbols_input.split('\n') if s.strip()]
        st.caption(f"✓ Testing {len(symbols)} stocks")
        
        st.markdown("**Which strategy?**")
        strategy_type = st.selectbox(
            "Pick a strategy:",
            ["Momentum", "Mean Reversion", "Sentiment-Based", "Hybrid"],
            help="Different strategies work better in different market conditions"
        )
        
        initial_capital = st.number_input(
            "Starting money:",
            min_value=1000,
            max_value=10000000,
            value=100000,
            step=10000,
            help="How much money to start the backtest with"
        )
    
    with col2:
        st.markdown("**How far back to test?**")
        days_back = st.slider(
            "Number of days:",
            min_value=30,
            max_value=365,
            value=180,
            step=30,
            help="More days = more reliable results but slower"
        )
        st.caption(f"✓ Testing {days_back} days of history")
        
        st.markdown("**Risk settings:**")
        max_position = st.slider(
            "Max per stock (% of portfolio):",
            min_value=5,
            max_value=25,
            value=10,
            help="Don't risk more than this on any single stock"
        )
        
        stop_loss = st.slider(
            "Stop loss (%):",
            min_value=3,
            max_value=15,
            value=5,
            help="Automatically sell if a stock drops this much"
        )
        
        take_profit = st.slider(
            "Take profit (%):",
            min_value=5,
            max_value=30,
            value=10,
            help="Automatically sell when profit reaches this level"
        )
    
    if st.button("🚀 Run Backtest", type="primary", use_container_width=True):
        with st.spinner(f"Testing strategy on {days_back} days of data..."):
            try:
                monitor = MarketDataMonitor()
                
                st.info(f"📥 Downloading historical data for {len(symbols)} stocks...")
                market_data = {}
                progress_bar = st.progress(0)
                
                for i, symbol in enumerate(symbols):
                    df = monitor.get_historical_bars(symbol, timeframe='1Day', days_back=days_back)
                    if not df.empty:
                        market_data[symbol] = df
                    progress_bar.progress((i + 1) / len(symbols))
                
                progress_bar.empty()
                
                if not market_data:
                    st.error("❌ Could not get market data. Try different stocks.")
                    return
                
                st.success(f"✅ Got data for {len(market_data)} stocks")
                
                if strategy_type == "Momentum":
                    strategy = MomentumStrategy()
                elif strategy_type == "Mean Reversion":
                    strategy = MeanReversionStrategy()
                elif strategy_type == "Sentiment-Based":
                    strategy = SentimentBasedStrategy()
                else:
                    strategy = HybridStrategy([MomentumStrategy(), MeanReversionStrategy()])
                
                risk_manager = RiskManager(
                    max_position_size=max_position / 100,
                    stop_loss_pct=stop_loss / 100,
                    take_profit_pct=take_profit / 100
                )
                
                backtester = Backtester(initial_capital=initial_capital, commission=0.001)
                
                st.info("🧮 Running backtest simulation...")
                results = backtester.run_backtest(
                    strategy=strategy,
                    market_data=market_data,
                    risk_manager=risk_manager
                )
                
                st.session_state.backtest_results = results
                st.session_state.backtester = backtester
                
                st.success("✅ Backtest completed!")
                
            except Exception as e:
                st.error(f"❌ Backtest failed: {str(e)}")
                st.exception(e)
    
    if 'backtest_results' in st.session_state:
        results = st.session_state.backtest_results
        backtester = st.session_state.backtester
        
        st.markdown("---")
        st.markdown("### 🎯 Results")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_return = results['total_return']
        
        with col1:
            if total_return > 0:
                st.success(f"**Return**\n\n## +{total_return:.2f}%")
            else:
                st.error(f"**Return**\n\n## {total_return:.2f}%")
        
        with col2:
            sharpe = results['sharpe_ratio']
            st.metric("Sharpe Ratio", f"{sharpe:.2f}", help="Risk-adjusted return (higher is better)")
        
        with col3:
            win_rate = results['win_rate']
            st.metric("Win Rate", f"{win_rate:.1f}%", help="Percentage of profitable trades")
        
        with col4:
            drawdown = results['max_drawdown']
            st.metric("Max Drawdown", f"{drawdown:.1f}%", help="Biggest loss from peak")
        
        st.markdown("### 📈 Performance Chart")
        fig = backtester.plot_results()
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Money")
            st.write(f"**Started with:** ${results['initial_capital']:,.2f}")
            st.write(f"**Ended with:** ${results['final_value']:,.2f}")
            profit = results['final_value'] - results['initial_capital']
            if profit > 0:
                st.success(f"**Profit:** ${profit:,.2f}")
            else:
                st.error(f"**Loss:** ${profit:,.2f}")
        
        with col2:
            st.markdown("#### 📊 Trades")
            st.write(f"**Total trades:** {results['total_trades']}")
            st.write(f"**Winning trades:** {results['winning_trades']}")
            st.write(f"**Losing trades:** {results['losing_trades']}")
            st.write(f"**Avg win:** ${results['avg_win']:,.2f}")
            st.write(f"**Avg loss:** ${results['avg_loss']:,.2f}")
        
        with st.expander("📋 See All Trades"):
            if results['trade_details']:
                trades_df = pd.DataFrame(results['trade_details'])
                trades_df['date'] = pd.to_datetime(trades_df['date']).dt.strftime('%Y-%m-%d')
                st.dataframe(trades_df, use_container_width=True, hide_index=True)
            else:
                st.info("No completed trades")
        
        st.markdown("---")
        
        if st.button("📥 Download Report", use_container_width=True):
            report = backtester.get_summary_report()
            st.download_button(
                "Save Report",
                report,
                f"backtest_{datetime.now().strftime('%Y%m%d')}.txt",
                "text/plain"
            )
