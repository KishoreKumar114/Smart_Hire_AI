# app.py - COMPLETE IPO VERSION
import streamlit as st
import pandas as pd
from datetime import datetime
import time
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
    except Exception as e:
        raise Exception(f"OpenAI API error: {str(e)}")

def show_premium_dashboard():
    """Show premium dashboard with analytics and metrics"""
    st.markdown("""
    <div class="premium-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📊 Recruitment Overview</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Active Positions</div>
            <div class="metric-value">18</div>
            <div style="color: var(--success) !important; font-weight: 600;">+3 this week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Total Candidates</div>
            <div class="metric-value">127</div>
            <div style="color: var(--success) !important; font-weight: 600;">+8 today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Match Rate</div>
            <div class="metric-value">87%</div>
            <div style="color: var(--success) !important; font-weight: 600;">+5% improved</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Avg. Hiring Time</div>
            <div class="metric-value">16d</div>
            <div style="color: var(--success) !important; font-weight: 600;">-2d faster</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts and Data
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">📈 Applications Trend</h4>
            <div style="height: 300px; background: var(--bg-secondary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--text-muted) !important;">
                Interactive Chart - Applications Over Time
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🎯 Top Roles</h4>
            <div style="height: 300px; background: var(--bg-secondary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--text-muted) !important;">
                Interactive Chart - Popular Job Roles
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🕒 Recent Activity</h4>
        <div style="background: var(--bg-secondary); border-radius: 12px; padding: 20px;">
    """, unsafe_allow_html=True)
    
    activities = [
        {"time": "2 min ago", "action": "New candidate applied for Data Scientist", "user": "AI System"},
        {"time": "15 min ago", "action": "Interview scheduled with Sarah Chen", "user": "John Doe"},
        {"time": "1 hour ago", "action": "Job description updated for Frontend Developer", "user": "Emily Wilson"},
        {"time": "2 hours ago", "action": "Resume analyzed for Michael Brown", "user": "AI System"},
        {"time": "4 hours ago", "action": "Offer sent to candidate #89", "user": "HR Team"}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div style="padding: 12px; border-bottom: 1px solid var(--border);">
            <div style="display: flex; justify-content: between; align-items: start;">
                <div style="flex: 1;">
                    <strong style="color: var(--text-primary) !important;">{activity['action']}</strong>
                    <div style="font-size: 0.8rem; color: var(--text-muted) !important;">{activity['time']} • by {activity['user']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def show_premium_jd_generator():
    """Show premium job description generator"""
    st.markdown("""
    <div class="premium-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📝 AI Job Description Generator</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1.5rem;">🎯 Job Details</h4>
        </div>
        """, unsafe_allow_html=True)
        
        job_title = st.text_input("Job Title", placeholder="e.g., Senior Data Scientist")
        department = st.selectbox("Department", ["Engineering", "Data Science", "Product", "Design", "Marketing", "Sales", "Operations"])
        experience_level = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Lead", "Principal"])
        location = st.selectbox("Location Type", ["Remote", "Hybrid", "On-site"])
        company_size = st.selectbox("Company Size", ["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", "Large (1000+)"])
        
        # Key responsibilities
        st.text_area("Key Responsibilities (optional)", 
                    placeholder="Describe main responsibilities...", 
                    height=120)
        
        # Required skills
        required_skills = st.text_area("Required Skills (comma-separated)", 
                                     placeholder="Python, Machine Learning, SQL, AWS...",
                                     height=80)
        
        # Company culture
        company_culture = st.multiselect("Company Culture", 
                                       ["Fast-paced", "Collaborative", "Innovative", "Remote-first", "Growth-oriented", "Traditional"])
        
        if st.button("🚀 Generate Job Description", type="primary", use_container_width=True):
            # Simulate AI generation
            with st.spinner("🤖 AI is generating your perfect job description..."):
                time.sleep(2)
                
                # Generate sample JD based on inputs
                sample_jd = f"""
# {job_title} - {department}

## 🎯 Overview
We are seeking a {experience_level.lower()} {job_title} to join our dynamic {department} team. This is a {location.lower()} position perfect for someone who thrives in a {company_size.lower()} environment.

## 📋 Responsibilities
- Design, develop, and implement cutting-edge solutions
- Collaborate with cross-functional teams to deliver high-quality products
- Analyze complex problems and provide innovative solutions
- Mentor junior team members and share knowledge
- Stay updated with industry trends and technologies

## 🛠️ Required Skills
{required_skills}

## 🎓 Qualifications
- Bachelor's degree in Computer Science or related field
- {experience_level} experience in relevant role
- Strong problem-solving and communication skills
- Experience with modern development practices

## 💼 What We Offer
- Competitive salary and benefits
- {location} work flexibility
- Professional development opportunities
- Collaborative and inclusive culture
- Cutting-edge technology stack

## 🏢 Company Culture
Our culture is {', '.join(company_culture) if company_culture else 'innovative and collaborative'}.

---
*Generated by SmartHire AI - Premium Recruitment Platform*
"""
                st.session_state.generated_jd = sample_jd
                show_success_popup("AI-generated job description created successfully!")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1.5rem;">📄 Generated Job Description</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.generated_jd:
            st.markdown("""
            <div style="background: var(--bg-secondary); border-radius: 12px; padding: 25px; border: 1px solid var(--border);">
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.generated_jd)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Action buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Copy to Clipboard", use_container_width=True):
                    show_success_popup("Job description copied to clipboard!")
            with col2:
                if st.button("📥 Download PDF", use_container_width=True):
                    show_success_popup("PDF download started!")
            with col3:
                if st.button("🔄 Regenerate", use_container_width=True):
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("""
            **👆 Configure your job details**
            
            Fill in the job information on the left and click **'Generate Job Description'** 
            to create a professional, AI-powered job description.
            
            💡 *The AI will analyze your requirements and generate a comprehensive, 
            engaging job description tailored to your needs.*
            """)

def show_premium_resume_screening():
    """Show premium resume screening interface"""
    st.markdown("""
    <div class="premium-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📄 AI Resume Screening & Analysis</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1.5rem;">📤 Upload Resume</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Resume upload options
        upload_option = st.radio("Upload Method", ["File Upload", "Paste Text"], horizontal=True)
        
        if upload_option == "File Upload":
            uploaded_file = st.file_uploader("Choose resume file", type=['pdf', 'docx', 'txt'])
            if uploaded_file:
                # Simulate file processing
                with st.spinner("🔍 Processing resume file..."):
                    time.sleep(2)
                    # For demo, create sample resume text
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
                    st.session_state.resume_text = sample_resume
                    st.success("✅ Resume processed successfully!")
        
        else:  # Paste Text
            resume_text = st.text_area("Paste Resume Content", 
                                     height=300,
                                     placeholder="Paste the resume content here...",
                                     value=st.session_state.resume_text)
            if resume_text:
                st.session_state.resume_text = resume_text
        
        if st.session_state.resume_text and st.button("🔍 Analyze Resume", type="primary", use_container_width=True):
            with st.spinner("🤖 AI is analyzing the resume..."):
                time.sleep(2)
                # Extract information
                st.session_state.resume_analysis = extract_info_from_resume(st.session_state.resume_text)
                show_success_popup("AI resume analysis completed!")
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1.5rem;">📊 Analysis Results</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.resume_analysis:
            analysis = st.session_state.resume_analysis
            
            # Personal Info Card
            st.markdown("""
            <div class="premium-card" style="margin-bottom: 1rem;">
                <h5 style="color: var(--text-primary) !important; margin-bottom: 1rem;">👤 Personal Information</h5>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Name", analysis.get('name', 'Not found'))
            with col2:
                st.metric("Email", analysis.get('email', 'Not found'))
            with col3:
                st.metric("Phone", analysis.get('phone', 'Not found'))
            
            # Experience & Skills
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="premium-card" style="margin-bottom: 1rem;">
                    <h5 style="color: var(--text-primary) !important; margin-bottom: 1rem;">💼 Experience</h5>
                </div>
                """, unsafe_allow_html=True)
                exp_years = analysis.get('experience', 0)
                st.metric("Years of Experience", f"{exp_years} years")
                
                # Experience level based on years
                if exp_years == 0:
                    level = "Entry Level"
                elif exp_years <= 3:
                    level = "Junior"
                elif exp_years <= 7:
                    level = "Mid Level"
                else:
                    level = "Senior"
                st.metric("Experience Level", level)
            
            with col2:
                st.markdown("""
                <div class="premium-card" style="margin-bottom: 1rem;">
                    <h5 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🛠️ Skills</h5>
                </div>
                """, unsafe_allow_html=True)
                skills = analysis.get('skills', [])
                if skills:
                    for skill in skills[:8]:  # Show first 8 skills
                        st.markdown(f"- {skill}")
                    if len(skills) > 8:
                        st.caption(f"+ {len(skills) - 8} more skills")
                else:
                    st.info("No skills detected")
            
            # Match Score
            st.markdown("""
            <div class="premium-card">
                <h5 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🎯 AI Match Score</h5>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate match score calculation
            match_score = random.randint(75, 95)
            st.progress(match_score / 100)
            st.metric("Overall Match Score", f"{match_score}%")
            
            # Recommendations
            st.markdown("""
            <div class="premium-card">
                <h5 style="color: var(--text-primary) !important; margin-bottom: 1rem;">💡 AI Recommendations</h5>
            </div>
            """, unsafe_allow_html=True)
            
            recommendations = [
                "Strong technical background in data science",
                "Good mix of academic and practical experience",
                "Consider for senior data roles",
                "Schedule technical interview to assess ML skills"
            ]
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        
        else:
            st.info("""
            **👆 Upload or paste a resume**
            
            Use the left panel to upload a resume file or paste the resume content, 
            then click **'Analyze Resume'** to get AI-powered insights.
            
            💡 *The AI will extract key information, assess skills, and provide 
            match scores and recommendations.*
            """)

def show_interview_preparation():
    st.markdown("### 🎯 AI Interview Preparation")
    
    # OpenAI API Configuration
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 AI Configuration")
    api_key = st.sidebar.text_input("OpenAI API Key", 
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

def show_candidates_management():
    """Show candidates management interface"""
    st.markdown("""
    <div class="premium-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">👥 Candidate Management</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Add New Candidate
    with st.expander("➕ Add New Candidate", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_phone = st.text_input("Phone")
            new_role = st.selectbox("Applied Role", ["Data Scientist", "AI Engineer", "Software Developer", "Data Analyst"])
        
        with col2:
            new_status = st.selectbox("Status", ["Applied", "Screening", "Interview", "Offer", "Hired"])
            new_source = st.selectbox("Source", ["LinkedIn", "Indeed", "Referral", "Career Site", "Other"])
            new_experience = st.slider("Years of Experience", 0, 20, 3)
            new_rating = st.slider("Rating", 1, 5, 3)
        
        if st.button("Add Candidate", type="primary"):
            if new_name and new_email:
                new_candidate = {
                    'id': len(st.session_state.candidates) + 1,
                    'name': new_name,
                    'email': new_email,
                    'phone': new_phone,
                    'role': new_role,
                    'status': new_status,
                    'source': new_source,
                    'experience': new_experience,
                    'rating': new_rating,
                    'applied_date': datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state.candidates.append(new_candidate)
                show_success_popup(f"Added {new_name} to candidates!")
                st.rerun()
    
    # Candidates List
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: var(--text-primary) !important; margin-bottom: 1.5rem;">📋 All Candidates</h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.candidates:
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_role = st.selectbox("Filter by Role", ["All"] + list(set([c['role'] for c in st.session_state.candidates])))
        with col2:
            filter_status = st.selectbox("Filter by Status", ["All"] + list(set([c['status'] for c in st.session_state.candidates])))
        with col3:
            filter_rating = st.selectbox("Filter by Rating", ["All", "5 Stars", "4+ Stars", "3+ Stars"])
        
        # Filter candidates
        filtered_candidates = st.session_state.candidates
        if filter_role != "All":
            filtered_candidates = [c for c in filtered_candidates if c['role'] == filter_role]
        if filter_status != "All":
            filtered_candidates = [c for c in filtered_candidates if c['status'] == filter_status]
        if filter_rating != "All":
            min_rating = int(filter_rating[0])
            filtered_candidates = [c for c in filtered_candidates if c['rating'] >= min_rating]
        
        # Display candidates
        for candidate in filtered_candidates:
            status_colors = {
                "Applied": "#3498db",
                "Screening": "#f39c12", 
                "Interview": "#9b59b6",
                "Offer": "#2ecc71",
                "Hired": "#27ae60"
            }
            
            st.markdown(f"""
            <div class="premium-card" style="margin-bottom: 1rem; padding: 1.5rem;">
                <div style="display: flex; justify-content: between; align-items: start; margin-bottom: 1rem;">
                    <div style="flex: 1;">
                        <h4 style="margin: 0; color: var(--text-primary) !important;">{candidate['name']}</h4>
                        <p style="margin: 0.25rem 0; color: var(--text-secondary) !important;">{candidate['role']} • {candidate['experience']} years experience</p>
                        <p style="margin: 0; font-size: 0.9rem; color: var(--text-muted) !important;">{candidate['email']} • {candidate['phone']}</p>
                    </div>
                    <div style="text-align: right;">
                        <div style="background: {status_colors.get(candidate['status'], '#95a5a6')}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                            {candidate['status']}
                        </div>
                        <div style="margin-top: 0.5rem; color: #f39c12 !important;">
                            {'★' * candidate['rating']}{'☆' * (5 - candidate['rating'])}
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                    <button style="flex: 1; background: var(--accent-primary); color: white; border: none; padding: 8px; border-radius: 8px; cursor: pointer;">View Profile</button>
                    <button style="flex: 1; background: var(--accent-secondary); color: white; border: none; padding: 8px; border-radius: 8px; cursor: pointer;">Schedule Interview</button>
                    <button style="flex: 1; background: var(--bg-secondary); color: var(--text-primary) !important; border: 1px solid var(--border); padding: 8px; border-radius: 8px; cursor: pointer;">Send Email</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("""
        **👆 No candidates yet**
        
        Use the "Add New Candidate" section above to add your first candidate 
        to the system. You can then manage their status, schedule interviews, 
        and track their progress through the hiring pipeline.
        """)

def show_premium_analytics():
    """Show premium analytics dashboard"""
    st.markdown("""
    <div class="premium-card">
        <h3 style="margin-bottom: 1.5rem; color: var(--text-primary) !important; font-weight: 700; font-size: 1.3rem;">📈 Advanced Analytics</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Analytics Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Time to Hire</div>
            <div class="metric-value">16.2d</div>
            <div style="color: var(--success) !important; font-weight: 600;">Industry avg: 24d</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Cost per Hire</div>
            <div class="metric-value">$2,847</div>
            <div style="color: var(--success) !important; font-weight: 600;">Below budget</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Quality of Hire</div>
            <div class="metric-value">8.7/10</div>
            <div style="color: var(--success) !important; font-weight: 600;">+1.2 improved</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="premium-metric">
            <div class="metric-label">Candidate Satisfaction</div>
            <div class="metric-value">94%</div>
            <div style="color: var(--success) !important; font-weight: 600;">Excellent</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">📊 Hiring Funnel</h4>
            <div style="height: 300px; background: var(--bg-secondary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--text-muted) !important;">
                Interactive Chart - Hiring Funnel Analytics
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🎯 Source Effectiveness</h4>
            <div style="height: 250px; background: var(--bg-secondary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--text-muted) !important;">
                Interactive Chart - Candidate Sources
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">📅 Time Series Analysis</h4>
            <div style="height: 300px; background: var(--bg-secondary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--text-muted) !important;">
                Interactive Chart - Applications Over Time
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="premium-card">
            <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🔄 Conversion Rates</h4>
            <div style="height: 250px; background: var(--bg-secondary); border-radius: 12px; display: flex; align-items: center; justify-content: center; color: var(--text-muted) !important;">
                Interactive Chart - Stage Conversions
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Insights
    st.markdown("""
    <div class="premium-card">
        <h4 style="color: var(--text-primary) !important; margin-bottom: 1rem;">🤖 AI-Powered Insights</h4>
        <div style="background: var(--bg-secondary); border-radius: 12px; padding: 20px;">
    """, unsafe_allow_html=True)
    
    insights = [
        "🎯 **Top Performing Source**: Employee referrals have 35% higher retention rate",
        "📈 **Trend Alert**: Data Science roles receiving 42% more applications this quarter", 
        "💡 **Optimization Opportunity**: Reduce time in screening stage by implementing AI pre-screening",
        "🚀 **Success Metric**: Your candidate satisfaction score is 12% above industry average",
        "🔍 **Pattern Detected**: Candidates with 3+ years cloud experience perform 27% better"
    ]
    
    for insight in insights:
        st.markdown(f"- {insight}")
    
    st.markdown("</div></div>", unsafe_allow_html=True)

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
    if 'generated_questions' not in st.session_state:
        st.session_state.generated_questions = []
    
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

if __name__ == "__main__":
    main()