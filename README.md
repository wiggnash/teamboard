# TeamBoard

A Django + Django REST Framework backend for a **B2B AI Knowledge Base API**.

Customer companies register, receive an API key and a JWT, and query a curated Q&A
knowledge base. Every query is logged so a platform admin can view usage statistics.

## Features

- **JWT authentication** (via `djangorestframework-simplejwt`) — every endpoint is protected
  by default; the public auth endpoints opt out explicitly.
- **Auto-provisioned API keys** — a `post_save` signal creates a `Company` profile and
  generates a secure `api_key` whenever a `User` registers.
- **Knowledge base search** — case-insensitive search across questions and answers, with every
  query logged atomically.
- **Usage dashboard** — admin-only aggregate statistics over all logged queries.

## Tech stack

| Concern | Choice |
|---------|--------|
| Framework | Django + Django REST Framework |
| Auth | `djangorestframework-simplejwt` (JWT) |
| Database | PostgreSQL (with a SQLite fallback for quick local dev) |
| Package / env manager | [`uv`](https://docs.astral.sh/uv/) |
| Config | `.env` via `python-dotenv` |

## Project structure

The project is split into three domain apps (apps own data; views orchestrate across them):

| App | Responsibility |
|-----|----------------|
| `companies` | `Company` model, register/login, the User→Company signal, admin permission |
| `kb_entries` | `KBEntry` model, knowledge base query endpoint |
| `query_logs` | `QueryLog` model, admin usage-summary endpoint |

## API endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register/` | Public | Register a company; returns JWT + API key |
| POST | `/api/auth/login/` | Public | Log in; returns JWT + company name + API key |
| POST | `/api/kb/query/` | JWT | Search the knowledge base (logs the query) |
| GET | `/api/admin/usage-summary/` | JWT + admin | Platform-wide usage statistics |

## Getting started

### Prerequisites

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- PostgreSQL (optional — SQLite works out of the box for local dev)

### 1. Install dependencies

```bash
uv sync
```

### 2. Configure environment

```bash
cp .env.example .env
```

The database is controlled by the `NODB` flag in `.env`:

- `NODB=true` → use **SQLite** (zero setup; good for local development)
- `NODB=false` → use **PostgreSQL** with the `DB_*` values from `.env`

```env
NODB=true

DB_NAME=teamboard
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

To use PostgreSQL, create the database first, then set `NODB=false`:

```sql
CREATE DATABASE teamboard;
```

### 3. Apply migrations

```bash
uv run python manage.py migrate
```

### 4. Run the server

```bash
uv run python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/`.

### 5. Seed the knowledge base

> _Seeding command / fixtures to be added._

## Development

Run Django's system checks:

```bash
uv run python manage.py check
```

Regenerate the pinned requirements file (for environments that don't use `uv`):

```bash
uv export --format requirements-txt > requirements.txt
```
