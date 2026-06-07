FROM python:3.14-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        build-essential \
        libpq-dev \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости через pip
RUN pip install --upgrade pip \
    && pip install \
        django \
        djangorestframework \
        psycopg2-binary \
        python-dotenv \
        drf-polymorphic \
        drf-spectacular \
        Pillow

# Копируем проект
COPY . .

# Создаём директории
RUN mkdir -p /app/media /app/static /app/staticfiles

# Порт
EXPOSE 8000

# Конвертация CRLF → LF для Windows и запуск
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]



