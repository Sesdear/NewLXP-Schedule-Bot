FROM python:3.11-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create true \
    && poetry config virtualenvs.in-project true \
    && poetry config installer.max-workers 1 \
    && poetry config requests.max-retries 5 \
    && poetry install --only main --no-root --no-interaction --no-ansi


FROM python:3.11-slim AS runtime

WORKDIR /app

COPY --from=builder /build/.venv /app/.venv
COPY app ./app

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "app/bot.py"]