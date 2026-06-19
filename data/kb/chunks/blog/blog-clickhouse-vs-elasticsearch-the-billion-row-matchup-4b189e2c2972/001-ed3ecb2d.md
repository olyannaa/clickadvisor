---
source: blog
url: https://www.elastic.co/
topic: clickhouse-vs-elasticsearch-the-billion-row-matchup
ch_version_introduced: '8.5'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 21
---

# ClickHouse vs. Elasticsearch: The Billion\-Row Matchup

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse vs. Elasticsearch: The Billion\-Row Matchup

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)May 7, 2024 · 55 minutes read
## Table of Contents [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#table-of-contents)

- [Introduction](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#introduction)
- [Count aggregations in ClickHouse and Elasticsearch](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#count-aggregations-in-clickhouse-and-elasticsearch)
- [Benchmark setup](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#benchmark-setup)
- [Benchmark queries](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#benchmark-queries)
- [Benchmark methodology](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#benchmark-methodology)
- [Benchmark results](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#benchmark-results)
	- [Summary](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#summary)
	- [Storage size](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#storage-size)
	- [Aggregation performance](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#aggregation-performance)
- [Summary](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#summary-1)

## Introduction [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#introduction)

![Elasticsearch_blog1_header.png](/uploads/Elasticsearch_blog1_header_d82d199670.png)
This blog examines the performance of ClickHouse vs. [Elasticsearch](https://www.elastic.co/) for workloads commonly present in large\-scale data analytics and observability use cases – `count(*)` aggregations over billions of table rows. This type of analysis is fundamental to many [time\-series database](https://clickhouse.com/resources/engineering/what-is-time-series-database) workloads, where understanding event frequency over time is critical. It shows that ClickHouse vastly outperforms Elasticsearch for running aggregation queries over large data volumes. Specifically:

- ClickHouse compresses data much better than Elasticsearch, resulting in **12 to 19 times less storage space** for large data sets, allowing smaller and cheaper hardware to be used.

![Elasticsearch_blog1_01.png](/uploads/Elasticsearch_blog1_01_1d7bc921fc.png)
- `Count(*)` aggregation queries in ClickHouse [utilize](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse) hardware highly efficiently, resulting in **at least 5 times lower latencies** for aggregating large data sets compared to Elasticsearch. This requires smaller and, as we will [demonstrate](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#1-billion-rows---raw-data) later, **4 times cheaper hardware** for comparable Elasticsearch latencies.

![Elasticsearch_blog1_02.png](/uploads/Elasticsearch_blog1_02_6b61827d7b.png)
- ClickHouse [features](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse-3) a **much more storage\- and compute\-efficient continuous data summarization technique** – [ClickHouse materialized views vs Elasticsearch transforms](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#approaches-for-continuous-data-summarization), further lowering computing and storage costs.

![Elasticsearch_blog1_03.png](/uploads/Elasticsearch_blog1_03_b1a41a1b91.png)
For these above\-mentioned reasons, we increasingly see users migrating from Elasticsearch to ClickHouse, with customers highlighting:

- [Drastically reducing the total cost of ownership (TCO) for petabyte\-scale observability use cases](https://clickhouse.com/resources/engineering/observability-tco-cost-reduction):

> “Migrating from Elasticsearch to ClickHouse, reduced the cost of our Observability hardware by over 30%.” [Didi Tech](https://clickhouse.com/blog/didi-migrates-from-elasticsearch-to-clickHouse-for-a-new-generation-log-storage-system)

- Lifts in technical limitations of data analytics applications:

> “This unleashed potential for new features, growth and easier scaling.” [Contentsquare](https://clickhouse.com/blog/contentsquare-migration-from-elasticsearch-to-clickhouse)

- Drastic improvements in scalability and query latencies for monitoring platforms:
