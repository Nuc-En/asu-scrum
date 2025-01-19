FROM tensorflow/tensorflow:2.6.0

# Устанавливаем Flask и необходимые пакеты
RUN pip install flask tensorflow keras numpy

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем приложение
COPY . .

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "app.py"]
