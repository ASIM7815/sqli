#!/bin/sh
set -eu

DB_PATH="/app/instance/data/sqli_lab.db"

if [ ! -f "$DB_PATH" ]; then
  echo "Initializing QueryQuest database..."
  python init_db.py
fi

exec gunicorn \
  --bind "0.0.0.0:${PORT:-5000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout 30 \
  --access-logfile - \
  --error-logfile - \
  'app:create_app()'
