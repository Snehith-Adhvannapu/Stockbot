import streamlit as st
from dotenv import load_dotenv
from utils.ui_helpers import apply_global_styles, render_sidebar_header, get_theme

# Load environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Stock Trading Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="auto"
)

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

apply_global_styles()

def main():
    """Main landing page"""
    theme = get_theme()
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <div class='logo' style='font-size: 2rem;'>Algora</div>
        <h1 style='font-size: 2.5rem; margin: 0;'>Stock Trading Platform</h1>
        <p style='font-size: 1.2rem; margin-top: 0.5rem;'>
            AI-Powered Trading Made Simple
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown(f"""
        <div style='background: {theme['card_bg']}; border-radius: 15px; padding: 2rem; 
             text-align: center; border: 2px solid {theme['border']}; 
             transition: all 0.3s ease; height: 100%;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🧠</div>
            <h2 style='color: #667eea; margin-bottom: 1rem;'>AI Stock Advisor</h2>
            <p style='font-size: 1.1rem; line-height: 1.6; color: {theme['text_secondary']};'>
                Get intelligent stock recommendations powered by AI sentiment analysis 
                and fundamental research. Make smarter investment decisions.
            </p>
            <p style='font-weight: 600; color: #667eea; margin-top: 1rem;'>
                Perfect for: Research & Analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Launch AI Advisor", type="primary", use_container_width=True, key="start_ai"):
            st.session_state.selected_mode = 'ai_advisor'
            st.session_state.selected_page = 'ai_advisor'
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div style='background: {theme['card_bg']}; border-radius: 15px; padding: 2rem; 
             text-align: center; border: 2px solid {theme['border']}; 
             transition: all 0.3s ease; height: 100%;'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
            <h2 style='color: #764ba2; margin-bottom: 1rem;'>Autonomous Trading Bot</h2>
            <p style='font-size: 1.1rem; line-height: 1.6; color: {theme['text_secondary']};'>
                Set up a fully automated trading system that monitors markets and 
                executes trades 24/7. Let AI handle the trading for you.
            </p>
            <p style='font-weight: 600; color: #764ba2; margin-top: 1rem;'>
                Perfect for: Hands-Off Trading
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Launch Trading Bot", type="primary", use_container_width=True, key="start_bot"):
            st.session_state.selected_mode = 'auto_trading'
            st.session_state.selected_page = 'dashboard'
            st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h2>Platform Features</h2>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='background: {theme['card_bg']}; border-radius: 12px; padding: 1.5rem; 
             margin: 0.5rem 0; border: 1px solid {theme['border']}; transition: all 0.2s ease;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📊</div>
            <h3 style='color: #667eea;'>Real-time Data</h3>
            <ul style='text-align: left; color: {theme['text_secondary']};'>
                <li>Live stock prices</li>
                <li>Market news updates</li>
                <li>Sentiment analysis</li>
                <li>Technical indicators</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='background: {theme['card_bg']}; border-radius: 12px; padding: 1.5rem; 
             margin: 0.5rem 0; border: 1px solid {theme['border']}; transition: all 0.2s ease;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
            <h3 style='color: #667eea;'>Smart Analysis</h3>
            <ul style='text-align: left; color: {theme['text_secondary']};'>
                <li>AI recommendations</li>
                <li>Pattern detection</li>
                <li>Strategy backtesting</li>
                <li>Market scanning</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='background: {theme['card_bg']}; border-radius: 12px; padding: 1.5rem; 
             margin: 0.5rem 0; border: 1px solid {theme['border']}; transition: all 0.2s ease;'>
            <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🛡️</div>
            <h3 style='color: #667eea;'>Risk Management</h3>
            <ul style='text-align: left; color: {theme['text_secondary']};'>
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
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            transform: translateX(0) !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        section[data-testid="stSidebar"] {
            transform: translateX(0) !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stAppViewContainer"] {
            transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .main {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .block-container {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        with st.sidebar:
            render_sidebar_header()
        
        if mode == 'ai_advisor':
            st.sidebar.markdown("### AI Advisor")
            
            from pages import ai_advisor
            ai_advisor.show()
        
        elif mode == 'auto_trading':
            st.sidebar.markdown("### Trading Platform")
            
            current_page = st.session_state.get('selected_page', 'dashboard')
            
            pages = {
                "📊 Dashboard": 'dashboard',
                "🤖 Trading Bot": 'auto_trading',
                "💼 Portfolio": 'portfolio',
                "👁️ Watchlist": 'watchlist',
                "📈 Charts": 'charts',
                "🔍 Scanner": 'scanner',
                "🎯 Patterns": 'patterns',
                "⏮️ Backtest": 'backtesting',
                "❓ Help": 'help'
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
        st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            transform: translateX(-100%) !important;
            opacity: 0 !important;
            pointer-events: none !important;
            position: fixed !important;
        }
        [data-testid="stSidebarNav"] {
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"] {
            transform: translateX(-100%) !important;
            opacity: 0 !important;
            pointer-events: none !important;
            position: fixed !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            transition: margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .main {
            margin-left: 0 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        .block-container {
            max-width: 100% !important;
            padding-left: 5rem !important;
            padding-right: 5rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        dark_mode = st.session_state.get('dark_mode', True)
        
        col_spacer, col_button = st.columns([20, 1])
        with col_button:
            if st.button("☀️" if dark_mode else "🌙", key="theme_toggle_main"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        main()
