---
source: blog
url: 'https://github.com/ClickHouse/pg_stat_ch):'
topic: pg-stat-ch-a-postgresql-extension-that-exports-every-metric-to-clickhouse
ch_version_introduced: '4.6'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 13
---

# pg\_stat\_ch: a PostgreSQL extension that exports every metric to ClickHouse

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# pg\_stat\_ch: a PostgreSQL extension that exports every metric to ClickHouse

![](/_next/image?url=%2Fuploads%2FImage_512x512_1_839aa54f62.jpeg&w=96&q=75)[Kaushik Iska](/authors/kaushik-iska)Feb 13, 2026 · 21 minutes readWe’re open sourcing [**pg\_stat\_ch**](https://github.com/ClickHouse/pg_stat_ch): a PostgreSQL extension that turns every query execution into a fixed\-size \~4\.6KB event and streams them into ClickHouse.

Once events are in ClickHouse, you can slice and drill into query behavior like an APM: p50 to p99 latency over time, top queries by runtime, errors by app, and “what changed between 2pm and 3pm” across days or months of history.

It’s open\-source, Apache 2\.0, and supports PostgreSQL 16 to 18\. If you want to try it, [give the quickstart a go.](https://github.com/ClickHouse/pg_stat_ch?tab=readme-ov-file#quickstart)

In this post, I’ll walk through how it works under the hood, the tradeoffs we made, and how it compares with existing extensions.

## Why build pg\_stat\_ch? [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#why-build-pg_stat_ch)

In January, we launched [Postgres managed by ClickHouse](https://clickhouse.com/cloud/postgres). We need to understand how the clusters we manage are running, and we want to provide the same level of insight to our customers.

ClickHouse, the analytical database we’re best known for, comes with its own internal system tables that collect everything happening within the server. It’s also built for analytics, so you can just analyse your ClickHouse usage within ClickHouse itself. We rely on this for the managed ClickHouse service in ClickHouse Cloud, as do our customers.

Postgres doesn’t have that level of introspection capability out of the box, and isn’t built for analytics. So, we wanted a way to match that level of detail about what's happening inside Postgres, and the same level of analytical capability to work with it. [See below for examples of the kind of insights you can get with pg\_stat\_ch.](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#what-you-can-actually-do-with-raw-events)

We frequently use extensions like [pg\_stat\_statements](https://www.postgresql.org/docs/current/pgstatstatements.html), [pg\_stat\_monitor](https://github.com/percona/pg_stat_monitor) and [pg\_tracing](https://github.com/DataDog/pg_tracing), and while they cover some parts of the problem, we had 3 primary goals that they didn’t cover:
