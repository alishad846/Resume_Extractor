"""Upload resume page."""

import streamlit as st
import requests
import json
from pathlib import Path


def render():
    """Render the upload resume page."""
    
    st.title("📤 Upload Your Resume")
    
    st.markdown("""
    Upload your resume in PDF or DOCX format. Our AI will automatically extract and analyze your information.
    """)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a resume file",
        type=["pdf", "docx", "doc"],
        help="Max file size: 10MB"
    )
    
    if uploaded_file:
        st.success(f"✅ File selected: {uploaded_file.name}")
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_file.name.split('/')[-1])
        with col2:
            st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
        with col3:
            st.metric("File Type", uploaded_file.type)
        
        st.markdown("---")
        
        # Process button
        if st.button("🚀 Analyze Resume", use_container_width=True, key="analyze_btn"):
            with st.spinner("🔄 Processing your resume..."):
                try:
                    # Save uploaded file temporarily
                    temp_file = f"/tmp/{uploaded_file.name}"
                    with open(temp_file, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Call backend API
                    with open(temp_file, "rb") as f:
                        files = {"file": f}
                        response = requests.post(
                            "http://localhost:8000/api/extraction/extract",
                            files=files
                        )
                    
                    if response.status_code == 200:
                        st.session_state.resume_data = response.json()
                        
                        st.success("✅ Resume analyzed successfully!")
                        st.balloons()
                        
                        # Show extracted data preview
                        st.markdown("### 📋 Extracted Information Preview")
                        
                        extracted = response.json().get('extracted_data', {})
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.write(f"**Name:** {extracted.get('name', 'N/A')}")
                            st.write(f"**Email:** {extracted.get('email', ['N/A'])[0] if extracted.get('email') else 'N/A'}")
                            st.write(f"**Phone:** {extracted.get('phone', ['N/A'])[0] if extracted.get('phone') else 'N/A'}")
                        
                        with col2:
                            st.write(f"**Skills:** {len(extracted.get('skills', []))} found")
                            st.write(f"**Experience:** {len(extracted.get('experience', []))} positions")
                            st.write(f"**Education:** {len(extracted.get('education', []))} entries")
                        
                        # Next steps
                        st.markdown("---")
                        st.markdown("### 📊 Next Steps")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            if st.button("📊 View Full Analysis", use_container_width=True):
                                st.switch_page("pages/3_analysis.py")
                        
                        with col2:
                            if st.button("🤖 Get AI Feedback", use_container_width=True):
                                st.switch_page("pages/4_feedback.py")
                        
                        with col3:
                            if st.button("🎯 Career Insights", use_container_width=True):
                                st.switch_page("pages/5_insights.py")
                    
                    else:
                        st.error(f"❌ Error: {response.text}")
                
                except Exception as e:
                    st.error(f"❌ Error processing resume: {str(e)}")
    
    else:
        # Empty state
        st.markdown("""
        <div style='text-align: center; padding: 60px 20px; background: #f0f2f6; border-radius: 10px;'>
            <h3>📄 No file selected</h3>
            <p style='color: #666;'>Drag and drop your resume above or click to browse</p>
            <p style='color: #999; font-size: 0.9em;'>Supported formats: PDF, DOCX, DOC (Max 10MB)</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tips section
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        - **Clear Format:** Use standard fonts and consistent formatting
        - **Complete Info:** Include all contact information (email, phone, LinkedIn, GitHub)
        - **Quantifiable Achievements:** Add metrics and results to your experience
        - **Keywords:** Include relevant technical keywords for your industry
        - **ATS Compatible:** Avoid tables, images, and unusual formatting for ATS compatibility
        - **Recent Updates:** Keep your resume current with recent projects and skills
        """)
