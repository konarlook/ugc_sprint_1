#!/bin/bash

export PYTHONPATH="/opt/app/src"

# Инициализация базы данных и применение миграций
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Запуск Flask-приложения
python /opt/app/src/app.py
