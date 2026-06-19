---
source: blog
url: https://clickhouse.com/blog/log-compression-170x
topic: improve-logs-compression-with-log-clustering
ch_version_introduced: '100.0'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 13
---

`Extracted` Map(LowCardinality(String), String) 6) ORDER BY (ServiceName, TemplateNumber) ``` ``` Now we can create the view. Below is a minimal version that supports only one service, for the SQL statement that covers all of them, follow [this link](https://raw.githubusercontent.com/ClickHouse/examples/refs/heads/main/blog-examples/log_clustering/mv.sql).

```

```
1CREATE MATERIALIZED VIEW IF NOT EXISTS mv_logs_structured_min
2TO logs_structured
3AS
4SELECT
5    ServiceName,
6    /* which template matched */
7   multiIf(m1, 1, m2, 2, 0) AS TemplateNumber,
8    /* extracted fields as Map(LowCardinality(String), String) */
9    CAST(
10    multiIf(
11      m1,
12      map(
13        'date',           g1_1,
14        'time',           g1_2,
15        'service_name',   g1_3,
16        'trace_sampled',  g1_4,
17        'prod_1',         g1_5,
18        'prod_2',         g1_6,
19        'prod_3',         g1_7,
20        'prod_4',         g1_8,
21        'prod_5',         g1_9
22      ),
23      m2,
24      map(
25        'prod_1', g2_1,
26        'prod_2', g2_2,
27        'prod_3', g2_3,
28        'prod_4', g2_4,
29        'prod_5', g2_5
30      ),
31      map()                   -- else: empty map
32    ),
33    'Map(LowCardinality(String), String)'
34  ) AS Extracted
35FROM
36(
37    /* compute once per row */
38    WITH
39        '^([^\\s]+) ([^\\s]+) INFO \[main\] \[recommendation_server.py:47\] \[trace_id=([^\\s]+) span_id=([^\\s]+) resource\.service\.name=recommendation trace_sampled=True\] - Receive ListRecommendations for product ids:\[([^\\s]+) ([^\\s]+) ([^\\s]+) ([^\\s]+) ([^\\s]+)\]$' AS pattern1,
40        '^Receive ListRecommendations for product ([^\\s]+) ([^\\s]+) ([^\\s]+) ([^\\s]+) ([^\\s]+)$' AS pattern2
41
42    SELECT
43        *,
44        match(Body, pattern1) AS m1,
45        match(Body, pattern2) AS m2,
46
47        extractAllGroups(Body, pattern1) AS g1,
48        extractAllGroups(Body, pattern2) AS g2,
49
50        /* pick first (and only) match’s capture groups */
51        arrayElement(arrayElement(g1, 1), 1) AS g1_1,
52        arrayElement(arrayElement(g1, 1), 2) AS g1_2,
53        arrayElement(arrayElement(g1, 1), 3) AS g1_3,
54        arrayElement(arrayElement(g1, 1), 4) AS g1_4,
55        arrayElement(arrayElement(g1, 1), 5) AS g1_5,
56        arrayElement(arrayElement(g1, 1), 6) AS g1_6,
57        arrayElement(arrayElement(g1, 1), 7) AS g1_7,
58        arrayElement(arrayElement(g1, 1), 7) AS g1_8,
59        arrayElement(arrayElement(g1, 1), 7) AS g1_9,
60
61        arrayElement(arrayElement(g2, 1), 1) AS g2_1,
62        arrayElement(arrayElement(g2, 1), 2) AS g2_2,
63        arrayElement(arrayElement(g2, 1), 3) AS g2_3,
64        arrayElement(arrayElement(g2, 1), 4) AS g2_4,
65        arrayElement(arrayElement(g2, 1), 5) AS g2_5
66
67    FROM raw_logs where ServiceName='recommendation'
68) WHERE m1 OR m2;
```

```

> In the full version, this approach may not scale efficiently because every pattern is evaluated against all logs, even when no match is possible. Later, we’ll look at an optimized approach that helps with this.

We reingest the data to the `raw_logs` table to execute the materialized view.
