"""
Safe training wrapper with automatic backup to E: drive
This ensures your model is saved even if C: drive has issues
"""
import os
import sys
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("SAFE MODEL TRAINING - With Automatic Backup")
print("=" * 70)

# Check disk space on both drives
def check_disk_space():
    c_stat = shutil.disk_usage("C:/")
    c_free_gb = c_stat.free / (1024**3)
    
    e_stat = shutil.disk_usage("E:/")
    e_free_gb = e_stat.free / (1024**3)
    
    print(f"\nDisk Space Check:")
    print(f"  C: drive - {c_free_gb:.2f} GB free")
    print(f"  E: drive - {e_free_gb:.2f} GB free")
    
    return c_free_gb, e_free_gb

c_free, e_free = check_disk_space()

# Determine primary save location
if c_free >= 5.0:
    print(f"\n✓ C: drive has sufficient space ({c_free:.2f} GB)")
    print("  Will save to C: drive (default location)")
    use_backup = True
else:
    print(f"\n⚠ C: drive is low on space ({c_free:.2f} GB)")
    print("  Will save ONLY to E: drive (safer)")
    use_backup = False
    
    # Modify the model save path to use E: drive
    from model import train
    train.SAVED_MODELS_DIR = "E:/LeprosyModels"
    train.MODEL_SAVE_PATH = os.path.join(train.SAVED_MODELS_DIR, "leprosy_xception.keras")
    train.CLASS_INDICES_PATH = os.path.join(train.SAVED_MODELS_DIR, "class_indices.json")
    print(f"  Modified save location to: {train.SAVED_MODELS_DIR}")

print("\n" + "=" * 70)
print("Starting Training...")
print("=" * 70)

# Import and run training
from model.train import train_model

try:
    train_model()
    
    # If we used E: drive, copy back to C: drive for the application
    if not use_backup:
        print("\n" + "=" * 70)
        print("Creating backup on C: drive for application use...")
        print("=" * 70)
        
        src_dir = "E:/LeprosyModels"
        dst_dir = "./saved_models"
        
        os.makedirs(dst_dir, exist_ok=True)
        
        # Copy all model files
        for filename in os.listdir(src_dir):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(dst_dir, filename)
            
            if os.path.isfile(src_file):
                print(f"  Copying {filename}...")
                shutil.copy2(src_file, dst_file)
        
        print("\n✓ Backup complete! Model files copied to C: drive")
    
    # If we saved to C: drive, create backup on E: drive
    elif use_backup and e_free >= 1.0:
        print("\n" + "=" * 70)
        print("Creating safety backup on E: drive...")
        print("=" * 70)
        
        backup_dir = "E:/LeprosyModels_Backup"
        os.makedirs(backup_dir, exist_ok=True)
        
        src_dir = "./saved_models"
        
        for filename in os.listdir(src_dir):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(backup_dir, filename)
            
            if os.path.isfile(src_file):
                print(f"  Backing up {filename}...")
                shutil.copy2(src_file, dst_file)
        
        print(f"\n✓ Backup complete! Safety copy saved to {backup_dir}")
    
    print("\n" + "=" * 70)
    print("✓ SUCCESS! Training completed and model saved safely!")
    print("=" * 70)
    print("\nModel locations:")
    print(f"  Primary: ./backend/saved_models/")
    if use_backup:
        print(f"  Backup:  E:/LeprosyModels_Backup/")
    else:
        print(f"  Primary: E:/LeprosyModels/")
        print(f"  Backup:  ./backend/saved_models/")
    
except Exception as e:
    print("\n" + "=" * 70)
    print(f"✗ ERROR: Training failed")
    print("=" * 70)
    print(f"\nError details: {e}")
    raise
