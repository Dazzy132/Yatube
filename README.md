# Социальная сеть для блогов

[![CI](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml/badge.svg?branch=master)](https://github.com/yandex-praktikum/hw05_final/actions/workflows/python-app.yml)

### Описание
Социальная сеть, которая позволяет пользователям делиться записями, заходить на чужие страницы, подписываться на других пользователей и комментировать их записи. Также пользователи могут создавать сообщества по интересам и выкладывать записи в них.


### Стек технологий
- Python 3.7.9
- Django 2.2.16
- UnitTest

------

### Наполнение .env файла
```dotenv
SECRET_KEY='SECRET_KEY'
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-example.com

# Если БД будет PostgreSQL
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=127.0.0.1
DB_PORT=5432
# ------------------------
```

### Установка и запуск проекта:

1. Клонировать репозиторий и перейти в него в командной строке:
```shell
git clone git@github.com:Dazzy132/Yatube.git
```

2. Перейти в каталог проекта
```shell
cd yatube
```

3. Создать и активировать виртуальное окружение
```shell
python -m venv venv

source venv/Scripts/activate (Для Windows)
source venv/bin/activate (Для Linux и MacOS)
```
4. Установить зависимости
```shell
pip install -r requirements.txt
```

5. Выполнить миграции
```shell
python manage.py makemigrations
python manage.py migrate
```

6. Создать суперпользователя (Рекомендуется)
```shell
python manage.py createsuperuser --username=root --email=root@mail.ru
```

7. Запустить сервер
```shell
python manage.py runserver
```
