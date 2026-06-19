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


- Capture everything a PostgreSQL cluster does: every SELECT, INSERT, DDL, and even the queries that fail.
- Ship events off to an external system to handle analyses
- Incur minimal overhead to PostgreSQL


We haven’t shipped pg\_stat\_ch to production yet, but we’re actively driving it there as part of ClickHouse’s managed Postgres effort. Today it streams per\-query events into ClickHouse with a 2KB query text cap and no plan capture yet.


If you operate PostgreSQL at scale, we’d love feedback, and we’ll keep sharing what we learn as it hardens.

### Try the unified data stack

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-60-try-the-unified-data-stack-get-access&utm_blogctaid=60)## The architecture in 30 seconds [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#the-architecture-in-30-seconds)


Under the hood, pg\_stat\_ch does the minimum work possible: on the hot path it’s just a [memcpy](https://en.cppreference.com/w/cpp/string/byte/memcpy.html) into a shared\-memory ring buffer. A background worker wakes up once a second, batches what’s in the buffer, and flushes it using ClickHouse’s native binary protocol with LZ4 compression.


![pg_stat_ch architecture diagram](/uploads/Logo_Architecture_Diagrams_for_pg_stat_ch_Release_Blog_1365_Open_e095fb2920.png)
Every time PostgreSQL executes a statement, whether it’s a SELECT, an INSERT, DDL, or even a query that fails with a syntax error, `pg_stat_ch` records it as a fixed size event. Each event includes 45 fields, covering timing, buffer I/O, WAL, CPU and JIT stats, error details, and basic client context.


From there, the backend does one quick copy into a shared\-memory ring buffer and moves on. Once a second, a background worker drains up to 10,000 events, packs them into a columnar block, compresses it with LZ4, and sends it to ClickHouse over the native binary protocol.


On the ClickHouse side, raw events land in [the `events_raw` table](https://github.com/ClickHouse/pg_stat_ch/blob/main/docker/init/00-schema.sql), and four materialized views pre\-aggregate them into dashboards you can query immediately:




| View | What it does |
| --- | --- |
| events\_recent\_1h | Rolling 1\-hour copy for “what’s happening right now” |
| query\_stats\_5m | 5\-minute buckets with p95/p99 via quantilesTDigest |
| db\_app\_user\_1m | Per\-database/app/user load attribution, 1\-minute granularity |
| errors\_recent | 7\-day rolling window of every error with full context |


The important bit here is that **all aggregation happens in ClickHouse, not in PostgreSQL.** Postgres captures events and pushes them out. ClickHouse compresses, stores, and answers analytical queries.


## Engineering decisions [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#engineering-decisions)


### Decision 1: fixed\-size events [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-1-fixed-size-events)


We had two options for event data: variable\-length (allocate per event based on query text size, like pg\_stat\_monitor does with [PostgreSQL’s DSA allocator](https://tselai.com/pg-dsm-registry-allocations)) or fixed\-size.


We chose fixed\-size. The memcpy is fast, but the real cost is LWLock acquisition, name resolution (get\_database\_name, GetUserNameFromId, GetClientAddress), and getrusage() for CPU timing. [We’ll get to the measured overhead below.](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#overhead-on-postgresql)


The bigger advantage of fixed\-size is a predictable memory footprint you can reason about at startup:



```
queue_capacity = 65,536 events (default)
event_size     = ~4.6 KB
total memory   = 65,536 × 4.6 KB = 294.4 MB

```

You know exactly how much shared memory you need at shared\_preload\_libraries time. The queue capacity and event size are configurable settings, so you can tune based on your workload.


There is a tradeoff: query texts longer than 2KB (or the configured event size) get truncated. You still get the fingerprint (query\_id) and all 45 metrics. If it’s running, you can look up the full text by the query\_id in pg\_stat\_statements.


### Decision 2: ensure negligible impact on Postgres [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-2-ensure-negligible-impact-on-postgres)


The ring buffer is the hottest data structure in the extension. Every backend process writes to it (producers), and one background worker reads from it (consumer). On a busy 32\-core system, that’s potentially dozens of concurrent writers.


Here’s the layout:



```
┌───────────────────────────────────────────┐
│ [Rarely changed]                          │
│   LWLock* lock                            │
│   uint32  capacity                        │
│                                           │
│ ─── CACHE LINE BOUNDARY (64 bytes) ───────│
│                                           │
│ [Producer-hot: many backends write]       │
│   atomic_uint64 head                      │
│   atomic_uint64 enqueued                  │
│   atomic_uint64 dropped                   │
│   atomic_flag   overflow_logged           │
│                                           │
│ ─── CACHE LINE BOUNDARY ──────────────────│
│                                           │
│ [Consumer-hot: bgworker reads/writes]     │
│   atomic_uint64 tail                      │
│   atomic_uint64 exported                  │
│                                           │
│ ─── CACHE LINE BOUNDARY ──────────────────│
│                                           │
│ [Stats: bgworker writes, anyone reads]    │
│   atomic_uint64 send_failures             │
│   TimestampTz   last_success_ts           │
│   TimestampTz   last_error_ts             |
│   char          last_error_text[256]      │
│   atomic_uint32 bgworker_pid              │
└───────────────────────────────────────────┘

```

The PG\_CACHE\_LINE\_SIZE padding between sections is the critical detail. Without it, every time the background worker updates tail, it invalidates the cache line containing head on every producer’s CPU core. That’s **false sharing** — and on multi\-socket systems it can cost 50–100ns per access. With the separation, producer cores and the consumer core work on independent cache lines and never interfere.


The capacity is always a power of 2 (1,024 to 65,536\), so slot addressing uses a bitmask (index \& (capacity \- 1\)) instead of modulo. One fewer division instruction in the hot path.


### Decision 3: no back\-pressure [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-3-no-back-pressure)


There are exactly two ways events can be lost, and both are deliberate:


1. **Queue overflow.** The ring buffer fills up faster than the background worker drains it. New events are dropped — the producer atomically increments a dropped counter and returns in nanoseconds.
2. **Export failure.** The background worker dequeues a batch, then the ClickHouse insert fails. Those events are gone. We don’t re\-enqueue them.


The alternative is back\-pressure. That would mean if ClickHouse slows down or goes offline, PostgreSQL starts feeling it too, and your queries get slower. **For us, that’s a non\-starter.**


For an OLTP system doing 50,000 queries/second, if back\-pressure adds a 10ms stall per query during a ClickHouse blip, p99 latency goes from 5ms to 15ms. This would have a material impact on SLOs and users will notice. This is not an acceptable tradeoff for monitoring.


This is the same philosophy behind UDP\-based metrics systems ([StatsD](https://www.etsy.com/codeascraft/measure-anything-measure-everything#:~:text=brag%20about%20them.-,Why%20UDP%3F,-So%2C%20why%20do), [DogStatsD](https://pkg.go.dev/github.com/DataDog/datadog-agent/cmd/dogstatsd?utm_source=chatgpt.com#section-readme:~:text=datadog/dogstatsd%3Alatest-,Why%20UDP%3F,-Like%20StatsD%2C%20DogStatsD)): a few lost data points are infinitely preferable to affecting the system you’re observing.


**Observability should observe, not obstruct.**


The dropped counter is visible via the included pg\_stat\_ch\_stats() function so you can monitor overflow and tune queue\_capacity. In practice, with a 1\-second flush interval and 10K batch size, you need sustained 65K QPS with a completely stalled ClickHouse to start dropping.


### Decision 4: minimize lock contention [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-4-minimize-lock-contention)


The enqueue path uses three tiers to minimize lock contention:


![pg_stat_ch enqueue path](/uploads/Dark_Mode_New_Diagram_0807f482fc.png)
1. **Step 1** is the safety valve. We check for overflow using atomics only. If the ring is full, we drop the event and return immediately. Overflow handling never takes a lock.
2. **Step 2** is the normal case. We try to grab the [LWLock](https://doxygen.postgresql.org/lwlock_8h_source.html) without blocking. When there is no contention, enqueue looks just like the simple design: take the lock, memcpy into the slot, bump head, release.
3. **Step 3** allows it to scale when you have lots of backends running at once (say 32\+). Instead of every backend vying for the same exclusive lock for every query, each backend stashes events in a small process\-local buffer and flushes them once per transaction. On TPC\-B, with about 5 queries per transaction, this design cuts lock acquisitions from roughly 150K per second to about 30K per second, around a 5x reduction.


That process\-local buffer lives in static [BSS](https://en.wikipedia.org/wiki/.bss), about 37KB per backend (8 events × \~4\.6KB each). pg\_stat\_ch also registers an [`on_shmem_exit`](https://doxygen.postgresql.org/ipc_8h.html) handler to flush anything left at backend shutdown, exporting buffered events even when a backend exits mid\-transaction.


### Decision 5: native protocol with LZ4 [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-5-native-protocol-with-lz4)


We use ClickHouse’s native binary protocol via clickhouse\-cpp (statically linked into the extension .so) rather than HTTP. Three reasons:


1. **LZ4 block compression** — critical for reducing bandwidth when shipping thousands of events/second over the network
2. **Columnar encoding** — data is sent column\-major, which ClickHouse can ingest directly without row\-to\-column transposition
3. **Type\-safe binary encoding** — no JSON parsing overhead


We compile the clickhouse\-cpp client into the extension as a static library. That keeps deployment simple: no extra runtime dependencies beyond PostgreSQL (and optionally OpenSSL). The downside is size. Static linking pushes the extension over 20 MB, but we’re fine with that tradeoff if it means fewer “it works on my box” surprises.


We intentionally set socket timeouts to 30 seconds. The background worker still needs to respond to PostgreSQL signals, especially during operations like DROP DATABASE (via `procsignal_sigusr1_handler`). If we used infinite timeouts and the network to ClickHouse stalled, we could end up hanging DROP DATABASE until the socket unwedged, which is not acceptable.


## How we hook into PostgreSQL [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#how-we-hook-into-postgresql)


PostgreSQL offers extensions a handful of hooks. pg\_stat\_ch wires into those hooks to capture the right data at the right moment, before Postgres tears down the state we need. Here are the hooks we use, what we do in each one, and why each matters.




| Hook | What pg\_stat\_ch Does | Why Here? |
| --- | --- | --- |
| ExecutorStart | Record query\_start\_ts, CPU baseline via getrusage(), enable INSTRUMENT\_ALL | Need a time\-zero reference *before* any work. If we don’t enable instrumentation here, Postgres won’t collect buffer/WAL/timing stats at all. |
| ExecutorRun | Increment/decrement nesting level (with PG\_FINALLY for exception safety) | Tracks query nesting for CTEs, subqueries, function calls. Otherwise, a nested query’s metrics bleed into the parent. |
| ExecutorFinish | Same nesting\-level tracking | AFTER triggers fire here and can execute nested queries — would corrupt the nesting count without tracking. |
| ExecutorEnd | **Main collection point.** Finalize timing, compute CPU delta, extract all 45 fields, enqueue event. | Must happen *before* standard\_ExecutorEnd() because it nulls out estate, planstate, totaltime. |
| ProcessUtility | Snapshot buffer/WAL/CPU counters, execute, compute delta | DDL/COPY/VACUUM bypass the executor entirely — no QueryDesc, no instrumentation. We manually compute the delta. |
| emit\_log\_hook | Capture SQLSTATE, severity, message text for errors | Error tracking is impossible from executor hooks alone. Syntax errors, permission denials, constraint violations — none of them reach ExecutorEnd. |


All hooks chain to previous hook values, so pg\_stat\_ch coexists with pg\_stat\_statements, auto\_explain, pg\_tracing, and anything else. The chaining order follows shared\_preload\_libraries load order.


![pg_stat_ch postgres hooks](/uploads/Logo_Architecture_Diagrams_for_pg_stat_ch_Release_Blog_1365_Open_1_8cdff66547.png)
## Overhead on PostgreSQL [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#overhead-on-postgresql)


We ran pgbench (TPC\-B, scale factor 10, 32 clients, 8 threads, 30 seconds) on an [AMD Ryzen AI MAX\+ 395 (16c/32t, 64MB L3, 128GB RAM)](https://frame.work/desktop) against PostgreSQL 18 with and without pg\_stat\_ch. ClickHouse was running locally in Docker.




|  | TPS | latency avg |
| --- | --- | --- |
| without pg\_stat\_ch | 41,309 | 0\.775 ms |
| with pg\_stat\_ch | 36,656 | 0\.873 ms |
| overhead | \~11% | \~11% |


At 36\.6K TPS, pg\_stat\_ch captured **7\.7 million events** over 30 seconds with **zero drops** (queue\_capacity\=4M, flush\_interval\=100ms, batch\_max\=100K). Each number is the average of two consecutive runs.


Here’s the flamegraph:


![Flamegraph of pgbench with pg_stat_ch](/uploads/image2_c36d949269.png)
We also profiled 8 backends for 10 seconds using perf record with DWARF call graphs:



```
Overhead Component                    % of CPU
──────────────────────────────────────────────────
Enqueue (try-lock fast path)            0.94%    ← was 2.32% before batching
  Batch flush (XactCallback → batch)    0.54%    ← new: amortized lock path
BuildEvent (QueryDesc → struct)         0.33%
ProcessUtility overhead                 0.08%
InstrAlloc (enable instrumentation)     0.05%
Nesting tracking (Run + Finish)         0.05%
──────────────────────────────────────────────────
TOTAL pg_stat_ch CPU overhead          ~2.0%

```

So, the observed CPU overhead of pg\_stat\_ch is \~2%. The \~11% overhead to TPS/latency we see in the benchmark is due to contention amplification on the enqueue lock. This pgbench TPC\-B setup has very short, sub\-millisecond transactions at high concurrency, so even a small serialized section can translate to a noticeable TPS drop.


Before [the try\-lock \+ local batching change](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#decision-4-minimize-lock-contention), pg\_stat\_ch acquired the enqueue LWLock on every query. Under this workload that lock became a hot spot and the TPS drop was about 24%. The try\-lock \+ local batching optimization brought this down to about 11%: backends now attempt a non\-blocking enqueue and, if the lock is contended, buffer events locally and flush them once per transaction. With roughly 5 queries per TPC\-B transaction, this reduces lock acquisitions from \~150K/s to \~30K/s (a 5x reduction), which materially reduces contention.


This also explains the apparent mismatch between \~2% CPU overhead and \~11% TPS overhead. The \~2% figure is the time spent in pg\_stat\_ch code itself (building events, enqueue fast path, batched flush) and it excludes the knock\-on effects of lock contention. The remaining gap is time lost to lock contention and scheduling effects around the shared enqueue path, which shows up as reduced throughput rather than CPU time spent in the extension.


TPC\-B at 32 clients is probably close to the worst case for this effect, we expect that most real workloads will see less impact. We’ll publish additional numbers on more representative workloads shortly after launch to quantify overhead when lock pressure is lower.


## Storage \& compression in ClickHouse [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#storage--compression-in-clickhouse)


Each PschEvent is fixed size in PostgreSQL shared memory. We shipped 7\.7M pgbench events to ClickHouse and measured the actual on\-disk size:



```
7.7M events × ~4.6KB ≈ 35 GB as raw structs
ClickHouse compressed:     426 MB
compression ratio:         ~83:1 (from raw event size)
bytes per row:             ~36 bytes compressed

```

The per\-column breakdown shows where the compression wins:




| Column | Compressed | Ratio | Bytes/row |
| --- | --- | --- | --- |
| query (text) | 119 MB | 5\.6:1 | 10\.0 |
| ts\_start | 44 MB | 2\.2:1 | 3\.7 |
| cpu\_user\_time\_us | 33 MB | 2\.9:1 | 2\.8 |
| duration\_us | 32 MB | 3\.0:1 | 2\.7 |
| query\_id | 30 MB | 3\.2:1 | 2\.5 |
| db | 317 KB | 230:1 | \~0 |
| username | 440 KB | 221:1 | \~0 |
| app | 440 KB | 221:1 | \~0 |


Low\-cardinality strings (db, username, app) compress to almost nothing — dictionary encoding reduces them to a few bits per row. The query column dominates at 119MB, but pgbench has only a handful of distinct query texts that repeat millions of times, so even that compresses 5\.6:1\.


A real workload with more diverse queries would compress differently — the query column would be larger, but the low\-cardinality columns would still be near\-zero. The point stands: months of query telemetry fits in surprisingly little space.


For a real workload at 10K QPS, we’d expect this to work out at under $100/month in storage costs:



```
events per day:       10,000 × 86,400 = 864M
raw event size:       864M × 4.6KB ≈ 4 TB/day
at 36 bytes/row:      864M × 36 = ~31 GB/day
monthly storage:      31 × 30 = ~930 GB/month

cloud block storage:  ~$0.08/GB/month = ~$74/month
S3-backed cold tiers: ~$0.02/GB/month = ~$19/month

```

We think that’s pretty reasonable for a 10K QPS workload, for the level of insight it allows over the events.

### Try the unified data stack

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-61-try-the-unified-data-stack-get-access&utm_blogctaid=61)## What you can actually do with raw events [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#what-you-can-actually-do-with-raw-events)


With raw events per query in ClickHouse, you can ask questions that are impossible with aggregate\-only systems. Here are some real queries:


**Find the individual queries causing cache misses:**



```
SELECT
    query_id,
    any(query) AS sample_query,
    count() AS executions,
    avg(shared_blks_read) AS avg_physical_reads,
    sum(shared_blks_read) AS total_physical_reads
FROM events_raw
WHERE ts_start > now() - INTERVAL 24 HOUR
  AND shared_blks_read > 1000
GROUP BY query_id
ORDER BY total_physical_reads DESC
LIMIT 20;

```

**Showing the most expensive queries with percentile distributions:**



```
SELECT
    query_id,
    any(query) AS sample_query,
    count() AS executions,
    round(100 * sum(duration_us) / (
        SELECT sum(duration_us)
        FROM pg_stat_ch.events_raw
        WHERE ts_start > now() - INTERVAL 24 HOUR
    ), 2) AS pct_runtime,
    count() AS cnt,    round(sum(duration_us) / 1e6, 2) AS total_seconds,
    round(quantile(0.50)(duration_us) / 1000, 0) AS p50_ms,
    round(quantile(0.90)(duration_us) / 1000, 0) AS p90_ms,
    round(quantile(0.99)(duration_us) / 1000, 0) AS p99_ms
FROM pg_stat_ch.events_raw
WHERE ts_start > now() - INTERVAL 24 HOUR
GROUP BY query_id
ORDER BY sum(duration_us) DESC
LIMIT 20;

```

Important details about the health of your Postgres database with a large lookback window, queries over ALL your historical insights in seconds, thanks to ClickHouse.


In fact, ClickHouse enables some truly fascinating queries. We can now see which query ran the most during our pgbench benchmark. Not the *type* of the query, but the ***exact*** query:



```
SELECT
    query,
    cmd_type,
    count(*) AS c
FROM events_raw
WHERE (query_id > 0) AND (cmd_type != 'UTILITY') AND (cmd_type != 'SELECT')
GROUP BY
    query,
    cmd_type
ORDER BY c DESC
LIMIT 5

Query id: abfc5785-48d8-4111-bfb9-2696a010a6d3
┌─query────────────────────────────────────┬─cmd_type─┬──c─┐
│ UPDATE pgbench_branches SET bbalance...  │ UPDATE   │ 26 │
│ UPDATE pgbench_branches SET bbalance...  │ UPDATE   │ 26 │
│ UPDATE pgbench_branches SET bbalance...  │ UPDATE   │ 26 │
│ UPDATE pgbench_branches SET bbalance...  │ UPDATE   │ 26 │
│ UPDATE pgbench_branches SET bbalance...  │ UPDATE   │ 25 │
└──────────────────────────────────────────┴──────────┴────┘
5 rows in set. Elapsed: 10.268 sec. Processed 63.33 million rows, 3.43 GB (6.17 million rows/s., 333.55 MB/s.)

```

The materialized views handle this too. The [\*State() / \*Merge() pattern](https://clickhouse.com/docs/sql-reference/aggregate-functions/combinators#-state) means aggregates are incrementally maintained — no re\-scanning raw data for dashboards:



```
CREATE MATERIALIZED VIEW query_stats_5m TO query_stats_5m_target AS
SELECT
    toStartOfFiveMinutes(ts_start) AS bucket,
    db, query_id, cmd_type,
    countState()                                    AS calls,
    quantilesTDigestState(0.95, 0.99)(duration_us)  AS duration_quantiles,
    sumState(shared_blks_hit)                       AS total_shared_blks_hit,
    sumState(shared_blks_read)                      AS total_shared_blks_read
FROM events_raw
GROUP BY bucket, db, query_id, cmd_type;

```

Query query\_stats\_5m for dashboards, events\_raw for drill\-down. Both are always up to date.


Using these, we can build monitoring dashboards to track the things we need to know:


![A ClickHouse Cloud dashboard for monitoring Postgres using pg_stat_ch](/uploads/postgres_dashboard_4d510ac57a.png)
## Comparison with other extensions [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#comparison-with-other-extensions)


There are several good tools in the Postgres metrics\-collection space already; they solve overlapping but different problems.


### pg\_stat\_statements [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#pg_stat_statements)


[pg\_stat\_statements](https://www.postgresql.org/docs/current/pgstatstatements.html) is the baseline every DBA is familiar with.


It has zero additional infrastructure, stores full query text and is battle\-tested over a decade. If you need basic “top queries by total time” and nothing else, it’s perfect.


What it didn’t solve for us is time\-series analysis (events have timestamps), percentiles (not just mean/min/max), error tracking (SQLSTATE \+ message \+ severity), and indefinite retention. If you need to answer “what changed between 2pm and 3pm yesterday?”, pg\_stat\_statements isn’t the answer.


Both use the same query\_id fingerprint, so they correlate naturally and you can run both.


### pg\_stat\_monitor [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#pg_stat_monitor)


Percona’s [pg\_stat\_monitor](https://docs.percona.com/pg-stat-monitor/) is the most ambitious extension in this space. It adds time\-bucketed histograms, query plan capture, error tracking, and client IP tracking on top of pg\_stat\_statements.


pg\_stat\_monitor includes query plan capture, which pg\_stat\_ch does not have yet, and it’s the single biggest feature gap. Also: no external dependencies. You CREATE EXTENSION and you’re done.


However, pg\_stat\_ch has unlimited retention (pg\_stat\_monitor rotates through N shared\-memory buckets — hours at most), raw event granularity instead of pre\-aggregated buckets, lower hot\-path overhead (memcpy vs. hash\-table lookup \+ update per query), and the full power of ClickHouse SQL for ad\-hoc analysis. Also, ClickHouse compression: a typical event compresses to \~100–200 bytes on disk, vs. the \~4\.6KB in Postgres shared memory.


### pg\_tracing [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#pg_tracing)


[pg\_tracing](https://github.com/DataDog/pg_tracing) generates OpenTelemetry spans for each query, including sub\-spans for individual plan nodes (SeqScan, HashJoin, etc.), triggers, and parallel workers. It adds distributed tracing for PostgreSQL.


These extensions solve different problems: pg\_tracing answers “why was *this specific query* slow?” (was it the HashJoin? the IndexScan? a trigger?), while pg\_stat\_ch answers “which queries are slow and do they trend over time?”


Again, you could run both: pg\_stat\_ch for fleet\-wide observability and alerting, pg\_tracing for individual slow queries analysis when pg\_stat\_ch tells you something is off.


### OpenTelemetry Collector [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#opentelemetry-collector)


The [OTel Collector PostgreSQL Receiver](https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/receiver/postgresqlreceiver/README.md) is an external scraper that polls pg\_stat\_\* views at configurable intervals.


If you already have an OTel pipeline, it slots in easily without needing to reconfigure much. It also collects system\-level metrics (connections, locks, replication lag) that pg\_stat\_ch doesn’t.


However, an external scraper with a 10\-second interval can never capture individual query executions. It only sees pre\-aggregated counter deltas. If you need to know “what queries executed between 3:00:00 and 3:00:05”, only an in\-process extension can tell you.

### Try the unified data stack

ClickHouse \+ Postgres has become the unified data stack for applications that scale. With Managed Postgres now available in ClickHouse Cloud, this stack is a day\-1 decision.[Get access](https://clickhouse.com/cloud/postgres?loc=blog-cta-62-try-the-unified-data-stack-get-access&utm_blogctaid=62)## What’s next [\#](/blog/pg_stat_ch-postgres-extension-stats-to-clickhouse#whats-next)


We’re actively working on:


- **Query plan capture**: storing execution plans as separate events
- **Sampling support**: for extremely high\-throughput systems that can’t afford to capture every query
- **[ClickStack](https://clickhouse.com/clickstack) \& Grafana dashboard templates**: pre\-built dashboards for common patterns
- **Production hardening**: stress testing, edge cases, more version coverage


pg\_stat\_ch also pairs naturally with [pg\_clickhouse](https://clickhouse.com/blog/introducing-pg_clickhouse), our extension for querying ClickHouse from PostgreSQL. Push telemetry with pg\_stat\_ch \& query it back via foreign tables without leaving psql.


We’d love your feedback. If you run PostgreSQL in production and care about observability, try pg\_stat\_ch and tell us what works and what’s broken. Join us in our [community Slack](https://clickhouse.com/slack)!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
