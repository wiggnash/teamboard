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
| POST | `/api/companies/auth/register/` | Public | Register a company; returns JWT + API key |
| POST | `/api/companies/auth/login/` | Public | Log in; returns JWT + company name + API key |
| POST | `/api/kb_entries/query/` | JWT | Search the knowledge base (logs the query) |
| GET | `/api/query_logs/admin/usage-summary/` | JWT + admin | Platform-wide usage statistics |

### Authentication

Auth is **JWT-by-default**: every endpoint requires a `Bearer` access token except the two
public auth endpoints. After registering or logging in, send the returned `access` token on
every protected request:

```
Authorization: Bearer <access-token>
```

Identity is always derived from the token (`request.user.company`) — a company ID is never
read from the request body. The `api_key` is the company's stable credential, but request
auth itself is via JWT.

### `POST /api/companies/auth/register/`

Creates a `User`; a `post_save` signal then auto-creates the `Company` and generates the
`api_key` (`secrets.token_urlsafe(32)`). `role` always defaults to `client` — it is never
accepted from the body. Returns `400` if the username is already taken.

```jsonc
// request
{
  "username": "acmecorp",
  "password": "securepass123",
  "company_name": "Acme Corp",
  "email": "dev@acmecorp.com"
}
// response 201
{
  "username": "acmecorp",
  "company_name": "Acme Corp",
  "api_key": "gT8x...auto-generated...",
  "access": "eyJhbGciOiJIUzI1NiI..."
}
```

### `POST /api/companies/auth/login/`

Validates credentials with Django's `authenticate()`. Returns `401` on bad credentials.

```jsonc
// request
{ "username": "acmecorp", "password": "securepass123" }
// response 200
{
  "username": "acmecorp",
  "company_name": "Acme Corp",
  "api_key": "gT8x...",
  "access": "eyJhbGciOiJIUzI1NiI..."
}
```

### `POST /api/kb_entries/query/` (JWT)

Searches `question` and `answer` (case-insensitive, `Q(...__icontains)`). The search and the
`QueryLog` write happen in a single `transaction.atomic()` block. The query is **always
logged**, even when nothing matches — a zero-result search returns `count: 0` with an empty
list (never `404`), because billing counts queries made, not answers found. Returns `400` if
`search` is missing/blank and `401` without a token.

```jsonc
// request
{ "search": "authenticate" }
// response 200
{
  "search": "authenticate",
  "count": 2,
  "results": [
    {
      "id": 2,
      "question": "How do I authenticate requests to an API?",
      "answer": "Common API authentication methods include API keys, JWT tokens...",
      "category": "api"
    }
  ]
}
```

### `GET /api/query_logs/admin/usage-summary/` (JWT + admin)

Admin-only platform statistics, gated by a custom `IsAdminUser` permission that checks
`request.user.company.role == Company.Role.ADMIN` (not Django's `is_staff`/`is_superuser`).
A regular client receives `403`; a missing token receives `401`.

```jsonc
// response 200
{
  "total_queries": 284,
  "active_companies": 7,
  "top_search_terms": [
    { "search_term": "select_related", "count": 42 },
    { "search_term": "transaction atomic", "count": 31 }
  ]
}
```

Stats are computed with ORM aggregations: `aggregate(Count('id'))` for `total_queries`,
`values('company').distinct().count()` for `active_companies`, and
`values('search_term').annotate(count=Count('id')).order_by('-count')[:5]` for the top terms.

## Getting started

### Prerequisites

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- PostgreSQL (optional — SQLite works out of the box for local dev)

### 1. Install dependencies (with `uv`)

This project is managed entirely with [`uv`](https://docs.astral.sh/uv/) — **do not** create a
venv by hand or run `pip install`. `uv` reads `pyproject.toml` + `uv.lock` and builds a fully
pinned environment for you.

First, install `uv` itself (skip if you already have it):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, from the project root, install all dependencies into a project-local `.venv`:

```bash
uv sync
```

> **Run every command through `uv run`** (e.g. `uv run python manage.py migrate`). This
> guarantees the command uses the project's `.venv` — you never need to manually `activate`
> the environment. Running `python manage.py ...` directly may use the wrong interpreter.

If you are deploying somewhere without `uv`, a pinned `requirements.txt` is also committed and
can be used with `pip install -r requirements.txt` instead.

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

A management command loads 26 starter Q&A entries across all categories (API, Database,
Cloud, Framework, General). Keywords intentionally overlap so a single search term matches
multiple entries:

```bash
uv run python manage.py seed_kb
```

### 6. Create an admin (for the usage-summary endpoint)

Every company registers as a `client` by default. To access `usage-summary`, promote a
company to `admin`. The role is read live from the DB on each request, so an existing token
starts working immediately — no re-login required. Either flip the `role` column in the DB
(e.g. PGAdmin), or use the Django shell:

```bash
uv run python manage.py shell -c "from companies.models import Company; c = Company.objects.get(company_name='Acme Corp'); c.role = Company.Role.ADMIN; c.save()"
```

## Development

Run Django's system checks:

```bash
uv run python manage.py check
```

Regenerate the pinned requirements file (for environments that don't use `uv`):

```bash
uv export --format requirements-txt > requirements.txt
```
