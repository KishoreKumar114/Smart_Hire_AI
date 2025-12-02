# database.py - FIXED VERSION
import mysql.connector
from mysql.connector import Error
import streamlit as st

@st.cache_resource
def init_connection():
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
        st.error(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None):
    conn = init_connection()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            conn.commit()
            return result
        except Error as e:
            st.error(f"Query error: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()
    return None

def execute_insert(query, params=None):
    conn = init_connection()
    if conn:
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
            conn.close()
    return None