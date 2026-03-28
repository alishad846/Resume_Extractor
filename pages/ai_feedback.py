import streamlit as st

def show():
    """AI feedback page with improvement suggestions"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h1>💡 AI-Powered Feedback & Suggestions</h1>
        <p>Get personalized improvement recommendations to strengthen your resume.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if resume is loaded
    if 'extracted_data' not in st.session_state:
        st.warning("📤 Please upload a resume first on the Upload page.")
        return
    
    # Quality Assessment
    st.markdown("## 📋 Resume Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #ecfdf5; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #10b981;">
            <h4>✅ Readability</h4>
            <p style="font-size: 1.5rem; color: #10b981; margin: 0.5rem 0;">8.5/10</p>
            <p style="color: #666; font-size: 0.9rem;">Clear formatting and structure</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #eff6ff; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #3b82f6;">
            <h4>🎯 Relevance</h4>
            <p style="font-size: 1.5rem; color: #3b82f6; margin: 0.5rem 0;">7.2/10</p>
            <p style="color: #666; font-size: 0.9rem;">Job description alignment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #fef3c7; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f59e0b;">
            <h4>⚡ Impact</h4>
            <p style="font-size: 1.5rem; color: #f59e0b; margin: 0.5rem 0;">7.8/10</p>
            <p style="color: #666; font-size: 0.9rem;">Achievement quantification</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feedback Sections
    st.markdown("## 💪 Your Strengths")
    
    with st.expander("✅ What's Working Well", expanded=True):
        st.markdown("""
        1. **Strong Technical Skills Section**
           - Well-organized list of technologies
           - Good mix of programming languages and tools
           - Shows progressive skill development
        
        2. **Clear Work Experience**
           - Chronological format is easy to scan
           - Job titles are prominent
           - Responsibilities are well-described
        
        3. **Professional Contact Information**
           - All key contact details present
           - LinkedIn profile linked
           - Email is professional
        """)
    
    st.markdown("---")
    
    # Areas to Improve
    st.markdown("## 🎯 Areas to Improve")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ef4444;">
            <h3>⚠️ High Priority</h3>
            
            <p><strong>1. Add Quantifiable Achievements</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Replace vague descriptions with metrics. Instead of "improved system performance," write "improved system performance by 40% (from 2s to 1.2s response time)."</p>
            
            <p><strong>2. Use Action Verbs</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Strengthen descriptions with powerful action verbs like "engineered," "architected," "optimized" instead of "worked on" or "helped with."</p>
            
            <p><strong>3. Include Keywords</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Add industry-specific keywords mentioned in target job descriptions to improve ATS scoring.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #fffbeb; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #f59e0b;">
            <h3>💡 Medium Priority</h3>
            
            <p><strong>1. Expand Project Section</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Add 2-3 significant projects with links to GitHub or live demos. Include impact and technologies used.</p>
            
            <p><strong>2. Add Certifications</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Include relevant certifications (AWS, Google Cloud, etc.) to strengthen credibility.</p>
            
            <p><strong>3. Improve Summary</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Add a 2-3 line professional summary highlighting unique value proposition.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Missing Sections
    st.markdown("## ❓ Missing Sections")
    
    missing_sections = [
        ("Professional Summary", "1-2 lines highlighting your career focus"),
        ("Certifications", "AWS, Google Cloud, or industry certifications"),
        ("Languages", "if you speak multiple languages"),
        ("Volunteer Work", "Shows community involvement"),
        ("Publications", "Papers, articles, or blog posts")
    ]
    
    col1, col2 = st.columns(2)
    for i, (section, description) in enumerate(missing_sections):
        if i < len(missing_sections) // 2:
            col1.markdown(f"- **{section}**: {description}")
        else:
            col2.markdown(f"- **{section}**: {description}")
    
    st.markdown("---")
    
    # ATS Optimization Tips
    st.markdown("## 🤖 ATS Optimization Tips")
    
    st.markdown("""
    **Applicant Tracking Systems (ATS) scan resumes before humans do. Here's how to optimize:**
    
    1. ✅ **Use Standard Formatting**
       - Stick to basic fonts (Arial, Calibri, Times New Roman)
       - Avoid tables, headers, footers, and graphics
       - Use simple bullet points
    
    2. ✅ **Include Keywords**
       - Mirror keywords from job description
       - Use industry-standard terminology
       - Don't overuse the same word repeatedly (use synonyms)
    
    3. ✅ **Proper File Format**
       - Save as PDF to preserve formatting
       - Alternatively, use .docx if specified
       - Avoid .pages or uncommon formats
    
    4. ✅ **Clear Structure**
       - Use standard section headers: Summary, Experience, Education, Skills
       - List dates in consistent format (MM/DD/YYYY)
       - One column layout works best
    
    5. ✅ **Optimize Skills Section**
       - List skills as a simple comma-separated list or bullet points
       - Include both technical and soft skills
       - Use exact terminology from job postings
    """)
    
    st.markdown("---")
    
    # Specific Suggestions
    st.markdown("## 📝 Specific Suggestions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Before & After Examples")
        with st.expander("Example 1: Vague to Specific", expanded=False):
            st.markdown("""
            ❌ **Before:**
            > Worked on web development and improved performance
            
            ✅ **After:**
            > Engineered responsive web application serving 100K+ monthly users; optimized database queries reducing load time by 35%
            """)
        
        with st.expander("Example 2: Passive to Active"):
            st.markdown("""
            ❌ **Before:**
            > Responsible for maintaining code quality
            
            ✅ **After:**
            > Established code review process and automated testing pipeline, reducing production bugs by 50%
            """)
    
    with col2:
        st.markdown("### Action Plan")
        st.markdown("""
        **Priority 1 (This Week)**
        - [ ] Add quantifiable metrics to 3 experiences
        - [ ] Replace weak action verbs
        - [ ] Spell-check entire document
        
        **Priority 2 (Next Week)**
        - [ ] Add Professional Summary
        - [ ] Expand Projects section
        - [ ] Add relevant Certifications
        
        **Priority 3 (Next Few Weeks)**
        - [ ] Create tailored versions for target roles
        - [ ] Get feedback from mentors
        - [ ] Track interview success rate
        """)
    
    st.markdown("---")
    
    # Navigation
    st.markdown("## 🚀 Continue Your Journey")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Analysis", use_container_width=True):
            st.session_state.page = "Analysis"
            st.rerun()
    
    with col2:
        if st.button("🎯 Career Insights", use_container_width=True):
            st.session_state.page = "Career Insights"
            st.rerun()
    
    with col3:
        if st.button("📤 Upload New", use_container_width=True):
            st.session_state.page = "Upload Resume"
            st.rerun()
