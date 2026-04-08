# utils/feature_extractor.py
import numpy as np
import librosa

def extract_features(signal, sr=22050):
    try:
        # === MFCC ===
        mfccs = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=40)

        # === Zero-Crossing Rate ===
        zcr = librosa.feature.zero_crossing_rate(y=signal)

        # === Root Mean Square Energy ===
        rms = librosa.feature.rms(y=signal)

        # === Chroma STFT ===
        chroma = librosa.feature.chroma_stft(y=signal, sr=sr)

        # === Combine all features ===
        # Ensure they have the same time axis (2nd dimension)
        min_frames = min(mfccs.shape[1], zcr.shape[1], rms.shape[1], chroma.shape[1])
        mfccs = mfccs[:, :min_frames]
        zcr = zcr[:, :min_frames]
        rms = rms[:, :min_frames]
        chroma = chroma[:, :min_frames]

        combined = np.vstack([mfccs, zcr, rms, chroma])  # shape = (num_features, time_steps)
        return combined

    except Exception as e:
        print(f"[Feature Extraction Error] {str(e)}")
        return None
