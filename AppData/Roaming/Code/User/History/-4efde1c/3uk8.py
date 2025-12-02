# app.py - UPDATED WITH LOGIN SYSTEM
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import plotly.graph_objects as go
import PyPDF2
import io
from docx import Document

# Import database and email configuration
try:
    from database import *
    DB_ENABLED = True
except ImportError:
    st.error("❌ database.py file not found.")
    DB_ENABLED = False

try:
    from email_config import get_email_config, validate_email_config
    EMAIL_CONFIG = get_email_config()
    EMAIL_ENABLED = True
except ImportError:
    st.error("❌ email_config.py file not found.")
    EMAIL_ENABLED = False
    EMAIL_CONFIG = {}

# Initialize users table
if DB_ENABLED:
    init_users_table()

# Ultra Premium Theme CSS with Login Animations
def load_ultra_premium_css():
    st.markdown("""
    <style>
    /* Ultra Premium Theme */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
        --bg-sidebar: #1a1a1a;
        --accent-primary: #00D4AA;
        --accent-secondary: #0099FF;
        --accent-gradient: linear-gradient(135deg, #00D4AA, #0099FF);
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --text-muted: #AAAAAA;
        --border: #333333;
        --input-bg: #2D2D2D;
        --input-text: #FFFFFF;
        --success: #00C853;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 16px 48px rgba(0, 212, 170, 0.2);
    }
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Login Page Specific Styles */
    .login-container {
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 50%, #2D2D2D 100%);
        position: relative;
        overflow: hidden;
    }
    
    .login-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(0, 212, 170, 0.1) 0%, transparent 70%);
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    .glowing-card {
        background: rgba(26, 26, 26, 0.95);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(0, 212, 170, 0.1),
            0 0 50px rgba(0, 212, 170, 0.2);
        animation: glow 3s ease-in-out infinite alternate;
        position: relative;
        z-index: 2;
        max-width: 450px;
        width: 90%;
    }
    
    @keyframes glow {
        from {
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(0, 212, 170, 0.1),
                0 0 50px rgba(0, 212, 170, 0.2);
        }
        to {
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.4),
                0 0 0 1px rgba(0, 212, 170, 0.2),
                0 0 60px rgba(0, 212, 170, 0.4);
        }
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .animated-logo {
        font-size: 4rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: bounce 2s ease-in-out infinite;
        display: inline-block;
    }
    
    @keyframes bounce {
        0%, 100% { transform: scale(1) rotate(0deg); }
        50% { transform: scale(1.1) rotate(5deg); }
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 10px 0;
    }
    
    .login-subtitle {
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }
    
    .login-input {
        background: rgba(45, 45, 45, 0.8) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 15px 20px !important;
        margin: 10px 0 !important;
        transition: all 0.3s ease !important;
    }
    
    .login-input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.3) !important;
        transform: translateY(-2px);
    }
    
    .login-button {
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 15px !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        margin: 20px 0 10px 0 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .login-button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 30px rgba(0, 212, 170, 0.4) !important;
    }
    
    .toggle-form {
        text-align: center;
        margin-top: 20px;
        color: var(--text-secondary);
    }
    
    .toggle-form a {
        color: var(--accent-primary);
        text-decoration: none;
        font-weight: 600;
        cursor: pointer;
    }
    
    .floating-particles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1;
    }
    
    .particle {
        position: absolute;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        border-radius: 50%;
        animation: float-particle 15s infinite linear;
    }
    
    @keyframes float-particle {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .glowing-card {
            margin: 20px;
            padding: 30px 20px;
        }
        
        .login-title {
            font-size: 2rem;
        }
        
        .animated-logo {
            font-size: 3rem;
        }
    }
    
    /* Rest of your existing CSS styles... */
    /* [Include all your existing CSS styles from previous version here] */
    
    </style>
    """, unsafe_allow_html=True)

def create_particles():
    """Create floating particles for background"""
    particles_html = "<div class='floating-particles'>"
    for i in range(15):
        size = random.randint(2, 6)
        left = random.randint(0, 100)
        delay = random.randint(0, 15)
        duration = random.randint(10, 20)
        particles_html += f"""
        <div class='particle' style='
            width: {size}px;
            height: {size}px;
            left: {left}%;
            animation-delay: {delay}s;
            animation-duration: {duration}s;
        '></div>
        """
    particles_html += "</div>"
    return particles_html

def show_login_page():
    """Show the animated login/signup page"""
    
    # Initialize session state for login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    # If user is logged in, don't show login page
    if st.session_state.logged_in:
        return True
    
    # Apply login page styles
    load_ultra_premium_css()
    
    # Create login container
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    
    # Add floating particles
    st.markdown(create_particles(), unsafe_allow_html=True)
    
    # Login/Signup Card
    with st.container():
        st.markdown("<div class='glowing-card'>", unsafe_allow_html=True)
        
        # Animated Logo and Title
        st.markdown("""
        <div class='login-logo'>
            <div class='animated-logo'>🚀</div>
            <h1 class='login-title'>SmartHire.AI</h1>
            <p class='login-subtitle'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.show_signup:
            # LOGIN FORM
            with st.form("login_form"):
                st.markdown("### 🔐 Welcome Back")
                
                username = st.text_input(
                    "👤 Username",
                    placeholder="Enter your username",
                    key="login_username"
                )
                
                password = st.text_input(
                    "🔒 Password", 
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                
                login_button = st.form_submit_button(
                    "🚀 Login to Dashboard",
                    use_container_width=True
                )
                
                if login_button:
                    if username and password:
                        if DB_ENABLED:
                            user = authenticate_user(username, password)
                            if user:
                                st.session_state.logged_in = True
                                st.session_state.current_user = user
                                st.success(f"🎉 Welcome back, {user['full_name']}!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Invalid username or password")
                        else:
                            st.error("❌ Database not available. Using demo mode.")
                            # Demo login
                            if username == "demo" and password == "demo":
                                st.session_state.logged_in = True
                                st.session_state.current_user = {
                                    'id': 1,
                                    'username': 'demo',
                                    'full_name': 'Demo User',
                                    'email': 'demo@smarthire.ai',
                                    'company': 'TechCorp'
                                }
                                st.success("🎉 Demo login successful!")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("❌ Demo credentials: username='demo', password='demo'")
                    else:
                        st.error("❌ Please fill in all fields")
            
            # Signup toggle
            st.markdown("""
            <div class='toggle-form'>
                Don't have an account? <a onclick="toggleSignup()">Sign up here</a>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript for toggle
            st.markdown("""
            <script>
            function toggleSignup() {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: 'show_signup'
                }, '*');
            }
            </script>
            """, unsafe_allow_html=True)
            
            # Handle the toggle
            if st.button("Sign up here", key="signup_toggle", use_container_width=True):
                st.session_state.show_signup = True
                st.rerun()
        
        else:
            # SIGNUP FORM
            with st.form("signup_form"):
                st.markdown("### 🌟 Create Account")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input(
                        "👤 Full Name",
                        placeholder="Enter your full name",
                        key="signup_name"
                    )
                    
                    username = st.text_input(
                        "👤 Username",
                        placeholder="Choose a username",
                        key="signup_username"
                    )
                
                with col2:
                    email = st.text_input(
                        "📧 Email Address",
                        placeholder="Enter your email",
                        key="signup_email"
                    )
                    
                    company = st.text_input(
                        "🏢 Company",
                        placeholder="Your company name",
                        key="signup_company"
                    )
                
                col3, col4 = st.columns(2)
                
                with col3:
                    password = st.text_input(
                        "🔒 Password",
                        type="password",
                        placeholder="Create a password",
                        key="signup_password"
                    )
                
                with col4:
                    confirm_password = st.text_input(
                        "🔒 Confirm Password",
                        type="password",
                        placeholder="Confirm your password",
                        key="signup_confirm_password"
                    )
                
                role = st.selectbox(
                    "💼 Your Role",
                    ["Recruiter", "Hiring Manager", "HR Professional", "Team Lead", "Other"],
                    key="signup_role"
                )
                
                signup_button = st.form_submit_button(
                    "🚀 Create Account",
                    use_container_width=True
                )
                
                if signup_button:
                    if not all([full_name, username, email, password, confirm_password]):
                        st.error("❌ Please fill in all required fields")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match")
                    elif len(password) < 6:
                        st.error("❌ Password must be at least 6 characters")
                    else:
                        if DB_ENABLED:
                            # Check if username or email exists
                            if check_username_exists(username):
                                st.error("❌ Username already exists")
                            elif check_email_exists(email):
                                st.error("❌ Email already registered")
                            else:
                                user_id = create_user(username, email, password, full_name, company, role)
                                if user_id:
                                    st.success("🎉 Account created successfully! Please login.")
                                    st.session_state.show_signup = False
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to create account")
                        else:
                            st.error("❌ Database not available. Cannot create account.")
            
            # Login toggle
            st.markdown("""
            <div class='toggle-form'>
                Already have an account? <a onclick="toggleLogin()">Login here</a>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript for toggle
            st.markdown("""
            <script>
            function toggleLogin() {
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: 'show_login'
                }, '*');
            }
            </script>
            """, unsafe_allow_html=True)
            
            # Handle the toggle
            if st.button("Login here", key="login_toggle", use_container_width=True):
                st.session_state.show_signup = False
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close glowing-card
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close login-container
    
    return False

def show_user_profile():
    """Show user profile in sidebar"""
    if st.session_state.logged_in and st.session_state.current_user:
        user = st.session_state.current_user
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Profile")
        
        st.sidebar.markdown(f"""
        **Name:** {user['full_name']}  
        **Username:** {user['username']}  
        **Email:** {user['email']}  
        **Company:** {user.get('company', 'Not specified')}  
        **Role:** {user.get('role', 'Not specified')}
        """)
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.rerun()

# [REST OF YOUR EXISTING FUNCTIONS REMAIN THE SAME]
# include all your existing functions like:
# extract_text_from_pdf, extract_text_from_docx, extract_info_from_resume,
# send_real_email, show_success_popup, create_trend_chart, get_ai_questions,
# show_dashboard, show_resume_screening, show_interview_prep, show_jd_generator,
# show_candidates, show_analytics

def main():
    st.set_page_config(
        page_title="SmartHire AI - Premium",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check login status
    if not show_login_page():
        return  # Stop execution if not logged in
    
    # User is logged in, show main application
    load_ultra_premium_css()
    
    # Initialize session states (same as before)
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = {}
    if 'candidates' not in st.session_state:
        st.session_state.candidates = []
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""
    if 'jd_created' not in st.session_state:
        st.session_state.jd_created = False
    if 'ai_questions' not in st.session_state:
        st.session_state.ai_questions = []
    
    # Show user profile in sidebar
    show_user_profile()
    
    # [REST OF YOUR MAIN FUNCTION REMAINS THE SAME]
    # Include your existing sidebar and main content logic

if __name__ == "__main__":
    main()