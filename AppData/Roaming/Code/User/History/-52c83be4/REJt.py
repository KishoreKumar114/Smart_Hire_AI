# login_page.py - Premium Login Page for SmartHire AI
import streamlit as st
import time

# Demo credentials
DEMO_CREDENTIALS = {
    "admin": "admin123", 
    "hr": "hr123",
    "recruiter": "recruiter123"
}

def load_login_css():
    """Load premium CSS styles for login page"""
    st.markdown("""
    <style>
    /* Ultra Premium Login Theme */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
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
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main app background */
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Login Page Container */
    .login-main-container {
        min-height: 100vh;
        background: var(--bg-primary);
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        z-index: 9999;
    }
    
    /* Animated Background Rings */
    .ring-container {
        position: absolute;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    
    .ring {
        position: relative;
        width: 500px;
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .ring i {
        position: absolute;
        inset: 0;
        border: 2px solid #fff;
        transition: 0.5s;
    }
    
    .ring i:nth-child(1) {
        border-radius: 38% 62% 63% 37% / 41% 44% 56% 59%;
        animation: animate 6s linear infinite;
    }
    
    .ring i:nth-child(2) {
        border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
        animation: animate 4s linear infinite;
    }
    
    .ring i:nth-child(3) {
        border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
        animation: animate2 10s linear infinite;
    }
    
    .ring:hover i {
        border: 6px solid var(--clr);
        filter: drop-shadow(0 0 20px var(--clr));
    }
    
    @keyframes animate {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    @keyframes animate2 {
        0% {
            transform: rotate(360deg);
        }
        100% {
            transform: rotate(0deg);
        }
    }
    
    /* Login Form Container */
    .login-form-container {
        position: relative;
        z-index: 1000;
        width: 100%;
        max-width: 450px;
        padding: 20px;
    }
    
    /* Logo Styles */
    .login-logo {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .login-logo-icon {
        font-size: 4rem !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        display: block;
    }
    
    .login-logo-text {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
        line-height: 1.2;
    }
    
    .login-logo-subtext {
        font-size: 1rem !important;
        color: var(--text-secondary) !important;
        margin: 0.5rem 0 0 0 !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
    }
    
    /* Form Card */
    .login-card {
        background: rgba(26, 26, 26, 0.95);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 20px;
        padding: 40px 30px;
        backdrop-filter: blur(10px);
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    }
    
    .login-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 212, 170, 0.3);
    }
    
    /* Form Title */
    .form-title {
        text-align: center;
        color: var(--text-primary);
        font-size: 1.8em;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .form-subtitle {
        text-align: center;
        color: var(--text-secondary);
        margin-bottom: 30px;
        font-size: 1em;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextInput>div>div>input:focus {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.3) !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Login Button */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 24px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px rgba(0, 212, 170, 0.4) !important;
    }
    
    /* Demo Credentials */
    .demo-credentials {
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 12px;
        padding: 20px;
        margin-top: 25px;
        text-align: center;
    }
    
    .demo-credentials h4 {
        color: var(--accent-primary);
        margin-bottom: 15px;
        font-size: 1.1em;
    }
    
    .demo-credentials p {
        color: var(--text-secondary);
        font-size: 0.9em;
        margin: 8px 0;
        line-height: 1.4;
    }
    
    /* Label Styling */
    .stTextInput label, .stTextInput label p {
        color: var(--text-primary) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* Success Message */
    .stSuccess {
        background: rgba(0, 200, 83, 0.1) !important;
        border: 1px solid rgba(0, 200, 83, 0.3) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    /* Error Message */
    .stError {
        background: rgba(255, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 0, 0, 0.3) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    /* Warning Message */
    .stWarning {
        background: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    
    /* Hide all Streamlit elements when login is shown */
    .login-main-container ~ * {
        display: none !important;
    }
    
    /* Ensure form container is properly positioned */
    .stForm {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Center the form content */
    .centered-form {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

def show_login_page():
    """Show the premium login page"""
    
    # Load CSS
    load_login_css()
    
    # Main login container - Complete HTML structure
    st.markdown("""
    <div class="login-main-container">
        <!-- Animated Background Rings -->
        <div class="ring-container">
            <div class="ring">
                <i style="--clr:#00ff0a;"></i>
                <i style="--clr:#ff0057;"></i>
                <i style="--clr:#fffd44;"></i>
            </div>
        </div>
        
        <!-- Login Form Container -->
        <div class="login-form-container">
            <div class="login-logo">
                <div class="login-logo-icon">🚀</div>
                <div class="login-logo-text">SmartHire AI</div>
                <div class="login-logo-subtext">Premium Recruitment Platform</div>
            </div>
            
            <div class="login-card">
                <div class="form-title">Welcome Back</div>
                <div class="form-subtitle">Sign in to access your recruitment dashboard</div>
                
                <!-- This is where Streamlit form will be injected -->
                <div id="streamlit-form-container"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Use columns to center the form content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create the actual login form using Streamlit
        with st.form("login_form", clear_on_submit=True):
            st.markdown('<div class="centered-form">', unsafe_allow_html=True)
            
            # Username field
            username = st.text_input(
                "**👤 Username**",
                placeholder="Enter your username",
                key="login_username"
            )
            
            # Password field
            password = st.text_input(
                "**🔑 Password**",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            # Login button
            login_button = st.form_submit_button(
                "🚀 Sign In to SmartHire AI",
                use_container_width=True
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Form submission handling
            if login_button:
                if username and password:
                    if username in DEMO_CREDENTIALS and password == DEMO_CREDENTIALS[username]:
                        # Successful login
                        st.session_state.authenticated = True
                        st.session_state.show_login = False
                        st.session_state.current_user = username
                        st.success(f"✅ Welcome back, {username}! Redirecting...")
                        
                        # Add a small delay for better UX
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password.")
        
        # Demo credentials section
        st.markdown("""
        <div class="demo-credentials">
            <h4>🎯 Demo Credentials</h4>
            <p><strong>👤 Username:</strong> admin | <strong>🔑 Password:</strong> admin123</p>
            <p><strong>👤 Username:</strong> hr | <strong>🔑 Password:</strong> hr123</p>
            <p><strong>👤 Username:</strong> recruiter | <strong>🔑 Password:</strong> recruiter123</p>
        </div>
        """, unsafe_allow_html=True)

def check_authentication():
    """Check if user is authenticated and initialize session state if needed"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'show_login' not in st.session_state:
        st.session_state.show_login = True
    if 'current_user' not in st.session_state:
        st.session_state.current_user = "Guest"
    
    return st.session_state.authenticated

# For testing the login page independently
if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        show_login_page()
    else:
        st.success(f"Welcome {st.session_state.current_user}! You are logged in.")
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()