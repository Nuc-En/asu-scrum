from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import os
import threading
import time
import numpy as np
import json

model = VGG16(weights="imagenet")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "model.h5"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

IMG_SIZE = 360

status = {}

def prepare_image(image_path):
    print(11)
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    print(12)
    return img_array

def predict_image(image_path, task_id):
    print(8)
    prepared_image = prepare_image(image_path)
    print(9)
    print(f"Expected input shape: {model.input_shape}")
    print(f"Provided input shape: {prepared_image.shape}")
    
    predictions = model.predict(prepared_image)
    print(10)

    decoded_predictions = decode_predictions(predictions, top=3)
    print(11, decoded_predictions)

    status[task_id] = {
        "completed": True,
        "predictions": [
            {"label": label, "description": description, "probability": float(prob)}
            for label, description, prob in decoded_predictions[0]
        ]
    }
    print(status)

    return decoded_predictions

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        print(1)
        file = request.files["file"]
        print(2)
        if file.filename == "":
            return "No selected file", 400
        print(3)
        task_id = str(len(status) + 1) 
        print(4)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"{task_id}.jpg")
        print(5)
        file.save(filepath)
        print(6)
        status[task_id] = {"completed": False}
        print(7)
        threading.Thread(target=predict_image, args=(filepath, task_id)).start()

        return jsonify({"task_id": task_id})
    return render_template("index.html")

@app.route("/status/<task_id>", methods=["GET"])
def get_status(task_id):
    if task_id not in status:
        return jsonify({"error": "Task not found"}), 404
    print(status[task_id])
    return jsonify(status[task_id])

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
