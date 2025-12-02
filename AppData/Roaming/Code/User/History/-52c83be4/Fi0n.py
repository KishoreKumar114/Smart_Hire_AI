import streamlit as st
import sqlite3
import hashlib
import time
import re
from datetime import datetime

def load_login_css():
    st.markdown("""
    <style>
    /* COMPLETE STYLE RESET */
    .stApp {
        background: #111 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide Streamlit elements */
    header { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stApp > div:first-child { display: none !important; }
    
    /* Main container */
    .login-main {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: #111 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        z-index: 9999 !important;
    }
    
    /* Ring animation */
    .ring {
        position: absolute;
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
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes animate2 {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }
    
    /* Form container */
    .form-container {
        position: absolute !important;
        width: 350px !important;
        background: rgba(0, 0, 0, 0.85) !important;
        padding: 30px 25px !important;
        border-radius: 20px !important;
        backdrop-filter: blur(15px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        z-index: 10000 !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Title */
    .form-title {
        color: white !important;
        font-size: 2em !important;
        text-align: center !important;
        margin-bottom: 25px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* Input styling - FIXED FOR NEW STREAMLIT */
    div[data-testid="stTextInput"] {
        margin-bottom: 15px !important;
    }
    
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    
    div[data-testid="stTextInput"] input {
        background: transparent !important;
        border: 2px solid white !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 12px 18px !important;
        width: 100% !important;
        font-size: 14px !important;
        font-family: 'Quicksand', sans-serif !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #ff357a !important;
        box-shadow: 0 0 10px rgba(255, 53, 122, 0.5) !important;
        outline: none !important;
    }
    
    /* Button styling */
    div[data-testid="stButton"] {
        margin-top: 10px !important;
    }
    
    div[data-testid="stButton"] button {
        width: 100% !important;
        background: linear-gradient(45deg, #ff357a, #fff172) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px !important;
        color: black !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        font-family: 'Quicksand', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(255, 53, 122, 0.4) !important;
    }
    
    /* Toggle buttons */
    .toggle-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    /* Links */
    .form-links {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
        padding: 0 10px;
    }
    
    .form-links a {
        color: white;
        text-decoration: none;
        font-size: 12px;
        font-family: 'Quicksand', sans-serif;
        transition: color 0.3s ease;
    }
    
    .form-links a:hover {
        color: #ff357a;
        text-decoration: underline;
    }
    
    /* Messages */
    .login-message {
        padding: 12px 15px;
        border-radius: 10px;
        margin: 15px 0;
        text-align: center;
        font-size: 14px;
        font-family: 'Quicksand', sans-serif;
    }
    
    .error-msg {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
        color: #ff6b6b;
    }
    
    .success-msg {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid rgba(0, 255, 0, 0.3);
        color: #51ff51;
    }
    
    /* Expander styling */
    .demo-expander {
        margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def init_database():
    """Initialize database"""
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create demo user
    c.execute('SELECT * FROM users WHERE username = "demo"')
    if not c.fetchone():
        demo_hash = hashlib.sha256("demo123".encode()).hexdigest()
        c.execute('INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)',
                 ("demo", "demo@smarthire.ai", demo_hash, "Demo User"))
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, username))
        user = c.fetchone()
        
        if user and user[3] == hash_password(password):
            user_data = {
                'id': user[0],
                'username': user[1], 
                'email': user[2],
                'full_name': user[4]
            }
            conn.close()
            return True, "🎉 Login successful! Redirecting...", user_data
        else:
            conn.close()
            return False, "❌ Invalid username or password", None
    except Exception as e:
        conn.close()
        return False, f"❌ Login error: {str(e)}", None

def register_user(username, email, password, full_name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        # Check if user exists
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            return False, "❌ Username or email already exists"
        
        # Insert new user
        password_hash = hash_password(password)
        c.execute('INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)',
                 (username, email, password_hash, full_name))
        conn.commit()
        conn.close()
        return True, "✅ Registration successful! Please login."
    except Exception as e:
        conn.close()
        return False, f"❌ Registration failed: {str(e)}"

def login_page():
    """Main login page function"""
    
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
    
    # Load CSS and initialize database
    load_login_css()
    init_database()
    
    # Main container with ring animation
    st.markdown("""
    <div class="login-main">
        <div class="ring">
            <i style="--clr:#00ff0a;"></i>
            <i style="--clr:#ff0057;"></i>
            <i style="--clr:#fffd44;"></i>
        </div>
        <div class="form-container">
    """, unsafe_allow_html=True)
    
    # Toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", 
                    key="login_toggle", 
                    use_container_width=True,
                    type="primary" if st.session_state.current_form == "login" else "secondary"):
            st.session_state.current_form = "login"
            st.rerun()
    
    with col2:
        if st.button("📝 Sign Up", 
                     key="signup_toggle", 
                     use_container_width=True,
                     type="primary" if st.session_state.current_form == "signup" else "secondary"):
            st.session_state.current_form = "signup"
            st.rerun()
    
    # Login Form
    if st.session_state.current_form == "login":
        st.markdown("<div class='form-title'>Login</div>", unsafe_allow_html=True)
        
        # FIX: Use proper labels with label_visibility
        username = st.text_input(
            "Username", 
            placeholder="Enter your username",
            key="login_username",
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "Password", 
            placeholder="Enter your password", 
            type="password",
            key="login_password",
            label_visibility="collapsed"
        )
        
        if st.button("🚀 Sign In", key="login_submit", use_container_width=True):
            if not username or not password:
                st.markdown('<div class="login-message error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                success, message, user_data = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.markdown(f'<div class="login-message success-msg">{message}</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f'<div class="login-message error-msg">{message}</div>', unsafe_allow_html=True)
    
    # Signup Form  
    else:
        st.markdown("<div class='form-title'>Sign Up</div>", unsafe_allow_html=True)
        
        full_name = st.text_input(
            "Full Name",
            placeholder="Enter your full name",
            key="signup_fullname",
            label_visibility="collapsed"
        )
        
        username = st.text_input(
            "Username",
            placeholder="Choose a username", 
            key="signup_username",
            label_visibility="collapsed"
        )
        
        email = st.text_input(
            "Email",
            placeholder="Enter your email address",
            key="signup_email", 
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "Password",
            placeholder="Create a password",
            type="password",
            key="signup_password",
            label_visibility="collapsed"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            placeholder="Confirm your password", 
            type="password",
            key="signup_confirm",
            label_visibility="collapsed"
        )
        
        if st.button("🎯 Create Account", key="signup_submit", use_container_width=True):
            # Validation
            if not all([full_name, username, email, password, confirm_password]):
                st.markdown('<div class="login-message error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="login-message error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
            elif len(password) < 6:
                st.markdown('<div class="login-message error-msg">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
            else:
                success, message = register_user(username, email, password, full_name)
                if success:
                    st.markdown(f'<div class="login-message success-msg">{message}</div>', unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.current_form = "login"
                    st.rerun()
                else:
                    st.markdown(f'<div class="login-message error-msg">{message}</div>', unsafe_allow_html=True)
    
    # Links
    st.markdown("""
    <div class="form-links">
        <a href="#">Forgot Password?</a>
        <a href="#">Need Help?</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo credentials
    with st.expander("🔑 Demo Credentials", expanded=False):
        st.markdown("""
        **Test Account:**
        - **Username:** `demo`
        - **Password:** `demo123`
        
        *Try this account to test the login*
        """)
    
    # Close HTML containers
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return False

# Test the login page directly
if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    if login_page():
        st.success("✅ Successfully logged in!")
    else:
        st.stop()