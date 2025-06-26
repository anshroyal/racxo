from rembg import remove, new_session
from PIL import Image
import io

# process.py

import cv2
import numpy as np
import io

def remove_img(image_bytes):
    """
    Remove background using OpenCV’s GrabCut.
    Input: raw image bytes
    Output: PNG bytes with background removed
    """
    # Decode image bytes to OpenCV format
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image")

    # Prepare mask and models for GrabCut
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    # Define a rectangle that’s inset a bit from the borders
    h, w = img.shape[:2]
    rect = (10, 10, w - 20, h - 20)

    # Run GrabCut
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

    # Create mask where sure/likely foreground
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img_nobg = img * mask2[:, :, np.newaxis]

    # Encode back to PNG bytes
    success, encoded = cv2.imencode('.png', img_nobg)
    if not success:
        raise RuntimeError("Failed to encode image")

    return encoded.tobytes()

