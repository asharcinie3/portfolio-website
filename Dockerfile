FROM python:3.10-slim

ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn \
    --bind 0.0.0.0:8080 \
    --worker-class eventlet \
    --workers 1 \
    --timeout 0 \
    app:app
