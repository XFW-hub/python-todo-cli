
#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p backups

timestamp=$(date +%Y%m%d_%H%M%S)

backup_file="backups/todo_${timestamp}.dump"

temp_file="${backup_file}.tmp"

trap 'rm -f "$temp_file"' EXIT

echo "Starting PostgreSQL backup..."

docker compose exec -T db sh -c \
  'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' \
  > "$temp_file"

docker compose exec -T db \
  pg_restore --list \
  < "$temp_file" > /dev/null

mv "$temp_file" "$backup_file"

echo "Backup completed: $backup_file"

ls -lh "$backup_file"
