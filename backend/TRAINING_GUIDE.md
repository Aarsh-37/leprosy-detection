# Model Training Guide

## ✅ SAFE TRAINING (RECOMMENDED)

Use this method - it automatically handles everything:

```powershell
cd C:\Users\VICTUS\LeprosyDetection\backend
python train_safe.py
```

### What it does:
1. ✓ Checks disk space on C: and E: drives
2. ✓ Chooses the best save location automatically
3. ✓ Uses the triple-failover system (3 save methods)
4. ✓ Creates automatic backups on both drives
5. ✓ Copies files to the right location for your app

**You can't lose your model with this approach!**

---

## Standard Training (Original)

```powershell
cd C:\Users\VICTUS\LeprosyDetection\backend\model
python train.py
```

This works fine if you have enough space on C: drive (you have 9.37 GB now, which is enough).

---

## What Happens During Training

### Phase 1: Head Training (5 epochs)
- Trains only the custom classification layers
- Takes ~5-10 minutes

### Phase 2: Fine-tuning (10 epochs)
- Fine-tunes the last 20 layers
- Takes ~15-25 minutes

**Total time: ~20-35 minutes**

---

## After Training Completes

You'll see one of these saved:

### Best Case (Preferred)
```
saved_models/
├── leprosy_xception.keras  ← Main model file
└── class_indices.json       ← Class labels
```

### Fallback Case
```
saved_models/
├── leprosy_xception_tf/     ← TensorFlow SavedModel folder
└── class_indices.json
```

### Emergency Case (if disk was tight)
```
saved_models/
├── leprosy_xception_weights.h5        ← Model weights
├── leprosy_xception_architecture.json ← Model structure
└── class_indices.json
```

**All formats work perfectly!** Your app will automatically load whichever format is available.

---

## Monitoring Training Progress

The training will show:
- Current epoch number
- Training accuracy & loss
- Validation accuracy & loss
- Time per epoch

Example output:
```
Epoch 1/5
45/45 [==============================] - 120s 3s/step - loss: 0.4234 - accuracy: 0.8123 - val_loss: 0.3456 - val_accuracy: 0.8567
```

---

## Disk Space Requirements

- **Minimum needed**: ~500 MB
- **Recommended**: 2-5 GB free
- **Your current space**: 
  - C: drive: 9.37 GB ✓
  - E: drive: 113.71 GB ✓

**You're good to go!**

---

## Troubleshooting

### If training fails:
1. Check disk space: `Get-Volume C, E`
2. Make sure data files exist in `data/train/` and `data/valid/`
3. Check the error message - it will tell you exactly what's wrong

### If model saving fails:
- Don't worry! The safe training script has multiple fallbacks
- At minimum, you'll get the weights file (60 MB)
- You can still use the model for predictions

### To verify model after training:
```powershell
python verify_model.py
```

---

## Quick Start (TL;DR)

```powershell
# Navigate to backend folder
cd C:\Users\VICTUS\LeprosyDetection\backend

# Run safe training (recommended)
python train_safe.py

# Wait 20-35 minutes for training to complete

# Verify it worked
python verify_model.py
```

**That's it!** Your model will be trained and ready to use.
