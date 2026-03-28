"""Career insights page."""

import streamlit as st
import plotly.express as px
import pandas as pd


def render():
    """Render the career insights page."""
    
    st.title("🎯 Career Insights & Recommendations")
    
    if 'resume_data' not in st.session_state:
        st.info("📤 Please upload a resume first")
        if st.button("Upload Resume"):
            st.switch_page("pages/2_upload.py")
        return
    
    extracted = st.session_state.resume_data.get('extracted_data', {})
    
    st.markdown(f"### Career Intelligence Report for {extracted.get('name', 'Your')} Profile")
    
    # Job Role Prediction
    st.markdown("## 💼 Predicted Job Roles")
    
    predicted_roles = [
        {"role": "Senior Software Engineer", "confidence": 0.92, "match": 92},
        {"role": "Full Stack Developer", "confidence": 0.87, "match": 87},
        {"role": "DevOps Engineer", "confidence": 0.81, "match": 81},
        {"role": "Tech Lead", "confidence": 0.78, "match": 78},
        {"role": "Cloud Architect", "confidence": 0.72, "match": 72},
    ]
    
    for i, role_info in enumerate(predicted_roles):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {i+1}. {role_info['role']}")
            st.progress(role_info['confidence'])
        
        with col2:
            st.metric("Match", f"{role_info['match']}%")
    
    st.markdown("---")
    
    # Skills Gap Analysis
    st.markdown("## 📚 Skills Gap Analysis")
    
    st.markdown("### Skills You Have")
    current_skills = extracted.get('skills', [])[:10]
    if current_skills:
        cols = st.columns(4)
        for i, skill in enumerate(current_skills):
            with cols[i % 4]:
                st.metric("", skill)
    
    st.markdown("### Skills to Learn")
    
    recommended_skills = [
        {"skill": "Kubernetes", "demand": "Very High", "relevance": "95%", "courses": 45},
        {"skill": "Go", "demand": "High", "relevance": "88%", "courses": 32},
        {"skill": "GraphQL", "demand": "High", "relevance": "85%", "courses": 28},
        {"skill": "Terraform", "demand": "Very High", "relevance": "92%", "courses": 19},
        {"skill": "Machine Learning", "demand": "High", "relevance": "78%", "courses": 67},
    ]
    
    df_skills = pd.DataFrame(recommended_skills)
    
    fig = px.bar(
        df_skills,
        x='relevance',
        y='skill',
        orientation='h',
        color='demand',
        color_discrete_map={
            'Very High': '#dc3545',
            'High': '#ffc107',
            'Medium': '#17a2b8'
        }
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Career Path Recommendations
    st.markdown("## 🗺️ Career Path Recommendations")
    
    career_paths = [
        {
            "path": "Frontend Specialist",
            "description": "Deep expertise in modern web frameworks and UI/UX",
            "timeline": "12-18 months",
            "investment": "Medium"
        },
        {
            "path": "Cloud & DevOps",
            "description": "Infrastructure, containerization, and cloud deployment",
            "timeline": "18-24 months",
            "investment": "High"
        },
        {
            "path": "Engineering Manager",
            "description": "Lead technical teams and manage projects",
            "timeline": "24-36 months",
            "investment": "Medium"
        },
        {
            "path": "AI/ML Engineer",
            "description": "Build machine learning models and data pipelines",
            "timeline": "18-24 months",
            "investment": "High"
        },
    ]
    
    for i, path in enumerate(career_paths):
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"### {path['path']}")
            st.caption(path['description'])
        
        with col2:
            st.metric("Timeline", path['timeline'])
        
        with col3:
            st.metric("Investment", path['investment'])
    
    st.markdown("---")
    
    # Salary Insights
    st.markdown("## 💰 Salary Insights")
    
    salary_data = pd.DataFrame({
        'Role': ['Junior Dev', 'Mid-level Dev', 'Senior Dev', 'Tech Lead', 'Engineering Manager'],
        'Min Salary': [60000, 90000, 120000, 150000, 180000],
        'Avg Salary': [75000, 110000, 145000, 175000, 210000],
        'Max Salary': [90000, 130000, 180000, 220000, 280000]
    })
    
    fig = px.bar(
        salary_data,
        x='Role',
        y=['Min Salary', 'Avg Salary', 'Max Salary'],
        barmode='group',
        title='Expected Salary Ranges by Role'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Learning Resources
    st.markdown("## 📖 Recommended Learning Resources")
    
    resources = {
        "Online Courses": [
            ("Kubernetes Complete Guide", "Udemy", "⭐⭐⭐⭐⭐"),
            ("Go Programming Masterclass", "Udemy", "⭐⭐⭐⭐⭐"),
            ("Machine Learning Specialization", "Coursera", "⭐⭐⭐⭐⭐"),
        ],
        "Books": [
            ("The Go Programming Language", "Alan Donovan & Brian Kernighan", "⭐⭐⭐⭐⭐"),
            ("Kubernetes in Action", "Marko Lukša", "⭐⭐⭐⭐⭐"),
            ("Hands-On Machine Learning", "Aurélien Géron", "⭐⭐⭐⭐⭐"),
        ],
        "Communities": [
            ("Tech Stack Overflow", "Developer Q&A", "Very Active"),
            ("Dev.to", "Tech Blog Community", "Very Active"),
            ("GitHub", "Open Source Contributions", "Very Active"),
        ]
    }
    
    for resource_type, items in resources.items():
        with st.expander(f"### {resource_type}"):
            for item, author, rating in items:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{item}** - {author}")
                with col2:
                    st.write(f"{rating}")
    
    st.markdown("---")
    
    # Job Recommendations
    st.markdown("## 🎯 Recommended Job Openings")
    
    job_recommendations = [
        ("Senior Python Developer", "TechCorp Inc", "San Francisco, CA", 95),
        ("Full Stack Engineer", "StartupXYZ", "Remote", 88),
        ("DevOps Engineer", "CloudSys Ltd", "New York, NY", 92),
        ("Technical Lead", "MegaTech Corp", "Austin, TX", 85),
    ]
    
    for job_title, company, location, match in job_recommendations:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{job_title}** @ {company}")
            st.caption(f"📍 {location}")
        
        with col2:
            st.metric("Match", f"{match}%")
        
        with col3:
            if st.button("View", key=f"job_{job_title}"):
                st.info(f"Viewing details for {job_title}")
    
    st.markdown("---")
    
    # Actionable Recommendations
    st.markdown("## 🚀 Your Action Plan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Short Term (1-3 months)")
        st.write("- Learn Kubernetes basics")
        st.write("- Get certified (CKA)")
        st.write("- Contribute to open source")
    
    with col2:
        st.markdown("### Long Term (6-12 months)")
        st.write("- Build cloud infrastructure projects")
        st.write("- Lead small team or mentor juniors")
        st.write("- Build personal brand (blog/speaking)")
