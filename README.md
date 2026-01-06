# Leprosy Skin-Lesion Detection Web Application

A full-stack web application for detecting leprosy from skin lesion images using a deep learning model based on Xception architecture.

## Features

- **Deep Learning Model**: Xception-based CNN for binary classification (Leprosy vs Non-Leprosy)
- **Flask Backend**: REST API for model inference
- **React Frontend**: Modern, responsive UI for image upload and result visualization
- **Transfer Learning**: Pre-trained on ImageNet, fine-tuned on leprosy dataset
- **Evaluation Tools**: Confusion matrix and classification metrics

## Tech Stack

### Backend
- Python 3.8+
- TensorFlow/Keras
- Flask
- OpenCV
- NumPy
- Seaborn (for visualization)

### Frontend
- React (Vite)
- Axios
- CSS3

## Setup Instructions

### Backend Setup

1. **Create a virtual environment** (recommended):
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows:
   venv\\Scripts\\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the model** (optional, if model is not provided):
   ```bash
   cd model
   python train.py
   ```
   
   **Note**: Update the `DATA_DIR` path in `train.py` to point to your dataset location.

4. **Run the Flask API**:
   ```bash
   cd ..
   python app.py
   ```
   
   The API will be available at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   
   The app will be available at `http://localhost:5173`

## Usage

1. **Start the backend server** (Flask API on port 5000)
2. **Start the frontend server** (React app on port 5173)
3. **Open your browser** and navigate to `http://localhost:5173`
4. **Upload an image** of a skin lesion:
   - Drag and drop an image into the upload zone, or
   - Click to select an image from your file system
5. **Click "Analyze Lesion"** to get the prediction
6. **View the results**:
   - Predicted class (Leprosy or Non-Leprosy)
   - Confidence levels for each class
   - Medical disclaimer

## API Endpoints

### `POST /predict`
- **Description**: Predict leprosy from an uploaded image
- **Request**: `multipart/form-data` with a `file` field
- **Response**:
  ```json
  {
    "predicted_class": "Lep",
    "probabilities": {
      "Lep": 0.92,
      "Non Lep": 0.08
    }
  }
  ```

### `GET /health`
- **Description**: Health check endpoint
- **Response**:
  ```json
  {
    "status": "healthy",
    "model_loaded": true
  }
  ```

## Model Training Details

The model uses the following architecture:
- **Base Model**: Xception (pre-trained on ImageNet)
- **Custom Head**:
  - GlobalAveragePooling2D
  - Dense(512, activation='relu')
  - Dropout(0.5)
  - Dense(num_classes, activation='softmax')

**Training Strategy**:
1. **Phase 1**: Freeze base model, train only the custom head (5 epochs)
2. **Phase 2**: Unfreeze top 20 layers, fine-tune with lower learning rate (10 epochs)

**Data Augmentation**:
- Rotation (±20°)
- Width/Height shift (±20%)
- Shear (±20%)
- Zoom (±20%)
- Horizontal flip

## Evaluation

To evaluate the model on the test set:

```bash
cd backend/evaluation
python evaluate.py
```

This will generate:
- Classification report (precision, recall, F1-score)
- Confusion matrix visualization (`confusion_matrix.png`)

## Dataset

The application expects a dataset with the following structure:

```
data/
├── train/
│   ├── _annotations.csv
│   └── [image files]
├── valid/
│   ├── _annotations.csv
│   └── [image files]
└── test/
    ├── _annotations.csv
    └── [image files]
```

**CSV Format**:
```csv
filename,width,height,class,xmin,ymin,xmax,ymax
image1.jpg,640,640,Lep,0,0,640,640
image2.jpg,640,640,Non Lep,0,0,640,640
```

## Important Notes

⚠️ **Medical Disclaimer**: This is an AI-based decision support tool and **NOT a substitute for professional medical diagnosis**. Always consult a qualified healthcare professional for proper diagnosis and treatment.

## Customization

### Changing Dataset Path
Update the `DATA_DIR` variable in `backend/model/train.py`:
```python
DATA_DIR = "path/to/your/dataset"
```

### Changing Model Parameters
Edit the configuration variables in `backend/model/train.py`:
- `TARGET_SIZE`: Input image size
- `BATCH_SIZE`: Batch size for training
- `EPOCHS_HEAD`: Epochs for phase 1
- `EPOCHS_FINETUNE`: Epochs for phase 2

### Changing API Port
In `backend/app.py`, modify:
```python
app.run(host="0.0.0.0", port=YOUR_PORT)
```

And update the frontend API client in `frontend/src/api/client.js`:
```javascript
const API_BASE_URL = 'http://localhost:YOUR_PORT';
```

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure `flask-cors` is installed and enabled in `backend/app.py`.

### Model Not Found
If the API returns "Model file not found", train the model first using `python backend/model/train.py`.

### Port Already in Use
If port 5000 or 5173 is already in use, change the port numbers as described in the Customization section.

## License

This project is for educational and research purposes.

## Contributors

Built as a demonstration of full-stack ML application development.
