# How ClickHouse became fast at joins


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# How ClickHouse became fast at joins

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jun 3, 2026 · 20 minutes read
> **TL;DR**  
> 
> Over two years, ClickHouse became **26× faster** on join\-heavy analytical workloads. This post explains the engineering that made joins a first\-class strength.


  

## Two years of focused join engineering [\#](/blog/clickhouse-fast-joins#two-years-of-focused-join-engineering)


ClickHouse is known for fast analytical queries, high compression, and real\-time performance at scale.


Over the last two years, one major engineering focus has been bringing that same performance profile to join\-heavy SQL queries.


At the [ClickHouse 24\.5 release webinar](https://www.youtube.com/live/dURnKjLuZLg?si=1Bx618RgGfAwN4iP&t=2216), Alexey Milovidov, inventor of ClickHouse, described the direction clearly:



> “From now on, you will see JOIN improvements in every ClickHouse release.”


The chart below shows what that looked like in practice.


![Blog-JOINS-improvements.001.png](/uploads/Blog_JOINS_improvements_001_be4d4145a8.png)
The first year laid the foundation: faster parallel hash join, smarter planning, aggressive filter pushdown, and local join reordering.



> By 25\.4, the same [TPC\-H](https://clickhouse.com/docs/getting-started/example-datasets/tpch) SF100 join\-heavy workload was already **4\.4× faster** than in 22\.4\.


The second year pushed much further. Between 25\.4 and 26\.4, a new wave of optimizer and execution improvements made the same workload another 6× faster with default settings.



> End to end, ClickHouse is now **26× faster** on TPC\-H SF100 than it was in 22\.4\.


This post explains how we got there. The [companion post](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift) shows what it unlocked: **ClickHouse Cloud now runs TPC\-H for less than a cent**, and competes head\-to\-head with Snowflake, Databricks, BigQuery, and Redshift on SF100\.


## Year one: building the foundation [\#](/blog/clickhouse-fast-joins#year-one-building-the-foundation)


A year ago, at [our first Open House user conference in San Francisco](https://clickhouse.com/blog/highlights-from-open-house-our-first-user-conference), ClickHouse join engineering lead, Robert Schulze, presented the first year of major join\-performance work.



  

That first year was about building the foundation. ClickHouse made parallel hash join the default in 24\.12, added local automatic join reordering for two\-table joins, and delivered a steady stream of low\-level execution improvements.


Several of those changes landed across consecutive releases:


- **24\.7:** [improved hash table allocation for faster parallel hash joins](https://clickhouse.com/blog/clickhouse-release-24-07#faster-parallel-hash-join)
- **24\.12:** made [parallel hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join) the default strategy and introduced [local automatic join reordering](https://clickhouse.com/blog/clickhouse-release-24-12#automatic-join-reordering)
- **25\.1:** [sped up the hash join probe phase](https://clickhouse.com/blog/clickhouse-release-25-01#faster-parallel-hash-join)
- **25\.2:** [removed thread contention in the hash join build phase](https://clickhouse.com/blog/clickhouse-release-25-02#faster-parallel-hash-join)


Together, those improvements made the same TPC\-H SF100 join\-heavy workload **4\.4× faster by 25\.4** compared with 22\.4\.


But year one was only the foundation. The second year is where joins became dramatically better with default settings.


## Year two: making joins competitive by default [\#](/blog/clickhouse-fast-joins#year-two-making-joins-competitive-by-default)


This year at Open House, Robert [is back](/uploads/image_cc8a4cd7f3.png) with the second chapter of the join\-performance story.


Year one built the foundation. Year two made joins competitive with default settings.


The goal was simple: users should not have to rewrite queries, tune join orders by hand, or know which internal optimization to enable. ClickHouse should recognize more join\-heavy SQL, automatically choose better plans, and avoid unnecessary work during execution.


The chart below shows the four main improvements that became effective by default between 25\.4 and 26\.4\. Together, they made the same TPC\-H SF100 join\-heavy workload another 6× faster.


![Blog-JOINS-improvements.002.png](/uploads/Blog_JOINS_improvements_002_0f8d32bb46.png)
The rest of this post walks through those four improvements:


① **Correlated subqueries in JOINs** — support more real\-world SQL directly.


② **Lazy column replication** — avoid copying repeated values produced by joins.


③ **Runtime filters** — skip probe\-side rows before expensive hash\-table lookups.


④ **Statistics\-based join reordering** — choose better join plans automatically.


All examples use [TPC\-H SF100](https://clickhouse.com/docs/getting-started/example-datasets/tpch) on the same hardware, an AWS EC2 m6i.8xlarge instance (32 vCPUs, 128 GiB RAM), so the improvements are easy to compare.


### ① Correlated  subqueries in JOINs [\#](/blog/clickhouse-fast-joins#-correlated-subqueries-in-joins)


Two years ago, the problem was not just that some joins were slower than we wanted them to be. Some important join\-heavy queries could not run at all.


#### Why this mattered [\#](/blog/clickhouse-fast-joins#why-this-mattered)


In the TPC\-H benchmark section of our [first research paper](https://www.vldb.org/pvldb/vol17/p3731-schulze.pdf), presented at VLDB 2024, we had to exclude seven queries: Q2, Q4, Q13, Q17, and Q20–Q22\. Because they used correlated subqueries, which ClickHouse did not fully support at the time.


#### A correlated TPC\-H query [\#](/blog/clickhouse-fast-joins#a-correlated-tpc-h-query)


TPC\-H Q4 is a good example. It contains an inner query over `lineitem` that references `orders`, the table from the outer query:


![Blog-JOINS-improvements.001.png](/uploads/Blog_JOINS_improvements_001_d351241bde.png)
This is what makes it a **correlated subquery**: the inner query cannot be understood in isolation, because it depends on values from the outer query.


#### From row\-by\-row execution to set\-oriented plans [\#](/blog/clickhouse-fast-joins#from-row-by-row-execution-to-set-oriented-plans)


Correlated subqueries are common because they are natural to write. They are also increasingly common in generated SQL, including queries produced by agentic systems. But for a database engine, they are hard to execute efficiently.


The naive plan is to evaluate the inner query once for every row from the outer query. That is simple, but often disastrous for performance. To make these queries fast, the optimizer has to decorrelate them: rewrite the query into an equivalent set\-oriented plan, typically using joins, aggregations, semi joins, or anti joins.


That rewrite must preserve SQL semantics around duplicates, aggregates, and NULLs, which makes it much harder than it looks.


#### Result [\#](/blog/clickhouse-fast-joins#result)



> Correlated subqueries are now first\-class SQL in ClickHouse. Queries that previously required manual rewrites \- including the excluded TPC\-H queries \- now run directly.


  

### ② Lazy column replication in JOINs [\#](/blog/clickhouse-fast-joins#-lazy-column-replication-in-joins)


Lazy column replication reduces CPU and memory usage when JOINs logically repeat the same values many times.


#### The problem: logical repetition becomes physical copying [\#](/blog/clickhouse-fast-joins#the-problem-logical-repetition-becomes-physical-copying)


In JOIN results, one input row can produce many output rows. In TPC\-H, for example, each customer can have multiple orders. When we join `orders` with `customer`, the customer columns are logically repeated once for every matching order.



```

```
SELECT
    o.o_orderkey,
    o.o_orderdate,
    c.c_name,
    c.c_address,
    c.c_comment
FROM orders AS o
INNER JOIN customer AS c
    ON o.o_custkey = c.c_custkey;
```


```

Logically, the result looks like this:


![Blog-JOINS-improvements.004.png](/uploads/Blog_JOINS_improvements_004_3a121d9e14.png)
Conceptually, this is the correct result: the same customer values appear next to each matching order.


The expensive part is physical replication. If ClickHouse copies wide values such as c\_address or c\_comment into every joined row, the join spends CPU cycles and memory bandwidth duplicating the same data again and again. And if later operators like aggregations discard most of those rows, much of that copying was unnecessary.


#### Lazy column replication avoids that eager copying. [\#](/blog/clickhouse-fast-joins#lazy-column-replication-avoids-that-eager-copying)


Instead of physically replicating repeated values during the join, ClickHouse keeps the original values once in a small dictionary data structure and represents the joined column as a compact index value pointing back to them:


![Blog-JOINS-improvements.005.png](/uploads/Blog_JOINS_improvements_005_5694c466bf.png)
If a later query step needs the fully materialized column, ClickHouse can still produce it. But many analytical operations can work directly on the compact representation, so the repeated values never need to be copied at all.


This is especially useful for JOINs that duplicate wide columns, such as strings.


#### Benchmark: avoiding physical replication [\#](/blog/clickhouse-fast-joins#benchmark-avoiding-physical-replication)


For the benchmark, we use a self\-join on `orders` to create many repeated `o_comment` values, and then immediately consume them with `cityHash64`.


First, we ran the following example join without lazy replication.



```

```
SELECT sum(cityHash64(t1.o_comment))
FROM orders AS t1
INNER JOIN orders AS t2
    ON t1.o_custkey = t2.o_custkey
SETTINGS
    enable_lazy_columns_replication = 0,
    allow_special_serialization_kinds_in_output_formats = 0;
```


```

Fastest of three runs:



```

```
1 row in set. Elapsed: 5.419 sec. Processed 300.00 million rows, 8.89 GB (55.36 million rows/s., 1.64 GB/s.)
Peak memory usage: 5.27 GiB.
```

```

Then, we ran the same query with lazy columns replication enabled.


This is the ideal case for lazy replication: `o_comment` is only needed as input to a function, so ClickHouse can evaluate `cityHash64` over the compact representation without physically materializing the repeated string column.



```

```
SELECT sum(cityHash64(t1.o_comment))
FROM orders AS t1
INNER JOIN orders AS t2
    ON t1.o_custkey = t2.o_custkey
SETTINGS
    enable_lazy_columns_replication = 1,
    allow_special_serialization_kinds_in_output_formats = 1;
```


```

Fastest of three runs:



```

```
1 row in set. Elapsed: 2.847 sec. Processed 300.00 million rows, 8.89 GB (105.36 million rows/s., 3.12 GB/s.)
Peak memory usage: 5.22 GiB.
```

```

#### Result [\#](/blog/clickhouse-fast-joins#result-1)



> Result: Lazy column replication made this join **1\.9× faster**, reducing runtime from 5\.419s to 2\.847s, while slightly lowering peak memory usage from 5\.27 GiB to 5\.22 GiB.


The speedup comes from evaluating `cityHash64` directly over the compact replicated\-column representation rather than physically copying repeated strings.


### ③ Runtime filters in JOINs [\#](/blog/clickhouse-fast-joins#-runtimefilters-in-joins)


Runtime filters reduce wasted probe\-side work in hash joins.


They generalize a technique already used by ClickHouse’s [full sorting merge join algorithm](https://clickhouse.com/blog/clickhouse-fully-supports-joins-full-sort-partial-merge-part3#full-sorting-merge-join), where joined tables can be [filtered by each other’s join keys](https://clickhouse.com/blog/clickhouse-fully-supports-joins-full-sort-partial-merge-part3#filtering-tables-by-each-others-join-key-values-before-joining) before the join itself runs. ClickHouse introduces a similar idea for the default parallel hash join algorithm.


As a reminder, the [parallel hash join algorithm](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join) is a variation of [hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#hash-join) that splits the input data to build several hash tables concurrently, speeding up the build phase.


In the example below, we set [max\_threads](https://clickhouse.com/docs/operations/settings/settings#max_threads) \= 2, so ClickHouse builds two hash tables in parallel. In practice, max\_threads is usually derived from the number of available CPU cores.


The diagram shows the physical query plan, called the query pipeline in ClickHouse, for a TPC\-H query joining orders with customer.


![Blog-JOINS-improvements.006.png](/uploads/Blog_JOINS_improvements_006_d7c0b8e7ae.png)
① The predicate on `customer` is pushed down and applied before the join.


② During the build phase, the filtered `customer` rows, the right side of the join, are split into two buckets because `max_threads = 2`. Each bucket is used to build one in\-memory hash table.


③ During the probe phase, `orders` rows, the left side of the join, are streamed in parallel and routed to the corresponding hash table for lookup.


#### The problem: wasted probe\-side work [\#](/blog/clickhouse-fast-joins#the-problem-wasted-probe-side-work)


Note that in step ②, only a subset of customer keys is inserted into the hash tables during the build phase. However, in step ③, ClickHouse still processes all orders rows. For orders whose customer was removed by the customer filter, the lookup can never succeed. Those rows still consume CPU and memory bandwidth before the join rejects them.


#### The idea: filter probe rows before lookup [\#](/blog/clickhouse-fast-joins#the-idea-filter-probe-rows-before-lookup)


Runtime filters address exactly this wasted work.


While ClickHouse builds the hash tables (in DRAM) from the filtered customer rows, it also creates a compact filter (bloom filter or min/max values) from the join keys that actually made it into the build side. In our example, that means only customer keys that survived c\_nation \= 'DE'.


That filter is applied to the orders side before the hash\-table lookup. If an orders row has an o\_custkey that is not present in the filtered build side, ClickHouse can discard it early instead of routing it into the join.


The runtime filter is much smaller than the hash tables themselves, so it can stay close to the CPU, typically in L1 or L2 cache.


#### How runtime filters fit into the query pipeline [\#](/blog/clickhouse-fast-joins#how-runtime-filters-fit-into-the-query-pipeline)


The updated pipeline looks like this:


![Blog-JOINS-improvements.007.png](/uploads/Blog_JOINS_improvements_007_1cf7d0baf0.png)
The updated pipeline adds two steps:


② While reading the filtered customer rows, ClickHouse builds a runtime filter from their join keys.


④ Before probing the hash tables, ClickHouse applies that runtime filter to the orders rows.


⑤ Only rows that pass the runtime filter continue to the hash\-table lookup.


The parallel hash join structure stays the same, but many probe\-side rows are removed before the expensive lookup.


This keeps the parallel hash join structure unchanged, but removes probe\-side rows that could never match. In selective joins, this can significantly reduce CPU work and memory bandwidth.


#### How it appears in the query plan [\#](/blog/clickhouse-fast-joins#how-it-appears-in-the-query-plan)


We can see this in the logical query plan with EXPLAIN plan.


First, with runtime pre\-filtering disabled:



```

```
EXPLAIN plan
SELECT *
FROM orders, customer
WHERE o_custkey = c_custkey
SETTINGS enable_join_runtime_filters = 0;
```


```


```

```
...                             
Join                                                       
...
ReadFromMergeTree (default.orders)                   
ReadFromMergeTree (default.customer)
```

```

We’ll skip the rest of the plan and focus on the core mechanics.


Reading the output from **bottom to top**, we can see that ClickHouse plans to read the data from the two tables, `orders` and `customer`, and perform the join.


Next, let’s inspect the logical query plan for the same join, but this time **with runtime pre\-filtering enabled**:



```

```
EXPLAIN plan
SELECT *
FROM orders, customer
WHERE o_custkey = c_custkey
SETTINGS enable_join_runtime_filters = 1;
```


```

The relevant parts of the plan look like this:



```

```
...
Join                                                                                                                                                                                             
...                                                                                                                                                                         
Prewhere filter column: __filterContains(_runtime_filter_14211390369232515712_0, __table1.o_custkey)                                                                          
...
BuildRuntimeFilter (Build runtime join filter on __table2.c_custkey (_runtime_filter_14211390369232515712_0))
...
```

```

Reading the plan from **bottom to top**, we can see that ClickHouse first ① builds a **runtime filter** from the join key values on the **right\-hand side** (`customer`) table.


This runtime filter is then ② applied as a **[PREWHERE](https://clickhouse.com/docs/optimize/prewhere) filter** on the **left\-hand side** (`orders`) table, allowing irrelevant rows to be skipped **before** the join is executed.


#### Benchmark: fewer rows, less memory [\#](/blog/clickhouse-fast-joins#benchmark-fewer-rows-less-memory)


To measure the effect, we use a slightly extended version of the query, joining orders, customer, and nation, and calculating the average order total for customers from France.


We’ll start with **runtime pre\-filtering disabled**:



```

```
SELECT avg(o_totalprice)
FROM orders, customer, nation
WHERE (c_custkey = o_custkey) AND (c_nationkey = n_nationkey) AND (n_name = 'FRANCE')
SETTINGS enable_join_runtime_filters = 0;
```


```


```

```
┌──avg(o_totalprice)─┐
│ 151149.41468432106 │
└────────────────────┘

1 row in set. Elapsed: 1.005 sec. Processed 165.00 million rows, 1.92 GB (164.25 million rows/s., 1.91 GB/s.)
Peak memory usage: 1.24 GiB.
```

```

Then, we run the same query again, this time **with runtime pre\-filtering enabled**:



```

```
SELECT avg(o_totalprice)
FROM orders, customer, nation
WHERE (c_custkey = o_custkey) AND (c_nationkey = n_nationkey) AND (n_name = 'FRANCE')
SETTINGS enable_join_runtime_filters = 1;
```


```


```

```
┌──avg(o_totalprice)─┐
│ 151149.41468432106 │
└────────────────────┘

1 row in set. Elapsed: 0.471 sec. Processed 165.00 million rows, 1.92 GB (350.64 million rows/s., 4.08 GB/s.)
Peak memory usage: 185.18 MiB.
```

```

#### Result [\#](/blog/clickhouse-fast-joins#result-2)



> Runtime pre\-filtering made this query **2\.1× faster**, reducing runtime from 1\.005s to 0\.471s, while cutting peak memory from 1\.24 GiB to 185 MiB.


By filtering rows early, ClickHouse avoids probe\-side work that cannot produce matches, reducing both CPU work and memory usage.


### ④ Statistics\-based join reordering [\#](/blog/clickhouse-fast-joins#-statistics-based-join-reordering)


ClickHouse can now reorder complex join graphs across dozens of tables and [all major join types](https://clickhouse.com/blog/clickhouse-fully-supports-joins-part1).


This matters because SQL joins are [associative](https://en.wikipedia.org/wiki/Associative_property): the same logical query can often be executed using many different join orders. The result is the same, but the runtime can be dramatically different.


#### The problem: join order matters [\#](/blog/clickhouse-fast-joins#the-problem-join-order-matters)


The diagram below shows three different join orders for the same join query and the resulting hash join trees. The query result will be the same in all three cases.


![Blog-JOINS-improvements.008.png](/uploads/Blog_JOINS_improvements_008_6eab572778.png)
The more tables a query joins, the more important the join order becomes.


As explained in the previous section, in a hash join, the right side is used to build an in\-memory hash table, and the left side probes it. Placing the smaller input on the build side is usually much more efficient.


In some cases, **good and bad join orders can differ by many orders of magnitude in runtime**!


#### Finding a good join order [\#](/blog/clickhouse-fast-joins#finding-a-good-join-order)


Finding a good join order is hard because the search space grows extremely quickly. With 12 joined tables, there are already **28 trillion** possible join orders.


ClickHouse therefore, uses a join order optimizer. At a high level, it enumerates candidate join trees, estimates their cost, and picks a good one.


![Blog-JOINS-improvements.009.png](/uploads/Blog_JOINS_improvements_009_b14a1bc01e.png)
#### Column statistics make the optimizer effective [\#](/blog/clickhouse-fast-joins#column-statistics-make-the-optimizer-effective)


The optimizer needs cardinality estimates: how many rows each intermediate join result is expected to contain after filters and join predicates.


Those estimates come from [column statistics](https://clickhouse.com/docs/engines/table-engines/mergetree-family/mergetree#available-types-of-column-statistics). Since 26\.4, ClickHouse generates those statistics automatically for all tables, which makes statistics\-based join reordering effective with default settings.


For small join graphs, ClickHouse can use exhaustive dynamic programming (DPSize) to find the optimal order. For larger join graphs, it uses a greedy search that is much faster but not guaranteed to find the optimum.


![Blog-JOINS-improvements.010.png](/uploads/Blog_JOINS_improvements_010_3fb770935a.png)
#### Benchmark: from one hour to 2\.7 seconds [\#](/blog/clickhouse-fast-joins#benchmark-from-one-hour-to-27-seconds)


To measure the impact, we ran the same six\-table TPC\-H query twice:


1. Without statistics: tables created with the [default DDL](https://clickhouse.com/docs/getting-started/example-datasets/tpch#data-generation-and-import).
2. With statistics: tables created with [extended DDL that enables column statistics](https://pastila.nl/?01031010/7475d7ba575a41d9fd86eaaff97cb201#SGYcmaof4DoQzewNH3tBKA==).


Both runs used the same query and the same join\-order optimizer settings.



```

```
SELECT
  n_name,
  sum(l_extendedprice * (1 - l_discount)) AS revenue
FROM
  customer, 
  orders, 
  lineitem, 
  supplier, 
  nation, 
  region
WHERE
c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND l_suppkey = s_suppkey
AND c_nationkey = s_nationkey
AND s_nationkey = n_nationkey
AND n_regionkey = r_regionkey
AND r_name = 'ASIA'
AND o_orderdate >= DATE '1994-01-01'
AND o_orderdate < DATE '1994-01-01' + INTERVAL '1' year
GROUP BY
  n_name
ORDER BY
  revenue DESC;
```


```

First, we executed the query on the tables **without statistics**:



```

```
USE tpch_no_stats;
SET query_plan_optimize_join_order_limit = 10;
SET allow_statistics_optimize = 1;
```

```


```

```
┌─n_name────┬─────────revenue─┐
│ VIETNAM   │  5310749966.867 │
│ INDIA     │ 5296094837.7503 │
│ JAPAN     │ 5282184528.8254 │
│ CHINA     │ 5270934901.5602 │
│ INDONESIA │ 5270340980.4608 │
└───────────┴─────────────────┘

5 rows in set. Elapsed: 3903.678 sec. Processed 766.04 million rows, 16.03 GB (196.23 thousand rows/s., 4.11 MB/s.)
Peak memory usage: 99.12 GiB.
```

```

That took over one hour! 🐌 And used 99 GiB of main memory.


Then we repeated the same query on the tables **with statistics**:



```

```
USE tpch_stats;
SET query_plan_optimize_join_order_limit = 10;
SET allow_statistics_optimize = 1;
```

```


```

```
┌─n_name────┬─────────revenue─┐
│ VIETNAM   │  5310749966.867 │
│ INDIA     │ 5296094837.7503 │
│ JAPAN     │ 5282184528.8254 │
│ CHINA     │ 5270934901.5602 │
│ INDONESIA │ 5270340980.4608 │
└───────────┴─────────────────┘

5 rows in set. Elapsed: 2.702 sec. Processed 638.85 million rows, 14.76 GB (236.44 million rows/s., 5.46 GB/s.)
Peak memory usage: 3.94 GiB.
```

```

#### Result [\#](/blog/clickhouse-fast-joins#result-3)



> With statistics\-based join reordering, the six\-table TPC\-H query dropped from 3903\.7s to 2\.7s \- about **1,450× faster** \- while peak memory fell from 99\.1 GiB to 3\.9 GiB.


  

## What this unlocked [\#](/blog/clickhouse-fast-joins#what-this-unlocked)


Two years ago, we decided to make joins a first\-class strength in ClickHouse.


The first year laid the foundation: faster parallel hash joins, smarter build/probe\-side choices, better planning, more aggressive filter pushdown, and local join reordering. By 25\.4, the same TPC\-H SF100 join\-heavy workload was already **4\.4× faster** than in 22\.4\.


The second year made joins dramatically better again. Between 25\.4 and 26\.4, another wave of optimizer and execution improvements made the same workload **another 6× faster** with default settings.


The four improvements we covered above each attacked a different part of the join problem:


**① Correlated subqueries** removed a major SQL compatibility gap. ClickHouse can now run correlated subqueries across `SELECT`, `WHERE`, and `HAVING`, including TPC\-H queries that previously required manual rewrites or had to be excluded entirely.


**② Lazy column replication** avoids physically copying repeated values produced by joins. In our TPC\-H example, it made the join **1\.9× faster**.


**③ Runtime filters** reduce wasted probe\-side work by filtering rows before they reach the hash\-table lookup. In our benchmark, runtime pre\-filtering made the query **2\.1× faster** and reduced peak memory by **nearly 7×**.


**④ Statistics\-based join reordering** lets ClickHouse choose better physical join plans automatically. In the six\-table TPC\-H query, the runtime dropped from **3903\.7 seconds to 2\.7 seconds** \- about **1,450× faster** \- while peak memory fell from **99\.1 GiB to 3\.9 GiB**.


Taken together, these changes moved joins from “something ClickHouse can do” to something ClickHouse can do **competitively, automatically, and with default settings**.


That is what made the [companion benchmark](/blog/tpc-h-clickhouse-cloud-vs-snowflake-databricks-bigquery-redshift) possible: ClickHouse Cloud can now run the full join\-heavy TPC\-H workload quickly and cost\-efficiently against Snowflake, Databricks, BigQuery, and Redshift, **for less than a cent**.


![Blog-JOINS-results.005.png](/uploads/Blog_JOINS_results_005_f2a4c0e257.png)
## What’s next [\#](/blog/clickhouse-fast-joins#whats-next)


ClickHouse has come a long way on joins.


Two years ago, the TPC\-H SF100 workload looked very different. After the first year of focused join engineering, it was already **4\.4× faster**. After the second year, it is now **26× faster than in 22\.4**, with the last year alone contributing another **6× speedup** under default settings.


That is the story this post covered: the first two years of making joins a first\-class strength in ClickHouse.


But we are just getting started. Year three is already underway, with [distributed joins](/blog/multi-stage-distributed-query-execution-clickhouse-cloud) as one of the next steps toward larger workloads such as TPC\-H SF1000 and beyond.


We’ll report back in a year.



> "When will you stop optimizing join performance? We will never stop!” – Alexey Milovidov, inventor of ClickHouse, [during the ClickHouse release 25\.10 webinar](https://www.youtube.com/live/cV2hiOCzDG4?si=hEjfRABUz6ZIfp-w&t=1866)

[Get started](https://clickhouse.cloud/signUp?loc=blog-cta-footer&utm_source=clickhouse&utm_medium=web&utm_campaign=blog) with ClickHouse Cloud today and receive $300 in credits. At the end of your 30\-day trial, continue with a pay\-as\-you\-go plan, or [contact us](/company/contact?loc=blog-cta-footer) to learn more about our volume\-based discounts. Visit our [pricing page](/pricing?loc=blog-cta-header) for details.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
