FROM python:3.12-slim AS builder
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv sync --no-dev

FROM python:3.12-slim AS runtime
WORKDIR /app
RUN apt-get update && apt-get install -y graphviz && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/.venv /app/.venv
COPY wiki_server/ wiki_server/
ENV PATH="/app/.venv/bin:$PATH"
RUN playwright install chromium --with-deps
EXPOSE 5000
CMD ["flask", "--app", "wiki_server.app", "run", "--host", "0.0.0.0", "--port", "5000"]
