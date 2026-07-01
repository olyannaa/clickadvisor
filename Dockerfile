FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    MCP_PATH=/mcp \
    PYTHONPATH=/app

COPY requirements-mcp.txt ./
RUN pip install --no-cache-dir -r requirements-mcp.txt

COPY clickadvisor/ ./clickadvisor/
COPY docs/rules/cards/ ./docs/rules/cards/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os, socket; s=socket.create_connection(('127.0.0.1', int(os.environ.get('PORT', '8000'))), 5); s.close()"

CMD ["sh", "-c", "python -c 'import os; from clickadvisor.mcp_server.server import run_http; run_http(host=\"0.0.0.0\", port=int(os.environ.get(\"PORT\", \"8000\")), path=os.environ.get(\"MCP_PATH\", \"/mcp\"))'"]
