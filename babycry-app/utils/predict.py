import numpy as np
from tensorflow.keras.models import load_model
from .audio_preprocess import clean_audio
from .feature_extractor import extract_features

# If using AttentionLayer in model
from tensorflow.keras.layers import Layer
import tensorflow.keras.backend as K

class AttentionLayer(Layer):
    def __init__(self, **kwargs):
        super(AttentionLayer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(name="att_weight", shape=(input_shape[-1], 1), initializer="normal")
        self.b = self.add_weight(name="att_bias", shape=(input_shape[1], 1), initializer="zeros")
        super().build(input_shape)

    def call(self, x):
        e = K.tanh(K.dot(x, self.W) + self.b)
        a = K.softmax(e, axis=1)
        return K.sum(x * a, axis=1)


class CryPredictor:
    def __init__(self, model_path):
        try:
            self.model = load_model(model_path, custom_objects={"AttentionLayer": AttentionLayer})
        except:
            self.model = load_model(model_path)  # fallback if AttentionLayer not used

        self.class_names = ['belly pain', 'burping', 'discomfort', 'hungry', 'tired']
        self.max_len = 173  # or dynamically read from model input shape

    def predict(self, audio_path):
        # Step 1: Clean audio
        signal = clean_audio(audio_path)
        if signal is None:
            return {"error": "Invalid or silent audio file."}

        # Step 2: Extract features (e.g., MFCC, ZCR, RMS, Chroma)
        features = extract_features(signal)
        if features is None:
            return {"error": "Failed to extract features from audio."}

        # Step 3: Ensure consistent length (time-steps)
        if features.shape[1] < self.max_len:
            features = np.pad(features, ((0, 0), (0, self.max_len - features.shape[1])), mode='constant')
        else:
            features = features[:, :self.max_len]

        # Step 4: Add batch and channel dimension
        features = features[np.newaxis, ..., np.newaxis]

        # Step 5: Predict probabilities
        predictions = self.model.predict(features)[0]

        return {
            self.class_names[i]: float(predictions[i])
            for i in range(len(self.class_names))
        }
