import streamlit as st
import json
import os

# Default user preferences
DEFAULT_PREFERENCES = {
    'theme': 'light',
    'notifications': True,
    'auto_save': True,
    'page_size': 25
}

def load_config():
    """Load configuration settings from Streamlit secrets or environment variables"""
    # Load VAPI API key from Streamlit secrets or environment variables
    vapi_api_key = st.secrets.get("VAPI_API_KEY") or os.environ.get("VAPI_API_KEY")
    vapi_phone_number_id = st.secrets.get("VAPI_PHONE_NUMBER_ID") or os.environ.get("VAPI_PHONE_NUMBER_ID")
    
    # Store in session state
    st.session_state.vapi_api_key = vapi_api_key
    st.session_state.vapi_phone_number_id = vapi_phone_number_id

def get_vapi_config():
    """Get VAPI configuration from session state"""
    return {
        'api_key': st.session_state.get("vapi_api_key", ""),
        'phone_number_id': st.session_state.get("vapi_phone_number_id", "")
    }

def validate_vapi_config(config: dict) -> tuple[bool, str]:
    """Validate VAPI configuration"""
    if not config.get('api_key'):
        return False, "VAPI_API_KEY is missing"
    if not config.get('phone_number_id'):
        return False, "VAPI_PHONE_NUMBER_ID is missing"
    return True, "Valid configuration"

def init_session_state():
    """Initialize session state with default values"""
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = DEFAULT_PREFERENCES
    
    if 'gsheets_creds' not in st.session_state:
        st.session_state.gsheets_creds = None
    
    if 'global_gsheets_creds' not in st.session_state:
        st.session_state.global_gsheets_creds = None

def get_user_preferences():
    """Get user preferences from session state"""
    return st.session_state.get('user_preferences', DEFAULT_PREFERENCES)

def save_user_preferences(preferences):
    """Save user preferences to session state"""
    st.session_state.user_preferences = preferences

def load_gsheets_config():
    """Load Google Sheets configuration from session state"""
    if 'gsheets_creds' in st.session_state:
        st.session_state.global_gsheets_creds = st.session_state.gsheets_creds

def save_gsheets_config(creds):
    """Save Google Sheets configuration to session state"""
    st.session_state.gsheets_creds = creds
    st.session_state.global_gsheets_creds = creds

def preserve_gsheets_config():
    """Preserve Google Sheets configuration across logout"""
    if 'global_gsheets_creds' in st.session_state:
        st.session_state.gsheets_creds = st.session_state.global_gsheets_creds

def clear_all_caches():
    """Clear all caches in the application"""
    cache_keys = ['sheets_cache', 'data_cache', 'sync_status']
    for key in cache_keys:
        if key in st.session_state:
            st.session_state[key] = {}

def get_gsheets_status():
    """Get Google Sheets connection status"""
    if 'global_gsheets_creds' in st.session_state:
        creds = st.session_state.global_gsheets_creds
        return {
            'connected': True,
            'client_email': creds.get('client_email', 'Unknown'),
            'project_id': creds.get('project_id', 'Unknown')
        }
    else:
        return {
            'connected': False,
            'message': "Google Sheets credentials not configured"
        }
