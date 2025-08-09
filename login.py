import streamlit as st
import json
from datetime import datetime
from utils.auth import authenticate_user, create_user_session, hash_password
from utils.config import load_gsheets_config, save_gsheets_config

def show_login():
    """Display login form and handle authentication"""
    st.title("🔑 Login")
    st.markdown("Welcome to the Business Management Suite. Please log in to continue.")

    # Load Google Sheets configuration
    load_gsheets_config()

    # Display Google Sheets configuration
    with st.expander("⚙️ Google Sheets Configuration", expanded=False):
        st.info("Configure your Google Sheets credentials to enable live data sync.")
        
        # File uploader for Google Sheets credentials
        gsheets_file = st.file_uploader(
            "Upload Google Service Account JSON",
            type=['json'],
            help="Upload your Google Service Account JSON file to connect to Google Sheets."
        )
        
        # Load credentials from file
        if gsheets_file is not None:
            try:
                gsheets_creds = json.load(gsheets_file)
                st.session_state.gsheets_creds = gsheets_creds
                st.success("✅ Google Sheets credentials loaded successfully!")
                
                # Save credentials to session state
                save_gsheets_config(gsheets_creds)
                
                # Store credentials globally for all pages
                st.session_state.global_gsheets_creds = gsheets_creds
                
            except json.JSONDecodeError:
                st.error("❌ Invalid JSON format. Please upload a valid Google Service Account JSON file.")
            except Exception as e:
                st.error(f"❌ Error loading Google Sheets credentials: {str(e)}")
        
        # Display current configuration
        if st.session_state.get('gsheets_creds'):
            st.write("Current Google Sheets Configuration:")
            st.json(st.session_state.gsheets_creds)
        else:
            st.info("No Google Sheets credentials configured.")

    # Login form
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember me", value=True)
        submitted = st.form_submit_button("Login")

        if submitted:
            # Authenticate user
            auth_result = authenticate_user(email, password)
            
            if auth_result["success"]:
                # Create user session
                if create_user_session(auth_result["user"], remember_me):
                    st.success(auth_result["message"])
                    st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.last_login = st.session_state.login_time
                    st.session_state.user_name = auth_result["user"]["name"]
                    st.session_state.user_email = auth_result["user"]["email"]
                    st.session_state.user_role = auth_result["user"]["role"]
                    st.session_state.current_page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Failed to create user session.")
            else:
                st.error(auth_result["message"])
