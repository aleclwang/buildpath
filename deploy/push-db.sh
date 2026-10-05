#!/usr/bin/env bash
# Copy the local Docker database to the server, replacing the server's copy.
# Usage (from the repo root, in Git Bash): SERVER=user@host deploy/push-db.sh
set -euo pipefail
# Stop Git Bash on Windows from rewriting container paths like /tmp/x into C:/...
export MSYS_NO_PATHCONV=1

: "${SERVER:?Set SERVER=user@host}"
DB_NAME="${DB_NAME:-buildpath_db}"
DB_USER="${DB_USER:-buildpath_user}"
DUMP="buildpath-$(date +%Y%m%d-%H%M%S).dump"
REMOTE_INFRA=/srv/infra
REMOTE_APP=/srv/buildpath/buildpath

cd "$(dirname "$0")/../buildpath"

echo "[push-db] Dumping local database..."
docker compose exec -T db pg_dump -U "$DB_USER" -Fc -f "/tmp/$DUMP" "$DB_NAME"
docker compose cp "db:/tmp/$DUMP" "$DUMP"
docker compose exec -T db rm "/tmp/$DUMP"

echo "[push-db] Uploading $(du -h "$DUMP" | cut -f1) to $SERVER..."
scp "$DUMP" "$SERVER:/tmp/$DUMP"
rm "$DUMP"

echo "[push-db] Restoring on server (site is briefly down)..."
ssh "$SERVER" bash -s <<EOF
set -euo pipefail
docker compose -f $REMOTE_APP/docker-compose.prod.yml stop web
docker compose -f $REMOTE_INFRA/docker-compose.yml cp /tmp/$DUMP postgres:/tmp/$DUMP
docker compose -f $REMOTE_INFRA/docker-compose.yml exec -T postgres \
    pg_restore -U $DB_USER -d $DB_NAME --clean --if-exists --no-owner --no-privileges --single-transaction /tmp/$DUMP
docker compose -f $REMOTE_INFRA/docker-compose.yml exec -T postgres rm /tmp/$DUMP
rm /tmp/$DUMP
docker compose -f $REMOTE_APP/docker-compose.prod.yml start web
EOF

echo "[push-db] Done."
