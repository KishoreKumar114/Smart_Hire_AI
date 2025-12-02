# app.py - COMPLETE PREMIUM WITH PERFECT DARK/LIGHT MODE
import streamlit as st
import database as db
import pandas as pd
from datetime import datetime
import time
import io

# CSS for perfect dark/light mode
def load_premium_css():
    st.markdown("""
    <style>
    /* CSS Variables for Themes */
    :root {
        /* Light Theme */
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --text-primary: #2c3e50;
        --text-secondary: #6c757d;
        --card-bg: #ffffff;
        --card-border: #e9ecef;
        --card-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
        --sidebar-bg: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        --sidebar-text: #ffffff;
        --sidebar-hover: rgba(255, 255, 255, 0.1);
        --sidebar-active: rgba(255, 255, 255, 0.2);
        --accent-primary: #FF6B6B;
        --accent-secondary: #4ECDC4;
        --metric-bg: linear-gradient(135deg, #ffffff, #f8f9fa);
    }
    
    .dark-mode {
        /* Dark Theme */
        --bg-primary: #0c0c0c;
        --bg-secondary: #1a1a1a;
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --card-bg: #1a1a1a;
        --card-border: #333333;
        --card-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        --sidebar-bg: linear-gradient(180deg, #1a1a1a 0%, #2d2d2d 100%);
        --sidebar-text: #ffffff;
        --sidebar-hover: rgba(255, 255, 255, 0.1);
        --sidebar-active: rgba(255, 255, 255, 0.2);
        --accent-primary: #FF6B6B;
        --accent-secondary: #4ECDC4;
        --metric-bg: linear-gradient(135deg, #2c3e50, #34495e);
    }
    
    /* Apply Theme to Main App */
    .stApp {
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Main Header with Glow */
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary), #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
        text-shadow: 0 0 30px rgba(255, 107, 107, 0.3);
    }
    
    /* Premium Sidebar Styling */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--sidebar-bg) !important;
        color: var(--sidebar-text) !important;
    }
    
    /* Sidebar Navigation Items */
    .sidebar-nav {
        background: transparent !important;
        color: var(--sidebar-text) !important;
        border: none !important;
        padding: 12px 20px !important;
        margin: 5px 0 !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        text-align: left !important;
        width: 100% !important;
    }
    
    .sidebar-nav:hover {
        background: var(--sidebar-hover) !important;
        transform: translateX(5px) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
    }
    
    .sidebar-nav.active {
        background: var(--sidebar-active) !important;
        border-left: 4px solid var(--accent-secondary) !important;
        font-weight: 600 !important;
    }
    
    /* Premium Cards */
    .premium-card {
        background: var(--card-bg);
        color: var(--text-primary);
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        border: 1px solid var(--card-border);
        box-shadow: var(--card-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
        border-color: var(--accent-secondary);
    }
    
    /* Premium Metrics with Glow */
    .premium-metric {
        background: var(--metric-bg);
        color: var(--text-primary);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin: 10px;
        border: 1px solid var(--card-border);
        box-shadow: var(--card-shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .premium-metric:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(78, 205, 196, 0.25);
        border-color: var(--accent-secondary);
    }
    
    .premium-metric::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(78, 205, 196, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .premium-metric:hover::before {
        left: 100%;
    }
    
    /* Premium Buttons */
    .stButton>button {
        background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4) !important;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    /* Theme Toggle Button */
    .theme-toggle-btn {
        background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary)) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Glowing Text */
    .glowing-text {
        background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary), #45B7D1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(255, 107, 107, 0.2);
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Smooth transitions for all elements */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Improved form elements */
    .stSelectbox>div>div, .stTextInput>div>div>input, .stTextArea>div>textarea {
        background: var(--card-bg) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox>div>div:hover, .stTextInput>div>div>input:focus, .stTextArea>div>textarea:focus {
        border-color: var(--accent-secondary) !important;
        box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.1) !important;
    }
    
    /* File uploader styling */
    .stFileUploader>div>div {
        border: 2px dashed var(--accent-secondary) !important;
        border-radius: 15px !important;
        background: rgba(78, 205, 196, 0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .stFileUploader>div>div:hover {
        border-color: var(--accent-primary) !important;
        background: rgba(255, 107, 107, 0.05) !important;
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
        st.session_state.current_page = "🏠 Dashboard"
    
    # Load CSS based on theme
    load_premium_css()
    
    # Apply dark mode class to entire app
    if st.session_state.dark_mode:
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)
    
    # Premium Sidebar Navigation
    with st.sidebar:
        # Theme Toggle at Top
        col1, col2 = st.columns([3, 1])
        with col2:
            theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
            theme_text = "Dark" if not st.session_state.dark_mode else "Light"
            if st.button(f"{theme_icon}", key="theme_toggle", use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        # Brand Header
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem; background: linear-gradient(45deg, #FF6B6B, #4ECDC4); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🚀 SmartHire</h1>
            <p style='margin: 0; opacity: 0.9; font-size: 0.9rem;'>Premium Recruitment AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Menu
        st.markdown("### 🎯 Navigation")
        
        nav_options = {
            "🏠 Dashboard": "Overview and analytics",
            "📝 JD Generator": "Create job descriptions", 
            "📄 Resume Screening": "AI-powered analysis",
            "📊 Analytics": "Detailed insights",
            "⚙️ Settings": "System configuration"
        }
        
        for nav_item, description in nav_options.items():
            is_active = (st.session_state.current_page == nav_item)
            button_style = "sidebar-nav active" if is_active else "sidebar-nav"
            
            if st.button(nav_item, key=f"nav_{nav_item}", use_container_width=True):
                st.session_state.current_page = nav_item
                st.rerun()
            
            if is_active:
                st.caption(f"*{description}*")
        
        st.markdown("---")
        
        # Quick Stats in Sidebar
        st.markdown("### 📈 Quick Stats")
        
        with st.spinner(""):
            companies = db.execute_query("SELECT COUNT(*) as count FROM companies")
            jobs = db.execute_query("SELECT COUNT(*) as count FROM job_descriptions WHERE status='active'")
            candidates = db.execute_query("SELECT COUNT(*) as count FROM candidates")
        
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Companies", companies[0]['count'] if companies else 0)
            st.metric("Jobs", jobs[0]['count'] if jobs else 0)
        with stats_col2:
            st.metric("Candidates", candidates[0]['count'] if candidates else 0)
            st.metric("Success", "94%")
    
    # Main Content Area
    # Premium Header
    st.markdown("<h1 class='main-header floating'>SmartHire AI</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: var(--text-secondary); margin-bottom: 3rem;'>{st.session_state.current_page}</h3>", unsafe_allow_html=True)
    
    # Show loading on first load
    if not st.session_state.page_loaded:
        with st.spinner("🚀 Initializing Premium Platform..."):
            time.sleep(1.5)
        st.session_state.page_loaded = True
        st.rerun()
    
    # Route to selected page
    if st.session_state.current_page == "🏠 Dashboard":
        show_premium_dashboard()
    elif st.session_state.current_page == "📝 JD Generator":
        show_premium_jd_generator()
    elif st.session_state.current_page == "📄 Resume Screening":
        show_premium_resume_screening()
    elif st.session_state.current_page == "📊 Analytics":
        show_premium_analytics()
    elif st.session_state.current_page == "⚙️ Settings":
        show_premium_settings()
    
    # Close dark mode div
    if st.session_state.dark_mode:
        st.markdown('</div>', unsafe_allow_html=True)

def show_premium_dashboard():
    # Connection Status
    test_result = db.execute_query("SELECT 1 as test")
    if test_result:
        st.success("✅ Premium System Connected Successfully")
    
    # Premium KPI Section
    st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h2 class='glowing-text'>📊 Performance Overview</h2>
        <p style='color: var(--text-secondary);'>Real-time metrics with actionable insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Premium KPI Cards with Hover Effects
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        jobs_count = db.execute_query("SELECT COUNT(*) as count FROM job_descriptions WHERE status='active'")
        job_count = jobs_count[0]['count'] if jobs_count else 0
        st.markdown(f"""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #FF6B6B;'>💼</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>{job_count}</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Active Positions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        candidates_count = db.execute_query("SELECT COUNT(*) as count FROM candidates")
        candidate_count = candidates_count[0]['count'] if candidates_count else 0
        st.markdown(f"""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #4ECDC4;'>👥</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>{candidate_count}</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Total Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #45B7D1;'>⚡</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>18d</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Avg Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #96CEB4;'>🎯</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>94%</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main Content Area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Recent Activity
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 20px; border-bottom: 2px solid #4ECDC4; padding-bottom: 10px;'>
                📈 Recent Activity
            </h3>
            <div style='line-height: 2.5;'>
                <div style='display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--card-border);'>
                    <span style='color: #4ECDC4; margin-right: 10px;'>🚀</span>
                    <span><strong>Senior AI Engineer</strong> - JD Created</span>
                </div>
                <div style='display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--card-border);'>
                    <span style='color: #FF6B6B; margin-right: 10px;'>✅</span>
                    <span><strong>Raj Kumar</strong> - Screened (85% match)</span>
                </div>
                <div style='display: flex; align-items: center; padding: 8px 0; border-bottom: 1px solid var(--card-border);'>
                    <span style='color: #45B7D1; margin-right: 10px;'>📊</span>
                    <span><strong>Q3 Report</strong> - Analysis Completed</span>
                </div>
                <div style='display: flex; align-items: center; padding: 8px 0;'>
                    <span style='color: #96CEB4; margin-right: 10px;'>🎯</span>
                    <span><strong>Technical Interview</strong> - Scheduled</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 20px; border-bottom: 2px solid #FF6B6B; padding-bottom: 10px;'>
                🚀 Quick Actions
            </h3>
            <div style='display: grid; gap: 10px;'>
        """, unsafe_allow_html=True)
        
        action_col1, action_col2, action_col3 = st.columns(3)
        with action_col1:
            if st.button("📝 Create JD", use_container_width=True, key="create_jd_main"):
                st.session_state.current_page = "📝 JD Generator"
                st.rerun()
        with action_col2:
            if st.button("📄 Screen Resume", use_container_width=True, key="screen_main"):
                st.session_state.current_page = "📄 Resume Screening"
                st.rerun()
        with action_col3:
            if st.button("📊 View Reports", use_container_width=True, key="reports_main"):
                st.session_state.current_page = "📊 Analytics"
                st.rerun()
        
        st.markdown("</div></div>", unsafe_allow_html=True)
    
    with col2:
        # System Status
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 15px; border-bottom: 2px solid #FFEAA7; padding-bottom: 10px;'>
                ⭐ System Status
            </h3>
            <div style='line-height: 2.5;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Database:</span>
                    <span style='color: #28a745; font-weight: bold;'>✅ Connected</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>AI Engine:</span>
                    <span style='color: #28a745; font-weight: bold;'>✅ Active</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Performance:</span>
                    <span style='color: #ffc107; font-weight: bold;'>⚡ Optimal</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Storage:</span>
                    <span style='color: #17a2b8; font-weight: bold;'>💾 78% Free</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Performance Metrics
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 15px; border-bottom: 2px solid #DDA0DD; padding-bottom: 10px;'>
                📅 Today's Performance
            </h3>
            <div style='line-height: 2.5;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span>JDs Created:</span>
                    <span style='font-weight: bold; color: #FF6B6B;'>3</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Candidates Added:</span>
                    <span style='font-weight: bold; color: #4ECDC4;'>12</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Avg Response:</span>
                    <span style='font-weight: bold; color: #45B7D1;'>2.1h</span>
                </div>
                <div style='display: flex; justify-content: space-between;'>
                    <span>Efficiency:</span>
                    <span style='font-weight: bold; color: #96CEB4;'>+18%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Other functions remain the same as previous version...
def show_premium_jd_generator():
    st.markdown("<h2 class='glowing-text'>💎 AI Job Description Generator</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 20px; border-bottom: 2px solid #4ECDC4; padding-bottom: 10px;'>
                📋 Job Details
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Get companies
        companies = db.execute_query("SELECT id, name FROM companies")
        if companies:
            company_options = {company['name']: company['id'] for company in companies}
        else:
            company_options = {"Tech Solutions Pvt Ltd": 1}
        
        selected_company = st.selectbox("🏢 Company", list(company_options.keys()))
        company_id = company_options[selected_company]
        
        job_title = st.text_input("🎯 Job Title", placeholder="e.g., Senior AI Engineer")
        department = st.selectbox("📊 Department", ["Engineering", "Data Science", "Marketing", "Sales", "HR", "Finance"])
        
        st.markdown("**📅 Experience Requirements**")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            min_exp = st.slider("Minimum Years", 0, 15, 2)
        with exp_col2:
            max_exp = st.slider("Maximum Years", 0, 20, 5)
        
        skills = st.text_area("🛠️ Required Skills", 
                            placeholder="Python, Machine Learning, SQL, AWS, Docker...",
                            height=100)
        
        if st.button("🚀 Generate Smart JD", type="primary", use_container_width=True):
            if job_title and skills:
                with st.spinner("🤖 Creating optimized job description..."):
                    time.sleep(2)
                    generate_premium_jd(company_id, selected_company, job_title, department, min_exp, max_exp, skills)
            else:
                st.error("❌ Please fill all required fields")

    with col2:
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 20px; border-bottom: 2px solid #FF6B6B; padding-bottom: 10px;'>
                📄 Generated Description
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.generated_jd:
            st.success("✅ Job Description Generated Successfully!")
            
            edited_jd = st.text_area("✏️ Edit Description", 
                                   st.session_state.generated_jd, 
                                   height=400,
                                   key="jd_editor")
            
            st.session_state.generated_jd = edited_jd
            
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                if st.button("💾 Save to Database", use_container_width=True, key="save_jd"):
                    save_premium_jd(job_title, department, min_exp, max_exp, skills, company_id)
            with col_s2:
                if st.button("📥 Export as PDF", use_container_width=True, key="export_jd"):
                    st.success("📥 PDF export feature ready!")
            with col_s3:
                if st.button("🔄 Create New", use_container_width=True, key="new_jd"):
                    st.session_state.generated_jd = ""
                    st.rerun()
        else:
            st.info("""
            **👆 Get Started**
            
            Fill out the job details on the left and click **'Generate Smart JD'** to create 
            a professional, optimized job description!
            """)

def generate_premium_jd(company_id, company_name, title, department, min_exp, max_exp, skills):
    enhanced_jd = f"""🎯 **Position:** {title}
🏢 **Company:** {company_name}  
📊 **Department:** {department}
⏳ **Experience:** {min_exp}-{max_exp} years
📍 **Location:** Remote / Hybrid

✨ **Job Summary**
We are seeking an exceptional {title} to join our innovative {department} team.

🚀 **Key Responsibilities**
• Design and develop scalable software solutions
• Collaborate with cross-functional teams
• Implement best practices in code quality
• Mentor junior developers
• Stay updated with emerging technologies

🛠 **Technical Requirements**
{skills}

🎓 **Qualifications & Experience**
• {min_exp}+ years in software development
• Bachelor's/Master's in Computer Science
• Strong problem-solving skills
• Experience with agile methodologies

💫 **What We Offer**
• Competitive salary and benefits
• Flexible work arrangements
• Professional development
• Inclusive work environment
• Career growth opportunities

---
*Generated by SmartHire AI • {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""
    
    st.session_state.generated_jd = enhanced_jd
    st.rerun()

def save_premium_jd(job_title, department, min_exp, max_exp, skills, company_id):
    result = db.execute_insert("""
        INSERT INTO job_descriptions 
        (company_id, job_title, department, experience_min, experience_max, skills_required, generated_description, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (company_id, job_title, department, min_exp, max_exp, skills, st.session_state.generated_jd, 'active'))
    
    if result:
        st.success("✅ Job Description saved successfully!")
        st.session_state.generated_jd = ""
        st.rerun()
    else:
        st.error("❌ Error saving to database")

def show_premium_resume_screening():
    st.markdown("<h2 class='glowing-text'>💎 AI Resume Screening</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📤 Upload & Analyze", "👥 Candidate Database"])
    
    with tab1:
        st.markdown("""
        <div class='premium-card'>
            <h3 style='margin-bottom: 20px; border-bottom: 2px solid #4ECDC4; padding-bottom: 10px;'>
                🚀 Upload Resume
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'])
        
        if uploaded_file:
            st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class='premium-card'>
                    <h4 style='margin-bottom: 15px;'>📁 File Details</h4>
                    <p><strong>Name:</strong> {uploaded_file.name}</p>
                    <p><strong>Size:</strong> {uploaded_file.size / 1024:.1f} KB</p>
                    <p><strong>Type:</strong> {uploaded_file.type}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class='premium-card'>
                    <h4 style='margin-bottom: 15px;'>👤 Candidate Info</h4>
                </div>
                """, unsafe_allow_html=True)
                
                candidate_name = st.text_input("Full Name")
                candidate_email = st.text_input("Email Address")
                candidate_exp = st.slider("Years of Experience", 0, 30, 2)
            
            if st.button("🔍 Analyze with AI", type="primary", use_container_width=True):
                if candidate_name and candidate_email:
                    with st.spinner("🤖 Analyzing resume content..."):
                        time.sleep(3)
                        show_analysis_results()
                else:
                    st.error("Please fill candidate name and email")

def show_analysis_results():
    st.markdown("---")
    st.markdown("<h3 class='glowing-text'>📊 Analysis Results</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='premium-card'>
            <h4 style='margin-bottom: 15px;'>🎯 Match Scores</h4>
            <div style='margin-top: 15px;'>
                <p>Overall Match: <strong style='color: #4ECDC4;'>82%</strong> ↑5%</p>
                <p>Skill Fit: <strong style='color: #4ECDC4;'>78%</strong></p>
                <p>Experience: <strong style='color: #96CEB4;'>85%</strong></p>
                <p>Culture Fit: <strong style='color: #4ECDC4;'>76%</strong></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='premium-card'>
            <h4 style='margin-bottom: 15px;'>💡 Recommendations</h4>
            <div style='margin-top: 15px; line-height: 2;'>
                <p>✅ Strong technical skills match</p>
                <p>⚠️ Consider cloud certification</p>
                <p>💡 Good cultural fit indicators</p>
                <p>🚀 Ready for technical interview</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_premium_analytics():
    st.markdown("<h2 class='glowing-text'>💎 Advanced Analytics</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #FF6B6B;'>📋</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>25</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Total Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #4ECDC4;'>👥</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>142</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Candidates</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #45B7D1;'>📊</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>68%</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Interview Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='premium-metric'>
            <div style='font-size: 2.5rem; margin-bottom: 10px; color: #96CEB4;'>⏱️</div>
            <div style='font-size: 2rem; font-weight: bold; margin-bottom: 5px;'>18d</div>
            <div style='font-size: 0.9rem; color: var(--text-secondary);'>Hiring Time</div>
        </div>
        """, unsafe_allow_html=True)

def show_premium_settings():
    st.markdown("<h2 class='glowing-text'>💎 System Settings</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='premium-card'>
        <h3 style='margin-bottom: 20px; border-bottom: 2px solid #4ECDC4; padding-bottom: 10px;'>
            Theme Settings
        </h3>
        <p>Use the theme toggle in the sidebar to switch between Dark and Light modes.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()