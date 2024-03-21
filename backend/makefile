include .env

VERSION=$$(git describe --always --tags)

dev:
	CONFIG_PATH=$(CONFIG_PATH) PYTHONPATH=./ poetry run python ./src/main

mypy:
	poetry run mypy src tests

lint:
	poetry run ruff check src

lint-fix:
	poetry run ruff check src --fix

pytest:
	poetry run pytest -vv -s --disable-warnings tests

format:
	@echo "Форматирование"
	poetry run ruff format src
