**Twitter Backend — корпоративный микроблог**

Бэкенд сервиса микроблогов для корпоративной сети.  

Стек: **FastAPI + PostgreSQL + Docker**.

**Возможности**

- Создание и удаление твитов

- Лайки / снятие лайков

- Подписки / отписки

- Лента твитов (сортировка по популярности — количество лайков)

- Загрузка изображений к твитам

- Авторизация через HTTP-заголовок `api-key`

**Быстрый старт (Docker)**

**Требования**

- Docker

- Docker Compose

**Запуск**

```bash

docker-compose up -d --build

После запуска:


| **Сервис**             | **URL**                                                                  |
| ---------------------- | ------------------------------------------------------------------------ |
| **UI (фронтенд)**      | [http://localhost:8000](http://localhost:8000)                           |
| API                    | [http://localhost:8000/api](http://localhost:8000/api)                   |
| Swagger (документация) | [http://localhost:8000/api/docs](http://localhost:8000/api/docs)         |
| OpenAPI JSON           | [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json) |


### **Тестовые пользователи**


| **Имя** | **api-key**       |
| ------- | ----------------- |
| Test    | `test` (ключ по умолчанию во фронте) |
| Alice   | `alice-key-123`   |
| Bob     | `bob-key-456`     |
| Charlie | `charlie-key-789` |


## **API**

Все запросы (кроме `/api/health`) требуют заголовок:

api-key: <ключ пользователя>


| **Метод** | **Путь**                 | **Описание**                   |
| --------- | ------------------------ | ------------------------------ |
| GET       | `/api/users/me`          | Профиль текущего пользователя  |
| GET       | `/api/users/{id}`        | Профиль пользователя по id     |
| POST      | `/api/users/{id}/follow` | Подписаться                    |
| DELETE    | `/api/users/{id}/follow` | Отписаться                     |
| GET       | `/api/tweets`            | Лента (твиты от подписок)      |
| POST      | `/api/tweets`            | Создать твит                   |
| DELETE    | `/api/tweets/{id}`       | Удалить свой твит              |
| POST      | `/api/tweets/{id}/likes` | Поставить лайк                 |
| DELETE    | `/api/tweets/{id}/likes` | Убрать лайк                    |
| POST      | `/api/medias`            | Загрузить картинку (form-data) |


### **Формат ошибок**

{

"result": false,

"error_type": "NotFound",

"error_message": "Описание ошибки"

}

## **Примеры запросов**

### **Профиль**

curl -H "api-key: alice-key-123" [http://localhost:8000/api/users/me](http://localhost:8000/api/users/me)

### **Создать твит**

curl -X POST -H "api-key: bob-key-456" -H "Content-Type: application/json" \

  -d "{\"tweet_data\": \"Привет!\", \"tweet_media_ids\": []}" \

  [http://localhost:8000/api/tweets](http://localhost:8000/api/tweets)

### **Лента**

curl -H "api-key: alice-key-123" [http://localhost:8000/api/tweets](http://localhost:8000/api/tweets)

### **Загрузить картинку**

curl -X POST -H "api-key: bob-key-456" -F "file=@image.jpg" \

[http://localhost:8000/api/medias](http://localhost:8000/api/medias)

### **Создать твит с картинкой**

1. Загрузить файл → получить `media_id`
2. Создать твит:

curl -X POST -H "api-key: bob-key-456" -H "Content-Type: application/json" \

-d "{\"tweet_data\": \"Твит с фото\", \"tweet_media_ids\": [1]}" \

[http://localhost:8000/api/tweets](http://localhost:8000/api/tweets)

## **Локальная разработка (без Docker app)**

python -m venv venv

venv\Scripts\activate           Windows

pip install -r requirements.txt

docker-compose up -d db         только PostgreSQL

alembic upgrade head

python scripts/seed_[users.py](http://users.py)

uvicorn app.main:app --reload

## **Тесты и линтер**

pytest -v

ruff check app tests

## **Структура проекта**

app/

  api/v1/        роутеры: users, tweets, medias

  core/          config, database, auth, exceptions

  models/        SQLAlchemy модели

  schemas/       Pydantic-схемы (формат API)

scripts/         seed-данные

alembic/       миграции БД

static/uploads/   загруженные картинки

frontend/         Vue UI (dist)

tests/            unit-тесты

## **Документация для фронтенда**

Интерактивная документация: **[http://localhost:8000/api/docs](http://localhost:8000/api/docs)**

  


