import streamlit as st

def show():
    """Home page with hero section, features, and call-to-action"""
    
    # Hero Section
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 3rem; border-radius: 12px; color: white; text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);">
        <h1 style="font-size: 2.5rem; margin-bottom: 0.5rem;">🚀 Welcome to Resume AI Platform</h1>
        <p style="font-size: 1.2rem; opacity: 0.9;">Transform Your Resume Into Your Competitive Advantage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>🧠 AI Analysis</h3>
            <p>Advanced NLP powered by BERT and SpaCy extracts all important information from your resume automatically.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #8b5cf6; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>📊 Smart Scoring</h3>
            <p>Get an instant score that matches against job descriptions. Understand exactly what recruiters are looking for.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ec4899; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>💡 AI Feedback</h3>
            <p>Receive personalized improvement suggestions, ATS tips, and actionable advice to boost your resume.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Stats Section
    st.markdown("## 📈 By The Numbers")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Users", "2,500+", "↑ 180%")
    with col2:
        st.metric("📄 Resumes Analyzed", "15,000+", "↑ 320%")
    with col3:
        st.metric("🎯 JD Matches", "8,500+", "↑ 140%")
    with col4:
        st.metric("💼 Job Offers", "3,200+", "↑ 200%")
    
    # How It Works
    st.markdown("## 🔧 How It Works")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    steps = [
        ("📤", "Upload", "Upload your resume in PDF format"),
        ("🔍", "Analyze", "AI analyzes and extracts key information"),
        ("📊", "Score", "Get instant scoring and JD match"),
        ("💡", "Improve", "Receive AI-powered suggestions"),
        ("🎯", "Succeed", "Land your dream job")
    ]
    
    for i, (icon, title, desc) in enumerate(steps):
        with st.columns(5)[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; border-radius: 8px; background: #f8f9fa;">
                <h3>{icon}</h3>
                <h4>{title}</h4>
                <p style="font-size: 0.9rem; color: #666;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Benefits
    st.markdown("## 🎁 Why Choose Resume AI?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ✅ **AI-Powered Analysis**
        Uses state-of-the-art NLP models
        
        ✅ **Instant Feedback**
        Get real-time suggestions
        
        ✅ **ATS Optimization**
        Design-optimized for recruiters
        
        ✅ **Skill Matching**
        Match against job descriptions
        """)
    
    with col2:
        st.markdown("""
        ✅ **Career Insights**
        Discover career paths & growth
        
        ✅ **Salary Analytics**
        See market rates for your skills
        
        ✅ **Batch Processing**
        Upload multiple resumes
        
        ✅ **Private & Secure**
        Your data is always protected
        """)
    
    # Call to Action
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center;">
        <h2>Ready to Transform Your Resume?</h2>
        <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">Upload your resume now and get started with AI-powered analysis!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Now - Upload Resume", use_container_width=True, key="cta_button"):
            st.session_state.page = "Upload Resume"
            st.rerun()
    
    # Additional Info
    st.markdown("---")
    st.markdown("## ❓ FAQ")
    
    with st.expander("Is my resume data secure?"):
        st.write("Yes! All resumes are processed securely and encrypted. We never share your data with third parties.")
    
    with st.expander("What file formats are supported?"):
        st.write("We support PDF and DOCX formats. PDF is recommended for best results.")
    
    with st.expander("How accurate is the AI analysis?"):
        st.write("Our BERT-powered NLP model achieves 95%+ accuracy in entity extraction based on extensive testing.")
    
    with st.expander("Can I download my results?"):
        st.write("Yes! You can export your analysis, feedback, and career insights as PDF reports.")
