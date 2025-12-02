# login_page.py - Premium Login Page with Database Integration
import streamlit as st
import time
from database import create_user, verify_user, check_username_exists, check_email_exists

def load_login_css():
    """Load premium CSS styles for login page"""
    st.markdown("""
    <style>
    /* Ultra Premium Theme */
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
        --warning: #FF9800;
        --error: #F44336;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 16px 48px rgba(0, 212, 170, 0.3);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Login Container */
    .login-container {
        min-height: 100vh;
        background: var(--bg-primary);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    
    /* Glass Morphism Card */
    .glass-card {
        background: rgba(26, 26, 26, 0.9);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        box-shadow: var(--shadow-lg);
        width: 100%;
        max-width: 450px;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 212, 170, 0.4);
    }
    
    /* Logo Styles */
    .logo-container {
        text-align: center;
        margin-bottom: 40px;
    }
    
    .logo-icon {
        font-size: 4rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
    }
    
    .logo-text {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .logo-subtext {
        color: var(--text-secondary);
        font-size: 1rem;
        margin: 5px 0 0 0;
        font-weight: 500;
    }
    
    /* Form Styles */
    .form-title {
        text-align: center;
        color: var(--text-primary);
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .form-subtitle {
        text-align: center;
        color: var(--text-secondary);
        margin-bottom: 30px;
        font-size: 1rem;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.3) !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Buttons */
    .stButton>button {
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
    
    /* Toggle Switch */
    .toggle-container {
        display: flex;
        justify-content: center;
        margin-bottom: 30px;
        background: var(--bg-card);
        border-radius: 50px;
        padding: 5px;
        border: 1px solid var(--border);
    }
    
    .toggle-option {
        padding: 10px 30px;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 500;
        text-align: center;
        flex: 1;
    }
    
    .toggle-option.active {
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    /* Success Animation */
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-pop {
        animation: successPop 0.6s ease-out;
    }
    
    /* Welcome Animation */
    @keyframes welcomeSlide {
        0% { transform: translateY(-20px); opacity: 0; }
        100% { transform: translateY(0); opacity: 1; }
    }
    
    .welcome-message {
        animation: welcomeSlide 0.8s ease-out;
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.1), rgba(0, 153, 255, 0.1));
        border-radius: 15px;
        border: 1px solid rgba(0, 212, 170, 0.3);
        margin: 20px 0;
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
        margin: 5px 0;
        line-height: 1.4;
    }
    </style>
    """, unsafe_allow_html=True)

def show_welcome_animation(username):
    """Show welcome animation after login"""
    st.markdown(f"""
    <div class="welcome-message success-pop">
        <h2 style="color: #00D4AA; margin-bottom: 10px;">🎉 Welcome Back, {username}!</h2>
        <p style="color: var(--text-secondary); margin: 0;">Ready to revolutionize your hiring process with SmartHire AI!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar for smooth transition
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress_bar.progress(i + 1)
    time.sleep(0.5)

def show_login_page():
    """Show the premium login/signup page"""
    
    # Load CSS
    load_login_css()
    
    # Initialize session state for login/signup toggle
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Logo Section
        st.markdown("""
        <div class="logo-container">
            <div class="logo-icon">🚀</div>
            <div class="logo-text">SmartHire AI</div>
            <div class="logo-subtext">Premium Recruitment Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Glass Morphism Card
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Login/Signup Toggle
        col1, col2 = st.columns(2)
        with col1:
            login_active = "active" if not st.session_state.show_signup else ""
            if st.button("🔐 Login", use_container_width=True, key="login_toggle"):
                st.session_state.show_signup = False
                st.rerun()
        with col2:
            signup_active = "active" if st.session_state.show_signup else ""
            if st.button("📝 Sign Up", use_container_width=True, key="signup_toggle"):
                st.session_state.show_signup = True
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)  # Close toggle container
        
        # Login Form
        if not st.session_state.show_signup:
            with st.form("login_form"):
                st.markdown("""
                <div class="form-title">Welcome Back</div>
                <div class="form-subtitle">Sign in to your SmartHire AI account</div>
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
                    "🚀 Sign In to SmartHire AI",
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
                <div class="form-title">Create Account</div>
                <div class="form-subtitle">Join SmartHire AI today</div>
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
                    "🎉 Create Account",
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
                        user_id = create_user(username, email, password)
                        if user_id:
                            st.success("✅ Account created successfully! You can now login.")
                            st.session_state.show_signup = False
                            st.rerun()
                        else:
                            st.error("❌ Failed to create account. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close glass-card
        
        # Demo credentials
        st.markdown("""
        <div class="demo-credentials">
            <h4>🎯 Demo Accounts</h4>
            <p><strong>👤 Username:</strong> admin | <strong>🔑 Password:</strong> admin123</p>
            <p><strong>👤 Username:</strong> hr | <strong>🔑 Password:</strong> hr123</p>
            <p><strong>👤 Username:</strong> recruiter | <strong>🔑 Password:</strong> recruiter123</p>
        </div>
        """, unsafe_allow_html=True)

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