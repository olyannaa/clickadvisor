---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"An
topic: an-introduction-to-ibis-clickhouse
ch_version_introduced: '24.7'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 7
---

to group by multiple columns, we still need to use the `agg` function. If we want to see the underlying SQL executed when we run this code, we can use the `ibis.to_sql` function: ``` 1print(ibis.to_sql(flights.dest.topk(k=5))) ``` Copy command

```
1SELECT
2  *
3FROM (
4  SELECT
5    "t1"."dest",
6    COUNT(*) AS "CountStar()"
7  FROM (
8    SELECT
9      "t0"."year",
10      "t0"."month",
11      "t0"."day",
12      "t0"."dep_time",
13      "t0"."sched_dep_time",
14      COALESCE(CAST("t0"."dep_delay" AS Nullable(Int64)), 0) AS "dep_delay",
15      "t0"."arr_time",
16      "t0"."sched_arr_time",
17      COALESCE(CAST("t0"."arr_delay" AS Nullable(Int64)), 0) AS "arr_delay",
18      "t0"."carrier",
19      "t0"."flight",
20      "t0"."tailnum",
21      "t0"."origin",
22      "t0"."dest",
23      "t0"."air_time",
24      "t0"."distance",
25      "t0"."hour",
26      "t0"."minute",
27      "t0"."time_hour"
28    FROM "flights" AS "t0"
29  ) AS "t1"
30  GROUP BY
31    "t1"."dest"
32) AS "t2"
33ORDER BY
34  "t2"."CountStar()" DESC
35LIMIT 5
```
Copy command
This is more complicated than we’d write by hand and has too many sub\-queries for my liking, but I guess it does the job!

## Composing Ibis expressions \#

Ibis expressions are evaluated lazily, meaning we can store an expression in a variable and then apply other operations later in our program.

For example, let’s say we create a variable called `routes_by_carrier` that groups flights by `dest`, `origin`, and `carrier` and counts the number of rows for each grouping key:

```
1routes_by_carrier = (flights
2  .group_by([flights.dest,flights.origin, flights.carrier])
3  .agg(flightCount = _.count())
4)
5routes_by_carrier
```
Copy command

```
1┏━━━━━━━━┳━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━┓
2┃ dest   ┃ origin ┃ carrier ┃ flightCount ┃
3┡━━━━━━━━╇━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━┩
4│ string │ string │ string  │ int64       │
5├────────┼────────┼─────────┼─────────────┤
6│ BNA    │ JFK    │ MQ      │         365 │
7│ MKE    │ LGA    │ 9E      │         132 │
8│ SBN    │ LGA    │ EV      │           6 │
9│ CLE    │ LGA    │ EV      │         419 │
10│ AVL    │ EWR    │ EV      │         265 │
11│ FLL    │ EWR    │ B6      │        1386 │
12│ IAH    │ JFK    │ AA      │         274 │
13│ SAV    │ EWR    │ EV      │         736 │
14│ DFW    │ EWR    │ UA      │        1094 │
15│ BZN    │ EWR    │ UA      │          36 │
16│ …      │ …      │ …       │           … │
17└────────┴────────┴─────────┴─────────────┘
```
Copy command
We might decide later that we’d like to find flights with American Airlines or Delta Airlines as the `carrier`. We could do that with the following code:
