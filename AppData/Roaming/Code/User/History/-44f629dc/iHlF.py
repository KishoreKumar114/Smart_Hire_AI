# email_config.py - FIXED VERSION
"""
SMTP Email Configuration for SmartHire AI
Make sure to use App Password for Gmail
"""

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "kishorekumarr2k4@gmail.com"

# ⚠️ IMPORTANT: Use App Password, NOT your regular Gmail password
# Generate App Password from: Google Account → Security → App passwords
SENDER_PASSWORD = "cmygqxibirjsxjzn"  # Your 16-character App Password

def get_email_config():
    """Get email configuration"""
    return {
        'smtp_server': SMTP_SERVER,
        'smtp_port': SMTP_PORT,
        'sender_email': SENDER_EMAIL,
        'sender_password': SENDER_PASSWORD
    }

def validate_email_config():
    """Validate email configuration"""
    config = get_email_config()
    if not config['sender_email'] or not config['sender_password']:
        return False, "Email configuration incomplete"
    return True, "Email configuration ready"