import streamlit as st
import pandas as pd
import hashlib
import sqlite3
import time
import re
from datetime import datetime
import json

# Premium Login Theme CSS - SIMPLIFIED VERSION
def load_login_css():
    st.markdown("""
    <style>
    /* Reset and Base Styles */
    .stApp {
        background: #0A0A0A !important;
        color: white !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main-container {
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #0A0A0A;
        padding: 20px;
    }
    
    /* Login Card */
    .login-card {
        background: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 20px;
        padding: 40px 35px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 16px 48px rgba(0, 212, 170, 0.2);
    }
    
    /* Logo and Brand */
    .logo-container {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .logo {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        margin-bottom: 10px;
    }
    
    .brand-name {
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .brand-tagline {
        color: #E0E0E0;
        font-size: 1rem;
        margin-bottom: 30px;
    }
    
    /* Toggle Buttons */
    .toggle-container {
        display: flex;
        gap: 10px;
        margin-bottom: 25px;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background: #2D2D2D !important;
        color: white !important;
        border: 2px solid #333333 !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        width: 100% !important;
        font-size: 14px !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #00D4AA !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1) !important;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-weight: 600 !important;
        margin-top: 10px !important;
    }
    
    /* Error Messages */
    .error-message {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.3);
        color: #f44336;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 15px 0;
    }
    
    /* Success Messages */
    .success-message {
        background: rgba(0, 200, 83, 0.1);
        border: 1px solid rgba(0, 200, 83, 0.3);
        color: #00C853;
        padding: 12px 16px;
        border-radius: 10px;
        margin: 15px 0;
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

# Email validation
def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

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
            if user[3] == hash_password(password):
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

def login_page():
    """Main login page function"""
    
    # Load CSS first
    load_login_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    # If already logged in, return True
    if st.session_state.logged_in:
        return True
    
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    
    # Logo and Brand - SIMPLE VERSION
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
        if st.button("🔐 Login", use_container_width=True, type="primary" if st.session_state.current_form == "login" else "secondary"):
            st.session_state.current_form = "login"
            st.rerun()
    
    with col2:
        if st.button("📝 Sign Up", use_container_width=True, type="primary" if st.session_state.current_form == "signup" else "secondary"):
            st.session_state.current_form = "signup"
            st.rerun()
    
    st.markdown("---")
    
    # Login Form
    if st.session_state.current_form == "login":
        st.subheader("🔐 Welcome Back")
        
        username = st.text_input("👤 Username or Email", placeholder="Enter your username or email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        if st.button("🚀 Sign In", use_container_width=True, type="primary"):
            if not username or not password:
                st.error("❌ Please fill in all fields")
            else:
                success, message, user_data = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.success("✅ Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Signup Form
    else:
        st.subheader("📝 Create Account")
        
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
        
        if st.button("🎯 Create Account", use_container_width=True, type="primary"):
            # Validation
            if not all([full_name, username, email, password, confirm_password]):
                st.error("❌ Please fill in all required fields")
            elif not is_valid_email(email):
                st.error("❌ Please enter a valid email address")
            elif password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 8:
                st.error("❌ Password must be at least 8 characters long")
            else:
                success, message = register_user(username, email, password, full_name, company)
                if success:
                    st.success("✅ Registration successful! Please log in.")
                    st.session_state.current_form = "login"
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    
    # Demo credentials
    st.markdown("---")
    with st.expander("🔑 Demo Credentials"):
        st.markdown("""
        **Test Account:**
        ```
        Username: demo
        Email: demo@smarthire.ai  
        Password: demo123
        ```
        
        **📧 Support:** support@smarthire.ai
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close login-card
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-container
    
    return st.session_state.logged_in

# For testing the login page independently
if __name__ == "__main__":
    # Set page config first
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
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