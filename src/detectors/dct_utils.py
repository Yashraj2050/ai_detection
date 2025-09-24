import numpy as np
import cv2


def dct_magnitude_map(img: np.ndarray, block_size: int = 8) -> np.ndarray:
    """Compute block-wise DCT magnitude map to highlight frequency anomalies."""
    if img.dtype != np.float32:
        img = img.astype(np.float32)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    H = h - (h % block_size)
    W = w - (w % block_size)
    gray = gray[:H, :W]
    mag_map = np.zeros_like(gray)
    for i in range(0, H, block_size):
        for j in range(0, W, block_size):
            block = gray[i:i+block_size, j:j+block_size]
            d = cv2.dct(block)
            mag = np.log1p(np.abs(d))
            mag_map[i:i+block_size, j:j+block_size] = mag
    # normalize
    norm = cv2.normalize(mag_map, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return norm