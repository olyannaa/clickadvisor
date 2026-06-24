# MCP Server

ClickAdvisor supports Model Context Protocol (MCP) for integration with Claude
Desktop, Cursor, Continue, Zed, and other AI-agent clients.

The MCP server uses stdio transport and wraps the same local analysis pipeline as
the CLI. SQL and metadata do not leave your machine.

## Start the server manually

```bash
poetry run chadvisor mcp-server
```

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

## Prompts

The server exposes MCP prompts for slash-command style workflows:

- `analyze` — asks the client to analyze SQL using `analyze_query`
- `explain` — asks the client to explain why a query is slow using
  `analyze_query` with `mode='explain'`

## Compatibility

The server is tested with the Python `mcp` package over stdio transport and is
compatible with MCP clients that support tools and prompts over stdio.
