---
source: blog
url: https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local
topic: enhancing-google-analytics-data-with-clickhouse
ch_version_introduced: '5.75'
last_updated: '2026-06-12'
chunk_index: 12
total_chunks_in_doc: 15
---

day. Even a site 100x larger than clickhouse.com should be able to host 10 yrs of data in a single Development Tier instance.** *\*This is prior to further schema optimizations e.g. removal of Nullables.* ### Query performance [\#](/blog/enhancing-google-analytics-data-with-clickhouse#query-performance)

The BigQuery export service for GA4 does not support the historical export of data. This prevents us from performing an extensive query test at this stage (we’ll share later based on real\-world usage), restricting the queries below to 42 days (the time since we started moving data from BigQuery into ClickHouse). This is sufficient for our use case as the majority of our queries cover a one\-month period, with queries analyzing historical trends rarer. The below queries query for total, returning, and new users for the month of October for the `blog` area of our website, grouping results by day.

**Total users**

```
SELECT
	event_date,
	uniqExact(user_pseudo_id) AS total_users
FROM ga_daily
WHERE (event_name = 'session_start') AND ((event_timestamp >= '2023-10-01') AND (event_timestamp <= '2023-10-31')) AND (page_location LIKE '%/blog/%')
GROUP BY event_date
ORDER BY event_date ASC

31 rows in set. Elapsed: 0.354 sec. Processed 4.05 million rows, 535.37 MB (11.43 million rows/s., 1.51 GB/s.)
Peak memory usage: 110.98 MiB.

```

**Returning users**

```
SELECT event_date, uniqExact(user_pseudo_id) AS returning_users
FROM ga_daily
WHERE (event_name = 'session_start') AND is_active_user AND (ga_session_number > 1 OR user_first_touch_timestamp < event_date) AND ((event_timestamp >= '2023-10-01') AND (event_timestamp <= '2023-10-31')) AND (page_location LIKE '%/blog/%')
GROUP BY event_date
ORDER BY event_date ASC

31 rows in set. Elapsed: 0.536 sec. Processed 4.05 million rows, 608.24 MB (7.55 million rows/s., 1.13 GB/s.)
Peak memory usage: 155.48 MiB.

```

**New Users**

```
SELECT event_date, count() AS new_users
FROM ga_daily
WHERE event_name = 'first_visit' AND ((event_timestamp >= '2023-10-01') AND (event_timestamp <= '2023-10-31')) AND (page_location LIKE '%/blog/%')
GROUP BY event_date
ORDER BY event_date ASC

31 rows in set. Elapsed: 0.320 sec. Processed 4.05 million rows, 411.97 MB (12.66 million rows/s., 1.29 GB/s.)
Peak memory usage: 100.78 MiB.

```

The above shows how all queries return in under 0\.5s. The ordering key for our table could be further optimized, and users are free to utilize features such as [Materialized Views](https://youtu.be/QUigKP7iy7Y?si=LOixamLYk93k1Yh6) and [Projections](https://clickhouse.com/blog/clickhouse-faster-queries-with-projections-and-primary-indexes) if further performance improvements are required.

### Cost [\#](/blog/enhancing-google-analytics-data-with-clickhouse#cost)
