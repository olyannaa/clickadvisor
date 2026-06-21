FROM python:3.12-slim AS builder

WORKDIR /app

RUN pip install poetry==2.4.1

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root --without dev

COPY . .

RUN poetry install --without dev

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["chadvisor"]
CMD ["--help"]
