import cv2
import numpy as np
import mediapipe as mp
from typing import Tuple

mp_face = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh


def detect_and_align(image: np.ndarray, desired_size: Tuple[int, int] = (299, 299)) -> Tuple[np.ndarray, dict]:
    """Detects the largest face using MediaPipe and aligns it roughly using eye centers. Returns aligned face and metadata."""
    with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as fd:
        results = fd.process(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        if not results.detections:
            raise ValueError("No face detected")
        # pick the largest detection
        det = max(results.detections, key=lambda d: d.location_data.relative_bounding_box.width * d.location_data.relative_bounding_box.height)
        bbox = det.location_data.relative_bounding_box
        h, w = image.shape[:2]
        x = int(bbox.xmin * w)
        y = int(bbox.ymin * h)
        bw = int(bbox.width * w)
        bh = int(bbox.height * h)
        # pad
        pad = int(0.2 * max(bw, bh))
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(w, x + bw + pad)
        y1 = min(h, y + bh + pad)
        face = image[y0:y1, x0:x1]
        face = cv2.resize(face, desired_size)
        meta = {"bbox": (x0, y0, x1, y1)}
        return face, meta


def get_landmarks(image: np.ndarray) -> np.ndarray:
    """Return 468 face landmarks (x, y) normalized to image size."""
    with mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True) as fm:
        res = fm.process(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        if not res.multi_face_landmarks:
            raise ValueError("No face landmarks detected")
        lm = res.multi_face_landmarks[0]
        pts = [(p.x * image.shape[1], p.y * image.shape[0]) for p in lm.landmark]
        return np.array(pts)