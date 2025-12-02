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
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Login Container */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    .login-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 40px;
        width: 100%;
        max-width: 450px;
        box-shadow: var(--shadow-lg);
        backdrop-filter: blur(10px);
    }
    
    /* Logo and Brand */
    .logo-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .logo {
        font-size: 4rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 10px;
    }
    
    .brand-name {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .brand-tagline {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 30px;
    }
    
    /* Form Styles */
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-label {
        color: var(--text-secondary);
        font-weight: 600;
        margin-bottom: 8px;
        display: block;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stTextInput>div>div>input:focus {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        width: 100% !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1) !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Buttons */
    .login-button {
        width: 100% !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        margin-top: 10px !important;
    }
    
    .login-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    /* Toggle between Login/Signup */
    .toggle-text {
        text-align: center;
        color: var(--text-secondary);
        margin-top: 25px;
    }
    
    .toggle-link {
        color: var(--accent-primary);
        cursor: pointer;
        font-weight: 600;
        text-decoration: none;
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
        padding: 30px;
    }
    
    /* Error Messages */
    .error-message {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        color: #f44336;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 14px;
    }
    
    /* Success Messages */
    .success-message {
        background: rgba(0, 200, 83, 0.1);
        border: 1px solid rgba(0, 200, 83, 0.3);
        color: #00C853;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 14px;
    }
    
    /* Password Strength */
    .password-strength {
        margin-top: 8px;
        font-size: 12px;
    }
    
    .strength-weak { color: #f44336; }
    .strength-medium { color: #ff9800; }
    .strength-strong { color: #4caf50; }
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

# Email validation
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Password strength validation
def check_password_strength(password):
    """Check password strength"""
    if len(password) < 8:
        return "weak", "Password must be at least 8 characters long"
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    score = sum([has_upper, has_lower, has_digit, has_special])
    
    if score >= 4:
        return "strong", "Strong password"
    elif score >= 3:
        return "medium", "Medium strength password"
    else:
        return "weak", "Weak password - include uppercase, lowercase, numbers, and special characters"

# User registration
def register_user(username, email, password, full_name, company=""):
    """Register a new user"""
    conn = init_database()
    c = conn.cursor()
    
    try:
        # Check if username or email already exists
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            return False, "Username or email already exists"
        
        # Hash password and insert user
        password_hash = hash_password(password)
        c.execute('''
            INSERT INTO users (username, email, password_hash, full_name, company)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, company))
        
        conn.commit()
        conn.close()
        return True, "Registration successful!"
        
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}"

# User login
def login_user(username, password):
    """Authenticate user login"""
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
                return True, "Login successful!", user_data
            else:
                conn.close()
                return False, "Invalid password", None
        else:
            conn.close()
            return False, "User not found", None
            
    except Exception as e:
        conn.close()
        return False, f"Login failed: {str(e)}", None

def show_welcome_popup(user_data):
    """Show welcome back popup with user data"""
    st.markdown(f"""
    <div class="welcome-pop">
        <div style='font-size: 4rem; margin-bottom: 20px;'>🎉</div>
        <h2 style='background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px;'>
            Welcome Back, {user_data['full_name']}!
        </h2>
        <p style='color: var(--text-secondary); margin-bottom: 20px;'>
            Ready to continue your recruitment journey with SmartHire AI
        </p>
        <div style='background: var(--bg-secondary); padding: 15px; border-radius: 10px; margin: 20px 0;'>
            <p style='margin: 5px 0;'>👤 <strong>Username:</strong> {user_data['username']}</p>
            <p style='margin: 5px 0;'>📧 <strong>Email:</strong> {user_data['email']}</p>
            {f"<p style='margin: 5px 0;'>🏢 <strong>Company:</strong> {user_data['company']}</p>" if user_data['company'] else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a loading delay before redirecting
    with st.spinner("Redirecting to main application..."):
        time.sleep(3)
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
        if st.button("🔐 Login", use_container_width=True, 
                    type="primary" if st.session_state.current_form == "login" else "secondary"):
            st.session_state.current_form = "login"
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", use_container_width=True,
                    type="primary" if st.session_state.current_form == "signup" else "secondary"):
            st.session_state.current_form = "signup"
            st.rerun()
    
    st.markdown("---")
    
    # Login Form
    if st.session_state.current_form == "login":
        st.markdown("### 🔐 Welcome Back")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username or Email", placeholder="Enter your username or email")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            login_submitted = st.form_submit_button("🚀 Sign In", use_container_width=True)
            
            if login_submitted:
                if not username or not password:
                    st.markdown('<div class="error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
                else:
                    success, message, user_data = login_user(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.user_data = user_data
                        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
    
    # Signup Form
    else:
        st.markdown("### 📝 Create Account")
        
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            with col2:
                company = st.text_input("🏢 Company (Optional)", placeholder="Your company name")
            
            username = st.text_input("👤 Username", placeholder="Choose a username")
            email = st.text_input("📧 Email Address", placeholder="Enter your email address")
            
            col_pass1, col_pass2 = st.columns(2)
            with col_pass1:
                password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
            with col_pass2:
                confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
            
            # Password strength indicator
            if password:
                strength, message = check_password_strength(password)
                st.markdown(f'<div class="password-strength strength-{strength}">🔐 {message}</div>', unsafe_allow_html=True)
            
            signup_submitted = st.form_submit_button("🎯 Create Account", use_container_width=True)
            
            if signup_submitted:
                # Validation
                if not all([full_name, username, email, password, confirm_password]):
                    st.markdown('<div class="error-message">❌ Please fill in all required fields</div>', unsafe_allow_html=True)
                elif not is_valid_email(email):
                    st.markdown('<div class="error-message">❌ Please enter a valid email address</div>', unsafe_allow_html=True)
                elif password != confirm_password:
                    st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
                elif len(password) < 8:
                    st.markdown('<div class="error-message">❌ Password must be at least 8 characters long</div>', unsafe_allow_html=True)
                else:
                    success, message = register_user(username, email, password, full_name, company)
                    if success:
                        st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                        # Auto-switch to login form
                        st.session_state.current_form = "login"
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
    
    # Demo credentials
    st.markdown("---")
    with st.expander("🔑 Demo Credentials"):
        st.markdown("""
        **Test Account:**
        ```
        Username: demo
        Email: demo@smartai.com  
        Password: demo123
        ```
        
        *You can also create your own account using the signup form above.*
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-container
    
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
        ''', ("demo", "demo@smartai.com", demo_password_hash, "Demo User", "SmartHire AI"))
        conn.commit()
    
    conn.close()
    
    # Run the login page
    if login_page():
        st.success("✅ Login successful! Redirecting to main application...")
        # Here you would typically redirect to your main app
        # For now, we'll just show a success message
else:
    # Initialize database when imported
    init_database()