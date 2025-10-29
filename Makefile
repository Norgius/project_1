lint: ## Проверяет линтерами код в репозитории
	uvx --python 3.12 ruff check ./
	uvx --python 3.12 --with pydantic mypy ./

format: ## Запуск автоформатера
	uvx --python 3.12 ruff check --fix ./

test: ## Запустить тесты
	docker compose run --rm --workdir /opt/app/ backend pytest -s
