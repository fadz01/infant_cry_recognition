import streamlit as st
from pathlib import Path
import base64
import os
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="Home - BabyCorp Recognition", page_icon="🏠", layout="wide")

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

BASE_DIR = Path(__file__).parent.parent

# --- Background Setup ---
def setup_background():
    bg_path = BASE_DIR / "assets" / "background.jpeg"
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

# --- Welcome Section ---
def show_welcome():
    logo_path = BASE_DIR / "assets" / "babycorp_logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_encoded = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="text-align:center; margin-top:2rem;">
                <img src="data:image/png;base64,{logo_encoded}" style="height:160px; border-radius:15px;" />
                <h1 style="color:#0f006f; margin-top: 1rem;">👶Welcome to BabyCry Recognition👶</h1>
                <p style="font-size: 1.1rem; color:#444;">Empowering parents with AI to decode their baby's needs</p>
            </div>
        """, unsafe_allow_html=True)

# --- Fullscreen Rotating Hero Banner ---
def show_slideshow():
    banner_folder = BASE_DIR / "assets" / "home_ads"
    image_files = sorted([f for f in os.listdir(banner_folder) if f.endswith((".png", ".jpg", ".jpeg"))])

    if not image_files:
        return

    img_tags = ""
    for f in image_files:
        img_path = banner_folder / f
        with open(img_path, "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
            img_tags += f'''
                <img class="mySlides" src="data:image/png;base64,{img_data}"
                style="width:100%; height:80vh; object-fit:cover; display:none;
                       margin:0 auto; border-radius: 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.2);" />
            '''

    html_code = f"""
    <style>
        .slideshow-container {{
            width: 100%;
            max-width: 1300px;
            margin: 0 auto;
            overflow: hidden;
            padding-top: 1rem;
        }}
    </style>
    <div class="slideshow-container">
        {img_tags}
    </div>
    <script>
    let slideIndex = 0;
    function carousel() {{
        const slides = document.getElementsByClassName("mySlides");
        for (let i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
        }}
        slideIndex++;
        if (slideIndex > slides.length) {{ slideIndex = 1; }}
        slides[slideIndex-1].style.display = "block";
        setTimeout(carousel, 3000);
    }}
    window.onload = carousel;
    </script>
    """
    components.html(html_code, height=620)

# --- Feature Cards with Pop Effect ---
def display_feature_cards():
    st.markdown("""
        <style>
        .feature-grid {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin-top: 3rem;
        }
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 20px;
            width: 280px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 6px 16px rgba(0,0,0,0.08);
            text-align: center;
        }
        .feature-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        }
        .feature-card h3 {
            margin-top: 1rem;
            color: #2c3e50;
        }
        .feature-card p {
            color: #555;
        }
        @media (max-width: 768px) {
            .feature-grid {
                flex-direction: column;
                align-items: center;
            }
        }
        </style>
        <div class="feature-grid">
            <div class="feature-card">
                <h3>🎤 Analyze Cry</h3>
                <p>Get real-world interpretation of your baby's cry and suggested care actions.</p>
                <p>Record or Upload: Click the "Upload" button to provide a cry sample (WAV or MP3 format).</p>
                <p>Analyze: The AI will classify the cry (hunger, discomfort, pain, etc.) in seconds.</p>
                <p>Get Care Tips: View suggested actions</p>
            </div>
            <div class="feature-card">
                <h3>📜 History Tracker</h3>
                <p>View past predictions and learn your baby’s behaviour patterns over time.</p>
                <p>Helps track and recall all past results.</p>
                <p>More easy and manageable for future work</p>
            </div>
            <div class="feature-card">
                <h3>ℹ️ About Project</h3>
                <p>Mission: Learn how BabyCorp AI uses research to decode infant cries.</p>
                <p>Vision: To become a leading digital companion in early child care.</p>
                <p>Let's know the origin history of the project development</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Navigation Instruction ---
def display_navigation_guide():
    st.markdown("""
        <div style="text-align:center; margin-top:3rem;">
            <h2 style="color:#2c3e50;">🧱 Navigate the App</h2>
            <p style="font-size:1.1rem; color:#555;">
                Use the sidebar on the left to explore features like Analyzer, History, or About.<br>
                Start your baby's emotional insight journey now!
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- Footer ---
def display_footer():
    st.markdown("""
        <div style="text-align:center; margin-top:4rem; color:#888;">
            <hr style="max-width:300px; margin:2rem auto;" />
            <p style="font-size:0.95rem;">Made with ❤️ by <strong>BabyCorp AI</strong> | For educational use</p>
        </div>
    """, unsafe_allow_html=True)

# --- Main Entry Point ---
def main():
    setup_background()
    show_welcome()
    display_feature_cards()
    show_slideshow()
    display_navigation_guide()
    display_footer()

if __name__ == "__main__":
    main()
