---
source: blog
url: https://clickhouse.com/cloud/ai-notebooks-in-clickstack-waitlist
topic: introducing-ai-observability-notebooks-for-managed-clickstack-in-private-preview
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 7
---

them easy to organize and discover, and automatic saving ensures that investigative context is preserved rather than lost in chat history. ![The Notebooks list view in ClickStack showing private and shared notebooks with name, tags, owner, and timestamps](/uploads/notebooks_mar2026_image2_6d2239d35e.png)

> Today, shared notebooks follow a simple last write wins model while we remain in private preview. Support for more advanced concurrent collaboration is in progress as we refine the experience with early users.

AI capabilities can also be enabled or disabled at the team level, giving organizations control over how and when AI assisted workflows are introduced.

## ClickHouse as an AI data platform [\#](/blog/clickstack-ai-notebooks#clickhouse_as_an_ai_data_platform)

Our approach to AI inside ClickStack is opinionated by design. Notebooks provide a structured, collaborative workspace where SREs stay within their existing observability workflows, accelerating analysis across logs, metrics, and traces. The engineer remains in control inside ClickStack, with AI assisting and proposing next steps as alternative paths are explored towards a root cause.

At the same time, this is not the only way to build AI\-powered observability. ClickHouse serves as an open foundation for a growing ecosystem of AI\-driven observability and agentic SRE platforms. Tools such as Resolve, WildMoose, and Traversal can build on ClickHouse as their SQL engine, benefiting from its high concurrency, low latency, and long\-term data retention, which AI systems rely on for context and performance.

Each platform will bring its own abstractions and opinionated layer. We believe there is room for multiple approaches, with a shared high\-performance foundation underneath them.

## Conclusion \& looking forward [\#](/blog/clickstack-ai-notebooks#conclusion_and_looking_forward)

We are releasing Notebooks in private preview because we believe this workflow is useful on day one. At the same time, there is meaningful work ahead. In the near term, we are focused on refining the experience: improving sharing, enabling true concurrent editing, and tightening the overall collaboration model as more teams begin using Notebooks together.

Beyond usability improvements, there are several longer term directions we are actively exploring.
