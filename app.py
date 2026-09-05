"""
=============================================================================
MediScan AI - Python Flask Medical Image Prediction Application
=============================================================================

This application provides a beginner-friendly web interface and REST API for
analyzing medical images across three specialized machine learning models:
1. Ear Disease Model
2. Nose Disease Model
3. Throat Disease Model (Third Model)

Key Workflow:
1. Load ML models (.keras) and class labels (.json) ONCE when Flask starts.
2. Accept uploaded images via HTTP POST API endpoints.
3. Validate file extensions and security rules.
4. Preprocess images into standard 224x224 RGB tensors.
5. Run TensorFlow inference to determine class probabilities.
6. Return structured JSON responses with predictions and health recommendations.
"""

import os
import sys
import json

# Ensure project root directory is in sys.path for Flask reloader
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

# Import local utility modules
from utils.prediction import run_model_prediction
from recommendations.recommendations import get_recommendation

# Initialize Flask Web Application
app = Flask(__name__)

# Configuration Parameters
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limit uploads to 16 Megabytes

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Ensure temporary upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Helper function to validate allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =============================================================================
# MODEL AND CLASS LOADING AT STARTUP
# =============================================================================
# Global dictionaries to store loaded models and class names
MODELS = {
    'ear': None,
    'nose': None,
    'third': None
}

CLASSES = {
    'ear': ["Acute Otitis Media", "Cerumen Impaction", "Chronic Otitis Media", "Myringosclerosis", "Normal"],
    'nose': ["Nasal Polyps", "Normal"],
    'third': ["Pharyngitis", "Tonsillitis", "Normal"]
}


def load_all_models():
    """
    Loads Keras model files (.keras) and class JSON maps (.json) ONCE during server startup.
    Searches both 'model' and 'models' directories, prioritizing real trained model files.
    """
    base_dir = os.path.dirname(__file__)
    search_dirs = [os.path.join(base_dir, 'model'), os.path.join(base_dir, 'models')]
    
    # Try importing TensorFlow/Keras
    try:
        import tensorflow as tf
        has_tf = True
        print("[INFO] TensorFlow imported successfully.")
    except ImportError:
        has_tf = False
        print("[WARNING] TensorFlow is not installed. Running in mock inference mode.")

    model_files = {
        'ear': ('ear_disease_model.keras', 'ear_classes.json'),
        'nose': ('nose_disease_model.keras', 'nose_classes.json'),
        'third': ('throat_model.keras', 'throat_classes.json')
    }

    for key, (model_filename, classes_filename) in model_files.items():
        # 1. Search for Class Names JSON in candidate directories
        for d in search_dirs:
            classes_path = os.path.join(d, classes_filename)
            if os.path.exists(classes_path):
                try:
                    with open(classes_path, 'r') as f:
                        CLASSES[key] = json.load(f)
                    print(f"[INFO] Loaded class map for '{key}' from {d}: {CLASSES[key]}")
                    break
                except Exception as e:
                    print(f"[ERROR] Failed loading {classes_filename}: {e}")

        # 2. Search for Keras Model in candidate directories (prioritizing real models > 1MB)
        model_found_path = None
        if has_tf:
            for d in search_dirs:
                candidate_path = os.path.join(d, model_filename)
                if os.path.exists(candidate_path):
                    # Check if file size indicates a real model (> 1MB) vs dummy model (< 1MB)
                    size_mb = os.path.getsize(candidate_path) / (1024 * 1024)
                    if model_found_path is None or size_mb > 1.0:
                        model_found_path = candidate_path

        if has_tf and model_found_path and os.path.exists(model_found_path):
            try:
                MODELS[key] = tf.keras.models.load_model(model_found_path)
                print(f"[INFO] Successfully loaded Keras model for '{key}' from {model_found_path} ({os.path.getsize(model_found_path)/1e6:.1f} MB)")
            except Exception as e:
                print(f"[WARNING] Could not load model '{model_filename}' from {model_found_path}: {e}. Using fallback.")
        else:
            print(f"[NOTICE] Model file '{model_filename}' not found. Fallback enabled for '{key}'.")

# Load models when app starts
load_all_models()


# =============================================================================
# FRONTEND HTML PAGE ROUTES
# =============================================================================

@app.route('/')
def home():
    """Renders the Home landing page."""
    return render_template('index.html')


@app.route('/prediction')
def prediction():
    """Renders the Prediction tool page."""
    return render_template('prediction.html')


@app.route('/about')
def about():
    """Renders the About information page."""
    return render_template('about.html')


@app.route('/contact')
def contact():
    """Renders the Contact page."""
    return render_template('contact.html')


# =============================================================================
# REST API PREDICTION ENDPOINTS
# =============================================================================

def handle_prediction_request(model_key):
    """
    Common handler function for image prediction requests across all models.
    
    Steps:
    1. Check if 'image' file is in HTTP request.
    2. Validate file existence and file type extension.
    3. Save file temporarily using secure_filename.
    4. Run ML model inference and fetch educational recommendation.
    5. Clean up / delete temporary uploaded image file.
    6. Return JSON response.
    """
    # 1. Check if an image file was provided in the request
    if 'image' not in request.files:
        return jsonify({
            "success": False,
            "error": "No image file provided in request."
        }), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({
            "success": False,
            "error": "No image selected. Please choose a file."
        }), 400

    # 2. Validate file extension
    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": "Invalid file format. Only JPG, JPEG, and PNG images are supported."
        }), 400

    # 3. Save file securely to temporary uploads folder
    temp_filename = secure_filename(file.filename)
    temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
    
    try:
        file.save(temp_path)

        # 4. Perform ML Prediction & Class Matching
        model = MODELS.get(model_key)
        class_names = CLASSES.get(model_key, [])
        
        prediction_result = run_model_prediction(
            model=model,
            class_names=class_names,
            image_path=temp_path,
            model_type_name=model_key
        )

        # Fetch educational recommendation based on predicted condition
        recommendation = get_recommendation(prediction_result["prediction"])

        # 5. Format successful JSON response
        response_payload = {
            "success": True,
            "model": prediction_result["model"],
            "prediction": prediction_result["prediction"],
            "confidence": prediction_result["confidence"],
            "confidence_percentage": prediction_result["confidence_percentage"],
            "probabilities": prediction_result["probabilities"],
            "recommendation": recommendation
        }

        return jsonify(response_payload), 200

    except Exception as e:
        # Handle server or processing errors gracefully
        return jsonify({
            "success": False,
            "error": f"An error occurred while analyzing the image: {str(e)}"
        }), 500

    finally:
        # 6. Clean up temporary uploaded file immediately for security & privacy
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass


@app.route('/api/predict/ear', methods=['POST'])
def predict_ear():
    """API endpoint for Ear Disease Prediction."""
    return handle_prediction_request('ear')


@app.route('/api/predict/nose', methods=['POST'])
def predict_nose():
    """API endpoint for Nose Disease Prediction."""
    return handle_prediction_request('nose')


@app.route('/api/predict/third', methods=['POST'])
@app.route('/api/predict/throat', methods=['POST'])
def predict_third():
    """API endpoint for Third (Throat) Disease Prediction."""
    return handle_prediction_request('third')


# =============================================================================
# APPLICATION LAUNCH
# =============================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    print("==================================================================")
    print(" Starting MediScan AI Flask Server...")
    print(f" Access the application in your web browser at: http://127.0.0.1:{port}/")
    print("==================================================================")
    app.run(host='127.0.0.1', port=port, debug=True)
