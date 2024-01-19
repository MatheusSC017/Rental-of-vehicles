#!/bin/sh

echo "Starting database and creating access token..."

python init_db.py

echo "DB started and token created"

exec "$@"
