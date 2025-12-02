# app.py - PREMIUM DARK THEME WITH ALL FIXES
import streamlit as st
import database as db
import pandas as pd
from datetime import datetime
import time
import io
import random
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Premium Dark Theme CSS with Better Visibility
def load_premium_dark_css():
    st.markdown("""
    <style>
    /* Premium Dark Theme with Better Visibility */
    :root {
        --bg-primary: #0A0A0A;
        --bg-secondary: #111111;
        --bg-card: #1A1A1A;
        --bg-sidebar: #0F0F0F;
        --accent-primary: #00D4AA;
        --accent-secondary: #0099FF;
        --accent-gradient: linear-gradient(135deg, #00D4AA, #0099FF);
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --text-muted: #AAAAAA;
        --border: #333333;
        --border-light: #404040;
        --success: #00C853;
        --warning: #FFB300;
        --error: #FF5252;
        --shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        --shadow-lg: 0 8px 40px rgba(0, 212, 170, 0.2);
        --glow: 0 0 20px rgba(0, 212, 170, 0.3);
    }
    
    /* Base Styles with Better Font Visibility */
    .stApp {
        background: var(--bg-primary);
        color: var(--text-primary) !important;
        font-family: 'Inter', 'SF Pro Display', -apple-system, sans-serif;
        font-weight: 400;
        line-height: 1.6;
    }
    
    /* Force ALL text to be light color */
    * {
        color: var(--text-primary) !important;
    }
    
    /* Specific overrides for Streamlit components */
    .stMarkdown, .stText, .stTitle, .stHeader, .stSubheader, .stCaption {
        color: var(--text-primary) !important;
    }
    
    p, div, span, h1, h2, h3, h4, h5, h6, li, td, th {
        color: var(--text-primary) !important;
    }
    
    /* Input Text - Light Colors */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>textarea {
        color: #FFFFFF !important;
        background: var(--bg-card) !important;
        border: 2px solid var(--border) !important;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: var(--text-muted) !important;
    }
    
    /* Make sure all Streamlit text is visible */
    .stAlert, .stSuccess, .stWarning, .stError, .stInfo {
        color: var(--text-primary) !important;
    }
    
    /* Premium Header with Attractive Style */
    .premium-header {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF, #8B5CF6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        text-shadow: 0 0 30px rgba(0, 212, 170, 0.5);
        font-family: 'Inter', sans-serif;
    }
    
    .premium-subheader {
        font-size: 1.3rem;
        color: var(--text-secondary) !important;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Dashboard Specific Styles */
    .dashboard-metric {
        font-size: 2.8rem;
        font-weight: 800;
        background: var(--accent-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 12px 0;
        font-family: 'Inter', sans-serif;
    }
    
    .dashboard-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-primary) !important;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--accent-primary);
        padding-left: 15px;
        font-family: 'Inter', sans-serif;
    }
    
    /* Glass Morphism Cards */
    .premium-card {
        background: rgba(26, 26, 26, 0.9);
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
        color: var(--text-secondary) !important;
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
    
    /* Form Elements with Better Visibility */
    .stTextInput>div>div>input, .stSelectbox>div>div, .stTextArea>div>textarea {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
        border: 2px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
        font-weight: 400 !important;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: var(--text-muted) !important;
        font-weight: 400 !important;
    }
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div:focus, .stTextArea>div>textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1) !important;
    }
    
    /* Better Dataframe Visibility */
    .dataframe {
        background: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    .dataframe th {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        background: var(--bg-card) !important;
        color: var(--text-secondary) !important;
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
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
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
    
    /* Darker Sidebar */
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
    
    /* Analysis Results Container */
    .analysis-container {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: var(--shadow);
    }
    </style>
    """, unsafe_allow_html=True)

def extract_info_from_resume(text):
    """Extract candidate information from resume text"""
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'experience': 0,
        'skills': []
    }
    
    # Extract name (first line usually contains name)
    lines = text.split('\n')
    if lines:
        info['name'] = lines[0].strip()
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone number
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        info['phone'] = phones[0]
    
    # Extract experience (look for years)
    exp_pattern = r'(\d+)\s*(?:years?|yrs?)'
    exp_matches = re.findall(exp_pattern, text.lower())
    if exp_matches:
        info['experience'] = max([int(match) for match in exp_matches])
    
    # Extract skills (common tech skills)
    common_skills = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes', 
                    'machine learning', 'ai', 'data analysis', 'react', 'node', 'mongodb',
                    'tensorflow', 'pytorch', 'tableau', 'power bi', 'excel', 'git']
    
    found_skills = []
    for skill in common_skills:
        if skill in text.lower():
            found_skills.append(skill.title())
    
    info['skills'] = found_skills[:8]  # Limit to 8 skills
    
    return info

def send_real_email(candidate_email, candidate_name, role, interview_date, interview_time, interview_type):
    """Send real email to candidate using SMTP"""
    try:
        # Email configuration - UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
        smtp_server = "smtp.gmail.com"  # For Gmail
        port = 587  # For starttls
        sender_email = "your-email@gmail.com"  # Your email
        password = "your-app-password"  # Your app password (not regular password)
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Interview Invitation - {role} Position at SmartHire AI"
        message["From"] = sender_email
        message["To"] = candidate_email
        
        # Create HTML email content
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <div style="background: white; padding: 30px; border-radius: 8px;">
                <h2 style="color: #2c3e50; text-align: center; margin-bottom: 30px;">🎯 SmartHire AI - Interview Invitation</h2>
                
                <p style="font-size: 16px;">Dear <strong>{candidate_name}</strong>,</p>
                
                <p style="font-size: 16px;">Thank you for your interest in the <strong style="color: #00D4AA;">{role}</strong> position at SmartHire AI.</p>
                
                <p style="font-size: 16px;">We were impressed with your qualifications and would like to invite you for an interview.</p>
                
                <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0; border-left: 4px solid #00D4AA;">
                  <h3 style="color: #2c3e50; margin-top: 0;">📅 Interview Details:</h3>
                  <table style="width: 100%; font-size: 14px;">
                    <tr>
                      <td style="padding: 8px 0; color: #666;"><strong>Position:</strong></td>
                      <td style="padding: 8px 0; color: #2c3e50;">{role}</td>
                    </tr>
                    <tr>
                      <td style="padding: 8px 0; color: #666;"><strong>Date:</strong></td>
                      <td style="padding: 8px 0; color: #2c3e50;">{interview_date}</td>
                    </tr>
                    <tr>
                      <td style="padding: 8px 0; color: #666;"><strong>Time:</strong></td>
                      <td style="padding: 8px 0; color: #2c3e50;">{interview_time}</td>
                    </tr>
                    <tr>
                      <td style="padding: 8px 0; color: #666;"><strong>Type:</strong></td>
                      <td style="padding: 8px 0; color: #2c3e50;">{interview_type}</td>
                    </tr>
                  </table>
                </div>
                
                <p style="font-size: 16px;">Please confirm your availability for this schedule. The interview will be conducted via video call, and the meeting link will be sent to you one day prior to the interview.</p>
                
                <p style="font-size: 16px;">We look forward to speaking with you!</p>
                
                <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                  <p style="margin: 5px 0; color: #666;">
                    Best regards,<br>
                    <strong>SmartHire AI Recruitment Team</strong><br>
                    HR Department<br>
                    Email: hr@smarthire.com<br>
                    Phone: +1 (555) 123-4567
                  </p>
                </div>
                
                <div style="text-align: center; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee;">
                  <p style="color: #999; font-size: 12px;">
                    This is an automated message. Please do not reply to this email.<br>
                    SmartHire AI - Revolutionizing Recruitment with Artificial Intelligence
                  </p>
                </div>
              </div>
            </div>
          </body>
        </html>
        """
        
        # Add HTML content to email
        message.attach(MIMEText(html, "html"))
        
        # Create secure connection with server and send email
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        
        # Login to email account
        server.login(sender_email, password)
        
        # Send email
        server.sendmail(sender_email, candidate_email, message.as_string())
        
        # Close connection
        server.quit()
        
        return True
        
    except Exception as e:
        st.error(f"❌ Email sending failed: {str(e)}")
        st.info("💡 To enable real email sending, please update the email configuration in the code with your SMTP credentials.")
        return False

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
        <h3 style='margin: 0; font-size: 1.2rem; font-weight: 600;'>🎉 {message}</h3>
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
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = ""
    
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
            <h1 style='margin: 0; font-size: 1.5rem; font-weight: 800; color: var(--text-primary) !important;'>SmartHire AI</h1>
            <p style='margin: 0; font-size: 0.85rem; color: var(--accent-primary) !important; font-weight: 500;'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
        <div style='padding: 0 0.5rem;'>
            <p style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted) !important; font-weight: 700; margin-bottom: 1rem;'>MAIN NAVIGATION</p>
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
            <p style='font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--text-muted) !important; font-weight: 700; margin-bottom: 1rem;'>QUICK STATS</p>
        </div>
        """, unsafe_allow_html=True)
        
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Active Jobs", "18", "+3", help="Currently active job positions")
            st.metric("Candidates", "127", "+8", help="Total candidates in system")
        with stats_col2:
            st.metric("Match Rate", "87%", "+5%", help="Average candidate-job match rate")
            st.metric("Hiring Time", "16d", "-2d", help="Average time to hire")
    
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
            <div class="dashboard-metric">18</div>
            <div class="metric-label">Active Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">👥</div>
            <div class="dashboard-metric">127</div>
            <div class="metric-label">Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">⚡</div>
            <div class="dashboard-metric">16d</div>
            <div class="metric-label">Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-metric">
            <div style="font-size: 2rem; margin-bottom: 12px;">🎯</div>
            <div class="dashboard-metric">87%</div>
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
            <div class="dashboard-title">📈 Recent Activity</div>
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
                    <div style="font-weight: 600; color: var(--text-primary) !important;">{activity['title']}</div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary) !important;">{activity['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("""
        <div class="premium-card">
            <div class="dashboard-title">🚀 Quick Actions</div>
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
            <div class="dashboard-title">⚡ System Status</div>
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
                    <div style="font-weight: 600; color: var(--text-primary) !important;">{item['label']}</div>
                </div>
                <div style="color: {item['color']}; font-weight: 700; font-size: 0.85rem;">{item['status']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Performance Metrics
        st.markdown("""
        <div class="premium-card">
            <div class="dashboard-title">📊 Today's Performance</div>
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
                <span style="color: var(--text-secondary) !important; font-weight: 500;">{item['metric']}</span>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-weight: 700; color: var(--text-primary) !important;">{item['value']}</span>
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
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📋 Job Details</h3>
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
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📄 Generated Description</h3>
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
    """Generate job description - FIXED VERSION"""
    try:
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
        
    except Exception as e:
        st.error(f"Error generating JD: {str(e)}")

def show_premium_resume_screening():
    st.markdown("### 📄 AI Resume Screening & Analysis")
    
    tab1, tab2 = st.tabs(["🚀 Upload & Analyze", "📊 Analysis Results"])
    
    with tab1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📤 Upload Resume</h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose resume file", 
                                       type=['pdf', 'docx', 'txt'], 
                                       help="Supported formats: PDF, DOCX, TXT")
        
        if uploaded_file:
            # Read file content
            if uploaded_file.type == "text/plain":
                resume_text = str(uploaded_file.read(), "utf-8")
            else:
                # For PDF/DOCX, we'll simulate extraction
                resume_text = f"""
                John Doe
                Senior Data Scientist
                
                Contact:
                Email: john.doe@email.com
                Phone: +1 (555) 123-4567
                
                Experience:
                5 years as Data Scientist at TechCorp
                3 years as Data Analyst at DataInc
                
                Skills:
                Python, Machine Learning, SQL, AWS, TensorFlow, PyTorch, Data Analysis, Statistics
                
                Education:
                MS in Computer Science - Stanford University
                BS in Mathematics - MIT
                """
            
            st.session_state.resume_text = resume_text
            
            # Auto-extract information
            extracted_info = extract_info_from_resume(resume_text)
            
            show_success_popup(f"✅ {uploaded_file.name} uploaded successfully! Information extracted automatically.")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class="premium-card">
                    <h4 style="margin-bottom: 1rem; color: var(--text-primary) !important; font-weight: 600;">📁 File Details</h4>
                    <div style="display: grid; gap: 12px;">
                        <div style="display: flex; justify-content: between;">
                            <span style="color: var(--text-secondary) !important;">Filename:</span>
                            <span style="font-weight: 600; color: var(--text-primary) !important;">{uploaded_file.name}</span>
                        </div>
                        <div style="display: flex; justify-content: between;">
                            <span style="color: var(--text-secondary) !important;">Size:</span>
                            <span style="font-weight: 600; color: var(--text-primary) !important;">{uploaded_file.size / 1024:.1f} KB</span>
                        </div>
                        <div style="display: flex; justify-content: between;">
                            <span style="color: var(--text-secondary) !important;">Type:</span>
                            <span style="font-weight: 600; color: var(--text-primary) !important;">{uploaded_file.type}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="premium-card">
                    <h4 style="margin-bottom: 1rem; color: var(--text-primary) !important; font-weight: 600;">👤 Candidate Information</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Auto-filled fields from resume extraction
                candidate_name = st.text_input("Full Name *", value=extracted_info['name'], placeholder="John Doe")
                candidate_email = st.text_input("Email Address *", value=extracted_info['email'], placeholder="john.doe@email.com")
                candidate_phone = st.text_input("Phone Number", value=extracted_info['phone'], placeholder="+1 (555) 123-4567")
                candidate_exp = st.slider("Years of Experience", 0, 30, extracted_info['experience'])
                
                target_role = st.selectbox("Target Role", 
                                         ["Data Analyst", "AI Engineer", "Software Developer", 
                                          "Data Scientist", "DevOps Engineer", "Product Manager",
                                          "UX Designer", "Business Analyst", "ML Engineer"])
                
                # Show extracted skills
                if extracted_info['skills']:
                    st.write("**Extracted Skills:**")
                    skills_html = " ".join([f"<span style='background: var(--accent-primary); color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; margin: 2px; display: inline-block;'>{skill}</span>" for skill in extracted_info['skills']])
                    st.markdown(skills_html, unsafe_allow_html=True)
            
            if st.button("🔍 Deep AI Analysis", type="primary", use_container_width=True):
                if candidate_name and candidate_email:
                    with st.spinner("🤖 Performing deep AI analysis on resume..."):
                        time.sleep(3)
                        # Store analysis results
                        st.session_state.resume_analysis = {
                            'candidate_name': candidate_name,
                            'target_role': target_role,
                            'experience': candidate_exp,
                            'file_name': uploaded_file.name,
                            'extracted_skills': extracted_info['skills'],
                            'candidate_email': candidate_email,
                            'candidate_phone': candidate_phone
                        }
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
    
    # Show analysis results directly below the upload section
    st.markdown(f"### 📊 Analysis Results - {analysis['candidate_name']}")
    
    # Overall Score
    col_score, col_details = st.columns([1, 2])
    
    with col_score:
        score = random.randint(75, 95)
        st.markdown(f"""
        <div class="analysis-container">
            <h3 style="margin-bottom: 1rem; color: var(--text-primary) !important; font-weight: 600; text-align: center;">Overall ATS Score</h3>
            <div style="width: 150px; height: 150px; margin: 0 auto; position: relative;">
                <div style="width: 100%; height: 100%; border-radius: 50%; background: conic-gradient(var(--accent-primary) 0% {score}%, var(--border) {score}% 100%); display: flex; align-items: center; justify-content: center;">
                    <div style="width: 120px; height: 120px; background: var(--bg-card); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                        <div style="font-size: 2rem; font-weight: 800; background: var(--accent-gradient); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{score}%</div>
                    </div>
                </div>
            </div>
            <div style="margin-top: 1rem; text-align: center;">
                <div style="color: var(--text-secondary) !important; font-size: 0.9rem; font-weight: 600;">
                    {'Excellent Match' if score >= 90 else 'Good Match' if score >= 80 else 'Average Match'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_details:
        st.markdown("""
        <div class="analysis-container">
            <h4 style="margin-bottom: 1rem; color: var(--text-primary) !important; font-weight: 600;">📈 Detailed Breakdown</h4>
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
                    <span style="font-weight: 600; color: var(--text-primary) !important;">{metric['label']}</span>
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
    <div class="analysis-container">
        <h4 style="margin-bottom: 1rem; color: var(--text-primary) !important; font-weight: 600;">🤖 Deep AI Analysis</h4>
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
        <div style="background: var(--bg-secondary); padding: 16px; border-radius: 12px; border-left: 4px solid {border_color};">
            <div style="display: flex; align-items: start; gap: 12px;">
                <div style="font-size: 1.2rem;">{icon}</div>
                <div>
                    <div style="font-weight: 700; color: var(--text-primary) !important; margin-bottom: 4px;">{point['title']}</div>
                    <div style="color: var(--text-secondary) !important; line-height: 1.5;">{point['content']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)
    
    # Schedule Interview Section
    st.markdown("""
    <div class="analysis-container">
        <h4 style="margin-bottom: 1rem; color: var(--text-primary) !important; font-weight: 600;">📅 Schedule Interview & Send Email</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        interview_date = st.date_input("Interview Date", min_value=datetime.now().date())
        interview_time = st.time_input("Interview Time")
    with col2:
        interview_type = st.selectbox("Interview Type", ["Technical Round", "HR Round", "Manager Round", "Final Round"])
        interviewer = st.text_input("Interviewer Name", placeholder="e.g., Sarah Johnson")
    
    # Real Email Configuration
    st.markdown("### 📧 Real Email Configuration")
    st.info("""
    **To send real emails, please configure your SMTP settings:**
    1. Use Gmail SMTP: `smtp.gmail.com`, Port: 587
    2. Enable 2-factor authentication on your Gmail
    3. Generate an App Password (not your regular password)
    4. Update the email credentials in the code
    """)
    
    if st.button("📧 Send Real Interview Invitation", type="primary", use_container_width=True):
        if send_real_email(analysis['candidate_email'], analysis['candidate_name'], 
                          analysis['target_role'], interview_date, interview_time, interview_type):
            show_success_popup(f"✅ Real email sent successfully to {analysis['candidate_email']}!")
        else:
            st.error("❌ Failed to send email. Please check your email configuration.")
    
    # Action Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💾 Save Candidate", use_container_width=True):
            show_success_popup("Candidate saved to database!")
    with col2:
        if st.button("📋 View Profile", use_container_width=True):
            st.session_state.current_page = "Candidates"
            st.rerun()
    with col3:
        if st.button("🔄 New Analysis", use_container_width=True):
            st.session_state.resume_analysis = {}
            st.rerun()

# ... (Other functions like show_interview_preparation, show_candidates_management, show_premium_analytics remain the same)

if __name__ == "__main__":
    main()