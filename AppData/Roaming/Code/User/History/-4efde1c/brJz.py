# app.py - URBAN DISTRICT PLANNER STYLE DESIGN
import streamlit as st
import database as db
import pandas as pd
from datetime import datetime
import time
import io

# Urban District Planner Inspired CSS
def load_urban_design_css():
    st.markdown("""
    <style>
    /* Urban District Planner Color Scheme */
    :root {
        --primary: #0EA5E9;
        --primary-dark: #0284C7;
        --primary-light: #38BDF8;
        --secondary: #64748B;
        --accent: #8B5CF6;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8FAFC;
        --bg-sidebar: #0F172A;
        --text-primary: #1E293B;
        --text-secondary: #475569;
        --text-light: #64748B;
        --border: #E2E8F0;
        --border-light: #F1F5F9;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03);
    }
    
    .dark-mode {
        --bg-primary: #0F172A;
        --bg-secondary: #1E293B;
        --bg-sidebar: #0F172A;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --text-light: #94A3B8;
        --border: #334155;
        --border-light: #1E293B;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.2);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.2), 0 4px 6px -2px rgba(0, 0, 0, 0.1);
    }
    
    /* Base Styles */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        line-height: 1.6;
    }
    
    /* Urban Style Header */
    .urban-header {
        font-size: 2.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.025em;
    }
    
    .urban-subheader {
        font-size: 1rem;
        color: var(--text-secondary);
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Glass Morphism Cards */
    .urban-card {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .urban-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .urban-card:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
        border-color: var(--primary-light);
    }
    
    .urban-card:hover::before {
        opacity: 1;
    }
    
    /* Metric Cards with Urban Style */
    .urban-metric {
        background: var(--bg-primary);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin: 8px;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
        position: relative;
    }
    
    .urban-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 16px 16px 0 0;
    }
    
    .urban-metric:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: var(--text-primary);
        margin: 8px 0;
        letter-spacing: -0.025em;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-change {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 8px;
        border-radius: 12px;
        margin-top: 4px;
        display: inline-block;
    }
    
    .change-positive {
        background: #DCFCE7;
        color: #166534;
    }
    
    .change-negative {
        background: #FEE2E2;
        color: #991B1B;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: var(--shadow-md);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        background: linear-gradient(135deg, var(--primary-dark), var(--primary));
    }
    
    /* Secondary Button */
    .secondary-button {
        background: transparent !important;
        color: var(--primary) !important;
        border: 1.5px solid var(--primary) !important;
    }
    
    .secondary-button:hover {
        background: var(--primary) !important;
        color: white !important;
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
        padding: 16px 20px !important;
        margin: 4px 0 !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
        width: 100% !important;
        font-weight: 500 !important;
    }
    
    .sidebar-nav:hover {
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        transform: translateX(4px);
    }
    
    .sidebar-nav.active {
        background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
        color: white !important;
        box-shadow: var(--shadow-md);
    }
    
    /* Form Elements */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>textarea {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 0.875rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div:focus, .stTextArea>div>textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.1) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--primary), var(--accent)) !important;
        border-radius: 8px !important;
    }
    
    /* File Uploader */
    .stFileUploader > div > div {
        border: 2px dashed var(--border) !important;
        border-radius: 16px !important;
        background: var(--bg-secondary) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader > div > div:hover {
        border-color: var(--primary) !important;
        background: var(--bg-primary) !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--bg-secondary);
        padding: 4px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: var(--text-primary) !important;
        box-shadow: var(--shadow-md);
    }
    
    /* Dataframe Styling */
    .dataframe {
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .status-active {
        background: #DCFCE7;
        color: #166534;
    }
    
    .status-pending {
        background: #FEF3C7;
        color: #92400E;
    }
    
    .status-draft {
        background: #E0E7FF;
        color: #3730A3;
    }
    
    /* Activity Timeline */
    .activity-item {
        display: flex;
        align-items: flex-start;
        padding: 16px 0;
        border-bottom: 1px solid var(--border-light);
    }
    
    .activity-item:last-child {
        border-bottom: none;
    }
    
    .activity-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        flex-shrink: 0;
    }
    
    .activity-content {
        flex: 1;
    }
    
    .activity-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 2px;
    }
    
    .activity-time {
        font-size: 0.75rem;
        color: var(--text-light);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--text-light);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(
        page_title="SmartHire AI",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'generated_jd' not in st.session_state:
        st.session_state.generated_jd = ""
    if 'page_loaded' not in st.session_state:
        st.session_state.page_loaded = False
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    
    # Load CSS
    load_urban_design_css()
    
    # Apply dark mode
    if st.session_state.dark_mode:
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
    
    # Urban Style Sidebar
    with st.sidebar:
        # Header with gradient
        st.markdown("""
        <div style='padding: 2rem 1.5rem 1.5rem; border-bottom: 1px solid #334155; margin-bottom: 1.5rem;'>
            <div style='display: flex; align-items: center; gap: 12px; margin-bottom: 8px;'>
                <div style='width: 32px; height: 32px; background: linear-gradient(135deg, #0EA5E9, #8B5CF6); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;'>S</div>
                <div>
                    <h1 style='margin: 0; font-size: 1.25rem; font-weight: 700; color: white;'>SmartHire AI</h1>
                    <p style='margin: 0; font-size: 0.75rem; color: #94A3B8;'>Recruitment Platform</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
        <div style='padding: 0 0.5rem;'>
            <p style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748B; font-weight: 600; margin-bottom: 1rem;'>Navigation</p>
        </div>
        """, unsafe_allow_html=True)
        
        nav_items = {
            "Dashboard": {"icon": "📊", "desc": "Overview & Analytics"},
            "JD Generator": {"icon": "📝", "desc": "Create Job Descriptions"}, 
            "Resume Screening": {"icon": "📄", "desc": "AI-Powered Analysis"},
            "Analytics": {"icon": "📈", "desc": "Detailed Insights"},
            "Candidates": {"icon": "👥", "desc": "Manage Candidates"},
            "Settings": {"icon": "⚙️", "desc": "System Configuration"}
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
            <p style='font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #64748B; font-weight: 600; margin-bottom: 1rem;'>Quick Stats</p>
        </div>
        """, unsafe_allow_html=True)
        
        stats = [
            {"label": "Active Jobs", "value": "25", "change": "+3"},
            {"label": "Candidates", "value": "142", "change": "+12"},
            {"label": "Match Rate", "value": "82%", "change": "+5%"},
            {"label": "Hiring Time", "value": "18d", "change": "-2d"}
        ]
        
        for stat in stats:
            st.markdown(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; background: rgba(255,255,255,0.05); border-radius: 8px; margin: 8px 0;'>
                <div>
                    <div style='font-size: 0.875rem; color: #94A3B8;'>{stat['label']}</div>
                    <div style='font-size: 1.25rem; font-weight: 700; color: white;'>{stat['value']}</div>
                </div>
                <div style='font-size: 0.75rem; font-weight: 600; color: #10B981;'>{stat['change']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Theme Toggle at bottom
        st.markdown("---")
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("""
            <div style='color: #94A3B8; font-size: 0.875rem;'>Theme</div>
            <div style='color: white; font-weight: 500;'>{}</div>
            """.format("Dark" if st.session_state.dark_mode else "Light"), unsafe_allow_html=True)
        with col2:
            if st.button("🌙" if not st.session_state.dark_mode else "☀️", key="theme_toggle"):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
    
    # Main Content Area
    st.markdown(f"<h1 class='urban-header'>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='urban-subheader'>SmartHire AI Recruitment Platform • {datetime.now().strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
    
    # Show loading
    if not st.session_state.page_loaded:
        with st.spinner("Loading SmartHire AI..."):
            time.sleep(1.5)
        st.session_state.page_loaded = True
        st.rerun()
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        show_urban_dashboard()
    elif st.session_state.current_page == "JD Generator":
        show_urban_jd_generator()
    elif st.session_state.current_page == "Resume Screening":
        show_urban_resume_screening()
    elif st.session_state.current_page == "Analytics":
        show_urban_analytics()
    elif st.session_state.current_page == "Candidates":
        show_urban_candidates()
    elif st.session_state.current_page == "Settings":
        show_urban_settings()

def show_urban_dashboard():
    # Connection Status
    test_result = db.execute_query("SELECT 1 as test")
    if test_result:
        st.success("✅ System connected successfully")
    
    # Main KPI Section
    st.markdown("### Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="urban-metric">
            <div style="font-size: 1.5rem; margin-bottom: 12px;">💼</div>
            <div class="metric-value">25</div>
            <div class="metric-label">Active Jobs</div>
            <div class="metric-change change-positive">+3 this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="urban-metric">
            <div style="font-size: 1.5rem; margin-bottom: 12px;">👥</div>
            <div class="metric-value">142</div>
            <div class="metric-label">Candidates</div>
            <div class="metric-change change-positive">+12 today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="urban-metric">
            <div style="font-size: 1.5rem; margin-bottom: 12px;">⚡</div>
            <div class="metric-value">18d</div>
            <div class="metric-label">Avg Hiring Time</div>
            <div class="metric-change change-positive">-2d vs last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="urban-metric">
            <div style="font-size: 1.5rem; margin-bottom: 12px;">🎯</div>
            <div class="metric-value">94%</div>
            <div class="metric-label">Success Rate</div>
            <div class="metric-change change-positive">+5% improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Content Grid
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recent Activity Timeline
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Recent Activity</h3>
            <div style="display: flex; flex-direction: column;">
        """, unsafe_allow_html=True)
        
        activities = [
            {"icon": "🚀", "bg": "#0EA5E9", "title": "Senior AI Engineer JD Created", "time": "2 hours ago", "status": "active"},
            {"icon": "✅", "bg": "#10B981", "title": "Raj Kumar - Screened (85% match)", "time": "4 hours ago", "status": "active"},
            {"icon": "📊", "bg": "#8B5CF6", "title": "Q3 Recruitment Report Generated", "time": "1 day ago", "status": "active"},
            {"icon": "🎯", "bg": "#F59E0B", "title": "Technical Interview Scheduled", "time": "Tomorrow", "status": "pending"}
        ]
        
        for activity in activities:
            st.markdown(f"""
            <div class="activity-item">
                <div class="activity-icon" style="background: {activity['bg']}20; color: {activity['bg']};">
                    {activity['icon']}
                </div>
                <div class="activity-content">
                    <div class="activity-title">{activity['title']}</div>
                    <div class="activity-time">{activity['time']}</div>
                </div>
                <div class="status-badge status-{activity['status']}">
                    {activity['status'].title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Quick Actions</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
        """, unsafe_allow_html=True)
        
        if st.button("📝 Create New JD", use_container_width=True):
            st.session_state.current_page = "JD Generator"
            st.rerun()
        
        if st.button("📄 Screen Resume", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
        
        if st.button("👥 View Candidates", use_container_width=True):
            st.session_state.current_page = "Candidates"
            st.rerun()
        
        if st.button("📈 View Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # System Status
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">System Status</h3>
            <div style="display: grid; gap: 16px;">
        """, unsafe_allow_html=True)
        
        status_items = [
            {"label": "Database", "status": "Connected", "color": "#10B981", "icon": "🔗"},
            {"label": "AI Engine", "status": "Active", "color": "#10B981", "icon": "🤖"},
            {"label": "API Services", "status": "Optimal", "color": "#F59E0B", "icon": "⚡"},
            {"label": "Storage", "status": "78% Free", "color": "#0EA5E9", "icon": "💾"}
        ]
        
        for item in status_items:
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 12px; background: var(--bg-secondary); border-radius: 8px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 1.25rem;">{item['icon']}</div>
                    <div>
                        <div style="font-weight: 500; color: var(--text-primary);">{item['label']}</div>
                    </div>
                </div>
                <div style="color: {item['color']}; font-weight: 600; font-size: 0.875rem;">{item['status']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Today's Performance
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Today's Performance</h3>
            <div style="display: grid; gap: 12px;">
        """, unsafe_allow_html=True)
        
        performance_items = [
            {"label": "JDs Created", "value": "3", "trend": "up"},
            {"label": "Candidates Added", "value": "12", "trend": "up"},
            {"label": "Matches Found", "value": "8", "trend": "up"},
            {"label": "Response Time", "value": "2.1h", "trend": "down"}
        ]
        
        for item in performance_items:
            trend_icon = "📈" if item['trend'] == "up" else "📉"
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0;">
                <span style="color: var(--text-secondary);">{item['label']}</span>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 600; color: var(--text-primary);">{item['value']}</span>
                    <span style="font-size: 0.875rem;">{trend_icon}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)

def show_urban_jd_generator():
    st.markdown("### Job Description Generator")
    
    # Progress Steps
    steps = ["Job Details", "Generate", "Review & Save"]
    current_step = 0 if not st.session_state.generated_jd else 2
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; margin-bottom: 2rem; background: var(--bg-secondary); padding: 8px; border-radius: 12px;">
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(steps):
        is_active = i <= current_step
        st.markdown(f"""
        <div style="flex: 1; text-align: center; padding: 8px; border-radius: 8px; 
                    background: {'var(--primary)' if is_active else 'transparent'}; 
                    color: {'white' if is_active else 'var(--text-secondary)'};
                    font-weight: 500; font-size: 0.875rem;">
            {step}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Job Details</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Form
        companies = db.execute_query("SELECT id, name FROM companies")
        company_options = {company['name']: company['id'] for company in companies} if companies else {"TechCorp Inc.": 1}
        
        selected_company = st.selectbox("🏢 Company", list(company_options.keys()))
        job_title = st.text_input("🎯 Job Title", placeholder="e.g., Senior AI Engineer")
        department = st.selectbox("📊 Department", ["Engineering", "Data Science", "Product", "Design", "Marketing", "Sales"])
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            min_exp = st.slider("Minimum Experience", 0, 15, 3)
        with col_exp2:
            max_exp = st.slider("Maximum Experience", 0, 20, 7)
        
        skills = st.text_area("🛠️ Required Skills", 
                            placeholder="Python, Machine Learning, SQL, AWS, Docker...",
                            height=120)
        
        if st.button("🚀 Generate Job Description", type="primary", use_container_width=True):
            if job_title and skills:
                with st.spinner("🤖 Generating optimized job description..."):
                    time.sleep(2)
                    generate_urban_jd(job_title, department, min_exp, max_exp, skills)
            else:
                st.error("Please fill in all required fields")
    
    with col2:
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Generated Description</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.generated_jd:
            st.success("✅ Job description generated successfully!")
            
            edited_jd = st.text_area("✏️ Edit the generated description", 
                                   st.session_state.generated_jd, 
                                   height=400,
                                   key="jd_editor")
            
            st.session_state.generated_jd = edited_jd
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("💾 Save to Database", use_container_width=True):
                    st.success("Saved successfully!")
            with col_s2:
                if st.button("📥 Export as PDF", use_container_width=True):
                    st.success("PDF export ready!")
            with col_s3:
                if st.button("🔄 Create New", use_container_width=True):
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("""
            **👆 Get Started**
            
            Fill out the job details on the left and click **'Generate Job Description'** 
            to create a professional, AI-optimized job description.
            
            *The system will analyze your requirements and generate a comprehensive JD.*
            """)

def generate_urban_jd(title, department, min_exp, max_exp, skills):
    enhanced_jd = f"""🎯 **Position:** {title}
🏢 **Department:** {department}
⏳ **Experience:** {min_exp}-{max_exp} years
📍 **Location:** Remote / Hybrid Options Available

✨ **Job Summary**
We are seeking an exceptional {title} to join our innovative {department} team. 
This role offers the opportunity to work on cutting-edge projects and make a 
significant impact on our technology stack.

🚀 **Key Responsibilities**
• Design, develop, and maintain scalable software solutions
• Collaborate with cross-functional teams to define and ship new features
• Implement best practices in code quality, testing, and deployment
• Mentor junior developers and conduct code reviews
• Stay updated with emerging technologies and industry trends

🛠 **Technical Requirements**
{skills}

🎓 **Qualifications & Experience**
• {min_exp}+ years of professional experience in software development
• Bachelor's or Master's degree in Computer Science or related field
• Strong problem-solving skills and analytical thinking
• Experience with agile development methodologies
• Excellent communication and teamwork abilities

💫 **What We Offer**
• Competitive salary and comprehensive benefits package
• Flexible work arrangements and remote work options
• Professional development and growth opportunities
• Inclusive and collaborative work environment
• Cutting-edge technology stack and challenging projects

---
*Generated by SmartHire AI • {datetime.now().strftime('%B %d, %Y %H:%M')}*"""
    
    st.session_state.generated_jd = enhanced_jd
    st.rerun()

# Other functions (Resume Screening, Analytics, Candidates, Settings) follow similar urban design pattern...

def show_urban_resume_screening():
    st.markdown("### Resume Screening")
    
    tab1, tab2 = st.tabs(["📤 Upload & Analyze", "👥 Candidate Database"])
    
    with tab1:
        st.markdown("""
        <div class="urban-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Upload Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'], 
                                       help="Supported formats: PDF, DOCX, TXT")
        
        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="urban-card">
                    <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">File Details</h4>
                    <div style="display: grid; gap: 8px;">
                        <div style="display: flex; justify-content: between;">
                            <span>Name:</span>
                            <span style="font-weight: 500;">{uploaded_file.name}</span>
                        </div>
                        <div style="display: flex; justify-content: between;">
                            <span>Size:</span>
                            <span style="font-weight: 500;">{uploaded_file.size / 1024:.1f} KB</span>
                        </div>
                        <div style="display: flex; justify-content: between;">
                            <span>Type:</span>
                            <span style="font-weight: 500;">{uploaded_file.type}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="urban-card">
                    <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">Candidate Information</h4>
                </div>
                """, unsafe_allow_html=True)
                
                candidate_name = st.text_input("Full Name")
                candidate_email = st.text_input("Email Address")
                candidate_phone = st.text_input("Phone Number")
                candidate_exp = st.slider("Years of Experience", 0, 30, 3)
            
            if st.button("🔍 Analyze with AI", type="primary", use_container_width=True):
                if candidate_name and candidate_email:
                    with st.spinner("🤖 Analyzing resume content and extracting insights..."):
                        time.sleep(3)
                        show_urban_analysis_results(candidate_name, candidate_exp)
                else:
                    st.error("Please fill in candidate name and email")

def show_urban_analysis_results(name, experience):
    st.markdown("---")
    st.markdown("### 📊 Analysis Results")
    
    # Score with progress circle
    col_score, col_details = st.columns([1, 2])
    
    with col_score:
        st.markdown("""
        <div class="urban-card" style="text-align: center;">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary);">Overall Match</h3>
            <div style="font-size: 3rem; font-weight: 800; color: var(--primary); margin: 1rem 0;">82%</div>
            <div style="color: var(--text-secondary); font-size: 0.875rem;">Strong Match</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_details:
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary);">Detailed Breakdown</h4>
            <div style="display: grid; gap: 12px;">
        """, unsafe_allow_html=True)
        
        metrics = [
            {"label": "Skill Fit", "value": 78, "color": "#0EA5E9"},
            {"label": "Experience Match", "value": 85, "color": "#10B981"},
            {"label": "Culture Fit", "value": 76, "color": "#8B5CF6"},
            {"label": "Education", "value": 82, "color": "#F59E0B"}
        ]
        
        for metric in metrics:
            st.markdown(f"""
            <div style="margin-bottom: 12px;">
                <div style="display: flex; justify-content: between; margin-bottom: 4px;">
                    <span style="font-weight: 500; color: var(--text-primary);">{metric['label']}</span>
                    <span style="font-weight: 600; color: {metric['color']};">{metric['value']}%</span>
                </div>
                <div style="width: 100%; height: 6px; background: var(--bg-secondary); border-radius: 3px; overflow: hidden;">
                    <div style="width: {metric['value']}%; height: 100%; background: {metric['color']}; border-radius: 3px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Recommendations
    st.markdown("""
    <div class="urban-card">
        <h4 style="margin-bottom: 1rem; color: var(--text-primary);">💡 Recommendations</h4>
        <div style="display: grid; gap: 12px;">
            <div style="display: flex; align-items: start; gap: 12px; padding: 12px; background: var(--bg-secondary); border-radius: 8px;">
                <span style="color: #10B981;">✅</span>
                <div>
                    <div style="font-weight: 500; color: var(--text-primary);">Strong Technical Foundation</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">Candidate shows excellent proficiency in required technologies</div>
                </div>
            </div>
            <div style="display: flex; align-items: start; gap: 12px; padding: 12px; background: var(--bg-secondary); border-radius: 8px;">
                <span style="color: #F59E0B;">⚠️</span>
                <div>
                    <div style="font-weight: 500; color: var(--text-primary);">Consider Additional Certification</div>
                    <div style="color: var(--text-secondary); font-size: 0.875rem;">Cloud certification would enhance candidate profile</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_urban_analytics():
    st.markdown("### Analytics Dashboard")
    
    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="urban-metric">
            <div class="metric-value">25</div>
            <div class="metric-label">Total Jobs</div>
            <div class="metric-change change-positive">+12% growth</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="urban-metric">
            <div class="metric-value">142</div>
            <div class="metric-label">Candidates</div>
            <div class="metric-change change-positive">+8 this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="urban-metric">
            <div class="metric-value">68%</div>
            <div class="metric-label">Interview Rate</div>
            <div class="metric-change change-positive">+5% vs target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="urban-metric">
            <div class="metric-value">18d</div>
            <div class="metric-label">Hiring Time</div>
            <div class="metric-change change-positive">-3d improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">Hiring Trends</h4>
            <div style="height: 300px; display: flex; align-items: center; justify-content: center; 
                     background: var(--bg-secondary); border-radius: 12px; color: var(--text-secondary);">
                [ Hiring Trends Chart ]
            </div>
            <div style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.875rem;">
                45% increase in tech hiring Q3 2024
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">Skill Demand Analysis</h4>
            <div style="height: 300px; display: flex; align-items: center; justify-content: center; 
                     background: var(--bg-secondary); border-radius: 12px; color: var(--text-secondary);">
                [ Skills Demand Chart ]
            </div>
            <div style="margin-top: 1rem; color: var(--text-secondary); font-size: 0.875rem;">
                Python and ML skills show highest demand
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_urban_candidates():
    st.markdown("### Candidate Management")
    
    # Search and Filters
    col_search, col_filter, col_actions = st.columns([2, 1, 1])
    
    with col_search:
        st.text_input("🔍 Search candidates", placeholder="Name, skills, or keywords...")
    
    with col_filter:
        st.selectbox("Filter by", ["All", "Screened", "Interview", "Hired"])
    
    with col_actions:
        st.button("➕ Add Candidate", use_container_width=True)
    
    # Candidates Table
    st.markdown("""
    <div class="urban-card">
        <h4 style="margin-bottom: 1rem; color: var(--text-primary); font-weight: 600;">Candidate List</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample candidate data
    candidates_data = {
        'Name': ['Raj Kumar', 'Priya Sharma', 'Amit Patel', 'Sneha Reddy'],
        'Role': ['AI Engineer', 'Data Scientist', 'Frontend Developer', 'DevOps Engineer'],
        'Experience': ['5 years', '3 years', '4 years', '6 years'],
        'Match Score': ['85%', '78%', '92%', '67%'],
        'Status': ['Interview', 'Screened', 'Hired', 'Screened']
    }
    
    df = pd.DataFrame(candidates_data)
    st.dataframe(df, use_container_width=True)

def show_urban_settings():
    st.markdown("### System Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Theme & Appearance</h4>
            <div style="display: grid; gap: 16px;">
                <div>
                    <div style="font-weight: 500; color: var(--text-primary); margin-bottom: 8px;">Current Theme</div>
                    <div style="color: var(--text-secondary);">{}</div>
                </div>
                <div>
                    <div style="font-weight: 500; color: var(--text-primary); margin-bottom: 8px;">Accent Color</div>
                    <div style="color: var(--text-secondary);">Sky Blue Gradient</div>
                </div>
            </div>
        </div>
        """.format("Dark Mode" if st.session_state.dark_mode else "Light Mode"), unsafe_allow_html=True)
        
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Notifications</h4>
            <div style="display: grid; gap: 12px;">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span style="color: var(--text-primary);">Email Notifications</span>
                    <span style="color: var(--success); font-weight: 600;">Enabled</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span style="color: var(--text-primary);">Push Alerts</span>
                    <span style="color: var(--success); font-weight: 600;">Enabled</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span style="color: var(--text-primary);">Weekly Reports</span>
                    <span style="color: var(--text-secondary); font-weight: 600;">Disabled</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">System Configuration</h4>
            <div style="display: grid; gap: 12px;">
                <div style="display: flex; justify-content: between;">
                    <span style="color: var(--text-primary);">AI Model Version</span>
                    <span style="font-weight: 600; color: var(--primary);">v2.1.0</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span style="color: var(--text-primary);">Data Retention</span>
                    <span style="font-weight: 600; color: var(--primary);">24 Months</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span style="color: var(--text-primary);">Auto Backup</span>
                    <span style="font-weight: 600; color: var(--primary);">Daily</span>
                </div>
                <div style="display: flex; justify-content: between;">
                    <span style="color: var(--text-primary);">API Version</span>
                    <span style="font-weight: 600; color: var(--primary);">v1.4.2</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="urban-card">
            <h4 style="margin-bottom: 1.5rem; color: var(--text-primary); font-weight: 600;">Security & Privacy</h4>
            <div style="display: grid; gap: 12px;">
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span style="color: var(--text-primary);">Data Encryption</span>
                    <span style="color: var(--success); font-weight: 600;">AES-256</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span style="color: var(--text-primary);">GDPR Compliance</span>
                    <span style="color: var(--success); font-weight: 600;">Enabled</span>
                </div>
                <div style="display: flex; justify-content: between; align-items: center;">
                    <span style="color: var(--text-primary);">Last Security Audit</span>
                    <span style="font-weight: 600; color: var(--primary);">2024-01-15</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()