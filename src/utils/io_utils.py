import os
import hashlib
import imageio
import cv2
from pathlib import Path
from typing import List


def file_hash(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_frames(video_path: str, out_dir: str, fps: int = 1) -> List[str]:
    """Extract frames using OpenCV at a sampling FPS. Returns list of file paths."""
    os.makedirs(out_dir, exist_ok=True)
    vid = cv2.VideoCapture(video_path)
    if not vid.isOpened():
        raise IOError(f"Cannot open video: {video_path}")
    orig_fps = vid.get(cv2.CAP_PROP_FPS) or 25
    step = max(1, int(orig_fps // fps))
    frames = []
    idx = 0
    saved = 0
    while True:
        ret, frame = vid.read()
        if not ret:
            break
        if idx % step == 0:
            out_path = os.path.join(out_dir, f"frame_{saved:06d}.jpg")
            cv2.imwrite(out_path, frame)
            frames.append(out_path)
            saved += 1
        idx += 1
    vid.release()
    return frames


def load_image(path: str):
    im = imageio.imread(path)
    if im.ndim == 2:
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2RGB)
    elif im.shape[2] == 4:
        im = cv2.cvtColor(im, cv2.COLOR_RGBA2RGB)
    return im