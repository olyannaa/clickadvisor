# A simple guide to ClickHouse query optimization: part 1


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# A simple guide to ClickHouse query optimization: part 1

![](/_next/image?url=%2Fuploads%2Flio_headshot_singapore_7cc9852011.jpg&w=96&q=75)[Lionel Palacin](/authors/lionel-palacin)Dec 11, 2024 · 24 minutes read
> You can find updated guidance on ClickHouse query optimization for 2026 and beyond in [The definitive guide to ClickHouse query optimization](https://clickhouse.com/resources/engineering/clickhouse-query-optimisation-definitive-guide?utm_medium=clickhouse&utm_source=blog&ref=a-simple-guide-to-clickhouse-query-optimization-part-1)


I started working on the product marketing engineering team at ClickHouse a few months ago. Coming from Elastic, where I focused on the Search solution, I had a lot to learn about ClickHouse and OLAP databases in general.


One of my first projects at ClickHouse was helping bring the new [ClickHouse Playground](https://sql.clickhouse.com/) to life. The Playground contains many different datasets, making it the perfect place for me to learn ClickHouse.


As we launched the ClickHouse Playground, I was curious about the user experience and whether some of the example queries we provided could be improved. Thanks to widely available learning materials, such as [on\-demand training](https://clickhouse.com/learn), [videos](https://www.youtube.com/@ClickHouseDB/videos), [documentation](https://clickhouse.com/docs), and [blogs](https://clickhouse.com/blog), I’ve learned a lot about optimizing ClickHouse queries. This is the first blog in a two\-part series in which I’ll share some tips for doing this.


In the first part, we present the tooling ClickHouse supports to investigate slow queries. Then, we discuss basic optimization and the importance of primary keys. In the next part, we will cover more advanced techniques to optimize queries, such as [projections](https://clickhouse.com/docs/en/sql-reference/statements/alter/projection), [materialized views](https://clickhouse.com/docs/en/materialized-view), and [data\-skipping indexes](https://clickhouse.com/docs/en/optimize/skipping-indexes).


## Understand query performance [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#understand-query-performance)


The best moment to think about performance optimization is when you’re setting up your [data schema](https://clickhouse.com/docs/en/data-modeling/schema-design) before ingesting data into ClickHouse for the first time. 


But let’s be honest; it is difficult to predict how much your data will grow or what types of queries will be executed. 


So, if you haven’t started your journey with ClickHouse, maybe you want to skip this part and go straight to the next section to learn about basic optimizations and the importance of primary keys. 


But if you have an existing deployment with a few queries that you want to improve, the first step is understanding how those queries perform and why some execute in a few milliseconds while others take longer.


ClickHouse has a rich set of tools to help you understand how your query is getting executed and the resources consumed to perform the execution. 


In this section, we will look at those tools and how to use them. 


## General considerations [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#general-considerations)


To understand query performance, let’s look at what happens in ClickHouse when a query is executed. 


The following part is deliberately simplified and takes some shortcuts; the idea here is not to drown you with details but to get you up to speed with the basic concepts. For more information you can consult the [query analyzer documentation](https://clickhouse.com/docs/en/guides/developer/understanding-query-execution-with-the-analyzer). 


From a very high\-level standpoint, when ClickHouse executes a query, the following happens: 


- **Query parsing and analysis**


The query is parsed and analyzed, and a generic query execution plan is created. 


- **Query optimization**


The query execution plan is optimized, unnecessary data is pruned, and a query pipeline is built from the query plan. 


- **Query pipeline execution**


The data is read and processed in parallel. This is the stage where ClickHouse actually executes the query operations such as filtering, aggregations, and sorting. 


- **Final processing**


The results are merged, sorted, and formatted into a final result before being sent to the client.


In reality, many [optimizations](https://clickhouse.com/docs/en/concepts/why-clickhouse-is-so-fast) are taking place, and we will discuss them a bit more in this guide, but for now, those main concepts give us a good understanding of what is happening behind the scenes when ClickHouse executes a query. 


With this high\-level understanding, let’s examine the tooling ClickHouse provides and how we can use it to track the metrics that affect query performance. 


## Demo environment [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#demo-environment)


As discussed in the introduction, we recently deployed the [ClickHouse Playground](https://sql.clickhouse.com/) demo environment for anyone to play with different datasets using ClickHouse. This environment runs on ClickHouse Cloud and is used by hundreds of users.


![clickhouse-playground.png](/uploads/clickhouse_playground_0600aa3c0e.png)
I’ll use this environment to illustrate my approach to optimizing query performance. 


### Dataset [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#dataset)


One of the datasets available on the ClickHouse Playground is the NYC Taxi dataset, which contains taxi ride data in NYC. We have ingested the NYC taxi dataset with no optimization.


Below is the command to create the table and insert data from an S3 bucket. Note that we infer the schema from the data voluntarily.



```
  
```
1-- Create table with inferred schema
2CREATE TABLE trips_small_inferred
3ORDER BY () EMPTY
4AS SELECT * FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/clickhouse-academy/nyc_taxi_2009-2010.parquet');
5
6-- Insert data into table with inferred schema
7INSERT INTO trips_small_inferred
8SELECT * 
9FROM s3Cluster
10('default','https://datasets-documentation.s3.eu-west-3.amazonaws.com/nyc-taxi/clickhouse-academy/nyc_taxi_2009-2010.parquet');
```


```

Let's have a look to the table schema automatically infered from the data.



```
  
```
1--- Display inferred table schema
2SHOW CREATE TABLE trips_small_inferred
3
4Query id: d97361fd-c050-478e-b831-369469f0784d
5
6CREATE TABLE nyc_taxi.trips_small_inferred
7(
8    `vendor_id` Nullable(String),
9    `pickup_datetime` Nullable(DateTime64(6, 'UTC')),
10    `dropoff_datetime` Nullable(DateTime64(6, 'UTC')),
11    `passenger_count` Nullable(Int64),
12    `trip_distance` Nullable(Float64),
13    `ratecode_id` Nullable(String),
14    `pickup_location_id` Nullable(String),
15    `dropoff_location_id` Nullable(String),
16    `payment_type` Nullable(Int64),
17    `fare_amount` Nullable(Float64),
18    `extra` Nullable(Float64),
19    `mta_tax` Nullable(Float64),
20    `tip_amount` Nullable(Float64),
21    `tolls_amount` Nullable(Float64),
22    `total_amount` Nullable(Float64)
23)
24ORDER BY tuple()
```


```

## Spot the slow queries [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#spot-the-slow-queries)


### Query logs [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#query-logs)


By default, ClickHouse collects and logs information about each executed query in the [query logs](https://clickhouse.com/docs/en/operations/system-tables/query_log). This data is stored in the table `system.query_log`. 



> The queries presented in this section have been executed on ClickHouse Cloud. The FROM section uses clusterAllReplicas(default, system.query\_log) as the query\_log table is distributed on multiple nodes in ClickHouse Cloud. Running locally, you can replace it with `FROM system.query_log`.


For each executed query, ClickHouse logs statistics such as query execution time, number of rows read, and resource usage, such as CPU, memory usage, or filesystem cache hits. 


Therefore, the query log is a good place to start when investigating slow queries. You can easily spot the queries that take a long time to execute and display the resource usage information for each one. 


Let’s find the top five long\-running queries on our NYC taxi dataset.



```
 
```
1-- Find top 5 long running queries from nyc_taxi database in the last 1 hour
2SELECT
3    type,
4    event_time,
5    query_duration_ms,
6    query,
7    read_rows,
8    tables
9FROM clusterAllReplicas(default, system.query_log)
10WHERE has(databases, 'nyc_taxi') AND (event_time >= (now() - toIntervalMinute(60))) AND type='QueryFinish'
11ORDER BY query_duration_ms DESC
12LIMIT 5
13FORMAT VERTICAL
14
15Query id: e3d48c9f-32bb-49a4-8303-080f59ed1835
16
17Row 1:
18──────
19type:              QueryFinish
20event_time:        2024-11-27 11:12:36
21query_duration_ms: 2967
22query:             WITH
23  dateDiff('s', pickup_datetime, dropoff_datetime) as trip_time,
24  trip_distance / trip_time * 3600 AS speed_mph
25SELECT
26  quantiles(0.5, 0.75, 0.9, 0.99)(trip_distance)
27FROM
28  nyc_taxi.trips_small_inferred
29WHERE
30  speed_mph > 30
31FORMAT JSON
32read_rows:         329044175
33tables:            ['nyc_taxi.trips_small_inferred']
34
35Row 2:
36──────
37type:              QueryFinish
38event_time:        2024-11-27 11:11:33
39query_duration_ms: 2026
40query:             SELECT 
41    payment_type,
42    COUNT() AS trip_count,
43    formatReadableQuantity(SUM(trip_distance)) AS total_distance,
44    AVG(total_amount) AS total_amount_avg,
45    AVG(tip_amount) AS tip_amount_avg
46FROM 
47    nyc_taxi.trips_small_inferred
48WHERE 
49    pickup_datetime >= '2009-01-01' AND pickup_datetime < '2009-04-01'
50GROUP BY 
51    payment_type
52ORDER BY 
53    trip_count DESC;
54
55read_rows:         329044175
56tables:            ['nyc_taxi.trips_small_inferred']
57
58Row 3:
59──────
60type:              QueryFinish
61event_time:        2024-11-27 11:12:17
62query_duration_ms: 1860
63query:             SELECT
64  avg(dateDiff('s', pickup_datetime, dropoff_datetime))
65FROM nyc_taxi.trips_small_inferred
66WHERE passenger_count = 1 or passenger_count = 2
67FORMAT JSON
68read_rows:         329044175
69tables:            ['nyc_taxi.trips_small_inferred']
70
71Row 4:
72──────
73type:              QueryFinish
74event_time:        2024-11-27 11:12:31
75query_duration_ms: 690
76query:             SELECT avg(total_amount) FROM nyc_taxi.trips_small_inferred WHERE trip_distance > 5
77FORMAT JSON
78read_rows:         329044175
79tables:            ['nyc_taxi.trips_small_inferred']
80
81Row 5:
82──────
83type:              QueryFinish
84event_time:        2024-11-27 11:12:44
85query_duration_ms: 634
86query:             SELECT
87vendor_id,
88avg(total_amount),
89avg(trip_distance),
90FROM
91nyc_taxi.trips_small_inferred
92GROUP BY vendor_id
93ORDER BY 1 DESC
94FORMAT JSON
95read_rows:         329044175
96tables:            ['nyc_taxi.trips_small_inferred']
```


```

The field `query_duration_ms` indicates how long it took for that particular query to execute. Looking at the results from the query logs, we can see that the first query is taking 2967ms to run, which could be improved. 


You might also want to know which queries are stressing the system by examining the query that consumes the most memory or CPU. 



```
 
```
1-- Top queries by memory usage 
2SELECT
3    type,
4    event_time,
5    query_id,
6    formatReadableSize(memory_usage) AS memory,
7    ProfileEvents.Values[indexOf(ProfileEvents.Names, 'UserTimeMicroseconds')] AS userCPU,
8    ProfileEvents.Values[indexOf(ProfileEvents.Names, 'SystemTimeMicroseconds')] AS systemCPU,
9    (ProfileEvents['CachedReadBufferReadFromCacheMicroseconds']) / 1000000 AS FromCacheSeconds,
10    (ProfileEvents['CachedReadBufferReadFromSourceMicroseconds']) / 1000000 AS FromSourceSeconds,
11    normalized_query_hash
12FROM clusterAllReplicas(default, system.query_log)
13WHERE has(databases, 'nyc_taxi') AND (type='QueryFinish') AND ((event_time >= (now() - toIntervalDay(2))) AND (event_time <= now())) AND (user NOT ILIKE '%internal%')
14ORDER BY memory_usage DESC
15LIMIT 30
```


```

Let’s isolate the long\-running queries we found and rerun them a few times to understand the response time. 


At this point, it is essential to turn off the filesystem cache by setting the `enable_filesystem_cache` setting to 0 to improve reproducibility.



```
 
```
1-- Disable filesystem cache
2set enable_filesystem_cache = 0;
3
4-- Run query 1
5WITH
6  dateDiff('s', pickup_datetime, dropoff_datetime) as trip_time,
7  trip_distance / trip_time * 3600 AS speed_mph
8SELECT
9  quantiles(0.5, 0.75, 0.9, 0.99)(trip_distance)
10FROM
11  nyc_taxi.trips_small_inferred
12WHERE
13  speed_mph > 30
14FORMAT JSON
15
16----
171 row in set. Elapsed: 1.699 sec. Processed 329.04 million rows, 8.88 GB (193.72 million rows/s., 5.23 GB/s.)
18Peak memory usage: 440.24 MiB.
19
20-- Run query 2
21SELECT 
22    payment_type,
23    COUNT() AS trip_count,
24    formatReadableQuantity(SUM(trip_distance)) AS total_distance,
25    AVG(total_amount) AS total_amount_avg,
26    AVG(tip_amount) AS tip_amount_avg
27FROM 
28    nyc_taxi.trips_small_inferred
29WHERE 
30    pickup_datetime >= '2009-01-01' AND pickup_datetime < '2009-04-01'
31GROUP BY 
32    payment_type
33ORDER BY 
34    trip_count DESC;
35
36--- 
374 rows in set. Elapsed: 1.419 sec. Processed 329.04 million rows, 5.72 GB (231.86 million rows/s., 4.03 GB/s.)
38Peak memory usage: 546.75 MiB.
39
40-- Run query 3
41SELECT
42  avg(dateDiff('s', pickup_datetime, dropoff_datetime))
43FROM nyc_taxi.trips_small_inferred
44WHERE passenger_count = 1 or passenger_count = 2
45FORMAT JSON
46
47---
481 row in set. Elapsed: 1.414 sec. Processed 329.04 million rows, 8.88 GB (232.63 million rows/s., 6.28 GB/s.)
49Peak memory usage: 451.53 MiB.
```


```

Summarize in the table for easy reading.




| Name | Elapsed | Rows processed | Peak memory |
| --- | --- | --- | --- |
| Query 1 | 1\.699 sec | 329\.04 million | 440\.24 MiB |
| Query 2 | 1\.419 sec | 329\.04 million | 546\.75 MiB |
| Query 3 | 1\.414 sec | 329\.04 million | 451\.53 MiB |


Let's understand a bit better what the queries achieve. 


- Query 1 calculates the distance distribution in rides with an average speed of over 30 miles per hour.
- Query 2 finds the number and average cost of rides per week.
- Query 3 calculates the average time of each trip in the dataset.


None of these queries are doing very complex processing, except the first query that calculates the trip time on the fly every time the query executes. However, each of these queries takes more than one second to execute, which, in the ClickHouse world, is a very long time. We can also note the memory usage of these queries; more or less 400 Mb for each query is quite a lot of memory. Also, each query appears to read the same number of rows (i.e., 329\.04 million). Let's quickly confirm how many rows are in this table.



```
 
```
1-- Count number of rows in table 
2SELECT count()
3FROM nyc_taxi.trips_small_inferred
4
5Query id: 733372c5-deaf-4719-94e3-261540933b23
6
7   ┌───count()─┐
81. │ 329044175 │ -- 329.04 million
9   └───────────┘
```


```

The table contains 329\.04 million rows, therefore each query is doing a full scan of the table.


*Alternatively, ClickHouse Cloud also provides a rich UI called Query insight to display the query log through various visualizations and tables.*


![cloud-query-insight.png](/uploads/cloud_query_insight_65ba345736.png)
### Explain statement [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#explain-statement)


Now that we have some long\-running queries, let's understand how they are executed. For this, ClickHouse supports the [EXPLAIN statement command](https://clickhouse.com/docs/en/sql-reference/statements/explain). It is a very useful tool that provides a very detailed view of all the query execution stages without actually running the query. While it can be overwhelming to look at for a non\-ClickHouse expert, it remains an essential tool for gaining insight into how your query is executed.


The documentation provides a detailed [guide](https://clickhouse.com/docs/en/guides/developer/understanding-query-execution-with-the-analyzer) on what the EXPLAIN statement is and how to use it to analyze your query execution. Rather than repeating what is in this guide, let's focus on a few commands that will help us find bottlenecks in query execution performance. 


**Explain indexes \= 1**


Let's start with EXPLAIN indexes \= 1 to inspect the query plan. The query plan is a tree showing how the query will be executed. There, you can see in which order the clauses from the query will be executed. The query plan returned by the EXPLAIN statement can be read from bottom to top.


Let's try using the first of our long\-running queries.



```
 
```
1EXPLAIN indexes = 1
2WITH
3    dateDiff('s', pickup_datetime, dropoff_datetime) AS trip_time,
4    (trip_distance / trip_time) * 3600 AS speed_mph
5SELECT quantiles(0.5, 0.75, 0.9, 0.99)(trip_distance)
6FROM nyc_taxi.trips_small_inferred
7WHERE speed_mph > 30
8
9Query id: f35c412a-edda-4089-914b-fa1622d69868
10
11   ┌─explain─────────────────────────────────────────────┐
121. │ Expression ((Projection + Before ORDER BY))         │
132. │   Aggregating                                       │
143. │     Expression (Before GROUP BY)                    │
154. │       Filter (WHERE)                                │
165. │         ReadFromMergeTree (nyc_taxi.trips_small_inferred) │
17   └─────────────────────────────────────────────────────┘
```


```

The output is straightforward. The query begins by reading data from the `nyc_taxi.trips_small_inferred` table. Then, the WHERE clause is applied to filter rows based on computed values. The filtered data is prepared for aggregation, and the quantiles are computed. Finally, the result is sorted and outputted. 


Here, we can note that no primary keys are used, which makes sense as we didn't define any when we created the table. As a result, ClickHouse is doing a full scan of the table for the query. 


**Explain Pipeline**


EXPLAIN Pipeline shows the concrete execution strategy for the query. There, you can see how ClickHouse actually executed the generic query plan we looked at previously.



```
 
```
1EXPLAIN PIPELINE
2WITH
3    dateDiff('s', pickup_datetime, dropoff_datetime) AS trip_time,
4    (trip_distance / trip_time) * 3600 AS speed_mph
5SELECT quantiles(0.5, 0.75, 0.9, 0.99)(trip_distance)
6FROM nyc_taxi.trips_small_inferred
7WHERE speed_mph > 30
8
9Query id: c7e11e7b-d970-4e35-936c-ecfc24e3b879
10
11    ┌─explain─────────────────────────────────────────────────────────────────────────────┐
12 1. │ (Expression)                                                                        │
13 2. │ ExpressionTransform × 59                                                            │
14 3. │   (Aggregating)                                                                     │
15 4. │   Resize 59 → 59                                                                    │
16 5. │     AggregatingTransform × 59                                                       │
17 6. │       StrictResize 59 → 59                                                          │
18 7. │         (Expression)                                                                │
19 8. │         ExpressionTransform × 59                                                    │
20 9. │           (Filter)                                                                  │
2110. │           FilterTransform × 59                                                      │
2211. │             (ReadFromMergeTree)                                                     │
2312. │             MergeTreeSelect(pool: PrefetchedReadPool, algorithm: Thread) × 59 0 → 1 │
```


```

Here, we can note the number of threads used to execute the query: 59 threads, which indicates a high parallelization. This speeds up the query, which would take longer to execute on a smaller machine. The number of threads running in parallel can explain the high volume of memory the query uses. 


Ideally, you would investigate all your slow queries the same way to identify unnecessary complex query plans and understand the number of rows read by each query and the resources consumed.


## Methodology [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#methodology)


It can be difficult to identify problematic queries on a production deployment, as there are probably a large number of queries being executed at any given time on your ClickHouse deployment. 


If you know which user, database, or tables are having issues, you can use the fields `user`, `tables`, or `databases` from the `system.query_logs` to narrow down the search. 


Once you identify the queries you want to optimize, you can start working on them to optimize. One common mistake developers make at this stage is changing multiple things simultaneously, running ad\-hoc experiments, and usually ending up with mixed results, but, more importantly, missing a good understanding of what made the query faster. 


Query optimization requires structure. I’m not talking about advanced benchmarking, but having a simple process in place to understand how your changes affect query performance can go a long way. 


Start by identifying your slow queries from query logs, then investigate potential improvements in isolation. When testing the query, make sure you disable the filesystem cache. 



> ClickHouse leverages [caching](https://clickhouse.com/docs/en/operations/caches) to speed up query performance at different stages. This is good for query performance, but during troubleshooting, it could hide potential I/O bottlenecks or poor table schema. For this reason, I suggest turning off the filesystem cache.


Once you have identified potential optimizations, it is recommended that you implement them one by one to better track how they affect performance. Below is a diagram describing the general approach.


![diagram-query-optimization-1.png](/uploads/diagram_query_optimization_1_328894ecdf.png)
*Finally, be cautious of outliers; it’s pretty common that a query might run slowly, either because a user tried an ad\-hoc expensive query or the system was under stress for another reason. You can group by the field normalized\_query\_hash to identify expensive queries that are being executed regularly. Those are probably the ones you want to investigate.*


## Basic optimization [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#basic-optimization)


Now that we have our framework to test, we can start optimizing.


The best place to start is to look at how the data is stored. As for any database, the less data we read, the faster the query will be executed. 


Depending on how you ingested your data, you might have leveraged ClickHouse [capabilities](https://clickhouse.com/docs/en/interfaces/schema-inference) to infer the table schema based on the ingested data. While this is very practical to get started, if you want to optimize your query performance, you’ll need to review the data schema to best fit your use case.


### Nullable [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#nullable)


As described in the [best practices documentation](https://clickhouse.com/docs/en/cloud/bestpractices/avoid-nullable-columns), avoid nullable columns wherever possible. It is tempting to use them often, as they make the data ingestion mechanism more flexible, but they negatively affect performance as an additional column has to be processed every time.


Running an SQL query that counts the rows with a NULL value can easily reveal the columns in your tables that actually need a Nullable value.



```
 
```
1-- Find non-null values columns 
2SELECT
3    countIf(vendor_id IS NULL) AS vendor_id_nulls,
4    countIf(pickup_datetime IS NULL) AS pickup_datetime_nulls,
5    countIf(dropoff_datetime IS NULL) AS dropoff_datetime_nulls,
6    countIf(passenger_count IS NULL) AS passenger_count_nulls,
7    countIf(trip_distance IS NULL) AS trip_distance_nulls,
8    countIf(fare_amount IS NULL) AS fare_amount_nulls,
9    countIf(mta_tax IS NULL) AS mta_tax_nulls,
10    countIf(tip_amount IS NULL) AS tip_amount_nulls,
11    countIf(tolls_amount IS NULL) AS tolls_amount_nulls,
12    countIf(total_amount IS NULL) AS total_amount_nulls,
13    countIf(payment_type IS NULL) AS payment_type_nulls,
14    countIf(pickup_location_id IS NULL) AS pickup_location_id_nulls,
15    countIf(dropoff_location_id IS NULL) AS dropoff_location_id_nulls
16FROM trips_small_inferred
17FORMAT VERTICAL
18
19Query id: 4a70fc5b-2501-41c8-813c-45ce241d85ae
20
21Row 1:
22──────
23vendor_id_nulls:           0
24pickup_datetime_nulls:     0
25dropoff_datetime_nulls:    0
26passenger_count_nulls:     0
27trip_distance_nulls:       0
28fare_amount_nulls:         0
29mta_tax_nulls:             137946731
30tip_amount_nulls:          0
31tolls_amount_nulls:        0
32total_amount_nulls:        0
33payment_type_nulls:        69305
34pickup_location_id_nulls:  0
35dropoff_location_id_nulls: 0
```


```

We have only two columns with null values: `mta_tax` and `payment_type`. The rest of the fields should not be using a `Nullable` column.


### Low cardinality [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#low-cardinality)


An easy optimization to apply to Strings is to make best use of the LowCardinality data type. As described in the low cardinality [documentation](https://clickhouse.com/docs/en/sql-reference/data-types/lowcardinality), ClickHouse applies dictionary coding to LowCardinality\-columns, which significantly increases query performance. 


An easy rule of thumb for determining which columns are good candidates for LowCardinality is that any column with less than 10,000 unique values is a perfect candidate.


You can use the following SQL query to find columns with a low number of unique values.



```
 
```
1-- Identify low cardinality columns
2SELECT
3    uniq(ratecode_id),
4    uniq(pickup_location_id),
5    uniq(dropoff_location_id),
6    uniq(vendor_id)
7FROM trips_small_inferred
8FORMAT VERTICAL
9
10Query id: d502c6a1-c9bc-4415-9d86-5de74dd6d932
11
12Row 1:
13──────
14uniq(ratecode_id):         6
15uniq(pickup_location_id):  260
16uniq(dropoff_location_id): 260
17uniq(vendor_id):           3
```


```

With a low cardinality, those four columns, `ratecode_id`, `pickup_location_id`, `dropoff_location_id`, and `vendor_id`, are good candidates for the LowCardinality field type.


### Optimize data type [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#optimize-data-type)


Clickhouse supports a large number of data types. Make sure to pick the smallest possible data type that fits your use case to optimize performance and reduce your data storage space on disk. 


For numbers, you can check the min/max value in your dataset to check if the current precision value matches the reality of your dataset. 



```
 
```
1-- Find min/max values for the payment_type field
2SELECT
3    min(payment_type),max(payment_type),
4    min(passenger_count), max(passenger_count)
5FROM trips_small_inferred
6
7Query id: 4306a8e1-2a9c-4b06-97b4-4d902d2233eb
8
9   ┌─min(payment_type)─┬─max(payment_type)─┐
101. │                 1 │                 4 │
11   └───────────────────┴───────────────────┘
```


```

For dates, you should pick a precision that matches your dataset and is best suited to answering the queries you’re planning to run.


### Apply the optimizations [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#apply-the-optimizations)


Let’s create a new table to use the optimized schema and re\-ingest the data.



```
 
```
1-- Create table with optimized data 
2CREATE TABLE trips_small_no_pk
3(
4    `vendor_id` LowCardinality(String),
5    `pickup_datetime` DateTime,
6    `dropoff_datetime` DateTime,
7    `passenger_count` UInt8,
8    `trip_distance` Float32,
9    `ratecode_id` LowCardinality(String),
10    `pickup_location_id` LowCardinality(String),
11    `dropoff_location_id` LowCardinality(String),
12    `payment_type` Nullable(UInt8),
13    `fare_amount` Decimal32(2),
14    `extra` Decimal32(2),
15    `mta_tax` Nullable(Decimal32(2)),
16    `tip_amount` Decimal32(2),
17    `tolls_amount` Decimal32(2),
18    `total_amount` Decimal32(2)
19)
20ORDER BY tuple();
21
22-- Insert the data 
23INSERT INTO trips_small_no_pk SELECT * FROM trips_small_inferred
```


```

We run the queries again using the new table to check for improvement. 




| Name | Run 1 \- Elapsed | Elapsed | Rows processed | Peak memory |
| --- | --- | --- | --- | --- |
| Query 1 | 1\.699 sec | 1\.353 sec | 329\.04 million | 337\.12 MiB |
| Query 2 | 1\.419 sec | 1\.171 sec | 329\.04 million | 531\.09 MiB |
| Query 3 | 1\.414 sec | 1\.188 sec | 329\.04 million | 265\.05 MiB |


We notice some improvements in both query time and memory usage. Thanks to the optimization in the data schema, we reduce the total volume of data that represents our data, leading to improved memory consumption and reduced processing time. 


Let's check the size of the tables to see the difference. 



```
 
```
1SELECT
2    `table`,
3    formatReadableSize(sum(data_compressed_bytes) AS size) AS compressed,
4    formatReadableSize(sum(data_uncompressed_bytes) AS usize) AS uncompressed,
5    sum(rows) AS rows
6FROM system.parts
7WHERE (active = 1) AND ((`table` = 'trips_small_no_pk') OR (`table` = 'trips_small_inferred'))
8GROUP BY
9    database,
10    `table`
11ORDER BY size DESC
12
13Query id: 72b5eb1c-ff33-4fdb-9d29-dd076ac6f532
14
15   ┌─table────────────────┬─compressed─┬─uncompressed─┬──────rows─┐
161. │ trips_small_inferred │ 7.38 GiB   │ 37.41 GiB    │ 329044175 │
172. │ trips_small_no_pk    │ 4.89 GiB   │ 15.31 GiB    │ 329044175 │
18   └──────────────────────┴────────────┴──────────────┴───────────┘
```


```

The new table is considerably smaller than the previous one. We see a reduction of about 34% in disk space for the table (7\.38 GiB vs 4\.89 GiB).


## The importance of primary keys [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#the-importance-of-primary-keys)


Primary keys in ClickHouse work differently than in most traditional database systems. In those systems, primary keys enforce uniqueness and data integrity. Any attempt to insert duplicate primary key values is rejected, and a B\-tree or hash\-based index is usually created for fast lookup. 


In ClickHouse, the primary key's [objective](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#a-table-with-a-primary-key) is different; it does not enforce uniqueness or help with data integrity. Instead, it is designed to optimize query performance. The primary key defines the order in which the data is stored on disk and is implemented as a sparse index that stores pointers to the first row of each granule.



> Granules in ClickHouse are the smallest units of data read during query execution. They contain up to a fixed number of rows, determined by index\_granularity, with a default value of 8192 rows. Granules are stored contiguously and sorted by the primary key.


Selecting a good set of primary keys is important for performance, and it's actually common to store the same data in different tables and use different sets of primary keys to speed up a specific set of queries. 


Other options supported by ClickHouse, such as Projection or Materialized view, allow you to use a different set of primary keys on the same data. The second part of this blog series will cover this in more detail. 


### Choose primary keys [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#choose-primary-keys)


Choosing the correct set of primary keys is a complex topic, and it might require trade\-offs and experiments to find the best combination. 


For now, we're going to follow these simple practices: 


- Use fields that are used to filter in most queries
- Choose columns with lower cardinality first
- Consider a time\-based component in your primary key, as filtering by time on a timestamp dataset is pretty common.


In our case, we will experiment with the following primary keys: `passenger_count`, `pickup_datetime`, and `dropoff_datetime`. 


The cardinality for passenger\_count is small (24 unique values) and used in our slow queries. We also add timestamp fields (`pickup_datetime` and `dropoff_datetime`) as they can be filtered often.


Create a new table with the primary keys and re\-ingest the data.



```
 
```
1CREATE TABLE trips_small_pk
2(
3    `vendor_id` UInt8,
4    `pickup_datetime` DateTime,
5    `dropoff_datetime` DateTime,
6    `passenger_count` UInt8,
7    `trip_distance` Float32,
8    `ratecode_id` LowCardinality(String),
9    `pickup_location_id` UInt16,
10    `dropoff_location_id` UInt16,
11    `payment_type` Nullable(UInt8),
12    `fare_amount` Decimal32(2),
13    `extra` Decimal32(2),
14    `mta_tax` Nullable(Decimal32(2)),
15    `tip_amount` Decimal32(2),
16    `tolls_amount` Decimal32(2),
17    `total_amount` Decimal32(2)
18)
19PRIMARY KEY (passenger_count, pickup_datetime, dropoff_datetime);
20
21-- Insert the data 
22INSERT INTO trips_small_pk SELECT * FROM trips_small_inferred
```


```

We then rerun our queries. We compile the results from the three experiments to see the improvements in elapsed time, rows processed, and memory consumption. 




| Query 1 | | | |
| --- | --- | --- | --- |
|  | Run 1 | Run 2 | Run 3 |
| Elapsed | 1\.699 sec | 1\.353 sec | 0\.765 sec |
| Rows processed | 329\.04 million | 329\.04 million | 329\.04 million |
| Peak memory | 440\.24 MiB | 337\.12 MiB | 444\.19 MiB |




| Query 2 | | | |
| --- | --- | --- | --- |
|  | Run 1 | Run 2 | Run 3 |
| Elapsed | 1\.419 sec | 1\.171 sec | 0\.248 sec |
| Rows processed | 329\.04 million | 329\.04 million | 41\.46 million |
| Peak memory | 546\.75 MiB | 531\.09 MiB | 173\.50 MiB |




| Query 3 | | | |
| --- | --- | --- | --- |
|  | Run 1 | Run 2 | Run 3 |
| Elapsed | 1\.414 sec | 1\.188 sec | 0\.431 sec |
| Rows processed | 329\.04 million | 329\.04 million | 276\.99 million |
| Peak memory | 451\.53 MiB | 265\.05 MiB | 197\.38 MiB |


We can see significant improvement across the board in execution time and memory used. 


Query 2 benefits most from the primary key. Let’s have a look at how the query plan generated is different from before.



```
 
```
1EXPLAIN indexes = 1
2SELECT
3    payment_type,
4    COUNT() AS trip_count,
5    formatReadableQuantity(SUM(trip_distance)) AS total_distance,
6    AVG(total_amount) AS total_amount_avg,
7    AVG(tip_amount) AS tip_amount_avg
8FROM nyc_taxi.trips_small_pk
9WHERE (pickup_datetime >= '2009-01-01') AND (pickup_datetime < '2009-04-01')
10GROUP BY payment_type
11ORDER BY trip_count DESC
12
13Query id: 30116a77-ba86-4e9f-a9a2-a01670ad2e15
14
15    ┌─explain──────────────────────────────────────────────────────────────────────────────────────────────────────────┐
16 1. │ Expression ((Projection + Before ORDER BY [lifted up part]))                                                     │
17 2. │   Sorting (Sorting for ORDER BY)                                                                                 │
18 3. │     Expression (Before ORDER BY)                                                                                 │
19 4. │       Aggregating                                                                                                │
20 5. │         Expression (Before GROUP BY)                                                                             │
21 6. │           Expression                                                                                             │
22 7. │             ReadFromMergeTree (nyc_taxi.trips_small_pk)                                                          │
23 8. │             Indexes:                                                                                             │
24 9. │               PrimaryKey                                                                                         │
2510. │                 Keys:                                                                                            │
2611. │                   pickup_datetime                                                                                │
2712. │                 Condition: and((pickup_datetime in (-Inf, 1238543999]), (pickup_datetime in [1230768000, +Inf))) │
2813. │                 Parts: 9/9                                                                                       │
2914. │                 Granules: 5061/40167                                                                             │
30    └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```

Thanks to the primary key, only a subset of the table granules has been selected. This alone greatly improves the query performance since ClickHouse has to process significantly less data.


## Conclusion  [\#](/blog/a-simple-guide-to-clickhouse-query-optimization-part-1#conclusion)


ClickHouse is a very performant analytical database and implements a ton of performance optimization to achieve that. However, to unlock the full power of ClickHouse performance, it is necessary to understand how the database works and how you can utilize it best. By leveraging what you learned in this blog, such as identifying your less performant queries and understanding how they can be optimized by applying basic but powerful changes to your data schema, you will see significant improvements in your query performance. 


It is a great place to start if you’re unfamiliar with ClickHouse. However, if you are an experienced ClickHouse user, some of the topics discussed in this blog post might not be news to you. In our next blog, we will cover more advanced topics such as projection, materialized views, and data skipping index. Stay tuned.

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
