# ClickAdvisor MCP Server
# Supports:
#   Local:   docker run -p 8000:8000 clickadvisor-mcp
#   Railway: auto-detects PORT env var

FROM python:3.11-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.2

# Copy only dependency files first (layer cache)
COPY pyproject.toml poetry.lock* ./

# Install dependencies without dev extras
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Copy source
COPY clickadvisor/ ./clickadvisor/
COPY README.md ./

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/health || exit 1

# Railway / Render inject PORT automatically; fall back to 8000 locally
ENV PORT=8000

EXPOSE ${PORT}

CMD ["sh", "-c", "python -m clickadvisor.mcp_server --transport sse --host 0.0.0.0 --port ${PORT}"]
