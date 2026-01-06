import os
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Configurations
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "../../data")
TEST_CSV = os.path.join(DATA_DIR, "test/_annotations.csv")
TEST_IMG_DIR = os.path.join(DATA_DIR, "test")
SAVED_MODELS_DIR = os.path.join(SCRIPT_DIR, "../saved_models")
MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "leprosy_xception.keras")
CLASS_INDICES_PATH = os.path.join(SAVED_MODELS_DIR, "class_indices.json")
TARGET_SIZE = (299, 299)
BATCH_SIZE = 32

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

def evaluate():
    # Load model and class indices
    try:
        model = load_model_flexible()
    except FileNotFoundError as e:
        print(e)
        return
        
    with open(CLASS_INDICES_PATH, 'r') as f:
        labels_map = json.load(f)
    
    # Load test data
    test_df = pd.read_csv(TEST_CSV)
    
    # Data Generator for Test
    from tensorflow.keras.applications.xception import preprocess_input
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    
    test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    
    test_generator = test_datagen.flow_from_dataframe(
        dataframe=test_df,
        directory=TEST_IMG_DIR,
        x_col="filename",
        y_col="class",
        target_size=TARGET_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )
    
    # Predictions
    print("Running predictions on test set...")
    preds = model.predict(test_generator)
    y_pred = np.argmax(preds, axis=1)
    y_true = test_generator.classes
    
    # Class names in order of indices
    class_names = [labels_map[str(i)] for i in range(len(labels_map))]
    
    # Metrics
    print("\nClassification Report:")
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    
    # Plotting
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.savefig('confusion_matrix.png')
    print("Confusion matrix saved to confusion_matrix.png")

if __name__ == "__main__":
    evaluate()
