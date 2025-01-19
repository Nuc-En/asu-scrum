FROM tensorflow/tensorflow:2.6.0

RUN pip install flask tensorflow keras numpy

WORKDIR /app

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
