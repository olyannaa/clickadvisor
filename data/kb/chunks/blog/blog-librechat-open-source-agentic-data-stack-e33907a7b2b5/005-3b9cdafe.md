---
source: blog
url: https://clickhouse.com/blog/agent-facing-analytics
topic: clickhouse-welcomes-librechat-introducing-the-open-source-agentic-data-stack
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 7
---

Token Counts per Day* If you want to experience the power of agentic analytics first\-hand, try the public [AgentHouse](https://clickhouse.com/blog/agenthouse-demo-clickhouse-llm-mcp) demo, which exposes publicly available datasets via the Agentic Data Stack. !['AgentHouse in use'](/uploads/agent_house_v3_7e163b96ca.gif) ## The open\-source advantage [\#](/blog/librechat-open-source-agentic-data-stack#the-open-source-advantage)

The agentic open\-source landscape is currently centered around developer tooling and SDKs, which makes perfect sense given that developers are typically the earliest adopters of emerging technologies. The main open\-source projects in this space aim to empower builders to create, extend, and customize agentic systems with SDKs, frameworks, orchestration layers, and integrations. This developer\-first focus helps establish the foundational ecosystem and standards needed before broader consumer applications take off.

We see the Agentic Data Stack as one of the first proposals of a composable software stack that focuses on the higher\-level integration story, allowing users to get started and deliver value in no time. Both ClickHouse and LibreChat share the same open\-source software DNA, and joining forces strengthens our commitment to that vision:

- **LibreChat remains 100% open\-source** under its existing MIT license
- **Community\-first development** continues with the same transparency and openness
- **Expanded roadmap** to bring an even more enterprise\-ready analytics experience.

This proven playbook is the same one that we applied when joining forces with [PeerDB](https://clickhouse.com/blog/clickhouse-welcomes-peerdb-adding-the-fastest-postgres-cdc-to-the-fastest-olap-database) to provide our ClickPipes CDC capabilities, and [HyperDX](https://clickhouse.com/blog/clickhouse-acquires-hyperdx-the-future-of-open-source-observability), which became the UX of our observability product, ClickStack.

We believe that being good stewards of open\-source means not just maintaining code, but actively investing in and growing the communities that depend on it.

## Limitations [\#](/blog/librechat-open-source-agentic-data-stack#limitations)

Large Language Models can be tricky to use in production. While grounding responses in real\-time data often helps, AI agents are not immune to hallucinations: situations where the model generates incorrect information with high confidence.

Our own experience running internal agents within ClickHouse taught us that the best remediation comes from providing the LLMs with the maximum and most accurate context possible. This can be achieved by commenting the tables using the SQL [COMMENT](https://clickhouse.com/docs/sql-reference/statements/alter/column#comment-column) syntax, for example, or by providing more context in\-line, in the chat, or part of the system prompt of the LLM session.

Finally, robust evaluations are critical for agentic analytics in production because they turn qualitative agent behavior into quantifiable insights, enabling teams to measure effectiveness, detect regressions, and continuously improve system performance.
