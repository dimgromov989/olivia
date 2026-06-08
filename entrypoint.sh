#!/bin/bash
set -e

echo "🚀 Запуск Olivia Pizza Backend..."

# Ждём PostgreSQL
echo "⏳ Ожидание PostgreSQL..."
until pg_isready -h db -U postgres -d menu; do
  sleep 2
done

# Применяем миграции
echo "🔄 Применение миграций..."
python manage.py migrate --noinput

# Собираем статику
echo "📦 Сборка статических файлов..."
python manage.py collectstatic --noinput --clear || echo "⚠️ collectstatic failed, skipping..."

# Создаём суперпользователя
echo "👤 Создание суперпользователя..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@olivia-pizza.ru', 'admin123')
    print('✅ Суперпользователь создан: admin / admin123')
else:
    print('✅ Суперпользователь уже существует')
EOF

echo "✅ Запуск Django сервера..."
exec "$@"