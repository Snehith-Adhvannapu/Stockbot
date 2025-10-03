import streamlit as st
from typing import Optional, Dict

THEME_CONFIG = {
    'dark': {
        'bg_primary': '#0f1419',
        'bg_secondary': '#1a1f2e',
        'bg_tertiary': '#252b3b',
        'card_bg': 'rgba(26, 31, 46, 0.95)',
        'sidebar_bg': 'linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%)',
        'text_primary': '#e8eaed',
        'text_secondary': '#9aa0a6',
        'accent_primary': '#667eea',
        'accent_secondary': '#764ba2',
        'border': 'rgba(255, 255, 255, 0.1)',
        'hover_bg': 'rgba(102, 126, 234, 0.1)',
        'success': '#4caf50',
        'warning': '#ff9800',
        'error': '#f44336',
    },
    'light': {
        'bg_primary': '#f5f7fa',
        'bg_secondary': '#ffffff',
        'bg_tertiary': '#e8ecef',
        'card_bg': 'rgba(255, 255, 255, 0.95)',
        'sidebar_bg': 'linear-gradient(180deg, #ffffff 0%, #f5f7fa 100%)',
        'text_primary': '#1a1a2e',
        'text_secondary': '#666666',
        'accent_primary': '#667eea',
        'accent_secondary': '#764ba2',
        'border': 'rgba(0, 0, 0, 0.1)',
        'hover_bg': 'rgba(102, 126, 234, 0.1)',
        'success': '#4caf50',
        'warning': '#ff9800',
        'error': '#f44336',
    }
}

def get_theme() -> Dict[str, str]:
    """Get current theme colors based on dark mode setting"""
    dark_mode = st.session_state.get('dark_mode', True)
    return THEME_CONFIG['dark' if dark_mode else 'light']

def apply_global_styles():
    """Apply global CSS styles based on current theme"""
    theme = get_theme()
    
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {{
            font-family: 'Inter', sans-serif;
        }}
        
        .stApp {{
            background: {theme['bg_primary']};
        }}
        
        .main {{
            background: {theme['bg_primary']};
            color: {theme['text_primary']};
            animation: fadeInContent 0.3s ease-out;
        }}
        
        .block-container {{
            background: transparent;
            color: {theme['text_primary']};
            animation: fadeInContent 0.3s ease-out;
        }}
        
        @keyframes fadeInContent {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        section[data-testid="stSidebar"] {{
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            color: {theme['text_primary']} !important;
        }}
        
        p, label, .stMarkdown {{
            color: {theme['text_primary']} !important;
        }}
        
        [data-testid="stSidebar"] {{
            background: {theme['sidebar_bg']} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: {theme['text_primary']} !important;
        }}
        
        [data-testid="stSidebar"] .stMarkdown {{
            color: {theme['text_primary']} !important;
        }}
        
        [data-testid="stSidebar"] button {{
            background: {theme['bg_tertiary']} !important;
            color: {theme['text_primary']} !important;
            border: 1.5px solid {theme['border']} !important;
            border-radius: 8px;
            transition: all 0.2s ease;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}
        
        [data-testid="stSidebar"] button:hover {{
            background: {theme['bg_secondary']} !important;
            border-color: {theme['accent_primary']} !important;
            transform: translateX(3px);
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
        }}
        
        [data-testid="stSidebar"] button[kind="primary"] {{
            background: linear-gradient(135deg, {theme['accent_primary']} 0%, {theme['accent_secondary']} 100%) !important;
            color: white !important;
            border: none !important;
            font-weight: 600;
        }}
        
        [data-testid="stSidebar"] button[kind="secondary"] {{
            background: {theme['bg_tertiary']} !important;
            color: {theme['text_primary']} !important;
            border: 1.5px solid rgba(102, 126, 234, 0.3) !important;
        }}
        
        .stButton button {{
            border-radius: 10px;
            font-weight: 500;
            padding: 0.7rem 1.5rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            background: {theme['bg_tertiary']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
        }}
        
        .stButton button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            border-color: {theme['accent_primary']};
        }}
        
        .stButton button:active {{
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0,0,0,0.15);
        }}
        
        .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, {theme['accent_primary']} 0%, {theme['accent_secondary']} 100%);
            color: white;
            border: none;
        }}
        
        .stButton button[kind="primary"]:hover {{
            box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        }}
        
        .metric-card {{
            background: {theme['card_bg']};
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid {theme['border']};
            backdrop-filter: blur(10px);
        }}
        
        .stMetric {{
            background: {theme['card_bg']};
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid {theme['border']};
        }}
        
        .stMetric label {{
            color: {theme['text_secondary']} !important;
        }}
        
        .stMetric [data-testid="stMetricValue"] {{
            color: {theme['text_primary']} !important;
        }}
        
        .stDataFrame {{
            background: {theme['card_bg']};
            border-radius: 8px;
        }}
        
        .stTextInput input, .stSelectbox select, .stMultiSelect {{
            background: {theme['bg_tertiary']} !important;
            color: {theme['text_primary']} !important;
            border: 1px solid {theme['border']} !important;
        }}
        
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, {theme['accent_primary']} 0%, {theme['accent_secondary']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        [data-testid="stIconMaterial"] {{
            color: {theme['text_primary']} !important;
        }}
        
        .st-emotion-cache-rw2m0o {{
            color: {theme['text_primary']} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header():
    """Render sidebar header with logo and controls"""
    theme = get_theme()
    dark_mode = st.session_state.get('dark_mode', True)
    
    st.markdown("<div class='logo'>Algora</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("☀️" if dark_mode else "🌙", key="theme_toggle", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with col2:
        if st.button("🏠", use_container_width=True, key="nav_home"):
            st.session_state.selected_mode = None
            st.session_state.selected_page = None
            st.rerun()
    
    st.markdown("---")

def show_success(message: str):
    """Display a success message"""
    st.success(f"✅ {message}")

def show_error(message: str, exception: Optional[Exception] = None):
    """Display an error message"""
    st.error(f"❌ {message}")
    if exception and st.session_state.get('debug_mode', False):
        st.exception(exception)

def show_warning(message: str):
    """Display a warning message"""
    st.warning(f"⚠️ {message}")

def show_info(message: str):
    """Display an info message"""
    st.info(f"ℹ️ {message}")

def format_currency(amount: float) -> str:
    """Format a number as currency"""
    return f"${amount:,.2f}"

def format_percentage(value: float) -> str:
    """Format a number as percentage"""
    return f"{value:.2f}%"

def format_percentage_with_sign(value: float) -> str:
    """Format a number as percentage with + or - sign"""
    return f"{value:+.2f}%"

def create_metric_card(title: str, value: str, delta: Optional[str] = None):
    """Create a metric display card"""
    st.metric(title, value, delta)

def confirm_action(message: str, key: str) -> bool:
    """Ask user to confirm an action by clicking twice"""
    if st.session_state.get(key, False):
        return True
    else:
        st.session_state[key] = True
        show_warning(f"{message} - Click again to confirm!")
        return False

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is zero"""
    try:
        return numerator / denominator if denominator != 0 else default
    except:
        return default

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length"""
    return text[:max_length] + "..." if len(text) > max_length else text
