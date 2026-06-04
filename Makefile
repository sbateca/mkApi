.PHONY: run test lint lint-fix format format-check quality clean revision migrate downgrade current history

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
