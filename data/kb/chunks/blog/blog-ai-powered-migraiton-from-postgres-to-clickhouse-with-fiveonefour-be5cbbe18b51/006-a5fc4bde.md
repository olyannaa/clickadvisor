---
source: blog
url: https://github.com/514-labs/moosestack
topic: ai-powered-migrations-from-postgres-to-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 6
total_chunks_in_doc: 11
---

type\-safety (and, depending on the CLI) the agent can also directly access the [MooseStack LSP](https://docs.fiveonefour.com/moosestack/language-server) for validating syntax, autocomplete and error diagnostics. ### Local dev feedback for AI: run the full OLAP stack end\-to\-end with `moose dev` [\#](/blog/ai-powered-migraiton-from-postgres-to-clickhouse-with-fiveonefour#local-dev-feedback-for-ai-run-the-full-olap-stack-end-to-end-with-moose-dev)

Many problems with real applications only show up once the entire system is actually running: mutations fail asynchronously, schemas apply in unexpected order, data arrives with unexpected shapes, or rollups silently produce the wrong numbers in the frontend.

That’s why your agent needs a fast, cheap runtime loop that mirrors your production stack. Agents should be able to apply schemas, push data through materialized views, execute real API queries, and validate the actual outputs your dashboards depend on.

The best version of this is local, hot\-reloading infrastructure with realistic data. Run your entire ClickHouse \+ Postgres \+ frontend stack locally, end\-to\-end, and make validation cheap enough that the agent can iterate on real mistakes instead of guessing.

With MooseStack, that starts with:

```
moose dev

```

This command spins up your whole OLAP stack locally (including ClickHouse), and then automatically infers and applies schema change DDLs in real time as your agent writes code.

This gives the agent two kinds of additional fast feedback:

1. **Runtime errors**. If, for example, your application can’t connect to ClickHouse or a transformation throws an exception when it encounters unexpected data shapes (JSON is a common culprit), these failures can’t be silent. With `moose dev` they surface immediately in the console logs, which makes them visible to both developers and agents while they’re iterating.
2. **MCP validation**. The [MooseDev MCP](https://docs.fiveonefour.com/moosestack/moosedev-mcp?lang=typescript) gives the agent tools to interrogate the local dev server. This allows the agent to validate: “did the system end up in the state the agent thought it created”? Are the right tables and views present? Does the transformed output look correct when queried? Are the logs telling the LLM anything interesting? The agent can even use `moose query` and `moose seed` to insert data to test data flows, sampling data from any step in the process.

Realistic data is what makes these checks meaningful. Without it, you can “pass” validation on toy datasets and still ship incorrect rollups.
