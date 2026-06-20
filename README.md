Twitter Backend — корпоративный микроблог

Бэкенд сервиса микроблогов (аналог Twitter) для корпоративной сети.

Реализован на FastAPI + PostgreSQL.

Возможности

- Создание и удаление твитов

- Лайки

- Подписки на пользователей

- Лента твитов (сортировка по популярности)

- Загрузка изображений к твитам

- Авторизация через заголовок `api-key`

Стек

- Python 3.12

- FastAPI

- SQLAlchemy

- PostgreSQL

- Alembic

- Docker / Docker Compose

Быстрый старт

Требования

- Docker и Docker Compose

Запуск

```bash

docker-compose up -d --build