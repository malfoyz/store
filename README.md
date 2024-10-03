<h2 align="center">Интернет-магазин на Django</h2>

Онлайн-магазин на Django в качестве домашнего задания ITM.

### Инструменты разработки

**Стек:**
- Python >= 3.12
- Postgres 15

## Старт

#### 1) Создать образ

    docker-compose build

##### 2) Запустить контейнер

    docker-compose up

###### или все вместе:

    docker-compose up --build
    
##### 3) Перейти по адресу

    http://127.0.0.1:8000/admin/

## Разработка с Docker

##### 1) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 2) В корне проекта создать .env

    SECRET_KEY=django-insecure-i95^ao9zm=2u0o^u&b6rc1^3q5o(uef3hm1+h@(2+@si6dz7sy
    DEBUG=True
    
    # for project
    DB_ENGINE=django.db.backends.postgresql
    DB_HOST=db
    DB_USER=postgres
    DB_PASS=postgres
    DB_NAME=store
    
    # for postgres container
    POSTGRES_DB=store
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    
##### 3) Создать образ

    docker-compose build

##### 4) Запустить контейнер

    docker-compose up

##### 5) В другой консоли зайти в контейнер:

    docker exec -it app /bin/sh

##### 6) Установить миграции
    
    python manage.py migrate
    
##### 7) Создать суперюзера

    python manage.py createsuperuser
                                                        
##### 8) Если нужно очистить БД

    docker-compose down -v