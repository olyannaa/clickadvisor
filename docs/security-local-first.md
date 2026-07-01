# Security And Local-First Runtime

ClickAdvisor is designed for teams that treat SQL, DDL, EXPLAIN output,
environment metadata, and query-log metadata as sensitive information.

## Trusted Local Path

The trusted runtime path is local:

```text
SQL / DDL / EXPLAIN / environment / query_log export
        |
        v
Local ClickAdvisor process
        |
        v
Deterministic findings / workload report
```

The rule engine, workload prototype, retrieval index, and MCP server run in the
user's environment. ClickAdvisor does not need a remote generative LLM to
produce recommendations.

## What ClickAdvisor Reads

Depending on the command and options, ClickAdvisor may read:

- SQL text;
- optional schema DDL;
- optional EXPLAIN output;
- optional environment JSON;
- optional sanitized `system.query_log` CSV export;
- ClickHouse version through `SELECT version()` when `--connect` is used;
- planner estimates through `EXPLAIN ESTIMATE` only when explicitly enabled.

## What ClickAdvisor Does Not Read

By design, ClickAdvisor does not need to read query result data or table rows.
It also does not run `ANALYZE`, apply DDL, mutate tables, or execute user SQL as
part of the default analysis path.

## MCP Boundary

The MCP server is local and wraps the same analysis pipeline as the CLI. This
reduces hallucination risk because an AI client can call a deterministic local
tool instead of inventing advice.

There is still an important boundary: if the user connects the local MCP server
to an external AI client, what the client sees depends on what the user sends to
that client and on the organization's policy for that AI tool. ClickAdvisor
does not silently send SQL to external providers.

## Query Log Privacy

`system.query_log` can contain sensitive literals, identifiers, internal table
names, usernames, service names, and workload timing. For enterprise use:

- export only the columns needed for analysis;
- prefer normalized queries or redact literals before sharing CSV files;
- keep exports local;
- use a read-only ClickHouse user for collection;
- treat query-log CSV files as sensitive artifacts.

The current workload prototype groups queries by normalized SQL and replaces
string/numeric literals in fingerprints. A stricter future collector should also
support identifier hashing and audit logs.

## Recommended Permissions

For single-query analysis, no database connection is required.

For version detection:

```sql
SELECT version()
```

For EXPLAIN ESTIMATE:

```sql
EXPLAIN ESTIMATE <query>
```

For workload exports, use a read-only user with access limited to
`system.query_log` metadata needed for reporting.
