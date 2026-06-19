# You can’t UPDATE what you can’t find: ClickHouse vs PostgreSQL


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# You can’t UPDATE what you can’t find: ClickHouse vs PostgreSQL

![Al Brown](/_next/image?url=%2Fuploads%2Fal_brown_headshot_09ae0cbce6.jpg&w=96&q=75)![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Al Brown](/authors/al-brown) and [Tom Schreiber](/authors/tom-schreiber)Aug 13, 2025 · 23 minutes read
> **TL;DR**  
>   
> · On identical hardware and data, ClickHouse is **up to 4,000× faster** on bulk UPDATEs, reaches **parity on single\-row updates**, and stays **competitive on cached point updates**.   
>   
> · Why it matters: Bulk updates are common in OLTP workloads, and ClickHouse’s columnar design \+ parallelism make them far faster.   
>   
> · Caveat: PostgreSQL is fully transactional by default; ClickHouse isn’t. Results reflect native execution models, not identical guarantees.


PostgreSQL is the most popular open\-source [OLTP database](https://clickhouse.com/resources/engineering/oltp-vs-olap) in the world.


It’s a fair assumption that, when a developer thinks about UPDATE performance, they probably think of the baseline that PostgreSQL sets.


In contrast, ClickHouse is the most popular open\-source OLAP database in the world.


While ClickHouse sets the expectation of OLAP performance, its OLTP potential is often underrated.


In July 2025, [ClickHouse v25\.7 brought high\-performance SQL\-standard UPDATEs to ClickHouse](https://clickhouse.com/blog/updates-in-clickhouse-2-sql-style-updates).


Naturally, we want to know how ClickHouse stacks up against the best. **Are UPDATEs in ClickHouse competitive with UPDATEs in Postgres?**


In this post we first look at cold runs, the stress\-test scenario where no data is cached, and then complement them with hot runs, which better reflect everyday workloads where indexes and cache hit rates are high.


## Comparing PostgreSQL and ClickHouse isn’t apples\-to\-apples [\#](/blog/update-performance-clickhouse-vs-postgresql#comparing-postgresql-and-clickhouse-isnt-apples-to-apples)


In our previous post, [we benchmarked the new high\-performance SQL\-standard UPDATEs against other ClickHouse update methods](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks). Here, out of curiosity, we’re running the same benchmarks against PostgreSQL on identical hardware and data.


We focus on two OLTP staples: single\-row updates and bulk changes on a classic orders dataset. These tests reveal how much update speed depends on finding rows efficiently, a strength ClickHouse inherits from its analytical roots.


Before diving into the numbers, we want to acknowledge something: a PostgreSQL vs. ClickHouse comparison isn’t apples\-to\-apples.


Both can run UPDATEs, but their execution models differ in ways that matter when interpreting results.



> **TL;DR:** PostgreSQL wraps every statement in a fully transactional context and flushes WAL at commit by default; ClickHouse doesn’t. That means these results aren’t a perfect measure of transaction or durability performance. However, they’re still an interesting and relevant look at how each system handles update workloads under its native execution model.


PostgreSQL and ClickHouse may both run UPDATE statements, but they don’t do it the same way. They share a similar approach to isolation, both use **Multi\-Version Concurrency Control (MVCC)**, but differ in how they handle transactions, commit semantics, and durability guarantees.


This difference matters when interpreting benchmark results.


### Multi\-Version Concurrency Control (MVCC) [\#](/blog/update-performance-clickhouse-vs-postgresql#multi-version-concurrency-control-mvcc)


Both PostgreSQL and ClickHouse use [MVCC](https://en.wikipedia.org/wiki/Multiversion_concurrency_control) to let readers and writers work in parallel without blocking each other. Every query sees a **consistent snapshot** of the data as it existed when it started, which means:


- Readers never see partial changes from concurrent updates.
- Readers and writers don’t block each other.
- Data is never overwritten in place; new versions are created, and old ones are kept until no query needs them.


How this looks in practice:


**PostgreSQL**


1. Creates a **new row version** with the updated data.
2. Keeps the old version until all readers of the old one finish.
3. Removes old versions later via **[VACUUM](https://www.postgresql.org/docs/current/sql-vacuum.html)**.


**ClickHouse**


1. Creates a **new [data part](https://clickhouse.com/docs/parts) ([patch](https://clickhouse.com/blog/updates-in-clickhouse-2-sql-style-updates#how-patch-parts-work))** with updated values.
2. [Keeps old data parts until all readers of the old one finish](https://clickhouse.com/blog/clickhouse-release-25-06#single-snapshot-for-select).
3. Merges updates into the source data part during a [background merge](https://clickhouse.com/docs/merges) and discards old versions.



> On isolation alone, PostgreSQL and ClickHouse behave very similarly; both ensure readers always see a consistent snapshot while updates are in flight.


### Transactions, commit, and rollback [\#](/blog/update-performance-clickhouse-vs-postgresql#transactions-commit-and-rollback)


Here’s where the paths diverge:


**PostgreSQL**


- Runs *every* statement, even a single UPDATE, inside a **[transaction context](https://www.postgresql.org/docs/current/tutorial-transactions.html)**.
- If you don’t start one, it still wraps the statement in an **implicit transaction** (BEGIN → execute → COMMIT).
- Writes all changes to the **Write\-Ahead Log ([WAL](https://www.postgresql.org/docs/current/wal-intro.html))** before touching the table for durability and crash recovery.
- **COMMIT** makes changes visible; **ROLLBACK** discards them before commit, marking old row versions invalid for later cleanup.


**ClickHouse**


- Single inserts and updates on a MergeTree table [are](https://clickhouse.com/docs/guides/developer/transactional#case-1-insert-into-one-partition-of-one-table-of-the-mergetree-family) **atomic, consistent, isolated, and durable**, applied as a whole, if they are packed and inserted as a single block.
- By default, it doesn’t wrap every statement in a transaction.
- Supports **experimental** [multi\-statement transactions](https://clickhouse.com/docs/guides/developer/transactional#transactions-commit-and-rollback) with explicit BEGIN, COMMIT, and ROLLBACK (not yet in ClickHouse Cloud).



> PostgreSQL is fully transactional by default, adding **per\-update\-statement overhead**. ClickHouse avoids extra bookkeeping unless you explicitly start a transaction (experimental feature, not yet in ClickHouse Cloud).


### Durability and flush policy [\#](/blog/update-performance-clickhouse-vs-postgresql#durability-and-flush-policy)


Here’s where the systems differ again, this time in how they guarantee durability and handle flushes to disk.


PostgreSQL:


- `fsync` \= `on`, `synchronous_commit` \= `on` by default → WAL is flushed to disk at every commit.
- Adds latency but guarantees durability even if the OS crashes.


ClickHouse:


- `fsync_after_insert` \= `false` by default → relies on OS page cache, parts are atomic but not immediately flushed.
- Faster inserts/updates, weaker immediate durability; you can enable `fsync_after_insert = 1` for stronger guarantees.



> Implication for benchmarks: Results reflect the default durability/flush settings. You can shift absolute times by changing these knobs, but the relative patterns (row vs. column update costs) dominate.


With the key execution model differences in mind, let’s look at how we put both systems to the test.


## Dataset and benchmark setup [\#](/blog/update-performance-clickhouse-vs-postgresql#dataset-and-benchmark-setup)


In our [previous blog](https://clickhouse.com/blog/updates-in-clickhouse-3-benchmarks) on fast updates in ClickHouse, we walked through the dataset, schema, and setup in detail. Here’s a quick recap of the essentials so we can focus on the new ClickHouse–PostgreSQL comparison.


### Dataset [\#](/blog/update-performance-clickhouse-vs-postgresql#dataset)


We use the [TPC\-H](https://clickhouse.com/docs/getting-started/example-datasets/tpch) lineitem table, which models items from customer orders. This is a classic [OLTP](https://clickhouse.com/resources/engineering/oltp-vs-olap)\-style scenario for updates, as quantities, prices, or discounts might change after the initial insert.


#### ClickHouse [\#](/blog/update-performance-clickhouse-vs-postgresql#clickhouse)



```

```
CREATE TABLE lineitem (
    l_orderkey       Int32,
    l_partkey        Int32,
    l_suppkey        Int32,
    l_linenumber     Int32,
    l_quantity       Decimal(15,2),
    l_extendedprice  Decimal(15,2),
    l_discount       Decimal(15,2),
    l_tax            Decimal(15,2),
    l_returnflag     String,
    l_linestatus     String,
    l_shipdate       Date,
    l_commitdate     Date,
    l_receiptdate    Date,
    l_shipinstruct   String,
    l_shipmode       String,
    l_comment        String)
ORDER BY (l_orderkey, l_linenumber);
```


```

#### PostgreSQL [\#](/blog/update-performance-clickhouse-vs-postgresql#postgresql)



```

```
CREATE TABLE lineitem
(
  l_orderkey          INT,
  l_partkey           INT,
  l_suppkey           INT,
  l_linenumber        INT,
  l_quantity          DECIMAL(15,2),
  l_extendedprice     DECIMAL(15,2),
  l_discount          DECIMAL(15,2),
  l_tax               DECIMAL(15,2),
  l_returnflag        CHAR(1),
  l_linestatus        CHAR(1),
  l_shipdate          DATE,
  l_commitdate        DATE,
  l_receiptdate       DATE,
  l_shipinstruct      CHAR(25),
  l_shipmode          CHAR(10),
  l_comment           VARCHAR(44),
  PRIMARY KEY (l_orderkey, l_linenumber)
);
```


```

#### Primary key and indexing [\#](/blog/update-performance-clickhouse-vs-postgresql#primary-key-and-indexing)


Both databases use [the official TPC\-H compound primary key](https://www.tpc.org/TPC_Documents_Current_Versions/pdf/TPC-H_v3.0.1.pdf) `(l_orderkey, l_linenumber)`.


- In **PostgreSQL**, this creates a **[B\-tree index](https://www.postgresql.org/docs/current/indexes-types.html#INDEXES-TYPES-BTREE)** by default.
- In **ClickHouse**, it creates a **[sparse primary index](https://clickhouse.com/docs/primary-indexes)** over the same columns.


In both cases, the index ensures that all queries with predicates on these columns can quickly locate matching rows, speeding up both updates and reads.


#### Data size [\#](/blog/update-performance-clickhouse-vs-postgresql#data-size)


We use the **scale factor 100** version of this table, which contains roughly **600 million rows** (\~600 million items from \~150 million orders) and occupies **\~30 GiB on disk with ClickHouse**, and **\~85 GiB with PostgreSQL**.


### Test environment [\#](/blog/update-performance-clickhouse-vs-postgresql#test-environment)


#### Hardware and OS [\#](/blog/update-performance-clickhouse-vs-postgresql#hardware-and-os)


We used an **AWS m6i.8xlarge** EC2 instance (32 cores, 128 GB RAM) with a **gp3 EBS volume** (16k IOPS, 1000 MiB/s max throughput) running **Ubuntu 24\.04 LTS**.


#### ClickHouse version [\#](/blog/update-performance-clickhouse-vs-postgresql#clickhouse-version)


We performed all tests with **ClickHouse 25\.7** with a default installation without any optimizations applied.


#### PostgreSQL version [\#](/blog/update-performance-clickhouse-vs-postgresql#postgresql-version)


We used **PostgreSQL 17\.5** and [installed it with optimized settings](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/benchmark.sh#L15).


### Benchmark methodology [\#](/blog/update-performance-clickhouse-vs-postgresql#benchmark-methodology)


We measured **cold update times** by dropping the OS\-level page cache before each update. This forces the database to load the affected rows from storage and apply the changes from scratch, without help from cached data or prior reads. The result is **upper\-bound (worst\-case) latency numbers**. Warm\-cache measurements are harder to compare fairly, as PostgreSQL and ClickHouse cache and reuse data differently.


**UPDATE**: To give a fuller picture, we now report both **cold run** and **hot runs**. Cold runs stress I/O and highlight worst\-case latencies, while hot runs simulate typical workloads with data already cached in memory.


### Running it yourself [\#](/blog/update-performance-clickhouse-vs-postgresql#running-it-yourself)


You can reproduce all results with the [Benchmark scripts](https://github.com/ClickHouse/examples/tree/main/blog-examples/UPDATEBench) on GitHub.


We’ll start small, looking at point updates that change a single row at a time, before moving on to multi\-row bulk changes.


## Single\-row (point) updates [\#](/blog/update-performance-clickhouse-vs-postgresql#single-row-point-updates)


We start with [10 standard SQL UPDATE statements](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/updates-point.sql), each targeting a single row identified by its [primary key](/blog/update-performance-clickhouse-vs-postgresql#primary-key-and-indexing). These updates are executed sequentially in both ClickHouse and PostgreSQL.


### Update latency [\#](/blog/update-performance-clickhouse-vs-postgresql#update-latency)


For each update, the chart shows the [cold](/blog/update-performance-clickhouse-vs-postgresql#benchmark-methodology) time from issuing the UPDATE to when the change becomes visible to queries. The `Cols upd` column indicates how many of the 16 table columns were updated in that statement.


![Blog-updates Part 4.001.png](/uploads/Blog_updates_Part_4_001_1ee0bc6501.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/cold_point.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_COLD_POINT.json) behind the chart above.)*


In these point\-updates, ClickHouse consistently finished faster, which is a super satisfying result. That said, we’ll highlight again that Postgres is incurring an overhead of wrapping every statement in a transaction context, which ClickHouse is not.


Given that, our main takeaways here are:


1. Postgres is really fast!
2. ClickHouse UPDATEs have started off strong, with great performance in cases where transactions aren’t needed.
3. The current performance is good enough that, should ClickHouse introduce production support for transactions, there is a good chance we’ll end up in parity with Postgres in a more apples\-to\-apples test.


It’s also interesting to consider that each system finds an individual row in different ways; PostgreSQL uses a B\-tree index with one entry per row to locate the target row directly. ClickHouse’s sparse primary index identifies the [block of rows](https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes#data-is-organized-into-granules-for-parallel-data-processing) (8,192 rows by default) that might contain the target, then [searches through all rows in parallel](https://clickhouse.com/docs/optimize/query-parallelism).


For most workloads, the update isn’t the end of the story; it’s what happens next that matters. In real dashboards and reports, updated values need to be reflected right away in downstream queries. So next, we check how each database handles analytical queries that run immediately after these updates.


### Query latency after update [\#](/blog/update-performance-clickhouse-vs-postgresql#query-latency-after-update)


We use **[10 typical analytical queries](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/analytical_queries.sql)** that would immediately benefit from updated data. They cover common warehouse\-style patterns, such as:


- **Revenue and margin recalculation** – e.g., computing net revenue for a given shipping mode.
- **Aggregates on filtered subsets** – e.g., average discounts and taxes for orders with certain comments or statuses.
- **Operational counts** – e.g., counting orders shipped under specific modes or with certain instructions.
- **Ad\-hoc investigations** – e.g., sampling rows that match a comment substring.


These queries represent the kind of **real\-time dashboards and analytical reports** where users expect updated facts to be reflected immediately after a change.


These queries are paired 1 with the 10 updates: After each update, its paired query runs. Each query touches at least the updated rows and columns, but many scan broader data for realistic analytics.


The following chart shows post\-update [cold](/blog/update-performance-clickhouse-vs-postgresql#benchmark-methodology) query times for all 10 queries after each single\-row UPDATE:


![Blog-updates Part 4.002.png](/uploads/Blog_updates_Part_4_002_d6353471d4.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/cold_point.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_COLD_POINT.json) behind the chart above.)*


For ClickHouse, we show **Before materialization** — queries see updated values instantly via *[patch\-on\-read](https://clickhouse.com/blog/updates-in-clickhouse-2-sql-style-updates#how-patch-on-read-works)*, without waiting for background merges.


It’s not too surprising that ClickHouse is consistently much faster here; these are *analytical queries over large datasets*, and that’s ClickHouse’s home turf. The key takeaway is how little the update stage slows it down: whether updates are freshly applied or fully merged, query performance stays high and predictable.


Single\-row updates are the OLTP baseline; they measure how quickly each engine can locate and modify an individual record. But many operational changes touch much larger slices of data, so next we look at bulk updates.


## Bulk updates (multi\-row changes) [\#](/blog/update-performance-clickhouse-vs-postgresql#bulk-updates-multi-row-changes)


We took the same [10 standard SQL UPDATE statements](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/updates-bulk.sql) used for the single\-row updates test, but modified the predicates so they no longer target individual rows by primary key. Instead, they match **dozens, hundreds, or even hundreds of thousands of rows**, a very common OLTP pattern in an orders table.


Typical reasons for such bulk updates include:


- **Correcting data entry errors** – fixing discounts, taxes, or prices for all orders matching a certain date and quantity.
- **Adjusting order statuses** – changing return flags, shipping modes, or line statuses in response to business events.
- **Applying policy or pricing changes** – repricing items for a given supplier, contract, or campaign.
- **Handling special\-case bulk actions** – marking orders as “priority,” “warranty extended,” or “return\-flagged” based on filters like commit date or quantity.


These scenarios are frequent in production OLTP workloads, where operational changes must be applied to large, filtered subsets of data rather than to just one row at a time.


### Update latency [\#](/blog/update-performance-clickhouse-vs-postgresql#update-latency-1)


For every one of the 10 bulk UPDATEs (that we run sequentially in both ClickHouse and PostgreSQL), the chart measures the [cold](/blog/update-performance-clickhouse-vs-postgresql#benchmark-methodology) time from issuing the UPDATE to the moment its changes are visible to queries. The `Rows upd` and `Cols upd` columns indicate how many rows and how many of the 16 table columns were updated in each statement.


![Blog-updates Part 4.003.png](/uploads/Blog_updates_Part_4_003_7338308ff0.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/cold_bulk.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_COLD_BULK.json) behind the chart above.)*


Initially, these results looked a bit off… but they actually make sense. Except for update ⑤, none of [these bulk updates](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/updates-bulk.sql) can use a [primary key index](/blog/update-performance-clickhouse-vs-postgresql#primary-key-and-indexing) because their WHERE clauses filter on columns other than the primary key. (Both systems could use extra indexes, but with 16 columns, covering all combinations is impractical, especially for ad\-hoc bulk updates, where creating the index might take longer than the update.)


In those cases, the real cost isn’t writing the changes, it’s finding the rows. That means scanning the table end to end.


For PostgreSQL, that takes 380–390 s on this dataset before the changes are visible. ClickHouse scans the same data in 0\.09–5\.23 s, up to 4,000× faster. The advantage comes from [highly parallel processing](https://clickhouse.com/docs/optimize/query-parallelism) and a [column\-oriented layout](https://clickhouse.com/docs/intro#row-oriented-vs-column-oriented-storage), only reading columns used in the UPDATE’s WHERE clause and only writing values for the columns being updated.


[Update ⑤](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/updates-bulk.sql#L5) is the one exception: both systems use an index to jump directly to the matching rows, narrowing the gap to “only” 26×. But in every other case, where both have to scan everything, ClickHouse’s raw scan speed keeps update\-visibility latency low, even for massive changes.



> In OLTP workloads, you can’t update what you haven’t located, and locating large numbers of rows quickly takes an analytical engine’s horsepower.


Still, applying the update is only part one. Part two is how quickly you can run analytics on the updated data, which is often the whole reason you made the change in the first place. Let’s see how each system performs when we immediately follow these bulk updates with representative analytical queries.


### Query latency after update [\#](/blog/update-performance-clickhouse-vs-postgresql#query-latency-after-update-1)


We use the same **[10 typical analytical queries](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/scripts/analytical_queries.sql)** as before, paired again 1 with the 10 updates: After each update, its paired query runs. Each query touches at least the updated rows and columns, but many scan broader data for realistic analytics.


The next chart shows post\-update [cold](/blog/update-performance-clickhouse-vs-postgresql#benchmark-methodology) query times for all 10 queries after each bulk\-row UPDATE:


![Blog-updates Part 4.004.png](/uploads/Blog_updates_Part_4_004_da3420b9b0.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/cold_bulk.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_COLD_BULK.json) behind the chart above.)*


As before, unsurprisingly, ClickHouse is consistently much faster than PostgreSQL on the same hardware and same dataset for typical analytical queries that would immediately benefit from updated data.


But cold runs only tell half the story. To complete the picture, let’s look at hot runs. Updates with data already cached, where different trade\-offs emerge.


## Hot results: the other side of the story [\#](/blog/update-performance-clickhouse-vs-postgresql#hot-results-the-other-side-of-the-story)


In the first version of this post, we focused on **cold runs**: queries executed without cached data. Cold results are useful as a stress test, since they highlight differences in how systems handle I/O and large batch updates.


That said, we also got valuable feedback: in typical **OLTP workloads**, cold runs are rare. Index and cache hit rates are often above 99%, which means most updates operate under **hot conditions** with data already in memory.


To give a fuller picture, we extended our benchmarks with **hot results** as well. This way, we can compare both the diagnostic “worst case” and the “realistic baseline” for everyday workloads.


To keep things comparable, we’ll walk through the same charts as before, first single\-row (point) updates, then bulk updates, this time under hot conditions.


### Single\-row (point) updates \- Update latency and query latency after update [\#](/blog/update-performance-clickhouse-vs-postgresql#single-row-point-updates---update-latency-and-query-latency-after-update)


For each update, the chart shows the *hot* latency from issuing the UPDATE to when the change becomes visible to queries, with all data already cached in memory. As before, the **Cols upd** column indicates how many of the 16 table columns were updated in that statement.


![Blog-updates Part 4.005.png](/uploads/Blog_updates_Part_4_005_4a7fed56c6.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/hot_point.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/main/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_HOT_POINT.json) behind the chart above.)*


In hot runs, where data is already cached in memory, PostgreSQL takes the lead. Even though every statement still pays the cost of being wrapped in a full transaction, its row\-level B\-tree index gives it a decisive advantage: it can pinpoint and update rows directly without scanning a block.


ClickHouse remains fast, consistently finishing updates in single\-digit milliseconds, but is slightly behind PostgreSQL in these in\-memory cases. That gap reflects the different execution models: ClickHouse’s sparse primary index always has to scan a full block of rows (8,192 by default), even when the data is already hot in memory.


The main takeaways are:


- PostgreSQL wins on hot point updates, despite transactional overhead. Its index structure makes row lookups extremely efficient once data is cached.
- ClickHouse is only a few milliseconds behind, still delivering excellent OLTP\-style latencies.
- Both systems are highly performant here, but their architectural trade\-offs show through clearly: PostgreSQL is optimized for transactional point\-updates, while ClickHouse’s design favors analytical workloads and still manages to compete closely.


The following chart shows post\-update hot query times for all 10 queries after each single\-row UPDATE:


![Blog-updates Part 4.006.png](/uploads/Blog_updates_Part_4_006_fa62020526.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/hot_point.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/main/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_HOT_POINT.json) behind the chart above.)*


For both PostgreSQL and ClickHouse, hot query runtimes are lower than in the cold runs since the data is already cached. But the relative behavior stays the same: as in the cold results, ClickHouse is consistently much faster than PostgreSQL on the same hardware and dataset when running typical analytical queries that immediately consume the updated data.


### Bulk updates \- Update latency and query latency after update [\#](/blog/update-performance-clickhouse-vs-postgresql#bulk-updates---update-latency-and-query-latency-after-update)


For each of the 10 bulk UPDATEs, the chart shows the hot time from issuing the UPDATE to when its changes become visible to queries. The Rows upd and Cols upd columns indicate how many rows and how many of the 16 table columns were updated in each statement.


![Blog-updates Part 4.007.png](/uploads/Blog_updates_Part_4_007_8910a82d40.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/hot_bulk.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_HOT_BULK.json) behind the chart above.)*


In hot runs, where data is already cached, both PostgreSQL and ClickHouse finish bulk updates faster than in the cold case. But the relative picture doesn’t change: PostgreSQL still spends tens of seconds locating rows, while ClickHouse’s parallel scans keep updates in the sub\-second range, up to 700× faster on this dataset.


The following chart shows post\-update hot query times for all 10 queries after each bulk\-row UPDATE:


![Blog-updates Part 4.008.png](/uploads/Blog_updates_Part_4_008_951839272d.png)
*(See the raw benchmark results for [PostgreSQL](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/postgresql/results/hot_bulk.json) and [ClickHouse](https://github.com/ClickHouse/examples/blob/ec031e87ec602da81fb844d81757ee9f1e912b57/blog-examples/UPDATEBench/clickhouse/results/update_timings_sequential_lightweight_p20_HOT_BULK.json) behind the chart above.)*


With data cached, both systems see faster query times than in the cold runs. But the pattern holds: ClickHouse remains consistently much faster than PostgreSQL on the same hardware for analytical queries that immediately use the updated data.


Taken together, these tests show that ClickHouse not only applies changes quickly, but also makes them immediately useful for analytical queries, a rare combination in OLTP\-heavy scenarios.


## Conclusion [\#](/blog/update-performance-clickhouse-vs-postgresql#conclusion)


High\-performance SQL\-standard UPDATEs are a rare feature in column stores and analytical databases. They’re hugely beneficial to analytical workloads, and one of the most challenging stepping stones toward supporting OLTP\-style workloads.


When we set out to build UPDATEs for ClickHouse, the goal wasn’t to “beat Postgres.” That’s still not the goal. But we’re extremely proud that the effort has paid off with such convincing results: parity with PostgreSQL for single\-row updates, and speedups of up to 4,000× for bulk updates.


Cold runs expose how differently the two systems handle large scans: ClickHouse is up to 4,000× faster on bulk updates. Hot runs confirm the trade\-offs: PostgreSQL wins on cached point updates thanks to its B\-tree index, but ClickHouse remains much faster for analytical queries and even holds its own on single\-row OLTP\-style updates.


We know that Postgres is offering full transaction semantics that aren’t yet possible in ClickHouse, but never say never. We see no reason why ClickHouse couldn’t support transactions in the future.


And we learned something that, perhaps, should have been obvious:
You can’t UPDATE what you can’t find — and ClickHouse finds fast.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
