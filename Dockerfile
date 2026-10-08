FROM python:3.12-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

COPY src ./src

RUN uv sync --frozen

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${APP_PORT:-8000}"]