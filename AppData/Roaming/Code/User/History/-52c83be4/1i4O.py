# login_page.py - STUNNING GLOWING LOGIN FORM
import streamlit as st
import time
import random  # ADD THIS IMPORT
from database import create_user, verify_user, check_username_exists, check_email_exists, initialize_database

def load_glowing_login_css():
    """Load stunning glowing CSS styles for login page"""
    st.markdown("""
    <style>
    /* Glowing Premium Theme */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
        --accent-primary: #00D4AA;
        --accent-secondary: #0099FF;
        --accent-glow: 0 0 20px rgba(0, 212, 170, 0.7);
        --accent-gradient: linear-gradient(135deg, #00D4AA, #0099FF);
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --text-muted: #AAAAAA;
        --border: #333333;
        --input-bg: rgba(45, 45, 45, 0.8);
        --input-text: #FFFFFF;
        --success: #00C853;
        --warning: #FF9800;
        --error: #F44336;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        overflow: hidden;
    }
    
    /* Main Container with Animated Gradient */
    .main-login-container {
        min-height: 100vh;
        background: linear-gradient(-45deg, #0A0A0A, #111111, #1a1a1a, #2d2d2d);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
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
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Floating Particles Background */
    .particles {
        position: absolute;
        width: 100%;
        height: 100%;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        background: rgba(0, 212, 170, 0.3);
        border-radius: 50%;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) rotate(360deg); opacity: 0; }
    }
    
    /* Glowing Card */
    .glowing-card {
        background: rgba(26, 26, 26, 0.85);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 50px 40px;
        box-shadow: 
            0 0 50px rgba(0, 212, 170, 0.3),
            inset 0 0 50px rgba(0, 212, 170, 0.1);
        width: 100%;
        max-width: 480px;
        position: relative;
        z-index: 100;
        transition: all 0.4s ease;
    }
    
    .glowing-card::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, #00D4AA, #0099FF, #00D4AA);
        border-radius: 27px;
        z-index: -1;
        animation: borderGlow 3s linear infinite;
        opacity: 0.7;
        filter: blur(10px);
    }
    
    @keyframes borderGlow {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    
    .glowing-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 
            0 0 80px rgba(0, 212, 170, 0.5),
            inset 0 0 60px rgba(0, 212, 170, 0.2);
    }
    
    /* Logo Styles */
    .logo-container {
        text-align: center;
        margin-bottom: 40px;
        position: relative;
    }
    
    .logo-icon {
        font-size: 4.5rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        display: block;
        animation: logoPulse 2s ease-in-out infinite alternate;
        filter: drop-shadow(0 0 20px rgba(0, 212, 170, 0.5));
    }
    
    @keyframes logoPulse {
        0% { transform: scale(1); }
        100% { transform: scale(1.1); }
    }
    
    .logo-text {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
    }
    
    .logo-subtext {
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin: 8px 0 0 0;
        font-weight: 500;
        letter-spacing: 2px;
    }
    
    /* Toggle Switch */
    .toggle-container {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
        background: rgba(45, 45, 45, 0.6);
        border-radius: 50px;
        padding: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .toggle-option {
        padding: 12px 35px;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        text-align: center;
        flex: 1;
        z-index: 2;
        position: relative;
        color: var(--text-secondary);
    }
    
    .toggle-option.active {
        color: white;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }
    
    .toggle-slider {
        position: absolute;
        top: 8px;
        left: 8px;
        height: calc(100% - 16px);
        width: calc(50% - 16px);
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.5);
    }
    
    /* Form Styles */
    .form-title {
        text-align: center;
        color: var(--text-primary);
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 15px;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    
    .form-subtitle {
        text-align: center;
        color: var(--text-secondary);
        margin-bottom: 40px;
        font-size: 1.1rem;
    }
    
    /* Glowing Input Fields */
    .stTextInput>div>div {
        background: transparent !important;
    }
    
    .stTextInput>div>div>input {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        padding: 18px 25px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px);
        box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00D4AA !important;
        box-shadow: 
            0 0 30px rgba(0, 212, 170, 0.4),
            inset 0 0 20px rgba(0, 212, 170, 0.1) !important;
        transform: scale(1.02);
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Glowing Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 18px 30px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        margin-top: 20px !important;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 30px rgba(0, 212, 170, 0.4);
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 0 50px rgba(0, 212, 170, 0.6);
    }
    
    /* Demo Credentials */
    .demo-credentials {
        background: rgba(0, 212, 170, 0.15);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 15px;
        padding: 25px;
        margin-top: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 212, 170, 0.2);
        transition: all 0.3s ease;
    }
    
    .demo-credentials:hover {
        transform: translateY(-5px);
        box-shadow: 0 0 40px rgba(0, 212, 170, 0.3);
    }
    
    .demo-title {
        color: var(--accent-primary);
        margin-bottom: 20px;
        font-size: 1.2em;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0, 212, 170, 0.5);
    }
    
    .demo-account {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 12px 0;
        padding: 10px 15px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .demo-account:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(5px);
    }
    
    .demo-username {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    .demo-password {
        color: var(--accent-primary);
        font-weight: 600;
    }
    
    /* Success Animation */
    @keyframes successPop {
        0% { transform: scale(0.5); opacity: 0; }
        70% { transform: scale(1.1); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-animation {
        animation: successPop 0.8s ease-out;
        text-align: center;
        padding: 30px;
        background: linear-gradient(135deg, rgba(0, 200, 83, 0.2), rgba(0, 212, 170, 0.2));
        border-radius: 20px;
        border: 1px solid rgba(0, 200, 83, 0.4);
        margin: 20px 0;
        box-shadow: 0 0 40px rgba(0, 200, 83, 0.3);
    }
    
    /* Hide Streamlit elements when login is active */
    .main-login-container ~ * {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

def create_particles():
    """Create animated particles background"""
    particles_html = """
    <div class="particles">
    """
    for i in range(20):
        size = random.randint(2, 6)
        left = random.randint(0, 100)
        delay = random.randint(0, 15)
        duration = random.randint(15, 30)
        particles_html += f"""
        <div class="particle" style="
            width: {size}px;
            height: {size}px;
            left: {left}%;
            animation-delay: {delay}s;
            animation-duration: {duration}s;
        "></div>
        """
    particles_html += "</div>"
    return particles_html

def show_welcome_animation(username):
    """Show welcome animation after login"""
    st.markdown(f"""
    <div class="success-animation">
        <h2 style="color: #00D4AA; margin-bottom: 15px; font-size: 2rem;">🎉 Welcome Back, {username}!</h2>
        <p style="color: var(--text-secondary); font-size: 1.2rem; margin: 0;">
            Ready to revolutionize your hiring process with SmartHire AI!
        </p>
        <div style="font-size: 3rem; margin-top: 15px;">🚀</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar for smooth transition
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02)
        progress_bar.progress(i + 1)
    time.sleep(1)

def show_login_page():
    """Show the stunning glowing login/signup page"""
    
    # Initialize database
    if not initialize_database():
        st.error("❌ Database initialization failed. Please check your database connection.")
        return
    
    # Load CSS
    load_glowing_login_css()
    
    # Initialize session state for login/signup toggle
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    # Create the main login container with particles
    st.markdown(f"""
    <div class="main-login-container">
        {create_particles()}
        
        <div class="glowing-card">
    """, unsafe_allow_html=True)
    
    # Logo Section
    st.markdown("""
    <div class="logo-container">
        <div class="logo-icon">🚀</div>
        <div class="logo-text">SmartHire AI</div>
        <div class="logo-subtext">PREMIUM RECRUITMENT PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login/Signup Toggle with Slider
    st.markdown("""
    <div class="toggle-container">
        <div class="toggle-slider" style="transform: translateX(%s);"></div>
        <div class="toggle-option %s" onclick="toggleLogin()">🔐 Login</div>
        <div class="toggle-option %s" onclick="toggleSignup()">📝 Sign Up</div>
    </div>
    """ % (
        "0%" if not st.session_state.show_signup else "100%",
        "active" if not st.session_state.show_signup else "",
        "active" if st.session_state.show_signup else ""
    ), unsafe_allow_html=True)
    
    # JavaScript for toggle
    st.markdown("""
    <script>
    function toggleLogin() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'login'}, '*');
    }
    function toggleSignup() {
        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'signup'}, '*');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Handle toggle via buttons (since JS might not work perfectly in Streamlit)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", use_container_width=True, key="login_btn"):
            st.session_state.show_signup = False
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", use_container_width=True, key="signup_btn"):
            st.session_state.show_signup = True
            st.rerun()
    
    # Login Form
    if not st.session_state.show_signup:
        with st.form("login_form"):
            st.markdown("""
            <div class="form-title">Welcome Back!</div>
            <div class="form-subtitle">Sign in to continue your recruitment journey</div>
            """, unsafe_allow_html=True)
            
            username = st.text_input(
                "👤 Username",
                placeholder="Enter your username",
                key="login_username"
            )
            
            password = st.text_input(
                "🔑 Password", 
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            login_button = st.form_submit_button(
                "🚀 SIGN IN TO SMART HIRE AI",
                use_container_width=True
            )
            
            if login_button:
                if username and password:
                    user = verify_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.current_user = user['username']
                        st.session_state.user_role = user['role']
                        st.session_state.user_email = user['email']
                        
                        # Show welcome animation
                        show_welcome_animation(user['username'])
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password. Please try again.")
                else:
                    st.warning("⚠️ Please enter both username and password.")
    
    # Signup Form
    else:
        with st.form("signup_form"):
            st.markdown("""
            <div class="form-title">Join SmartHire AI!</div>
            <div class="form-subtitle">Create your account and transform your hiring process</div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input(
                    "👤 Username",
                    placeholder="Choose a username",
                    key="signup_username"
                )
            with col2:
                email = st.text_input(
                    "📧 Email",
                    placeholder="Enter your email",
                    key="signup_email"
                )
            
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input(
                    "🔑 Password",
                    type="password",
                    placeholder="Create a password",
                    key="signup_password"
                )
            with col2:
                confirm_password = st.text_input(
                    "✅ Confirm Password",
                    type="password", 
                    placeholder="Confirm your password",
                    key="signup_confirm_password"
                )
            
            signup_button = st.form_submit_button(
                "🎉 CREATE MY ACCOUNT",
                use_container_width=True
            )
            
            if signup_button:
                if not username or not email or not password or not confirm_password:
                    st.error("❌ Please fill in all fields.")
                elif password != confirm_password:
                    st.error("❌ Passwords do not match.")
                elif len(password) < 6:
                    st.error("❌ Password must be at least 6 characters long.")
                elif check_username_exists(username):
                    st.error("❌ Username already exists. Please choose another.")
                elif check_email_exists(email):
                    st.error("❌ Email already registered. Please use another.")
                else:
                    if create_user(username, email, password):
                        st.success("✅ Account created successfully! You can now login.")
                        st.session_state.show_signup = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to create account. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close glowing-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-login-container
    
    # Demo Credentials Section
    st.markdown("""
    <div class="demo-credentials">
        <div class="demo-title">🎯 Demo Accounts - Try Them Out!</div>
        <div class="demo-account">
            <span class="demo-username">👤 admin</span>
            <span class="demo-password">🔑 admin123</span>
        </div>
        <div class="demo-account">
            <span class="demo-username">👤 hr</span>
            <span class="demo-password">🔑 hr123</span>
        </div>
        <div class="demo-account">
            <span class="demo-username">👤 recruiter</span>
            <span class="demo-password">🔑 recruiter123</span>
        </div>
        <p style="color: var(--text-secondary); margin-top: 15px; font-size: 0.9em;">
            💡 Click on any demo account to quickly test the platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add click handlers for demo accounts
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Use Admin", key="demo_admin", use_container_width=True):
            st.session_state.login_username = "admin"
            st.session_state.login_password = "admin123"
            st.session_state.show_signup = False
            st.rerun()
    with col2:
        if st.button("Use HR", key="demo_hr", use_container_width=True):
            st.session_state.login_username = "hr"
            st.session_state.login_password = "hr123"
            st.session_state.show_signup = False
            st.rerun()
    with col3:
        if st.button("Use Recruiter", key="demo_recruiter", use_container_width=True):
            st.session_state.login_username = "recruiter"
            st.session_state.login_password = "recruiter123"
            st.session_state.show_signup = False
            st.rerun()

def check_authentication():
    """Check if user is authenticated"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    
    return st.session_state.authenticated