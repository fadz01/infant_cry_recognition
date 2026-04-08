import streamlit as st
from pathlib import Path
import base64
import os
import streamlit.components.v1 as components

# --- Page Configuration ---
st.set_page_config(page_title="BabyCorp AI", page_icon="👶", layout="wide")

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

# --- Background Setup (optional, can skip if using full banner) ---
def setup_background():
    bg_path = Path(__file__).parent / "assets" / "background.jpeg"
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

# --- Fullscreen Rotating Hero Banner ---
def show_slideshow():
    banner_folder = Path(__file__).parent / "assets" / "banners"
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
    var slideIndex = 0;
    carousel();
    function carousel() {{
        var i;
        var slides = document.getElementsByClassName("mySlides");
        for (i = 0; i < slides.length; i++) {{
            slides[i].style.display = "none";
        }}
        slideIndex++;
        if (slideIndex > slides.length) {{ slideIndex = 1 }}
        slides[slideIndex-1].style.display = "block";
        setTimeout(carousel, 3000);
    }}
    </script>
    """
    components.html(html_code, height=620)


# --- Welcome Section ---
def show_welcome():
    logo_path = Path(__file__).parent / "assets" / "babycorp_logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_encoded = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <div style="text-align:center; margin-top:2rem;">
                    <img src="data:image/png;base64,{logo_encoded}" style="height:160px; border-radius:15px;" />
                    <h1 style="color:#0f006f; margin-top: 1rem;">👶Welcome to BabyCry Recognition👶</h1>
                    <p style="font-size: 1.1rem; color:#444;">Use the sidebar to start analyzing baby cries with AI</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<hr><p style='text-align:center;'>Made with ❤️ by BabyCorp AI | For educational use</p>", unsafe_allow_html=True)


# --- Run Sections ---
setup_background()      # optional
show_slideshow()        # fullscreen rotating ad
show_welcome()          # BabyCorp logo + text
