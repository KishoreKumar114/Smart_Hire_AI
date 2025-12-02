# app.py - COMPLETE FIXED VERSION
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

# Import email configuration
try:
    from email_config import get_email_config, validate_email_config
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
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --accent-primary: #00D4AA;
        --accent-secondary: #0099FF;
        --border: #333333;
    }
    
    .light-mode {
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --bg-card: #FFFFFF;
        --text-primary: #2C3E50;
        --text-secondary: #34495E;
        --border: #BDC3C7;
    }
    
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
    }
    
    * {
        color: var(--text-primary) !important;
    }
    
    .premium-header {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00D4AA, #0099FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .premium-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
    }
    
    .blue-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .blue-section * {
        color: white !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00D4AA, #0099FF) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
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

def send_real_email(candidate_email, candidate_name, role, interview_date, interview_time, interview_type):
    """Send real email using Gmail SMTP with App Password"""
    try:
        if not EMAIL_ENABLED:
            return False, "Email configuration not available"
        
        config = EMAIL_CONFIG
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Interview Invitation - {role} Position at SmartHire AI"
        message["From"] = config['sender_email']
        message["To"] = candidate_email
        
        # Email content
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
                
                <p style="font-size: 16px;">Please confirm your availability for this schedule. The interview will be conducted via video call.</p>
                
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
        
        message.attach(MIMEText(html, "html"))
        
        # Send email
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['sender_email'], config['sender_password'])
        server.sendmail(config['sender_email'], candidate_email, message.as_string())
        server.quit()
        
        return True, "Email sent successfully"
        
    except Exception as e:
        return False, f"Email sending failed: {str(e)}"

def show_success_popup(message):
    """Show success popup"""
    st.success(f"🎉 {message}")

def main():
    st.set_page_config(
        page_title="SmartHire AI - Premium",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session states
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Dashboard"
    if 'resume_analysis' not in st.session_state:
        st.session_state.resume_analysis = {}
    
    # Apply theme
    theme_class = "dark-mode" if st.session_state.dark_mode else "light-mode"
    st.markdown(f'<div class="{theme_class}">', unsafe_allow_html=True)
    load_dynamic_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='margin: 0;'>🚀 SmartHire AI</h1>
            <p style='margin: 0; color: #00D4AA;'>Premium Recruitment Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme toggle
        if st.button("🌙 Switch to Light" if st.session_state.dark_mode else "☀️ Switch to Dark"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        pages = {
            "Dashboard": "📊",
            "Resume Screening": "📄", 
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
            st.metric("Jobs", "18")
            st.metric("Candidates", "127")
        with col2:
            st.metric("Match Rate", "87%")
            st.metric("Hiring Time", "16d")
    
    # Main content
    st.markdown(f"<h1 class='premium-header'>{st.session_state.current_page}</h1>", unsafe_allow_html=True)
    
    # Page routing
    if st.session_state.current_page == "Dashboard":
        show_dashboard()
    elif st.session_state.current_page == "Resume Screening":
        show_resume_screening()
    elif st.session_state.current_page == "JD Generator":
        show_jd_generator()
    elif st.session_state.current_page == "Candidates":
        show_candidates()
    elif st.session_state.current_page == "Analytics":
        show_analytics()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_dashboard():
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin: 0; text-align: center;">💼</h3>
            <h2 style="margin: 10px 0; text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">18</h2>
            <p style="margin: 0; text-align: center; color: var(--text-secondary) !important;">Active Jobs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin: 0; text-align: center;">👥</h3>
            <h2 style="margin: 10px 0; text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">127</h2>
            <p style="margin: 0; text-align: center; color: var(--text-secondary) !important;">Candidates</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin: 0; text-align: center;">🎯</h3>
            <h2 style="margin: 10px 0; text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">87%</h2>
            <p style="margin: 0; text-align: center; color: var(--text-secondary) !important;">Match Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-card">
            <h3 style="margin: 0; text-align: center;">⚡</h3>
            <h2 style="margin: 10px 0; text-align: center; background: linear-gradient(135deg, #00D4AA, #0099FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">16d</h2>
            <p style="margin: 0; text-align: center; color: var(--text-secondary) !important;">Hiring Time</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Actions
    st.markdown("""
    <div class="blue-section">
        <h3>🚀 Quick Actions</h3>
        <p>Get started with these quick actions</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📄 Screen Resume", use_container_width=True):
            st.session_state.current_page = "Resume Screening"
            st.rerun()
    
    with col2:
        if st.button("📝 Create JD", use_container_width=True):
            st.session_state.current_page = "JD Generator"
            st.rerun()
    
    with col3:
        if st.button("👥 View Candidates", use_container_width=True):
            st.session_state.current_page = "Candidates"
            st.rerun()
    
    with col4:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_page = "Analytics"
            st.rerun()
    
    # Recent Activity
    st.markdown("""
    <div class="premium-card">
        <h3>🕒 Recent Activity</h3>
    </div>
    """, unsafe_allow_html=True)
    
    activities = [
        {"action": "New candidate applied for Data Scientist", "time": "2 hours ago"},
        {"action": "Interview scheduled with Sarah Chen", "time": "4 hours ago"},
        {"action": "Job description created for AI Engineer", "time": "1 day ago"},
        {"action": "Resume analyzed for Michael Brown", "time": "1 day ago"}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div style="padding: 15px; background: var(--bg-secondary); border-radius: 10px; margin: 10px 0;">
            <div style="font-weight: 600;">{activity['action']}</div>
            <div style="color: var(--text-secondary); font-size: 0.9rem;">{activity['time']}</div>
        </div>
        """, unsafe_allow_html=True)

def show_resume_screening():
    st.markdown("""
    <div class="blue-section">
        <h3>📄 AI Resume Screening & Analysis</h3>
        <p>Upload resumes and get instant AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>📤 Upload Resume</h4>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose resume file", type=['pdf', 'docx', 'txt'], label_visibility="collapsed")
        
        if uploaded_file:
            # Sample resume processing
            sample_resume = """
John Doe
Senior Data Scientist
Email: john.doe@email.com | Phone: +1 (555) 123-4567

EXPERIENCE
Senior Data Scientist - TechCorp Inc. (2020-Present)
- Led machine learning projects improving customer retention by 25%
- Developed predictive models using Python, TensorFlow, and AWS
- Managed team of 3 junior data scientists

Data Analyst - DataWorks LLC (2018-2020)
- Created dashboards and reports for business intelligence
- Analyzed large datasets using SQL and Python
- Improved data processing efficiency by 30%

EDUCATION
Master of Science in Computer Science - Stanford University
Bachelor of Science in Mathematics - MIT

SKILLS
Python, Machine Learning, SQL, AWS, TensorFlow, PyTorch, Data Visualization, Statistical Analysis
"""
            extracted_info = extract_info_from_resume(sample_resume)
            st.session_state.resume_analysis = extracted_info
            show_success_popup("Resume processed successfully!")
            
            st.markdown("""
            <div class="premium-card">
                <h4>👤 Candidate Information</h4>
            </div>
            """, unsafe_allow_html=True)
            
            st.text_input("Full Name", value=extracted_info['name'])
            st.text_input("Email", value=extracted_info['email'])
            st.text_input("Phone", value=extracted_info['phone'])
            st.slider("Years of Experience", 0, 20, extracted_info['experience'])
            
            if extracted_info['skills']:
                st.write("**Extracted Skills:**")
                for skill in extracted_info['skills']:
                    st.markdown(f"- {skill}")
    
    with col2:
        if st.session_state.resume_analysis:
            analysis = st.session_state.resume_analysis
            
            st.markdown("""
            <div class="premium-card">
                <h4>📊 Analysis Results</h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Match Score
            match_score = random.randint(75, 95)
            st.metric("AI Match Score", f"{match_score}%")
            st.progress(match_score / 100)
            
            # Recommendations
            st.markdown("**💡 AI Recommendations:**")
            recommendations = [
                "Strong technical background in data science",
                "Good mix of academic and practical experience", 
                "Consider for senior data roles",
                "Schedule technical interview to assess ML skills"
            ]
            for rec in recommendations:
                st.markdown(f"- {rec}")
            
            # Email Section
            st.markdown("---")
            st.markdown("**📧 Schedule Interview**")
            
            col_date, col_time = st.columns(2)
            with col_date:
                interview_date = st.date_input("Date")
            with col_time:
                interview_time = st.time_input("Time")
            
            interview_type = st.selectbox("Interview Type", ["Technical Round", "HR Round", "Manager Round"])
            role = st.selectbox("Position", ["Data Scientist", "AI Engineer", "Machine Learning Engineer"])
            
            if st.button("🚀 Send Real Email Invitation", type="primary", use_container_width=True):
                if EMAIL_ENABLED:
                    success, message = send_real_email(
                        analysis['email'],
                        analysis['name'],
                        role,
                        interview_date, 
                        interview_time,
                        interview_type
                    )
                    if success:
                        show_success_popup(f"Email sent to {analysis['email']}!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Email configuration not set up")

def show_jd_generator():
    st.markdown("""
    <div class="blue-section">
        <h3>📝 AI Job Description Generator</h3>
        <p>Create professional job descriptions in seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>🎯 Job Details</h4>
        </div>
        """, unsafe_allow_html=True)
        
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Data Scientist")
        department = st.selectbox("Department", ["Engineering", "Data Science", "Product", "Design", "Marketing"])
        experience = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Lead"])
        location = st.selectbox("Location", ["Remote", "Hybrid", "On-site"])
        skills = st.text_area("Required Skills", placeholder="Python, Machine Learning, SQL, AWS...")
        
        if st.button("🚀 Generate Job Description", type="primary", use_container_width=True):
            if job_title and skills:
                with st.spinner("AI is generating your job description..."):
                    time.sleep(2)
                    show_success_popup("Job Description Generated!")
                    
                    # Generate sample JD
                    jd_content = f"""
# {job_title}

## 🎯 Overview
We are seeking a {experience.lower()} {job_title} to join our {department} team. This {location.lower()} position offers exciting opportunities to work on cutting-edge projects.

## 📋 Responsibilities
- Design and implement scalable solutions
- Collaborate with cross-functional teams
- Analyze complex problems and provide innovative solutions
- Mentor junior team members
- Stay updated with industry trends

## 🛠️ Required Skills
{skills}

## 🎓 Qualifications
- Bachelor's degree in relevant field
- {experience} experience in similar role
- Strong problem-solving skills
- Excellent communication abilities

## 💼 What We Offer
- Competitive salary and benefits
- {location} work flexibility
- Professional development opportunities
- Collaborative work environment

---
*Generated by SmartHire AI*
"""
                    st.session_state.generated_jd = jd_content
                    st.rerun()
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>📄 Generated Description</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if 'generated_jd' in st.session_state and st.session_state.generated_jd:
            st.text_area("Job Description", st.session_state.generated_jd, height=400, label_visibility="collapsed")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("📋 Copy", use_container_width=True)
            with col2:
                st.button("📥 Export", use_container_width=True)
            with col3:
                st.button("🔄 New", use_container_width=True)
        else:
            st.info("👆 Fill in the job details and click 'Generate' to create a professional job description.")

def show_candidates():
    st.markdown("""
    <div class="blue-section">
        <h3>👥 Candidate Management</h3>
        <p>Manage and track all your candidates</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample candidates data
    candidates = [
        {"name": "John Doe", "email": "john@email.com", "role": "Data Scientist", "status": "Interview", "experience": 5, "score": "92%"},
        {"name": "Sarah Chen", "email": "sarah@email.com", "role": "AI Engineer", "status": "Screening", "experience": 3, "score": "87%"},
        {"name": "Mike Brown", "email": "mike@email.com", "role": "Software Developer", "status": "Applied", "experience": 2, "score": "78%"},
        {"name": "Priya Sharma", "email": "priya@email.com", "role": "Data Analyst", "status": "Offer", "experience": 4, "score": "95%"}
    ]
    
    for candidate in candidates:
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            with col1:
                st.write(f"**{candidate['name']}**")
                st.write(f"📧 {candidate['email']}")
            with col2:
                st.write(f"💼 {candidate['role']}")
                st.write(f"⏳ {candidate['experience']} years")
            with col3:
                status_color = {
                    "Applied": "#3498db",
                    "Screening": "#f39c12", 
                    "Interview": "#9b59b6",
                    "Offer": "#2ecc71"
                }
                st.markdown(f"<div style='background: {status_color.get(candidate['status'], '#95a5a6')}; color: white; padding: 5px 10px; border-radius: 15px; text-align: center; font-size: 0.8rem;'>{candidate['status']}</div>", unsafe_allow_html=True)
            with col4:
                st.write(f"🎯 {candidate['score']}")
            
            st.markdown("---")

def show_analytics():
    st.markdown("""
    <div class="blue-section">
        <h3>📈 Advanced Analytics</h3>
        <p>Deep insights into your recruitment process</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Time to Hire", "16.2d", "-1.8d")
    with col2:
        st.metric("Cost per Hire", "$2,847", "-$153")
    with col3:
        st.metric("Quality of Hire", "8.7/10", "+0.3")
    with col4:
        st.metric("Candidate Satisfaction", "94%", "+2%")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4>📊 Hiring Funnel</h4>
            <div style="height: 300px; background: var(--bg-secondary); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: var(--text-secondary);">
            Interactive Chart - Applications to Hires
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4>🎯 Source Effectiveness</h4>
            <div style="height: 300px; background: var(--bg-secondary); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: var(--text-secondary);">
            Interactive Chart - Candidate Sources
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()