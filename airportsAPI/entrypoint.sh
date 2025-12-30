#!/bin/sh

python manage.py migrate

echo "from django.contrib.auth import get_user_model; \
User = get_user_model(); \
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists(): \
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')" \
| python manage.py shell

gunicorn airportsAPI.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000