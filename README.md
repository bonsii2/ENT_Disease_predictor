# AI Medical Image Prediction System

A beginner-friendly, educational AI medical image classification web application built with **Python Flask**, **TensorFlow/Keras**, and **Vanilla HTML5/CSS3/JavaScript**.

---

> ⚠️ **IMPORTANT DISCLAIMER**
> **This platform is built strictly for educational, learning, and research decision-support purposes.**
> It must **NOT** be used as a replacement for evaluation, diagnosis, or treatment by a qualified healthcare professional.

---

## 1. Project Overview

This application allows users to select one of three specialized AI models (**Ear**, **Nose**, and **Throat/Third Model**) and upload a medical image. The backend processes the image using deep learning models and returns:
- **Predicted Condition / Disease Class**
- **Model Confidence Score & Percentage**
- **Full Probability Breakdown Across All Classes**
- **General Educational Recommendations & Advice**

---

## 2. Project Structure

```
medical-ai-project/
│
├── app.py                      # Main Flask application and REST API endpoints
├── requirements.txt            # Python dependencies list
├── create_dummy_models.py      # Utility script to generate sample Keras models
├── generate_logo.py            # Utility script to create static logo image
│
├── models/                     # ML Model storage directory
│   ├── ear_disease_model.keras # Trained ear classification model
│   ├── nose_disease_model.keras# Trained nose classification model
│   ├── throat_model.keras      # Trained throat classification model
│   ├── ear_classes.json        # Ear class names list
│   ├── nose_classes.json       # Nose class names list
│   └── throat_classes.json     # Throat class names list
│
├── utils/
│   ├── __init__.py
│   └── prediction.py           # Image preprocessing and model prediction logic
│
├── recommendations/
│   ├── __init__.py
│   └── recommendations.py     # Educational health information knowledge base
│
├── templates/                  # HTML5 pages (Jinja templates)
│   ├── index.html              # Landing page
│   ├── prediction.html         # Interactive prediction page with uploader
│   ├── about.html              # Project workflow & architecture info
│   └── contact.html            # Contact form with JS validation
│
├── static/                     # CSS, JavaScript & Images
│   ├── css/
│   │   └── style.css           # Custom medical tech design system stylesheet
│   ├── js/
│   │   ├── main.js             # Mobile navbar & contact form validator
│   │   └── prediction.js       # Dynamic tab switcher, uploader, API & results
│   └── images/
│       └── logo.png            # Application logo
│
└── uploads/                    # Temporary folder for processed images
    └── .gitkeep
```

---

## 3. System Requirements & Dependencies

- **Python 3.9+**
- **Flask** (Web framework)
- **TensorFlow** (Machine learning library)
- **NumPy** (Numerical computing)
- **Pillow** (PIL Image library)
- **Werkzeug** (Flask utility)

---

## 4. Step-by-Step Setup Guide

### Step 1: Create a Virtual Environment

It is recommended to run Python projects inside an isolated virtual environment.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 2: Install Required Dependencies

Install all required Python packages listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

---

### Step 3: Generate Initial Models & Logo

To allow Flask to start immediately out-of-the-box before placing your final trained custom model weights:

Run the included model generator script:
```bash
python create_dummy_models.py
```
*This creates sample `.keras` files inside `models/` so `tf.keras.models.load_model()` succeeds seamlessly.*

---

### Step 4: Run the Flask Web Application

Start the local Flask development server:
```bash
python app.py
```

You will see log messages in your terminal indicating that the models have loaded:
```
==================================================================
 Starting MediScan AI Flask Server...
 Access the application in your web browser at: http://127.0.0.1:5000/
==================================================================
```

---

### Step 5: Open the Application in your Browser

Open your web browser (Chrome, Firefox, Edge, or Safari) and navigate to:
```
http://127.0.0.1:5000/
```

---

## 5. How Frontend and Backend Communicate

```
User (Browser)
   │
   ├─► Selects Model Tab (Ear / Nose / Throat)
   ├─► Selects Image (Drag & Drop or File Picker)
   ├─► Clicks PREDICT
   │
   ▼
JavaScript (static/js/prediction.js)
   │
   ├─► Validates file format (.jpg, .jpeg, .png) & file size (<10MB)
   ├─► Packs image into FormData object
   ├─► Calls fetch('POST', '/api/predict/ear')
   │
   ▼
Flask API (app.py)
   │
   ├─► Receives request file
   ├─► Saves temporary image to uploads/ folder
   ├─► Calls utils/prediction.py
   │
   ▼
TensorFlow ML Model (models/*.keras)
   │
   ├─► Preprocesses image into 224x224 RGB tensor
   ├─► Computes Softmax class probabilities
   │
   ▼
Flask API Response (app.py)
   │
   ├─► Generates educational recommendation from recommendations.py
   ├─► Deletes temporary uploaded image file
   ├─► Returns JSON response payload
   │
   ▼
JavaScript Renderer (static/js/prediction.js)
   │
   ├─► Displays prediction title & confidence percentage
   ├─► Animates horizontal probability progress bars
   ├─► Renders recommendation and safety disclaimer box
```

---

## 6. API Endpoint Reference

### 1. Ear Disease Prediction
- **URL:** `POST /api/predict/ear`
- **Payload:** `multipart/form-data` with key `image`

### 2. Nose Disease Prediction
- **URL:** `POST /api/predict/nose`
- **Payload:** `multipart/form-data` with key `image`

### 3. Third (Throat) Disease Prediction
- **URL:** `POST /api/predict/third` (Alias: `/api/predict/throat`)
- **Payload:** `multipart/form-data` with key `image`

---

### Sample JSON API Response
```json
{
  "success": true,
  "model": "ear",
  "prediction": "Normal",
  "confidence": 0.91,
  "confidence_percentage": 91.0,
  "probabilities": {
    "Acute Otitis Media": 0.02,
    "Cerumen Impaction": 0.01,
    "Chronic Otitis Media": 0.03,
    "Myringosclerosis": 0.03,
    "Normal": 0.91
  },
  "recommendation": {
    "title": "Normal Appearance Predicted",
    "message": "The medical image was classified as Normal by the AI model.",
    "advice": "No significant anatomical abnormality was detected by the algorithm. However, if you are experiencing pain, discharge, discomfort, fever, or other symptoms, always seek evaluation by a qualified healthcare professional."
  }
}
```

---

## 7. How to Replace or Update Trained ML Models

1. Train your Keras model in Python / Google Colab with target input shape `(224, 224, 3)`.
2. Save your trained model file as `.keras` (e.g. `ear_disease_model.keras`).
3. Replace the corresponding file in the `models/` directory:
   - `models/ear_disease_model.keras`
   - `models/nose_disease_model.keras`
   - `models/throat_model.keras`
4. Update the corresponding `.json` class labels file (e.g., `models/ear_classes.json`) to match your exact class order.
5. Restart Flask (`python app.py`).

---

## 8. How to Change Educational Recommendations

To modify or add health recommendations:
1. Open [`recommendations/recommendations.py`](file:///c:/Users/Bonsaa%20Daba/OneDrive/Desktop/ent_project/recommendations/recommendations.py).
2. Edit or add keys matching your model class names in the `RECOMMENDATIONS` dictionary.
3. Keep advice general, non-prescriptive, and educational.

---

## 9. Common Errors and Solutions

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed in active environment. | Run `pip install -r requirements.txt` inside active `venv`. |
| `OSError: SavedModel file does not exist` | Missing `.keras` file in `models/`. | Run `python create_dummy_models.py` or place your trained `.keras` file in `models/`. |
| `400 Bad Request: Invalid file format` | User uploaded unsupported format (.bmp, .pdf, .txt). | Upload only `.jpg`, `.jpeg`, or `.png` images. |
| `Port 5000 in use` | Another Flask server or app is running on port 5000. | Change port in `app.py` to `port=5001` or stop the existing process. |

---

## 10. License & Learning Usage

This project is open for basic programming classes, computer vision demonstrations, and educational research.
# ENT_Disease_predictor
