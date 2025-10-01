import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(
    page_title="🤖 AI Stock Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def display_results(results, fundamental_weight, sentiment_weight):
    """Display comprehensive analysis results with modern card-based interface"""
    
    results_sorted = sorted(results, key=lambda x: x['overall_score'], reverse=True)
    
    st.markdown("<div class='section-spacing'>", unsafe_allow_html=True)
    st.markdown("## 🧾 Stock Analysis Results")
    st.markdown("Here are your personalized stock recommendations based on AI analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    
    buy_count = len([r for r in results_sorted if r['recommendation'] == 'BUY'])
    hold_count = len([r for r in results_sorted if r['recommendation'] == 'HOLD'])
    sell_count = len([r for r in results_sorted if r['recommendation'] == 'SELL'])
    avg_score = np.mean([r['overall_score'] for r in results_sorted])
    
    with col1:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #4CAF50, #45a049);'>
            <h2>✅ {}</h2>
            <p>BUY Recommendations</p>
        </div>
        """.format(buy_count), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #FF9800, #f57c00);'>
            <h2>⚠️ {}</h2>
            <p>HOLD Recommendations</p>
        </div>
        """.format(hold_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #f44336, #d32f2f);'>
            <h2>❌ {}</h2>
            <p>SELL Recommendations</p>
        </div>
        """.format(sell_count), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='metric-card' style='background: linear-gradient(135deg, #2196F3, #1976d2);'>
            <h2>{:.1f}</h2>
            <p>Average Score</p>
        </div>
        """.format(avg_score), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if len(results_sorted) > 1:
        fig = go.Figure()
        
        colors = ['#4CAF50' if r['recommendation'] == 'BUY' 
                 else '#FF9800' if r['recommendation'] == 'HOLD' 
                 else '#f44336' for r in results_sorted]
        
        fig.add_trace(go.Bar(
            x=[r['ticker'] for r in results_sorted],
            y=[r['overall_score'] for r in results_sorted],
            marker_color=colors,
            text=[f"{r['overall_score']:.1f}" for r in results_sorted],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="📊 Stock Performance Comparison",
            xaxis_title="Stock Ticker",
            yaxis_title="Overall Score",
            showlegend=False,
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='section-spacing'>", unsafe_allow_html=True)
    st.markdown("### 📋 Detailed Stock Analysis")
    st.markdown("Click each stock to see full analysis details")
    
    for i, result in enumerate(results_sorted):
        if result['recommendation'] == 'BUY':
            badge_color = '#4CAF50'
            badge_bg = 'linear-gradient(135deg, #4CAF50, #45a049)'
            badge_emoji = '✅'
        elif result['recommendation'] == 'HOLD':
            badge_color = '#FF9800'
            badge_bg = 'linear-gradient(135deg, #FF9800, #f57c00)'
            badge_emoji = '⚠️'
        else:
            badge_color = '#f44336'
            badge_bg = 'linear-gradient(135deg, #f44336, #d32f2f)'
            badge_emoji = '❌'
        
        with st.expander(f"#{i+1} {result['ticker']} - {result['company_name']}", expanded=(i==0)):
            
            st.markdown(f"""
            <div style='background: {badge_bg}; color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <div>
                        <h2 style='margin: 0; font-size: 1.8rem; font-weight: 700;'>{badge_emoji} {result['recommendation']}</h2>
                        <p style='margin: 8px 0 0 0; opacity: 0.9; font-size: 1.1rem;'>Overall Score: {result['overall_score']:.1f}/100</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### ⚖️ Analysis Balance")
                fund_pct = fundamental_weight
                sent_pct = sentiment_weight
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                    <div style='display: flex; height: 25px; border-radius: 12px; overflow: hidden; margin: 10px 0;'>
                        <div style='background: linear-gradient(135deg, #4CAF50, #45a049); width: {fund_pct}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: 600;'>
                            📊 {fund_pct}%
                        </div>
                        <div style='background: linear-gradient(135deg, #2196F3, #1976d2); width: {sent_pct}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 12px; font-weight: 600;'>
                            🗞️ {sent_pct}%
                        </div>
                    </div>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;'>Fundamentals vs Sentiment</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("#### 📊 Fundamental Score")
                fund_score = result.get('fundamental_score', 50)
                fund_color = '#4CAF50' if fund_score >= 70 else '#FF9800' if fund_score >= 50 else '#f44336'
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;'>
                    <h3 style='margin: 0; color: {fund_color}; font-size: 2rem;'>{fund_score:.1f}</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;'>Financial Health</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("#### 🗞️ Sentiment Score")
                sent_score = result.get('sentiment_score', 50)
                sent_color = '#4CAF50' if sent_score >= 70 else '#FF9800' if sent_score >= 50 else '#f44336'
                
                st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin: 10px 0; text-align: center;'>
                    <h3 style='margin: 0; color: {sent_color}; font-size: 2rem;'>{sent_score:.1f}</h3>
                    <p style='margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.8;'>Market Sentiment</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 💡 AI Analysis Summary")
            reasoning = result.get('reasoning', 'Analysis completed successfully')
            st.markdown(f"""
            <div style='background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px; border-left: 4px solid {badge_color}; margin: 15px 0;'>
                <p style='margin: 0; font-size: 1rem; line-height: 1.6;'>{reasoning}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        df_export = pd.DataFrame([{
            'Rank': i+1,
            'Ticker': r['ticker'],
            'Company': r['company_name'],
            'Recommendation': r['recommendation'],
            'Score': r['overall_score'],
            'PE_Ratio': r.get('pe_ratio', 'N/A'),
            'Sentiment': r.get('avg_sentiment', 'N/A')
        } for i, r in enumerate(results_sorted)])
        
        csv = df_export.to_csv(index=False)
        st.download_button(
            "📥 Download CSV",
            data=csv,
            file_name=f"stock_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        if st.button("🔄 Refresh Analysis", use_container_width=True):
            st.rerun()

def main():
    st.markdown("""
    <style>
    .hero-section {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .hero-section h1 {
        color: white;
        font-size: 4rem;
        margin: 0;
        text-shadow: 3px 3px 10px rgba(0,0,0,0.3);
        font-weight: 800;
        letter-spacing: -1px;
    }
    
    .hero-section p {
        color: rgba(255,255,255,0.95);
        font-size: 1.5rem;
        margin: 1rem 0 0 0;
        font-weight: 300;
    }
    
    .mode-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transition: all 0.4s ease;
        text-align: center;
        height: 100%;
        border: 3px solid transparent;
    }
    
    .mode-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 50px rgba(0,0,0,0.2);
        border-color: #667eea;
    }
    
    .mode-card h2 {
        font-size: 2.5rem;
        margin: 0 0 1rem 0;
        color: #2c3e50;
    }
    
    .mode-card .icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .mode-card h3 {
        color: #667eea;
        font-size: 1.8rem;
        margin: 1rem 0;
        font-weight: 600;
    }
    
    .mode-card p {
        color: #5a6c7d;
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 1rem 0;
    }
    
    .mode-card ul {
        text-align: left;
        color: #5a6c7d;
        font-size: 1rem;
        line-height: 1.8;
    }
    
    .mode-card ul li {
        margin: 0.5rem 0;
    }
    
    .metric-card {
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .metric-card h2 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
        font-weight: 500;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='hero-section'>
        <h1>🤖 AI Stock Platform</h1>
        <p>Choose your trading experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='mode-card'>
            <div class='icon'>🧠</div>
            <h3>AI Stock Advisor</h3>
            <p><strong>Get intelligent stock recommendations powered by multi-agent AI analysis</strong></p>
            <ul>
                <li>📊 <strong>Fundamental Analysis</strong> - PE, PB, ROE, financial health</li>
                <li>📰 <strong>Sentiment Analysis</strong> - News & market buzz</li>
                <li>🎯 <strong>Sector-based</strong> - Focused analysis by industry</li>
                <li>⚖️ <strong>Customizable</strong> - Balance fundamental vs sentiment</li>
                <li>💡 <strong>Explainable</strong> - Clear reasoning for each recommendation</li>
            </ul>
            <p style='margin-top: 1.5rem; font-style: italic; color: #7b1fa2;'>Perfect for investors who want AI-powered insights before making decisions</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🧠 Launch AI Stock Advisor", use_container_width=True, type="primary"):
            st.session_state.selected_mode = 'ai_advisor'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='mode-card'>
            <div class='icon'>🤖</div>
            <h3>Autonomous Trading Bot</h3>
            <p><strong>Fully automated algorithmic trading on autopilot</strong></p>
            <ul>
                <li>📈 <strong>Live Market Data</strong> - Real-time monitoring & analysis</li>
                <li>🎯 <strong>Multiple Strategies</strong> - Momentum, mean reversion, sentiment</li>
                <li>🛡️ <strong>Risk Management</strong> - Stop-loss, position sizing, drawdown protection</li>
                <li>⚡ <strong>Auto-execution</strong> - Trades executed automatically 24/7</li>
                <li>📊 <strong>Performance Dashboard</strong> - Track metrics & trade history</li>
            </ul>
            <p style='margin-top: 1.5rem; font-style: italic; color: #1976d2;'>Perfect for algorithmic traders who want hands-free automated trading</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🤖 Launch Autonomous Bot", use_container_width=True, type="primary"):
            st.session_state.selected_mode = 'auto_trading'
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("### 🌟 Why Choose Our Platform?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🔒 Secure**
        - Paper trading mode available
        - API key encryption
        - Risk management built-in
        """)
    
    with col2:
        st.markdown("""
        **⚡ Powerful**
        - Real-time market data
        - Advanced AI algorithms
        - Professional-grade strategies
        """)
    
    with col3:
        st.markdown("""
        **📊 Transparent**
        - Full trade logging
        - Performance metrics
        - Clear decision explanations
        """)

if __name__ == "__main__":
    if 'selected_mode' in st.session_state:
        if st.session_state.selected_mode == 'ai_advisor':
            from pages import ai_advisor
            ai_advisor.show()
        elif st.session_state.selected_mode == 'auto_trading':
            from pages import auto_trading
            auto_trading.show()
    else:
        main()
