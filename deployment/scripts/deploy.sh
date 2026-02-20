#!/usr/bin/env bash
# deploy.sh — Zero-downtime deploy to goh.nlibera.com
# Usage: ./deployment/scripts/deploy.sh [--skip-frontend]
#
# Run locally. Requires:
#   - SSH access to root@goh.nlibera.com
#   - node + npm available locally (for frontend build)
set -euo pipefail

REMOTE="root@goh.nlibera.com"
APP_DIR="/opt/goh"
STATIC_DIR="/var/www/goh"
APP_USER="goh"
SKIP_FRONTEND="${1:-}"

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "==> Deploying Guilds of Heroes"
echo "    Repo: ${REPO_ROOT}"
echo "    Remote: ${REMOTE}"
echo ""

# ── 1. Build frontend locally ──────────────────────────────────────────────────
if [ "${SKIP_FRONTEND}" != "--skip-frontend" ]; then
    echo "[1/5] Building React frontend..."
    cd "${REPO_ROOT}/frontend"
    npm ci
    VITE_API_URL=/api/v1 npm run build
    echo "      Frontend built: $(du -sh dist | cut -f1)"
else
    echo "[1/5] Skipping frontend build (--skip-frontend)"
fi

# ── 2. Push code to server ─────────────────────────────────────────────────────
echo "[2/5] Syncing backend code..."
rsync -az --exclude='.git' --exclude='frontend/node_modules' \
    --exclude='frontend/dist' --exclude='__pycache__' \
    --exclude='*.pyc' --exclude='.env' \
    "${REPO_ROOT}/" "${REMOTE}:${APP_DIR}/"

# ── 3. Push frontend dist ──────────────────────────────────────────────────────
if [ "${SKIP_FRONTEND}" != "--skip-frontend" ]; then
    echo "[3/5] Uploading frontend to ${STATIC_DIR}..."
    rsync -az --delete "${REPO_ROOT}/frontend/dist/" "${REMOTE}:${STATIC_DIR}/"
    ssh "${REMOTE}" "chown -R www-data:www-data ${STATIC_DIR}"
else
    echo "[3/5] Skipping frontend upload"
fi

# ── 4. Update Python deps & run migrations ─────────────────────────────────────
echo "[4/5] Updating dependencies and running migrations..."
ssh "${REMOTE}" bash << ENDSSH
set -euo pipefail
cd ${APP_DIR}
sudo -u ${APP_USER} .venv/bin/pip install -q -e ".[prod]"
sudo -u ${APP_USER} .venv/bin/goh db migrate
echo "      Migrations done"
ENDSSH

# ── 5. Graceful reload (no downtime) ──────────────────────────────────────────
echo "[5/5] Reloading services..."
ssh "${REMOTE}" bash << ENDSSH
systemctl reload-or-restart goh-api
nginx -t && systemctl reload nginx
echo "      Services reloaded"
ENDSSH

echo ""
echo "=== Deploy complete! ==="
echo "    https://goh.nlibera.com/api/v1/health"
