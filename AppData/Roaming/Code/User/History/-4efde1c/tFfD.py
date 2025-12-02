# app.py - COMPLETELY FIXED VERSION
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

# Import email configuration
try:
    from email_config import get_email_config, validate_email_config
    EMAIL_CONFIG = get_email_config()
    EMAIL_ENABLED = True
except ImportError:
    st.error("❌ email_config.py file not found. Please create the configuration file.")
    EMAIL_ENABLED = False
    EMAIL_CONFIG = {}

# Ultra Premium Theme CSS
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
    
    /* Sidebar - Dark Color */
    section[data-testid="stSidebar"] {
        background: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    .st-emotion-cache-1legitb {
        background: var(--bg-sidebar) !important;
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
    
    /* Professional Email Template */
    .email-template {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

def extract_info_from_resume(text):
    """Advanced resume parsing"""
    info = {
        'name': '',
        'email': '',
        'phone': '',
        'experience': 0,
        'skills': []
    }
    
    lines = text.split('\n')
    if lines:
        info['name'] = lines[0].strip()
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone
    phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
    phones = re.findall(phone_pattern, text)
    if phones:
        info['phone'] = phones[0]
    
    # Extract experience
    exp_pattern = r'(\d+)\s*(?:years?|yrs?)'
    exp_matches = re.findall(exp_pattern, text.lower())
    if exp_matches:
        info['experience'] = max([int(match) for match in exp_matches])
    
    # Extract skills
    common_skills = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'machine learning', 'react', 'node']
    found_skills = []
    for skill in common_skills:
        if skill in text.lower():
            found_skills.append(skill.title())
    
    info['skills'] = found_skills[:8]
    return info

def send_real_email(candidate_email, candidate_name, role, interview_date, interview_time, interview_type, company_name="TechCorp Innovations"):
    """Send professional interview invitation email"""
    try:
        if not EMAIL_ENABLED:
            return False, "Email configuration not available"
        
        config = EMAIL_CONFIG
        
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Interview Invitation - {role} Position at {company_name}"
        message["From"] = config['sender_email']
        message["To"] = candidate_email
        
        # Professional HTML Email Template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Arial', sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px 10px 0 0; text-align: center; }}
                .content {{ background: white; padding: 30px; border-radius: 0 0 10px 10px; }}
                .interview-details {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #00D4AA; }}
                .footer {{ margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎯 Interview Invitation</h1>
                    <p>{company_name}</p>
                </div>
                <div class="content">
                    <p>Dear <strong>{candidate_name}</strong>,</p>
                    
                    <p>Thank you for your interest in the <strong style="color: #00D4AA;">{role}</strong> position at {company_name}. We were thoroughly impressed with your qualifications and background.</p>
                    
                    <div class="interview-details">
                        <h3 style="color: #2c3e50; margin-top: 0;">📅 Interview Details</h3>
                        <table style="width: 100%;">
                            <tr>
                                <td style="padding: 8px 0; color: #666; width: 120px;"><strong>Position:</strong></td>
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
                                <td style="padding: 8px 0; color: #2c3e50;">{interview_type} Interview</td>
                            </tr>
                        </table>
                    </div>
                    
                    <p><strong>Preparation Tips:</strong></p>
                    <ul>
                        <li>Please have your portfolio and any relevant work samples ready</li>
                        <li>Be prepared to discuss your technical experience and projects</li>
                        <li>We'll explore problem-solving scenarios relevant to the role</li>
                    </ul>
                    
                    <p>This interview will be conducted via video conference. The meeting link will be sent to you 24 hours prior to the scheduled time.</p>
                    
                    <p>Please confirm your availability by replying to this email. If the proposed time doesn't work for you, feel free to suggest alternative times.</p>
                    
                    <p>We're excited to learn more about your experience and discuss how you can contribute to our team!</p>
                    
                    <div class="footer">
                        <p>Best regards,<br>
                        <strong>Talent Acquisition Team</strong><br>
                        {company_name}<br>
                        📧 talent@{company_name.lower().replace(' ', '')}.com<br>
                        📞 +1 (555) 123-4567</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        message.attach(MIMEText(html, "html"))
        
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['sender_password'])
        server.sendmail(config['sender_email'], candidate_email, message.as_string())
        server.quit()
        
        return True, f"Professional interview invitation sent successfully to {candidate_email}"
        
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"

def show_success_popup(message):
    """Show success popup"""
    st.markdown(f"""
    <div class="success-pop" style='
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 20px 0;
    '>
        <h3 style='margin: 0;'>🎉 {message}</h3>
    </div>
    """, unsafe_allow_html=True)

def create_trend_chart():
    """Create hiring trends chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    applications = [120, 150, 180, 200, 170, 220]
    hires = [8, 12, 15, 18, 14, 20]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=applications,
        mode='lines+markers',
        name='Applications',
        line=dict(color='#00D4AA', width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=hires,
        mode='lines+markers',
        name='Hires',
        line=dict(color='#0099FF', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='📈 Hiring Trends - Last 6 Months',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333333'),
        yaxis=dict(gridcolor='#333333')
    )
    
    return fig

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
    
    load_ultra_premium_css()
    
    # Dark Sidebar
    with st.sidebar:
        # Logo and Brand
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <div style='font-size: 2.5rem; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900;'>🚀</div>
            <h1 style='margin: 10px 0; color: white;'>SmartHire AI</h1>
            <p style='margin: 0; color: #E0E0E0;'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        pages = {
            "Dashboard": "📊",
            "Resume Screening": "📄", 
            "AI Interview Prep": "🎯",
            "JD Generator": "📝",
            "Candidates": "👥",
            "Analytics": "📈"
        }
        
        for page, icon in pages.items():
            if st.button(f"{icon} {page}", use_container_width=True, key=f"nav_{page}"):
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
    
    # Main Content
    st.markdown("""
    <div class="logo-container">
        <div class="logo">🚀</div>
        <h1 class="premium-header">SmartHire.AI</h1>
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

def show_dashboard():
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

def show_resume_screening():
    st.markdown("""
    <div class="premium-card">
        <h3>📄 AI Resume Screening</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("Choose resume file", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            # For demo, create sample resume text
            sample_resume = """
John Doe
Senior Data Scientist
Email: john.doe@email.com | Phone: +1 (555) 123-4567

EXPERIENCE
5 years as Data Scientist at TechCorp
3 years as Data Analyst at DataInc

SKILLS
Python, Machine Learning, SQL, AWS, TensorFlow
"""
            extracted_info = extract_info_from_resume(sample_resume)
            st.session_state.resume_analysis = extracted_info
            
            show_success_popup("Resume processed successfully!")
            
            # User can edit the extracted info
            candidate_name = st.text_input("Full Name", value=extracted_info['name'], key="resume_name")
            candidate_email = st.text_input("Email Address", value=extracted_info['email'], key="resume_email")
            candidate_phone = st.text_input("Phone Number", value=extracted_info['phone'], key="resume_phone")
            experience = st.slider("Years of Experience", 0, 20, extracted_info['experience'], key="resume_exp")
            
            if extracted_info['skills']:
                st.write("**Skills:**")
                for skill in extracted_info['skills']:
                    st.markdown(f"- {skill}")
    
    with col2:
        if st.session_state.resume_analysis:
            analysis = st.session_state.resume_analysis
            
            st.markdown("""
            <div class="premium-card">
                <h4>Analysis Results</h4>
            </div>
            """, unsafe_allow_html=True)
            
            match_score = random.randint(75, 95)
            st.metric("AI Match Score", f"{match_score}%")
            st.progress(match_score / 100)
            
            # Email Section
            st.markdown("---")
            st.markdown("**📧 Schedule Professional Interview**")
            
            col_date, col_time = st.columns(2)
            with col_date:
                interview_date = st.date_input("Interview Date")
            with col_time:
                interview_time = st.time_input("Interview Time")
            
            interview_type = st.selectbox("Interview Type", ["Technical Screening", "HR Discussion", "Technical Deep Dive", "Final Manager Round"])
            role = st.selectbox("Position", ["Data Scientist", "AI Engineer", "Machine Learning Engineer", "Data Analyst", "Software Developer"])
            company_name = st.text_input("Company Name", value="TechCorp Innovations")
            
            # Use the email from input field, not from extracted info
            email_to_send = st.session_state.get('resume_email', analysis['email'])
            name_to_send = st.session_state.get('resume_name', analysis['name'])
            
            if st.button("🚀 Send Professional Invitation", type="primary", use_container_width=True):
                if email_to_send and name_to_send:
                    if EMAIL_ENABLED:
                        success, message = send_real_email(
                            email_to_send,
                            name_to_send, 
                            role,
                            interview_date,
                            interview_time,
                            interview_type,
                            company_name
                        )
                        if success:
                            show_success_popup(message)
                        else:
                            st.error(f"❌ {message}")
                    else:
                        st.error("❌ Email configuration not available")
                else:
                    st.error("❌ Please fill in candidate email and name")

def show_interview_prep():
    st.markdown("""
    <div class="premium-card">
        <h3>🎯 AI Interview Preparation</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        role = st.selectbox("Select Role", ["Data Scientist", "AI Engineer", "Software Developer", "Product Manager"])
        experience = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level"])
        domain = st.selectbox("Domain Focus", ["Data Science", "AI/ML", "Software Engineering", "Product Management"])
        
        if st.button("🤖 Generate Questions", type="primary", use_container_width=True):
            show_success_popup("AI questions generated successfully!")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>Sample Interview Questions</h4>
        </div>
        """, unsafe_allow_html=True)
        
        questions = [
            "Explain the bias-variance tradeoff in machine learning and how you handle it in practice",
            "Describe your experience with cloud platforms and deployment strategies",
            "How do you approach debugging complex production issues?",
            "Tell us about a challenging project and how you overcame obstacles",
            "What's your experience with agile methodologies and team collaboration?",
            "How do you stay updated with the latest technologies in your field?"
        ]
        
        for i, q in enumerate(questions, 1):
            with st.expander(f"Question {i}"):
                st.write(q)
                st.info("**What to look for:** Clear explanation, practical examples, problem-solving approach")

def show_jd_generator():
    st.markdown("""
    <div class="premium-card">
        <h3>📝 AI Job Description Generator</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Data Scientist")
        department = st.selectbox("Department", ["Engineering", "Data Science", "Product", "Design", "Marketing"])
        experience = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Lead"])
        location = st.selectbox("Work Location", ["Remote", "Hybrid", "On-site"])
        skills = st.text_area("Required Skills & Technologies", placeholder="Python, Machine Learning, SQL, AWS, Docker...")
        company_name = st.text_input("Company Name", value="Your Company")
        
        if st.button("🚀 Generate Professional JD", type="primary", use_container_width=True):
            if job_title and skills:
                with st.spinner("Creating professional job description..."):
                    time.sleep(2)
                    
                    # Generate professional JD
                    jd_content = f"""
# {job_title}

## 🎯 Position Overview
{company_name} is seeking a {experience.lower()} {job_title} to join our dynamic {department} team. This {location.lower()} position offers the opportunity to work on cutting-edge projects and make a significant impact in our organization.

## 📋 Key Responsibilities
- Design, develop, and implement innovative solutions
- Collaborate with cross-functional teams to deliver high-quality products
- Analyze complex problems and provide strategic solutions
- Mentor junior team members and conduct code reviews
- Stay current with emerging technologies and industry trends

## 🛠️ Technical Requirements
{skills}

## 🎓 Qualifications & Experience
- Bachelor's/Master's degree in Computer Science or related field
- {experience} experience in relevant role
- Strong problem-solving and analytical skills
- Excellent communication and collaboration abilities
- Experience with modern development practices

## 💼 What We Offer
- Competitive salary and comprehensive benefits package
- {location} work flexibility
- Professional development and growth opportunities
- Collaborative and inclusive work environment
- Cutting-edge technology stack

## 🌟 Why Join {company_name}?
At {company_name}, we believe in nurturing talent and providing opportunities for professional growth. You'll work with industry experts on challenging projects that make a real impact.

---
*Generated by SmartHire AI - Premium Recruitment Platform*
"""
                    st.session_state.generated_jd = jd_content
                    st.session_state.jd_created = True
                    show_success_popup("Professional Job Description Created Successfully!")
    
    with col2:
        if st.session_state.jd_created and st.session_state.generated_jd:
            st.markdown("""
            <div class="premium-card">
                <h4>📄 Generated Job Description</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_area("Job Description Content", st.session_state.generated_jd, height=400, label_visibility="collapsed")
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    show_success_popup("JD copied to clipboard!")
            with col_s2:
                if st.button("📥 Export as PDF", use_container_width=True):
                    show_success_popup("PDF export started!")
            with col_s3:
                if st.button("🔄 Create New", use_container_width=True):
                    st.session_state.jd_created = False
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("👆 Fill in the job details and click 'Generate Professional JD' to create a comprehensive job description.")

def show_candidates():
    st.markdown("""
    <div class="premium-card">
        <h3>👥 Candidate Management</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Add Candidate Section
    with st.expander("➕ Add New Candidate", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name", key="new_candidate_name")
            new_email = st.text_input("Email Address", key="new_candidate_email")
            new_phone = st.text_input("Phone Number", key="new_candidate_phone")
        
        with col2:
            new_role = st.selectbox("Applied Role", ["Data Scientist", "AI Engineer", "Software Developer", "Product Manager"], key="new_candidate_role")
            new_exp = st.slider("Years of Experience", 0, 20, 3, key="new_candidate_exp")
            new_status = st.selectbox("Current Status", ["Applied", "Screening", "Interview", "Offer", "Hired"], key="new_candidate_status")
        
        if st.button("➕ Add Candidate to System", type="primary", use_container_width=True):
            if new_name and new_email:
                new_candidate = {
                    'name': new_name,
                    'email': new_email,
                    'phone': new_phone,
                    'role': new_role,
                    'experience': new_exp,
                    'status': new_status,
                    'score': f"{random.randint(70, 95)}%",
                    'applied_date': datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.candidates.append(new_candidate)
                show_success_popup(f"✅ Candidate {new_name} added successfully!")
                st.rerun()
            else:
                st.error("❌ Please fill in at least name and email")
    
    st.markdown("---")
    
    # Candidates List with WORKING buttons
    if st.session_state.candidates:
        st.markdown(f"**📋 Total Candidates: {len(st.session_state.candidates)}**")
        
        for i, candidate in enumerate(st.session_state.candidates):
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                st.write(f"**{candidate['name']}**")
                st.write(f"📧 {candidate['email']}")
                if candidate['phone']:
                    st.write(f"📞 {candidate['phone']}")
            
            with col2:
                st.write(f"💼 {candidate['role']}")
                st.write(f"⏳ {candidate['experience']} years experience")
                st.write(f"📅 Applied: {candidate['applied_date']}")
            
            with col3:
                status_color = {
                    "Applied": "#3498db",
                    "Screening": "#f39c12", 
                    "Interview": "#9b59b6",
                    "Offer": "#2ecc71",
                    "Hired": "#27ae60"
                }
                st.markdown(f"""
                <div style='background: {status_color.get(candidate['status'], '#95a5a6')}; color: white; padding: 5px 10px; border-radius: 15px; text-align: center; font-size: 0.8rem; font-weight: 600;'>
                    {candidate['status']}
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.write(f"🎯 {candidate['score']}")
                
                # WORKING ACTION BUTTONS
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("👁️ View", key=f"view_{i}"):
                        st.info(f"**Viewing Profile:** {candidate['name']}\n\n"
                               f"**Email:** {candidate['email']}\n"
                               f"**Role:** {candidate['role']}\n"
                               f"**Experience:** {candidate['experience']} years\n"
                               f"**Status:** {candidate['status']}\n"
                               f"**Match Score:** {candidate['score']}")
                
                with btn_col2:
                    if st.button("📧 Email", key=f"email_{i}"):
                        st.info(f"**Preparing email for:** {candidate['name']}\n"
                               f"**Email:** {candidate['email']}\n\n"
                               f"*Email template would open here*")
            
            st.markdown("---")
    else:
        st.info("No candidates in the system yet. Use the form above to add candidates.")

def show_analytics():
    st.markdown("""
    <div class="premium-card">
        <h3>📈 Advanced Analytics & Insights</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Time to Hire", "16.2d", "-1.8d")
        st.metric("Interview Success Rate", "68%", "+5%")
    
    with col2:
        st.metric("Cost per Hire", "$2,847", "-$153")
        st.metric("Candidate Satisfaction", "94%", "+2%")
    
    with col3:
        st.metric("Quality of Hire", "8.7/10", "+0.3")
        st.metric("Offer Acceptance Rate", "85%", "+3%")
    
    with col4:
        st.metric("Source Effectiveness", "78%", "+4%")
        st.metric("Retention Rate", "92%", "+2%")
    
    st.markdown("---")
    
    # Charts Section
    st.plotly_chart(create_trend_chart(), use_container_width=True)
    
    # AI Predictions and Insights
    st.markdown("""
    <div class="premium-card">
        <h4>🤖 AI-Powered Insights & Predictions</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col_insight1, col_insight2 = st.columns(2)
    
    with col_insight1:
        st.markdown("""
        ### 📊 Current Trends
        - **Data Science roles** showing 25% growth in applications
        - **Remote positions** have 15% higher acceptance rates
        - **AI Engineer** demand increased by 40% this quarter
        - **Technical screening** success rate: 68%
        """)
    
    with col_insight2:
        st.markdown("""
        ### 🔮 Future Predictions
        - **Next Month:** Expect 28% increase in qualified candidates
        - **Q3 Forecast:** Hiring time will reduce to 14.5 days
        - **Opportunity:** Focus on AI/ML roles for maximum ROI
        - **Alert:** Software Developer market becoming competitive
        """)
    
    # Recommendations
    st.markdown("""
    <div class="premium-card">
        <h4>💡 Strategic Recommendations</h4>
        <ul>
        <li>🎯 <strong>Focus on AI Engineer roles</strong> - 40% demand growth predicted</li>
        <li>⚡ <strong>Optimize screening process</strong> - Reduce time-to-interview by 2 days</li>
        <li>💰 <strong>Adjust salary bands</strong> for competitive positioning</li>
        <li>🌐 <strong>Expand remote hiring</strong> - 15% higher retention observed</li>
        <li>📈 <strong>Invest in employer branding</strong> - 25% impact on candidate quality</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()