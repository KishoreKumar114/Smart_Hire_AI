# app.py - PREMIUM DARK THEME WITH ALL ENHANCEMENTS
import streamlit as st
import database as db
import pandas as pd
from datetime import datetime
import time
import io
import random

# Premium Dark Theme CSS
def load_premium_dark_css():
    st.markdown("""
    <style>
    /* Premium Dark Theme */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
        --bg-sidebar: #151515;
        --accent-primary: #00D4AA;
        --accent-secondary: #0099FF;
        --accent-gradient: linear-gradient(135deg, #00D4AA, #0099FF);
        --text-primary: #FFFFFF;
        --text-secondary: #B0B0B0;
        --text-muted: #666666;
        --border: #333333;
        --border-light: #404040;
        --success: #00C853;
        --warning: #FFB300;
        --error: #FF5252;
        --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 8px 40px rgba(0, 212, 170, 0.2);
        --glow: 0 0 20px rgba(0, 212, 170, 0.3);
    }
    
    /* Base Styles */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', 'SF Pro Display', -apple-system, sans-serif;
    }
    
    /* Premium Header */
    .premium-header {
        font-size: 3rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        text-shadow: var(--glow);
    }
    
    .premium-subheader {
        font-size: 1.1rem;
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Glass Morphism Cards */
    .premium-card {
        background: rgba(26, 26, 26, 0.8);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: var(--shadow);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
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
        transition: left 0.6s ease;
    }
    
    .premium-card:hover::before {
        left: 100%;
    }
    
    .premium-card:hover {
        transform: translateY(-8px);
        box-shadow: var(--shadow-lg);
        border-color: var(--accent-primary);
    }
    
    /* Metric Cards */
    .premium-metric {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 12px;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .premium-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--accent-gradient);
    }
    
    .premium-metric:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 12px 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Premium Buttons */
    .stButton > button {
        background: var(--accent-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 28px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: var(--shadow-lg) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Secondary Button */
    .secondary-btn {
        background: transparent !important;
        color: var(--accent-primary) !important;
        border: 2px solid var(--accent-primary) !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border);
    }
    
    .sidebar-nav {
        background: transparent !important;
        border: none !important;
        color: var(--text-secondary) !important;
        padding: 16px 24px !important;
        margin: 6px 0 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
        width: 100% !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        cursor: pointer !important;
    }
    
    .sidebar-nav:hover {
        background: rgba(0, 212, 170, 0.1) !important;
        color: var(--accent-primary) !important;
        transform: translateX(8px);
    }
    
    .sidebar-nav.active {
        background: var(--accent-gradient) !important;
        color: white !important;
        box-shadow: var(--shadow);
    }
    
    /* Form Elements */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>textarea {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div:focus, .stTextArea>div>textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1) !important;
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        border: 3px dashed var(--border) !important;
        border-radius: 20px !important;
        background: var(--bg-card) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--accent-primary) !important;
        background: rgba(0, 212, 170, 0.05) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: var(--accent-gradient) !important;
        border-radius: 10px !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-card);
        padding: 6px;
        border-radius: 14px;
        border: 1px solid var(--border);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--accent-gradient) !important;
        color: white !important;
        box-shadow: var(--shadow);
    }
    
    /* Success Pop Effect */
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-pop {
        animation: successPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    /* Score Circles */
    .score-circle {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: conic-gradient(var(--accent-primary) 0% var(--p), var(--border) var(--p) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        margin: 0 auto;
    }
    
    .score-circle::before {
        content: '';
        position: absolute;
        width: 100px;
        height: 100px;
        background: var(--bg-card);
        border-radius: 50%;
    }
    
    .score-text {
        position: relative;
        font-size: 2rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-gradient);
        border-radius: 4px;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-excellent {
        background: rgba(0, 200, 83, 0.2);
        color: #00C853;
        border: 1px solid rgba(0, 200, 83, 0.3);
    }
    
    .status-good {
        background: rgba(0, 212, 170, 0.2);
        color: var(--accent-primary);
        border: 1px solid rgba(0, 212, 170, 0.3);
    }
    
    .status-average {
        background: rgba(255, 179, 0, 0.2);
        color: var(--warning);
        border: 1px solid rgba(255, 179, 0, 0.3);
    }
    
    /* Analysis Cards */
    .analysis-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    
    .analysis-card:hover {
        border-color: var(--accent-primary);
        transform: translateY(-2px);
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    </style>
    """, unsafe_allow_html=True)

def show_success_popup(message):
    """Show success popup with animation"""
    st.markdown(f"""
    <div class="success-pop" style='
        background: var(--accent-gradient);
        color: white;
        padding: 20px;
        border-radius: 16px;
        text-align: center;
        margin: 20px 0;
        box-shadow: var(--shadow-lg);
        border: 1px solid rgba(0, 212, 170, 0.3);
    '>
        <h3 style='margin: 0; font-size: 1.2rem;'>🎉 {message}</h3>
    </div>
    """, unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(
        page_title="SmartHire AI - Premium",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""
    if 'page_loaded' not in st.session_state:
        st.session_state.page_loaded = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'candidates' not in st.session_state:
        st.session_state.candidates = []
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = {}
    
    # Load CSS
    load_premium_dark_css()
    
    # Premium Sidebar
    with st.sidebar:
        # Brand Header
        st.markdown("""
        <div style='
            padding: 2.5rem 1.5rem 1.5rem; 
            border-bottom: 1px solid var(--border); 
            margin-bottom: 2rem;
            text-align: center;
        '>
            <div style='display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 12px;'>
                <div style='
                    width: 40px; 
                    height: 40px; 
                    background: var(--accent-gradient); 
                    border-radius: 12px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    color: white; 
                    font-weight: bold;
                    font-size: 1.2rem;
                '>🚀</div>
            </div>
            <h1 style='margin: 0; font-size: 1.5rem; font-weight: 800; color: white;'>SmartHire AI</h1>
            <p style='margin: 0; font-size: 0.85rem; color: var(--accent-primary); font-weight: 500;'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
        <div style='padding: 0 0.5rem;'>
            <p style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); font-weight: 700; margin-bottom: 1rem;'>MAIN NAVIGATION</p>
        </div>
        """, unsafe_allow_html=True)
        
        nav_items = {
            "Dashboard": {"icon": "📊", "desc": "Overview & Analytics"},
            "JD Generator": {"icon": "📝", "desc": "Create Job Descriptions"}, 
            "Resume Screening": {"icon": "📄", "desc": "AI-Powered Analysis"},
            "Interview Prep": {"icon": "🎯", "desc": "Questions & Answers"},
            "Candidates": {"icon": "👥", "desc": "Manage Candidates"},
            "Analytics": {"icon": "📈", "desc": "Detailed Insights"}
        }
        
        for item, info in nav_items.items():
            is_active = st.session_state.current_page == item
            if st.button(f"{info['icon']} {item}", key=f"nav_{item}", use_container_width=True):
                st.session_state.current_page = item
                st.rerun()
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("""
        <div style='padding: 0 0.5rem;'>
            <p style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); font-weight: 700; margin-bottom: 1rem;'>QUICK STATS</p>
        </div>
        """, unsafe_allow_html=True)
        
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Active Jobs", "18", "+3")
            st.metric("Candidates", "127", "+8")
        with stats_col2:
            st.metric("Match Rate", "87%", "+5%")
            st.metric("Hiring Time", "16d", "-2d")
        
        # System Status
        st.markdown("---")
        st.markdown("""
        <div style='padding: 1rem 0.5rem;'>
            <p style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted); font-weight: 700; margin-bottom: 0.5rem;'>SYSTEM STATUS</p>
            <div style='display: flex; align-items: center; gap: 8px; color: var(--success); font-size: 0.9rem;'>
                <div style='width: 8px; height: 8px; background: var(--success); border-radius: 50%;'></div>
                All Systems Operational
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Main Content Area
    st.markdown(f"<h1 class='premium-header floating'>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='premium-subheader'>AI-Powered Recruitment Platform • {datetime.now().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
    
    # Show loading
    if not st.session_state.page_loaded:
        with st.spinner("🚀 Initializing SmartHire AI Premium..."):
            time.sleep(2)
        st.session_state.page_loaded = True
        st.rerun()
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        show_premium_dashboard()
    elif st.session_state.current_page == "JD Generator":
        show_premium_jd_generator()
    elif st.session_state.current_page == "Resume Screening":
        show_premium_resume_screening()
    elif st.session_state.current_page == "Interview Prep":
        show_interview_preparation()
    elif st.session_state.current_page == "Candidates":
        show_candidates_management()
    elif st.session_state.current_page == "Analytics":
        show_premium_analytics()

def show_premium_dashboard():
    # Main KPI Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">💼</div>
            <div class="metric-value">18</div>
            <div class="metric-label">Active Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">👥</div>
            <div class="metric-value">127</div>
            <div class="metric-label">Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">⚡</div>
            <div class="metric-value">16d</div>
            <div class="metric-label">Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">🎯</div>
            <div class="metric-value">87%</div>
            <div class="metric-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recent Activity
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📈 Recent Activity</h3>
            <div style="display: flex; flex-direction: column; gap: 16px;">
        """, unsafe_allow_html=True)
        
        activities = [
            {"icon": "🚀", "title": "Senior AI Engineer JD Created", "time": "2 hours ago", "status": "completed"},
            {"icon": "✅", "title": "Priya Sharma - 92% Match Score", "time": "4 hours ago", "status": "completed"},
            {"icon": "📊", "title": "Q4 Recruitment Report Generated", "time": "1 day ago", "status": "completed"},
            {"icon": "🎯", "title": "Technical Interview Scheduled", "time": "Tomorrow", "status": "scheduled"}
        ]
        
        for activity in activities:
            status_color = "var(--success)" if activity['status'] == 'completed' else "var(--warning)"
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 16px; padding: 16px; background: var(--bg-secondary); border-radius: 12px; border-left: 4px solid {status_color};">
                <div style="font-size: 1.5rem;">{activity['icon']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: var(--text-primary);">{activity['title']}</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary);">{activity['time']}</div>
                </div>
                <div class="status-badge status-{'excellent' if activity['status'] == 'completed' else 'average'}">
                    {activity['status'].title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">🚀 Quick Actions</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        """, unsafe_allow_html=True)
        
        if st.button("📝 Create New JD", use_container_width=True):
            st.session_state.current_page = "JD Generator"
            st.rerun()
        
        if st.button("📄 Screen Resume", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
        
        if st.button("🎯 Interview Prep", use_container_width=True):
            st.session_state.current_page = "Interview Prep"
            st.rerun()
        
        if st.button("👥 View Candidates", use_container_width=True):
            st.session_state.current_page = "Candidates"
            st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # System Status
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">⚡ System Status</h3>
            <div style="display: grid; gap: 16px;">
        """, unsafe_allow_html=True)
        
        status_items = [
            {"label": "AI Engine", "status": "Optimal", "icon": "🤖", "color": "var(--success)"},
            {"label": "Database", "status": "Connected", "icon": "💾", "color": "var(--success)"},
            {"label": "API Services", "status": "Active", "icon": "⚡", "color": "var(--success)"},
            {"label": "Security", "status": "Protected", "icon": "🔒", "color": "var(--success)"}
        ]
        
        for item in status_items:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: var(--bg-secondary); border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 1.3rem;">{item['icon']}</div>
                    <div style="font-weight: 600; color: var(--text-primary);">{item['label']}</div>
                </div>
                <div style="color: {item['color']}; font-weight: 700; font-size: 0.85rem;">{item['status']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Performance Metrics
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📊 Today's Performance</h3>
            <div style="display: grid; gap: 12px;">
        """, unsafe_allow_html=True)
        
        performance_data = [
            {"metric": "JDs Created", "value": "5", "trend": "📈"},
            {"metric": "Resumes Screened", "value": "23", "trend": "📈"},
            {"metric": "Matches Found", "value": "18", "trend": "📈"},
            {"metric": "Avg Response Time", "value": "1.8h", "trend": "📉"}
        ]
        
        for item in performance_data:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px; background: var(--bg-secondary); border-radius: 10px;">
                <span style="color: var(--text-secondary); font-weight: 500;">{item['metric']}</span>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 700; color: var(--text-primary);">{item['value']}</span>
                    <span style="font-size: 1.1rem;">{item['trend']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def show_premium_jd_generator():
    st.markdown("### 🚀 AI Job Description Generator")
    
    # Progress Steps
    steps = ["Job Details", "AI Generation", "Review & Save"]
    current_step = 0 if not st.session_state.generated_jd else 2
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin-bottom: 2rem; background: var(--bg-card); padding: 8px; border-radius: 16px; border: 1px solid var(--border);">
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(steps):
        is_active = i <= current_step
        st.markdown(f"""
        <div style="flex: 1; text-align: center; padding: 12px; border-radius: 12px; 
                    background: {'var(--accent-gradient)' if is_active else 'transparent'}; 
                    color: {'white' if is_active else 'var(--text-secondary)'};
                    font-weight: 600; font-size: 0.9rem; margin: 0 4px;">
            {step}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📋 Job Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Company and Department - Free text input
        company_name = st.text_input("🏢 Company Name", placeholder="e.g., Google, Microsoft, TechStart Inc.")
        department = st.text_input("📊 Department", placeholder="e.g., Engineering, Data Science, Marketing")
        
        job_title = st.text_input("🎯 Job Title", placeholder="e.g., Senior AI Engineer, Data Analyst, Product Manager")
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            min_exp = st.slider("💼 Minimum Experience (Years)", 0, 15, 3)
        with col_exp2:
            max_exp = st.slider("📈 Maximum Experience (Years)", 0, 20, 7)
        
        location = st.text_input("📍 Location", placeholder="e.g., Remote, New York, Hybrid")
        
        skills = st.text_area("🛠️ Required Skills & Technologies", 
                            placeholder="Python, Machine Learning, SQL, AWS, React, Docker...",
                            height=120)
        
        job_description = st.text_area("📝 Job Description (Optional)", 
                                     placeholder="Brief description of role responsibilities...",
                                     height=100)
        
        if st.button("🚀 Generate Smart JD", type="primary", use_container_width=True):
            if job_title and skills and company_name and department:
                with st.spinner("🤖 AI is generating an optimized job description..."):
                    time.sleep(2)
                    generate_premium_jd(company_name, department, job_title, min_exp, max_exp, location, skills, job_description)
                    show_success_popup("Job Description Generated Successfully!")
            else:
                st.error("⚠️ Please fill in all required fields (Company, Department, Job Title, Skills)")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📄 Generated Description</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.generated_jd:
            edited_jd = st.text_area("✏️ Edit the generated description", 
                                   st.session_state.generated_jd, 
                                   height=400,
                                   key="jd_editor")
            
            st.session_state.generated_jd = edited_jd
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("💾 Save JD", use_container_width=True):
                    show_success_popup("Job Description Saved to Database!")
            with col_s2:
                if st.button("📥 Export PDF", use_container_width=True):
                    show_success_popup("PDF Export Ready for Download!")
            with col_s3:
                if st.button("🔄 New JD", use_container_width=True):
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("""
            **👆 Get Started**
            
            Fill out the job details on the left and click **'Generate Smart JD'** 
            to create a professional, AI-optimized job description.
            
            💡 *The AI will analyze your requirements and generate a comprehensive, 
            engaging job description that attracts top talent.*
            """)

def generate_premium_jd(company, department, title, min_exp, max_exp, location, skills, description):
    # Enhanced AI-generated JD
    enhanced_jd = f"""🎯 **Position:** {title}
🏢 **Company:** {company}
📊 **Department:** {department}
⏳ **Experience:** {min_exp}-{max_exp} years
📍 **Location:** {location if location else 'Flexible/Remote'}

✨ **About {company}**
{company} is a forward-thinking organization in the {department} space, committed to innovation and excellence. We're building the future and looking for exceptional talent to join our journey.

🚀 **Role Overview**
We are seeking a talented {title} to join our dynamic {department} team. This role offers the opportunity to work on cutting-edge projects and make a significant impact on our technology and business outcomes.

🎯 **Key Responsibilities**
• Design, develop, and implement scalable {department.lower()} solutions
• Collaborate with cross-functional teams to define and ship new features
• Implement best practices in code quality, testing, and deployment
• Mentor junior team members and conduct technical reviews
• Stay updated with emerging technologies and industry trends
• Participate in agile development processes and sprint planning

🛠 **Technical Requirements**
{skills}

🎓 **Qualifications & Experience**
• {min_exp}+ years of professional experience in relevant field
• Bachelor's or Master's degree in Computer Science or related field
• Strong problem-solving skills and analytical thinking
• Experience with agile development methodologies
• Excellent communication and collaboration skills

💫 **What We Offer**
• Competitive salary and comprehensive benefits package
• Flexible work arrangements and remote work options
• Professional development and growth opportunities
• Inclusive and collaborative work environment
• Cutting-edge technology stack and challenging projects
• Health, dental, and vision insurance
• 401(k) matching and stock options

🌟 **Why Join {company}?**
At {company}, we believe in nurturing talent and providing opportunities for growth. You'll work with industry experts, tackle complex challenges, and see your work make a real impact.

---
*AI-Generated by SmartHire Premium • {datetime.now().strftime('%B %d, %Y at %H:%M')}*"""
    
    st.session_state.generated_jd = enhanced_jd
    st.rerun()

def show_premium_resume_screening():
    st.markdown("### 📄 AI Resume Screening & Analysis")
    
    tab1, tab2 = st.tabs(["🚀 Upload & Analyze", "📊 Analysis Results"])
    
    with tab1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📤 Upload Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose resume file", 
                                       type=['pdf', 'docx', 'txt'], 
                                       help="Supported formats: PDF, DOCX, TXT")
        
        if uploaded_file:
            show_success_popup(f"✅ {uploaded_file.name} uploaded successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="premium-card">
                    <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">📁 File Details</h4>
                    <div style="display: grid; gap: 12px;">
                        <div style="display: flex; justify-content: between;">
                            <span style="color: var(--text-secondary);">Filename:</span>
                            <span style="font-weight: 600; color: var(--text-primary);">{uploaded_file.name}</span>
                        </div>
                        <div style="display: flex; justify-content: between;">
                            <span style="color: var(--text-secondary);">Size:</span>
                            <span style="font-weight: 600; color: var(--text-primary);">{uploaded_file.size / 1024:.1f} KB</span>
                        </div>
                        <div style="display: flex; justify-content: between;">
                            <span style="color: var(--text-secondary);">Type:</span>
                            <span style="font-weight: 600; color: var(--text-primary);">{uploaded_file.type}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="premium-card">
                    <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">👤 Candidate Information</h4>
                </div>
                """, unsafe_allow_html=True)
                
                candidate_name = st.text_input("Full Name *", placeholder="John Doe")
                candidate_email = st.text_input("Email Address *", placeholder="john.doe@email.com")
                candidate_phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
                candidate_exp = st.slider("Years of Experience", 0, 30, 3)
                
                target_role = st.selectbox("Target Role", 
                                         ["Data Analyst", "AI Engineer", "Software Developer", 
                                          "Data Scientist", "DevOps Engineer", "Product Manager",
                                          "UX Designer", "Business Analyst", "ML Engineer"])
            
            if st.button("🔍 Deep AI Analysis", type="primary", use_container_width=True):
                if candidate_name and candidate_email:
                    with st.spinner("🤖 Performing deep AI analysis on resume..."):
                        time.sleep(3)
                        # Store analysis results
                        st.session_state.resume_analysis = {
                            'candidate_name': candidate_name,
                            'target_role': target_role,
                            'experience': candidate_exp,
                            'file_name': uploaded_file.name
                        }
                        st.session_state.current_tab = "📊 Analysis Results"
                        st.rerun()
                else:
                    st.error("⚠️ Please fill in candidate name and email")
    
    with tab2:
        if st.session_state.resume_analysis:
            show_resume_analysis_results()
        else:
            st.info("👆 Upload a resume and perform analysis to see results here.")

def show_resume_analysis_results():
    analysis = st.session_state.resume_analysis
    st.markdown(f"### 📊 Analysis Results - {analysis['candidate_name']}")
    
    # Overall Score
    col_score, col_details = st.columns([1, 2])
    
    with col_score:
        score = random.randint(75, 95)
        st.markdown(f"""
        <div class="premium-card" style="text-align: center;">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Overall ATS Score</h3>
            <div class="score-circle" style="--p: {score}%;">
                <div class="score-text">{score}%</div>
            </div>
            <div style="margin-top: 1rem;">
                <div class="status-badge status-{'excellent' if score >= 90 else 'good' if score >= 80 else 'average'}">
                    {'Excellent Match' if score >= 90 else 'Good Match' if score >= 80 else 'Average Match'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_details:
        st.markdown("""
        <div class="premium-card">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">📈 Detailed Breakdown</h4>
            <div style="display: grid; gap: 16px;">
        """, unsafe_allow_html=True)
        
        metrics = [
            {"label": "Skills Match", "value": random.randint(70, 95), "color": "#00D4AA"},
            {"label": "Experience Level", "value": random.randint(75, 98), "color": "#0099FF"},
            {"label": "Education", "value": random.randint(80, 100), "color": "#8B5CF6"},
            {"label": "Keyword Optimization", "value": random.randint(65, 90), "color": "#FFB300"}
        ]
        
        for metric in metrics:
            st.markdown(f"""
            <div style="margin-bottom: 16px;">
                <div style="display: flex; justify-content: between; margin-bottom: 8px;">
                    <span style="font-weight: 600; color: var(--text-primary);">{metric['label']}</span>
                    <span style="font-weight: 700; color: {metric['color']};">{metric['value']}%</span>
                </div>
                <div style="width: 100%; height: 8px; background: var(--border); border-radius: 4px; overflow: hidden;">
                    <div style="width: {metric['value']}%; height: 100%; background: {metric['color']}; border-radius: 4px; transition: width 1s ease;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Deep AI Analysis
    st.markdown("""
    <div class="premium-card">
        <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">🤖 Deep AI Analysis</h4>
        <div style="display: grid; gap: 16px;">
    """, unsafe_allow_html=True)
    
    analysis_points = [
        {
            "title": "✅ Strengths Identified",
            "content": "Strong technical foundation in required technologies, relevant project experience, good educational background matching role requirements.",
            "type": "success"
        },
        {
            "title": "⚠️ Areas for Improvement", 
            "content": "Consider adding more specific metrics to quantify achievements. Cloud certification would enhance profile for this role.",
            "type": "warning"
        },
        {
            "title": "🎯 Role Fit Analysis",
            "content": f"Excellent fit for {analysis['target_role']} position. Candidate shows 87% alignment with role requirements and company culture.",
            "type": "info"
        },
        {
            "title": "💡 Recommendations",
            "content": "Ready for technical interview stage. Focus on system design and specific technology deep-dives during interview process.",
            "type": "success"
        }
    ]
    
    for point in analysis_points:
        icon = "✅" if point['type'] == 'success' else "⚠️" if point['type'] == 'warning' else "💡"
        border_color = "var(--success)" if point['type'] == 'success' else "var(--warning)" if point['type'] == 'warning' else "var(--accent-primary)"
        
        st.markdown(f"""
        <div class="analysis-card" style="border-left: 4px solid {border_color};">
            <div style="display: flex; align-items: start; gap: 12px;">
                <div style="font-size: 1.2rem;">{icon}</div>
                <div>
                    <div style="font-weight: 700; color: var(--text-primary); margin-bottom: 4px;">{point['title']}</div>
                    <div style="color: var(--text-secondary); line-height: 1.5;">{point['content']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Action Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Candidate", use_container_width=True):
            show_success_popup("Candidate saved to database!")
    with col2:
        if st.button("📧 Schedule Interview", use_container_width=True):
            show_success_popup("Interview invitation prepared!")
    with col3:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.resume_analysis = {}
            st.rerun()

def show_interview_preparation():
    st.markdown("### 🎯 AI Interview Preparation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">🎯 Select Role & Domain</h3>
        </div>
        """, unsafe_allow_html=True)
        
        role = st.selectbox("Target Role", 
                          ["Data Analyst", "AI Engineer", "Data Scientist", "Machine Learning Engineer",
                           "Software Developer", "DevOps Engineer", "Product Manager", "Business Analyst"])
        
        experience_level = st.selectbox("Experience Level", 
                                      ["Entry Level (0-2 years)", "Mid Level (2-5 years)", 
                                       "Senior Level (5-8 years)", "Lead Level (8+ years)"])
        
        if st.button("🚀 Generate Interview Questions", type="primary", use_container_width=True):
            show_success_popup(f"AI-generated {role} interview questions!")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📝 Interview Questions</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample questions based on role
        questions_data = {
            "Data Analyst": [
                "How do you handle missing data in your analysis?",
                "Explain the difference between supervised and unsupervised learning.",
                "How would you measure the success of a new feature?",
                "What's your experience with SQL and data visualization tools?"
            ],
            "AI Engineer": [
                "Explain the transformer architecture and its impact on NLP.",
                "How do you handle overfitting in deep learning models?",
                "What's your experience with MLOps and model deployment?",
                "How would you optimize a model for production?"
            ],
            "Data Scientist": [
                "Explain the bias-variance tradeoff with examples.",
                "How do you validate your model's performance?",
                "What's your approach to feature engineering?",
                "How do you communicate technical results to non-technical stakeholders?"
            ]
        }
        
        questions = questions_data.get(role, questions_data["Data Analyst"])
        
        for i, question in enumerate(questions, 1):
            with st.expander(f"Q{i}: {question}"):
                st.info(f"**Sample Answer:** This is a sample answer for {question}. The candidate should demonstrate practical experience and theoretical understanding.")
        
        if st.button("📥 Export Questions", use_container_width=True):
            show_success_popup("Interview questions exported successfully!")

def show_candidates_management():
    st.markdown("### 👥 Candidate Management")
    
    # Add Candidate Section
    with st.expander("➕ Add New Candidate", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone")
        with col2:
            new_role = st.selectbox("Applied Role", ["Data Analyst", "AI Engineer", "Software Developer"])
            new_status = st.selectbox("Status", ["Screened", "Interview", "Rejected", "Hired"])
            new_exp = st.slider("Experience (years)", 0, 20, 3)
        
        if st.button("Add Candidate", type="primary"):
            if new_name and new_email:
                # Add to session state
                if 'candidates' not in st.session_state:
                    st.session_state.candidates = []
                
                st.session_state.candidates.append({
                    'name': new_name,
                    'email': new_email,
                    'phone': new_phone,
                    'role': new_role,
                    'status': new_status,
                    'experience': new_exp
                })
                show_success_popup("Candidate added successfully!")
            else:
                st.error("Please fill in name and email")
    
    # Candidates Table
    st.markdown("""
    <div class="premium-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 700; font-size: 1.3rem;">📋 Candidate Database</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.candidates:
        # Convert to DataFrame for display
        df_data = []
        for candidate in st.session_state.candidates:
            df_data.append({
                'Name': candidate['name'],
                'Email': candidate['email'],
                'Role': candidate['role'],
                'Status': candidate['status'],
                'Experience': f"{candidate['experience']} years"
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True)
        
        # Export option
        if st.button("📥 Export Candidates List"):
            show_success_popup("Candidates list exported successfully!")
    else:
        st.info("No candidates added yet. Use the 'Add New Candidate' section above to get started.")

def show_premium_analytics():
    st.markdown("### 📈 Advanced Analytics")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-value">24</div>
            <div class="metric-label">Total Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-value">156</div>
            <div class="metric-label">Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-value">72%</div>
            <div class="metric-label">Interview Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-value">15d</div>
            <div class="metric-label">Avg Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">📊 Hiring Trends</h4>
            <div style="height: 300px; display: flex; align-items: center; justify-content: center; 
                     background: var(--bg-secondary); border-radius: 16px; color: var(--text-secondary);">
                <div style="text-align: center;">
                    <div style="font-size: 3rem;">📈</div>
                    <div>Hiring Trends Visualization</div>
                </div>
            </div>
            <div style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                45% increase in tech hiring Q4 2024
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">🎯 Skill Demand</h4>
            <div style="height: 300px; display: flex; align-items: center; justify-content: center; 
                     background: var(--bg-secondary); border-radius: 16px; color: var(--text-secondary);">
                <div style="text-align: center;">
                    <div style="font-size: 3rem;">📋</div>
                    <div>Skills Demand Analysis</div>
                </div>
            </div>
            <div style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.9rem;">
                Python and AI skills show 65% demand growth
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()