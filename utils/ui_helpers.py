import streamlit as st
from typing import Optional

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
