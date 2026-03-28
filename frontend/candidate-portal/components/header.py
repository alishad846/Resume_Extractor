"""Header component for Streamlit app."""

import base64
import streamlit as st
from pathlib import Path


def render_header():
    """Render application header with branding."""
    
    assets_dir = Path(__file__).resolve().parent.parent / "assets"
    logo_svg = assets_dir / "logo.svg"
    logo_png = assets_dir / "logo.png"

    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if logo_png.exists():
            st.image(str(logo_png), width=80, use_column_width=False)
        elif logo_svg.exists():
            encoded = base64.b64encode(logo_svg.read_bytes()).decode("utf-8")
            st.markdown(
                f"<img src='data:image/svg+xml;base64,{encoded}' width='80' style='border-radius:6px;'>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)  # placeholder
    
    with col2:
        st.markdown("""
        <h1 style='text-align: center; color: #1f77b4; margin: 0; padding: 10px 0;'>
            📄 Resume AI Platform
        </h1>
        <p style='text-align: center; color: #666; margin: 0;'>
            Advanced Resume Processing & Career Intelligence
        </p>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.session_state.user:
            st.write(f"👤 {st.session_state.user['name']}")
        else:
            st.write("👤 Guest")
    
    st.markdown("---")
