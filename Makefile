IMAGE_NAME ?= mkapi
HOST_PORT ?= 8000
POSTGRES_HOST_PORT ?= 5433
ENV_FILE ?= .env.dev

.PHONY: check-env-file run run-otel test test-coverage lint lint-fix format format-check quality clean docker-up-dev docker-up-prod docker-down docker-logs docker-logs-otel docker-migrate revision migrate downgrade current history

check-env-file:
	@test -f "$(ENV_FILE)" || (echo "Environment file not found: $(ENV_FILE)" && exit 1)

run: check-env-file
	@set -a; \
	. "$(ENV_FILE)"; \
	set +a; \
	exec poetry run uvicorn main:app --reload --app-dir src

run-otel: check-env-file
	@set -a; \
	. "$(ENV_FILE)"; \
	set +a; \
	OTEL_SERVICE_NAME=mk-api-dev \
	OTEL_RESOURCE_ATTRIBUTES=service.name=mk-api-dev,service.version=0.1.0,deployment.environment=development,service.namespace=mkapi \
	OTEL_TRACES_EXPORTER=otlp \
	OTEL_METRICS_EXPORTER=otlp \
	OTEL_LOGS_EXPORTER=otlp \
	OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318 \
	OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf \
	OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED=true \
	OTEL_PYTHON_LOG_LEVEL=info \
	exec poetry run opentelemetry-instrument uvicorn main:app --reload --app-dir src

test:
	poetry run pytest

test-coverage:
	poetry run pytest --cov=src --cov-report=term --cov-report=xml

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check . --fix

format:
	poetry run ruff format .

format-check:
	poetry run ruff format . --check

quality:
	poetry run ruff check .
	poetry run ruff format . --check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .coverage coverage.xml htmlcov

docker-up-dev:
	docker compose --env-file .env.dev up --build

docker-up-prod:
	docker compose --env-file .env.prod up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-logs-otel:
	docker logs -f otel-collector

docker-migrate:
	docker compose --env-file .env.dev exec mkapi poetry run alembic upgrade head

revision: check-env-file
	@set -a; . "$(ENV_FILE)"; set +a; \
	exec poetry run alembic revision --autogenerate -m "$(m)"

migrate: check-env-file
	@set -a; . "$(ENV_FILE)"; set +a; \
	exec poetry run alembic upgrade head

downgrade: check-env-file
	@set -a; . "$(ENV_FILE)"; set +a; \
	exec poetry run alembic downgrade -1

current: check-env-file
	@set -a; . "$(ENV_FILE)"; set +a; \
	exec poetry run alembic current

history: check-env-file
	@set -a; . "$(ENV_FILE)"; set +a; \
	exec poetry run alembic history
