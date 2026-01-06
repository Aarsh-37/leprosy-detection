import os
import pandas as pd
import json
import tensorflow as tf
from tensorflow.keras.applications import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Configurations - use absolute paths to avoid file saving issues
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "../../data")
TRAIN_CSV = os.path.join(DATA_DIR, "train/_annotations.csv")
VALID_CSV = os.path.join(DATA_DIR, "valid/_annotations.csv")
TRAIN_IMG_DIR = os.path.join(DATA_DIR, "train")
VALID_IMG_DIR = os.path.join(DATA_DIR, "valid")
SAVED_MODELS_DIR = os.path.join(SCRIPT_DIR, "../saved_models")
MODEL_SAVE_PATH = os.path.join(SAVED_MODELS_DIR, "leprosy_xception.keras")
CLASS_INDICES_PATH = os.path.join(SAVED_MODELS_DIR, "class_indices.json")
TARGET_SIZE = (299, 299)
BATCH_SIZE = 32
EPOCHS_HEAD = 5
EPOCHS_FINETUNE = 10

def train_model():
    # Load dataframes
    train_df = pd.read_csv(TRAIN_CSV)
    valid_df = pd.read_csv(VALID_CSV)
    
    # Ensure class labels are consistent
    print("Classes found:", train_df['class'].unique())
    
    # Data Augmentation
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    valid_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    
    # Create generators
    train_generator = train_datagen.flow_from_dataframe(
        dataframe=train_df,
        directory=TRAIN_IMG_DIR,
        x_col="filename",
        y_col="class",
        target_size=TARGET_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    valid_generator = valid_datagen.flow_from_dataframe(
        dataframe=valid_df,
        directory=VALID_IMG_DIR,
        x_col="filename",
        y_col="class",
        target_size=TARGET_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )
    
    # Save class indices
    os.makedirs(os.path.dirname(CLASS_INDICES_PATH), exist_ok=True)
    with open(CLASS_INDICES_PATH, 'w') as f:
        # Inverting the dictionary for easier lookup: {0: "Lep", 1: "Non Lep"}
        inv_map = {v: k for k, v in train_generator.class_indices.items()}
        json.dump(inv_map, f)
        
    num_classes = len(train_generator.class_indices)
    
    # Build Model
    base_model = Xception(weights='imagenet', include_top=False, input_shape=(299, 299, 3))
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Phase 1: Train only the head
    print("Starting Phase 1: Training the head...")
    for layer in base_model.layers:
        layer.trainable = False
        
    model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])
    
    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        validation_data=valid_generator,
        validation_steps=valid_generator.samples // BATCH_SIZE,
        epochs=EPOCHS_HEAD
    )
    
    # Phase 2: Fine-tuning
    print("Starting Phase 2: Fine-tuning...")
    # Unfreeze the top layers of the base model
    for layer in base_model.layers[-20:]: # Unfreeze last 20 layers
        layer.trainable = True
        
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    
    model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // BATCH_SIZE,
        validation_data=valid_generator,
        validation_steps=valid_generator.samples // BATCH_SIZE,
        epochs=EPOCHS_FINETUNE
    )
    
    # Save model with proper path handling
    save_dir = os.path.normpath(SAVED_MODELS_DIR)
    save_path = os.path.normpath(MODEL_SAVE_PATH)
    os.makedirs(save_dir, exist_ok=True)
    
    # Check disk space before saving
    import shutil
    stat = shutil.disk_usage(save_dir)
    free_gb = stat.free / (1024**3)
    print(f"Available disk space: {free_gb:.2f} GB")
    
    if free_gb < 1.0:
        print(f"WARNING: Low disk space ({free_gb:.2f} GB). Model saving may fail.")
        print("Consider freeing up disk space or changing save location.")
    
    print(f"Saving model to: {save_path}")
    
    # Try multiple saving methods
    saved_successfully = False
    
    # Method 1: Native Keras format with compression
    try:
        print("Attempting to save in native Keras format...")
        model.save(save_path, save_format='keras')
        print(f"✓ Model saved successfully to {save_path}")
        saved_successfully = True
    except Exception as e:
        print(f"✗ Error saving in Keras format: {e}")
    
    # Method 2: TensorFlow SavedModel format (more reliable for large models)
    if not saved_successfully:
        try:
            tf_save_path = os.path.join(save_dir, "leprosy_xception_tf")
            print(f"Attempting to save in TensorFlow SavedModel format to {tf_save_path}...")
            model.save(tf_save_path, save_format='tf')
            print(f"✓ Model saved successfully to {tf_save_path}")
            saved_successfully = True
        except Exception as e:
            print(f"✗ Error saving in TF format: {e}")
    
    # Method 3: Weights only (lightest option)
    if not saved_successfully:
        try:
            weights_path = os.path.join(save_dir, "leprosy_xception_weights.h5")
            print(f"Attempting to save weights only to {weights_path}...")
            model.save_weights(weights_path)
            # Also save the model architecture
            architecture_path = os.path.join(save_dir, "leprosy_xception_architecture.json")
            with open(architecture_path, 'w') as f:
                f.write(model.to_json())
            print(f"✓ Weights saved to {weights_path}")
            print(f"✓ Architecture saved to {architecture_path}")
            print("NOTE: You'll need to reconstruct the model from architecture + weights when loading")
        except Exception as e:
            print(f"✗ CRITICAL: All save methods failed: {e}")
            raise

if __name__ == "__main__":
    train_model()
