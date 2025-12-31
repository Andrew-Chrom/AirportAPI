ARG PYTHON_VERSION=3.13.7
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt /app/

# for psycopg2
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean   

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# for problem with settings.py
ENV DJANGO_SETTINGS_MODULE=airportsAPI.settings
ENV SECRET_KEY=dummy-secret-key
ENV ALLOWED_HOSTS=*
ENV DATABASE_URL=sqlite:///db.sqlite3

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "airportsAPI.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
