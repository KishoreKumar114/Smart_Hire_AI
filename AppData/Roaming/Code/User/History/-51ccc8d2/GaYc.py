# database.py - FIXED VERSION
import mysql.connector
from mysql.connector import Error
import streamlit as st
import hashlib

def get_connection():
    """Create a new connection for each query"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pass123",
            database="smarthire_ai",
            auth_plugin='mysql_native_password'
        )
        return connection
    except Error as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

def execute_query(query, params=None):
    """Execute SELECT query"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except Error as e:
        st.error(f"❌ Query error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def execute_insert(query, params=None):
    """Execute INSERT/UPDATE query"""
    conn = get_connection()
    if not conn:
        return False
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        st.error(f"❌ Insert error: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, email, password, role="user"):
    """Create new user in database"""
    hashed_password = hash_password(password)
    query = """
    INSERT INTO users (username, email, password_hash, role, created_at)
    VALUES (%s, %s, %s, %s, NOW())
    """
    return execute_insert(query, (username, email, hashed_password, role))

def verify_user(username, password):
    """Verify user credentials"""
    hashed_password = hash_password(password)
    query = "SELECT * FROM users WHERE username = %s AND password_hash = %s"
    result = execute_query(query, (username, hashed_password))
    return result[0] if result else None

def check_username_exists(username):
    """Check if username already exists"""
    query = "SELECT id FROM users WHERE username = %s"
    result = execute_query(query, (username,))
    return result is not None and len(result) > 0

def check_email_exists(email):
    """Check if email already exists"""
    query = "SELECT id FROM users WHERE email = %s"
    result = execute_query(query, (email,))
    return result is not None and len(result) > 0

def get_user_by_username(username):
    """Get user by username"""
    query = "SELECT * FROM users WHERE username = %s"
    result = execute_query(query, (username,))
    return result[0] if result else None

def initialize_database():
    """Initialize database tables if they don't exist"""
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('admin', 'hr', 'recruiter', 'user') DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP NULL,
                is_active BOOLEAN DEFAULT TRUE
            )
            """)
            
            # Insert demo users if they don't exist
            demo_users = [
                ('admin', 'admin@smarthire.ai', 'admin123', 'admin'),
                ('hr', 'hr@smarthire.ai', 'hr123', 'hr'),
                ('recruiter', 'recruiter@smarthire.ai', 'recruiter123', 'recruiter')
            ]
            
            for username, email, password, role in demo_users:
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                if not cursor.fetchone():
                    hashed_password = hash_password(password)
                    cursor.execute(
                        "INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                        (username, email, hashed_password, role)
                    )
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
    except Error as e:
        st.error(f"❌ Database initialization failed: {e}")
        return False