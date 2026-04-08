import streamlit as st
import base64
from pathlib import Path

# Page configuration MUST be the first Streamlit command
st.set_page_config(page_title="About - BabyCorp AI: BabyCry Recognition", page_icon="ℹ️", layout="wide")

from utils.style_utils import apply_background
apply_background()

BASE_DIR = Path(__file__).parent.parent

# --- Custom Sidebar Title ---
st.markdown("""
    <style>
        [data-testid="stSidebar"]::before {
            content: "👶 BabyCorp AI 👶";
            display: block;
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            padding: 1rem 0 0.5rem 0;
            color: #0f006f;
        }
    </style>
""", unsafe_allow_html=True)

# --- UiTM Logo Section ---
def get_uitm_logo_html():
    logo_path = BASE_DIR / "assets" / "uitm_logo.jpg"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"""
        <div style="text-align:center; margin-top:3rem;">
            <img src="data:image/jpeg;base64,{encoded}" 
                 style="max-width:280px; border-radius:12px; box-shadow:0 6px 16px rgba(0,0,0,0.15);" 
                 alt="UiTM Logo" />
            <p style="margin-top:0.5rem; font-size:1rem; color:#555;">Universiti Teknologi MARA (UiTM), Shah Alam</p>
            <p style="font-size:0.95rem; color:#777;">40450 Shah Alam, Selangor, Malaysia</p>
        </div>
        """
    return "<p style='color:red;'>⚠️ UiTM logo not found in assets folder.</p>"

# --- Main Page ---
def main():

    # Title
    st.markdown("""
        <h1 style='text-align: center; font-size: 3rem; margin-top: 1rem; color: #2c3e50;'>📝 About the BabyCorp AI: BabyCry Recognition Website</h1>
    """, unsafe_allow_html=True)

    # Description Container
    st.markdown("""
        <style>
            .about-container {
                background-color: #ffffffdd;
                padding: 2rem;
                margin: 2rem auto;
                max-width: 1100px;
                border-radius: 18px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                font-family: 'Segoe UI', sans-serif;
            }
            .about-container h3 {
                color: #2c3e50;
                font-size: 1.5rem;
                margin-top: 2rem;
            }
            .about-container p {
                color: #444;
                font-size: 1.1rem;
                line-height: 1.7;
                margin-bottom: 1rem;
            }
            .about-container ul {
                font-size: 1.05rem;
                padding-left: 1.5rem;
                color: #555;
            }
        </style>

        <div class="about-container">

        <p><strong>BabyCorp AI </strong> is an intelligent web application designed to help parents and caregivers understand the emotional and physical needs of their infants through AI-powered cry analysis. By analysing the acoustic patterns of a baby's cry, the system can detect potential causes such as hunger, tiredness, discomfort, burping, or belly pain. This tool bridges the communication gap between babies and their caretakers, offering a reassuring level of support especially for first-time parents.</p>

        <p>The website is built with simplicity, responsiveness, and care in mind. It features:</p>

        <ul>
            <li>A cry <strong>Analyzer</strong> that gives real-world predictions and smart caregiving tips.</li>
            <li>A <strong>History</strong> tracker to monitor and review past cry analyses.</li>
            <li>A detailed <strong>About</strong> section that explains the project’s origin and goals.</li>
            <li>A soft, friendly interface that aligns with the needs of young parents.</li>
        </ul>

        <h3>🎯 Project Objectives</h3>
        <ul>
            <li>To develop a deep learning model capable of classifying various types of infant cries with high accuracy.</li>
            <li>To use Mel Spectrograms and audio preprocessing techniques to extract meaningful sound features.</li>
            <li>To create a web-based interface that allows parents to easily upload and analyse their baby's cries.</li>
            <li>To provide actionable caregiving suggestions based on the classification results.</li>
            <li>To support new parents in understanding their baby’s non-verbal cues more confidently.</li>
        </ul>

        <h3>🚀 Mission</h3>
        <p>To empower parents and caregivers with intelligent tools that translate infant cries into understandable needs, fostering better infant care and stronger emotional bonding.</p>

        <h3>👁️‍🗨️ Vision</h3>
        <p>To become a leading digital companion in early child care, offering trustworthy, AI-assisted insights that make parenting more informed, responsive, and emotionally attuned.</p>

        </div>
    """, unsafe_allow_html=True)

    # UiTM Logo
    st.markdown(get_uitm_logo_html(), unsafe_allow_html=True)

    # Special Thanks
    st.markdown("""
        <div style="max-width: 800px; margin: 3rem auto 0; padding: 1rem; text-align: center;">
            <h3 style="color: #2c3e50;">🙏 Special Thanks</h3>
            <p style="font-size: 1.05rem; color: #444;">
                I would like to express my deepest gratitude to <strong>Dr. Nor Nadiah Binti Yusof</strong> 
                for her invaluable guidance, supervision, and encouragement throughout this project.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Profile Picture
    profile_path = BASE_DIR / "assets" / "profile.jpg"
    if profile_path.exists():
        with open(profile_path, "rb") as f:
            encoded_profile = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="text-align:center; margin-top:0.5rem;">
                <img src="data:image/jpg;base64,{encoded_profile}" 
                     style="height:160px; border-radius:50%; box-shadow:0 4px 10px rgba(0,0,0,0.15);" 
                     alt="Profile Picture"/>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ profile.jpeg not found in assets folder.")

    # Contact Email
    st.markdown("""
        <div style="text-align:center; margin-top:2rem;">
            <p style="font-size: 1.05rem; color: #2c3e50;">
                📬 <strong>Contact:</strong> 
                <a href="mailto:nurulfadzlin478@gmail.com" style="color:#0a66c2;">nurulfadzlin478@gmail.com</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div style="text-align:center; margin-top:3rem; padding:1rem 0; color:#888; font-size:0.95rem;">
            <hr style="max-width:300px; margin: 2rem auto;" />
            <p>Made with ❤️ by <strong>BabyCorp AI</strong> | Final Year Project | UiTM Shah Alam</p>
            <p style="font-size:0.9rem;">© 2025 BabyCry Analyzer. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
