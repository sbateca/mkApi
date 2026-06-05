IMAGE_NAME ?= mkapi
HOST_PORT ?= 8000
POSTGRES_HOST_PORT ?= 5433

.PHONY: run test lint lint-fix format format-check quality clean docker-up docker-down docker-logs docker-migrate revision migrate downgrade current history

run:
	poetry run uvicorn main:app --reload --app-dir src

test:
	poetry run pytest

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
	find . -type d -name ".mypy_cache" -exec rm -rf {} +


docker-up:
	IMAGE_NAME=$(IMAGE_NAME) HOST_PORT=$(HOST_PORT) POSTGRES_HOST_PORT=$(POSTGRES_HOST_PORT) docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f api postgres

docker-migrate:
	docker compose exec -T api alembic upgrade head

revision:
	PYTHONPATH=src poetry run alembic revision --autogenerate -m "$(m)"

migrate:
	PYTHONPATH=src poetry run alembic upgrade head

downgrade:
	PYTHONPATH=src poetry run alembic downgrade -1

current:
	PYTHONPATH=src poetry run alembic current

history:
	PYTHONPATH=src poetry run alembic history
