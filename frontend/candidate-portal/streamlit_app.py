"""
Resume AI Platform - Candidate Portal
Main application entry point using Streamlit

Features:
- Resume upload and parsing
- AI-powered feedback and suggestions
- Resume scoring and JD matching
- Career insights and recommendations
- Professional dashboard with analytics
"""

import base64
import streamlit as st
from streamlit_option_menu import option_menu
from pathlib import Path
import sys
import os

# Add backend path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

from components.header import render_header
from components.sidebar import render_sidebar
from pages import upload_resume, resume_analysis, ai_feedback, career_insights, home

# Configure Streamlit page
ASSETS_DIR = Path("assets")
ICON_CANDIDATES = [
    ("logo.png", "image/png"),
    ("logo.svg", "image/svg+xml"),
]
PAGE_ICON = "📄"
for icon_name, mime in ICON_CANDIDATES:
    icon_path = ASSETS_DIR / icon_name
    if icon_path.exists():
        encoded = base64.b64encode(icon_path.read_bytes()).decode("utf-8")
        PAGE_ICON = f"data:{mime};base64,{encoded}"
        break

st.set_page_config(
    page_title="Resume AI Platform",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://docs.example.com",
        "Report a bug": "https://github.com/example/issues",
        "About": "Resume AI Platform v1.0 - Powered by Advanced NLP & ML"
    }
)

# Custom CSS for professional look
st.markdown("""
<style>
    * {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stTitle {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 0.5em;
    }
    
    .stHeader {
        color: #2c3e50;
        font-weight: 600;
    }
    
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeeba;
        color: #856404;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .error-box {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 12px;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-weight: 600;
    }
    
    .score-display {
        font-size: 3em;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
    }
    
    .grade-a { color: #28a745; }
    .grade-b { color: #17a2b8; }
    .grade-c { color: #ffc107; }
    .grade-d { color: #fd7e14; }
    .grade-f { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"


def main():
    """Main application entry point."""
    
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Main navigation using option_menu
    with st.sidebar:
        st.markdown("---")
        selected = option_menu(
            menu_title="Navigation",
            options=["🏠 Home", "📤 Upload Resume", "📊 Resume Analysis", 
                    "🤖 AI Feedback", "🎯 Career Insights"],
            icons=["house", "upload", "bar-chart", "robot", "target"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                "icon": {"color": "#1f77b4", "font-size": "20px"},
                "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {
                    "background-color": "#1f77b4",
                    "color": "white",
                    "border-radius": "5px"
                },
            }
        )
    
    # Route to selected page
    if selected == "🏠 Home":
        home.render()
    
    elif selected == "📤 Upload Resume":
        upload_resume.render()
    
    elif selected == "📊 Resume Analysis":
        resume_analysis.render()
    
    elif selected == "🤖 AI Feedback":
        ai_feedback.render()
    
    elif selected == "🎯 Career Insights":
        career_insights.render()


if __name__ == "__main__":
    main()
