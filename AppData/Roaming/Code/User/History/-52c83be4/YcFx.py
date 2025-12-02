import streamlit as st
import sqlite3
import hashlib
import time
import re
from datetime import datetime

def load_login_css():
    st.markdown("""
    <style>
    /* COMPLETELY RESET STREAMLIT STYLES */
    .stApp {
        background: #111 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    
    /* Hide all Streamlit elements */
    .stApp > header { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }
    .stApp > div:first-child { display: none !important; }
    
    /* Main container - FIXED POSITION */
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
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Ring container */
    .ring-container {
        position: absolute;
        width: 500px;
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .ring {
        position: relative;
        width: 100%;
        height: 100%;
    }
    
    .ring i {
        position: absolute;
        inset: 0;
        border: 2px solid #fff;
        transition: 0.5s;
        border-radius: 50%;
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
    
    @keyframes animate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes animate2 {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }
    
    /* Form container - ABSOLUTE POSITION */
    .form-container {
        position: absolute !important;
        width: 320px !important;
        background: rgba(0, 0, 0, 0.8) !important;
        padding: 30px !important;
        border-radius: 20px !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        z-index: 10000 !important;
        display: block !important;
        visibility: visible !important;
    }
    
    /* Title */
    .form-title {
        color: white !important;
        font-size: 2em !important;
        text-align: center !important;
        margin-bottom: 20px !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 600 !important;
    }
    
    /* Make Streamlit inputs visible */
    .stTextInput {
        position: relative !important;
        z-index: 10001 !important;
        margin-bottom: 15px !important;
    }
    
    .stTextInput input {
        background: transparent !important;
        border: 2px solid white !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 12px 15px !important;
        width: 100% !important;
        font-size: 14px !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .stTextInput input:focus {
        border-color: #ff357a !important;
        box-shadow: 0 0 10px rgba(255, 53, 122, 0.5) !important;
    }
    
    /* Make buttons visible */
    .stButton {
        position: relative !important;
        z-index: 10001 !important;
        margin-top: 10px !important;
    }
    
    .stButton button {
        width: 100% !important;
        background: linear-gradient(45deg, #ff357a, #fff172) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 12px !important;
        color: black !important;
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* Toggle buttons */
    .toggle-buttons {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
    }
    
    .toggle-btn {
        flex: 1;
        background: transparent !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 20px !important;
        padding: 8px !important;
    }
    
    /* Links */
    .form-links {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
    }
    
    .form-links a {
        color: white;
        text-decoration: none;
        font-size: 12px;
    }
    
    .form-links a:hover {
        color: #ff357a;
    }
    
    /* Messages */
    .login-message {
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
        font-size: 14px;
    }
    
    .error-msg {
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.3);
        color: #ff4444;
    }
    
    .success-msg {
        background: rgba(0, 255, 0, 0.1);
        border: 1px solid rgba(0, 255, 0, 0.3);
        color: #00ff88;
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
                 ("demo", "demo@test.com", demo_hash, "Demo User"))
    
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
            user_data = {'username': user[1], 'email': user[2], 'full_name': user[4]}
            conn.close()
            return True, "Login successful!", user_data
        else:
            conn.close()
            return False, "Invalid credentials", None
    except:
        conn.close()
        return False, "Login failed", None

def register_user(username, email, password, full_name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            return False, "Username or email exists"
        
        c.execute('INSERT INTO users (username, email, password_hash, full_name) VALUES (?, ?, ?, ?)',
                 (username, email, hash_password(password), full_name))
        conn.commit()
        conn.close()
        return True, "Registration successful!"
    except:
        conn.close()
        return False, "Registration failed"

def login_page():
    """Main login page"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    
    if st.session_state.logged_in:
        return True
    
    # Load CSS and initialize DB
    load_login_css()
    init_database()
    
    # Main HTML structure
    st.markdown("""
    <div class="login-main">
        <div class="ring-container">
            <div class="ring">
                <i style="--clr:#00ff0a;"></i>
                <i style="--clr:#ff0057;"></i>
                <i style="--clr:#fffd44;"></i>
            </div>
        </div>
        <div class="form-container">
    """, unsafe_allow_html=True)
    
    # Toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", key="btn_login", use_container_width=True):
            st.session_state.current_form = "login"
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", key="btn_signup", use_container_width=True):
            st.session_state.current_form = "signup"
            st.rerun()
    
    # Forms
    if st.session_state.current_form == "login":
        st.markdown("<div class='form-title'>Login</div>", unsafe_allow_html=True)
        
        username = st.text_input("", placeholder="Username", key="inp_user")
        password = st.text_input("", placeholder="Password", type="password", key="inp_pass")
        
        if st.button("Sign In", key="btn_signin", use_container_width=True):
            if username and password:
                success, msg, user_data = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.markdown(f'<div class="login-message success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f'<div class="login-message error-msg">❌ {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="login-message error-msg">❌ Fill all fields</div>', unsafe_allow_html=True)
    
    else:  # Signup
        st.markdown("<div class='form-title'>Sign Up</div>", unsafe_allow_html=True)
        
        full_name = st.text_input("", placeholder="Full Name", key="sup_name")
        username = st.text_input("", placeholder="Username", key="sup_user")
        email = st.text_input("", placeholder="Email", key="sup_email")
        password = st.text_input("", placeholder="Password", type="password", key="sup_pass")
        confirm = st.text_input("", placeholder="Confirm Password", type="password", key="sup_conf")
        
        if st.button("Create Account", key="btn_create", use_container_width=True):
            if all([full_name, username, email, password, confirm]):
                if password == confirm:
                    success, msg = register_user(username, email, password, full_name)
                    if success:
                        st.markdown(f'<div class="login-message success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                        time.sleep(2)
                        st.session_state.current_form = "login"
                        st.rerun()
                    else:
                        st.markdown(f'<div class="login-message error-msg">❌ {msg}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="login-message error-msg">❌ Passwords dont match</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="login-message error-msg">❌ Fill all fields</div>', unsafe_allow_html=True)
    
    # Links
    st.markdown("""
    <div class="form-links">
        <a href="#">Forgot Password?</a>
        <a href="#">Help</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo info
    with st.expander("🔑 Demo Account"):
        st.write("**Username:** demo")
        st.write("**Password:** demo123")
    
    # Close containers
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return False

# Test directly
if __name__ == "__main__":
    st.set_page_config(
        page_title="Login",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    if login_page():
        st.success("Logged in! Redirecting...")
    else:
        st.stop()