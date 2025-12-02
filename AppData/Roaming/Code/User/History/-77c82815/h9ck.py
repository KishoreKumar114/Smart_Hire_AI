# ui_animations.py
import streamlit as st
import time
import json
from typing import Any

class UIAnimations:
    def __init__(self):
        self.loading_dots = 0
        
    def loading_spinner(self, text="Processing", dots=3):
        """Animated loading dots"""
        dot_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        placeholder = st.empty()
        
        for i in range(len(dot_chars) * dots):
            frame = i % len(dot_chars)
            placeholder.markdown(f"<div style='text-align: center; padding: 20px;'>"
                               f"<h3 style='color: #1f77b4;'>{dot_chars[frame]} {text}</h3>"
                               f"</div>", unsafe_allow_html=True)
            time.sleep(0.1)
        
        placeholder.empty()
    
    def typewriter_effect(self, text, speed=0.03):
        """Typewriter animation for text"""
        placeholder = st.empty()
        typed_text = ""
        
        for char in text:
            typed_text += char
            placeholder.markdown(f"<div style='font-family: monospace; background: #f0f2f6; "
                               f"padding: 10px; border-radius: 5px; border-left: 4px solid #ff4b4b;'>"
                               f"{typed_text}</div>", unsafe_allow_html=True)
            time.sleep(speed)
    
    def fade_in_element(self, element_func, delay=0.5):
        """Fade in animation for any element"""
        with st.spinner(""):
            time.sleep(delay)
            element_func()
    
    def success_animation(self, message):
        """Success message with animation"""
        st.balloons()
        st.success(f"🎉 {message}")
    
    def progress_bar_with_percentage(self, steps, descriptions):
        """Animated progress bar with steps"""
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, (step, desc) in enumerate(zip(steps, descriptions)):
            progress = (i + 1) / len(steps)
            progress_bar.progress(progress)
            status_text.text(f"{desc}... {int(progress * 100)}%")
            time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
    
    def pulse_animation(self, element, duration=2):
        """Pulse animation for important elements"""
        st.markdown(f"""
        <style>
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        .pulse {{
            animation: pulse {duration}s infinite;
        }}
        </style>
        <div class="pulse">
            {element}
        </div>
        """, unsafe_allow_html=True)

# Create global instance
animations = UIAnimations()