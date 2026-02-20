# Guilds of Heroes (GOH) — Coding Standards

## Stack
- **Backend**: Python 3.10+, Flask (HTTP adapter ONLY), Gunicorn, Click (CLI)
- **Database**: SQLite (WAL mode), raw SQL (NO ORM)
- **Frontend**: React 18 + TypeScript + Vite
- **Auth**: JWT (access+refresh), magic link, OAuth (Google/Discord), username+password (bcrypt)
- **Logging**: structlog (JSON prod, console dev)
- **Deploy**: nginx, systemd, DigitalOcean droplet

## Architecture — Headless-First, Paper-Thin Flask

```
goh/          # Pure Python business logic (ZERO Flask imports)
  domain/     # Frozen dataclasses, AppError hierarchy
  repositories/  # Raw SQL, returns domain entities
  services/   # Business logic, takes db: Connection as 1st arg
  db/         # SQLite connection factory, migrations
  observability/  # structlog, correlation IDs, timing, metrics

cli/          # Click CLI (headless-first interface)
api/          # Flask HTTP adapter (PAPER THIN)
frontend/     # React + Vite + TypeScript
```

## Key Rules

1. **Flask routes ONLY**: parse request → call service → format response. ZERO business logic in routes.
2. **Zero Flask imports** in `goh/` (domain, services, repositories). They are pure Python.
3. **Every service function** takes `db: sqlite3.Connection` as first argument.
4. **Every feature** is CLI-first: implement and test via Click before adding API routes.
5. **Raw SQL only** — NO ORM, NO query builders. SQLite with WAL mode.
6. **All IDs** are INTEGER PRIMARY KEY. All timestamps are ISO8601 TEXT.

## Code Standards

- **Fully typed**: All function signatures have type hints. Use `mypy --strict`.
- **No bare `except`**: Always catch specific exceptions.
- **Custom exceptions**: Use `AppError` hierarchy from `goh/domain/exceptions.py`.
- **No magic numbers**: Use named constants or config values.
- **No `print()`**: Use structlog logger ONLY.
- **Structured logging**: Every log includes correlation_id, timestamp, module, level.

## Observability (NON-NEGOTIABLE)

- **structlog**: JSON renderer in prod, console in dev.
- **Correlation ID**: `contextvars.ContextVar`. CLI generates at start, Flask reads `X-Correlation-Id` or generates new.
- **@timed decorator**: Logs start/end/duration. WARNING if > 500ms.
- **Health endpoints**: `/api/v1/health` (liveness), `/api/v1/health/deep` (DB + metrics).
- **Error responses**: Always include `correlation_id`.
- **Audit log**: Every write operation logged to `audit_log` table.

## Testing

- **Framework**: pytest
- **CLI tests**: Click `CliRunner`
- **API tests**: `httpx` with `WSGITransport`
- **DB tests**: In-memory SQLite (`:memory:`)
- **Coverage target**: All services, all CLI commands, all API endpoints

## NEVER Do

- Import Flask in `goh/` (domain, services, repositories)
- Use an ORM or query builder
- Use bare `except:`
- Use `print()` — structlog only
- Put secrets in code — use environment variables via config/settings.py
- Put business logic in Flask routes
- Skip correlation IDs in logs or error responses
