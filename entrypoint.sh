#!/bin/sh
set -e

echo "[startup] Running migrations..."
alembic upgrade head

echo "[startup] Starting API..."
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
