# ClickHouse Release 24\.12


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.12

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jan 9, 2025 · 17 minutes readAnother month goes by, which means it’s time for another release!


ClickHouse version 24\.12 contains **16** new features 🦃 **16** performance optimizations ⛸️ **36** bug fixes 🏕️


In this release, we have Enum usability improvements, Iceberg REST catalog and schema evolution support, reverse table ordering, the ability to use JSON subcolumns as a primary key, automatic JOIN reordering and more!


## New Contributors [\#](/blog/clickhouse-release-24-12#new-contributors)


As always, we send a special welcome to all the new contributors in 24\.12! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.


Below are the names of the new contributors:


*Emmanuel Dias, Xavier Leune, Zawa\_ll, Zaynulla, erickurbanov, jotosoares, zhangwanyun1, zwy991114, “JiaQi*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.12/).


## Enum usability improvements [\#](/blog/clickhouse-release-24-12#enum-usability-improvements)


### Contributed by ZhangLiStar [\#](/blog/clickhouse-release-24-12#contributed-by-zhanglistar)


This release also sees usability improvements when working with Enums. We’re going to explore them with help from the [Reddit comments dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/reddit-comments). We’ll create a table with just a couple of the columns:



```
    
```
1CREATE TABLE reddit
2    (
3        subreddit LowCardinality(String),
4        subreddit_type Enum(
5            'public' = 1, 'restricted' = 2, 'user' = 3, 
6            'archived' = 4, 'gold_restricted' = 5, 'private' = 6
7        ),
8    )
9    ENGINE = MergeTree
10    ORDER BY (subreddit);
```


```

We can insert the data like this:



```

```
1INSERT INTO reddit
2SELECT subreddit, subreddit_type
3FROM s3(        
4  'https://clickhouse-public-datasets.s3.eu-central-1.amazonaws.com/reddit/original/RC_2017-12.xz',
5  'JSONEachRow'
6);
```

```

Let’s say we want to count the number of posts by `subreddit_type` where the type contains the string `e`. We can write the following query using the `LIKE` operator:



```
    
```
1SELECT
2    subreddit_type,
3    count() AS c
4FROM reddit
5WHERE subreddit_type LIKE '%restricted%'
6GROUP BY ALL
7ORDER BY c DESC;
```

```

If we run this query before 24\.12, we’ll see an error message like this:



```
Received exception:
Code: 43. DB::Exception: Illegal type Enum8('public' = 1, 'restricted' = 2, 'user' = 3, 'archived' = 4, 'gold_restricted' = 5, 'private' = 6) of argument of function like: In scope SELECT subreddit, count() AS c FROM reddit WHERE subreddit_type LIKE '%e%' GROUP BY subreddit ORDER BY c DESC LIMIT 20. (ILLEGAL_TYPE_OF_ARGUMENT)

```

If we run it in 24\.12, we’ll get the following result:



```
   ┌─subreddit_type─┬──────c─┐
1. │ restricted     │ 698263 │
2. │ user           │  39640 │
   └────────────────┴────────┘

```

The equality and IN operators also now accept unknown values. For example, the following query returns any records that have a type of `Foo` or `public`:



```
SELECT count() AS c
FROM reddit
WHERE subreddit_type IN ('Foo', 'public')
GROUP BY ALL;

```

If we run this query before 24\.12, we’ll see an error message like this:



```
Received exception:
Code: 691. DB::Exception: Unknown element 'Foo' for enum: while converting 'Foo' to Enum8('public' = 1, 'restricted' = 2, 'user' = 3, 'archived' = 4, 'gold_restricted' = 5, 'private' = 6). (UNKNOWN_ELEMENT_OF_ENUM)


```

If we run it in 24\.12, we’ll get the following result:



```
   ┌────────c─┐
1. │ 85235907 │ -- 85.24 million
   └──────────┘

```

## Reverse table ordering [\#](/blog/clickhouse-release-24-12#reverse-table-ordering)


### Contributed by Amos Bird [\#](/blog/clickhouse-release-24-12#contributed-by-amos-bird)


This release added a new MergeTree setting, `allow_experimental_reverse_key,` which enables support for descending sort order in MergeTree sorting keys. You can see an example of usage below:



```
ENGINE = MergeTree 
ORDER BY (time DESC, key)
SETTINGS allow_experimental_reverse_key=1;

```

This table will sort the `time` field in descending order.


The ability to sort data like this is handy for [time series analysis](https://clickhouse.com/blog/working-with-time-series-data-and-functions-ClickHouse), especially Top N queries.


## JSON subcolumns as table primary key [\#](/blog/clickhouse-release-24-12#json-subcolumns-as-table-primary-key)


### Contributed by Pavel Kruglov [\#](/blog/clickhouse-release-24-12#contributed-by-pavel-kruglov)


As a reminder, ClickHouse’s [new powerful JSON implementation](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) stores the values of each unique JSON path in a true columnar fashion:


![0_release_24_12.png](/uploads/0_release_24_12_10b4d050d4.png)
The diagram above sketches how ClickHouse stores (and reads) any inserted JSON key path as a native subcolumn, allowing high data compression and maintaining query performance seen on classic types.


This release now supports using JSON subcolumns as a table’s primary key columns:



```
CREATE TABLE T
(
    data JSON()
)
ORDER BY (data.a, data.b);

```

This means that ingested JSON documents are (per [table part](https://clickhouse.com/docs/en/parts)) stored on disk [ordered](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#data-is-stored-on-disk-ordered-by-primary-key-columns) by the JSON subcolumns that are used as primary key columns. Additionally, ClickHouse will create a [primary index](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes) file for automatically [speeding up](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#the-primary-index-is-used-for-selecting-granules) queries that filter on primary key columns:


![1_release_24_12.png](/uploads/1_release_24_12_64853e1e91.png)
Furthermore, using JSON subcolumns as primary key columns [enables](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes#optimal-compression-ratio-of-data-files) optimal compression ratios for the subcolumns' `*.bin` data files, provided the primary key columns are arranged in ascending order of cardinality.


Let’s look at a more concrete example.


We use an AWS EC2 `m6i.8xlarge` instance as a test machine with 32 vCPUs and 128 GiB of main memory and the [Bluesky dataset as a test dataset](https://clickhouse.com/blog/building-a-medallion-architecture-for-bluesky-json-data-with-clickhouse).


We loaded the 100 million Bluesky events (one JSON document per event) into two ClickHouse tables.


This is the first table that doesn’t use any JSON subcolumns as primary key columns:



```
CREATE TABLE bluesky_100m_raw
(
    data JSON()
)
ORDER BY ();

```

The second table uses some JSON subcolumns as primary key columns (plus optionally some [type hints](https://clickhouse.com/docs/en/sql-reference/data-types/newjson) for these columns to get rid of some type\-casts in queries):



```

```
1CREATE TABLE bluesky_100m_primary_key
2(
3    data JSON(
4        kind LowCardinality(String), 
5        commit.operation LowCardinality(String), 
6        commit.collection LowCardinality(String), 
7        time_us UInt64
8    )
9)
10ORDER BY (
11    data.kind, 
12    data.commit.operation, 
13    data.commit.collection, 
14    fromUnixTimestamp64Micro(data.time_us)
15);
```

```

Both tables contain the same 100 million JSON docs.


Now we run a query (“When do people block people on BlueSky” \- adapted from the "When do people use BlueSky?” query that you can [run on the ClickHouse SQL playground](https://sql.clickhouse.com/?query_id=51KVUJ5FGJUQV9XU13JKL3&run_query=true&tab=charts)) on the table without a primary key:



```

```
1SELECT
2    toHour(fromUnixTimestamp64Micro(data.time_us::UInt64)) AS hour_of_day,
3    count() AS block_events
4FROM bluesky_100m_raw
5WHERE (data.kind = 'commit') 
6AND (data.commit.operation = 'create') 
7AND (data.commit.collection = 'app.bsky.graph.block')
8GROUP BY hour_of_day
9ORDER BY hour_of_day ASC;
```

```


```
    ┌─hour_of_day─┬─block_events─┐
 1. │           0 │        89395 │
 2. │           1 │       143542 │
 3. │           2 │       154424 │
 4. │           3 │       162894 │
 5. │           4 │        65893 │
 6. │           5 │        39556 │
 7. │           6 │        34359 │
 8. │           7 │        35230 │
 9. │           8 │        30812 │
10. │           9 │        35620 │
11. │          10 │        31094 │
12. │          16 │        33359 │
13. │          17 │        65555 │
14. │          18 │        65135 │
15. │          19 │        65775 │
16. │          20 │        70096 │
17. │          21 │        65640 │
18. │          22 │        75840 │
19. │          23 │       143024 │
    └─────────────┴──────────────┘

19 rows in set. Elapsed: 0.607 sec. Processed 100.00 million rows, 10.21 GB (164.83 million rows/s., 16.83 GB/s.)
Peak memory usage: 337.52 MiB.


```

Let’s run the same query on the table with a primary key (note that the query filters on a prefix of the primary key columns):



```

```
1SELECT
2    toHour(fromUnixTimestamp64Micro(data.time_us)) AS hour_of_day,
3    count() AS block_events
4FROM bluesky_100m_primary_key
5WHERE (data.kind = 'commit') 
6AND (data.commit.operation = 'create') 
7AND (data.commit.collection = 'app.bsky.graph.block')
8GROUP BY hour_of_day
9ORDER BY hour_of_day ASC;
```

```


```
    ┌─hour_of_day─┬─block_events─┐
 1. │           0 │        89395 │
 2. │           1 │       143542 │
 3. │           2 │       154424 │
 4. │           3 │       162894 │
 5. │           4 │        65893 │
 6. │           5 │        39556 │
 7. │           6 │        34359 │
 8. │           7 │        35230 │
 9. │           8 │        30812 │
10. │           9 │        35620 │
11. │          10 │        31094 │
12. │          16 │        33359 │
13. │          17 │        65555 │
14. │          18 │        65135 │
15. │          19 │        65775 │
16. │          20 │        70096 │
17. │          21 │        65640 │
18. │          22 │        75840 │
19. │          23 │       143024 │
    └─────────────┴──────────────┘

19 rows in set. Elapsed: 0.011 sec. Processed 1.47 million rows, 16.16 MB (129.69 million rows/s., 1.43 GB/s.)
Peak memory usage: 2.18 MiB.

```

Boom: The query runs 50 times faster and uses 150 times less memory.


## Iceberg REST catalog and schema evolution support [\#](/blog/clickhouse-release-24-12#iceberg-rest-catalog-and-schema-evolution-support)


### Contributed by Daniil Ivanik and Kseniia Sumarokova [\#](/blog/clickhouse-release-24-12#contributed-by-daniil-ivanik-and-kseniia-sumarokova)


This release introduces support for querying [Apache Iceberg REST catalogs](https://iceberg.apache.org/concepts/catalog/). At the moment, the Unity and Polaris catalogs are supported. We first create a table using the [Iceberg table engine](https://clickhouse.com/docs/en/engines/table-engines/integrations/iceberg):



```
CREATE TABLE unity_demo
ENGINE = Iceberg('https://dbc-55555555-5555.cloud.databricks.com/api/2.1/unity-catalog/iceberg')
SETTINGS
  catalog_type = 'rest',
  catalog_credential = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee:...',
  warehouse = 'unity',
  oauth_server_uri = 'https://dbc-55555555-5555.cloud.databricks.com/oidc/v1/token',
  auth_scope = 'all-apis,sql';

```

Then, we can query the data in the catalog’s underlying table:



```

SHOW TABLES FROM unity_demo;
SELECT * unity_demo."webinar.test";

```

The Iceberg table function supports schema evolution, including columns added or removed over time, renamed columns, and data types changed between primitive types.


## Parallel hash join by default in action [\#](/blog/clickhouse-release-24-12#parallel-hash-join-by-default-in-action)


### Contributed by Nikita Taranov [\#](/blog/clickhouse-release-24-12#contributed-by-nikita-taranov)


[Every](https://clickhouse.com/blog/clickhouse-release-24-05#cross-join-improvements) ClickHouse release brings JOIN improvements, and since this is our special Christmas release, it’s loaded with a sleigh full of JOIN enhancements! ✨


In the [24\.11 release post](https://clickhouse.com/blog/clickhouse-release-24-11#parallel-hash-join-is-the-default-join-strategy), we briefly mentioned that the [parallel hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join) is now ClickHouse's [default join strategy](https://clickhouse.com/docs/en/operations/settings/settings#join_algorithm). In this post, we will demonstrate the performance improvements of this change with a concrete example.


We use an AWS EC2 m6i.8xlarge instance with 32 vCPUs and 128 GiB of main memory as a test machine.


We use the [TPC\-H dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch) with a scaling factor of 100 as a test dataset for table joins, which means that the overall amount of data stored in all tables is 100 GB.  

We created and loaded the 8 tables (modeling a wholesale supplier's data warehouse) by [following the instructions in the docs](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch#data-generation-and-import).


Now we run query 3 from the [set of standard TPC\-H benchmark queries](https://clickhouse.com/docs/en/getting-started/example-datasets/tpch#queries) with the previous default join strategy of ClickHouse \- the [hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#hash-join):



```

```
1SELECT
2    l_orderkey,
3    sum(l_extendedprice * (1 - l_discount)) AS revenue,
4    o_orderdate,
5    o_shippriority
6FROM
7    customer,
8    orders,
9    lineitem
10WHERE
11    c_mktsegment = 'BUILDING'
12    AND c_custkey = o_custkey
13    AND l_orderkey = o_orderkey
14    AND o_orderdate < DATE '1995-03-15'
15    AND l_shipdate > DATE '1995-03-15'
16GROUP BY
17    l_orderkey,
18    o_orderdate,
19    o_shippriority
20ORDER BY
21    revenue DESC,
22    o_orderdate
23FORMAT Null
24SETTINGS join_algorithm='hash';
```

```


```
0 rows in set. Elapsed: 38.305 sec. Processed 765.04 million rows, 15.03 GB (19.97 million rows/s., 392.40 MB/s.)
Peak memory usage: 25.42 GiB.

```

Next, we run the same query with the new default join strategy of ClickHouse \- the [parallel hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join):



```

```
1SELECT
2    l_orderkey,
3    sum(l_extendedprice * (1 - l_discount)) AS revenue,
4    o_orderdate,
5    o_shippriority
6FROM
7    customer,
8    orders,
9    lineitem
10WHERE
11    c_mktsegment = 'BUILDING'
12    AND c_custkey = o_custkey
13    AND l_orderkey = o_orderkey
14    AND o_orderdate < DATE '1995-03-15'
15    AND l_shipdate > DATE '1995-03-15'
16GROUP BY
17    l_orderkey,
18    o_orderdate,
19    o_shippriority
20ORDER BY
21    revenue DESC,
22    o_orderdate
23FORMAT Null
24SETTINGS join_algorithm='default';
```

```


```
0 rows in set. Elapsed: 5.099 sec. Processed 765.04 million rows, 15.03 GB (150.04 million rows/s., 2.95 GB/s.)
Peak memory usage: 29.65 GiB.

```

The query runs \~8 times faster with the parallel hash join.


## Automatic JOIN reordering [\#](/blog/clickhouse-release-24-12#automatic-join-reordering)


### Contributed by Vladimir Cherkasov [\#](/blog/clickhouse-release-24-12#contributed-by-vladimir-cherkasov)


The next JOIN improvement of our Xmas release is automatic join reordering.


As a reminder, ClickHouse’s [fastest](https://clickhouse.com/blog/clickhouse-fully-supports-joins-how-to-choose-the-right-algorithm-part5#imdb-large-join-runs) join algorithms, like its new default algorithm, the [parallel hash join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join), are based on in\-memory hash tables and work by ① first loading the data from the right\-hand side table of the join query into a hash table (this is also called the build phase), and ② then the data from the left\-hand side table is streamed and joined by doing lookups into the hash table (this is called the scan phase):


![2_release_24_12.png](/uploads/2_release_24_12_a52f673ebf.png)
Note that because ClickHouse takes the right\-hand side table and creates a hash table with its data in RAM, placing the smaller table on the right\-hand side of the JOIN is more memory efficient and often much faster.


Similarly, ClickHouse’s additional non\-memory bound [join algorithms](https://clickhouse.com/blog/clickhouse-fully-supports-joins-how-to-choose-the-right-algorithm-part5#overview-of-clickhouse-join-algorithms) based on external sorting, like the [partial merge join](https://clickhouse.com/blog/clickhouse-fully-supports-joins-full-sort-partial-merge-part3#partial-merge-join), have a a build and a scan phase. For example, the partial merge join first builds a sorted version of the right table and then scans the left table. Therefore, placing the smaller table on the right\-hand side of the JOIN is often much faster.


Instead of always using the right table of a join for the build phase, ClickHouse now has a new setting \- [query\_plan\_join\_swap\_table](https://clickhouse.com/docs/en/operations/settings/settings#query_plan_join_swap_table) \- to determine which side of the join should be the build table. Possible values are:


- `auto` (the default value): In this mode, ClickHouse will try to choose the table with the smallest number of rows for the build phase. This is beneficial for almost every join query.
- `false`: Never swap tables (the right table is the build table).
- `true`: Always swap tables (the left table is the build table).


We will demonstrate the `auto` mode of the new `query_plan_join_swap_table` setting with another query over the TPC\-H tables (see the previous section for instructions to create and load the tables, and info about the test hardware) where we join the `lineitem` and the `part` tables.


First, we check the size of these two tables:



```
SELECT
    table,
    formatReadableQuantity(sum(rows)) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS size_on_disk
FROM system.parts
WHERE active AND (table IN ['lineitem', 'part'])
GROUP BY table
ORDER BY table ASC;

```


```
   ┌─table────┬─rows───────────┬─size_on_disk─┐
1. │ lineitem │ 600.04 million │ 26.69 GiB    │
2. │ part     │ 20.00 million  │ 896.47 MiB   │
   └──────────┴────────────────┴──────────────┘

```

As you can see, the `lineitem` table is significantly larger than the `part` table.


The next query joins the `lineitem` and the `part` tables, and places the much larger `lineitem` table on the right side of the join:



```

```
1SELECT 100.00 * sum(
2  CASE
3  WHEN p_type LIKE 'PROMO%'
4  THEN l_extendedprice * (1 - l_discount)
5  ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
6FROM part, lineitem
7WHERE l_partkey = p_partkey;
```

```

We run this query with the new `query_plan_join_swap_table` setting set to `false`, meaning that, as usual, the right table is the build table, and therefore ClickHouse first loads the data from the very large `lineitem` table into the main memory (in parallel into multiple hash tables as [the parallel hash join is the default join algoirthm](https://clickhouse.com/blog/clickhouse-release-24-11#parallel-hash-join-is-the-default-join-strategy)):



```

```
1SELECT 100.00 * sum(
2  CASE
3  WHEN p_type LIKE 'PROMO%'
4  THEN l_extendedprice * (1 - l_discount)
5  ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
6FROM part, lineitem
7WHERE l_partkey = p_partkey
8SETTINGS query_plan_join_swap_table='false';
```

```


```
   ┌──────promo_revenue─┐
1. │ 16.650141208349083 │
   └────────────────────┘

1 row in set. Elapsed: 55.687 sec. Processed 620.04 million rows, 12.67 GB (11.13 million rows/s., 227.57 MB/s.)
Peak memory usage: 24.39 GiB.

```

Next, we run the same query with the new `query_plan_join_swap_table` setting set to `auto` (the default value). Now ClickHouse will use estimations of the table sizes to determine which side of the join should be the build table. Therefore, ClickHouse first loads the data from the very much smaller `part` table into the main memory into hash tables before streaming and joining the data from the `lineitem` table:



```

```
1SELECT 100.00 * sum(
2  CASE
3  WHEN p_type LIKE 'PROMO%'
4  THEN l_extendedprice * (1 - l_discount)
5  ELSE 0 END) / sum(l_extendedprice * (1 - l_discount)) AS promo_revenue
6FROM part, lineitem
7WHERE l_partkey = p_partkey
8SETTINGS query_plan_join_swap_table='auto';
```

```


```
   ┌──────promo_revenue─┐
1. │ 16.650141208349083 │
   └────────────────────┘

1 row in set. Elapsed: 9.447 sec. Processed 620.04 million rows, 12.67 GB (65.63 million rows/s., 1.34 GB/s.)
Peak memory usage: 4.72 GiB.

```

As you can see, the query runs over 5 times faster and uses 5 times less memory.


## Optimization of JOIN expressions [\#](/blog/clickhouse-release-24-12#optimization-of-join-expressions)


### Contributed by János Benjamin Antal [\#](/blog/clickhouse-release-24-12#contributed-by-j%C3%A1nos-benjamin-antal)


For joins with a chain of conditions, separated by `OR`s, like shown in this abstract example…



```
JOIN ... ON (a=b AND x) OR (a=b AND y) OR (a=b AND z)

```

… ClickHouse uses hash tables per condition (when one of the [hash table\-based join algorithms](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2) is used).


One way to reduce the number of hash tables and to allow better predicate push downs is to extract common expressions from ON clause of the example JOIN above:



```
JOIN ...ON a=b AND (x OR y OR z)

```

This behavior can be enabled by setting the new `optimize_extract_common_expressions` setting to `1`. Because this setting is currently experimental, the default value is currently `0`.


We demonstrate this new setting with another query over the TPC\-H tables (see the previous section for instructions on creating and loading the tables, plus infos about the used hardware).


We run the following join query that has a chain of conditions, separated by `OR`s, with `optimize_extract_common_expressions` set to `0` (which disables the setting):



```

```
1SELECT
2  sum(l_extendedprice * (1 - l_discount)) AS revenue
3FROM
4  lineitem, part
5WHERE
6(
7        p_partkey = l_partkey
8    AND p_brand = 'Brand#12'
9    AND p_container in ('SM CASE', 'SM BOX','SM PACK', 'SM PKG')
10    AND l_quantity >= 1 AND l_quantity <= 1 + 10
11    AND p_size BETWEEN 1 AND 5
12    AND l_shipmode in ('AIR', 'AIR REG')
13    AND l_shipinstruct = 'DELIVER IN PERSON'
14)
15OR
16(
17        p_partkey = l_partkey
18    AND p_brand = 'Brand#23'
19    AND p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
20    AND l_quantity >= 10 AND l_quantity <= 10 + 10
21    AND p_size BETWEEN 1 AND 10
22    AND l_shipmode in ('AIR', 'AIR REG')
23    AND l_shipinstruct = 'DELIVER IN PERSON'
24)
25OR
26(
27        p_partkey = l_partkey
28    AND p_brand = 'Brand#34'
29    AND p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
30    AND l_quantity >= 20 AND l_quantity <= 20 + 10
31    AND p_size BETWEEN 1 AND 15
32    AND l_shipmode in ('AIR', 'AIR REG')
33    AND l_shipinstruct = 'DELIVER IN PERSON'
34)
35SETTINGS optimize_extract_common_expressions = 0;
```

```

On our test machine, this query had a progress of 3% after 30 minutes…so we aborted, and ran the same query with enabled `optimize_extract_common_expressions` setting:



```

```
1SELECT
2  sum(l_extendedprice * (1 - l_discount)) AS revenue
3FROM
4  lineitem, part
5WHERE
6(
7        p_partkey = l_partkey
8    AND p_brand = 'Brand#12'
9    AND p_container in ('SM CASE', 'SM BOX','SM PACK', 'SM PKG')
10    AND l_quantity >= 1 AND l_quantity <= 1 + 10
11    AND p_size BETWEEN 1 AND 5
12    AND l_shipmode in ('AIR', 'AIR REG')
13    AND l_shipinstruct = 'DELIVER IN PERSON'
14)
15OR
16(
17        p_partkey = l_partkey
18    AND p_brand = 'Brand#23'
19    AND p_container in ('MED BAG', 'MED BOX', 'MED PKG', 'MED PACK')
20    AND l_quantity >= 10 AND l_quantity <= 10 + 10
21    AND p_size BETWEEN 1 AND 10
22    AND l_shipmode in ('AIR', 'AIR REG')
23    AND l_shipinstruct = 'DELIVER IN PERSON'
24)
25OR
26(
27        p_partkey = l_partkey
28    AND p_brand = 'Brand#34'
29    AND p_container in ('LG CASE', 'LG BOX', 'LG PACK', 'LG PKG')
30    AND l_quantity >= 20 AND l_quantity <= 20 + 10
31    AND p_size BETWEEN 1 AND 15
32    AND l_shipmode in ('AIR', 'AIR REG')
33    AND l_shipinstruct = 'DELIVER IN PERSON'
34)
35SETTINGS optimize_extract_common_expressions = 1;
```

```


```
   ┌───────revenue─┐
1. │ 298937728.882 │ -- 298.94 million
   └───────────────┘

1 row in set. Elapsed: 3.021 sec. Processed 620.04 million rows, 38.21 GB (205.24 million rows/s., 12.65 GB/s.)
Peak memory usage: 2.79 GiB.

```

Now the query returned its result in 3 seconds.


## Non\-equi JOINs supported by default [\#](/blog/clickhouse-release-24-12#non-equi-joins-supported-by-default)


### Contributed by Vladimir Cherkasov [\#](/blog/clickhouse-release-24-12#contributed-by-vladimir-cherkasov-1)


Since version 24\.05, ClickHouse [had experimental support for non\-equal conditions](https://clickhouse.com/blog/clickhouse-release-24-05#non-equal-join) in the ON clause of JOIN:



```
-- Equi join
SELECT t1.*, t2.* FROM t1 JOIN t2 ON t1.key = t2.key;

-- Non-equi joins
SELECT t1.*, t2.* FROM t1 JOIN t2 ON t1.key != t2.key;
SELECT t1.*, t2.* FROM t1 JOIN t2 ON t1.key > t2.key


```

With the current release, this support is no longer experimental and enabled by default.


Stay tuned for the next releases this year that will bring, [as promised](https://clickhouse.com/blog/clickhouse-release-24-05#cross-join-improvements), even more JOIN improvements!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
