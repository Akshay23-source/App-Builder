#!/usr/bin/env bg
set -e

echo "=== Initializing ForgeAI Database Migrations ==="
cd "$(dirname "$0")/../../backend"
python -m alembic upgrade head
echo "=== Database Initialization Complete ==="
