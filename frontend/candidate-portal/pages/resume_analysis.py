"""Resume analysis page."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def render():
    """Render the resume analysis page."""
    
    st.title("📊 Resume Analysis")
    
    if 'resume_data' not in st.session_state:
        st.info("📤 Please upload a resume first")
        if st.button("Upload Resume"):
            st.switch_page("pages/2_upload.py")
        return
    
    resume_data = st.session_state.resume_data
    extracted = resume_data.get('extracted_data', {})
    
    st.markdown(f"### {extracted.get('name', 'Unknown')}'s Resume Analysis")
    
    # Resume Score Display
    st.markdown("---")
    st.markdown("## 📈 Resume Score")
    
    # Mock scoring (would call backend)
    overall_score = 78.5
    grade = "B"
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Circular gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Score"},
            delta={'reference': 80},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#1f77b4"},
                   'steps': [
                       {'range': [0, 40], 'color': "#dc3545"},
                       {'range': [40, 60], 'color': "#ffc107"},
                       {'range': [60, 80], 'color': "#17a2b8"},
                       {'range': [80, 100], 'color': "#28a745"}
                   ]}
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.metric("Grade", grade, delta=None)
        st.metric("Percentile", "72nd", delta="+5")
    
    with col3:
        st.metric("Completeness", "92%", delta="+3%")
    
    with col4:
        st.metric("ATS Score", "85%", delta="-2%")
    
    st.markdown("---")
    
    # Dimension Scores
    st.markdown("## 📊 Dimension Scores")
    
    scores_data = {
        'Skills Match': 82,
        'Experience': 76,
        'Education': 71,
        'Projects': 68,
        'Completeness': 92
    }
    
    fig = px.bar(
        x=list(scores_data.values()),
        y=list(scores_data.keys()),
        orientation='h',
        color=list(scores_data.values()),
        color_continuous_scale='RdYlGn',
        range_color=[0, 100]
    )
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Extracted Data Summary
    st.markdown("## 📋 Extracted Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Contact Information")
        st.write(f"**Name:** {extracted.get('name', 'N/A')}")
        st.write(f"**Email:** {extracted.get('email', ['N/A'])[0] if extracted.get('email') else 'N/A'}")
        st.write(f"**Phone:** {extracted.get('phone', ['N/A'])[0] if extracted.get('phone') else 'N/A'}")
        st.write(f"**LinkedIn:** {extracted.get('linkedin', 'N/A') or 'Not found'}")
        st.write(f"**GitHub:** {extracted.get('github', 'N/A') or 'Not found'}")
    
    with col2:
        st.markdown("### Summary Statistics")
        st.write(f"**Skills:** {len(extracted.get('skills', []))} technical skills identified")
        st.write(f"**Experience:** {len(extracted.get('experience', []))} work positions")
        st.write(f"**Education:** {len(extracted.get('education', []))} educational entries")
        st.write(f"**Projects:** {len(extracted.get('projects', []))} projects listed")
        st.write(f"**Languages:** {len(extracted.get('languages', []))} languages")
    
    st.markdown("---")
    
    # Skills Analysis
    st.markdown("## 💻 Skills Analysis")
    
    skills = extracted.get('skills', [])
    
    if skills:
        # Skills word cloud / bar chart
        skill_counts = {skill: 1 for skill in skills[:15]}
        
        df_skills = pd.DataFrame(list(skill_counts.items()), columns=['Skill', 'Count'])
        
        fig = px.bar(df_skills, x='Count', y='Skill', orientation='h')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Skills tags
        st.markdown("### Top Skills")
        cols = st.columns(4)
        for i, skill in enumerate(skills[:12]):
            with cols[i % 4]:
                st.label_color_primary = "#1f77b4"
                st.markdown(f"🏷️ {skill}")
    
    else:
        st.info("No skills found in resume")
    
    st.markdown("---")
    
    # Experience Timeline
    st.markdown("## 📼 Experience Timeline")
    
    experience = extracted.get('experience', [])
    
    if experience:
        for i, exp in enumerate(experience[:5]):
            with st.expander(f"**{exp.get('position', 'Position')}** at {exp.get('company', 'Company')}"):
                st.write(f"**Duration:** {exp.get('duration', 'Not specified')}")
                st.write(f"**Description:** {exp.get('description', 'N/A')}")
    
    else:
        st.info("No work experience found")
    
    st.markdown("---")
    
    # Action Items
    st.markdown("## 🎯 Recommended Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🤖 Get AI Feedback", use_container_width=True):
            st.switch_page("pages/4_feedback.py")
    
    with col2:
        if st.button("📝 Edit Resume", use_container_width=True):
            st.info("Resume editing feature coming soon")
    
    with col3:
        if st.button("📊 JD Matching", use_container_width=True):
            st.info("JD matching feature coming soon")
