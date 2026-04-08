import librosa
import librosa.display
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Layer
import tensorflow as tf
import matplotlib.pyplot as plt
import base64
import os
from pathlib import Path
from datetime import datetime
from utils.style_utils import apply_background
import streamlit as st

st.set_page_config(page_title="BabyCry Analyzer", page_icon="🎤", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎤 Baby Cry Recognition</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Understand your baby's needs through their cries</p>", unsafe_allow_html=True)

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

# --- PATH SETUP ---
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CUSTOM ATTENTION LAYER ---
class AttentionLayer(Layer):
    def init(self, **kwargs):
        super(AttentionLayer, self).init(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super().build(input_shape)

    def call(self, x):
        e = tf.keras.backend.tanh(tf.keras.backend.dot(x, self.W) + self.b)
        a = tf.keras.backend.softmax(e, axis=1)
        return tf.keras.backend.sum(x * a, axis=1)

# --- Mappings ---
CLASSES = ["belly pain", "burping", "discomfort", "hungry", "tired"]
EMOJIS = ["🤢", "🤱", "😣", "🍼", "😴"]
COLORS = {
    "belly pain": "#ffe5e5",
    "burping": "#e0fff8",
    "discomfort": "#e5f0ff",
    "hungry": "#fff3e5",
    "tired": "#e9fff5",
}
recommendations = {
    "belly pain": [
        "Try gentle tummy massage in a clockwise motion to ease gas.",
        "Do bicycle leg movements (move baby’s legs as if pedaling).",
        "Offer a warm compress on their tummy for a few minutes.",
        "If symptoms persist, consult your pediatrician."
    ],
    "burping": [
        "Hold baby upright against your chest and gently pat or rub their back.",
        "Try different burping positions (e.g., over shoulder or sitting upright).",
        "Burp frequently during and after feeding."
    ],
    "discomfort": [
        "Check for a wet or soiled diaper.",
        "Adjust clothing to avoid tightness or irritation.",
        "Ensure room temperature is comfortable.",
        "Look for hair wrapped around fingers or toes."
    ],
    "hungry": [
        "Look for hunger cues like rooting or sucking on hands.",
        "Offer breastfeeding or a bottle in a quiet environment.",
        "Track feeding times to anticipate hunger.",
        "Keep track of feeding times to anticipate hunger before crying starts."
    ],
    "tired": [
        "Watch for sleep cues like yawning or rubbing eyes.",
        "Create a calm, dimly lit environment.",
        "Use swaddling (if appropriate), rocking, or white noise.",
        "Establish a consistent nap/bedtime routine."
    ]
}

# --- MAIN APP ---
def main():
    try:
        model_path = BASE_DIR / "models" / "best_model1.keras"
        model = load_model(model_path, custom_objects={"AttentionLayer": AttentionLayer})
    except Exception as e:
        st.error(f"⚠️ Model loading failed: {str(e)}")
        st.stop()

    if "history" not in st.session_state:
        st.session_state.history = []

    uploaded_file = st.file_uploader("Upload baby's cry (WAV/MP3)", type=["wav", "mp3"])
    if uploaded_file:
        temp_path = BASE_DIR / "temp_audio.wav"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.audio(str(temp_path), format="audio/wav")

        try:
            with st.spinner("🔍 Analyzing..."):
                signal, sr = librosa.load(temp_path, sr=22050, duration=None)
                spec = librosa.feature.melspectrogram(y=signal, sr=sr, n_fft=2048, hop_length=256, n_mels=130, fmax=sr/2)
                log_spec = librosa.power_to_db(spec, ref=np.max)
                log_spec = (log_spec - log_spec.min()) / (log_spec.max() - log_spec.min())

                if log_spec.shape != (130, 187):
                    log_spec = librosa.util.fix_length(log_spec, size=187, axis=1)

                features = log_spec.T.reshape(1, 187, 130, 1)
                prediction = model.predict(features)
                predicted_class = np.argmax(prediction[0])
                label = CLASSES[predicted_class]
                emoji = EMOJIS[predicted_class]
                bg_color = COLORS[label]
                top3_indices = prediction[0].argsort()[-3:][::-1]
                top3 = [(EMOJIS[i], CLASSES[i].title()) for i in top3_indices]

            # Result Box and Styling
            st.markdown(f"""
                <style>
                .pulse {{
                    animation: beat 1.5s infinite;
                }}
                @keyframes beat {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.05); }}
                }}
                .big-text {{
                    font-size: 1.7rem;
                    font-weight: bold;
                    text-align: center;
                }}
                .top3-emotion {{
                    font-size: 1.2rem;
                    margin: 0.5rem 0;
                }}
                </style>
                <div class="result-box pulse" style="text-align:center;
                    background:{bg_color};
                    padding:1.5rem;
                    border-radius:15px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
                    <h2>Prediction Result</h2>
                    <h3 class="big-text">{emoji} {label.title()}</h3>
                </div>
            """, unsafe_allow_html=True)

            # Columns: Top 3 and Spectrogram
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🏆 Top 3 Likely Emotions")
                for i, (emj, lbl) in enumerate(top3, 1):
                    st.markdown(f"<div class='top3-emotion'>🔹 {i}. {emj} {lbl}</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("#### 🎵 Audio Spectrogram")
                fig, ax = plt.subplots(figsize=(6, 3))
                librosa.display.specshow(log_spec, sr=sr, hop_length=256, x_axis='time', y_axis='mel', cmap='magma')
                plt.colorbar(format='%+2.0f dB')
                st.pyplot(fig)

            # Recommendations
            st.markdown(f"""
                <div style="background:#fffbe6; padding:1rem;
                    border-left:5px solid #ffc107; border-radius:8px; margin-top:1rem;">
                    <h4>💡 Recommended Actions</h4>
                    <ul>
            """, unsafe_allow_html=True)
            for rec in recommendations[label]:
                st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)

            # Baby GIF
            gif_path = BASE_DIR / "assets" / "baby.gif"
            if gif_path.exists():
                with open(gif_path, "rb") as f:
                    encoded_gif = base64.b64encode(f.read()).decode()
                st.markdown(f"""
                    <div style='text-align:center; margin-top:1rem;'>
                        <img src='data:image/gif;base64,{encoded_gif}' style='height:150px; border-radius:10px;' />
                    </div>
                """, unsafe_allow_html=True)

            # Save history
            st.session_state.history.append({
                "file": uploaded_file.name,
                "class": label,
                "emoji": emoji,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        except Exception as e:
            st.error(f"❌ Processing error: {str(e)}")
        finally:
            if temp_path.exists():
                temp_path.unlink()

    st.markdown("<hr><p style='text-align:center;'>Made with ❤️ by BabyCorp AI | For educational use</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()