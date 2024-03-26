#!/bin/sh
# wait_for_postgres.sh

set -e

host="db"  # не забыть поменять когда переменные окружения
user="ugc_user"
password="ugc_pass"
database="ugc_database"
cmd="$@"

until PGPASSWORD="$password" psql -h "$host" -U "$user" -d "$database" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"
exec $cmd
