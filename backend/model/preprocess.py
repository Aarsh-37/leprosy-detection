import cv2
import numpy as np

def read_image(file_bytes):
    """
    Load image from bytes.
    """
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

def preprocess_for_model(img, target_size=(299, 299)):
    """
    Resize to Xception input size, normalize, and convert color channels if needed.
    Xception expects input in range [-1, 1].
    """
    # Convert BGR (OpenCV default) to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Resize
    img_resized = cv2.resize(img_rgb, target_size)
    
    # Normalize to [-1, 1] as expected by Xception
    img_normalized = (img_resized.astype(np.float32) / 127.5) - 1.0
    
    return img_normalized
