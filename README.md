# AI Medical Image Prediction System

A beginner-friendly, educational AI medical image classification web application built with **Python Flask**, **TensorFlow/Keras**, and **Vanilla HTML5/CSS3/JavaScript**.

---

> ⚠️ **IMPORTANT DISCLAIMER**
> **This platform is built strictly for educational, learning, and research decision-support purposes.**
> It must **NOT** be used as a replacement for evaluation, diagnosis, or treatment by a qualified healthcare professional.

---

## 🚀 Beginner's Quick-Start Roadmap (For Students New to GitHub)

If you have **never used GitHub or command line before**, follow these simple step-by-step instructions to get the application up and running on your computer.

---

### Step 0: Check Prerequisites

1. **Check if Python is installed:**
   Open your terminal/command prompt and type:
   ```bash
   python --version
   ```
   *(If Python is not installed, download it from [python.org](https://www.python.org/downloads/).)*

2. **Check if Git is installed:**
   Type:
   ```bash
   git --version
   ```
   *(If Git is not installed, download it from [git-scm.com](https://git-scm.com/downloads).)*

---

### Step 1: Open Your Terminal or Command Prompt

- **On Windows:**
  Press `Win + R`, type `cmd` (or `powershell`), and press **Enter**.
- **On Mac:**
  Press `Cmd + Space`, type `Terminal`, and press **Enter**.

---

### Step 2: Clone (Download) the Repository

Navigate to your Desktop (or any folder where you want to keep the project):
```bash
cd Desktop
```

Clone the repository to your computer:
```bash
git clone https://github.com/bonsii2/ENT_Disease_predictor
```


Navigate into the downloaded project folder:
```bash
cd ENT_Disease_predictor
```

---

### Step 3: Pull Future Updates from GitHub (When code is updated)

Whenever your teacher or teammate updates code on GitHub, run this command inside the project folder to get the latest updates:
```bash
git pull origin main
```

---

### Step 4: Create a Python Virtual Environment

A virtual environment keeps all project packages isolated and prevents conflicts with other Python projects.

- **On Windows (Command Prompt or PowerShell):**
  ```bash
  python -m venv venv
  ```
- **On Mac / Linux:**
  ```bash
  python3 -m venv venv
  ```

---

### Step 5: Activate the Virtual Environment

- **On Windows (Command Prompt `cmd`):**
  ```cmd
  venv\Scripts\activate
  ```
- **On Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```
  *(If PowerShell shows an execution policy error, run: `Set-ExecutionPolicy Unrestricted -Scope Process` first).*

- **On Mac / Linux:**
  ```bash
  source venv/bin/activate
  ```

> 💡 **How do you know it's activated?**
> You will see `(venv)` at the beginning of your terminal command prompt line!

---

### Step 6: Install Required Packages

Install all necessary libraries (Flask, TensorFlow, NumPy, Pillow, Werkzeug) in one command:
```bash
pip install -r requirements.txt
```

---

### Step 7: Generate Initial Models & Assets (First Time Only)

Run this script once so TensorFlow creates sample model files inside `models/`:
```bash
python create_dummy_models.py
```

---

### Step 8: Run the Flask Web Application

Start the web server:
```bash
python app.py
```

You will see output in your terminal:
```
==================================================================
 Starting MediScan AI Flask Server...
 Access the application in your web browser at: http://127.0.0.1:5000/
==================================================================
```

---

### Step 9: Open the Website in Your Browser

Open your web browser (Chrome, Edge, Firefox, or Safari) and go to:
```
http://127.0.0.1:5000/
```

---

## 📋 Summary Checklist for Daily Use

Every time you open terminal to work on this project, run these 3 quick commands:

```bash
# 1. Go into the project directory
cd Desktop/ENT_Disease_predictor

# 2. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 3. Start Flask app
python app.py
```

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

## 4. How Frontend and Backend Communicate

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

## 5. API Endpoint Reference

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

## 6. How to Replace or Update Trained ML Models

1. Train your Keras model in Python / Google Colab with target input shape `(224, 224, 3)`.
2. Save your trained model file as `.keras` (e.g. `ear_disease_model.keras`).
3. Replace the corresponding file in the `models/` directory:
   - `models/ear_disease_model.keras`
   - `models/nose_disease_model.keras`
   - `models/throat_model.keras`
4. Update the corresponding `.json` class labels file (e.g., `models/ear_classes.json`) to match your exact class order.
5. Restart Flask (`python app.py`).

---

## 7. How to Change Educational Recommendations

To modify or add health recommendations:
1. Open [`recommendations/recommendations.py`](file:///c:/Users/Bonsaa%20Daba/OneDrive/Desktop/ent_project/recommendations/recommendations.py).
2. Edit or add keys matching your model class names in the `RECOMMENDATIONS` dictionary.
3. Keep advice general, non-prescriptive, and educational.

---

## 8. Common Errors and Solutions

| Problem | Cause | Solution |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'flask'` | Dependencies not installed in active environment. | Run `pip install -r requirements.txt` inside active `venv`. |
| `OSError: SavedModel file does not exist` | Missing `.keras` file in `models/`. | Run `python create_dummy_models.py` or place your trained `.keras` file in `models/`. |
| `400 Bad Request: Invalid file format` | User uploaded unsupported format (.bmp, .pdf, .txt). | Upload only `.jpg`, `.jpeg`, or `.png` images. |
| `Port 5000 in use` | Another Flask server or app is running on port 5000. | Change port in `app.py` to `port=5001` or stop the existing process. |

---

## 9. License & Learning Usage

This project is open for basic programming classes, computer vision demonstrations, and educational research.
