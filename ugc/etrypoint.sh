#!/bin/sh

echo "Waiting Kafka start"
while ! nc -z "${KAFKA_HOST}" "${KAFKA_PORT}"; do
  sleep 1
done
echo "Kafka started"

cd src || exit

gunicorn -c gunicorn/gunicorn.py main:app
