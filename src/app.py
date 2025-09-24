import streamlit as st
import os, tempfile
import numpy as np
import cv2
from PIL import Image
import torch

from src.utils.io_utils import extract_frames, load_image, file_hash
from src.utils.preprocessing import detect_and_align, get_landmarks
from src.detectors.ela import ela_image
from src.detectors.dct_utils import dct_magnitude_map
from src.models.artifact_detector import ArtifactPipeline
from src.models.motion_detector import MotionPipeline
from src.models.fusion import FusionModel

# --------------------------
# GLOBAL DEVICE SELECTION
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"DeepGuard app running on {device}")
# --------------------------

# Load models (they internally use device)
artifact = ArtifactPipeline(model_path='checkpoints/artifact_detector.pth')
motion = MotionPipeline(model_path='checkpoints/motion_lstm.h5')
fusion = FusionModel(model_path='checkpoints/fusion.pkl')

st.title("DeepGuard — Deepfake Detection")
uploaded_file = st.file_uploader("Upload Image or Video", type=['jpg','png','mp4','avi'])

if uploaded_file:
    temp_dir = tempfile.mkdtemp()
    path = os.path.join(temp_dir, uploaded_file.name)
    with open(path, 'wb') as f:
        f.write(uploaded_file.read())
    filehash = file_hash(path)

    if path.lower().endswith(('.jpg', '.png')):
        frames = [path]
    else:
        frames = extract_frames(path, temp_dir, fps=1)

    artifact_scores = []
    motion_scores = []

    for fpath in frames:
        img = load_image(fpath)
        try:
            face, _ = detect_and_align(img)
        except:
            continue

        # Artifact detection
        art_score = artifact.predict(face)
        artifact_scores.append(art_score)

        # Motion detection
        lms = get_landmarks(face).flatten()[:136]  # 68 points *2
        motion_scores.append(lms)

        # Visual ELA/DCT for display
        ela = ela_image(Image.fromarray(cv2.cvtColor(face, cv2.COLOR_RGB2BGR)))
        dct_map = dct_magnitude_map(face)

        st.image([face, ela, dct_map], caption=['Aligned Face', 'ELA', 'DCT Map'])

    # Prepare motion sequence prediction
    if len(motion_scores) >= 30:
        seq = np.array(motion_scores[-30:]).reshape(1,30,-1)
        motion_pred = motion.predict_sequence(seq)
    else:
        motion_pred = 0.5  # Neutral if insufficient frames

    # Combine with artifact avg score
    art_avg = float(np.mean(artifact_scores)) if artifact_scores else 0.5
    fusion_score = fusion.predict(np.array([[art_avg, motion_pred]]))[0]

    st.subheader(f"Manipulation Confidence: {fusion_score:.2f}")
    if fusion_score > 0.5:
        st.error("Likely Deepfake Detected!")
    else:
        st.success("Likely Authentic Content")

    # Optional PDF report
    if st.button("Download Report"):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        pdf_path = os.path.join(temp_dir, "report.pdf")
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(72, 750, "DeepGuard Detection Report")
        c.drawString(72, 730, f"File: {uploaded_file.name}")
        c.drawString(72, 710, f"Hash: {filehash}")
        c.drawString(72, 690, f"Artifact Avg Score: {art_avg:.2f}")
        c.drawString(72, 670, f"Motion Score: {motion_pred:.2f}")
        c.drawString(72, 650, f"Fusion Confidence: {fusion_score:.2f}")
        c.save()
        with open(pdf_path, "rb") as f:
            st.download_button("Download PDF", data=f, file_name="DeepGuard_Report.pdf")