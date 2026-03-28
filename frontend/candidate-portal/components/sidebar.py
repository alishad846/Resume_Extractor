"""Sidebar component for Streamlit app."""

import streamlit as st


def render_sidebar():
    """Render sidebar with user info and settings."""
    
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h3 style='color: #1f77b4;'>Welcome to Resume AI</h3>
            <p style='font-size: 0.9em; color: #666;'>
                Your personal career assistant powered by AI
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User section
        st.markdown("### 👤 User")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", key="login_btn", use_container_width=True):
                if email and password:
                    st.success("✅ Logged in successfully!")
                    st.session_state.user = {"name": email.split("@")[0]}
                else:
                    st.error("❌ Please enter email and password")
        
        with tab2:
            reg_email = st.text_input("Email", key="reg_email")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_password = st.text_input("Password", type="password", key="reg_pass")
            
            if st.button("Register", key="reg_btn", use_container_width=True):
                if reg_email and reg_name and reg_password:
                    st.success("✅ Account created! Please login.")
                else:
                    st.error("❌ Please fill all fields")
        
        if st.session_state.user:
            if st.button("Logout", key="logout_btn", use_container_width=True):
                st.session_state.user = None
                st.rerun()
        
        st.markdown("---")
        
        # Info section
        st.markdown("### ℹ️ About")
        st.info("""
        **Resume AI Platform** helps you:
        - Upload & analyze resumes
        - Get AI-powered feedback
        - Improve your resume score
        - Find ideal career paths
        - Match with job descriptions
        """)
        
        st.markdown("---")
        
        # Settings
        st.markdown("### ⚙️ Settings")
        theme = st.radio("Theme", ["Light", "Dark"])
        notifications = st.checkbox("Enable notifications")
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style='text-align: center; padding: 20px 0; color: #999; font-size: 0.85em;'>
            <p>Resume AI Platform v1.0</p>
            <p>📧 support@resumeai.com</p>
            <p>🔗 <a href='#'>Documentation</a> | <a href='#'>Contact</a></p>
        </div>
        """, unsafe_allow_html=True)
