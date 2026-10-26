---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Postgres
topic: postgres-on-nvme-performance-and-the-convergence-of-transactions-and-analytics-clickhouse
ch_version_introduced: auto
last_updated: '2026-10-26'
chunk_index: 5
total_chunks_in_doc: 7
---

Because storage latency is only one part of the problem. NVMe makes random access dramatically cheaper. It doesn't turn a row store into a column store. Transactional and analytical workloads ask fundamentally different things of a storage engine.

**Postgres** stores complete rows in 8 KB pages. A point read touches one page, MVCC keeps row versions in place so writers never block readers, and B\-tree indexes make selective lookups cheap. The cost is that an aggregation over a billion rows reads every page of every row, whether it needs those columns or not. `sum(amount) GROUP BY country` still loads whole rows, even when each page comes back in microseconds.

**ClickHouse** stores and processes data column\-by\-column. Each column lives in its own file, an aggregation reads only the columns it references, execution is vectorized in cache\-sized batches, and similar values compress extremely well under per\-column codecs (10× is routine). MergeTree absorbs append\-heavy ingest with background merges instead of materializing every insert on a page immediately.

What has changed is *when* teams hit this wall. Growing from 10 GB to 100 GB used to take 12–18 months; now it takes one to three. AI\-native products log inference and agent runs from day one, and need analytics on them from day one. Security platforms ingest append\-only event streams and quickly reach terabytes of data. Product analytics SaaS sells dashboards to customers, and a 30\-second dashboard is a dashboard nobody trusts.

## One architecture, two engines \#

The pattern I keep seeing in the field is simple. The application keeps writing to Postgres: transactions, ACID, point lookups, unchanged. Change data capture streams every insert, update, and delete to ClickHouse with seconds\-level freshness. And [pg\_clickhouse](https://github.com/ClickHouse/pg_clickhouse), an open\-source Postgres extension, lets the application query the ClickHouse copy over its existing Postgres connection, so ClickHouse behaves almost like an analytical read replica.

![](/_next/image?url=%2Fuploads%2Fpostgres_nvme_sep2026_image3_b9e73c397d.png&w=2048&q=75)
