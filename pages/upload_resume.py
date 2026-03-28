import streamlit as st
import fitz
from model_utils import load_ner_model, extract_entities

def show():
    """Resume upload page with file handling and preview"""
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;">
        <h1>📤 Upload Your Resume</h1>
        <p>Upload your resume and let AI extract and analyze all important information automatically.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File Upload Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📁 Choose File")
        uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    
    with col2:
        st.markdown("### 📋 Accepted Formats")
        st.info("✅ PDF\n✅ DOCX\n\n👉 PDF recommended")
    
    if uploaded_file:
        st.markdown("---")
        
        # Processing Status
        with st.spinner("🔄 Processing your resume..."):
            try:
                # Extract text based on file type
                if uploaded_file.type == "application/pdf":
                    pdf_doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                    full_text = ""
                    for page in pdf_doc:
                        full_text += page.get_text()
                else:
                    st.warning("DOCX support coming soon. Please use PDF format.")
                    return
                
                # Display file info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("File Size", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
                with col2:
                    st.metric("Characters", f"{len(full_text):,}")
                with col3:
                    st.metric("Pages", len(pdf_doc))
                
                st.markdown("---")
                
                # Extracted Text Preview
                st.markdown("### 📃 Extracted Text Preview")
                with st.expander("View Full Text", expanded=False):
                    st.text_area("Resume Text", full_text, height=300, disabled=True)
                
                # Extract Entities
                st.markdown("### 🧠 AI Analysis Results")
                
                with st.spinner("Extracting information..."):
                    ner_model = load_ner_model()
                    extracted_data = extract_entities(full_text, ner_model)
                
                # Display extracted entities in nice columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### 👤 Personal Information")
                    if extracted_data.get('NAME'):
                        st.markdown(f"**Name:** {', '.join(extracted_data['NAME'])}")
                    if extracted_data.get('EMAIL'):
                        st.markdown(f"**Email:** {', '.join(extracted_data['EMAIL'])}")
                    if extracted_data.get('PHONE'):
                        st.markdown(f"**Phone:** {', '.join(extracted_data['PHONE'])}")
                    if extracted_data.get('URL'):
                        st.markdown(f"**Website:** {', '.join(extracted_data['URL'][:2])}")
                
                with col2:
                    st.markdown("#### 🎓 Education & Skills")
                    if extracted_data.get('EDUCATION'):
                        st.markdown(f"**Education:** {', '.join(extracted_data['EDUCATION'])}")
                    if extracted_data.get('SKILL'):
                        st.markdown(f"**Skills:** {', '.join(extracted_data['SKILL'][:10])}")
                
                st.markdown("---")
                
                # Next Steps
                st.markdown("### 🚀 Next Steps")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📊 View Full Analysis", use_container_width=True):
                        st.session_state.page = "Analysis"
                        st.rerun()
                
                with col2:
                    if st.button("💡 Get AI Feedback", use_container_width=True):
                        st.session_state.page = "AI Feedback"
                        st.rerun()
                
                with col3:
                    if st.button("🎯 Career Insights", use_container_width=True):
                        st.session_state.page = "Career Insights"
                        st.rerun()
                
                # Save to session state
                st.session_state.resume_text = full_text
                st.session_state.extracted_data = extracted_data
                st.success("✅ Resume uploaded and analyzed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    else:
        st.markdown("---")
        st.info("👆 Upload a resume to get started!")
        
        # Tips Section
        st.markdown("### 💡 Tips for Best Results")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ✅ Use standard fonts (Arial, Calibri)
            ✅ Keep formatting simple
            ✅ Include contact information
            ✅ List skills clearly
            """)
        
        with col2:
            st.markdown("""
            ❌ Avoid images and graphics
            ❌ Don't use unusual colors
            ❌ Skip creative formatting
            ❌ Keep sections well-organized
            """)
