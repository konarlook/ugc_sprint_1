#!/bin/bash

export PYTHONPATH="/opt/app"

# Ожидание доступности PostgreSQL
/opt/app/core/wait_for_postgres.sh

# Инициализация базы данных и применение миграций
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Запуск Flask-приложения
python /opt/app/app.py
