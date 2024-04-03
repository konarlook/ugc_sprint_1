echo "Waiting Kafka start"
while ! nc -z "${KAFKA_HOST}" "${KAFKA_PORT}"; do
  sleep 1
done
echo "Kafka started"

cd src || exit

gunicorn --worker-class gevent --workers 4 --bind "0.0.0.0:5001" --log-level debug main:app
