---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-24-10
ch_version_introduced: '922.460'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 10
---

table’s partitions. When we run the clone operation, ClickHouse doesn’t create a copy of the data for the new table. Instead, it creates new parts for the new table that are hard links to the existing table parts.

Data parts in ClickHouse are immutable, which means that if we add new data or modify existing data in either of the tables, the other table will not be affected.

For example, let’s say we have a table called `people` based on the CSV file mentioned earlier:

```
CREATE TABLE people 
ORDER BY Index AS
SELECT * 
FROM 'people*.csv'
SETTINGS schema_inference_make_columns_nullable=0;

```

We can clone this table to another table called `people2` by running the following query:

```
CREATE TABLE people2 CLONE AS people;

```

The two tables now contain the same data.

```
SELECT count()
FROM people

   ┌─count()─┐
1. │ 1000000 │
   └─────────┘

SELECT count()
FROM people2

   ┌─count()─┐
1. │ 1000000 │
   └─────────┘

```

But we can still add data to them independently. For example, let’s add all the rows from the CSV file to the `people2` table:

```
INSERT INTO people2 
SELECT * 
FROM 'people*.csv';

```

Now, let’s count the number of records in each table:

```
SELECT count()
FROM people

   ┌─count()─┐
1. │ 1000000 │
   └─────────┘

SELECT count()
FROM people2

   ┌─count()─┐
1. │ 2000000 │
   └─────────┘

```

## Real\-time metrics in the client [\#](/blog/clickhouse-release-24-10#real-time-metrics-in-the-client)

### Contributed by Maria Khristenko, Julia Kartseva [\#](/blog/clickhouse-release-24-10#contributed-by-maria-khristenko-julia-kartseva)

When running queries from the ClickHouse Client or with clickhouse\-local, we can get a more fine\-grained view of what’s happening by pressing the space bar.

For example, let’s say we run the following query:

```
SELECT product_category, count() AS reviews, 
       round(avg(star_rating), 2) as avg
FROM s3(
  's3://datasets-documentation/amazon_reviews/amazon_reviews_2015.snappy.parquet'
)
GROUP BY ALL
LIMIT 10;

```

If we press the space bar while the query’s running, we’ll see the following:

Your browser does not support the video tag.

Then, when the query finishes, it will show the following stats:

```
Event name                            Value
AddressesMarkedAsFailed               2
ContextLock                           32
InitialQuery                          1
QueriesWithSubqueries                 1
Query                                 1
S3Clients                             1
S3HeadObject                          2
S3ReadMicroseconds                    9.15 s
S3ReadRequestsCount                   52
S3WriteRequestsCount                  2
S3WriteRequestsErrors                 2
SchemaInferenceCacheHits              1
SchemaInferenceCacheSchemaHits        1
SelectQueriesWithSubqueries           1
SelectQuery                           1
StorageConnectionsCreated             17
StorageConnectionsElapsedMicroseconds 5.02 s
StorageConnectionsErrors              2
StorageConnectionsExpired             12
StorageConnectionsPreserved           47
StorageConnectionsReset               7
StorageConnectionsReused              35
TableFunctionExecute                  1

```

## Caching remote files [\#](/blog/clickhouse-release-24-10#caching-remote-files)

### Contributed by Kseniia Sumarokova [\#](/blog/clickhouse-release-24-10#contributed-by-kseniia-sumarokova)
