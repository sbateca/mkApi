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

Equivalent command:

```sh
poetry run uvicorn main:app --reload --app-dir src
```

After startup, the interactive docs are available at:

```text
http://127.0.0.1:8000/docs
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
