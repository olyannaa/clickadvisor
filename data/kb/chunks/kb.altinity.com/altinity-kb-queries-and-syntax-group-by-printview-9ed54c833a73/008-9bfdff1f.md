---
source: kb.altinity.com
url: https://github.com/ClickHouse/ClickHouse/blob/8ab5270ded39c8b044f60f73c1de00c8117ab8f2/src/Interpreters/Aggregator.cpp#L382
topic: group-by-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '8.888'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 14
---

/ 300) AS created_at, CAST((number + 14) % 3, 'Enum8(\'Bat\' = 0, \'Mice\' = 1, \'Rat\' = 2)') AS platform, number % 17 AS clicks, generateUUIDv4() AS session_id SELECT app, user_id, created_at, platform, clicks, session_id FROM numbers_mt(1000000000); ```

```
SELECT
    app,
    platform,
    sum(clicks)
FROM
(
    SELECT
        argMax(app, created_at) AS app,
        argMax(platform, created_at) AS platform,
        user_id,
        argMax(clicks, created_at) AS clicks
    FROM sessions_distributed
    GROUP BY user_id
)
GROUP BY
    app,
    platform;

[chi-distr-groupby-distr-groupby-0-0-0] MemoryTracker: Current memory usage (for query): 12.02 GiB.
[chi-distr-groupby-distr-groupby-1-0-0] MemoryTracker: Current memory usage (for query): 12.05 GiB.
[chi-distr-groupby-distr-groupby-2-0-0] MemoryTracker: Current memory usage (for query): 12.05 GiB.

MemoryTracker: Peak memory usage (for query): 12.20 GiB.

12 rows in set. Elapsed: 28.345 sec. Processed 1.00 billion rows, 32.00 GB (35.28 million rows/s., 1.13 GB/s.)

SELECT
    app,
    platform,
    sum(clicks)
FROM
(
    SELECT
        argMax(app, created_at) AS app,
        argMax(platform, created_at) AS platform,
        user_id,
        argMax(clicks, created_at) AS clicks
    FROM sessions_distributed_2
    GROUP BY user_id
)
GROUP BY
    app,
    platform;

[chi-distr-groupby-distr-groupby-0-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
[chi-distr-groupby-distr-groupby-1-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
[chi-distr-groupby-distr-groupby-2-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.

MemoryTracker: Peak memory usage (for query): 5.61 GiB.

12 rows in set. Elapsed: 11.952 sec. Processed 1.00 billion rows, 32.00 GB (83.66 million rows/s., 2.68 GB/s.)

SELECT
    app,
    platform,
    sum(clicks)
FROM
(
    SELECT
        argMax(app, created_at) AS app,
        argMax(platform, created_at) AS platform,
        user_id,
        argMax(clicks, created_at) AS clicks
    FROM sessions_distributed_2
    GROUP BY user_id
)
GROUP BY
    app,
    platform
SETTINGS optimize_distributed_group_by_sharding_key = 1

[chi-distr-groupby-distr-groupby-0-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
[chi-distr-groupby-distr-groupby-1-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
[chi-distr-groupby-distr-groupby-2-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
MemoryTracker: Peak memory usage (for query): 5.61 GiB.

12 rows in set. Elapsed: 11.916 sec. Processed 1.00 billion rows, 32.00 GB (83.92 million rows/s., 2.69 GB/s.)


SELECT
    app,
    platform,
    sum(clicks)
FROM cluster('distr-groupby', view(
    SELECT
        app,
        platform,
        sum(clicks) as clicks
    FROM
    (
        SELECT
            argMax(app, created_at) AS app,
            argMax(platform, created_at) AS platform,
            user_id,
            argMax(clicks, created_at) AS clicks
        FROM sessions_2
        GROUP BY user_id
    )
    GROUP BY
        app,
        platform
))
GROUP BY
    app,
    platform;

[chi-distr-groupby-distr-groupby-0-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
[chi-distr-groupby-distr-groupby-1-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.
[chi-distr-groupby-distr-groupby-2-0-0] MemoryTracker: Current memory usage (for query): 5.05 GiB.

MemoryTracker: Peak memory usage (for query): 5.55 GiB.

12 rows in set. Elapsed: 9.491 sec. Processed 1.00 billion rows, 32.00 GB (105.36 million rows/s., 3.37 GB/s.)

```
Query with bigger state:
