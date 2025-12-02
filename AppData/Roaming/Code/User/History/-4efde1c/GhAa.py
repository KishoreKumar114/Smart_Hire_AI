# app.py - SMART HIRE AI PREMIUM APPLICATION
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import random
import plotly.graph_objects as go
from login_page import show_login_page, check_authentication, show_welcome_animation

# Import your existing modules
from database import execute_query, execute_insert
# Import other modules as needed...

def load_premium_css():
    """Load premium CSS for main application"""
    st.markdown("""
    <style>
    /* Premium Theme Variables */
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
        --success: #00C853;
        --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 16px 48px rgba(0, 212, 170, 0.2);
    }
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Premium Cards with Hover Effects */
    .premium-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(0, 212, 170, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .premium-card:hover::before {
        left: 100%;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-primary);
    }
    
    /* Gradient Text */
    .gradient-text {
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }
    
    /* Navigation Styles */
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
    
    /* Add more styles as needed... */
    </style>
    """, unsafe_allow_html=True)

def create_premium_navigation():
    """Create premium navigation sidebar"""
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
    
    # Navigation pages
    pages = {
        "Dashboard": "📊",
        "Resume Screening": "📄", 
        "AI Interview Prep": "🎯",
        "JD Generator": "📝",
        "Candidates": "👥",
        "Analytics": "📈",
        "Settings": "⚙️"
    }
    
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
        st.metric("Active Jobs", "18", "2")
        st.metric("Candidates", "127", "12")
    with col2:
        st.metric("Match Rate", "87%", "3%")
        st.metric("Hiring Time", "16d", "-2d")
    
    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.session_state.current_page = "Dashboard"
        st.rerun()

def show_dashboard():
    """Show premium dashboard"""
    # Welcome message with animation
    st.markdown(f"""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 class='gradient-text' style='font-size: 2.5rem; margin-bottom: 10px;'>Welcome Back, {st.session_state.current_user}! 👋</h1>
        <p style='color: var(--text-secondary); font-size: 1.1rem;'>Ready to revolutionize your hiring process with AI-powered insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Cards
    col1, col2, col3, col4 = st.columns(4)
    
    stats = [
        {"icon": "💼", "value": "18", "label": "Active Jobs", "change": "+2"},
        {"icon": "👥", "value": "127", "label": "Candidates", "change": "+12"},
        {"icon": "🎯", "value": "87%", "label": "Match Rate", "change": "+3%"},
        {"icon": "⚡", "value": "16d", "label": "Hiring Time", "change": "-2d"}
    ]
    
    for i, stat in enumerate(stats):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class='premium-card'>
                <div style='text-align: center;'>
                    <div style='font-size: 2rem; margin-bottom: 10px;'>{stat['icon']}</div>
                    <h2 style='margin: 0; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>{stat['value']}</h2>
                    <p style='margin: 5px 0; color: var(--text-secondary);'>{stat['label']}</p>
                    <small style='color: #00D4AA;'>📈 {stat['change']}</small>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    actions = [
        {"icon": "📄", "label": "Screen Resume", "page": "Resume Screening"},
        {"icon": "🎯", "label": "Interview Prep", "page": "AI Interview Prep"},
        {"icon": "📝", "label": "Create JD", "page": "JD Generator"},
        {"icon": "👥", "label": "View Candidates", "page": "Candidates"}
    ]
    
    for i, action in enumerate(actions):
        with [col1, col2, col3, col4][i]:
            if st.button(
                f"{action['icon']} {action['label']}", 
                use_container_width=True,
                key=f"action_{i}"
            ):
                st.session_state.current_page = action['page']
                st.rerun()

# Add other page functions (show_resume_screening, show_interview_prep, etc.)
def show_resume_screening():
    st.markdown("### 📄 Resume Screening - Coming Soon!")
    st.info("AI-powered resume screening feature will be available soon!")

def show_interview_prep():
    st.markdown("### 🎯 Interview Prep - Coming Soon!")
    st.info("AI interview preparation feature will be available soon!")

def show_jd_generator():
    st.markdown("### 📝 JD Generator - Coming Soon!")
    st.info("Job description generator feature will be available soon!")

def show_candidates():
    st.markdown("### 👥 Candidates - Coming Soon!")
    st.info("Candidate management feature will be available soon!")

def show_analytics():
    st.markdown("### 📈 Analytics - Coming Soon!")
    st.info("Advanced analytics dashboard will be available soon!")

def main():
    """Main application function"""
    st.set_page_config(
        page_title="SmartHire AI - Premium",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    # Check authentication
    if not check_authentication():
        show_login_page()
        return
    
    # Load premium CSS
    load_premium_css()
    
    # Main application layout
    with st.sidebar:
        create_premium_navigation()
    
    # Main content area
    col1, col2, col3 = st.columns([1, 8, 1])
    
    with col2:
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

if __name__ == "__main__":
    main()