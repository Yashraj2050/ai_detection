import torch
import torch.nn as nn
import torchvision.transforms as T
import timm
import numpy as np
from PIL import Image

# --------------------------
# DEVICE SELECTION: MPS (Apple GPU) or CPU fallback
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"ArtifactDetector running on {device}")
# --------------------------

class ArtifactDetector(nn.Module):
    def __init__(self, model_name='tf_efficientnet_b3_ns', pretrained=True, n_classes=1):
        super().__init__()
        self.backbone = timm.create_model(model_name, pretrained=pretrained, features_only=False)
        in_ch = self.backbone.get_classifier().in_features if hasattr(self.backbone, 'get_classifier') else self.backbone.num_features
        self.backbone.reset_classifier(0)
        self.head = nn.Sequential(
            nn.Linear(in_ch, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, n_classes),
            nn.Sigmoid()
        )

    def forward(self, x):
        feats = self.backbone.forward_features(x) if hasattr(self.backbone, 'forward_features') else self.backbone(x)
        if isinstance(feats, (list, tuple)):
            feats = feats[-1]
        out = self.head(feats.flatten(1))
        return out


class ArtifactPipeline:
    def __init__(self, model_path=None):
        self.device = device
        self.model = ArtifactDetector().to(self.device)
        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        self.preprocess = T.Compose([
            T.ToPILImage(),
            T.Resize((224,224)),
            T.ToTensor(),
            T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
        ])

    def predict(self, img: np.ndarray) -> float:
        x = self.preprocess(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            out = self.model(x).cpu().numpy().ravel()[0]
        return float(out)