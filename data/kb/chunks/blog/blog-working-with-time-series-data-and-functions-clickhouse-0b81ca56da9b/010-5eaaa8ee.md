---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Working
topic: working-with-time-series-data-in-clickhouse-clickhouse
ch_version_introduced: '15.329'
last_updated: '2026-09-07'
chunk_index: 10
total_chunks_in_doc: 16
---

the previous example, sometimes we want to do the opposite \- get a cumulative sum of certain metrics over time. This is usually used for counters to visualize cumulative growth and can be easily implemented using window functions:

```

SELECT
    toDate(time) AS d,
    sum(hits) AS h,
    sum(h) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND 0 FOLLOWING) AS c,
    bar(c, 0, 3200000, 25) AS b
FROM wikistat
WHERE path = 'Ana_Sayfa'
GROUP BY d
ORDER BY d ASC
LIMIT 15

┌──────────d─┬──────h─┬───────c─┬─b─────────────────────────┐
│ 2015-05-01 │ 214612 │  214612 │ █▋                        │
│ 2015-05-02 │ 211546 │  426158 │ ███▎                      │
│ 2015-05-03 │ 221412 │  647570 │ █████                     │
│ 2015-05-04 │ 219940 │  867510 │ ██████▋                   │
│ 2015-05-05 │ 211548 │ 1079058 │ ████████▍                 │
│ 2015-05-06 │ 212358 │ 1291416 │ ██████████                │
│ 2015-05-07 │ 208150 │ 1499566 │ ███████████▋              │
│ 2015-05-08 │ 208871 │ 1708437 │ █████████████▎            │
│ 2015-05-09 │ 210753 │ 1919190 │ ██████████████▊           │
│ 2015-05-10 │ 212918 │ 2132108 │ ████████████████▋         │
│ 2015-05-11 │ 211884 │ 2343992 │ ██████████████████▎       │
│ 2015-05-12 │ 212314 │ 2556306 │ ███████████████████▊      │
│ 2015-05-13 │ 211192 │ 2767498 │ █████████████████████▌    │
│ 2015-05-14 │ 206172 │ 2973670 │ ███████████████████████▏  │
│ 2015-05-15 │ 195832 │ 3169502 │ ████████████████████████▋ │
└────────────┴────────┴─────────┴───────────────────────────┘

15 rows in set. Elapsed: 0.557 sec. Processed 1.00 billion rows, 28.62 GB (1.80 billion rows/s., 51.40 GB/s.)

[✎](https://sql.clickhouse.com?query_id=CRHBCIOY1ZKMX6ZK7DXG7Z)

```

We’ve built cumulative daily hits sum and visualized growth for a given page within a 15\-day period.

### Rates \#

Calculating metric rates (speed per time unit) is also popular when working with time series. Suppose we want to get a certain page hit rate per second for a given date grouped by hours:
