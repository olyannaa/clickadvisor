# MCP Server

ClickAdvisor supports Model Context Protocol (MCP) for integration with Claude
Desktop, Cursor, Continue, Zed, and other AI-agent clients.

The MCP server uses stdio transport and wraps the same local analysis pipeline as
the CLI. SQL and metadata do not leave your machine.

MCP is an interface, not a second optimizer. The trusted findings still come
from the deterministic ClickAdvisor rule engine.

## Start the server manually

```bash
poetry run chadvisor mcp-server
```

This starts the local stdio MCP server.

For Streamable HTTP MCP:

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

For a remote demo, expose this endpoint only through HTTPS and authentication.
See [MCP Deployment Options](mcp-deployment.md).

## Connect To Public Remote MCP

Remote MCP clients connect to ClickAdvisor through the hosted Streamable HTTP
endpoint:

```text
https://clickadvisor-mcp-production.up.railway.app/mcp
```

Claude / Anthropic API URL-based server config:

Claude / Claude Desktop:

```text
Customize -> Connectors -> Add custom connector
Name: ClickAdvisor
URL:  https://clickadvisor-mcp-production.up.railway.app/mcp
```

Claude Code:

```bash
claude mcp add --transport http clickadvisor \
  https://clickadvisor-mcp-production.up.railway.app/mcp
```

Anthropic API:

```json
{
  "mcp_servers": [
    {
      "type": "url",
      "name": "clickadvisor",
      "url": "https://clickadvisor-mcp-production.up.railway.app/mcp"
    }
  ]
}
```

Opening the endpoint in a browser can return `Not Acceptable: Client must
accept text/event-stream`. This is expected for Streamable HTTP MCP; use an MCP
client or MCP Inspector to test the tool calls.

## Connect to Claude Desktop

Add this to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "clickadvisor": {
      "command": "poetry",
      "args": ["run", "chadvisor", "mcp-server"],
      "cwd": "/путь/к/вашему/проекту/CLI"
    }
  }
}
```

Restart Claude Desktop after changing the config.

## Connect after package publication

```json
{
  "mcpServers": {
    "clickadvisor": {
      "command": "chadvisor",
      "args": ["mcp-server"]
    }
  }
}
```

## Tools

### `analyze_query`

Analyzes ClickHouse SQL and returns a Markdown report.

Arguments:

- `sql` (required)
- `ch_version` (optional)
- `schema_ddl` (optional)
- `mode`: `diagnose` or `explain`

If the user mentioned a ClickHouse version, pass it as `ch_version`. If the user
mentioned a cluster address, call `detect_ch_version` first and pass the result
into `analyze_query`.

### `analyze_query_json`

Analyzes ClickHouse SQL and returns structured JSON. RAG findings are excluded
from this output so downstream automation receives deterministic rule findings.

Arguments:

- `sql` (required)
- `ch_version` (optional)
- `schema_ddl` (optional)

### `list_rules`

Returns available optimization rules grouped by tier.

Arguments:

- `tier`: `1A`, `1B`, `1C`, `detector`, or `all`

### `detect_ch_version`

Connects to a ClickHouse HTTP endpoint and returns the server version when
available.

Arguments:

- `connect_url` (required), e.g. `http://localhost:8123`
- `user` (default: `default`)
- `password` (default: empty string)

## Recommended Agent Workflow

Use this instruction in MCP-capable AI clients:

```text
When reviewing ClickHouse SQL, call the local ClickAdvisor MCP tool first.
Do not invent optimization advice. Summarize returned rule_id, severity, tier,
confidence, and suggestion. If ClickAdvisor returns no finding, say that no
deterministic issue was found and list remaining manual checks separately.
```

This workflow lowers hallucination risk because the AI client formats and
explains structured findings instead of becoming the source of the finding set.

## Security Boundary

The MCP process runs locally. ClickAdvisor itself does not send SQL, DDL,
EXPLAIN, or environment context to an external LLM provider.

If you connect the local MCP server to an external AI client, data exposure is
controlled by what you send to that client and by your organization's policy for
that client. Treat SQL and query context as sensitive.

More details:

- [MCP Deployment Options](mcp-deployment.md)
- [AI And MCP Workflow](ai-mcp-workflow.md)
- [Security And Local-First Runtime](security-local-first.md)

## Prompts

The server exposes MCP prompts for slash-command style workflows:

- `analyze` — asks the client to analyze SQL using `analyze_query`
- `explain` — asks the client to explain why a query is slow using
  `analyze_query` with `mode='explain'`

## Compatibility

The server is tested with the Python `mcp` package over stdio and Streamable
HTTP transports. It is compatible with MCP clients that support tools and
prompts over stdio, and with clients that can connect to a Streamable HTTP MCP
endpoint such as `/mcp`.
