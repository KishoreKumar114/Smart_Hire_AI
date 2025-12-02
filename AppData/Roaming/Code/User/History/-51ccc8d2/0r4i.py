# database.py - SIMPLE FIXED VERSION
import mysql.connector
from mysql.connector import Error
import streamlit as st

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
        st.error(f"Query error: {e}")
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
        return None
    
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        st.error(f"Insert error: {e}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()