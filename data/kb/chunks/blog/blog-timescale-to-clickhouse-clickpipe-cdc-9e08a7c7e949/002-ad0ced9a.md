---
source: blog
url: https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector
topic: timescaledb-to-clickhouse-replication-use-cases-features-and-how-we-built-it
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 5
---

provides [significantly faster performance](https://benchmark.clickhouse.com/#system=+lik%7CsaB&type=-&machine=-ca2%7C6t%7Cgle%7C6ax%7Cae-%7C6ale%7C3al%7Cgel&cluster_size=-&opensource=-&tuned=+n&metric=hot&queries=-). This is where ClickHouse has been compelling for them, as it is a purpose\-built analytical database. To ensure a smooth migration, they seek a one\-click online migration option from TimescaleDB to ClickHouse Cloud. [![clickbench-cdc-blog-img.png](/uploads/clickbench_timescale_ch_cdc_f00a9e26bc.png)](https://benchmark.clickhouse.com/#system=+lik%7CsaB&type=-&machine=-ca2%7C6t%7Cgle%7C6ax%7Cae-%7C6ale%7C3al%7Cgel&cluster_size=-&opensource=-&tuned=+n&metric=hot&queries=-)

2. **Iterative migration from TimescaleDB to ClickHouse**: In this use case, similar to the one above, a customer wants to migrate from TimescaleDB to ClickHouse but prefers to do so iteratively. Because the application is complex, they choose to migrate in stages \- moving a few workloads at a time, offloading reads first, and then migrating the write pipeline. The Postgres CDC connector is particularly useful in such scenarios, as it keeps both TimescaleDB and ClickHouse in sync with lag as low as a few seconds, while gradually migrating all workloads to ClickHouse. Here is a testimonial from one of our customers, Kindly, who falls under this category of iterative migration from TimescaleDB to ClickHouse.

> “The Postgres CDC connector made it easy for us to transition to ClickHouse Cloud without redesigning our entire pipeline. It has significantly improved dashboard performance and enabled faster data exploration, making our analytics more efficient and scalable.” \- Team @ Kindly.ai

3. **Co\-existence use case** – In this scenario, customers use both TimescaleDB and ClickHouse to power their real\-time applications. For example, they run transactional or time\-series workloads on TimescaleDB while using ClickHouse for fast, advanced analytics. Postgres CDC makes sure to reliably replicate operational data from TimescaleDB to ClickHouse for lightning\-fast real\-time analytics.

## Features and demo [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#features-and-demo)

The Postgres CDC connector in ClickPipes (and PeerDB) supports both initial load/backfill (initial snapshot of data) and ongoing sync/CDC from TimescaleDB Hypertables to ClickHouse. This is possible thanks to the native logical replication support in TimescaleDB, a benefit of it being a Postgres extension. The connector supports both compressed and uncompressed Hypertables. Here are its main features:
