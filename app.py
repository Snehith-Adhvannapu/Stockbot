import streamlit as st

st.set_page_config(
    page_title="Stock Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    .stApp {
        background: transparent;
    }
    
    .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem;
        backdrop-filter: blur(10px);
    }
    
    .stButton button {
        border-radius: 10px;
        font-weight: 500;
        padding: 0.7rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    div[data-testid="stSidebar"] button {
        margin-bottom: 0.5rem;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    div[data-testid="stSidebar"] button:hover {
        transform: translateX(5px);
    }
    
    div[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    h1 {
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .mode-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        height: 100%;
    }
    
    .mode-card:hover {
        transform: translateY(-10px);
        border-color: #667eea;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .feature-box {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .feature-box:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main landing page"""
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3.5rem; margin: 0;'>📈 Stock Trading Platform</h1>
        <p style='font-size: 1.3rem; color: #666; margin-top: 0.5rem;'>
            AI-Powered Trading Made Simple
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("""
        <div class='mode-card'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🧠</div>
            <h2 style='color: #667eea; margin-bottom: 1rem;'>AI Stock Advisor</h2>
            <p style='font-size: 1.1rem; line-height: 1.6; color: #555;'>
                Get intelligent stock recommendations powered by AI sentiment analysis 
                and fundamental research. Make smarter investment decisions.
            </p>
            <p style='font-weight: 600; color: #667eea; margin-top: 1rem;'>
                Perfect for: Research & Analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Launch AI Advisor →", type="primary", use_container_width=True, key="start_ai"):
            st.session_state.selected_mode = 'ai_advisor'
            st.session_state.selected_page = 'ai_advisor'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='mode-card'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🤖</div>
            <h2 style='color: #764ba2; margin-bottom: 1rem;'>Autonomous Trading Bot</h2>
            <p style='font-size: 1.1rem; line-height: 1.6; color: #555;'>
                Set up a fully automated trading system that monitors markets and 
                executes trades 24/7. Let AI handle the trading for you.
            </p>
            <p style='font-weight: 600; color: #764ba2; margin-top: 1rem;'>
                Perfect for: Hands-Off Trading
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Launch Trading Bot →", type="primary", use_container_width=True, key="start_bot"):
            st.session_state.selected_mode = 'auto_trading'
            st.session_state.selected_page = 'dashboard'
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h2 style='color: #333;'>✨ Everything You Need</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='feature-box'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>📊</div>
            <h3 style='color: #667eea;'>Real-time Data</h3>
            <ul style='text-align: left; color: #555;'>
                <li>Live stock prices</li>
                <li>Market news updates</li>
                <li>Sentiment analysis</li>
                <li>Technical indicators</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-box'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🎯</div>
            <h3 style='color: #667eea;'>Smart Analysis</h3>
            <ul style='text-align: left; color: #555;'>
                <li>AI recommendations</li>
                <li>Pattern detection</li>
                <li>Strategy backtesting</li>
                <li>Market scanning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-box'>
            <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🛡️</div>
            <h3 style='color: #667eea;'>Risk Management</h3>
            <ul style='text-align: left; color: #555;'>
                <li>Paper trading mode</li>
                <li>Automated stop-loss</li>
                <li>Position sizing</li>
                <li>Portfolio tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'selected_mode' not in st.session_state:
        st.session_state.selected_mode = None
    
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = None
    
    mode = st.session_state.selected_mode
    
    if mode:
        st.sidebar.markdown("## 🧭 Navigation")
        
        if st.sidebar.button("🏠 Home", use_container_width=True, type="primary", key="nav_home"):
            st.session_state.selected_mode = None
            st.session_state.selected_page = None
            st.rerun()
        
        st.sidebar.markdown("---")
        
        if mode == 'ai_advisor':
            st.sidebar.markdown("### 🧠 AI Advisor")
            
            from pages import ai_advisor
            ai_advisor.show()
        
        elif mode == 'auto_trading':
            st.sidebar.markdown("### 🤖 Trading Platform")
            
            current_page = st.session_state.get('selected_page', 'dashboard')
            
            pages = {
                "📊 Dashboard": 'dashboard',
                "🤖 Trading Bot": 'auto_trading',
                "💼 Portfolio": 'portfolio',
                "👀 Watchlist": 'watchlist',
                "📈 Charts": 'charts',
                "🔍 Scanner": 'scanner',
                "🔎 Patterns": 'patterns',
                "📊 Backtest": 'backtesting',
                "📚 Help": 'help'
            }
            
            for label, page_id in pages.items():
                button_type = "primary" if current_page == page_id else "secondary"
                if st.sidebar.button(label, use_container_width=True, type=button_type, key=f"nav_{page_id}"):
                    st.session_state.selected_page = page_id
                    st.rerun()
            
            page = st.session_state.get('selected_page', 'dashboard')
            
            if page == 'dashboard':
                from pages import dashboard
                dashboard.show()
            elif page == 'auto_trading':
                from pages import auto_trading
                auto_trading.show()
            elif page == 'portfolio':
                from pages import portfolio_manager
                portfolio_manager.show()
            elif page == 'backtesting':
                from pages import backtesting
                backtesting.show()
            elif page == 'scanner':
                from pages import market_scanner
                market_scanner.show()
            elif page == 'charts':
                from pages import charting
                charting.show()
            elif page == 'patterns':
                from pages import pattern_scanner
                pattern_scanner.show()
            elif page == 'watchlist':
                from pages import watchlist
                watchlist.show()
            elif page == 'help':
                from pages import help
                help.show()
            else:
                from pages import dashboard
                dashboard.show()
    else:
        main()
