from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os
import threading
import time
import numpy as np

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
MODEL_PATH = "model.h5"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

IMG_SIZE = 360
MODEL_PATH = 'model.h5'
# Загружаем модель
model = load_model(MODEL_PATH)

# Глобальный объект для отслеживания статуса распознавания
status = {}

# Предсказываем класс изображения
def predict_image(image_path, task_id):
    img = load_img(image_path, target_size=(IMG_SIZE, IMG_SIZE))  # Убедитесь, что размер соответствует обученной модели
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    probability = predictions[0][predicted_class]

    # Обновляем статус задачи
    status[task_id] = {"completed": True, "class": int(predicted_class), "probability": float(probability)}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Сохраняем загруженное изображение
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        task_id = str(len(status) + 1)  # Генерируем уникальный ID для задачи
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], f"{task_id}.jpg")
        file.save(filepath)

        # Инициализируем задачу распознавания
        status[task_id] = {"completed": False}
        threading.Thread(target=predict_image, args=(filepath, task_id)).start()

        return jsonify({"task_id": task_id})
    return render_template("index.html")

@app.route("/status/<task_id>", methods=["GET"])
def get_status(task_id):
    if task_id not in status:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(status[task_id])

if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="0.0.0.0", port=5000)
