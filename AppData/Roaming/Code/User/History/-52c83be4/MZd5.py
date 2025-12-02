import streamlit as st
import sqlite3
import hashlib
import time

# Simple CSS without conflicts
def load_simple_css():
    st.markdown("""
    <style>
    .stApp {
        background: #000000;
    }
    
    /* Simple dark theme */
    .main {
        background: #000000;
        color: white;
        padding: 50px;
    }
    
    /* Center the form */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 40px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Input styling */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(45deg, #FF0080, #FF8C00) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        width: 100% !important;
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
    """Simple login page that definitely works"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    
    if st.session_state.logged_in:
        return True
    
    # Load simple CSS
    load_simple_css()
    init_database()
    
    # Main container
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Title
    st.markdown("<h1 style='text-align: center; color: white;'>🚀 SmartHire AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #ccc;'>Premium Recruitment Platform</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
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
        
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
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
    
    # Signup Form (Simple version)
    else:
        st.subheader("Create New Account")
        st.info("Signup functionality coming soon. Use demo account for now.")
        
        st.markdown("""
        **Demo Account:**
        - **Username:** `demo`
        - **Password:** `demo123`
        """)
        
        if st.button("Use Demo Account", type="primary", use_container_width=True):
            success, message, user_data = login_user("demo", "demo123")
            if success:
                st.session_state.logged_in = True
                st.session_state.user_data = user_data
                st.success("Demo login successful!")
                time.sleep(1)
                st.rerun()
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #888;'>Need help? Contact support</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    return False

# Test directly
if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered"
    )
    
    if login_page():
        st.success("✅ Logged in successfully!")
        st.balloons()
    else:
        st.stop()