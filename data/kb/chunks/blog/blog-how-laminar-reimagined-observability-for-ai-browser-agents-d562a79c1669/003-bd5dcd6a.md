---
source: blog
url: https://www.lmnr.ai/
topic: how-laminar-is-using-clickhouse-to-reimagine-observability-for-ai-browser-agents
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 5
---

honestly didn’t even consider others,” Robert says. “ClickHouse was the obvious choice.” ### Get started today Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)
At first glance, Laminar’s use case might not seem like a natural fit. ClickHouse is traditionally used for analytics, not video\-style trace replay. But the team knew what it could do, and they saw an opportunity to push it further. “We really liked the fast writes and fast reads,” Robert says. “We needed a database that could handle high\-throughput ingestion without adding latency or slowing down the core logic of the application.”

That confidence was reinforced by earlier trials. Before standardizing on ClickHouse, the team had experimented with other databases to support search functionality. “The first version was Postgres\-like, and it was incredibly slow,” Robert says. “Then we tried another open\-source database, but it didn’t work well either. Once we switched to ClickHouse, everything just worked. It was incredibly fast.”

While the team appreciated ClickHouse’s open\-source roots (“all of our tech stack is open\-source,” Robert notes), they ultimately chose to run [ClickHouse Cloud](https://clickhouse.com/cloud). “Even though we like managing infra, we don’t need to manage yet another thing,” he says. “As a small team, ClickHouse Cloud lets us focus on what we care about and offload database management to the people who do it best. Plus, the pricing was great.”

## Performance that feels like magic [\#](/blog/how-laminar-reimagined-observability-for-ai-browser-agents#performance-that-feels-like-magic)

Today, Laminar’s system ingests over 500,000 browser events per day. Thanks to ClickHouse, Robert says, the load “doesn’t affect our infra at all. It’s that smooth.” Since launch, the platform has recorded over 1 billion events and read more than 50 billion (mostly due to developers replaying traces multiple times while debugging).

Agent sessions can last 30 minutes or more, generating hundreds of thousands of DOM diff events. Yet when users load a trace, it opens almost instantly. “This is because we made some ClickHouse magic with highly optimized [tables and partitions](https://clickhouse.com/docs/partitions),” Robert says.
