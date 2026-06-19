# Working with Time Series Data in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Working with Time Series Data in ClickHouse

![](/_next/image?url=%2Fuploads%2FDenys_96799559c1.png&w=96&q=75)[Denys Golotiuk](/authors/denys-golotiuk)Jan 10, 2023 · 24 minutes read![time-series.png](/uploads/time_series_cd37aa68a3.png)
## Introduction [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#introduction)


Many datasets are collected over time to analyze and discover meaningful trends. Each data point usually has a time assigned when we collect logs or business events. When exploring our data during an analysis stage, we often slice or group by different periods to understand how our data changes over time. Any data that changes over time in any way is **time\-series data**. ClickHouse has powerful tools to store and process time\-series data efficiently and can be used for both simple solutions and data discovery, as well as for powering real\-time analytical applications at the Petabyte scale.


This blog post provides tips and tricks for working with [time series data](https://clickhouse.com/engineering-resources/what-is-time-series-database) based on everyday tasks that we see our users needing to perform. We cover querying and common data type problems, such as handling gauges, and explore how performance can be improved as we scale.


All examples in this post can be reproduced in our [sql.clickhouse.com](https://sql.clickhouse.com) environment (see the `blogs` database). Alternatively, if you want to dive deeper into this dataset, [ClickHouse Cloud](https://clickhouse.cloud/signUp) is a great starting point \- spin up a cluster using a free trial, load the data, let us deal with the infrastructure, and get querying!


## Date and time types available in ClickHouse [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#date-and-time-types-available-in-clickhouse)


ClickHouse has several date and time types. Depending on your use case, different types can be applied. Using the [Date](https://clickhouse.com/docs/en/sql-reference/data-types/date) type for dates should be sufficient in most cases. This type only requires 2 bytes to store a date but limits the range to `[1970-01-01, 2149-06-06]`. The [DateTime](https://clickhouse.com/docs/en/sql-reference/data-types/datetime) allows storing dates and times up to the year 2106\. For cases where more precision is required, the [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) can be used. This allows storing time with up to nanoseconds precision:



```

CREATE TABLE dates
(
    `date` Date,
    `datetime` DateTime,
    `precise_datetime` DateTime64(3),
    `very_precise_datetime` DateTime64(9)
)
ENGINE = MergeTree
ORDER BY tuple()


```


We can use the `now()` function to return the current time and `now64()` to get it in a specified precision via the first argument.



```

INSERT INTO dates SELECT NOW(), NOW(), NOW64(3), NOW64(9);


```


This will populate our columns with time accordingly to the column type:



```

SELECT * FROM dates

Row 1:
──────
date:                  2022-12-27
datetime:              2022-12-27 12:51:15
precise_datetime:      2022-12-27 12:51:15.329
very_precise_datetime: 2022-12-27 12:51:15.329098089


```


### Timezones [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#timezones)


Practical cases require having timezones stored as well in many cases. ClickHouse let’s us set timezone as a last argument to the [DateTime](https://clickhouse.com/docs/en/sql-reference/data-types/datetime) or [DateTime64](https://clickhouse.com/docs/en/sql-reference/data-types/datetime64) types:



```

CREATE TABLE dtz
(
    `id` Int8,
    `t` DateTime('Europe/Berlin')
)
ENGINE = MergeTree
ORDER BY tuple()


```


Having defined a timezone in our DDL, we can now insert times using different timezones:



```

INSERT INTO dtz SELECT 1, toDateTime('2022-12-12 12:13:14', 'America/New_York')

INSERT INTO dtz SELECT 2, toDateTime('2022-12-12 12:13:14')

SELECT * FROM dtz

┌─id─┬───────────────────t─┐
│  1 │ 2022-12-12 18:13:14 │
│  2 │ 2022-12-12 13:13:14 │
└────┴─────────────────────┘


```


Note how we have inserted time in `America/New_York` format, and it was automatically converted to `Europe/Berlin` at query time. When no time zone is specified, the server's local time zone is used.


## Querying [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#querying)


We’re going to explore ClickHouse time\-series querying capabilities with the [Wikistat](https://github.com/ClickHouse/ClickHouse/issues/15318) (Wikipedia pageviews data) dataset:



```

CREATE TABLE wikistat
(
    `time` DateTime,
    `project` String,
    `subproject` String,
    `path` String,
    `hits` UInt64
)
ENGINE = MergeTree
ORDER BY (time)


```


Let’s populate this table with 1b records:



```

INSERT INTO wikistat SELECT *
FROM s3('https://ClickHouse-public-datasets.s3.amazonaws.com/wikistat/partitioned/wikistat*.native.zst') LIMIT 1e9

0 rows in set. Elapsed: 421.868 sec. Processed 2.00 billion rows, 100.89 GB (4.74 million rows/s., 239.15 MB/s.)


```


### Aggregating based on time periods [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#aggregating-based-on-time-periods)


The most popular requirement is to aggregate data based on periods, e.g. get the total amount of hits for each day:



```

SELECT
    sum(hits) AS h,
    toDate(time) AS d
FROM wikistat
GROUP BY d
ORDER BY d ASC
LIMIT 5

┌────────h─┬──────────d─┐
│ 31045470 │ 2015-05-01 │
│ 30309226 │ 2015-05-02 │
│ 33704223 │ 2015-05-03 │
│ 34700248 │ 2015-05-04 │
│ 34634353 │ 2015-05-05 │
└──────────┴────────────┘

5 rows in set. Elapsed: 0.264 sec. Processed 1.00 billion rows, 12.00 GB (3.78 billion rows/s., 45.40 GB/s.)

[✎](https://sql.clickhouse.com?query_id=537DNRRQ1XJBOTNA9UXWPA)

```


We’ve used [toDate()](https://clickhouse.com/docs/en/sql-reference/functions/type-conversion-functions/#todate) function here, which converts the specified time to a date type. Alternatively, we can batch by an hour and filter on the specific date:



```

SELECT
    sum(hits) AS v,
    toStartOfHour(time) AS h
FROM wikistat
WHERE date(time) = '2015-05-01'
GROUP BY h
ORDER BY h ASC
LIMIT 5

┌───────v─┬───────────────────h─┐
│ 1199168 │ 2015-05-01 01:00:00 │
│ 1207276 │ 2015-05-01 02:00:00 │
│ 1189451 │ 2015-05-01 03:00:00 │
│ 1119078 │ 2015-05-01 04:00:00 │
│ 1037526 │ 2015-05-01 05:00:00 │
└─────────┴─────────────────────┘
5 rows in set. Elapsed: 0.013 sec. Processed 7.72 million rows, 92.54 MB (593.64 million rows/s., 7.12 GB/s.)

[✎](https://sql.clickhouse.com?query_id=9GJNUGQSWRRPZRPMFVD2DU)

```


The [`toStartOfHour()`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#tostartofhour) function used here converts the given time to the start of the hour. ClickHouse has [batching functions](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#tostartofyear) for generating periods that cover almost all imaginable cases, allowing you to group by year, month, day, hour, or even arbitrary intervals, e.g., [5 minutes](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#tostartoffiveminutes), easily.


### Custom grouping intervals [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#custom-grouping-intervals)


We can also use the [toStartOfInterval()](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#tostartofintervaltime_or_data-interval-x-unit--time_zone) function to group by custom intervals. Let’s say we want to group by 4\-hour intervals:



```

SELECT
    sum(hits) AS v,
    toStartOfInterval(time, INTERVAL 4 HOUR) AS h
FROM wikistat
WHERE date(time) = '2015-05-01'
GROUP BY h
ORDER BY h ASC
LIMIT 6

┌───────v─┬───────────────────h─┐
│ 3595895 │ 2015-05-01 00:00:00 │
│ 4161080 │ 2015-05-01 04:00:00 │
│ 4602523 │ 2015-05-01 08:00:00 │
│ 6072107 │ 2015-05-01 12:00:00 │
│ 6604783 │ 2015-05-01 16:00:00 │
│ 6009082 │ 2015-05-01 20:00:00 │
└─────────┴─────────────────────┘

6 rows in set. Elapsed: 0.020 sec. Processed 7.72 million rows, 92.54 MB (386.78 million rows/s., 4.64 GB/s.)

[✎](https://sql.clickhouse.com?query_id=7HPC3EXF1K3CCFEZGJ36XT)

```


With the [`toStartOfInterval()`](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#tostartofintervaltime_or_data-interval-x-unit--time_zone) function, we use [INTERVAL](https://clickhouse.com/docs/en/sql-reference/data-types/special-data-types/interval/) clause to set the required batching period:


### Filling empty groups [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#filling-empty-groups)


In a lot of cases we deal with sparse data with some absent intervals. This results in empty buckets. Let’s take the following example where we group data by 1\-hour intervals. This will out the following stats with some hours missing values:



```

SELECT
    toStartOfHour(time) AS h,
    sum(hits)
FROM wikistat
WHERE (project = 'it') AND (subproject = 'm') AND (date(time) = '2015-06-12')
GROUP BY h
ORDER BY h ASC

┌───────────────────h─┬─sum(hits)─┐
│ 2015-06-12 00:00:00 │     16246 │
│ 2015-06-12 01:00:00 │      7900 │
│ 2015-06-12 02:00:00 │      4517 │
│ 2015-06-12 03:00:00 │      2982 │
│ 2015-06-12 04:00:00 │      2748 │
│ 2015-06-12 05:00:00 │      4581 │
│ 2015-06-12 06:00:00 │      8908 │
│ 2015-06-12 07:00:00 │     13514 │
│ 2015-06-12 08:00:00 │     18327 │
│ 2015-06-12 09:00:00 │     22541 │
│ 2015-06-12 10:00:00 │     25366 │
│ 2015-06-12 11:00:00 │     25383 │
│ 2015-06-12 12:00:00 │     29074 │ <- missing values
│ 2015-06-12 23:00:00 │     27199 │
└─────────────────────┴───────────┘

14 rows in set. Elapsed: 0.029 sec. Processed 6.98 million rows, 225.76 MB (237.19 million rows/s., 7.67 GB/s.)

[✎](https://sql.clickhouse.com?query_id=AWOMAV5AQUHFUHVXZ5UGDR)

```


ClickHouse provides the [WITH FILL](https://clickhouse.com/docs/en/sql-reference/statements/select/order-by/#order-by-expr-with-fill-modifier) modifier to address this. This will fill out all the empty hours with zeros, so we can better understand distribution over time:



```

SELECT
    toStartOfHour(time) AS h,
    sum(hits)
FROM wikistat
WHERE (project = 'it') AND (subproject = 'm') AND (date(time) = '2015-06-12')
GROUP BY h
ORDER BY h ASC WITH FILL STEP toIntervalHour(1)

┌───────────────────h─┬─sum(hits)─┐
│ 2015-06-12 00:00:00 │     16246 │
│ 2015-06-12 01:00:00 │      7900 │
│ 2015-06-12 02:00:00 │      4517 │
│ 2015-06-12 03:00:00 │      2982 │
│ 2015-06-12 04:00:00 │      2748 │
│ 2015-06-12 05:00:00 │      4581 │
│ 2015-06-12 06:00:00 │      8908 │
│ 2015-06-12 07:00:00 │     13514 │
│ 2015-06-12 08:00:00 │     18327 │
│ 2015-06-12 09:00:00 │     22541 │
│ 2015-06-12 10:00:00 │     25366 │
│ 2015-06-12 11:00:00 │     25383 │
│ 2015-06-12 12:00:00 │     29074 │
│ 2015-06-12 13:00:00 │         0 │
│ 2015-06-12 14:00:00 │         0 │
│ 2015-06-12 15:00:00 │         0 │
│ 2015-06-12 16:00:00 │         0 │
│ 2015-06-12 17:00:00 │         0 │
│ 2015-06-12 18:00:00 │         0 │
│ 2015-06-12 19:00:00 │         0 │
│ 2015-06-12 20:00:00 │         0 │
│ 2015-06-12 21:00:00 │         0 │
│ 2015-06-12 22:00:00 │         0 │
│ 2015-06-12 23:00:00 │     27199 │
└─────────────────────┴───────────┘

24 rows in set. Elapsed: 0.039 sec. Processed 6.98 million rows, 225.76 MB (180.92 million rows/s., 5.85 GB/s.)

[✎](https://sql.clickhouse.com?query_id=PUNOYTV9U37JUHQHDBK1RB)

```


### Rolling time windows [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#rolling-time-windows)


Sometimes, we don’t want to deal with the start of intervals (like the start of the day or an hour) but window intervals. Let’s say we want to understand the total hits for a window, not based on days but on a 24\-hour period offset from 6 pm. We’ve used [date\_diff()](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#date_diff) function to calculate the difference between a basepoint time and each record’s time. In this case, the `d` column will represent the difference in days (e.g., 1 day ago, 2 days ago, etc.):



```

SELECT
    sum(hits),
    dateDiff('day', toDateTime('2015-05-01 18:00:00'), time) AS d
FROM wikistat
GROUP BY d
ORDER BY d ASC
LIMIT 5

┌─sum(hits)─┬─d─┐
│  31045470 │ 0 │
│  30309226 │ 1 │
│  33704223 │ 2 │
│  34700248 │ 3 │
│  34634353 │ 4 │
└───────────┴───┘

5 rows in set. Elapsed: 0.283 sec. Processed 1.00 billion rows, 12.00 GB (3.54 billion rows/s., 42.46 GB/s.)

[✎](https://sql.clickhouse.com?query_id=NT9TMF54T6ZD6EIJOQSWSQ)

```


## Quick visual analysis [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#quick-visual-analysis)


ClickHouse provides the [bar()](https://clickhouse.com/docs/en/sql-reference/functions/other-functions/#bar) function to build quick visuals and help with the analysis of data. This will quickly visualize the most and least popular hours in terms of page views:



```

SELECT
    toHour(time) AS h,
    sum(hits) AS t,
    bar(t, 0, max(t) OVER (), 50) AS bar
FROM wikistat
GROUP BY h
ORDER BY h ASC

┌──h─┬─────────t─┬─bar────────────────────────────────────────────────┐
│  0 │ 146208847 │ ██████████████████████████████████████▋            │
│  1 │ 143713140 │ █████████████████████████████████████▊             │
│  2 │ 144977675 │ ██████████████████████████████████████▎            │
│  3 │ 145089174 │ ██████████████████████████████████████▎            │
│  4 │ 139602368 │ ████████████████████████████████████▊              │
│  5 │ 130795734 │ ██████████████████████████████████▌                │
│  6 │ 126456113 │ █████████████████████████████████▍                 │
│  7 │ 127328312 │ █████████████████████████████████▋                 │
│  8 │ 131772449 │ ██████████████████████████████████▋                │
│  9 │ 137695533 │ ████████████████████████████████████▍              │
│ 10 │ 143381876 │ █████████████████████████████████████▊             │
│ 11 │ 146690963 │ ██████████████████████████████████████▋            │
│ 12 │ 155662847 │ █████████████████████████████████████████▏         │
│ 13 │ 169130249 │ ████████████████████████████████████████████▋      │
│ 14 │ 182213956 │ ████████████████████████████████████████████████▏  │
│ 15 │ 188534642 │ █████████████████████████████████████████████████▋ │
│ 16 │ 189214224 │ ██████████████████████████████████████████████████ │
│ 17 │ 186824967 │ █████████████████████████████████████████████████▎ │
│ 18 │ 185885433 │ █████████████████████████████████████████████████  │
│ 19 │ 186112653 │ █████████████████████████████████████████████████▏ │
│ 20 │ 187530882 │ █████████████████████████████████████████████████▌ │
│ 21 │ 185485979 │ █████████████████████████████████████████████████  │
│ 22 │ 175522556 │ ██████████████████████████████████████████████▍    │
│ 23 │ 157537595 │ █████████████████████████████████████████▋         │
└────┴───────────┴────────────────────────────────────────────────────┘

24 rows in set. Elapsed: 0.264 sec. Processed 1.00 billion rows, 12.00 GB (3.79 billion rows/s., 45.53 GB/s.)

[✎](https://sql.clickhouse.com?query_id=7FM7GEM6MGK3I4Y916BRKK)

```


Note how we’ve used a window max() to compute the max hits per hour, passing this to the `bar()` function for visualization.


## Counters and Gauge metrics [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#counters-and-gauge-metrics)


There are two basic types of metrics we encounter when working with time series:


- Counters are used to count the total number of tracked events sliced by attributes and grouped by a time frame. A popular example here is tracking website visitors.
- Gauges are used to set a metric value that tends to change over time. A good example here is tracking CPU load.


Both metric types are easy to work with in ClickHouse and don’t require any additional configuration. Counters can be easily queried using `count()` or `sum()` functions, depending on the storage policy. To efficiently query for gauges, the [`any()`](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/any/) aggregate function can be used together with [INTERPOLATE](https://clickhouse.com/docs/en/sql-reference/statements/select/order-by/#order-by-expr-with-fill-modifier) modifier to fill any missing data points:



```

CREATE TABLE metrics
( `time` DateTime, `name` String, `value` UInt32 )
ENGINE = MergeTree ORDER BY tuple();

INSERT INTO metrics VALUES
('2022-12-28 06:32:16', 'cpu', 7), ('2022-12-28 14:31:22', 'cpu', 50), ('2022-12-28 14:30:30', 'cpu', 25), ('2022-12-28 14:25:36', 'cpu', 10), ('2022-12-28 11:32:08', 'cpu', 5), ('2022-12-28 10:32:12', 'cpu', 5);

SELECT
    toStartOfHour(time) AS h,
    any(value) AS v
FROM metrics
GROUP BY h
ORDER BY h ASC WITH FILL STEP toIntervalHour(1)
INTERPOLATE ( v AS v )

┌───────────────────h─┬──v─┐
│ 2022-12-28 06:00:00 │  7 │
│ 2022-12-28 07:00:00 │  7 │ <- filled
│ 2022-12-28 08:00:00 │  7 │ <- filled
│ 2022-12-28 09:00:00 │  7 │ <- filled
│ 2022-12-28 10:00:00 │  5 │
│ 2022-12-28 11:00:00 │  5 │ <- filled
│ 2022-12-28 12:00:00 │  5 │ <- filled
│ 2022-12-28 13:00:00 │  5 │ <- filled
│ 2022-12-28 14:00:00 │ 50 │
└─────────────────────┴────┘


```


In this case, highlighted values were automatically filled by ClickHouse, to follow the gauge nature of the metric within a continuous time range.


### Histograms [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#histograms)


A popular use case for time series data is to build histograms based on tracked events. Suppose we wanted to understand the distribution of a number of pages based on their total hits for a specific date. We can use the [histogram()](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/parametric-functions/#histogram) function to automatically generate an adaptive histogram based on the number of bins and then use [arrayJoin()](https://clickhouse.com/docs/en/sql-reference/functions/array-join/) and [bar()](https://clickhouse.com/docs/en/sql-reference/functions/other-functions/#bar) to visualize it:



```

WITH histogram(10)(hits) AS h
SELECT
    round(arrayJoin(h).1) AS l,
    round(arrayJoin(h).2) AS u,
    arrayJoin(h).3 AS w,
    bar(w, 0, max(w) OVER (), 20) AS b
FROM
(
    SELECT
        path,
        sum(hits) AS hits
    FROM wikistat
    WHERE date(time) = '2015-06-15'
    GROUP BY path
    HAVING hits > 10000.
)

┌───────l─┬───────u─┬──────w─┬─b────────────────────┐
│   10034 │   27769 │ 84.375 │ ████████████████████ │
│   27769 │   54281 │  19.75 │ ████▋                │
│   54281 │   79020 │  3.875 │ ▊                    │
│   79020 │   96858 │   2.75 │ ▋                    │
│   96858 │  117182 │   1.25 │ ▎                    │
│  117182 │  173244 │      1 │ ▏                    │
│  173244 │  232806 │  1.125 │ ▎                    │
│  232806 │  405693 │   1.75 │ ▍                    │
│  405693 │ 1126826 │  1.125 │ ▎                    │
│ 1126826 │ 1691188 │      1 │ ▏                    │
└─────────┴─────────┴────────┴──────────────────────┘

10 rows in set. Elapsed: 0.134 sec. Processed 6.64 million rows, 268.25 MB (49.48 million rows/s., 2.00 GB/s.)

[✎](https://sql.clickhouse.com?query_id=JAEWDDPZHMJOVSZEDD3RVB)

```


We’ve filtered only pages with more than 10k views. In the result set, `l` and `r` are the left and right boundaries of the bin, and `w` is a bin width (count of items in this bin).


### Trends [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#trends)


Sometimes we want to understand how metrics change over time by calculating the difference between consecutive values. Let’s compute daily hits for a given page (`path` column) and the change in this value from the previous day:



```

SELECT
    toDate(time) AS d,
    sum(hits) AS h,
    lagInFrame(h) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS p,
    h - p AS trend
FROM wikistat
WHERE path = 'Ana_Sayfa'
GROUP BY d
ORDER BY d ASC
LIMIT 15

┌──────────d─┬──────h─┬──────p─┬──trend─┐
│ 2015-05-01 │ 214612 │      0 │ 214612 │
│ 2015-05-02 │ 211546 │ 214612 │  -3066 │
│ 2015-05-03 │ 221412 │ 211546 │   9866 │
│ 2015-05-04 │ 219940 │ 221412 │  -1472 │
│ 2015-05-05 │ 211548 │ 219940 │  -8392 │
│ 2015-05-06 │ 212358 │ 211548 │    810 │
│ 2015-05-07 │ 208150 │ 212358 │  -4208 │
│ 2015-05-08 │ 208871 │ 208150 │    721 │
│ 2015-05-09 │ 210753 │ 208871 │   1882 │
│ 2015-05-10 │ 212918 │ 210753 │   2165 │
│ 2015-05-11 │ 211884 │ 212918 │  -1034 │
│ 2015-05-12 │ 212314 │ 211884 │    430 │
│ 2015-05-13 │ 211192 │ 212314 │  -1122 │
│ 2015-05-14 │ 206172 │ 211192 │  -5020 │
│ 2015-05-15 │ 195832 │ 206172 │ -10340 │
└────────────┴────────┴────────┴────────┘

15 rows in set. Elapsed: 0.550 sec. Processed 1.00 billion rows, 28.62 GB (1.82 billion rows/s., 52.00 GB/s.)

[✎](https://sql.clickhouse.com?query_id=5GDTHIPSNWHKXN1KUSQSMJ)

```


We’ve used [lagInFrame() window](https://clickhouse.com/docs/en/sql-reference/window-functions/) function to get the previous `hits` value, and then used this to calculate the difference as a `trend` column.


### Cumulative values [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#cumulative-values)


Following the previous example, sometimes we want to do the opposite \- get a cumulative sum of certain metrics over time. This is usually used for counters to visualize cumulative growth and can be easily implemented using window functions:



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


### Rates [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#rates)


Calculating metric rates (speed per time unit) is also popular when working with time series. Suppose we want to get a certain page hit rate per second for a given date grouped by hours:



```

SELECT
    toStartOfHour(time) AS t,
    sum(hits) AS h,
    round(h / (60 * 60), 2) AS rate,
    bar(rate * 10, 0, max(rate * 10) OVER (), 25) AS b
FROM wikistat
WHERE path = 'Ana_Sayfa'
GROUP BY t
ORDER BY t ASC
LIMIT 23

┌───────────────────t─┬─────h─┬─rate─┬─b───────────────────────┐
│ 2015-05-01 01:00:00 │  6749 │ 1.87 │ ████████████▊           │
│ 2015-05-01 02:00:00 │  6054 │ 1.68 │ ███████████▋            │
│ 2015-05-01 03:00:00 │  5823 │ 1.62 │ ███████████▏            │
│ 2015-05-01 04:00:00 │  5908 │ 1.64 │ ███████████▎            │
│ 2015-05-01 05:00:00 │  6131 │  1.7 │ ███████████▋            │
│ 2015-05-01 06:00:00 │  7067 │ 1.96 │ █████████████▌          │
│ 2015-05-01 07:00:00 │  8169 │ 2.27 │ ███████████████▋        │
│ 2015-05-01 08:00:00 │  9526 │ 2.65 │ ██████████████████▎     │
│ 2015-05-01 09:00:00 │ 10474 │ 2.91 │ ████████████████████▏   │
│ 2015-05-01 10:00:00 │ 10389 │ 2.89 │ ████████████████████    │
│ 2015-05-01 11:00:00 │  9830 │ 2.73 │ ██████████████████▊     │
│ 2015-05-01 12:00:00 │ 10712 │ 2.98 │ ████████████████████▋   │
│ 2015-05-01 13:00:00 │ 10301 │ 2.86 │ ███████████████████▋    │
│ 2015-05-01 14:00:00 │ 10181 │ 2.83 │ ███████████████████▌    │
│ 2015-05-01 15:00:00 │ 10324 │ 2.87 │ ███████████████████▊    │
│ 2015-05-01 16:00:00 │ 10497 │ 2.92 │ ████████████████████▏   │
│ 2015-05-01 17:00:00 │ 10676 │ 2.97 │ ████████████████████▌   │
│ 2015-05-01 18:00:00 │ 11121 │ 3.09 │ █████████████████████▍  │
│ 2015-05-01 19:00:00 │ 11277 │ 3.13 │ █████████████████████▋  │
│ 2015-05-01 20:00:00 │ 11553 │ 3.21 │ ██████████████████████▏ │
│ 2015-05-01 21:00:00 │ 11637 │ 3.23 │ ██████████████████████▎ │
│ 2015-05-01 22:00:00 │ 11298 │ 3.14 │ █████████████████████▋  │
│ 2015-05-01 23:00:00 │  8915 │ 2.48 │ █████████████████▏      │
└─────────────────────┴───────┴──────┴─────────────────────────┘

23 rows in set. Elapsed: 0.572 sec. Processed 1.00 billion rows, 28.62 GB (1.75 billion rows/s., 50.06 GB/s.)

[✎](https://sql.clickhouse.com?query_id=XQVSQGEZEZUZUAQURVO8VZ)

```


## Improving time series storage efficiency [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#improving-time-series-storage-efficiency)


### Type optimization [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#type-optimization)


The general approach to optimizing storage efficiency is using [optimal data types](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema). Let’s take the `project` and `subprojects` columns. These columns are of type String, but have a relatively small amount of unique values:



```

SELECT
    uniq(project),
    uniq(subproject)
FROM wikistat

┌─uniq(project)─┬─uniq(subproject)─┐
│          1095 │               99 │
└───────────────┴──────────────────┘

1 row in set. Elapsed: 0.895 sec. Processed 1.00 billion rows, 20.43 GB (1.12 billion rows/s., 22.84 GB/s.)

[✎](https://sql.clickhouse.com?query_id=G7YRTCRZ7RJPMTZCRFCPDB)

```


This means we can use the [LowCardinality()](https://clickhouse.com/docs/en/sql-reference/data-types/lowcardinality/) data type, which uses dictionary\-based encoding. This causes ClickHouse to store the internal value ID instead of the original string value, which in turn saves a lot of space:



```

ALTER TABLE wikistat
    MODIFY COLUMN `project` LowCardinality(String),
    MODIFY COLUMN `subproject` LowCardinality(String)


```


We’ve also used [UInt64](https://clickhouse.com/docs/en/sql-reference/data-types/int-uint/) type for the `hits` column, which takes 8 bytes, but has a relatively small max value:



```

SELECT max(hits)
FROM wikistat

┌─max(hits)─┐
│    237913 │
└───────────┘

[✎](https://sql.clickhouse.com?query_id=DE5AJMQ3DLWAPSOJP1PI9C)

```


Given this value, we can use `UInt32` instead, which takes only 4 bytes, and allows us to store up to \~4b as a max value:



```

ALTER TABLE wikistat
MODIFY COLUMN `hits` UInt32


```


This will reduce the size of this column in memory by at least 2 times. Note that the size on disk will remain unchanged due to compression. But be careful, pick data types that are not too small!


### Codecs to optimize sequences storage [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#codecs-to-optimize-sequences-storage)


When we deal with sequential data, which time\-series data effectively is, we can further improve storage efficiency by using [special codecs](https://clickhouse.com/docs/en/sql-reference/statements/create/table/#specialized-codecs). The general idea is to store changes between values instead of absolute values themselves, which results in much less space needed when dealing with slowly changing data:



```

ALTER TABLE wikistat
MODIFY COLUMN `time` CODEC(Delta, ZSTD)


```


We’ve used [Delta](https://clickhouse.com/docs/en/sql-reference/statements/create/table/#delta) codec for `time` column, which fits time series data best. The [right ordering key](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-cardinality/) can also save disk space. Since we usually want to filter by a path, we should also add this to the key. This requires recreation of the table. Let’s wrap it all and compare storage efficiency with and without optimized types:




| **Unoptimized table** | **Optimized table** |
| --- | --- |
| ```  CREATE TABLE wikistat (     `time` DateTime,     `project` String,     `subproject` String,     `path` String,     `hits` UInt64 ) ENGINE = MergeTree ORDER BY (time)   ``` | ```  CREATE TABLE optimized_wikistat (     `time` DateTime CODEC(Delta(4), ZSTD(1)),     `project` LowCardinality(String),     `subproject` LowCardinality(String),     `path` String,     `hits` UInt32 ) ENGINE = MergeTree ORDER BY (path, time)   ``` |
| **11\.09 GiB** | **1\.68 GiB** |



As we can see, we have optimized storage by ten times without any actual loss in data. For further details on optimizing storage using types and codecs, see our recent blog [Optimizing ClickHouse with Schemas and Codecs](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema).


## Improving time\-series query performance [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#improving-time-series-query-performance)


### Optimize ORDER BY keys [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#optimize-order-by-keys)


Before attempting other optimizations, users should optimize their [ordering key](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-cardinality/) to ensure ClickHouse produces the fastest possible results. Choosing the key right largely depends on the queries you’re going to run. Suppose most of our queries filter by `project` and `subproject` columns. In this case, its a good idea to add them to the ordering key \- as well as the `time` column since we query on time as well:



```

CREATE TABLE optimized_wikistat
(…)
ENGINE = MergeTree
ORDER BY (project, subproject, time)


```


Let’s now compare multiple queries to get an idea of how essential our ordering key expression is to performance. Note that we have also applied our previous data type and codec optimizations:




| **Query** | **Ordering Key** | |
| --- | --- | --- |
|  | **(time)** | **(project, subproject, time)** |
| ```  SELECT     project,     sum(hits) AS h FROM wikistat GROUP BY project ORDER BY h DESC LIMIT 10   ``` | [0\.518 sec ✎](https://sql.clickhouse.com?query_id=HPGEZK7USHGDUGTJTHJAYV) | [0\.258 sec ✎](https://sql.clickhouse.com?query_id=GFCCTYVJ3YVGMTOFXDQZJT) |
| ```  SELECT     subproject,     sum(hits) AS h FROM wikistat WHERE project = 'it' GROUP BY subproject ORDER BY h DESC LIMIT 10   ``` | [0\.67 sec ✎](https://sql.clickhouse.com?query_id=2Q8G2SWXOOSHHVVBQB8ND2) | [0\.025 sec ✎](https://sql.clickhouse.com?query_id=1G21SEVPJZM1XFRTPR6MVR) |
| ```  SELECT     toStartOfMonth(time) AS m,     sum(hits) AS h FROM wikistat WHERE (project = 'it') AND (subproject = 'zero') GROUP BY m ORDER BY m DESC LIMIT 10   ``` | [0\.65 sec ✎](https://sql.clickhouse.com?query_id=4TB6QY6HMELIW5PUWRNG4M) | [0\.014 sec ✎](https://sql.clickhouse.com?query_id=9EBNNA5MNGKSDJMNLGMCHB) |
| ```  SELECT     path,     sum(hits) AS h FROM wikistat WHERE (project = 'it') AND (subproject = 'zero') GROUP BY path ORDER BY h DESC LIMIT 10   ``` | [0\.148 sec ✎](https://sql.clickhouse.com?query_id=WW6JBMONCU5VKCKQXSYTFM) | [0\.010 sec ✎](https://sql.clickhouse.com?query_id=3EYNNE9LVWLHSAH2MD4N3Y) |


Note how we got a 2…40x performance increase by picking up a more appropriate ordering key. For further details on choosing a primary key, including how to decide the order of the columns, read our excellent guide [here](https://clickhouse.com/docs/en/guides/improving-query-performance/sparse-primary-indexes/sparse-primary-indexes-intro).


### Materialized views [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#materialized-views)


Another option is to use [materialized views](https://clickhouse.com/docs/en/sql-reference/statements/create/view/#materialized-view) to aggregate and store the results of popular queries. These results can be queried instead of the original table. Suppose the following query is executed quite often in our case:



```

SELECT
    path,
    SUM(hits) AS v
FROM wikistat
WHERE toStartOfMonth(time) = '2015-05-01'
GROUP BY path
ORDER BY v DESC
LIMIT 10

┌─path──────────────────┬────────v─┐
│ -                     │ 89742164 │
│ Angelsberg            │ 19191582 │
│ Ana_Sayfa             │  6376578 │
│ Academy_Awards        │  4901470 │
│ Accueil_(homonymie)   │  3810047 │
│ 2015_in_spaceflight   │  2077195 │
│ Albert_Einstein       │  1621175 │
│ 19_Kids_and_Counting  │  1432484 │
│ 2015_Nepal_earthquake │  1406457 │
│ Alive                 │  1390624 │
└───────────────────────┴──────────┘

10 rows in set. Elapsed: 1.016 sec. Processed 256.84 million rows, 10.17 GB (252.69 million rows/s., 10.01 GB/s.)

[✎](https://sql.clickhouse.com?query_id=WW6JBMONCU5VKCKQXSYTFM)

```


We can create the following materialized view:



```

CREATE MATERIALIZED VIEW blogs.wikistat_top
ENGINE = SummingMergeTree
ORDER BY (month, hits) POPULATE AS
SELECT
    path,
    toStartOfMonth(time) AS month,
    sum(hits) AS hits
FROM blogs.wikistat
GROUP BY
    path,
    month

0 rows in set. Elapsed: 8.589 sec. Processed 1.00 billion rows, 40.52 GB (116.43 million rows/s., 4.72 GB/s.)


```


Now we can query the materialized view instead of the original table:



```

SELECT
    path,
    hits
FROM wikistat_top
WHERE month = '2015-05-01'
ORDER BY hits DESC
LIMIT 10

┌─path──────────────────┬─────hits─┐
│ -                     │ 89742164 │
│ Angelsberg            │ 19191582 │
│ Ana_Sayfa             │  6376578 │
│ Academy_Awards        │  4901470 │
│ Accueil_(homonymie)   │  3810047 │
│ 2015_in_spaceflight   │  2077195 │
│ Albert_Einstein       │  1621175 │
│ 19_Kids_and_Counting  │  1432484 │
│ 2015_Nepal_earthquake │  1406457 │
│ Alive                 │  1390624 │
└───────────────────────┴──────────┘
10 rows in set. Elapsed: 0.005 sec. Processed 24.58 thousand rows, 935.16 KB (5.26 million rows/s., 200.31 MB/s.)

[✎](https://sql.clickhouse.com?query_id=PSZHGXKFFDGDRADCAMCF1Q)

```


Our performance improvement here is dramatic. We will publish a blog post on materialized views soon, so watch this space!


## Scaling time series [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#scaling-time-series)


ClickHouse is efficient in storage and queries and easily scalable to Petabytes, maintaining the same level of performance and simplicity. In a future post, we will explore techniques for scaling to almost 400 billion rows using the [full Wikistat dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/wikistat). We will show how you can scale in terms of storage and processing capacity using our Cloud service, which separates storage and compute and deals with this automatically, or by using a manual clustering solution.


## Summary [\#](/blog/working-with-time-series-data-and-functions-ClickHouse#summary)


In this post, we have shown how you can efficiently store and query time series data using the power of SQL and the performance of ClickHouse. Given this, you won’t need to install additional extensions or tools to collect and process time series, as ClickHouse has everything in place.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
