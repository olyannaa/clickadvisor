---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Postgres
topic: postgres-fdw-pushdown-is-a-negotiation-clickhouse
ch_version_introduced: '0.95'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 13
---

past 6 months, we found that a single question drives most of the engineering work: how much of a query do we send across the wire as SQL versus how many rows do we drag back as data?

That question encompasses the meaning of [pushdown](https://whatisdatabase.com/optimizing-database-performance-with-pushdown-techniques): how much work can we “push down” to the remote service? The answer seems simple: “send everything!” — the `WHERE` clause, the `GROUP BY`, the `LIMIT`. But a closer examination reveals the complexity: Some clauses we can send. Some we can almost send — if we rewrite them. Some we used to send but stopped, because they returned the wrong results. And some clauses can never be sent by any FDW, regardless of the engineering one throws at them.

We’ve found the process of making these determinations highly iterative.

To demonstrate, let’s examine the impact of that iteration on a single query: what gets pushed down, what doesn't, and how we continuously modified the code in response to the question.

The goal is to illuminate the inner workings of an FDW for people who’ve heard of FDWs but don’t know how they work in detail. Whether you're a Postgres user curious about ClickHouse, a ClickHouse user curious about Postgres, or someone thinking about writing an FDW yourself, we hope you find this exercise edifying.

## The query that takes 80 ms or 4 minutes \#

This query ranks the busiest web events in the last week for the US, UK, and DE, by country and event name. It reports volume, unique users, premium share, p95 latency, and each event’s rank by country, returning the top 100 rows overall to provide a small snapshot and avoid streaming raw events.
