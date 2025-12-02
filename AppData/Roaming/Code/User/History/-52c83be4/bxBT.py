# login_page.py - SIMPLE WORKING VERSION
import streamlit as st
import time

DEMO_CREDENTIALS = {
    "admin": "admin123", 
    "hr": "hr123",
    "recruiter": "recruiter123"
}

def show_login_page():
    """Show a simple but beautiful login page"""
    
    # Custom CSS for login page
    st.markdown("""
    <style>
    .login-container {
        background: #0A0A0A;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
    }
    .login-card {
        background: #1A1A1A;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #333;
        box-shadow: 0 20px 40px rgba(0, 212, 170, 0.2);
        max-width: 400px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create centered layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; margin-bottom: 30px;'>
            <h1 style='font-size: 3rem; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🚀</h1>
            <h1 style='background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 10px 0;'>SmartHire AI</h1>
            <p style='color: #E0E0E0;'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        with st.form("login_form"):
            st.markdown("### 🔐 Sign In")
            
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")
            
            login_btn = st.form_submit_button("🚀 Sign In", use_container_width=True)
            
            if login_btn:
                if username in DEMO_CREDENTIALS and password == DEMO_CREDENTIALS[username]:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.success(f"Welcome {username}! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        
        # Demo info
        st.info("**Demo Accounts:** admin/admin123, hr/hr123, recruiter/recruiter123")

def check_authentication():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated