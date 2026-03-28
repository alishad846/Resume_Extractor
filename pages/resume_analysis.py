import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

def show():
    """Resume analysis page with scoring and detailed breakdown"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h1>📊 Resume Analysis & Scoring</h1>
        <p>Detailed breakdown of your resume with AI-powered scoring and recommendations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if resume is loaded
    if 'extracted_data' not in st.session_state:
        st.warning("📤 Please upload a resume first on the Upload page.")
        return
    
    extracted_data = st.session_state.extracted_data
    
    # Overall Score Section
    st.markdown("## 🎯 Overall Score")
    
    # Generate mock score (in real implementation, this comes from scorer.py)
    overall_score = 78
    grade = "B+"
    percentile = 85
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        fig = go.Figure(data=[go.Indicator(
            mode="gauge+number",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#667eea"},
                'steps': [
                    {'range': [0, 50], 'color': "#fee2e2"},
                    {'range': [50, 75], 'color': "#fef3c7"},
                    {'range': [75, 100], 'color': "#dcfce7"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}
        )])
        fig.update_layout(height=300, width=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Grade", grade, delta="Above Average")
    
    with col3:
        st.metric("Percentile", f"{percentile}%", delta="+5%")
    
    with col4:
        st.metric("Completeness", "92%", delta="+8%")
    
    st.markdown("---")
    
    # Dimension Scores
    st.markdown("## 📈 Dimension Breakdown")
    
    dimensions = {
        "Skills Match": 82,
        "Experience": 76,
        "Education": 88,
        "Projects": 71,
        "Completeness": 92
    }
    
    # Bar chart
    fig = px.bar(
        x=list(dimensions.keys()),
        y=list(dimensions.values()),
        color=list(dimensions.values()),
        color_continuous_scale="Viridis",
        title="Score by Dimension",
        labels={"y": "Score", "x": "Dimension"}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4>🧠 Skills Match</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #667eea; margin: 0;">82%</p>
            <p style="color: #666; margin-top: 0.5rem;">Matches job market demand</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #8b5cf6; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4>💼 Experience</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #8b5cf6; margin: 0;">76%</p>
            <p style="color: #666; margin-top: 0.5rem;">Years & relevance score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; border-left: 4px solid #ec4899; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4>🎓 Education</h4>
            <p style="font-size: 2rem; font-weight: bold; color: #ec4899; margin: 0;">88%</p>
            <p style="color: #666; margin-top: 0.5rem;">Degree & certification quality</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Extracted Data Display
    st.markdown("## 📋 Extracted Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Personal Information")
        displayed_data = {
            "Name": ", ".join(extracted_data.get('NAME', ['Not found'])),
            "Email": ", ".join(extracted_data.get('EMAIL', ['Not found'])),
            "Phone": ", ".join(extracted_data.get('PHONE', ['Not found'])),
            "Website": ", ".join(extracted_data.get('URL', ['Not found'])[:1]),
        }
        for key, value in displayed_data.items():
            st.write(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### Skills & Qualifications")
        displayed_skills = {
            "Skills": ", ".join(extracted_data.get('SKILL', ['Not found'])[:5]),
            "Education": ", ".join(extracted_data.get('EDUCATION', ['Not found'])),
        }
        for key, value in displayed_skills.items():
            st.write(f"**{key}:** {value}")
    
    st.markdown("---")
    
    # Skills Chart
    st.markdown("## 🎯 Skills Analysis")
    
    skills = extracted_data.get('SKILL', [])
    if skills:
        # Count skill frequency (mock data for visualization)
        skill_data = {skill: len(skill) % 10 + 1 for skill in skills[:8]}
        fig = px.bar(
            x=list(skill_data.keys()),
            y=list(skill_data.values()),
            title="Top Skills",
            labels={"x": "Skill", "y": "Occurrences"}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Experience Timeline (mock)
    st.markdown("## 📅 Experience Timeline")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #f0f4ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;">
            <h4>2022 - Present</h4>
            <p><strong>Senior Developer</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Led ML projects, managed teams</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f4ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;">
            <h4>2020 - 2022</h4>
            <p><strong>Software Engineer</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Full-stack development, APIs</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #f0f4ff; padding: 1rem; border-radius: 8px; border-left: 4px solid #667eea;">
            <h4>2018 - 2020</h4>
            <p><strong>Junior Developer</strong></p>
            <p style="color: #666; font-size: 0.9rem;">Web development, internship</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Actions
    st.markdown("## 🚀 Next Steps")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Get AI Feedback", use_container_width=True):
            st.session_state.page = "AI Feedback"
            st.rerun()
    
    with col2:
        if st.button("📈 Career Insights", use_container_width=True):
            st.session_state.page = "Career Insights"
            st.rerun()
    
    with col3:
        if st.button("📤 Upload Another", use_container_width=True):
            st.session_state.page = "Upload Resume"
            st.rerun()
