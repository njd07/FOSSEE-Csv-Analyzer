#!/bin/bash
set -e

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'njd07')
    print('Superuser created')
else:
    print('Superuser already exists')
" || echo "Note: Superuser creation attempted"

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting gunicorn..."
exec gunicorn visualizer_api.wsgi --log-file - --bind 0.0.0.0:8080
