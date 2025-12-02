# ui_animations.py - PREMIUM VERSION
import streamlit as st
import time
import random

class PremiumAnimations:
    def __init__(self):
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
    
    def premium_loading(self, text="Processing"):
        """Premium loading animation with floating dots"""
        placeholder = st.empty()
        dots = ["●○○", "○●○", "○○●", "○●○"]
        
        for i in range(12):
            color = random.choice(self.colors)
            placeholder.markdown(f"""
            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 2rem; color: {color}; margin-bottom: 10px;">
                    {dots[i % 4]}
                </div>
                <h3 style="color: #2c3e50; font-weight: 300;">{text}</h3>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.2)
        placeholder.empty()
    
    def glowing_success(self, message):
        """Glowing success effect instead of balloons"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            border: 2px solid rgba(255,255,255,0.2);
            animation: glow 2s ease-in-out infinite alternate;
        ">
            <h3 style="margin: 0;">✨ {message} ✨</h3>
        </div>
        <style>
        @keyframes glow {{
            from {{
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            }}
            to {{
                box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
            }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def dark_glow_effect(self, content, color="#FF6B6B"):
        """Dark glowing effect for premium elements"""
        return f"""
        <div style="
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 25px;
            border-radius: 20px;
            margin: 15px 0;
            border: 1px solid {color};
            box-shadow: 
                0 0 20px {color}40,
                0 0 40px {color}20,
                inset 0 0 20px {color}10;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, {color}20 0%, transparent 70%);
                animation: rotate 10s linear infinite;
            "></div>
            <div style="position: relative; z-index: 2;">
                {content}
            </div>
        </div>
        <style>
        @keyframes rotate {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        </style>
        """
    
    def floating_metrics(self, icon, value, title, color="#FF6B6B"):
        """Floating metrics with glow effect"""
        return f"""
        <div style="
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            margin: 10px;
            border: 1px solid {color};
            box-shadow: 
                0 10px 30px {color}40,
                0 0 50px {color}20;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        "
        onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 20px 40px {color}60, 0 0 60px {color}30';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 10px 30px {color}40, 0 0 50px {color}20';"
        >
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, {color}, transparent);
                animation: slide 3s linear infinite;
            "></div>
            
            <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
            <div style="font-size: 2rem; font-weight: bold; margin-bottom: 5px;">{value}</div>
            <div style="font-size: 0.9rem; opacity: 0.9;">{title}</div>
        </div>
        
        <style>
        @keyframes slide {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        </style>
        """
    
    def premium_card(self, content, glow_color="#4ECDC4"):
        """Premium card with glowing border"""
        return f"""
        <div style="
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
            color: white;
            padding: 25px;
            border-radius: 20px;
            margin: 15px 0;
            border: 1px solid {glow_color};
            box-shadow: 
                0 0 30px {glow_color}30,
                0 0 60px {glow_color}15;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: -10px;
                left: -10px;
                right: -10px;
                bottom: -10px;
                background: linear-gradient(45deg, transparent, {glow_color}10, transparent);
                animation: shimmer 3s ease-in-out infinite;
            "></div>
            <div style="position: relative; z-index: 2;">
                {content}
            </div>
        </div>
        
        <style>
        @keyframes shimmer {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 0.7; }}
        }}
        </style>
        """

# Create global instance
premium_anim = PremiumAnimations()