# Sign Language Translator

## Overview
This project provides a simple sign language letter classifier using a trained TensorFlow model and a React frontend that uses the webcam.

- **Backend** (Python + Flask): accepts an image from the browser, runs the model, and returns the predicted letter.
- **Frontend** (React): captures webcam image, sends it to the backend, and displays the detected letter.

## Setup (Windows)

### 1) Prepare Python environment

1. Open a terminal and change to the project root:
   ```powershell
   cd F:\sign-language-translator
   ```
2. Create and activate a venv (if not already):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install Python dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### 2) Start the backend server

From the project root (with the venv activated):

```powershell
python -m app.server
```

This starts a Flask server on `http://localhost:5000`.

### 3) Start the frontend

In a separate terminal, run:

```powershell
cd frontend\sign-ui
npm install
npm start
```

Then open the browser at `http://localhost:3000`.

---

## Usage

1. Allow the browser to use your webcam.
2. Click **Capture** to take a snapshot.
3. The app sends the image to the backend, which returns the predicted letter and confidence.

## Notes

- The model in `model/model.h5` expects 64x64 RGB images.
- The frontend currently sends a full-frame screenshot to the backend.

---

## Extending the project

- Add word-level smoothing / buffering.
- Improve hand detection / ROI cropping before prediction.
- Add a training pipeline that exports an up-to-date model.
