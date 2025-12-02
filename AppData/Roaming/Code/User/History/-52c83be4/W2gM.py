import streamlit as st
import sqlite3
import hashlib
import time
import re
from datetime import datetime

def load_login_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    /* Reset Streamlit default styles */
    .stApp {
        background: #111 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main container */
    .main-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #111;
        z-index: 9999;
    }
    
    /* Ring animation */
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
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes animate2 {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }
    
    /* Login form container */
    .login-form-container {
        position: absolute;
        width: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 15px;
        z-index: 10000;
        background: rgba(0, 0, 0, 0.7);
        padding: 30px 20px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .login-title {
        font-size: 2em;
        color: #fff;
        font-weight: 600;
        margin-bottom: 10px;
        font-family: "Quicksand", sans-serif;
    }
    
    /* Input styling */
    .stTextInput>div>div>input {
        width: 100% !important;
        padding: 12px 20px !important;
        background: transparent !important;
        border: 2px solid #fff !important;
        border-radius: 40px !important;
        font-size: 1em !important;
        color: #fff !important;
        font-family: "Quicksand", sans-serif !important;
    }
    
    .stTextInput>div>div>input::placeholder {
        color: rgba(255, 255, 255, 0.75) !important;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #ff357a !important;
        box-shadow: 0 0 10px rgba(255, 53, 122, 0.5) !important;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100% !important;
        background: linear-gradient(45deg, #ff357a, #fff172) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 12px 20px !important;
        font-size: 1.1em !important;
        color: #000 !important;
        font-weight: 600 !important;
        font-family: "Quicksand", sans-serif !important;
        margin-top: 10px !important;
    }
    
    /* Toggle buttons */
    .toggle-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        width: 100%;
    }
    
    .toggle-btn {
        flex: 1;
        background: transparent !important;
        color: #fff !important;
        border: 2px solid #fff !important;
        border-radius: 25px !important;
        padding: 8px !important;
        font-family: "Quicksand", sans-serif !important;
    }
    
    .toggle-btn:hover {
        border-color: #ff357a !important;
        color: #ff357a !important;
    }
    
    /* Links */
    .links {
        display: flex;
        justify-content: space-between;
        width: 100%;
        margin-top: 15px;
    }
    
    .links a {
        color: #fff;
        text-decoration: none;
        font-size: 0.9em;
        font-family: "Quicksand", sans-serif;
    }
    
    .links a:hover {
        color: #ff357a;
        text-decoration: underline;
    }
    
    /* Messages */
    .message {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        font-size: 0.9em;
        text-align: center;
        font-family: "Quicksand", sans-serif;
        width: 100%;
    }
    
    .error-message {
        background: rgba(244, 67, 54, 0.1);
        border: 1px solid rgba(244, 67, 54, 0.5);
        color: #ff4444;
    }
    
    .success-message {
        background: rgba(0, 200, 83, 0.1);
        border: 1px solid rgba(0, 200, 83, 0.5);
        color: #00ff88;
    }
    </style>
    """, unsafe_allow_html=True)

def init_database():
    """Initialize SQLite database for user management"""
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
    
    conn.commit()
    
    # Create demo user if not exists
    c.execute('SELECT * FROM users WHERE username = "demo"')
    if not c.fetchone():
        demo_password_hash = hashlib.sha256("demo123".encode()).hexdigest()
        c.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', ("demo", "demo@smarthire.ai", demo_password_hash, "Demo User"))
        conn.commit()
    
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(username, email, password, full_name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if c.fetchone():
            return False, "Username or email already exists"
        
        password_hash = hash_password(password)
        c.execute('''
            INSERT INTO users (username, email, password_hash, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, email, password_hash, full_name))
        
        conn.commit()
        conn.close()
        return True, "Registration successful!"
        
    except Exception as e:
        conn.close()
        return False, f"Registration failed: {str(e)}"

def login_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, username))
        user = c.fetchone()
        
        if user:
            if user[3] == hash_password(password):
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[4]
                }
                conn.close()
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
    
    # Load CSS
    load_login_css()
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    if 'user_data' not in st.session_state:
        st.session_state.user_data = None
    
    if st.session_state.logged_in:
        return True
    
    # Initialize database
    init_database()
    
    # Main container with ring animation
    st.markdown("""
    <div class="main-container">
        <div class="ring">
            <i style="--clr:#00ff0a;"></i>
            <i style="--clr:#ff0057;"></i>
            <i style="--clr:#fffd44;"></i>
        </div>
        <div class="login-form-container">
    """, unsafe_allow_html=True)
    
    # Toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", key="login_toggle", use_container_width=True):
            st.session_state.current_form = "login"
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", key="signup_toggle", use_container_width=True):
            st.session_state.current_form = "signup"
            st.rerun()
    
    # Login Form
    if st.session_state.current_form == "login":
        st.markdown("<div class='login-title'>Login</div>", unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter username", key="login_user")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_pass")
        
        if st.button("Sign In", key="login_btn", use_container_width=True):
            if not username or not password:
                st.markdown('<div class="message error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
            else:
                success, message, user_data = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.markdown(f'<div class="message success-message">✅ {message}</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f'<div class="message error-message">❌ {message}</div>', unsafe_allow_html=True)
    
    # Signup Form
    else:
        st.markdown("<div class='login-title'>Sign Up</div>", unsafe_allow_html=True)
        
        full_name = st.text_input("Full Name", placeholder="Enter full name", key="signup_name")
        username = st.text_input("Username", placeholder="Choose username", key="signup_user")
        email = st.text_input("Email", placeholder="Enter email", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="Create password", key="signup_pass")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password", key="signup_confirm")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if not all([full_name, username, email, password, confirm_password]):
                st.markdown('<div class="message error-message">❌ Please fill in all fields</div>', unsafe_allow_html=True)
            elif not is_valid_email(email):
                st.markdown('<div class="message error-message">❌ Please enter valid email</div>', unsafe_allow_html=True)
            elif password != confirm_password:
                st.markdown('<div class="message error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
            elif len(password) < 6:
                st.markdown('<div class="message error-message">❌ Password must be 6+ characters</div>', unsafe_allow_html=True)
            else:
                success, message = register_user(username, email, password, full_name)
                if success:
                    st.markdown(f'<div class="message success-message">✅ {message}</div>', unsafe_allow_html=True)
                    time.sleep(2)
                    st.session_state.current_form = "login"
                    st.rerun()
                else:
                    st.markdown(f'<div class="message error-message">❌ {message}</div>', unsafe_allow_html=True)
    
    # Links
    st.markdown("""
    <div class="links">
        <a href="#">Forgot Password?</a>
        <a href="#">Need Help?</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo info
    with st.expander("🔑 Demo Credentials"):
        st.info("""
        **Test Account:**
        - Username: **demo**
        - Password: **demo123**
        """)
    
    # Close containers
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return st.session_state.logged_in

# Test the login page
if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    if login_page():
        st.success("✅ Login successful! Redirecting...")