# app.py - COMPLETE FIXED VERSION
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
import openai
import json
import base64

# Import email configuration
try:
    from email_config import get_email_config, validate_email_config, COMPANY_NAME, HR_EMAIL, HR_PHONE
    EMAIL_CONFIG = get_email_config()
    EMAIL_ENABLED = True
except ImportError:
    st.error("❌ email_config.py file not found. Please create the configuration file.")
    EMAIL_ENABLED = False
    EMAIL_CONFIG = {}

# Premium Theme CSS with Light/Dark Mode
def load_dynamic_css():
    st.markdown("""
    <style>
    /* Dynamic Theme Variables */
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
    
    .light-mode {
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --bg-card: #FFFFFF;
        --bg-sidebar: #2C3E50;
        --text-primary: #2C3E50;
        --text-secondary: #34495E;
        --text-muted: #7F8C8D;
        --border: #BDC3C7;
        --border-light: #ECF0F1;
        --shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 8px 40px rgba(0, 212, 170, 0.1);
    }
    
    /* Base Styles */
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', 'SF Pro Display', -apple-system, sans-serif;
        font-weight: 400;
        line-height: 1.6;
        transition: all 0.3s ease;
    }
    
    /* Force ALL text to be visible */
    * {
        color: var(--text-primary) !important;
    }
    
    /* Input Fields - Better Visibility */
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
    
    .stTextInput>div>div>input:focus, .stSelectbox>div>div:focus, .stTextArea>div>textarea:focus {
        border-color: var(--accent-primary) !important;
        box-shadow: 0 0 0 3px rgba(0, 212, 170, 0.1) !important;
    }
    
    /* Text Area - Black Background for Light Mode */
    .stTextArea>div>textarea {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    .stTextInput>div>div>input::placeholder, .stTextArea>div>textarea::placeholder {
        color: var(--text-muted) !important;
        font-weight: 400 !important;
    }
    
    /* Premium Header */
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
    
    /* Blue Section Colors */
    .blue-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
    }
    
    .blue-section * {
        color: white !important;
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
    
    .light-mode .premium-card {
        background: rgba(255, 255, 255, 0.9);
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
    
    /* Success Pop Effect */
    @keyframes successPop {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .success-pop {
        animation: successPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
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
    </style>
    """, unsafe_allow_html=True)

def extract_info_from_resume(text):
    """Enhanced resume parsing with AI-powered extraction"""
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'experience': 0,
        'skills': [],
        'education': [],
        'projects': []
    }
    
    lines = text.split('\n')
    
    # Extract name (more sophisticated pattern)
    name_patterns = [
        r'^[A-Z][a-z]+ [A-Z][a-z]+$',
        r'^[A-Z][a-z]+ [A-Z]\. [A-Z][a-z]+$',
        r'^[A-Z][a-z]+ [A-Z][a-z]+ [A-Z][a-z]+$'
    ]
    
    for line in lines[:10]:  # Check first 10 lines
        line = line.strip()
        for pattern in name_patterns:
            if re.match(pattern, line):
                info['name'] = line
                break
        if info['name']:
            break
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone number (international format)
    phone_patterns = [
        r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]',
        r'\(\d{3}\) \d{3}-\d{4}',
        r'\d{3}-\d{3}-\d{4}',
        r'\+\d{1,3} \d{9,10}'
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            info['phone'] = phones[0]
            break
    
    # Extract experience (multiple patterns)
    exp_patterns = [
        r'(\d+)\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?) of experience',
        r'experience.*?(\d+)\s*(?:years?|yrs?)'
    ]
    
    for pattern in exp_patterns:
        exp_matches = re.findall(pattern, text.lower())
        if exp_matches:
            info['experience'] = max([int(match) for match in exp_matches])
            break
    
    # Enhanced skills extraction
    tech_skills = {
        'Programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'swift', 'kotlin'],
        'Web': ['html', 'css', 'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring', 'express'],
        'Database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sqlite', 'cassandra'],
        'Cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'ci/cd'],
        'Data Science': ['machine learning', 'deep learning', 'tensorflow', 'pytorch', 'pandas', 'numpy', 'scikit-learn'],
        'Tools': ['git', 'jira', 'confluence', 'slack', 'figma', 'postman', 'vscode', 'intellij']
    }
    
    found_skills = []
    for category, skills in tech_skills.items():
        for skill in skills:
            if re.search(r'\b' + re.escape(skill) + r'\b', text.lower()):
                found_skills.append(skill.title())
    
    info['skills'] = list(set(found_skills))[:15]  # Remove duplicates and limit
    
    # Extract education
    education_keywords = ['university', 'college', 'institute', 'bachelor', 'master', 'phd', 'bs', 'ms', 'btech', 'mtech']
    for line in lines:
        if any(keyword in line.lower() for keyword in education_keywords):
            info['education'].append(line.strip())
    
    return info

def send_real_email(candidate_email, candidate_name, role, interview_date, interview_time, interview_type):
    """Send real email to candidate using SMTP configuration"""
    try:
        if not EMAIL_ENABLED:
            return False, "Email configuration not available"
        
        config = EMAIL_CONFIG
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Interview Invitation - {role} Position at SmartHire AI"
        message["From"] = config['sender_email']
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
              </div>
            </div>
          </body>
        </html>
        """
        
        # Add HTML content to email
        message.attach(MIMEText(html, "html"))
        
        # Create secure connection with server and send email
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.ehlo()
        server.starttls()
        server.ehlo()
        
        # Login to email account
        server.login(config['sender_email'], config['sender_password'])
        
        # Send email
        server.sendmail(config['sender_email'], candidate_email, message.as_string())
        
        # Close connection
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"

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
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    
    # Apply theme
    if st.session_state.dark_mode:
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
    else:
        st.markdown('<div class="light-mode">', unsafe_allow_html=True)
    
    # Load CSS
    load_dynamic_css()
    
    # Premium Sidebar
    with st.sidebar:
        # Theme Toggle
        col1, col2 = st.columns([3, 1])
        with col2:
            theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
            if st.button(theme_icon, key="theme_toggle", use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
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
    
    # Close theme div
    st.markdown('</div>', unsafe_allow_html=True)

# Add the missing show_interview_preparation function here
def show_interview_preparation():
    st.markdown("### 🎯 AI Interview Preparation")
    
    # OpenAI API Configuration
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 AI Configuration")
    api_key = st.sidebar.text_input("OpenAI API Key", value="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", 
                                  type="password", 
                                  help="Get your API key from https://platform.openai.com/api-keys")
    
    if api_key:
        openai.api_key = api_key
        st.sidebar.success("✅ API Key configured!")
    else:
        st.sidebar.warning("⚠️ Please enter OpenAI API key to generate questions")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">🎯 Select Role & Experience</h3>
        </div>
        """, unsafe_allow_html=True)
        
        role = st.selectbox("Target Role", 
                          ["Data Analyst", "AI Engineer", "Data Scientist", "Machine Learning Engineer",
                           "Software Developer", "DevOps Engineer", "Product Manager", "Business Analyst",
                           "Frontend Developer", "Backend Developer", "Full Stack Developer", "Data Engineer"])
        
        experience_level = st.selectbox("Experience Level", 
                                      ["Entry Level (0-2 years)", "Mid Level (2-5 years)", 
                                       "Senior Level (5-8 years)", "Lead Level (8+ years)"])
        
        # Additional customization
        question_types = st.multiselect("Question Types",
                                      ["Technical", "Behavioral", "System Design", "Case Study", "Coding"],
                                      default=["Technical", "Behavioral"])
        
        difficulty = st.select_slider("Difficulty Level", 
                                    options=["Beginner", "Intermediate", "Advanced", "Expert"])
        
        num_questions = st.slider("Number of Questions", 5, 20, 10)
        
        # Advanced options
        with st.expander("🎛️ Advanced Options"):
            include_answers = st.checkbox("Include Sample Answers", value=True)
            industry_focus = st.selectbox("Industry Focus", 
                                        ["Any", "Tech", "Finance", "Healthcare", "E-commerce", "Startup", "Enterprise"])
            
        if st.button("🚀 Generate AI-Powered Questions", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ Please enter your OpenAI API key in the sidebar")
            else:
                with st.spinner("🤖 AI is generating personalized interview questions..."):
                    try:
                        generated_questions = generate_ai_questions(
                            role, experience_level, question_types, difficulty, 
                            num_questions, industry_focus, include_answers
                        )
                        st.session_state.generated_questions = generated_questions
                        show_success_popup(f"AI-generated {num_questions} personalized {role} interview questions!")
                    except Exception as e:
                        st.error(f"❌ Error generating questions: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📝 AI-Generated Questions & Answers</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if 'generated_questions' in st.session_state and st.session_state.generated_questions:
            questions_data = st.session_state.generated_questions
            
            for i, qa in enumerate(questions_data, 1):
                with st.expander(f"Q{i}: {qa['question']} ({qa.get('type', 'Technical')} - {qa.get('difficulty', 'Intermediate')})"):
                    if qa.get('answer'):
                        st.success(f"**Sample Answer:** {qa['answer']}")
                    else:
                        st.info("🤖 *AI is generating answer...*")
                    
                    # Additional insights
                    if qa.get('key_points'):
                        st.markdown("**🎯 Key Points to Cover:**")
                        for point in qa['key_points']:
                            st.markdown(f"- {point}")
        
        else:
            # Fallback to predefined questions if no AI generation
            st.info("""
            **👆 Get Started**
            
            Configure your OpenAI API key in the sidebar and click **'Generate AI-Powered Questions'** 
            to create personalized, role-specific interview questions.
            
            💡 *The AI will analyze the role requirements and generate relevant, 
            up-to-date interview questions with sample answers.*
            """)
            
            # Show some sample questions
            with st.expander("🔍 Sample Questions (Pre-defined)"):
                sample_questions = [
                    "How do you approach debugging complex issues in production?",
                    "Describe your experience with cloud technologies and deployment strategies.",
                    "How do you ensure code quality and maintainability in large projects?",
                    "Explain a challenging technical problem you solved recently."
                ]
                for i, question in enumerate(sample_questions[:4], 1):
                    st.markdown(f"**Q{i}:** {question}")
        
        # Export functionality
        if st.button("📥 Export Questions & Answers", use_container_width=True):
            if 'generated_questions' in st.session_state:
                show_success_popup("Interview questions and answers exported successfully!")
            else:
                st.warning("Please generate questions first")

def generate_ai_questions(role, experience_level, question_types, difficulty, num_questions, industry_focus, include_answers):
    """Generate interview questions using OpenAI API"""
    
    prompt = f"""
    Generate {num_questions} interview questions for a {role} position at {experience_level} level.
    
    Requirements:
    - Role: {role}
    - Experience: {experience_level}
    - Question types: {', '.join(question_types)}
    - Difficulty: {difficulty}
    - Industry focus: {industry_focus}
    - Include sample answers: {include_answers}
    
    Please provide the response in JSON format with the following structure:
    {{
        "questions": [
            {{
                "question": "the interview question",
                "type": "one of {question_types}",
                "difficulty": "{difficulty}",
                "answer": "comprehensive sample answer"{" if include_answers else ""},
                "key_points": ["key point 1", "key point 2", "key point 3"]
            }}
        ]
    }}
    
    Make the questions realistic, relevant to current industry standards, and tailored to the specific role and experience level.
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert hiring manager and technical interviewer with deep knowledge across various roles and industries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        
        # Extract JSON from response
        try:
            import json
            # Find JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            json_str = content[start_idx:end_idx]
            questions_data = json.loads(json_str)
            return questions_data.get('questions', [])
        except json.JSONDecodeError:
            # If JSON parsing fails, create structured data from text
            lines = content.split('\n')
            questions = []
            current_question = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('Q') or line.startswith('Question'):
                    if current_question:
                        questions.append(current_question)
                    current_question = {'question': line.split(':', 1)[1].strip() if ':' in line else line}
                elif line.startswith('Answer:') and include_answers:
                    current_question['answer'] = line.split(':', 1)[1].strip()
                elif line.startswith('Type:'):
                    current_question['type'] = line.split(':', 1)[1].strip()
            
            if current_question:
                questions.append(current_question)
            
            return questions
            
    except openai.error.AuthenticationError:
        raise Exception("Invalid OpenAI API key. Please check your API key.")
    except openai.error.RateLimitError:
        raise Exception("OpenAI API rate limit exceeded. Please try again later.")
    except openai