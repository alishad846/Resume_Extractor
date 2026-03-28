import fitz
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

from model_utils import (
    calculate_jd_match,
    calculate_resume_score,
    extract_entities,
    generate_ai_feedback,
    infer_role_matches,
    load_ner_model,
)


st.set_page_config(
    page_title="Resume AI Platform",
    page_icon="Resume",
    layout="wide",
    initial_sidebar_state="expanded",
)

css = """
<style>
    .main { background: linear-gradient(to bottom, #f8fafc 0%, #e0e7ff 100%); padding: 2rem; border-radius: 12px; color: #000000; }
    .stApp, .stApp p, .stApp div, .stApp span, .stApp label, .stApp li, .stMarkdown {
        color: #000000 !important;
    }
    [data-testid="stSidebarNavItems"] {
        display: none;
    }
    .stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; padding: 0.75rem 1.5rem; font-weight: 600; }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4); }
</style>
"""
st.markdown(css, unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"
if "resume_text" not in st.session_state:
    st.session_state.resume_text = None
if "extracted_data" not in st.session_state:
    st.session_state.extracted_data = None


def render_header(title, subtitle=""):
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_extracted():
    return st.session_state.extracted_data or {}


with st.sidebar:
    st.markdown("### Resume AI Platform")
    st.markdown("---")

    menu_options = ["Home", "Upload Resume", "Resume Analysis", "AI Feedback", "Career Insights"]
    menu_icons = ["house", "cloud-upload", "bar-chart", "lightbulb", "briefcase"]
    current_page = st.session_state.page
    if current_page not in menu_options:
        current_page = "Home"

    selected = option_menu(
        menu_title=None,
        options=menu_options,
        icons=menu_icons,
        default_index=menu_options.index(current_page),
    )

    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

    st.markdown("---")
    st.markdown("### Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Resumes", "1" if st.session_state.resume_text else "0")
    with col2:
        if st.session_state.resume_text and st.session_state.extracted_data:
            score = calculate_resume_score(st.session_state.resume_text, st.session_state.extracted_data)["overall_score"]
        else:
            score = 0
        st.metric("Score", f"{score}%")


if st.session_state.page == "Home":
    render_header("Resume AI Platform", "Extract resume data, compare with job descriptions, and get grounded feedback.")

    st.markdown("## Key Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Resume Extraction")
        st.write("Parse contact info, skills, education, experience, projects, and links from PDF resumes.")
    with col2:
        st.markdown("### JD Matching")
        st.write("Compare resume skills and experience against a pasted job description.")
    with col3:
        st.markdown("### Real Feedback")
        st.write("Get feedback and role suggestions based on the extracted resume content, not fixed demo text.")

    if st.button("Start Now", use_container_width=True):
        st.session_state.page = "Upload Resume"
        st.rerun()


elif st.session_state.page == "Upload Resume":
    render_header("Upload Your Resume", "Upload a PDF and let the parser extract the real content.")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        with st.spinner("Processing resume..."):
            try:
                pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                full_text = ""
                for page in pdf_doc:
                    full_text += page.get_text("text", sort=True) + "\n"

                extracted_data = extract_entities(full_text, load_ner_model())
                st.session_state.resume_text = full_text
                st.session_state.extracted_data = extracted_data

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
                with col2:
                    st.metric("Characters", f"{len(full_text):,}")
                with col3:
                    st.metric("Pages", len(pdf_doc))

                st.success("Resume processed successfully.")
                st.markdown("---")
                st.markdown("### Resume processed — continue to Resume Analysis for extraction details, scoring, and JD matching.")
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("View Analysis", use_container_width=True):
                        st.session_state.page = "Resume Analysis"
                        st.rerun()
                with col2:
                    if st.button("Open Feedback", use_container_width=True):
                        st.session_state.page = "AI Feedback"
                        st.rerun()
                with col3:
                    if st.button("Open Career Insights", use_container_width=True):
                        st.session_state.page = "Career Insights"
                        st.rerun()
            except Exception as exc:
                st.error(f"Error: {exc}")


elif st.session_state.page == "Resume Analysis":
    if not st.session_state.resume_text:
        st.warning("Please upload a resume first.")
    else:
        render_header("Resume Analysis", "A score breakdown based on the extracted resume structure and content.")
        extracted = get_extracted()
        resume_scores = calculate_resume_score(st.session_state.resume_text, extracted)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Overall Score", resume_scores["overall_score"])
        with col2:
            st.metric("Grade", resume_scores["grade"])
        with col3:
            st.metric("Percentile", f"{resume_scores['percentile']}%")
        with col4:
            st.metric("Completeness", f"{resume_scores['dimensions']['Completeness']}%")

        dimensions = resume_scores["dimensions"]
        fig = px.bar(
            x=list(dimensions.keys()),
            y=list(dimensions.values()),
            title="Resume Score by Dimension",
            color=list(dimensions.values()),
            color_continuous_scale="Viridis",
        )
        fig.update_layout(height=400, showlegend=False, yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("## Extracted Information")
        col1, col2 = st.columns(2)
        with col1:
            st.write("Names:", ", ".join(extracted.get("NAME", ["N/A"])))
            st.write("Emails:", ", ".join(extracted.get("EMAIL", ["N/A"])))
            st.write("Phones:", ", ".join(extracted.get("PHONE", ["N/A"])))
            st.write("Location:", ", ".join(extracted.get("LOCATION", ["N/A"])))
        with col2:
            st.write("Skills:", ", ".join(extracted.get("SKILL", ["N/A"])[:20]))
            st.write("Education:", ", ".join(extracted.get("EDUCATION", ["N/A"])[:5]))
            st.write("Experience:", ", ".join(extracted.get("EXPERIENCE", ["N/A"])[:5]))
            st.write("Projects:", ", ".join(extracted.get("PROJECT", ["N/A"])[:5]))
        st.markdown("---")
        st.markdown("## Job Description Matching")
        jd_input = st.text_area(
            "Paste a job description",
            height=140,
            placeholder="Example: Looking for a Python developer with 3+ years of experience in FastAPI, SQL, and Docker...",
        )
        if jd_input and jd_input.strip():
            jd_match = calculate_jd_match(
                st.session_state.resume_text,
                extracted.get("SKILL", []),
                jd_input,
                extracted,
            )
            if jd_match:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Overall Match", f"{jd_match['match_percentage']}%")
                with col2:
                    st.metric("Skill Match", f"{len(jd_match['matched_skills'])}/{len(jd_match['jd_found_skills'])}")
                with col3:
                    st.metric("Experience Fit", f"{jd_match['experience_fit_score']}/100")

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Matched Skills")
                    if jd_match["matched_skills"]:
                        for skill in jd_match["matched_skills"]:
                            st.write(f"- {skill}")
                    else:
                        st.write("- No matched skills found")
                with col2:
                    st.markdown("### Missing Skills")
                    if jd_match["missing_skills"]:
                        for skill in jd_match["missing_skills"][:8]:
                            st.write(f"- {skill}")
                    else:
                        st.write("- No major missing skills detected")

                domain_required = jd_match.get("domains_required", [])
                stack_required = jd_match.get("stack_required", [])
                if domain_required or stack_required:
                    st.markdown("### Domain & Stack Fit")
                    if domain_required:
                        matched_domains = jd_match.get("domains_matched", [])
                        missing_domains = jd_match.get("domains_missing", [])
                        if matched_domains:
                            st.write(f"Matched domains: {', '.join(matched_domains)}")
                        if missing_domains:
                            st.write(f"Missing domain focus: {', '.join(missing_domains)}")
                    if stack_required:
                        matched_stack = jd_match.get("stack_matched", [])
                        missing_stack = jd_match.get("stack_missing", [])
                        if matched_stack:
                            st.write(f"Matched AI stack topics: {', '.join(matched_stack)}")
                        if missing_stack:
                            st.write(f"Missing stack focus: {', '.join(missing_stack)}")

                st.markdown("### Recommendations")
                for item in jd_match["recommendations"]:
                    st.write(f"- {item}")


elif st.session_state.page == "AI Feedback":
    if not st.session_state.resume_text:
        st.warning("Please upload a resume first.")
    else:
        render_header("AI-Powered Feedback", "Feedback grounded in the extracted sections and actual resume content.")
        feedback = generate_ai_feedback(st.session_state.resume_text, get_extracted())

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Readability", f"{feedback['readability_score']}/100")
        with col2:
            st.metric("Completeness", f"{feedback['completeness_score']}/100")
        with col3:
            st.metric("Impact", f"{feedback['impact_score']}/100")

        st.markdown("## Strengths")
        if feedback["strengths"]:
            for item in feedback["strengths"]:
                st.write(f"- {item}")
        else:
            st.write("- The resume still needs stronger extracted evidence before strengths can be stated confidently.")

        st.markdown("## Improvements")
        if feedback["improvements"]:
            for item in feedback["improvements"]:
                st.write(f"- {item}")
        else:
            st.write("- No major improvement items detected from the current extraction.")

        if feedback["missing_sections"]:
            st.markdown("## Missing Sections")
            for section in feedback["missing_sections"]:
                st.write(f"- {section}")

        if feedback["action_plan"]:
            st.markdown("## Next Steps")
            for item in feedback["action_plan"]:
                st.write(f"- {item}")


elif st.session_state.page == "Career Insights":
    if not st.session_state.resume_text:
        st.warning("Please upload a resume first.")
    else:
        render_header("Career Insights", "Suggested role directions based on the skills that were actually extracted.")
        extracted = get_extracted()
        role_matches = infer_role_matches(extracted)
        top_skills = extracted.get("SKILL", [])

        st.markdown("## Predicted Job Roles")
        if role_matches:
            fig = px.bar(
                x=[item["score"] for item in role_matches],
                y=[item["role"] for item in role_matches],
                orientation="h",
                title="Role Match Based on Extracted Skills",
                color=[item["score"] for item in role_matches],
                color_continuous_scale="Viridis",
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

            for role in role_matches:
                st.markdown(f"### {role['role']}")
                st.write(f"Matched skills: {', '.join(role['matched_skills'])}")
                if role["missing_skills"]:
                    st.write(f"Missing for this path: {', '.join(role['missing_skills'])}")
        else:
            st.info("Not enough extracted skill evidence yet to infer reliable role matches.")

        st.markdown("## Current Strength Areas")
        if top_skills:
            st.write(", ".join(top_skills[:20]))
        else:
            st.write("No reliable skills extracted yet.")

        st.markdown("## Suggested Next Skills")
        suggested_skills = []
        for role in role_matches:
            for skill in role["missing_skills"]:
                if skill not in suggested_skills:
                    suggested_skills.append(skill)

        if suggested_skills:
            for skill in suggested_skills[:10]:
                st.write(f"- {skill}")
        else:
            st.write("- Keep strengthening portfolio depth, quantified impact, and role-specific projects.")
