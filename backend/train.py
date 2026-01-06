import os
import sys
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("SAFE MODEL TRAINING - GitHub Compatible")
print("=" * 70)

# ---------------- CONFIG ---------------- #
PRIMARY_MODEL_DIR = os.getenv(
    "PRIMARY_MODEL_DIR",
    os.path.join(os.getcwd(), "saved_models")
)

BACKUP_MODEL_DIR = os.getenv(
    "BACKUP_MODEL_DIR",
    None  # e.g. "/mnt/backup/LeprosyModels"
)
# ---------------------------------------- #

def check_disk_space(path):
    try:
        stat = shutil.disk_usage(path)
        return stat.free / (1024 ** 3)
    except FileNotFoundError:
        return None

print("\nDisk Space Check:")
primary_free = check_disk_space(PRIMARY_MODEL_DIR)

if primary_free is not None:
    print(f"  Primary location: {PRIMARY_MODEL_DIR}")
    print(f"  Free space: {primary_free:.2f} GB")
else:
    print(f"  Primary location does not exist yet.")

if BACKUP_MODEL_DIR:
    backup_free = check_disk_space(BACKUP_MODEL_DIR)
    if backup_free is not None:
        print(f"  Backup location: {BACKUP_MODEL_DIR}")
        print(f"  Free space: {backup_free:.2f} GB")

print("\n" + "=" * 70)
print("Starting Training...")
print("=" * 70)

from model.train import train_model

try:
    train_model()

    # Backup if enabled
    if BACKUP_MODEL_DIR:
        print("\nCreating backup...")
        os.makedirs(BACKUP_MODEL_DIR, exist_ok=True)

        for filename in os.listdir(PRIMARY_MODEL_DIR):
            src = os.path.join(PRIMARY_MODEL_DIR, filename)
            dst = os.path.join(BACKUP_MODEL_DIR, filename)

            if os.path.isfile(src):
                shutil.copy2(src, dst)
                print(f"  Backed up: {filename}")

        print("✓ Backup completed successfully")

    print("\n" + "=" * 70)
    print("✓ TRAINING COMPLETED SUCCESSFULLY")
    print("=" * 70)

    print("\nModel locations:")
    print(f"  Primary: {PRIMARY_MODEL_DIR}")
    if BACKUP_MODEL_DIR:
        print(f"  Backup:  {BACKUP_MODEL_DIR}")

except Exception as e:
    print("\n" + "=" * 70)
    print("✗ TRAINING FAILED")
    print("=" * 70)
    print(f"Error: {e}")
    raise
