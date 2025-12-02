import streamlit as st
import sqlite3
import hashlib
import time

def load_login_css():
    st.markdown("""
    <style>
    /* Basic reset */
    .stApp {
        background: #000000 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Main container */
    .main-container {
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        background: #000;
        position: relative;
    }
    
    /* Ring animation */
    .ring-container {
        position: absolute;
        width: 400px;
        height: 400px;
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
        border-radius: 50%;
        animation: rotate 6s linear infinite;
    }
    
    .ring i:nth-child(1) {
        border-color: #00ff0a;
        animation-duration: 4s;
    }
    
    .ring i:nth-child(2) {
        border-color: #ff0057;
        animation-duration: 6s;
        animation-direction: reverse;
    }
    
    .ring i:nth-child(3) {
        border-color: #fffd44;
        animation-duration: 8s;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Login form */
    .login-form {
        position: relative;
        z-index: 10;
        background: rgba(0, 0, 0, 0.8);
        padding: 40px 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        width: 350px;
    }
    
    /* Input styling */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        padding: 12px 15px !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    .stTextInput input:focus {
        border-color: #ff0057 !important;
        box-shadow: 0 0 10px rgba(255, 0, 87, 0.5) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #ff0057, #fffd44) !important;
        color: black !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px !important;
        font-weight: 600 !important;
        margin-top: 10px !important;
    }
    
    /* Title */
    .title {
        text-align: center;
        color: white;
        font-size: 2.5em;
        margin-bottom: 10px;
        background: linear-gradient(45deg, #00ff0a, #ff0057, #fffd44);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

def init_database():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    
    # Add demo user
    c.execute('SELECT * FROM users WHERE username = "demo"')
    if not c.fetchone():
        demo_hash = hashlib.sha256("demo123".encode()).hexdigest()
        c.execute('INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)',
                 ("demo", demo_hash, "Demo User"))
    
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):
        return True, "Login successful!", {"username": user[1], "full_name": user[3]}
    return False, "Invalid credentials", None

def login_page():
    """Login page with ring animation"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    
    if st.session_state.logged_in:
        return True
    
    # Load CSS and init DB
    load_login_css()
    init_database()
    
    # Main container with rings
    st.markdown("""
    <div class="main-container">
        <div class="ring-container">
            <div class="ring">
                <i></i>
                <i></i>
                <i></i>
            </div>
        </div>
        
        <div class="login-form">
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown("<div class='title'>🚀 SmartHire AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Premium Recruitment Platform</div>", unsafe_allow_html=True)
    
    # Toggle buttons
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
        st.subheader("Login to Your Account")
        
        username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
        
        if st.button("Sign In", type="primary", use_container_width=True):
            if username and password:
                success, message, user_data = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.success(message)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")
    
    # Signup Form
    else:
        st.subheader("Create New Account")
        
        full_name = st.text_input("Full Name", placeholder="Enter your full name", label_visibility="collapsed")
        username = st.text_input("Username", placeholder="Choose a username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Create password", label_visibility="collapsed")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password", label_visibility="collapsed")
        
        if st.button("Create Account", type="primary", use_container_width=True):
            if all([full_name, username, password, confirm_password]):
                if password == confirm_password:
                    # Simple registration
                    conn = sqlite3.connect('users.db', check_same_thread=False)
                    c = conn.cursor()
                    try:
                        password_hash = hash_password(password)
                        c.execute('INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)',
                                 (username, password_hash, full_name))
                        conn.commit()
                        conn.close()
                        st.success("Account created successfully! Please login.")
                        st.session_state.current_form = "login"
                        st.rerun()
                    except:
                        conn.close()
                        st.error("Username already exists")
                else:
                    st.error("Passwords don't match")
            else:
                st.error("Please fill all fields")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #888;'>
        <strong>Demo Account:</strong> demo / demo123
    </div>
    """, unsafe_allow_html=True)
    
    # Close containers
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    return False

# Test directly
if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered"
    )
    
    if login_page():
        st.success("✅ Welcome to SmartHire AI!")
        st.balloons()
    else:
        st.stop()