FROM python:3.11-slim AS builder

ENV POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml README.md ./
COPY clickadvisor ./clickadvisor

RUN poetry install --only main --no-interaction --no-ansi

FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin
COPY clickadvisor ./clickadvisor
COPY README.md pyproject.toml ./

ENTRYPOINT ["python", "-m", "clickadvisor"]
CMD ["--help"]
