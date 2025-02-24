#!/bin/sh

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
        sleep 0.1
    done
    echo "PostgreSQL is ready."
fi

python manage.py makemigrations core
python manage.py flush --no-input  
python manage.py migrate --noinput

exec python manage.py runserver 0.0.0.0:8000
