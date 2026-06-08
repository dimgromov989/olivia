FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install \
        django \
        djangorestframework \
        psycopg2-binary \
        python-dotenv \
        drf-polymorphic \
        drf-spectacular \
        Pillow \
        django-storages \
        boto3

COPY . .

RUN mkdir -p /app/media /app/static /app/staticfiles

EXPOSE 8000

COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]