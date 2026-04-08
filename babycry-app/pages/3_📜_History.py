import streamlit as st
from datetime import datetime
from utils.style_utils import apply_background

# MUST BE FIRST Streamlit COMMAND
st.set_page_config(page_title="Analysis History", page_icon="📜")

apply_background()

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

# Transparent hover-friendly color map
CATEGORY_COLORS = {
    "belly pain": "rgba(255,107,107,0.15)",
    "burping": "rgba(78,205,196,0.15)",
    "discomfort": "rgba(69,183,209,0.15)",
    "hungry": "rgba(255,160,122,0.15)",
    "tired": "rgba(152,216,200,0.15)",
}

def main():
    st.markdown("""
        <style>
        .history-box {
            border-radius: 12px;
            padding: 1.2rem;
            margin: 1rem 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .history-box:hover {
            transform: translateY(-6px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }
        </style>

        <div class="header" style="text-align:center;">
            <h1 style="font-size:2.5rem;">📜 Analysis History 📜</h1>
            <p class="subheader" style="font-size:1.1rem;">Review your previous baby cry analyses</p>
        </div>
    """, unsafe_allow_html=True)

    if "history" not in st.session_state or not any("file" in h and "time" in h for h in st.session_state.history):
        st.info("No history available yet. Analyze some cries first!")
        return

    for entry in reversed(st.session_state.history):
        if "file" not in entry or "time" not in entry:
            continue

        class_name = entry["class"].lower()
        bg_color = CATEGORY_COLORS.get(class_name, "rgba(0,0,0,0.04)")

        st.markdown(f"""
            <div class="history-box" style="background: {bg_color};">
                <h4 style="margin-bottom: 0.5rem;">{entry["emoji"]} <strong>{entry["class"].title()}</strong></h4>
                <p style="margin:0.2rem 0;"><strong>📁 File</strong>: {entry.get("file", "N/A")}</p>
                <p style="margin:0.2rem 0;"><strong>⏰ Time</strong>: {entry.get("time", "N/A")}</p>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        #st.experimental_rerun()

    st.markdown("<hr><p style='text-align:center;'>Made with ❤️ by <strong>BabyCorp AI</strong> | For educational use</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
