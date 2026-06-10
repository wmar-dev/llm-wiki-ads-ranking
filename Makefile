.PHONY: install serve dev test lint docker-build docker-up docker-down index render-dot validate-mermaid

install:
	uv sync --all-extras && uv run playwright install chromium

serve:
	uv run flask --app wiki_server.app run --host 127.0.0.1 --port 5000

dev:
	uv run flask --app wiki_server.app run --host 127.0.0.1 --port 5000 --debug

test:
	uv run pytest tests/ -v

lint:
	uv run ruff check wiki_server/ tests/

docker-build:
	docker build -t llm-wiki .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

index:
	uv run python -m wiki_server.search rebuild

render-dot:
	uv run python scripts/render_dot.py --all

validate-mermaid:
	uv run python scripts/validate_mermaid.py --all
