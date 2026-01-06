import os
import json
import tensorflow as tf
from .preprocess import read_image, preprocess_for_model

SAVED_MODELS_DIR = os.path.join(os.path.dirname(__file__), "../saved_models")
MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "leprosy_xception.keras")
CLASS_LABELS_PATH = os.path.join(SAVED_MODELS_DIR, "class_indices.json")

# Global variables to store the loaded model and labels
_model = None
_labels = None

def load_model_flexible():
    """Load model from multiple possible formats"""
    # Try method 1: Native Keras format
    if os.path.exists(MODEL_PATH):
        try:
            print(f"Loading model from {MODEL_PATH}...")
            return tf.keras.models.load_model(MODEL_PATH)
        except Exception as e:
            print(f"Failed to load Keras format: {e}")
    
    # Try method 2: TensorFlow SavedModel format
    tf_model_path = os.path.join(SAVED_MODELS_DIR, "leprosy_xception_tf")
    if os.path.exists(tf_model_path):
        try:
            print(f"Loading model from TensorFlow SavedModel format: {tf_model_path}...")
            return tf.keras.models.load_model(tf_model_path)
        except Exception as e:
            print(f"Failed to load TF format: {e}")
    
    # Try method 3: Reconstruct from weights + architecture
    weights_path = os.path.join(SAVED_MODELS_DIR, "leprosy_xception_weights.h5")
    architecture_path = os.path.join(SAVED_MODELS_DIR, "leprosy_xception_architecture.json")
    
    if os.path.exists(weights_path) and os.path.exists(architecture_path):
        try:
            print(f"Reconstructing model from architecture and weights...")
            with open(architecture_path, 'r') as f:
                model = tf.keras.models.model_from_json(f.read())
            model.load_weights(weights_path)
            return model
        except Exception as e:
            print(f"Failed to reconstruct from weights: {e}")
    
    raise FileNotFoundError("No valid model files found. Please train the model first.")

def load_model_and_labels():
    """
    Load the saved Xception model and class labels mapping.
    """
    global _model, _labels
    
    if _model is None:
        _model = load_model_flexible()
        print(f"Model loaded successfully")
        
    if _labels is None:
        if not os.path.exists(CLASS_LABELS_PATH):
            raise FileNotFoundError(f"Class indices file not found at {CLASS_LABELS_PATH}. Please train the model first.")
        with open(CLASS_LABELS_PATH, 'r') as f:
            # { "0": "Lep", "1": "Non Lep" }
            _labels = json.load(f)
        print(f"Labels loaded from {CLASS_LABELS_PATH}")
            
    return _model, _labels

def predict_image(image_bytes):
    """
    Read, preprocess, and predict a single image.
    """
    model, labels = load_model_and_labels()
    
    # Read image
    img = read_image(image_bytes)
    
    # Preprocess
    img_processed = preprocess_for_model(img)
    
    # Add batch dimension
    img_batch = tf.expand_dims(img_processed, axis=0)
    
    # Run prediction
    preds = model.predict(img_batch)[0]
    
    # Format response
    probabilities = {}
    for i, prob in enumerate(preds):
        label = labels.get(str(i), f"Class {i}")
        probabilities[label] = float(prob)
        
    predicted_class_idx = tf.argmax(preds).numpy()
    predicted_class = labels.get(str(predicted_class_idx), f"Class {predicted_class_idx}")
    
    return predicted_class, probabilities
