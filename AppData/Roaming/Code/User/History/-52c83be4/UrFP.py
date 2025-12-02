import streamlit as st
import sqlite3
import hashlib
import time

def load_login_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    /* COMPLETE RESET */
    .stApp {
        background: #111 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        font-family: 'Quicksand', sans-serif !important;
    }
    
    /* Hide Streamlit elements */
    header { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    
    /* Main container */
    .main-container {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        width: 100vw !important;
        height: 100vh !important;
        background: #111 !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }
    
    /* Ring container - FORM IS INSIDE THIS */
    .ring-with-form {
        position: relative;
        width: 500px;
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    /* Ring animation */
    .ring {
        position: absolute;
        width: 100%;
        height: 100%;
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
        border-color: #00ff0a;
    }
    
    .ring i:nth-child(2) {
        border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
        animation: animate 4s linear infinite;
        border-color: #ff0057;
    }
    
    .ring i:nth-child(3) {
        border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
        animation: animate2 10s linear infinite;
        border-color: #fffd44;
    }
    
    .ring:hover i {
        border-width: 4px !important;
        filter: drop-shadow(0 0 20px var(--clr)) !important;
    }
    
    @keyframes animate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes animate2 {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }
    
    /* Login form - INSIDE THE RING */
    .login-form {
        position: relative;
        z-index: 100;
        background: rgba(0, 0, 0, 0.9);
        padding: 40px 35px;
        border-radius: 20px;
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        width: 320px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.8);
    }
    
    /* Title inside ring */
    .form-title {
        color: white !important;
        font-size: 2em !important;
        text-align: center !important;
        margin-bottom: 5px !important;
        font-weight: 700 !important;
        background: linear-gradient(45deg, #00ff0a, #ff0057, #fffd44);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .form-subtitle {
        color: rgba(255, 255, 255, 0.7) !important;
        text-align: center !important;
        margin-bottom: 30px !important;
        font-size: 0.9em !important;
    }
    
    /* Input styling */
    div[data-testid="stTextInput"] {
        margin-bottom: 20px !important;
    }
    
    div[data-testid="stTextInput"] label {
        display: none !important;
    }
    
    div[data-testid="stTextInput"] input {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 14px 20px !important;
        width: 100% !important;
        font-size: 14px !important;
        font-family: 'Quicksand', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stTextInput"] input::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #ff0057 !important;
        box-shadow: 0 0 15px rgba(255, 0, 87, 0.5) !important;
        outline: none !important;
    }
    
    /* Button styling */
    div[data-testid="stButton"] {
        margin-top: 10px !important;
    }
    
    div[data-testid="stButton"] button {
        width: 100% !important;
        background: linear-gradient(45deg, #ff0057, #fffd44) !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 14px !important;
        color: black !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        font-family: 'Quicksand', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(255, 0, 87, 0.4) !important;
    }
    
    /* Toggle buttons */
    .toggle-container {
        display: flex;
        gap: 10px;
        margin-bottom: 25px;
    }
    
    /* Links */
    .form-links {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
        padding: 0 10px;
    }
    
    .form-links a {
        color: rgba(255, 255, 255, 0.7);
        text-decoration: none;
        font-size: 12px;
        font-family: 'Quicksand', sans-serif;
        transition: color 0.3s ease;
    }
    
    .form-links a:hover {
        color: #ff0057;
        text-decoration: underline;
    }
    
    /* Messages */
    .alert-box {
        padding: 12px 16px;
        border-radius: 10px;
        margin: 15px 0;
        text-align: center;
        font-family: 'Quicksand', sans-serif;
        font-size: 14px;
        border: 1px solid;
    }
    
    .alert-success {
        background: rgba(0, 255, 0, 0.1);
        border-color: rgba(0, 255, 0, 0.3);
        color: #00ff88;
    }
    
    .alert-error {
        background: rgba(255, 0, 0, 0.1);
        border-color: rgba(255, 0, 0, 0.3);
        color: #ff6b6b;
    }
    
    /* Demo expander */
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
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    
    # Create demo user
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
    
    try:
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        
        if user and user[2] == hash_password(password):
            user_data = {
                'username': user[1],
                'full_name': user[3]
            }
            conn.close()
            return True, "🎉 Login successful! Redirecting...", user_data
        else:
            conn.close()
            return False, "❌ Invalid username or password", None
    except Exception as e:
        conn.close()
        return False, f"❌ Login error: {str(e)}", None

def register_user(username, password, full_name):
    conn = sqlite3.connect('users.db', check_same_thread=False)
    c = conn.cursor()
    
    try:
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        if c.fetchone():
            return False, "❌ Username already exists"
        
        password_hash = hash_password(password)
        c.execute('INSERT INTO users (username, password_hash, full_name) VALUES (?, ?, ?)',
                 (username, password_hash, full_name))
        conn.commit()
        conn.close()
        return True, "✅ Account created! Please login."
    except Exception as e:
        conn.close()
        return False, f"❌ Registration failed: {str(e)}"

def login_page():
    """Main login page - FORM INSIDE RING"""
    
    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_form' not in st.session_state:
        st.session_state.current_form = "login"
    
    if st.session_state.logged_in:
        return True
    
    # Load CSS and initialize database
    load_login_css()
    init_database()
    
    # Main container with ring AND form together
    st.markdown("""
    <div class="main-container">
        <div class="ring-with-form">
            <!-- Ring Animation -->
            <div class="ring">
                <i style="--clr:#00ff0a;"></i>
                <i style="--clr:#ff0057;"></i>
                <i style="--clr:#fffd44;"></i>
            </div>
            
            <!-- Login Form INSIDE the ring -->
            <div class="login-form">
    """, unsafe_allow_html=True)
    
    # Form content
    st.markdown("<div class='form-title'>🚀 SmartHire AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='form-subtitle'>Premium Recruitment Platform</div>", unsafe_allow_html=True)
    
    # Toggle buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔐 Login", 
                    key="btn_login", 
                    use_container_width=True,
                    type="primary" if st.session_state.current_form == "login" else "secondary"):
            st.session_state.current_form = "login"
            st.rerun()
    
    with col2:
        if st.button("📝 Sign Up", 
                     key="btn_signup", 
                     use_container_width=True,
                     type="primary" if st.session_state.current_form == "signup" else "secondary"):
            st.session_state.current_form = "signup"
            st.rerun()
    
    st.markdown("---")
    
    # Login Form
    if st.session_state.current_form == "login":
        username = st.text_input(
            "Username",
            placeholder="Enter username", 
            key="login_username",
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "Password",
            placeholder="Enter password",
            type="password", 
            key="login_password",
            label_visibility="collapsed"
        )
        
        if st.button("🚀 Sign In", key="btn_signin", use_container_width=True, type="primary"):
            if username and password:
                success, message, user_data = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data
                    st.markdown(f'<div class="alert-box alert-success">{message}</div>', unsafe_allow_html=True)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.markdown(f'<div class="alert-box alert-error">{message}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-box alert-error">❌ Please fill in all fields</div>', unsafe_allow_html=True)
    
    # Signup Form
    else:
        full_name = st.text_input(
            "Full Name",
            placeholder="Full name",
            key="signup_name", 
            label_visibility="collapsed"
        )
        
        username = st.text_input(
            "Username", 
            placeholder="Choose username",
            key="signup_username",
            label_visibility="collapsed"
        )
        
        password = st.text_input(
            "Password",
            placeholder="Create password", 
            type="password",
            key="signup_password",
            label_visibility="collapsed"
        )
        
        confirm_password = st.text_input(
            "Confirm Password",
            placeholder="Confirm password",
            type="password",
            key="signup_confirm", 
            label_visibility="collapsed"
        )
        
        if st.button("🎯 Create Account", key="btn_create", use_container_width=True, type="primary"):
            if all([full_name, username, password, confirm_password]):
                if password == confirm_password:
                    success, message = register_user(username, password, full_name)
                    if success:
                        st.markdown(f'<div class="alert-box alert-success">{message}</div>', unsafe_allow_html=True)
                        time.sleep(2)
                        st.session_state.current_form = "login"
                        st.rerun()
                    else:
                        st.markdown(f'<div class="alert-box alert-error">{message}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="alert-box alert-error">❌ Passwords do not match</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-box alert-error">❌ Please fill all fields</div>', unsafe_allow_html=True)
    
    # Links
    st.markdown("""
    <div class="form-links">
        <a href="#">Forgot Password?</a>
        <a href="#">Need Help?</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo info
    with st.expander("🔑 Demo Account", expanded=False):
        st.markdown("""
        **Username:** `demo`  
        **Password:** `demo123`
        """)
    
    # Close the form and containers
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return False

# Test directly
if __name__ == "__main__":
    st.set_page_config(
        page_title="SmartHire AI - Login",
        page_icon="🚀",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    if login_page():
        st.balloons()
        st.success("Welcome to SmartHire AI!")
    else:
        st.stop()