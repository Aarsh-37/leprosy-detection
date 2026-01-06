from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model.utils import predict_image, load_model_and_labels

app = Flask(__name__)
CORS(app) # Enable CORS for frontend communication

# Pre-load model at startup
try:
    load_model_and_labels()
except Exception as e:
    print(f"Warning: Could not load model at startup: {e}")

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No filename provided"}), 400
    
    try:
        image_bytes = file.read()
        predicted_class, probabilities = predict_image(image_bytes)
        
        return jsonify({
            "predicted_class": predicted_class,
            "probabilities": probabilities
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "model_loaded": os.path.exists("./saved_models/leprosy_xception.keras")})

if __name__ == "__main__":
    # Ensure saved_models directory exists
    os.makedirs("./saved_models", exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
