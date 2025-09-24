import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import torch

# --------------------------
# DEVICE SELECTION: for future torch-based fusion (optional)
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"FusionModel running on {device}")
# --------------------------

class FusionModel:
    def __init__(self, model_path=None):
        self.device = device
        self.model = GradientBoostingClassifier()
        if model_path:
            self.model = joblib.load(model_path)

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict(self, X):
        return self.model.predict_proba(X)[:, 1]

    def save(self, path):
        joblib.dump(self.model, path)