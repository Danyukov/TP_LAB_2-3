#!/bin/sh
set -e

DB_HOST="${DATABASE_HOST:-db}"
DB_PORT="${DATABASE_PORT:-5432}"

echo "Waiting for Postgres at $DB_HOST:$DB_PORT..."
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.5
done

python manage.py migrate --noinput

# фикстура с товарами (в репо она есть)
python manage.py loaddata products.yaml || true
python manage.py loaddata promo_codes.yaml || true


exec "$@"
