# mkApi

FastAPI service for Microlab client management, organized with hexagonal
architecture. The domain owns the business rules, application handlers translate
API DTOs into domain models, and infrastructure adapters connect the outside
world to the domain ports.

## Tech stack

- Python 3.14+
- FastAPI
- SQLAlchemy async engine
- asyncpg
- PostgreSQL
- Alembic
- Poetry
- Ruff

## Project structure

```text
.
├── src
│   ├── main.py
│   ├── domain
│   │   ├── api
│   │   │   └── client_service_port.py
│   │   ├── spi
│   │   │   └── client_persistence_port.py
│   │   ├── model
│   │   │   └── client.py
│   │   ├── usecase
│   │   │   └── client_use_case.py
│   │   ├── exception
│   │   └── util
│   ├── application
│   │   ├── dto
│   │   │   ├── request
│   │   │   └── response
│   │   ├── handler
│   │   │   └── impl
│   │   └── mapper
│   └── infrastructure
│       ├── configuration
│       ├── input
│       │   └── rest
│       │       └── exception
│       ├── output
│       │   └── postgresql
│       │       ├── adapter
│       │       ├── database
│       │       ├── entity
│       │       ├── mapper
│       │       ├── migration
│       │       └── repository
│       └── util
├── tests
├── alembic.ini
├── Makefile
├── poetry.lock
└── pyproject.toml
```

## Hexagonal architecture

The code is split by responsibility instead of by framework.

- `domain/` contains the core model, business use cases, exceptions, and ports.
  It does not depend on FastAPI, SQLAlchemy, or PostgreSQL.
- `domain/api/` defines input ports. `ClientServicePort` is the domain contract
  used by the application layer.
- `domain/spi/` defines output ports. `ClientPersistencePort` is the persistence
  contract required by the use case.
- `application/` coordinates API-facing DTOs, handlers, and mappers. It converts
  request objects into domain models and converts domain results back to response
  DTOs.
- `infrastructure/input/rest/` is the driving adapter. It exposes FastAPI routes
  and delegates work to application handlers.
- `infrastructure/output/postgresql/` is the driven adapter. It implements the
  persistence port with SQLAlchemy, PostgreSQL entities, repositories, and
  mappers.
- `infrastructure/configuration/` wires dependencies from adapters to ports.

Current client creation flow:

```text
POST /clients
  -> infrastructure/input/rest/client_controller.py
  -> application/handler/impl/client_handler.py
  -> domain/api/client_service_port.py
  -> domain/usecase/client_use_case.py
  -> domain/spi/client_persistence_port.py
  -> infrastructure/output/postgresql/adapter/client_persistence_adapter.py
  -> infrastructure/output/postgresql/repository/client_repository.py
  -> PostgreSQL
```

## API

### Create client

```http
POST /clients
Content-Type: application/json
```

Request body:

```json
{
  "name": "Acme Labs",
  "email": "contact@acme.test",
  "phone": "3001234567",
  "nit": "900123456",
  "address": "Main Street 123"
}
```

Successful response:

```http
201 Created
```

```json
{
  "id": "f2edbd83-8ea3-4f95-bc4b-28d33e40f81d",
  "name": "Acme Labs",
  "email": "contact@acme.test",
  "phone": "3001234567",
  "nit": "900123456",
  "address": "Main Street 123"
}
```

## Setup

Install dependencies:

```sh
poetry install
```

The application reads configuration exclusively from the process environment;
it does not select or load a `.env` file. Configure at least:

```sh
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/microlab
JWT_SECRET_KEY=<a-random-secret-with-at-least-32-characters>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_SECONDS=900
REFRESH_TOKEN_EXPIRATION_SECONDS=2592000
```

Generate a suitable secret with `openssl rand -hex 32`. Do not commit or reuse
the production secret; the application refuses to start when it is missing or
shorter than 32 characters.

In production, inject these variables through the deployment platform or a
secret manager. For Docker Compose, choose the file externally when starting
the stack:

```sh
docker compose --env-file /secure/path/mkapi.env up --build
```

Compose resolves that file and explicitly passes the required values into the
container. For a direct local run, export the variables in the shell before
starting Uvicorn. This keeps environment selection outside the application.

The current PostgreSQL session configuration points to:

```text
postgresql+asyncpg://postgres:0000@localhost:5432/microlab
```

Make sure that database exists and is reachable before running migrations or the
API.

## Run

Run the API with the Makefile:

```sh
make run
```

For local development, `make run` loads `.env.dev` before starting the API.
The application itself still reads only process environment variables. To use a
different local file:

```sh
make run ENV_FILE=.env.local
```

Equivalent command:

```sh
poetry run uvicorn main:app --reload --app-dir src
```

After startup, the interactive docs are available at:

```text
http://127.0.0.1:8000/docs
```

## Docker

Run the API with PostgreSQL in Docker:

```sh
make docker-up
```

Apply database migrations in the Docker PostgreSQL database:

```sh
make docker-migrate
```

Stop the Docker stack:

```sh
make docker-down
```

This starts two services:

- `postgres`, available to the API as `postgres:5432`
- `api`, available on `http://127.0.0.1:8000`

If port `5432` is already used on your machine, change the host port for the
PostgreSQL container:

```sh
make docker-up POSTGRES_HOST_PORT=5433
```

## Database migrations

Create a new Alembic revision:

```sh
make revision m="describe change"
```

Apply migrations:

```sh
make migrate
```

Authentication stores hashed, rotating refresh tokens in the `refresh_tokens`
table. Apply the latest migration before using `POST /auth/refresh` or
`POST /auth/logout`. Access tokens remain stateless and short-lived. As with
`make run`, migration commands load `ENV_FILE` (default: `.env.dev`) externally
through the Makefile.

Each login creates an independent refresh-token family. Rotation links the old
token to its replacement. Reuse of an already rotated token is treated as a
possible theft and revokes the entire family; logout also revokes that session's
family without closing sessions created by other logins.

Rollback the latest migration:

```sh
make downgrade
```

Inspect migration state:

```sh
make current
make history
```

## Quality

Run Ruff checks:

```sh
make lint
```

Format code:

```sh
make format
```

Run both lint and format verification:

```sh
make quality
```

Clean local caches:

```sh
make clean
```

## Development notes

- Keep business rules inside `domain/usecase`.
- Add input adapters under `infrastructure/input`.
- Add output adapters under `infrastructure/output`.
- Depend on domain ports from the outside layers, not on concrete adapters.
- Wire concrete implementations in `infrastructure/configuration/dependencies.py`.
