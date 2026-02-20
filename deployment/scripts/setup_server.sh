#!/usr/bin/env bash
# setup_server.sh — One-time server provisioning for goh.nlibera.com
# Run as root on a fresh DigitalOcean Ubuntu 22.04 droplet.
set -euo pipefail

DOMAIN="goh.nlibera.com"
APP_DIR="/opt/goh"
APP_USER="goh"
LOG_DIR="/var/log/goh"
STATIC_DIR="/var/www/goh"

echo "==> Updating system packages"
apt-get update -y
apt-get upgrade -y
apt-get install -y \
    git curl wget unzip \
    python3.11 python3.11-venv python3.11-dev \
    python3-pip \
    build-essential \
    nginx \
    certbot python3-certbot-nginx \
    ufw

echo "==> Configuring firewall"
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "==> Creating app user: ${APP_USER}"
id -u "${APP_USER}" &>/dev/null || useradd -r -m -d "${APP_DIR}" -s /bin/bash "${APP_USER}"

echo "==> Creating directories"
mkdir -p "${APP_DIR}" "${LOG_DIR}" "${STATIC_DIR}"
chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}" "${LOG_DIR}"
chown -R www-data:www-data "${STATIC_DIR}"

echo "==> Cloning / pulling repository"
if [ -d "${APP_DIR}/.git" ]; then
    git -C "${APP_DIR}" pull
else
    git clone https://github.com/YOUR_ORG/GOH.git "${APP_DIR}"
    chown -R "${APP_USER}:${APP_USER}" "${APP_DIR}"
fi

echo "==> Creating Python virtual environment"
sudo -u "${APP_USER}" python3.11 -m venv "${APP_DIR}/.venv"
sudo -u "${APP_USER}" "${APP_DIR}/.venv/bin/pip" install --upgrade pip
sudo -u "${APP_USER}" "${APP_DIR}/.venv/bin/pip" install -e "${APP_DIR}[prod]"
sudo -u "${APP_USER}" "${APP_DIR}/.venv/bin/pip" install gunicorn

echo "==> Creating .env (fill in secrets!)"
if [ ! -f "${APP_DIR}/.env" ]; then
    cat > "${APP_DIR}/.env" << 'EOF'
GOH_ENV=production
GOH_DATABASE_PATH=/opt/goh/data/goh.db
GOH_SECRET_KEY=CHANGE_ME_generate_with_openssl_rand_hex_32
GOH_JWT_SECRET=CHANGE_ME_generate_with_openssl_rand_hex_32
GOH_JWT_REFRESH_SECRET=CHANGE_ME_generate_with_openssl_rand_hex_32
GOH_SERVER_HOST=127.0.0.1
GOH_SERVER_PORT=5050
EOF
    chown "${APP_USER}:${APP_USER}" "${APP_DIR}/.env"
    chmod 600 "${APP_DIR}/.env"
    echo "!!! EDIT ${APP_DIR}/.env and set real secrets before starting the service !!!"
fi

mkdir -p "${APP_DIR}/data"
chown "${APP_USER}:${APP_USER}" "${APP_DIR}/data"

echo "==> Running database migrations"
sudo -u "${APP_USER}" bash -c "cd ${APP_DIR} && .venv/bin/goh db migrate"

echo "==> Installing nginx config"
cp "${APP_DIR}/deployment/nginx/goh.nlibera.com.conf" \
   "/etc/nginx/sites-available/${DOMAIN}.conf"
ln -sf "/etc/nginx/sites-available/${DOMAIN}.conf" \
       "/etc/nginx/sites-enabled/${DOMAIN}.conf"
rm -f /etc/nginx/sites-enabled/default
nginx -t

echo "==> Installing systemd service"
cp "${APP_DIR}/deployment/systemd/goh-api.service" \
   /etc/systemd/system/goh-api.service
systemctl daemon-reload
systemctl enable goh-api

echo "==> Obtaining SSL certificate (certbot)"
echo "Starting nginx for ACME challenge..."
systemctl start nginx || true
certbot --nginx -d "${DOMAIN}" --non-interactive --agree-tos \
    --email admin@nlibera.com --redirect

echo "==> Starting services"
systemctl start goh-api
systemctl reload nginx

echo ""
echo "=== Setup complete! ==="
echo "Verify: curl https://${DOMAIN}/api/v1/health"
