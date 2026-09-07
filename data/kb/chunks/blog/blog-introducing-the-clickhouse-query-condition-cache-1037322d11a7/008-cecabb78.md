---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Introducing
topic: introducing-the-query-condition-cache-clickhouse
ch_version_introduced: '100.00'
last_updated: '2026-09-07'
chunk_index: 8
total_chunks_in_doc: 10
---

AS count 4FROM bluesky 5WHERE 6 data.kind = 'commit' 7 AND data.commit.operation = 'create' 8 AND data.commit.collection = 'app.bsky.feed.post' 9 AND data.commit.record.text LIKE '%🥨%' 10GROUP BY language 11ORDER BY count DESC 12SETTINGS use_query_condition_cache = false; ``` Copy command

```
┌─language─┬─count─┐
│ en       │    38 │
│ de       │    10 │
│ ja       │     8 │
│ es       │     5 │
│ pt       │     2 │
│ nl       │     1 │
│ zh       │     1 │
│ el       │     1 │
│ fr       │     1 │
└──────────┴───────┘

9 rows in set. Elapsed: 0.601 sec. Processed 99.43 million rows, 9.00 GB (165.33 million rows/s., 14.96 GB/s.)
Peak memory usage: 418.93 MiB.
```
Copy command
Now, we’re back to an almost full table scan, as the query gains little benefit from the table’s primary index.

## Reusing the predicate: Peak pretzel posting hours \#

We wrap up the pretzel post analysis with a third query, again using the same predicate as before, that shows the most popular hours of the day for pretzel posts on Bluesky:

```
1SELECT
2    toHour(fromUnixTimestamp64Micro(data.time_us)) AS hour_of_day,
3    count() AS count,
4    bar(count, 0, 10, 30) AS bar
5FROM bluesky
6WHERE
7    data.kind = 'commit'
8    AND data.commit.operation = 'create'
9    AND data.commit.collection = 'app.bsky.feed.post'
10    AND data.commit.record.text LIKE '%🥨%'
11GROUP BY hour_of_day
12SETTINGS use_query_condition_cache = true;
```
Copy command
