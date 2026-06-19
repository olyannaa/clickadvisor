---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-24-12
ch_version_introduced: '85.24'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 12
---

contains the string `e`. We can write the following query using the `LIKE` operator: ``` ``` 1SELECT 2 subreddit_type, 3 count() AS c 4FROM reddit 5WHERE subreddit_type LIKE '%restricted%' 6GROUP BY ALL 7ORDER BY c DESC; ``` ```

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
