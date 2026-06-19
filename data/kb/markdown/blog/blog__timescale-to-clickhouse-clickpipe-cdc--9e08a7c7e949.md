# TimescaleDB to ClickHouse replication: Use cases, features, and how we built it


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# TimescaleDB to ClickHouse replication: Use cases, features, and how we built it

![ClickHouse Team](/_next/image?url=%2Fuploads%2Flogo_square_120_2cca16e3e3.png&w=96&q=75)[The ClickPipes Team](/authors/clickpipes-team)Sep 9, 2025 · 7 minutes readThe [Postgres CDC connector in ClickPipes](https://clickhouse.com/cloud/clickpipes/postgres-cdc-connector) enables users to continuously replicate data from [Postgres](https://www.postgresql.org/) to [ClickHouse Cloud](https://clickhouse.com/cloud) for blazing\-fast, real\-time analytics. This connector supports both one\-time migrations and continuous replication and is powered by [PeerDB](https://github.com/PeerDB-io/peerdb), an open\-source Postgres CDC company [acquired](https://techcrunch.com/2024/07/30/real-time-database-startup-clickhouse-acquires-peerdb-to-expand-its-postgres-support/) by ClickHouse. Since its GA launch a few months ago, we’ve seen a surge in customer requests to extend these CDC capabilities to [TimescaleDB](https://github.com/timescale/timescaledb), the time\-series Postgres extension maintained by TigerData.


## Use\-cases [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#use-cases)


We see use cases that involve both one\-time migrations and continuous replication. They primarily fall into three buckets:


1. **Online data migrations from TimescaleDB to ClickHouse:** In this use case, customers already run analytics on TimescaleDB. As their data or workloads (e.g., advanced analytics) scale, TimescaleDB no longer performs well without significant tuning and optimizations that require deep database/DBA expertise. These customers prefer a more turnkey solution that provides [significantly faster performance](https://benchmark.clickhouse.com/#system=+lik%7CsaB&type=-&machine=-ca2%7C6t%7Cgle%7C6ax%7Cae-%7C6ale%7C3al%7Cgel&cluster_size=-&opensource=-&tuned=+n&metric=hot&queries=-). This is where ClickHouse has been compelling for them, as it is a purpose\-built analytical database. To ensure a smooth migration, they seek a one\-click online migration option from TimescaleDB to ClickHouse Cloud.


[![clickbench-cdc-blog-img.png](/uploads/clickbench_timescale_ch_cdc_f00a9e26bc.png)](https://benchmark.clickhouse.com/#system=+lik%7CsaB&type=-&machine=-ca2%7C6t%7Cgle%7C6ax%7Cae-%7C6ale%7C3al%7Cgel&cluster_size=-&opensource=-&tuned=+n&metric=hot&queries=-)


2. **Iterative migration from TimescaleDB to ClickHouse**: In this use case, similar to the one above, a customer wants to migrate from TimescaleDB to ClickHouse but prefers to do so iteratively. Because the application is complex, they choose to migrate in stages \- moving a few workloads at a time, offloading reads first, and then migrating the write pipeline. The Postgres CDC connector is particularly useful in such scenarios, as it keeps both TimescaleDB and ClickHouse in sync with lag as low as a few seconds, while gradually migrating all workloads to ClickHouse. Here is a testimonial from one of our customers, Kindly, who falls under this category of iterative migration from TimescaleDB to ClickHouse.



> “The Postgres CDC connector made it easy for us to transition to ClickHouse Cloud without redesigning our entire pipeline. It has significantly improved dashboard performance and enabled faster data exploration, making our analytics more efficient and scalable.” \- Team @ Kindly.ai


3. **Co\-existence use case** – In this scenario, customers use both TimescaleDB and ClickHouse to power their real\-time applications. For example, they run transactional or time\-series workloads on TimescaleDB while using ClickHouse for fast, advanced analytics. Postgres CDC makes sure to reliably replicate operational data from TimescaleDB to ClickHouse for lightning\-fast real\-time analytics.


## Features and demo [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#features-and-demo)


The Postgres CDC connector in ClickPipes (and PeerDB) supports both initial load/backfill (initial snapshot of data) and ongoing sync/CDC from TimescaleDB Hypertables to ClickHouse. This is possible thanks to the native logical replication support in TimescaleDB, a benefit of it being a Postgres extension. The connector supports both compressed and uncompressed Hypertables. Here are its main features:


1. **Blazing fast initial loads** – One of the flagship features of ClickPipes is [**parallel snapshotting**](https://clickhouse.com/docs/integrations/clickpipes/postgres/parallel_initial_load), which migrates a single large table using parallel threads. This enables moving terabytes of data in just a few hours instead of days. It works for **TimescaleDB hypertables,** as well, although It does not extend to compressed hypertables, which don’t support CTID columns. In such cases, ClickPipes falls back to single\-threaded execution — which remains fast thanks to a range of micro\-optimizations, including cursors and efficient data movement via Avro \+ Zstd, among others.
2. **Support for both uncompressed and compressed hypertables** – The ClickPipes Postgres CDC connector works with both uncompressed and compressed TimescaleDB hypertables, ensuring seamless replication into ClickHouse.
3. **Support for schema changes** \- The ClickPipes Postgres CDC connector also supports automatic replication of [schema changes](https://clickhouse.com/docs/integrations/clickpipes/postgres/schema-changes) from TimescaleDB including adding and dropping columns.
4. **Comprehensive alerts and metrics** – ClickPipes provides extensive metrics including throughput, inserts/updates/deletes per table, latency, and Postgres\-native metrics such as replication slot size over time and wait events during replication. It also offers advanced [alerts](https://clickhouse.com/blog/postgres-cdc-connector-clickpipes-public-beta#user-facing-alerts) through Slack or email for issues like replication slot growth or replication failures etc. The goal is to deliver deep visibility into the replication process and ensure an enterprise\-ready experience.



## How did we build it? [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#how-did-we-build-it)


### Handling hypertables and chunks in logical replication [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#handling-hypertables-and-chunks-in-logical-replication)


The TimescaleDB extension introduces **hypertables**—automatically partitioned tables designed to optimize query performance for time\-series data. Like Postgres partitioned tables, hypertables don’t store data directly but do it in child tables called **chunks**. This design complicates logical replication, since changes must be tracked at the chunk level rather than the parent hypertable. It also requires handling scenarios where TimescaleDB automatically creates new chunks as data arrives.


For standard [Postgres partitioned tables](https://blog.peerdb.io/real-time-change-data-capture-for-postgres-partitioned-tables), logical replication relies on the [`publish_via_partition_root`](https://amitlan.com/writing/pg/partition-logical-replication/) option, which rewrites changes to appear as if they originated from the parent table. Hypertables, however, don’t support this option. ClickPipes (via PeerDB) therefore [performs the parent lookup explicitly](https://github.com/PeerDB-io/peerdb/blob/da537889fe9b9bbe84b85799385f3b576b5b34dd/flow/connectors/postgres/cdc.go#L1152) while processing changes. As long as the publication includes all child tables, this ensures that changes are routed correctly to the target ClickHouse table.


![timescalediagramfinal.png](/uploads/timescalediagramfinal_cb752d0018.png)
To manage newly created chunks, TimescaleDB stores them under the `_timescaledb_internal` schema. By adding this schema to the Postgres publication, we capture all future chunks. It requires a bit of setup upfront but, once configured, results in a **hands\-off replication experience** with ClickPipes.


### Supporting Compression [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#supporting-compression)


Another TimescaleDB feature beyond vanilla Postgres is **hypertable compression**, enabled via transparent compression or the newer Hypercore hybrid row\-columnar engine. These configurations bring compression benefits similar to columnar and time\-series databases like ClickHouse.


However, compressed storage introduces challenges. Our parallel initial\-load strategy using `ctid` partitions doesn’t work here and fails with errors such as:


`ERROR: transparent decompression only supports tableoid system column`


We recently [shipped an improvement](https://github.com/search?q=repo%3APeerDB-io%2Fpeerdb+timescaledb&type=pullrequests) to detect this scenario and automatically fall back to a code path that avoids relying on the `ctid` column, ensuring replication remains reliable even with compressed hypertables.


## Conclusion [\#](/blog/timescale-to-clickhouse-clickpipe-cdc#conclusion)


To get started with replicating or migrating your TimescaleDB workloads to ClickHouse, you can follow the resources below.


1. [Steps to setup logical replication on TimescaleDB](https://clickhouse.com/docs/integrations/clickpipes/postgres/source/timescale)
2. [ClickPipes for replicating TimescaleDB to ClickHouse Cloud](https://clickhouse.com/docs/integrations/clickpipes/postgres)
3. [PeerDB for replication TimescaleDB to ClickHouse Open Source](https://github.com/PeerDB-io/peerdb)


*\* Third\-party logos and trademarks belong to their respective owners and are used here for identification purposes only. No endorsement is implied.*

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
