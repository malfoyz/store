#!/bin/bash

cd src

# python manage.py flush --no-input
# python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000