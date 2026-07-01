# MCP Deployment Options

ClickAdvisor exposes MCP in two deployment profiles:

- local stdio MCP for developer machines and IDE/desktop clients;
- Streamable HTTP MCP for remote-compatible demos and shared environments.

The trusted analysis path is the same in both profiles: deterministic
ClickAdvisor tools produce the findings.

## Option 1: Local MCP Server

Best for daily use and enterprise-safe workflows.

```bash
poetry run chadvisor mcp-server
```

Example Claude Desktop config:

```json
{
  "mcpServers": {
    "clickadvisor": {
      "command": "poetry",
      "args": ["run", "chadvisor", "mcp-server"],
      "cwd": "/path/to/clickadvisor"
    }
  }
}
```

Use this when the SQL should stay on the user's laptop or inside the company
network.

## Option 2: Local HTTP Endpoint For Demo

Best for testing Streamable HTTP clients on the same machine.

```bash
poetry run chadvisor mcp-http-server \
  --host 127.0.0.1 \
  --port 8765 \
  --path /mcp
```

Endpoint:

```text
http://127.0.0.1:8765/mcp
```

If you need to expose the local endpoint through a temporary tunnel, bind the
server to `0.0.0.0` so the tunneled Host header is accepted:

```bash
poetry run chadvisor mcp-http-server \
  --host 0.0.0.0 \
  --port 8765 \
  --path /mcp
```

Then, in another terminal:

```bash
cloudflared tunnel --url http://127.0.0.1:8765 --no-autoupdate
```

Cloudflare prints a temporary URL:

```text
https://<random-name>.trycloudflare.com/mcp
```

This is useful for quick checks, but it is not a stable production/demo URL.
The link exists only while the local server and tunnel process are running.

## Option 3: Remote Demo Endpoint

Best for a defense/demo where experts should be able to connect without
installing the repository.

Recommended setup:

```text
MCP client
   |
   v
HTTPS/auth proxy or tunnel
   |
   v
chadvisor mcp-http-server on a controlled host
```

Reasonable places to host the demo endpoint:

- a small VPS with HTTPS reverse proxy and an access token;
- Railway/Render/Fly.io style Python service deployment;
- Cloudflare Tunnel or similar tunnel in front of a local machine;
- Tailscale/Funnel for a controlled private demo network.

Do not expose a writable or unauthenticated MCP endpoint publicly. The official
MCP transport guidance requires special care for remote HTTP servers: validate
origins, bind local servers to localhost by default, and use proper
authentication for remote connections.

### Fast path: Railway

Railway is the fastest path when the goal is "give experts a public URL during
the defense".

1. Push this repository to GitHub.
2. Open Railway and create a new project from the GitHub repository.
3. Railway reads `railway.json` and builds the root `Dockerfile`.
4. In service variables, keep:

```text
PORT=8000
MCP_PATH=/mcp
```

5. Open the service settings and generate a public domain.

Result:

```text
https://<your-service>.up.railway.app/mcp
```

This endpoint is suitable for demo SQL and read-only testing. If experts will
send real company SQL, use local MCP instead.

### Alternative: Render

Render is a good option when you want a stable paid web service with a clear
dashboard and HTTPS domain.

1. Push this repository to GitHub.
2. In Render, create a Blueprint from the repo, or create a Web Service
   manually.
3. If using the Blueprint, Render reads `render.yaml`.
4. If creating manually, set:

```text
Environment: Docker
Dockerfile Path: ./Dockerfile
Docker Context: .
PORT=8000
MCP_PATH=/mcp
```

Result:

```text
https://<your-service>.onrender.com/mcp
```

For a short defense demo, use a paid instance or warm the service before the
presentation so the first connection is not delayed by cold start.

### Alternative: Fly.io

Fly.io is useful if you prefer CLI-based deploys and regional placement.

Example `fly.toml` build section:

```toml
[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"
  MCP_PATH = "/mcp"
```

Then:

```bash
fly launch --no-deploy
fly deploy
```

Result:

```text
https://<your-app>.fly.dev/mcp
```

### What the Docker image contains

The root `Dockerfile` is intentionally MCP-only and lightweight. It installs
only the packages needed for deterministic SQL analysis and Streamable HTTP
MCP:

- `mcp`
- `typer`
- `rich`
- `sqlglot`
- `PyYAML`
- `httpx`

It does not install `sentence-transformers`, Torch, CatBoost, scikit-learn, or
the local Qdrant retrieval stack. That keeps public demo deploys fast and
predictable. Full local development and DS experiments still use:

```bash
poetry install
```

## What To Tell Experts During A Demo

There are two safe test paths:

1. Local install:

```bash
git clone https://github.com/olyannaa/clickadvisor.git
cd clickadvisor
poetry install
poetry run chadvisor mcp-server
```

2. Remote demo endpoint:

```text
https://your-demo-domain.example/mcp
```

The remote endpoint should be used only with demo SQL or explicitly approved
queries, because anything sent to the remote MCP endpoint leaves the expert's
machine.
