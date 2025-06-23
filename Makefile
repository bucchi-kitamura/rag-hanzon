format:
	uv run ruff format src/

lint:
	uv run ruff check src/

lint-fix:
	uv run ruff check src/ --fix

test:
	uv run python -m pytest tests/