---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"How
topic: how-to-build-ai-agents-with-mcp-12-framework-comparison-2025-clickhouse
ch_version_introduced: '3.10'
last_updated: '2026-09-07'
chunk_index: 20
total_chunks_in_doc: 22
---

with error handling. The frameworks in this guide handle all of this complexity for you. Even lightweight options like the OpenAI Agents SDK are easier than rolling your own. ### How do I debug MCP connection issues? \#

Start by checking the MCP server logs \- most servers provide detailed logging. Common issues include authentication failures (check your environment variables), network connectivity (ensure the host is reachable), and timeout errors (increase connection timeout). Use the `--verbose` flag when running MCP servers locally to see detailed debug output.

### What's the difference between local and remote MCP servers? \#

Local MCP servers run as subprocess on your machine using stdio communication \- they're started and stopped by your agent. Remote MCP servers run as standalone services accessed over HTTP/WebSocket, supporting multiple concurrent clients. Local servers are simpler to set up but don't scale. Remote servers require more infrastructure but support production workloads.

### Can MCP servers modify data or only read it? \#

MCP servers can provide any tools they want, including destructive operations. The ClickHouse MCP server intentionally only provides `run_select_query` to prevent accidental data modification, but other servers might offer write operations. Always review which tools an MCP server exposes, especially in production. The Claude Agent SDK's allowlist approach is good practice here.

### How do I handle MCP server authentication? \#

Authentication is handled through environment variables passed to the MCP server on startup. Each server defines its own auth requirements \- ClickHouse uses standard database credentials, GitHub uses personal access tokens, etc. Store credentials securely (use environment variables, not hardcoded values) and ensure they have minimal required permissions.

### What happens if an MCP tool call fails? \#

Error handling varies by framework. Most will return the error to the LLM, which can then decide whether to retry, try a different approach, or report the failure. Some frameworks like Agno include automatic retry logic. You should implement timeout handling and consider circuit breakers for production deployments.

### Can I create custom MCP servers? \#

Yes, MCP is an open protocol. [You can build MCP servers in Python](https://modelcontextprotocol.io/docs/develop/build-server), TypeScript, or any language that can handle JSON\-RPC over stdio or HTTP. The [MCP SDK](https://github.com/modelcontextprotocol/python-sdk) provides templates and utilities. Custom servers are useful for exposing internal APIs or building domain\-specific tools.
