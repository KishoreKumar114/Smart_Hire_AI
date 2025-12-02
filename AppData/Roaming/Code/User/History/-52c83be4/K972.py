def load_login_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: #111 !important;
        margin: 0 !important;
        padding: 0 !important;
        font-family: 'Quicksand', sans-serif !important;
    }
    
    .main-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: #111;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .ring {
        position: relative;
        width: 500px;
        height: 500px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .ring i {
        position: absolute;
        inset: 0;
        border: 2px solid #fff;
        transition: 0.5s;
    }
    
    .ring i:nth-child(1) {
        border-radius: 38% 62% 63% 37% / 41% 44% 56% 59%;
        animation: animate 6s linear infinite;
    }
    
    .ring i:nth-child(2) {
        border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
        animation: animate 4s linear infinite;
    }
    
    .ring i:nth-child(3) {
        border-radius: 41% 44% 56% 59%/38% 62% 63% 37%;
        animation: animate2 10s linear infinite;
    }
    
    .ring:hover i {
        border: 6px solid var(--clr);
        filter: drop-shadow(0 0 20px var(--clr));
    }
    
    @keyframes animate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes animate2 {
        0% { transform: rotate(360deg); }
        100% { transform: rotate(0deg); }
    }
    
    .login-form {
        position: absolute;
        width: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        gap: 20px;
        z-index: 1000;
        background: rgba(0, 0, 0, 0.8);
        padding: 40px 30px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    
    .login-form h2 {
        font-size: 2em;
        color: #fff;
        font-family: 'Quicksand', sans-serif;
    }
    
    .stTextInput input {
        width: 100% !important;
        padding: 12px 20px !important;
        background: transparent !important;
        border: 2px solid #fff !important;
        border-radius: 40px !important;
        font-size: 1.2em !important;
        color: #fff !important;
        font-family: 'Quicksand', sans-serif !important;
    }
    
    .stTextInput input::placeholder {
        color: rgba(255, 255, 255, 0.75) !important;
    }
    
    .stButton button {
        width: 100% !important;
        background: linear-gradient(45deg, #ff357a, #fff172) !important;
        border: none !important;
        border-radius: 40px !important;
        padding: 12px 20px !important;
        font-size: 1.2em !important;
        color: #000 !important;
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 600 !important;
    }
    
    .form-links {
        width: 100%;
        display: flex;
        justify-content: space-between;
        padding: 0 10px;
    }
    
    .form-links a {
        color: #fff;
        text-decoration: none;
        font-family: 'Quicksand', sans-serif;
    }
    </style>
    
    <div class="main-container">
        <div class="ring">
            <i style="--clr:#00ff0a;"></i>
            <i style="--clr:#ff0057;"></i>
            <i style="--clr:#fffd44;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)