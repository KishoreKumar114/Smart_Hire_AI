# email_config.py - FIXED VERSION WITH APP PASSWORD
"""
SMTP Email Configuration for SmartHire AI
Use App Password for Gmail instead of regular password
"""

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "kishorekumarr2k4@gmail.com"  # Your Gmail
# Use App Password instead of regular password
SENDER_PASSWORD = "your_app_password_here"  # Generate from Google Account settings

# Email Settings
EMAIL_SUBJECT_PREFIX = "SmartHire AI - Interview Invitation"

# Company Information
COMPANY_NAME = "SmartHire AI"
HR_EMAIL = "hr@smarthire.com"
HR_PHONE = "+1 (555) 123-4567"

def validate_email_config():
    """Validate if email configuration is set up correctly"""
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        return False, "Email configuration is incomplete"
    if SENDER_PASSWORD == "your_app_password_here":
        return False, "Please update SENDER_PASSWORD with your Gmail App Password"
    return True, "Email configuration is ready"

def get_email_config():
    """Get email configuration"""
    return {
        'smtp_server': SMTP_SERVER,
        'smtp_port': SMTP_PORT,
        'sender_email': SENDER_EMAIL,
        'sender_password': SENDER_PASSWORD
    }