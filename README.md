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

3. **Train the model**:
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

## Important Notes

⚠️ **Medical Disclaimer**: This is an AI-based decision support tool and **NOT a substitute for professional medical diagnosis**. Always consult a qualified healthcare professional for proper diagnosis and treatment.


## License

This project is for educational and research purposes.
