import base64
import os
from pathlib import Path
import streamlit as st

def apply_background():
    base_dir = Path(__file__).parent.parent
    bg_path = base_dir / "assets" / "background.jpeg"
    
    if bg_path.exists():
        with open(bg_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-attachment: fixed;
                background-position: center;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            </style>
        """, unsafe_allow_html=True)
