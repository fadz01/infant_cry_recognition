# utils/audio_preprocess.py
import numpy as np
import librosa
import noisereduce as nr

SAMPLE_RATE = 22050        # Audio sampling rate
MAX_DURATION = 3           # Maximum duration in seconds
MAX_LENGTH = SAMPLE_RATE * MAX_DURATION  # Maximum number of samples

def clean_audio(file_path):
    try:
        # Load the audio file
        signal, _ = librosa.load(file_path, sr=SAMPLE_RATE)

        # Check for non-silent signal
        if signal is None or len(signal) == 0 or np.max(np.abs(signal)) == 0:
            return None

        # Normalise amplitude
        signal = signal / np.max(np.abs(signal))

        # Apply noise reduction
        signal = nr.reduce_noise(y=signal, sr=SAMPLE_RATE)

        # Trim leading/trailing silence
        signal, _ = librosa.effects.trim(signal)

        # Ensure consistent length
        if len(signal) > MAX_LENGTH:
            signal = signal[:MAX_LENGTH]
        else:
            signal = np.pad(signal, (0, MAX_LENGTH - len(signal)))

        return signal

    except Exception as e:
        print(f"Audio processing error: {str(e)}")
        return None
