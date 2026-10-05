#!/usr/bin/env bash
# Pull the latest main and rebuild the app. Run on the server.
# GitHub Actions' deploy key is restricted to running only this script
# (forced command in ~/.ssh/authorized_keys), so it can't do anything else.
#
# Everything is inside main() so bash parses the whole file before git pull
# can rewrite it mid-run.
set -euo pipefail

main() {
    cd /srv/buildpath
    echo "[deploy] Pulling latest main..."
    git pull --ff-only origin main
    echo "[deploy] Now at $(git log -1 --format='%h %s')"

    cd buildpath
    echo "[deploy] Rebuilding and restarting app..."
    docker compose -f docker-compose.prod.yml up -d --build --quiet-pull </dev/null

    echo "[deploy] Waiting for app to come up..."
    for _ in $(seq 1 30); do
        if docker compose -f docker-compose.prod.yml exec -T web \
            python -c "import os, urllib.request as u; u.urlopen(u.Request('http://localhost:8000/api/champions/', headers={'Host': os.environ['ALLOWED_HOSTS'].split(',')[0]}))" \
            </dev/null >/dev/null 2>&1; then
            echo "[deploy] App is responding"
            docker image prune -f >/dev/null
            exit 0
        fi
        sleep 2
    done

    echo "[deploy] App did not respond within 60s; recent logs:"
    docker compose -f docker-compose.prod.yml logs --tail 30 </dev/null
    exit 1
}

main "$@"
