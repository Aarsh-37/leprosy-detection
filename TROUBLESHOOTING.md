# Troubleshooting Guide - Leprosy Detection Model

## Issue: Unable to Save Model - Disk Space Error

### Problem
Error message: `RuntimeError: Can't decrement id ref count (unable to extend file properly)`

### Root Cause
**Low disk space** on C: drive. The system currently has only **6 GB (2.54%)** free space, which is insufficient for saving large Keras models.

---

## Solutions

### Solution 1: Free Up Disk Space (RECOMMENDED)

Free up at least 5-10 GB of disk space:

1. **Empty Recycle Bin**
   - Right-click Recycle Bin → Empty Recycle Bin

2. **Run Disk Cleanup**
   ```powershell
   cleanmgr
   ```
   - Select drive C:
   - Check all boxes (Temporary files, Downloads, etc.)
   - Click OK to clean

3. **Clear Windows Update Cache**
   ```powershell
   # Run PowerShell as Administrator
   Stop-Service wuauserv
   Remove-Item C:\Windows\SoftwareDistribution\Download\* -Recurse -Force
   Start-Service wuauserv
   ```

4. **Find Large Files**
   ```powershell
   Get-ChildItem C:\ -Recurse -ErrorAction SilentlyContinue | 
   Sort-Object Length -Descending | 
   Select-Object -First 20 FullName, @{Name="SizeMB";Expression={[math]::Round($_.Length/1MB,2)}}
   ```

5. **Uninstall Unused Programs**
   - Settings → Apps → Apps & features
   - Remove programs you don't use

---

### Solution 2: Enhanced Save Logic (ALREADY IMPLEMENTED)

The training script now includes:

1. **Disk Space Check** - Warns if less than 1 GB free
2. **Multiple Save Formats** with automatic fallback:
   - **Method 1**: Native Keras format (`.keras`) - Most efficient
   - **Method 2**: TensorFlow SavedModel format - More reliable for large models
   - **Method 3**: Weights + Architecture separately - Lightest option

3. **Flexible Model Loading** - All components (train, evaluate, API) now automatically detect and load from any available format

---

## How to Train the Model

After freeing up disk space, train the model:

```powershell
cd C:\Users\VICTUS\LeprosyDetection\backend\model
python train.py
```

The script will:
1. Check available disk space
2. Train the model
3. Attempt to save using the best available method
4. Provide clear feedback on which method succeeded

---

## Verification

Check if the model was saved:

```powershell
cd C:\Users\VICTUS\LeprosyDetection\backend\saved_models
ls
```

You should see at least one of:
- `leprosy_xception.keras` (preferred)
- `leprosy_xception_tf/` (directory)
- `leprosy_xception_weights.h5` + `leprosy_xception_architecture.json`

---

## Model Loading

The application will automatically find and load the model regardless of which format was saved:

```python
from model.utils import load_model_and_labels

# This will try all formats automatically
model, labels = load_model_and_labels()
```

---

## Additional Tips

### Monitor Disk Space
```powershell
Get-Volume C | Select-Object DriveLetter, 
  @{Name="SizeGB";Expression={[math]::Round($_.Size/1GB,2)}}, 
  @{Name="FreeSpaceGB";Expression={[math]::Round($_.SizeRemaining/1GB,2)}}, 
  @{Name="PercentFree";Expression={[math]::Round(($_.SizeRemaining/$_.Size)*100,2)}}
```

### Alternative: Use External Drive
If you have limited C: drive space, consider saving models to an external drive:

```python
# In train.py, modify line 21:
MODEL_SAVE_PATH = "D:/Models/leprosy_xception.keras"  # Change to your drive
```

### Reduce Model Size
- Reduce training epochs
- Use smaller batch sizes
- Implement model quantization after training

---

## Prevention

Maintain at least **15-20% free disk space** to avoid issues:
- Set up automatic cleanup schedules
- Regularly review and remove unnecessary files
- Move large non-system files to external storage
- Use cloud storage for archives

---

## Support

If issues persist after freeing disk space:
1. Check the console output for specific error messages
2. Verify all dependencies are installed: `pip install -r requirements.txt`
3. Ensure you have write permissions to the `saved_models` directory
