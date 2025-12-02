# database.py - NEW VERSION
import mysql.connector
from mysql.connector import Error
import streamlit as st

class Database:
    def __init__(self):
        self.connection = None
    
    def get_connection(self):
        if self.connection is None or not self.connection.is_connected():
            try:
                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="pass123",
                    database="smarthire_ai",
                    auth_plugin='mysql_native_password'
                )
                st.success("✅ Database connected successfully!")
            except Error as e:
                st.error(f"❌ Database connection failed: {e}")
                return None
        return self.connection
    
    def execute_query(self, query, params=None):
        conn = self.get_connection()
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
            # Don't close connection here - keep it open
    
    def execute_insert(self, query, params=None):
        conn = self.get_connection()
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

# Create a single instance
db = Database()