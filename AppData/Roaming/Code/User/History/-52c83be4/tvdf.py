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
    elif score