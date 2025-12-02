import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import time
import re
from datetime import datetime
import json

# Premium Login Theme CSS
def load_login_css():
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
    
    /* Remove default padding and margin */
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
    }
    
    /* Main container to prevent scrolling */
    .main-container {
        height: 100vh;
        width: 100vw;
        margin: 0;
        padding: 0;
        overflow: hidden;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Login Container - Fixed positioning */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        width: 100vw;
        padding: 0;
        margin: 0;
        position: fixed;
        top: 0;
        left: 0;
        background: var(--bg-primary);
    }
    
    .login-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 40px 35px;
        width: 90%;
        max-width: 420px;
        max-height: 85vh;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
        overflow-y: auto;
        margin: auto;
    }
    
    /* Hide scrollbar for login card */
    .login-card::-webkit-scrollbar {
        display: none;
    }
    
    .login-card {
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
    
    /* Logo and Brand */
    .logo-container {
        text-align: center;
        margin-bottom: 25px;
    }
    
    .logo {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 8px;
    }
    
    .brand-name {
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
        line-height: 1.2;
    }
    
    .brand-tagline {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-bottom: 25px;
        line-height: 1.4;
    }
    
    /* Form Styles */
    .form-group {
        margin-bottom: 18px;
    }
    
    .form-label {
        color: var(--text-secondary);
        font-weight: 600;
        margin-bottom: 6px;
        display: block;
        font-size: 0.9rem;
    }
    
    /* Input Fields - Improved styling */
    .stTextInput>div>div>input {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        width: 100% !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        height: 48px !important;
        box-sizing: border-box !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--text-muted) !important;
        font-size: 13px !important;
    }
    
    /* Password input specific */
    .stTextInput>div>div>input[type="password"] {
        letter-spacing: 1px !important;
    }
    
    /* Buttons - Improved styling */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        margin-top: 8px !important;
        height: 48px !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Toggle buttons */
    .toggle-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .toggle-btn {
        flex: 1;
        background: var(--bg-secondary) !important;
        color: var(--text-secondary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .toggle-btn:hover {
        border-color: var(--accent-primary) !important;
        color: var(--accent-primary) !important;
    }
    
    .toggle-btn.active {
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border-color: transparent !important;
    }
    
    /* Toggle between Login/Signup */
    .toggle-text {
        text-align: center;
        color: var(--text-secondary);
        margin-top: 20px;
        font-size: 0.9rem;
    }
    
    .toggle-link {
        color: var(--accent-primary);
        cursor: pointer;
        font-weight: 600;
        text-decoration: none;
        margin-left: 5px;
    }
    
    .toggle-link:hover {
        text-decoration: underline;
    }
    
    /* Success Animation */
    @keyframes welcomePop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .welcome-pop {
        animation: welcomePop 0.6s ease-out;
        text-align: center;
        padding: 25px 20px;
        background: var(--bg-card);
        border-radius: 15px;
        margin: 10px 0;
    }
    
    /* Error Messages */
    .error-message {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        color: #f44336;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 12px 0;
        font-size: 13px;
        line-height: 1.4;
    }
    
    /* Success Messages */
    .success-message {
        background: rgba(0, 200, 83, 0.1);
        border: 1px solid rgba(0, 200, 83, 0.3);
        color: #00C853;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 12px 0;
        font-size: 13px;
        line-height: 1.4;
    }
    
    /* Password Strength */
    .password-strength {
        margin-top: 6px;
        font-size: 11px;
        line-height: 1.3;
    }
    
    .strength-weak { color: #f44336; }
    .strength-medium { color: #ff9800; }
    .strength-strong { color: #4caf50; }
    
    /* Form separator */
    .form-separator {
        height: 1px;
        background: var(--border);
        margin: 20px 0;
        opacity: 0.5;
    }
    
    /* Demo credentials expander */
    .demo-expander {
        margin-top: 15px;
    }
    
    /* Responsive design */
    @media (max-height: 700px) {
        .login-card {
            max-height: 95vh;
            padding: 30px 25px;
        }
        
        .logo {
            font-size: 3rem;
        }
        
        .brand-name {
            font-size: 2rem;
        }
    }
    
    /* Fix for form focus states */
    .stTextInput>div>div>input:not(:placeholder-shown) {
        border-color: var(--accent-primary) !important;
    }
    
    /* Email validation styling */
    .email-valid {
        border-color: #4caf50 !important;
    }
    
    .email-invalid {
        border-color: #f44336 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Database setup
def init_database():
    """Initialize SQLite database for user management"""
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            company TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    conn.commit()
    return conn

# Password hashing
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# Enhanced Email validation
def is_valid_email(email):
    """Validate email format with better rules"""
    if not email:
        return False
    
    # Basic pattern check
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False
    
    # Additional checks
    if '..' in email:
        return False
    
    if email.startswith('.') or email.endswith('.'):
        return False
    
    # Check for common disposable email domains
    disposable_domains = [
        'tempmail.com', 'fakeinbox.com', 'throwaway.com',
        'guerrillamail.com', 'mailinator.com', '10minutemail.com'
    ]
    
    domain = email.split('@')[1].lower()
    if domain in disposable_domains:
        return False
    
    return True

# Enhanced Password strength validation
def check_password_strength(password):
    """Check password strength with detailed feedback"""
    if len(password) < 8:
        return "weak", "❌ Password must be at least 8 characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    score = sum([has_upper, has_lower, has_digit, has_special])
    
    if score >= 4 and len(password) >= 12:
        return "strong", "✅ Strong password - Excellent!"
    elif score >= 4:
        return "strong", "✅ Strong password"
    elif score >= 3:
        return "medium", "⚠️ Good password - Add special characters for better security"
    else:
        missing = []
        if not has_upper:
            missing.append("uppercase letters")
        if not has_lower:
            missing.append("lowercase letters")
        if not has_digit:
            missing.append("numbers")
        if not has_special:
            missing.append("special characters")
        
        return "weak", f"❌ Weak password - Add {', '.join(missing)}"

# Enhanced User registration
def register_user(username, email, password, full_name, company=""):
    """Register a new user with enhanced validation"""
    conn = init_database()
    c = conn.cursor()
    
    try:
        # Validate username format
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return False, "Username must be 3-20 characters long and contain only letters, numbers, and underscores"
        
        # Check if username or email already exists
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        existing_user = c.fetchone()
        
        if existing_user:
            if existing_user[1] == username:  # username match
                return False, "Username already exists. Please choose a different one."
            else:  # email match
                return False, "Email address already registered. Please use a different email or try logging in."
        
        # Hash password and insert user
        password_hash = hash_password(password)
        c.execute('''
            INSERT INTO users (username, email, password_hash, full_name, company)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, company))
        
        conn.commit()
        conn.close()
        return True, "🎉 Registration successful! You can now log in with your credentials."
        
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}"

# Enhanced User login
def login_user(username, password):
    """Authenticate user login with better error handling"""
    conn = init_database()
    c = conn.cursor()
    
    try:
        # Find user by username or email
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, username))
        user = c.fetchone()
        
        if user:
            # Verify password
            if user[3] == hash_password(password):  # password_hash is at index 3
                # Update last login
                c.execute('UPDATE users SET last_login = ? WHERE id = ?', (datetime.now(), user[0]))
                conn.commit()
                conn.close()
                
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[4],
                    'company': user[5],
                    'created_at': user[6]
                }
                return True, "✅ Login successful! Welcome back.", user_data
            else:
                conn.close()
                return False, "❌ Invalid password. Please try again.", None
        else:
            conn.close()
            return False, "❌ User not found. Please check your username/email or sign up for a new account.", None
            
    except Exception as e:
        conn.close()
        return False, f"❌ Login failed: {str(e)}", None

def show_welcome_popup(user_data):
    """Show welcome back popup with user data"""
    st.markdown(f"""
    <div class="welcome-pop">
        <div style='font-size: 3.5rem; margin-bottom: 15px;'>🎉</div>
        <h2 style='background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 8px; font-size: 1.5rem;'>
            Welcome Back, {user_data['full_name']}!
        </h2>
        <p style='color: var(--text-secondary); margin-bottom: 15px; font-size: 0.9rem;'>
            Ready to continue your recruitment journey with SmartHire AI
        </p>
        <div style='background: var(--bg-secondary); padding: 12px; border-radius: 8px; margin: 15px 0; font-size: 0.8rem;'>
            <p style='margin: 4px 0;'>👤 <strong>Username:</strong> {user_data['username']}</p>
            <p style='margin: 4px 0;'>📧 <strong>Email:</strong> {user_data['email']}</p>
            {f"<p style='margin: 4px 0;'>🏢 <strong>Company:</strong> {user_data['company']}</p>" if user_data['company'] else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a loading delay before redirecting
    with st.spinner("🚀 Redirecting to main application..."):
        time.sleep(2)
    return True

def login_page():
    """Main login page function"""
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Load CSS
    load_login_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    if 'show_welcome' not in st.session_state:
        st.session_state.show_welcome = False
    
    # If user is logged in and welcome is shown, return to main app
    if st.session_state.logged_in and st.session_state.show_welcome:
        return True
    
    # Show welcome popup if just logged in
    if st.session_state.logged_in and st.session_state.user_data and not st.session_state.show_welcome:
        if show_welcome_popup(st.session_state.user_data):
            st.session_state.show_welcome = True
            st.rerun()
        return True
    
    # Main login container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Logo and Brand
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🚀</div>
        <div class="brand-name">SmartHire.AI</div>
        <div class="brand-tagline">Premium AI Recruitment Platform</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle between Login and Signup
    col1, col2 = st.columns(2)
    with col1:
        login_btn = st.button("🔐 Login", 
                            use_container_width=True, 
                            key="login_btn",
                            type="primary" if st.session_state.current_form == "login" else "secondary")
    with col2:
        signup_btn = st.button("📝 Sign Up", 
                             use_container_width=True, 
                             key="signup_btn",
                             type="primary" if st.session_state.current_form == "signup" else "secondary")
    
    if login_btn:
        st.session_state.current_form = "login"
        st.rerun()
    if signup_btn:
        st.session_state.current_form = "signup"
        st.rerun()
    
    st.markdown('<div class="form-separator"></div>', unsafe_allow_html=True)
    
    # Login Form
    if st.session_state.current_form == "login":
        st.markdown("### 🔐 Welcome Back")
        
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("👤 Username or Email", 
                                   placeholder="Enter your username or email address",
                                   key="login_username")
            
            password = st.text_input("🔒 Password", 
                                   type="password", 
                                   placeholder="Enter your password",
                                   key="login_password")
            
            login_submitted = st.form_submit_button("🚀 Sign In", use_container_width=True)
            
            if login_submitted:
                if not username or not password:
                    st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
                else:
                    success, message, user_data = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_data = user_data
                        st.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">{message}</div>', unsafe_allow_html=True)
    
    # Signup Form
    else:
        st.markdown("### 📝 Create Account")
        
        with st.form("signup_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("👤 Full Name*", 
                                        placeholder="Enter your full name",
                                        key="signup_name")
            with col2:
                company = st.text_input("🏢 Company", 
                                      placeholder="Your company (optional)",
                                      key="signup_company")
            
            username = st.text_input("👤 Username*", 
                                   placeholder="Choose a username (3-20 characters)",
                                   key="signup_username")
            
            email = st.text_input("📧 Email Address*", 
                                placeholder="your.email@company.com",
                                key="signup_email")
            
            col_pass1, col_pass2 = st.columns(2)
            with col_pass1:
                password = st.text_input("🔒 Password*", 
                                       type="password", 
                                       placeholder="Create a strong password",
                                       key="signup_password")
            with col_pass2:
                confirm_password = st.text_input("🔒 Confirm Password*", 
                                               type="password", 
                                               placeholder="Confirm your password",
                                               key="signup_confirm_password")
            
            # Real-time password strength indicator
            if password:
                strength, message = check_password_strength(password)
                st.markdown(f'<div class="password-strength strength-{strength}">{message}</div>', unsafe_allow_html=True)
            
            # Real-time email validation
            if email and not is_valid_email(email):
                st.markdown('<div class="error-message" style="margin: 5px 0; font-size: 12px;">⚠️ Please enter a valid email address</div>', unsafe_allow_html=True)
            
            signup_submitted = st.form_submit_button("🎯 Create Account", use_container_width=True)
            
            if signup_submitted:
                # Enhanced validation
                validation_errors = []
                
                if not full_name:
                    validation_errors.append("Full name is required")
                if not username:
                    validation_errors.append("Username is required")
                elif not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
                    validation_errors.append("Username must be 3-20 characters with only letters, numbers, and underscores")
                if not email:
                    validation_errors.append("Email address is required")
                elif not is_valid_email(email):
                    validation_errors.append("Please enter a valid email address")
                if not password:
                    validation_errors.append("Password is required")
                elif len(password) < 8:
                    validation_errors.append("Password must be at least 8 characters long")
                if password != confirm_password:
                    validation_errors.append("Passwords do not match")
                
                if validation_errors:
                    error_html = "❌ " + "<br>• ".join(validation_errors)
                    st.markdown(f'<div class="error-message">{error_html}</div>', unsafe_allow_html=True)
                else:
                    success, message = register_user(username, email, password, full_name, company)
                    if success:
                        st.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)
                        # Auto-switch to login form after successful registration
                        time.sleep(2)
                        st.session_state.current_form = "login"
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">{message}</div>', unsafe_allow_html=True)
    
    # Demo credentials
    st.markdown('<div class="form-separator"></div>', unsafe_allow_html=True)
    with st.expander("🔑 Demo Credentials", expanded=False):
        st.markdown("""
        **Test Account:**
        ```
        Username: demo
        Email: demo@smartai.com  
        Password: demo123
        ```
        
        *You can also create your own account using the signup form above.*
        
        **📧 Email Support:** support@smarthire.ai
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-container
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
    
    return st.session_state.logged_in

# For testing the login page independently
if __name__ == "__main__":
    # Create a demo user for testing
    conn = init_database()
    c = conn.cursor()
    
    # Check if demo user exists, if not create one
    c.execute('SELECT * FROM users WHERE username = "demo"')
    if not c.fetchone():
        demo_password_hash = hash_password("demo123")
        c.execute('''
            INSERT INTO users (username, email, password_hash, full_name, company)
            VALUES (?, ?, ?, ?, ?)
        ''', ("demo", "demo@smarthire.ai", demo_password_hash, "Demo User", "SmartHire AI"))
        conn.commit()
    
    conn.close()
    
    # Run the login page
    if login_page():
        st.success("✅ Login successful! Redirecting to main application...")
else:
    # Initialize database when imported
    init_database()