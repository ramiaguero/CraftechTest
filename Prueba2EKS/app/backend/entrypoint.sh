#!/bin/sh

# Wait for PostgreSQL to be ready before proceeding
if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for PostgreSQL..."
    while ! nc -z "$SQL_HOST" "$SQL_PORT"; do
        sleep 0.1
    done
    echo "PostgreSQL is ready."
fi

# Apply migrations properly
python manage.py makemigrations core
python manage.py flush --no-input  # Ensure clean state
python manage.py migrate --noinput

# Run the server (replacing shell process)
exec python manage.py runserver 0.0.0.0:8000
