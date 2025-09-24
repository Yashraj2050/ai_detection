import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import torch

# --------------------------
# DEVICE SELECTION: for future torch tensors if needed
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"MotionDetector running on {device}")
# --------------------------

def build_lstm(seq_len=30, n_features=136):
    model = Sequential([
        LSTM(128, return_sequences=True, input_shape=(seq_len, n_features)),
        Dropout(0.3),
        LSTM(64),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

class MotionPipeline:
    def __init__(self, model_path=None):
        self.device = device
        self.model = build_lstm()
        if model_path:
            self.model.load_weights(model_path)

    def predict_sequence(self, seq_landmarks: np.ndarray) -> float:
        # seq_landmarks: (seq_len, n_features)
        seq_landmarks = seq_landmarks.astype('float32')
        pred = self.model.predict(seq_landmarks[np.newaxis, ...])[0][0]
        return float(pred)