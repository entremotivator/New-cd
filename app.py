import streamlit as st
from pathlib import Path
from login import show_login
from sidebar import show_sidebar
from utils.config import load_config, init_session_state

# Configure Streamlit page
st.set_page_config(
    page_title="Business Management Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main app logic
def main():
    load_css()
    load_config()
    init_session_state()

    # Check login via JSON upload
    if not st.session_state.get("logged_in", False):
        show_login()
    else:
        show_sidebar()

        # Set default page
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Dashboard"

        # Define available pages
        page_mapping = {
            "Dashboard": "pages/1_Dashboard.py",
            "Calendar": "pages/2_Calendar.py",
            "Invoices": "pages/3_Invoices.py",
            "Customers": "pages/4_Customers.py",
            "Appointments": "pages/5_Appointments.py",
            "Pricing": "pages/6_Pricing.py",
            "AI Chat": "pages/7_Super_Chat.py",
            "Voice Calls": "pages/8_AI_Caller.py",
            "Call Center": "pages/9_Call_Center.py",
            "Project Management": "pages/Project_Management.py",
            "Settings": "pages/Settings.py"
        }

        selected_page = st.session_state.get("current_page")

        if selected_page in page_mapping:
            try:
                st.switch_page(page_mapping[selected_page])
            except Exception as e:
                st.error(f"❌ Failed to switch page to {selected_page}: {e}")
                st.warning("⚠️ Showing fallback dashboard.")
                st.title("📊 Dashboard (Fallback)")
                st.info("Use the sidebar to select a valid page.")
        else:
            st.warning("⚠️ Page not found. Showing fallback dashboard.")
            st.title("📊 Dashboard (Fallback)")
            st.info("Use the sidebar to select a valid page.")

if __name__ == "__main__":
    main()
