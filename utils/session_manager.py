import streamlit as st
from typing import Any, Optional

class SessionManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get a value from session state"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any):
        """Set a value in session state"""
        st.session_state[key] = value
    
    @staticmethod
    def delete(key: str):
        """Delete a key from session state"""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def has(key: str) -> bool:
        """Check if a key exists in session state"""
        return key in st.session_state
    
    @staticmethod
    def clear_all():
        """Clear all session state"""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
    
    @staticmethod
    def init_defaults():
        """Initialize default session state values"""
        defaults = {
            'selected_mode': None,
            'selected_page': None,
            'trading_bot_initialized': False,
            'debug_mode': False
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
