"""Home page component."""

import streamlit as st


def render():
    """Render the home page."""
    
    st.title("🏠 Welcome to Resume AI Platform")
    
    # Hero section
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                 padding: 50px; border-radius: 10px; color: white; text-align: center;
                 margin-bottom: 30px;'>
        <h2>Transform Your Resume with AI</h2>
        <p style='font-size: 1.1em; margin: 20px 0;'>
            Get intelligent feedback, improve your score, and land your dream job
        </p>
        <button style='background: white; color: #667eea; padding: 12px 30px; 
                      border: none; border-radius: 5px; font-weight: bold; cursor: pointer;'>
            Get Started →
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📤 Upload & Parse
        Upload your resume in PDF or DOCX format. Our AI automatically extracts and organizes your information.
        """)
    
    with col2:
        st.markdown("""
        ### 🤖 AI Feedback
        Get detailed AI-generated suggestions to improve your resume structure, content, and formatting.
        """)
    
    with col3:
        st.markdown("""
        ### 📊 Score & Ranking
        See your resume score breakdown across multiple dimensions and compare with job descriptions.
        """)
    
    st.markdown("---")
    
    # Stats section
    st.markdown("## 📈 Platform Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Resumes", "5,234", "+12%")
    
    with col2:
        st.metric("Avg Resume Score", "74.2", "+2.1")
    
    with col3:
        st.metric("Users Placed", "892", "+45")
    
    with col4:
        st.metric("Success Rate", "68.5%", "+3.2%")
    
    st.markdown("---")
    
    # How it works
    st.markdown("## 🎯 How It Works")
    
    steps = [
        ("1️⃣ Upload", "Upload your resume in PDF or DOCX format"),
        ("2️⃣ Analyze", "Our AI analyzes your resume and extracts information"),
        ("3️⃣ Get Feedback", "Receive detailed feedback and improvement suggestions"),
        ("4️⃣ Improve", "Follow recommendations and enhance your resume"),
        ("5️⃣ Match", "Match your resume with job descriptions"),
        ("6️⃣ Apply", "Use your improved resume to apply for jobs"),
    ]
    
    for title, desc in steps:
        st.markdown(f"**{title}** - {desc}")
    
    st.markdown("---")
    
    # Call to action
    st.markdown("""
    <div style='background: #f0f2f6; padding: 30px; border-radius: 10px; text-align: center;'>
        <h3>Ready to Improve Your Resume?</h3>
        <p>Start by uploading your resume and get instant AI-powered feedback</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📤 Upload Resume Now", use_container_width=True, key="home_upload_btn"):
        st.switch_page("pages/1_upload.py")
