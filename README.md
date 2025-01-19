# asu-scrum
Проект представляет собой сайт для распознавания фруктов, где пользователь может выложить картинку, в ответ сайт подумает и выведет какой фрукт или овощь выложил пользователь. Лучше всего работает с квадратными картинками.

Тесты модели распознавания и процесс обучения  можно посмотреть, скачав файл `dev_model.ipynb`

Точность рапознавания на валидационной выборке составила 0.91

Модель можно скачать по [ссылке](https://mega.nz/file/AconRT7Z#mFy8KBTJrq_cX5JKUUciqvMqPLy8YWEp8J6bmrMHBPc). github имеет ограничение на размер файла 100мб, поэтому так.

## Структура сайта
- app.py
- Dockerfile
- docker-compose.yml
- model.h5
- /templates
- - index.html
- /uploads

## Используемые технологии
flask для сервера, tensorflow - для распознавания.

## Требования
Установить [docker](https://docs.docker.com/compose/install/)

## Запуск
- скачать [модель](https://mega.nz/file/AconRT7Z#mFy8KBTJrq_cX5JKUUciqvMqPLy8YWEp8J6bmrMHBPc) в папку проекта
- запустить docker
```bash
docker compose up -d
```