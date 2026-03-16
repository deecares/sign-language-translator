import base64
import re

import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request

import os

app = Flask(__name__)

# Load the trained model once at startup.
# Use an absolute path so this works no matter the current working directory.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(PROJECT_ROOT, "model", "model.h5")
# Load the model without compiling to avoid incompatibilities with optimizer configs
# (we only need it for inference).
model = tf.keras.models.load_model(MODEL_PATH, compile=False)
labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")



def _make_cors_response(response):
    # Simple CORS support for local development.
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.after_request
def add_cors_headers(response):
    return _make_cors_response(response)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


def _decode_image(data_url: str) -> np.ndarray:
    """Decode a data-url (base64) image into an OpenCV BGR array."""
    # Remove prefix if it exists (data:image/jpeg;base64,...)
    if data_url.startswith("data:"):
        data_url = data_url.split(",", 1)[1]

    image_bytes = base64.b64decode(data_url)
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


def _prepare_model_input(img: np.ndarray) -> np.ndarray:
    """Preprocess the image to match the model input requirements."""

    # Crop a centered square region to reduce background noise.
    h, w = img.shape[:2]
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    img = img[start_y : start_y + min_dim, start_x : start_x + min_dim]

    # Convert to RGB (model was trained on RGB images) and resize to (64,64).
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (64, 64), interpolation=cv2.INTER_AREA)

    # Normalize pixel values.
    normalized = resized.astype(np.float32) / 255.0
    return np.expand_dims(normalized, axis=0)


@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)
    if not payload or "image" not in payload:
        return _make_cors_response(
            jsonify({"error": "Missing required field 'image' in JSON body."}),
        ), 400

    try:
        img = _decode_image(payload["image"])
    except Exception as exc:
        return _make_cors_response(
            jsonify({"error": "Failed to decode image.", "details": str(exc)}),
        ), 400

    if img is None:
        return _make_cors_response(
            jsonify({"error": "Could not decode image into an array."}),
        ), 400

    model_input = _prepare_model_input(img)

    prediction = model.predict(model_input, verbose=0)
    confidence = float(np.max(prediction))
    letter = labels[int(np.argmax(prediction))]

    return _make_cors_response(
        jsonify({
            "letter": letter,
            "confidence": confidence,
        }),
    )


if __name__ == "__main__":
    # For local development, run the server on port 5000.
    app.run(host="0.0.0.0", port=5000)
