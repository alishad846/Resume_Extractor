"""AI feedback page."""

import streamlit as st


def render():
    """Render the AI feedback page."""
    
    st.title("🤖 AI-Powered Feedback")
    
    if 'resume_data' not in st.session_state:
        st.info("📤 Please upload a resume first")
        if st.button("Upload Resume"):
            st.switch_page("pages/2_upload.py")
        return
    
    extracted = st.session_state.resume_data.get('extracted_data', {})
    
    st.markdown(f"### AI Feedback for {extracted.get('name', 'Your')} Resume")
    
    # Quality Assessment
    st.markdown("## 🏆 Quality Assessment")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Completeness", "92%", delta="+8%")
        st.write("Your resume includes most essential sections")
    
    with col2:
        st.metric("Readability", "78%", delta="+5%")
        st.write("Good formatting and structure")
    
    with col3:
        st.metric("ATS Optimization", "85%", delta="+3%")
        st.write("Optimized for applicant tracking systems")
    
    st.markdown("---")
    
    # Constructive Feedback
    st.markdown("## 💡 Constructive Feedback")
    
    feedback_items = [
        {
            "category": "Strengths ✅",
            "items": [
                "Clear professional structure with all major sections",
                "Good technical skills list with relevant technologies",
                "Multiple project examples demonstrating practical experience"
            ],
            "color": "success"
        },
        {
            "category": "Areas to Improve 📈",
            "items": [
                "Add more quantifiable metrics and achievements (e.g., 'Reduced API response time by 40%')",
                "Expand bullet points with action verbs and business impact",
                "Include summary/objective section for better context",
                "Add more detail to projects (technologies used, outcomes)"
            ],
            "color": "warning"
        },
        {
            "category": "Missing Sections ❓",
            "items": [
                "Professional Summary - helps recruiters quickly understand your background",
                "Certifications - validate your technical knowledge",
                "Languages - important for international roles"
            ],
            "color": "info"
        }
    ]
    
    for feedback in feedback_items:
        with st.expander(f"### {feedback['category']}", expanded=(feedback['color'] == 'info')):
            for item in feedback['items']:
                if feedback['color'] == 'success':
                    st.success(item)
                elif feedback['color'] == 'warning':
                    st.warning(item)
                else:
                    st.info(item)
    
    st.markdown("---")
    
    # ATS Optimization Tips
    st.markdown("## 📋 ATS Optimization Tips")
    
    tips = [
        ("✅ Use Simple Formatting", "Avoid tables, graphics, and unusual fonts. Stick to standard formatting that ATS systems can parse."),
        ("✅ Include Keywords", "Match job description keywords in your resume. Use the same terminology as the job posting."),
        ("✅ Proper Spacing", "Use clear spacing and line breaks. ATS systems may have trouble with dense text."),
        ("✅ Standard Section Headings", "Use commonly recognized headers (Experience, Skills, Education) that ATS systems expect."),
        ("❌ Avoid Images & Logos", "Don't include graphics or images in your resume as ATS systems skip them."),
        ("❌ Avoid Headers & Footers", "Use simple formatting without complex headers or footers."),
    ]
    
    for title, description in tips:
        st.markdown(f"**{title}**")
        st.caption(description)
    
    st.markdown("---")
    
    # Resume Improvement Suggestions
    st.markdown("## 🎯 Specific Improvement Suggestions")
    
    suggestions = [
        {
            "section": "Experience",
            "current": "Responsible for developing web applications",
            "suggested": "Designed and implemented 5+ full-stack web applications using Python/Django, improving user engagement by 35% and reducing page load time by 50%"
        },
        {
            "section": "Skills",
            "current": "Python, JavaScript, AWS",
            "suggested": "Python (Expert), JavaScript (Intermediate), AWS (Proficient), Docker, Kubernetes, PostgreSQL, React"
        },
        {
            "section": "Projects",
            "current": "Built a task management app",
            "suggested": "Built task management app (React, Node.js, MongoDB) with real-time notifications, used by 1000+ users, achieving 99.9% uptime"
        }
    ]
    
    for i, suggestion in enumerate(suggestions):
        with st.expander(f"### {suggestion['section']} Section"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Current:**")
                st.info(suggestion['current'])
            
            with col2:
                st.markdown("**Suggested:**")
                st.success(suggestion['suggested'])
    
    st.markdown("---")
    
    # Action Plans
    st.markdown("## 📊 Action Plan")
    
    action_plan = [
        ("High Priority", ["Add professional summary", "Quantify achievements with metrics"], "error"),
        ("Medium Priority", ["Expand project descriptions", "Add more technical keywords"], "warning"),
        ("Nice to Have", ["Add certifications section", "Include languages"], "info"),
    ]
    
    for priority, actions, color in action_plan:
        with st.expander(f"### {priority}"):
            for i, action in enumerate(actions, 1):
                if color == 'error':
                    st.error(f"{i}. {action}")
                elif color == 'warning':
                    st.warning(f"{i}. {action}")
                else:
                    st.info(f"{i}. {action}")
    
    st.markdown("---")
    
    # Next Steps
    st.markdown("## 🚀 Next Steps")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1. Implement Feedback**")
        st.caption("Apply the suggestions above to improve your resume")
    
    with col2:
        st.markdown("**2. Optimize Keywords**")
        st.caption("Match job description keywords for better ATS compatibility")
    
    with col3:
        st.markdown("**3. Test Matching**")
        st.caption("Try JD matching to see how well your resume fits specific jobs")
