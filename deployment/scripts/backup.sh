#!/usr/bin/env bash
# backup.sh — SQLite WAL-safe backup for Guilds of Heroes
# Runs on the server (via cron or manual).
# Usage: ./backup.sh [backup_dir]
#
# Add to crontab (daily at 03:00):
#   0 3 * * * /opt/goh/deployment/scripts/backup.sh >> /var/log/goh/backup.log 2>&1
set -euo pipefail

DB_PATH="${GOH_DATABASE_PATH:-/opt/goh/data/goh.db}"
BACKUP_DIR="${1:-/opt/goh/backups}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="${BACKUP_DIR}/goh_${TIMESTAMP}.db"
KEEP_DAYS=14

echo "[$(date -Iseconds)] Starting backup"

# Create backup directory if needed
mkdir -p "${BACKUP_DIR}"

# SQLite online backup (safe while DB is open / WAL mode)
sqlite3 "${DB_PATH}" ".backup '${BACKUP_FILE}'"

SIZE="$(du -sh "${BACKUP_FILE}" | cut -f1)"
echo "[$(date -Iseconds)] Backup written: ${BACKUP_FILE} (${SIZE})"

# Compress
gzip -f "${BACKUP_FILE}"
echo "[$(date -Iseconds)] Compressed: ${BACKUP_FILE}.gz"

# Remove backups older than KEEP_DAYS
REMOVED=$(find "${BACKUP_DIR}" -name "goh_*.db.gz" \
    -mtime "+${KEEP_DAYS}" -print -delete | wc -l)
echo "[$(date -Iseconds)] Pruned ${REMOVED} old backup(s) (>${KEEP_DAYS} days)"

echo "[$(date -Iseconds)] Backup complete"
