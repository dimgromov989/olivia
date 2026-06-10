#!/bin/bash
set -e

echo "🚀 Запуск Olivia Pizza Backend..."

# Ждём PostgreSQL
echo "⏳ Ожидание PostgreSQL..."
until pg_isready -h db -U postgres -d menu; do
  sleep 2
done

# Создаем миграции для новых приложений
echo "🔄 Создание миграций..."
python manage.py makemigrations --noinput

# Применяем миграции
echo "🔄 Применение миграций..."
python manage.py migrate --noinput

# Собираем статику
echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput --clear || echo "⚠️ collectstatic failed, skipping..."

# Создаём суперпользователя (ИСПРАВЛЕНО под кастомную модель User)
echo "👤 Создание суперпользователя..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='admin@olivia-pizza.ru').exists():
    User.objects.create_superuser(
        email='admin@olivia-pizza.ru',
        phone='+79999999999',
        password='admin123'
    )
    print('✅ Суперпользователь создан: admin@olivia-pizza.ru / admin123')
else:
    print('✅ Суперпользователь уже существует')
EOF

echo "✅ Запуск Django сервера..."
exec "$@"
