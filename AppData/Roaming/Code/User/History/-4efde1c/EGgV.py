# app.py - SMART HIRE AI WITH PREMIUM LOGIN PAGE
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import plotly.graph_objects as go
import PyPDF2
import io
from docx import Document

# Import email configuration
try:
    from email_config import get_email_config, validate_email_config
    EMAIL_CONFIG = get_email_config()
    EMAIL_ENABLED = True
except ImportError:
    st.error("❌ email_config.py file not found. Please create the configuration file.")
    EMAIL_ENABLED = False
    EMAIL_CONFIG = {}

# Session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'show_login' not in st.session_state:
    st.session_state.show_login = True

# Demo credentials
DEMO_CREDENTIALS = {
    "admin": "admin123",
    "hr": "hr123",
    "recruiter": "recruiter123"
}

# Ultra Premium Theme CSS with Login Styles
def load_ultra_premium_css():
    st.markdown("""
    <style>
    /* Ultra Premium Theme */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
        --bg-sidebar: #1a1a1a;
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
    
    /* Login Page Styles */
    .login-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        background: #0A0A0A;
        width: 100%;
        overflow: hidden;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 9999;
    }
    
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
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    @keyframes animate2 {
        0% {
            transform: rotate(360deg);
        }
        100% {
            transform: rotate(0deg);
        }
    }
    
    .login-box {
        position: absolute;
        width: 400px;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 25px;
        z-index: 1000;
    }
    
    .login-logo {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .login-logo-icon {
        font-size: 4rem !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        display: block;
    }
    
    .login-logo-text {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 !important;
    }
    
    .login-logo-subtext {
        font-size: 1rem !important;
        color: var(--text-secondary) !important;
        margin: 0.2rem 0 0 0 !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
    }
    
    .login-title {
        font-size: 2em;
        color: #fff;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .login-subtitle {
        color: var(--text-secondary);
        margin-bottom: 30px;
        text-align: center;
        font-size: 1.1em;
    }
    
    .inputBx {
        position: relative;
        width: 100%;
        margin: 15px 0;
    }
    
    .inputBx input {
        position: relative;
        width: 100%;
        padding: 15px 25px;
        background: rgba(255, 255, 255, 0.1);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 40px;
        font-size: 1.1em;
        color: #fff;
        box-shadow: none;
        outline: none;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .inputBx input:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 20px rgba(0, 212, 170, 0.3);
    }
    
    .inputBx input[type="submit"] {
        width: 100%;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        border: none;
        cursor: pointer;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .inputBx input[type="submit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 212, 170, 0.4);
    }
    
    .inputBx input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    .login-links {
        position: relative;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 10px;
        margin-top: 20px;
    }
    
    .login-links a {
        color: var(--text-secondary);
        text-decoration: none;
        font-size: 0.9em;
        transition: color 0.3s ease;
    }
    
    .login-links a:hover {
        color: var(--accent-primary);
    }
    
    .demo-credentials {
        background: rgba(0, 212, 170, 0.1);
        border: 1px solid rgba(0, 212, 170, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin-top: 20px;
        text-align: center;
    }
    
    .demo-credentials h4 {
        color: var(--accent-primary);
        margin-bottom: 10px;
    }
    
    .demo-credentials p {
        color: var(--text-secondary);
        font-size: 0.9em;
        margin: 5px 0;
    }
    
    /* Hide Streamlit elements on login page */
    .login-container ~ * {
        display: none !important;
    }

    /* Fix ALL text colors to white */
    .st-emotion-cache-3qzj0x p, 
    .st-emotion-cache-3qzj0x ol, 
    .st-emotion-cache-3qzj0x ul, 
    .st-emotion-cache-3qzj0x dl, 
    .st-emotion-cache-3qzj0x li {
        color: white !important;
    }
    
    /* Fix file uploader text color */
    .stFileUploader label p {
        color: white !important;
    }
    
    .stFileUploader label {
        color: white !important;
    }
    
    /* Fix Date Input text color */
    .stDateInput input {
        color: white !important;
    }
    
    .stDateInput > div > div > input {
        color: white !important;
    }
    
    /* Fix all input text colors */
    input, textarea, select {
        color: white !important;
    }
    
    /* Fix text area content color */
    .stTextArea textarea {
        color: white !important;
    }
    
    /* Fix select box text color */
    .stSelectbox > div > div {
        color: white !important;
    }
    
    /* Fix text input color */
    .stTextInput input {
        color: white !important;
    }
    
    /* JD Generator Specific - Black Text on White Background */
    .jd-generator-input input,
    .jd-generator-input textarea,
    .jd-generator-input .stSelectbox > div > div {
        background: white !important;
        color: black !important;
        border: 2px solid #00D4AA !important;
    }
    
    .jd-generator-input input::placeholder,
    .jd-generator-input textarea::placeholder {
        color: #666666 !important;
    }
    
    /* SPECIFIC FIX FOR JD GENERATOR OUTPUT TEXTAREA */
    .jd-generator-output textarea {
        background: white !important;
        color: black !important;
        border: 2px solid #0099FF !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* HIGH SPECIFICITY OVERRIDE FOR JD GENERATOR */
    div[data-testid="stTextArea"] textarea.jd-output {
        background: white !important;
        color: black !important;
    }
    
    /* Force black text in specific text areas */
    textarea[value*="#"] {
        color: black !important;
        background: white !important;
    }
    
    /* Sidebar - Dark Color */
    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    .st-emotion-cache-1legitb {
        background: var(--bg-sidebar) !important;
    }
    
    /* Navigation Button Styles */
    .nav-button {
        width: 100%;
        text-align: left;
        padding: 12px 16px;
        margin: 5px 0;
        border: none;
        border-radius: 8px;
        background: transparent;
        color: var(--text-secondary);
        font-size: 14px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background: rgba(0, 212, 170, 0.1);
        color: var(--accent-primary);
        transform: translateX(5px);
    }
    
    .nav-button.active {
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    .nav-button.active::before {
        content: "▶";
        margin-right: 8px;
        font-size: 12px;
    }
    
    /* Fix Select Box Background */
    .stSelectbox > div > div {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: var(--accent-primary) !important;
    }
    
    /* Input Fields - Dark Background with White Text */
    .stTextInput>div>div>input, .stTextArea>div>textarea {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Date Input and Time Input */
    .stDateInput > div > div, .stTimeInput > div > div {
        background: var(--input-bg) !important;
        color: var(--input-text) !important;
        border: 2px solid var(--border) !important;
        border-radius: 10px !important;
    }
    
    /* Premium Header with Logo */
    .premium-header {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 2rem;
    }
    
    .logo {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    /* Premium Cards */
    .premium-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Success Animation */
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-pop {
        animation: successPop 0.6s ease-out;
    }
    
    /* Horizontal button layout for candidates */
    .horizontal-buttons {
        display: flex !important;
        flex-direction: row !important;
        gap: 10px !important;
        margin-top: 10px !important;
    }
    
    .horizontal-buttons .stButton {
        flex: 1 !important;
    }
    
    /* Dashboard Description */
    .dashboard-description {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        line-height: 1.6;
    }
    
    /* Fix text in text areas and inputs */
    .stTextArea textarea, .stTextInput input {
        color: white !important;
    }
    
    /* Fix placeholder text color */
    ::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Fix all Streamlit text elements */
    .stMarkdown, .stText, .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
        color: white !important;
    }
    
    /* Current Page Indicator */
    .current-page-indicator {
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    /* HIGH PRIORITY OVERRIDES FOR JD GENERATOR */
    [data-testid="stTextArea"] textarea {
        color: inherit !important;
    }
    
    /* Specific override for JD output */
    div[data-testid="stTextArea"] textarea[aria-label="Job Description Content"] {
        background: white !important;
        color: black !important;
        border: 2px solid #0099FF !important;
    }
    </style>
    """, unsafe_allow_html=True)

def show_login_page():
    """Show the premium login page"""
    st.markdown("""
    <div class="login-container">
        <div class="ring">
            <i style="--clr:#00ff0a;"></i>
            <i style="--clr:#ff0057;"></i>
            <i style="--clr:#fffd44;"></i>
            <div class="login-box">
                <div class="login-logo">
                    <div class="login-logo-icon">🚀</div>
                    <div class="login-logo-text">SmartHire AI</div>
                    <div class="login-logo-subtext">Premium Recruitment Platform</div>
                </div>
                
                <h2 class="login-title">Welcome Back</h2>
                <p class="login-subtitle">Sign in to access your recruitment dashboard</p>
                
                <div class="inputBx">
                    <input type="text" id="username" placeholder="Username" autocomplete="username">
                </div>
                <div class="inputBx">
                    <input type="password" id="password" placeholder="Password" autocomplete="current-password">
                </div>
                <div class="inputBx">
                    <input type="submit" id="login-btn" value="Sign in">
                </div>
                
                <div class="login-links">
                    <a href="#">Forget Password</a>
                    <a href="#">Signup</a>
                </div>
                
                <div class="demo-credentials">
                    <h4>Demo Credentials</h4>
                    <p><strong>Username:</strong> admin | <strong>Password:</strong> admin123</p>
                    <p><strong>Username:</strong> hr | <strong>Password:</strong> hr123</p>
                    <p><strong>Username:</strong> recruiter | <strong>Password:</strong> recruiter123</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login functionality
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("🚀 Sign In")
            
            if login_button:
                if username in DEMO_CREDENTIALS and password == DEMO_CREDENTIALS[username]:
                    st.session_state.authenticated = True
                    st.session_state.show_login = False
                    st.session_state.current_user = username
                    st.success(f"✅ Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")

# AI Question Bank with Questions & Answers
AI_QUESTION_BANK = {
    "Data Science": [
        {
            "question": "Explain the bias-variance tradeoff in machine learning",
            "answer": "The bias-variance tradeoff is a fundamental concept in ML where:\n\n• **High Bias**: Model is too simple, underfits the data (e.g., linear regression for complex patterns)\n• **High Variance**: Model is too complex, overfits the data (e.g., deep neural networks with little data)\n• **Tradeoff**: As model complexity increases, bias decreases but variance increases\n\n**Solution**: Use cross-validation, regularization, and ensemble methods to find the right balance.",
            "type": "Technical",
            "difficulty": "Intermediate"
        },
        {
            "question": "How do you handle missing data in your datasets?",
            "answer": "Missing data handling strategies:\n\n1. **Deletion**: Remove rows/columns if missing data <5%\n2. **Mean/Median/Mode Imputation**: For numerical/categorical data\n3. **Predictive Imputation**: Use ML models to predict missing values\n4. **K-Nearest Neighbors**: Impute based on similar records\n5. **Advanced Methods**: MICE (Multiple Imputation by Chained Equations)\n\n**Best Practice**: Always analyze why data is missing (MCAR, MAR, MNAR) before choosing method.",
            "type": "Technical", 
            "difficulty": "Intermediate"
        },
        {
            "question": "What's the difference between L1 and L2 regularization?",
            "answer": "L1 vs L2 Regularization:\n\n**L1 (Lasso)**:\n• Adds absolute value of coefficients to loss function\n• Can reduce coefficients to exactly zero\n• Performs feature selection\n• Good for sparse models\n\n**L2 (Ridge)**:\n• Adds squared value of coefficients to loss function\n• Shrinks coefficients but never to zero\n• Handles multicollinearity well\n• More stable than L1\n\n**Use Case**: L1 for feature selection, L2 to prevent overfitting.",
            "type": "Technical",
            "difficulty": "Advanced"
        }
    ],
    "AI Engineering": [
        {
            "question": "Explain transformer architecture in NLP",
            "answer": "Transformer Architecture Key Components:\n\n1. **Self-Attention Mechanism**: Weights importance of different words\n2. **Multi-Head Attention**: Multiple attention heads capture different relationships\n3. **Positional Encoding**: Adds sequence order information\n4. **Feed-Forward Networks**: Applies non-linear transformations\n5. **Layer Normalization**: Stabilizes training\n\n**Advantages**:\n• Parallel processing (unlike RNNs)\n• Captures long-range dependencies\n• Scalable to large datasets\n\n**Applications**: BERT, GPT, T5 models",
            "type": "Technical",
            "difficulty": "Advanced"
        },
        {
            "question": "How do you optimize model inference speed?",
            "answer": "Model Inference Optimization Techniques:\n\n1. **Quantization**: Reduce precision (FP32 → FP16/INT8)\n2. **Pruning**: Remove unimportant weights\n3. **Knowledge Distillation**: Train smaller model from large model\n4. **Model Compression**: Architecture search for efficiency\n5. **Hardware Acceleration**: GPU/TPU optimization\n6. **Batching**: Process multiple inputs together\n7. **Caching**: Store frequent inference results\n\n**Tools**: TensorRT, ONNX Runtime, OpenVINO",
            "type": "Technical",
            "difficulty": "Advanced"
        },
        {
            "question": "What's your experience with MLOps practices?",
            "answer": "MLOps Key Practices:\n\n1. **Version Control**: DVC for data, Git for code\n2. **CI/CD**: Automated testing and deployment\n3. **Model Registry**: Track model versions and lineage\n4. **Monitoring**: Model performance and data drift detection\n5. **Feature Store**: Centralized feature management\n6. **Experiment Tracking**: MLflow, Weights & Biases\n7. **Automated Retraining**: Pipeline orchestration\n\n**Tools**: Kubeflow, MLflow, Airflow, Docker, Kubernetes",
            "type": "Technical",
            "difficulty": "Intermediate"
        }
    ]
}

# ... (Keep all your existing functions: extract_text_from_pdf, extract_text_from_docx, extract_info_from_resume, send_real_email, show_success_popup, create_trend_chart, get_ai_questions)

def create_premium_navigation():
    """Create premium navigation with user info"""
    pages = {
        "Dashboard": "📊",
        "Resume Screening": "📄", 
        "AI Interview Prep": "🎯",
        "JD Generator": "📝",
        "Candidates": "👥",
        "Analytics": "📈"
    }
    
    # User info at top
    st.markdown(f"""
    <div style='text-align: center; padding: 20px 0;'>
        <div style='font-size: 2.5rem; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>🚀</div>
        <h1 style='margin: 10px 0; color: white;'>SmartHire AI</h1>
        <p style='margin: 0; color: #E0E0E0;'>Premium Recruitment Platform</p>
        <div style='background: rgba(0, 212, 170, 0.2); padding: 8px 16px; border-radius: 20px; margin-top: 10px;'>
            <p style='margin: 0; color: #00D4AA; font-size: 0.9rem;'>Welcome, {st.session_state.current_user}!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Navigation buttons
    for page, icon in pages.items():
        if st.button(f"{icon} {page}", 
                    use_container_width=True, 
                    key=f"nav_{page}",
                    type="primary" if st.session_state.current_page == page else "secondary"):
            st.session_state.current_page = page
            st.rerun()
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("**📊 Quick Stats**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Active Jobs", "18")
        st.metric("Candidates", "127")
    with col2:
        st.metric("Match Rate", "87%")
        st.metric("Hiring Time", "16d")
    
    # Logout button at bottom
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.show_login = True
        st.rerun()

def main():
    st.set_page_config(
        page_title="SmartHire AI - Premium",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = {}
    if 'candidates' not in st.session_state:
        st.session_state.candidates = []
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""
    if 'jd_created' not in st.session_state:
        st.session_state.jd_created = False
    if 'ai_questions' not in st.session_state:
        st.session_state.ai_questions = []
    if 'current_user' not in st.session_state:
        st.session_state.current_user = "Guest"
    
    load_ultra_premium_css()
    
    # Show login page if not authenticated
    if not st.session_state.authenticated:
        show_login_page()
        return
    
    # Main application after login
    with st.sidebar:
        create_premium_navigation()
    
    # Main Content with Current Page Indicator
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🚀</div>
        <h1 class="premium-header">SmartHire.AI</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Current Page Indicator
    st.markdown(f"""
    <div class="current-page-indicator">
        📍 Currently Viewing: {st.session_state.current_page} | 👤 User: {st.session_state.current_user}
    </div>
    """, unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Resume Screening":
        show_resume_screening()
    elif st.session_state.current_page == "AI Interview Prep":
        show_interview_prep()
    elif st.session_state.current_page == "JD Generator":
        show_jd_generator()
    elif st.session_state.current_page == "Candidates":
        show_candidates()
    elif st.session_state.current_page == "Analytics":
        show_analytics()

# ... (Keep all your existing page functions: show_dashboard, show_resume_screening, show_interview_prep, show_jd_generator, show_candidates, show_analytics)

def show_dashboard():
    # Dashboard Description
    st.markdown("""
    <div class="dashboard-description">
        <h3>🚀 Welcome to SmartHire AI - Your Intelligent Recruitment Partner</h3>
        <p>Streamline your hiring process with AI-powered tools for resume screening, interview preparation, 
        candidate management, and data-driven insights. Save time, make better hiring decisions, and find 
        the perfect candidates faster.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">💼</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">18</h2>
            <p style="text-align: center; color: var(--text-secondary);">Active Jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">👥</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">127</h2>
            <p style="text-align: center; color: var(--text-secondary);">Candidates</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">🎯</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">87%</h2>
            <p style="text-align: center; color: var(--text-secondary);">Match Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-card">
            <h3 style="text-align: center;">⚡</h3>
            <h2 style="text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">16d</h2>
            <p style="text-align: center; color: var(--text-secondary);">Hiring Time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Screen Resume", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    
    with col2:
        if st.button("🎯 Interview Prep", use_container_width=True):
            st.session_state.current_page = "AI Interview Prep"
            st.rerun()
    
    with col3:
        if st.button("📝 Create JD", use_container_width=True):
            st.session_state.current_page = "JD Generator"
            st.rerun()
    
    with col4:
        if st.button("👥 View Candidates", use_container_width=True):
            st.session_state.current_page = "Candidates"
            st.rerun()

# ... (Keep all your other page functions exactly as they were)

if __name__ == "__main__":
    main()