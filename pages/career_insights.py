import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def show():
    """Career insights page with job recommendations and career paths"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h1>🎯 Career Insights & Recommendations</h1>
        <p>Discover job opportunities, career paths, and salary insights based on your profile.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if resume is loaded
    if 'extracted_data' not in st.session_state:
        st.warning("📤 Please upload a resume first on the Upload page.")
        return
    
    # Predicted Job Roles
    st.markdown("## 💼 Predicted Job Roles")
    
    job_roles = [
        ("Senior Software Engineer", 0.94),
        ("Full Stack Developer", 0.88),
        ("Technical Lead", 0.81),
        ("Solutions Architect", 0.76),
        ("DevOps Engineer", 0.71)
    ]
    
    roles, scores = zip(*job_roles)
    fig = px.barh(
        x=scores,
        y=roles,
        color=scores,
        color_continuous_scale="Viridis",
        title="Job Role Match Score",
        labels={"x": "Match Confidence", "y": "Role"}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Salary Insights
    st.markdown("## 💰 Salary Insights")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    salary_levels = [
        ("Entry Level", "$70K", "-"),
        ("Mid Level", "$110K", "Current"),
        ("Senior", "$150K", "+"),
        ("Lead", "$180K", "++"),
        ("Executive", "$220K", "++++")
    ]
    
    for i, (level, salary, badge) in enumerate(salary_levels):
        with st.columns(5)[i]:
            if badge == "Current":
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 8px; color: white; text-align: center; border: 3px solid #667eea;">
                    <h4 style="margin: 0; font-size: 0.9rem;">{level}</h4>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: bold;">{salary}</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem;">📍 Current</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #f3f4f6; padding: 1rem; border-radius: 8px; color: #1f2937; text-align: center;">
                    <h4 style="margin: 0; font-size: 0.9rem;">{level}</h4>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.3rem; font-weight: bold;">{salary}</p>
                    <p style="margin: 0.3rem 0 0 0; font-size: 0.8rem;">{badge}</p>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Skills Gap Analysis
    st.markdown("## 🎯 Skills Gap Analysis")
    
    current_skills = ["Python", "JavaScript", "SQL", "AWS", "Docker"]
    in_demand_skills = ["Python", "JavaScript", "SQL", "AWS", "Docker", "Kubernetes", "Terraform", "Grafana"]
    missing_skills = [s for s in in_demand_skills if s not in current_skills]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💪 Your Current Skills")
        for skill in current_skills:
            st.markdown(f"✅ {skill}")
    
    with col2:
        st.markdown("### 📍 Skills To Acquire")
        for skill in missing_skills:
            st.markdown(f"🎯 {skill}")
    
    st.markdown("---")
    
    # Career Paths
    st.markdown("## 📈 Possible Career Paths")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>🚀 Path 1: Management Track</h3>
            <p><strong>Timeline:</strong> 3-5 years</p>
            <ol>
                <li>Senior Software Engineer (1-2 years)</li>
                <li>Engineering Manager (2-3 years)</li>
                <li>Director of Engineering (2+ years)</li>
            </ol>
            <p><strong>Skills Needed:</strong> Leadership, Communication, Business acumen</p>
            <p><strong>Average Salary Growth:</strong> $110K → $220K+</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>🏗️ Path 2: Architecture Track</h3>
            <p><strong>Timeline:</strong> 4-6 years</p>
            <ol>
                <li>Senior Software Engineer (1-2 years)</li>
                <li>Solutions Architect (2-3 years)</li>
                <li>Chief Architect (2+ years)</li>
            </ol>
            <p><strong>Skills Needed:</strong> System design, Cloud expertise, Mentoring</p>
            <p><strong>Average Salary Growth:</strong> $110K → $200K+</p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>🔧 Path 3: Specialist Track</h3>
            <p><strong>Timeline:</strong> 3-4 years</p>
            <ol>
                <li>Senior Software Engineer (1-2 years)</li>
                <li>Principal Engineer (2-3 years)</li>
                <li>Staff Engineer (2+ years)</li>
            </ol>
            <p><strong>Skills Needed:</strong> Deep expertise, Innovation, Open source</p>
            <p><strong>Average Salary Growth:</strong> $110K → $210K+</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h3>🚀 Path 4: Startup Founder</h3>
            <p><strong>Timeline:</strong> Variable</p>
            <ol>
                <li>Build side project (1-2 years)</li>
                <li>Get funding (6-12 months)</li>
                <li>Scale company (ongoing)</li>
            </ol>
            <p><strong>Skills Needed:</strong> Product thinking, Sales, Fundraising</p>
            <p><strong>Potential Upside:</strong> $1M+ (equity dependent)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Learning Resources
    st.markdown("## 📚 Recommended Learning Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎓 Online Courses
        - **Udemy**: AWS Solutions Architect
        - **Coursera**: Google Cloud Platform specialization
        - **Pluralsight**: System Design masterclass
        - **LinkedIn Learning**: Leadership fundamentals
        """)
    
    with col2:
        st.markdown("""
        ### 📖 Books to Read
        - "System Design Interview" by Alex Xu
        - "The Manager's Path" by Camille Fournier
        - "Staff Engineer" by Will Larson
        - "Designing Data-Intensive Applications" by Martin Kleppmann
        """)
    
    st.markdown("---")
    
    # Job Recommendations
    st.markdown("## 💼 Recommended Jobs")
    
    jobs = [
        {
            "title": "Senior Full Stack Engineer",
            "company": "TechCorp Inc",
            "salary": "$140K - $180K",
            "match": "94%",
            "location": "San Francisco, CA"
        },
        {
            "title": "Backend Engineer Lead",
            "company": "CloudStart",
            "salary": "$130K - $160K",
            "match": "88%",
            "location": "New York, NY"
        },
        {
            "title": "Solutions Architect",
            "company": "Enterprise Software",
            "salary": "$150K - $190K",
            "match": "81%",
            "location": "Remote"
        },
        {
            "title": "DevOps Engineer",
            "company": "StartupXYZ",
            "salary": "$120K - $150K",
            "match": "76%",
            "location": "Austin, TX"
        }
    ]
    
    for job in jobs:
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h4 style="margin: 0;">{job['title']}</h4>
                <p style="margin: 0.3rem 0; color: #667eea; font-weight: bold;">{job['company']}</p>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">📍 {job['location']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"💰 {job['salary']}")
        
        with col3:
            st.markdown(f"**{job['match']}** Match")
    
    st.markdown("---")
    
    # Industry Trends
    st.markdown("## 📊 Industry Trends")
    
    year = [2020, 2021, 2022, 2023, 2024, 2025]
    demand = [60, 70, 82, 90, 95, 100]
    salary = [85, 95, 110, 125, 140, 155]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=year, y=demand,
        mode='lines+markers',
        name='Job Demand Index',
        line=dict(color='#667eea', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=year, y=salary,
        mode='lines+markers',
        name='Avg Salary (K)',
        line=dict(color='#ec4899', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='Tech Industry Trends',
        xaxis_title='Year',
        yaxis_title='Job Demand Index',
        yaxis2=dict(title='Average Salary (K)', overlaying='y', side='right'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 View Analysis", use_container_width=True):
            st.session_state.page = "Analysis"
            st.rerun()
    
    with col2:
        if st.button("💡 Get Feedback", use_container_width=True):
            st.session_state.page = "AI Feedback"
            st.rerun()
    
    with col3:
        if st.button("📤 Upload New", use_container_width=True):
            st.session_state.page = "Upload Resume"
            st.rerun()
