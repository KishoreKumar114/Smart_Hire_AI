# ui_animations.py - ENHANCED INTERACTIVE VERSION
import streamlit as st
import time
import random
import json

class PremiumAnimations:
    def __init__(self):
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']
        self.icons = ['🚀', '💎', '⭐', '🔥', '✨', '🎯', '⚡', '💫', '🌟']
    
    def premium_loading(self, text="Processing", subtext=None):
        """Enhanced loading animation with progress bar and floating elements"""
        placeholder = st.empty()
        
        # Create a progress bar
        progress_bar = st.progress(0)
        
        # Advanced loading animation
        for i in range(1, 101):
            percent = i
            color = self.colors[i % len(self.colors)]
            icon = self.icons[i % len(self.icons)]
            
            # Update progress bar
            progress_bar.progress(percent)
            
            # Dynamic loading content
            placeholder.markdown(f"""
            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 3rem; margin-bottom: 15px; animation: bounce 2s infinite;">
                    {icon}
                </div>
                <h3 style="color: var(--text-primary); font-weight: 600; margin-bottom: 10px;">
                    {text}
                </h3>
                {f'<p style="color: var(--text-secondary); font-size: 0.9rem;">{subtext}</p>' if subtext else ''}
                <div style="display: inline-block; padding: 8px 16px; background: {color}20; 
                         border-radius: 20px; margin-top: 15px; border: 1px solid {color}40;">
                    <span style="color: {color}; font-weight: bold;">{percent}%</span>
                </div>
            </div>
            
            <style>
            @keyframes bounce {{
                0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                40% {{ transform: translateY(-10px); }}
                60% {{ transform: translateY(-5px); }}
            }}
            </style>
            """, unsafe_allow_html=True)
            
            time.sleep(0.03 + random.random() * 0.02)  # Variable speed
        
        placeholder.empty()
        progress_bar.empty()
    
    def interactive_success(self, message, submessage=None, duration=3):
        """Interactive success message with confetti effect"""
        success_container = st.empty()
        
        # Success animation with confetti
        success_container.markdown(f"""
        <div id="successAnimation" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            margin: 20px 0;
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
            border: 2px solid rgba(255,255,255,0.3);
            position: relative;
            overflow: hidden;
            animation: successPop 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        ">
            <div style="font-size: 4rem; margin-bottom: 15px; animation: iconBounce 0.8s ease-in-out;">
                ✅
            </div>
            <h3 style="margin: 0 0 10px 0; font-size: 1.5rem;">{message}</h3>
            {f'<p style="margin: 0; opacity: 0.9; font-size: 1rem;">{submessage}</p>' if submessage else ''}
        </div>
        
        <!-- Confetti Container -->
        <div id="confettiContainer" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;"></div>
        
        <style>
        @keyframes successPop {{
            0% {{ transform: scale(0.5); opacity: 0; }}
            70% {{ transform: scale(1.1); }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        @keyframes iconBounce {{
            0%, 20%, 50%, 80%, 100% {{ transform: translateY(0) scale(1); }}
            40% {{ transform: translateY(-10px) scale(1.1); }}
            60% {{ transform: translateY(-5px) scale(1.05); }}
        }}
        </style>
        
        <script>
        // Confetti animation
        function createConfetti() {{
            const container = document.getElementById('confettiContainer');
            const colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'];
            
            for (let i = 0; i < 50; i++) {{
                const confetti = document.createElement('div');
                confetti.style.position = 'absolute';
                confetti.style.width = '10px';
                confetti.style.height = '10px';
                confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
                confetti.style.borderRadius = '50%';
                confetti.style.top = '0';
                confetti.style.left = Math.random() * 100 + 'vw';
                confetti.style.opacity = '0.8';
                confetti.style.animation = `confettiFall ${{1 + Math.random() * 2}}s ease-in forwards`;
                
                container.appendChild(confetti);
                
                // Remove confetti after animation
                setTimeout(() => confetti.remove(), 3000);
            }}
        }}
        
        // Confetti falling animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes confettiFall {{
                0% {{ 
                    transform: translateY(0) rotate(0deg); 
                    opacity: 1;
                }}
                100% {{ 
                    transform: translateY(100vh) rotate(360deg); 
                    opacity: 0;
                }}
            }}
        `;
        document.head.append(style);
        
        // Trigger confetti
        createConfetti();
        </script>
        """, unsafe_allow_html=True)
        
        # Auto-remove after duration
        time.sleep(duration)
        success_container.empty()
    
    def floating_metrics_interactive(self, icon, value, title, color="#FF6B6B", tooltip=None):
        """Interactive floating metrics with hover effects"""
        tooltip_html = f'data-tooltip="{tooltip}"' if tooltip else ""
        
        return f"""
        <div {tooltip_html} style="
            background: linear-gradient(135deg, var(--card-bg), var(--bg-secondary));
            color: var(--text-primary);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            margin: 10px;
            border: 1px solid {color}40;
            box-shadow: 
                0 5px 15px rgba(0,0,0,0.1),
                0 0 0 0px {color}00;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        "
        onmouseover="this.style.transform='translateY(-8px) scale(1.02)'; this.style.boxShadow='0 15px 30px rgba(0,0,0,0.15), 0 0 0 3px {color}40'; this.style.borderColor='{color}80';"
        onmouseout="this.style.transform='translateY(0) scale(1)'; this.style.boxShadow='0 5px 15px rgba(0,0,0,0.1), 0 0 0 0px {color}00'; this.style.borderColor='{color}40';"
        onclick="this.style.animation='pulse 0.5s ease-in-out'; setTimeout(() => this.style.animation='', 500);"
        >
            <!-- Animated background gradient -->
            <div style="
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, {color}15, transparent);
                transition: left 0.6s ease;
            "></div>
            
            <!-- Main content -->
            <div style="position: relative; z-index: 2;">
                <div style="font-size: 2.5rem; margin-bottom: 10px; color: {color}; 
                         animation: floatIcon 3s ease-in-out infinite;">{icon}</div>
                <div style="font-size: 2rem; font-weight: bold; margin-bottom: 5px; 
                         background: linear-gradient(45deg, {color}, var(--accent-secondary));
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {value}
                </div>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">{title}</div>
            </div>
        </div>
        
        <style>
        @keyframes floatIcon {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-5px); }}
        }}
        
        @keyframes pulse {{
            0% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
            100% {{ transform: scale(1); }}
        }}
        
        /* Tooltip styling */
        [data-tooltip] {{
            position: relative;
        }}
        
        [data-tooltip]:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            white-space: nowrap;
            z-index: 1000;
            margin-bottom: 5px;
        }}
        </style>
        """
    
    def interactive_card(self, title, content, glow_color="#4ECDC4", expandable=False, expanded_content=None):
        """Interactive card with expandable content"""
        expand_id = f"expand_{random.randint(1000,9999)}"
        
        expand_script = ""
        expand_button = ""
        
        if expandable and expanded_content:
            expand_script = f"""
            <script>
            function toggleExpand{expand_id}() {{
                const content = document.getElementById('expandedContent{expand_id}');
                const button = document.getElementById('expandBtn{expand_id}');
                if (content.style.display === 'none') {{
                    content.style.display = 'block';
                    button.innerHTML = '▲ Collapse';
                    button.style.background = '{glow_color}40';
                }} else {{
                    content.style.display = 'none';
                    button.innerHTML = '▼ Expand';
                    button.style.background = 'transparent';
                }}
            }}
            </script>
            """
            
            expand_button = f"""
            <div style="text-align: center; margin-top: 15px;">
                <button id="expandBtn{expand_id}" onclick="toggleExpand{expand_id}()" 
                style="background: transparent; border: 1px solid {glow_color}60; color: {glow_color}; 
                       padding: 5px 15px; border-radius: 15px; cursor: pointer; transition: all 0.3s ease;">
                ▼ Expand
                </button>
            </div>
            
            <div id="expandedContent{expand_id}" style="display: none; margin-top: 15px; padding-top: 15px; 
                 border-top: 1px solid {glow_color}20; animation: fadeIn 0.5s ease-in-out;">
                {expanded_content}
            </div>
            """
        
        return f"""
        <div style="
            background: var(--card-bg);
            color: var(--text-primary);
            padding: 25px;
            border-radius: 20px;
            margin: 15px 0;
            border: 1px solid {glow_color}30;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        "
        onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 15px 35px rgba(0,0,0,0.15), 0 0 20px {glow_color}20';"
        onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.1)';"
        >
            <!-- Animated border -->
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, {glow_color}, {glow_color}80, {glow_color});
                background-size: 200% 100%;
                animation: shimmerBorder 3s ease-in-out infinite;
            "></div>
            
            <h3 style="margin-bottom: 15px; color: {glow_color}; border-bottom: 2px solid {glow_color}30; 
                    padding-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                <span style="font-size: 1.5rem;">{title.split(' ')[0]}</span>
                <span>{' '.join(title.split(' ')[1:])}</span>
            </h3>
            
            <div style="line-height: 1.6;">
                {content}
            </div>
            
            {expand_button}
        </div>
        
        {expand_script}
        
        <style>
        @keyframes shimmerBorder {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        """
    
    def progress_tracker(self, steps, current_step, title="Progress"):
        """Interactive progress tracker"""
        steps_html = ""
        for i, step in enumerate(steps):
            is_active = i == current_step
            is_completed = i < current_step
            status_icon = "✅" if is_completed else "🟢" if is_active else "⚪"
            
            steps_html += f"""
            <div style="display: flex; align-items: center; margin: 15px 0; padding: 10px; 
                     background: {'var(--accent-secondary)20' if is_active else 'transparent'}; 
                     border-radius: 10px; border-left: 3px solid {'var(--accent-secondary)' if is_active else 'transparent'};">
                <div style="font-size: 1.2rem; margin-right: 15px; min-width: 30px;">{status_icon}</div>
                <div style="flex-grow: 1;">
                    <div style="font-weight: {'bold' if is_active or is_completed else 'normal'}; 
                             color: {'var(--accent-secondary)' if is_active else 'var(--text-primary)'};">
                        {step}
                    </div>
                </div>
            </div>
            """
        
        return self.interactive_card(
            title,
            f"""
            <div style="position: relative;">
                <!-- Progress line -->
                <div style="position: absolute; left: 21px; top: 0; bottom: 0; width: 2px; 
                         background: linear-gradient(to bottom, var(--accent-secondary), var(--accent-primary)); 
                         z-index: 1;"></div>
                <div style="position: relative; z-index: 2;">
                    {steps_html}
                </div>
            </div>
            """,
            glow_color="#4ECDC4"
        )
    
    def typewriter_effect(self, text, speed=50, container=None):
        """Typewriter animation effect"""
        if container is None:
            container = st.empty()
        
        displayed_text = ""
        for char in text:
            displayed_text += char
            container.markdown(f"""
            <div style="
                background: var(--bg-secondary);
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid var(--accent-primary);
                font-family: 'Courier New', monospace;
                line-height: 1.6;
            ">
                {displayed_text}<span style="animation: blink 1s infinite;">|</span>
            </div>
            
            <style>
            @keyframes blink {{
                0%, 50% {{ opacity: 1; }}
                51%, 100% {{ opacity: 0; }}
            }}
            </style>
            """, unsafe_allow_html=True)
            time.sleep(speed / 1000)
        
        # Remove cursor after completion
        container.markdown(f"""
        <div style="
            background: var(--bg-secondary);
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid var(--accent-primary);
            font-family: 'Courier New', monospace;
            line-height: 1.6;
        ">
            {displayed_text}
        </div>
        """, unsafe_allow_html=True)
    
    def countup_animation(self, start_value, end_value, duration=2000, prefix="", suffix=""):
        """Animated counting up effect"""
        container = st.empty()
        
        steps = 60  # Number of animation steps
        step_duration = duration / steps
        increment = (end_value - start_value) / steps
        
        current_value = start_value
        for i in range(steps + 1):
            if i == steps:  # Ensure we end exactly at the target value
                current_value = end_value
            
            # Format number with commas
            formatted_value = f"{int(current_value):,}" if isinstance(end_value, int) else f"{current_value:.1f}"
            
            container.markdown(f"""
            <div style="
                text-align: center;
                font-size: 2.5rem;
                font-weight: bold;
                background: linear-gradient(45deg, var(--accent-primary), var(--accent-secondary));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                padding: 10px;
                animation: pulseCount 0.5s ease-in-out;
            ">
                {prefix}{formatted_value}{suffix}
            </div>
            
            <style>
            @keyframes pulseCount {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            </style>
            """, unsafe_allow_html=True)
            
            current_value += increment
            time.sleep(step_duration / 1000)
        
        return container

# Create global instance
premium_anim = PremiumAnimations()