import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from agents.trading_agent import TradingAgent
from trading.portfolio_analyzer import PortfolioAnalyzer

def show():
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <h1 style='font-size: 2.5rem; margin: 0;'>💼 Portfolio Manager</h1>
        <p style='color: #666; font-size: 1.1rem;'>Track and analyze your investments</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    try:
        trading_agent = TradingAgent()
        analyzer = PortfolioAnalyzer()
        
        account = trading_agent.get_account_info()
        positions = trading_agent.get_positions()
        
        if 'error' in account:
            st.error("⚠️ Cannot connect to your trading account")
            st.info("💡 Check that your Alpaca API keys are configured correctly")
            return
        
        st.markdown("### 💰 Account Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # USD to INR conversion rate
        usd_to_inr = 83.0
        
        portfolio_value_usd = float(account.get('portfolio_value', 0))
        portfolio_value_inr = portfolio_value_usd * usd_to_inr
        
        cash_usd = float(account.get('cash', 0))
        cash_inr = cash_usd * usd_to_inr
        
        buying_power_usd = float(account.get('buying_power', 0))
        buying_power_inr = buying_power_usd * usd_to_inr
        
        with col1:
            st.metric(
                "Total Portfolio",
                f"₹{portfolio_value_inr:,.2f}",
                help="Total value of cash + positions"
            )
        
        with col2:
            st.metric(
                "Available Cash",
                f"₹{cash_inr:,.2f}",
                help="Cash ready to invest"
            )
        
        with col3:
            st.metric(
                "Positions",
                len(positions),
                help="Number of stocks you own"
            )
        
        with col4:
            st.metric(
                "Buying Power",
                f"₹{buying_power_inr:,.2f}",
                help="Maximum you can invest"
            )
        
        if not positions or any('error' in p for p in positions):
            st.markdown("---")
            st.info("💡 You don't have any positions yet")
            st.markdown("""
            **Ready to start trading?**
            
            1. Go to the Trading Bot page
            2. Configure your bot settings
            3. Start the bot
            4. Your positions will appear here!
            """)
            
            if st.button("🚀 Go to Trading Bot", use_container_width=True, type="primary"):
                st.session_state.selected_page = 'auto_trading'
                st.rerun()
            
            return
        
        st.markdown("---")
        
        analysis = analyzer.analyze_portfolio(positions, account)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Portfolio Distribution")
            fig = analyzer.create_allocation_chart(positions)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Performance")
            fig = analyzer.create_performance_chart(positions)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📋 Your Positions")
        
        positions_data = []
        total_value = 0
        total_pnl = 0
        usd_to_inr = 83.0
        
        for pos in positions:
            pnl_usd = float(pos.get('unrealized_pl', 0))
            pnl_inr = pnl_usd * usd_to_inr
            pnl_pct = float(pos.get('unrealized_plpc', 0)) * 100
            
            market_value_usd = float(pos.get('market_value', 0))
            market_value_inr = market_value_usd * usd_to_inr
            
            avg_cost_usd = float(pos.get('avg_entry_price', 0))
            avg_cost_inr = avg_cost_usd * usd_to_inr
            
            current_price_usd = float(pos.get('current_price', 0))
            current_price_inr = current_price_usd * usd_to_inr
            
            total_value += market_value_inr
            total_pnl += pnl_inr
            
            positions_data.append({
                'Stock': pos.get('symbol'),
                'Shares': int(float(pos.get('qty', 0))),
                'Avg Cost': f"₹{avg_cost_inr:.2f}",
                'Current': f"₹{current_price_inr:.2f}",
                'Value': f"₹{market_value_inr:,.2f}",
                'P/L': f"₹{pnl_inr:,.2f}",
                'Return': f"{pnl_pct:+.2f}%"
            })
        
        df = pd.DataFrame(positions_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if total_pnl > 0:
                st.success(f"**Total Profit**\n\n+₹{total_pnl:,.2f}")
            elif total_pnl < 0:
                st.error(f"**Total Loss**\n\n₹{total_pnl:,.2f}")
            else:
                st.info(f"**Total P/L**\n\n₹{total_pnl:,.2f}")
        
        with col2:
            avg_return = analysis['performance_metrics']['avg_return_pct']
            st.metric("Average Return", f"{avg_return:.2f}%")
        
        with col3:
            win_rate = analysis['performance_metrics']['win_rate']
            st.metric("Win Rate", f"{win_rate:.1f}%")
        
        with col4:
            div_score = analysis['diversification_score']
            st.metric("Diversification", f"{div_score:.0f}/100")
        
        with st.expander("📊 Detailed Analysis"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Performance**")
                st.write(f"Winning Positions: {analysis['performance_metrics']['num_winners']}")
                st.write(f"Losing Positions: {analysis['performance_metrics']['num_losers']}")
                
                avg_win_usd = analysis['performance_metrics'].get('avg_win', 0)
                avg_win_inr = avg_win_usd * usd_to_inr
                st.write(f"Average Win: ₹{avg_win_inr:,.2f}")
                
                avg_loss_usd = analysis['performance_metrics'].get('avg_loss', 0)
                avg_loss_inr = avg_loss_usd * usd_to_inr
                st.write(f"Average Loss: ₹{avg_loss_inr:,.2f}")
            
            with col2:
                st.markdown("**Risk Metrics**")
                st.write(f"Top 3 Concentration: {analysis['concentration_risk']['top_3_concentration']:.1f}%")
                st.write(f"Herfindahl Index: {analysis['concentration_risk']['herfindahl_index']:.4f}")
                
                if analysis['concentration_risk']['herfindahl_index'] > 0.25:
                    st.warning("⚠️ High concentration - consider diversifying")
                else:
                    st.success("✅ Good diversification")
        
        st.markdown("---")
        st.markdown("### ⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Export Portfolio", use_container_width=True):
                csv = df.to_csv(index=False)
                st.download_button(
                    "Download CSV",
                    csv,
                    f"portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📈 View Charts", use_container_width=True):
                st.session_state.selected_page = 'charts'
                st.rerun()
        
        with col3:
            if st.button("⚠️ Close All", use_container_width=True):
                if st.session_state.get('confirm_close_all'):
                    result = trading_agent.close_all_positions()
                    if result.get('success'):
                        st.success(f"✅ Closed {result.get('closed_count', 0)} positions")
                        st.session_state.confirm_close_all = False
                        st.rerun()
                    else:
                        st.error(f"Failed: {result.get('error')}")
                else:
                    st.session_state.confirm_close_all = True
                    st.warning("⚠️ Click again to confirm!")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("💡 Try refreshing the page or check your connection")
