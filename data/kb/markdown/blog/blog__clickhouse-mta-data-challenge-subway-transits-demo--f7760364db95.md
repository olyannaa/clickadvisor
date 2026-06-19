# ClickHouse and the MTA Data Challenge


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse and the MTA Data Challenge

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96.png&w=96&q=75)[PME Team](/authors/pme-team)Oct 24, 2024 · 21 minutes readWe love [open data challenges](https://clickhouse.com/blog/clickhouse-1-trillion-row-challenge) at ClickHouse, so when we saw that MTA (Metropolitan Transportation Authority) had [announced such a challenge](https://new.mta.info/article/mta-open-data-challenge) on their website, we couldn’t resist the temptation to contribute. We’ve focused on the turnstile dataset allowing analysis of subway usage in NYC, making this available in our new playground where users can query the data for free.



> The MTA (Metropolitan Transportation Authority) operates public transportation systems in New York City, including subways, buses, and commuter rail services, serving millions of passengers daily. The MTA Open Data Challenge is a month\-long competition aimed at developers and data enthusiasts. MTA encourages participants to use their datasets to create projects that creatively leverage the data, whether through web apps, visualizations, or reports. Submissions must use at least one dataset from data.ny.gov, and will be judged on creativity, utility, execution, and transparency.


While the MTA challenge has 176 datasets to play around with, most of them are quite small, with only a few hundred rows. They still make excellent resources, but they aren’t really the volume of data to which ClickHouse is best suited.


ClickHouse is an OLAP database designed for scale, and we, therefore, wanted to find the largest dataset to explore! This happens to be the [turnstile dataset](https://data.ny.gov/browse?q=turnstile&sortBy=relevance), which contains 100 million rows over all the years. This dataset contains information on entry/exit values for turnstiles in New York City, thus allowing an analysis of the movement of people around the city. At first glance, this dataset seemed quite simple, but as we found out, it required significantly more effort to clean and provide in usable form than first expected.



> The dataset itself covers the years 2014 to 2022\. A (much cleaner) version of the turnstile data is available for more recent years. We’ve also loaded this dataset and provided example queries. In the interest of making all of the data available, however, we focus on the historical data in this blog.


In this post, we’ll explore the steps to load and clean this data to make it usable for further analysis so others can reproduce it in their own ClickHouse instance. This highlights some of the key features ClickHouse makes available for data engineering with many of the steps and queries reusable for other datasets.


![example_sql_clickhouse.png](/uploads/example_sql_clickhouse_6b6cac3cb8.png)
For those just interested in the final dataset, we’ve made it available in our new [ClickHouse playground](https://sql.clickhouse.com), where we’ve got more than 220 queries and 35 datasets for you [to try out!](https://sql.clickhouse.com/?query_id=HPN5AHXEHK1NM2NB9S3AV2) To contribute new queries and datasets, [visit the demo repository](https://github.com/ClickHouse/sql.clickhouse.com).



> All of the steps in this blog can be reproduced with [clickhouse\-local](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local), an easy\-to\-use version of ClickHouse that is ideal for developers who need to perform fast processing on local and remote files using SQL without having to install a full database server.


## Initial data exploration and load [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#initial-data-exploration-and-load)


To simplify loading, we’ve made the turnstile data (distributed as TSV files) available on a public bucket. We can explore the columns available with a simple S3 query. This relies on ClickHouse schema inference to infer the column types:



```
DESCRIBE TABLE s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/mta/*.tsv')
SETTINGS describe_compact_output = 1

┌─name───────────────────────────────────────────────────────┬─type────────────────────┐
│ C/A                                                    	 │ Nullable(String)    	   │
│ Unit                                                   	 │ Nullable(String)    	   │
│ SCP                                                    	 │ Nullable(String)    	   │
│ Station                                                	 │ Nullable(String)    	   │
│ Line Name                                              	 │ Nullable(String)    	   │
│ Division                                               	 │ Nullable(String)    	   │
│ Date                                                   	 │ Nullable(DateTime64(9)) │
│ Time                                                   	 │ Nullable(String)    	   │
│ Description                                            	 │ Nullable(String)    	   │
│ Entries                                                	 │ Nullable(Int64)     	   │
│ Exits                                                  	 │ Nullable(Int64)     	   │
└────────────────────────────────────────────────────────────┴─────────────────────────┘


11 rows in set. Elapsed: 0.309 sec.

```

If we sample the data and review the [dataset description](https://data.ny.gov/api/views/i55r-43gk/files/e348e3e7-9998-4e5e-926b-bdf04b62610e?download=true&filename=MTA_SubwayTurnstileUsageData2014_Overview.pdf), we can see that each row represents the entry and exit counts for a turnstile reported at a specific time. The description highlights these counts are reported periodically, so these statistics represent the previous period. Below, we query the data directly in S3 (in\-place):



```
SELECT *
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/mta/*.tsv')
LIMIT 1
FORMAT Vertical

Row 1:
──────
C/A:                                                        A002
Unit:                                                       R051
SCP:                                                        02-00-00
Station:                                                    LEXINGTON AVE
Line Name:                                                  NQR456
Division:                                                   BMT
Date:                                                       2014-12-31 00:00:00.000000000
Time:                                                       23:00:00
Description:                                                REGULAR
Entries:                                                    4943320
Exits                                                     : 1674736

1 rows in set. Elapsed: 1.113 sec.

```

For easier processing and to prevent repeated downloads of the data, we can load this data into a local table. To create this table from the inferred schema and load the data, we can use the following. 



```
CREATE TABLE subway_transits_2014_2022_raw
ENGINE = MergeTree
ORDER BY tuple() EMPTY
AS SELECT *
FROM s3('https://datasets-documentation.s3.eu-west-3.amazonaws.com/mta/*.tsv')

```

This creates an empty table using the schema. We’ll use this as a staging table for data exploration only and, for now, omit [an ordering key](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes): Loading this data becomes a simple `INSERT INTO SELECT`:



```
INSERT INTO subway_transits_2014_2022_raw
SETTINGS max_insert_threads = 16, parallel_distributed_insert_select = 2
SELECT *
FROM s3Cluster('default', 'https://datasets-documentation.s3.eu-west-3.amazonaws.com/mta/*.tsv')
SETTINGS max_insert_threads = 16, parallel_distributed_insert_select = 2

0 rows in set. Elapsed: 39.236 sec. Processed 94.88 million rows, 13.82 GB (2.42 million rows/s., 352.14 MB/s.)
Peak memory usage: 1.54 GiB.

SELECT count()
FROM subway_transits_2014_2022_raw

┌──count()─┐
│ 94875892 │ -- 94.88 million
└──────────┘

1 row in set. Elapsed: 0.002 sec.


```


> We’ve applied some simple optimizations to speed up this load, such as using the s3Cluster function. You can read more about these in the [Optimizing for S3 Insert and Read Performance guide](https://clickhouse.com:8443/docs/en/integrations/s3/performance)\*. The above timings (and subsequent) are from our sql.clickhouse.com environment, which consists of 3 nodes, each with 30vCPUs. Your performance will vary, but given the size of the dataset will heavily depend on network connection.


## Schema improvements [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#schema-improvements)


Examining the table schema reveals plenty of opportunities for optimization.



```
SHOW CREATE TABLE subway_transits_2014_2022_raw
CREATE TABLE subway_transits_2014_2022_raw
(
	`C/A` Nullable(String),
	`Unit` Nullable(String),
	`SCP` Nullable(String),
	`Station` Nullable(String),
	`Line Name` Nullable(String),
	`Division` Nullable(String),
	`Date` Nullable(DateTime64(9)),
	`Time` Nullable(String),
	`Description` Nullable(String),
	`Entries` Nullable(Int64),
	`Exits                                                 	` Nullable(Int64)
)
ENGINE = SharedMergeTree('/clickhouse/tables/{uuid}/{shard}', '{replica}')
ORDER BY tuple()

```

Aside from the column names being less than ideal (lowercase with no special chars is preferred), the Nullable type isn’t required. This [consumes additional space](https://clickhouse.com/docs/en/cloud/bestpractices/avoid-nullable-columns) to differentiate between a Null and empty value and should be avoided. Furthermore, our `Date` and `Time` should be combined into a `date_time` column \- ClickHouse has a rich set of [date time functions](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions) that enable a DateTime type to be queried with respect to time, date, or both.


A quick check of the [column descriptions for the data](https://data.ny.gov/api/views/ug6q-shqc/files/5fea1a03-cb1b-45af-b05f-a121019e949e?download=true&filename=MTA_SubwayTurnstileUsageData2015_DataDictionary.pdf) reveals some additional opportunities for optimization. The entries and exits cannot exceed an Int32, after which they wrap around (separate issue), and can only be positive. Most of the String columns are also low cardinality, something we can confirm with a quick query:



```
SELECT
    uniq(`C/A`),
    uniq(Unit),
    uniq(SCP),
    uniq(Station),
    uniq(`Line Name`),
    uniq(Division),
    uniq(Description)
FROM subway_transits_2014_2022_raw
FORMAT Vertical

Query id: c925aaa4-6302-41e4-9f1e-1ba88587c3bc

Row 1:
──────
uniq(C/A):         762
uniq(Unit):        476
uniq(SCP):         334
uniq(Station):     579
uniq(Line Name):   130
uniq(Division):    7
uniq(Description): 2

1 row in set. Elapsed: 0.959 sec. Processed 94.88 million rows, 10.27 GB (98.91 million rows/s., 10.71 GB/s.)
Peak memory usage: 461.18 MiB.

```

It therefore makes sense to make these a `LowCardinality(String)` type [which will lead to better compression and faster queries](https://clickhouse.com/docs/en/data-compression/compression-in-clickhouse)!


Anyone from NYC will also be familiar with the line naming system. The column `Line Name` denotes the lines available from the turnstile i.e.


“The train lines that stop at the station, such as 456”


![4523572781_c8f1c3a4b6_o.jpg](/uploads/4523572781_c8f1c3a4b6_o_711cf233fc.jpg)
456 thus represents the 4, 5 and 6 lines. Glancing over the data revealed these aren’t consistently ordered. For example, `456NQR` is the same as `NQR456`:

```
SELECT `Line Name`
FROM subway_transits_2014_2022_raw
WHERE (`Line Name` = 'NQR456') OR (`Line Name` = '456NQR')
LIMIT 1 BY `Line Name`

┌─Line Name─┐
│ NQR456	│
│ 456NQR	│
└───────────┘

2 rows in set. Elapsed: 0.059 sec. Processed 94.88 million rows, 1.20 GB (1.60 billion rows/s., 20.20 GB/s.)
Peak memory usage: 105.88 MiB.

```

To simplify future queries we tokenize this string into an `Array(LowCardinality(String))` and sort the values.


Finally, `station` and `date_time` seem like reasonable first choices for [our ordering key](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes).


Our table schema thus becomes:



```
CREATE TABLE subway_transits_2014_2022_v1
(
   `ca` LowCardinality(String),
   `unit` LowCardinality(String),
   `scp` LowCardinality(String),
   `station` LowCardinality(String),
   `line_names` Array(LowCardinality(String)),
   `division` LowCardinality(String),
   `date_time` DateTime32,
   `description` LowCardinality(String),
   `entries` UInt32,
   `exits` UInt32
)
ENGINE = MergeTree
ORDER BY (station, date_time)

```

We can load this data by reading from our earlier `subway_transits_2014_2022_raw` table, using a `SELECT` to transform the rows.



```
INSERT INTO subway_transits_2014_2022_v1 SELECT
	`C/A` AS ca,
	Unit AS unit,
	SCP AS scp,
	Station AS station,
	arraySort(ngrams(assumeNotNull(`Line Name`), 1)) AS line_names,
	Division AS division,
	parseDateTimeBestEffort(trimBoth(concat(CAST(Date, 'Date32'), ' ', Time))) AS date_time,
	Description AS description,
	Entries AS entries,
	`Exits                                                 	` AS exits
FROM subway_transits_2014_2022_raw
SETTINGS max_insert_threads = 16

0 rows in set. Elapsed: 4.235 sec. Processed 94.88 million rows, 14.54 GB (22.40 million rows/s., 3.43 GB/s.)

```

## Cleaning the MTA transit dataset [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#cleaning-the-mta-transit-dataset)


Let’s now go through the steps that we took to clean the data. We found a couple of major issues, which we’ll go through in turn.


### Challenge 1: cumulative values and outliers [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#challenge-1-cumulative-values-and-outliers)


MTA provides a longer form [description of the data](https://data.ny.gov/api/views/ug6q-shqc/files/29edbef3-268e-461d-95f1-374b1c8a6f9d?download=true&filename=MTA_SubwayTurnstileUsageData2015_Overview.pdf), which provides insight into some data quality issues and challenges. Not least, the `entries` and `exit` values are cumulative.


*\> Data is provided about every four hours for the cumulative register values for entries and exits for each turnstile, similar to odometer readings. The four\-hour intervals will differ from other stations due to the need for staggering to prevent flooding the system with audit readings all at once. Systemwide, stations have been set to begin audit transmittal between 00 to 03 hours, then every four hours after the first audit of the day. The number of people who entered or exited a turnstile in a period can be obtained by comparing it to an earlier reading.*


These cumulative values are challenging to use and would require queries to compute time ordered derivatives for every turnstile. We note that the 4 hour periodic delivery of data will make attributing usage of a station to specific periods still very imprecise. This is something we can't resolve, so counts below the granularity of this period are unlikely to be accurate.


These values also have some clear data quality issues:


*\> Turnstile audits are often not available every four hours, turnstiles sometimes count down instead of up, exit and entry counters periodically get reset, and the timestamps for audits vary between turnstiles. In addition, the data is 10 digits long and will roll over to zero on overflow.*


Ideally we'd like to compute the number of entries and exits for each row based on the difference to the previous time value for the turnstile. This requires us to reliably be able to identify a turnstile.


While turnstiles have an `scp` identifier, this is not unique across stations. Instead we can use a combination of the scp, ca (booth identifier at station) and unit(remote unit ID of the station) to identify a specific station.


To compute the number of entries and exits for each turnstile, requires a [window function](https://clickhouse.com/docs/en/sql-reference/window-functions). The following computes the columns `entries_change` and `exits_change` for each row.



```
WITH 1000 AS threshold_per_hour
SELECT
    *,
    any(date_time) OVER (PARTITION BY ca, unit, scp ORDER BY date_time ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS p_date_time,
    any(entries) OVER (PARTITION BY ca, unit, scp ORDER BY date_time ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS p_entries,
    any(exits) OVER (PARTITION BY ca, unit, scp ORDER BY date_time ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS p_exits,
    dateDiff('hour', p_date_time, date_time) AS hours,
    if((entries < p_entries) OR (((entries - p_entries) / if(hours > 0, hours, 1)) > threshold_per_hour), 0, entries - p_entries) AS entries_change,
    if((exits < p_exits) OR (((exits - p_exits) / if(hours > 0, hours, 1)) > threshold_per_hour), 0, exits - p_exits) AS exits_change
FROM subway_transits_2014_2022_v1
ORDER BY
    ca ASC,
    unit ASC,
    scp ASC,
    date_time ASC

```

A few important points for the query:


- We order by `ca`, `unit`, `scp`, and `date_time` (ascending). This ensures the rows for each turnstile are processed together in increasing time order, allowing us to compute the delta.
- The function creates a window for each turnstile using `PARTITION BY ca, unit, scp`. Within each window the data is again ordered by increasing time. The `ROWS BETWEEN 1 PRECEDING AND CURRENT ROW` clause is used to add the columns `p_entries` and `p_exits`. These contain the previous entries and exit values for each row. The time from the previous row is captured in `p_date_time`.
- The columns `entries_change` and `exits_change` contain the delta between the previous and current values for the entries and exits, respectively. Importantly, if the change is negative, we return a value of 0, assuming this represents a rollover. Additionally, an analysis of the data revealed **significant outlier values** where the change would be unrealistically high e.g. 10,000 people used a turnstile in an hour. If the change exceeds a threshold of N per hour (1000\), we also return 0 to filter out these values. Choosing a value threshold was based on the number of realistic people who could pass through a turnstile in our hour ([10\-15 people per minute](https://www.turnstiles.us/turnstile-passthrough-rates-how-many-people-can-pass-per-minute/)). This approach is imperfect with more sophisticated approaches which consider historical trends possible.


### Challenge 2: missing/inconsistent station names [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#challenge-2-missinginconsistent-station-names)


While the datasets for each year use the same schema, the [dataset for 2022](https://data.ny.gov/Transportation/MTA-Subway-Turnstile-Usage-Data-2022/k7j9-jnct/about_data) is missing station names.



```
SELECT toYear(date_time) AS year
FROM mta.subway_transits_2014_2022_v1
WHERE station = ''
GROUP BY year

   ┌─year─┐
1. │ 2022 │
   └──────┘

1 row in set. Elapsed: 0.016 sec. Processed 10.98 million rows, 54.90 MB (678.86 million rows/s., 3.39 GB/s.)
Peak memory usage: 98.99 MiB.

```

To make this dataset more usable, we would ideally populate the station name for 2022 based on a unique turnstile id to station name mapping (populated from earlier data).


However, if we analyze the station names, we can see they are rarely consistent, even for the same turnstile! For example, inconsistent use of `AV` and `AVE` for “avenue” appears to result in multiple entries for the same station.



```
SELECT DISTINCT station
FROM subway_transits_2014_2022_v1
WHERE station LIKE '%AV%'
ORDER BY station ASC
LIMIT 10
FORMAT PrettyCompactMonoBlock

┌─station──────┐
│ 1 AV         │
│ 1 AVE        │
│ 138 ST-3 AVE │
│ 14 ST-6 AVE  │
│ 149 ST-3 AVE │
│ 18 AV        │
│ 18 AVE       │
│ 2 AV         │
│ 2 AVE        │
│ 20 AV        │
└──────────────┘

10 rows in set. Elapsed: 0.024 sec. Processed 36.20 million rows, 41.62 MB (1.53 billion rows/s., 1.75 GB/s.)
Peak memory usage: 26.68 MiB.

```

If we can establish a turnstile to station name mapping, we can address simple issues like this by just picking one of the names consistently (e.g. always the longest) and remapping all of the data. Note this won't address more complex mappings, such as mapping the names '42 ST\-TIMES SQ', and 'TIMES SQ\-42 ST' to "TIMES SQ". We can defer these to query time for now.


To hold our mapping, we can use a dictionary. This in\-memory structure will allow a station name lookup by a tuple of `(ca, unit, scp)` . We populate this dictionary with the query shown below, selecting the longest station name for each turnstile. The latter is achieved by producing a distinct list of station names assigned to each `(ca, unit, scp)` via the `groupArrayDistinct` function. This is then sorted by length, with the first (longest) entry selected.



```
CREATE DICTIONARY station_names
(
`ca` String,
`unit` String,
`scp` String,
`station_name` String
)
PRIMARY KEY (ca, unit, scp)
SOURCE(CLICKHOUSE(QUERY $query$
   SELECT
       ca,
       unit,
       scp,
       arrayReverseSort(station -> length(station), groupArrayDistinct(station))[1] AS station_name
   FROM subway_transits_2014_2022_v1
   WHERE station != ''
   GROUP BY
       ca,
       unit,
       scp
$query$))
LIFETIME(MIN 0 MAX 0)
LAYOUT(complex_key_hashed())

```


> For more details on dictionaries, including the types available and how to configure them, see the Dictionaries documentation.


We can efficiently retrieve a specific station name using the dictGet\` function. For example:



```
SELECT dictGet(station_names, 'station_name', ('R148', 'R033', '01-04-01'))

┌─name───────────┐
│ 42 ST-TIMES SQ │
└────────────────┘

1 row in set. Elapsed: 0.001 sec.

```


> Note the first time the dictionary is invoked, the request might be slow depending on whether the data is loaded eagerly on creation or lazily on the first request. This can be [configured using dictionaries\_lazy\_load](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#dictionaries_lazy_load).


### Combining solutions for final data [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#combining-solutions-for-final-data)


We can now combine our window function and dictionary lookup to produce a final version of the data. The idea here is simple: execute a query using the window function and `dictGet` against v1 of our table, inserting the results into a new table. Our final table schema:



```
CREATE TABLE mta.subway_transits_2014_2022_v2
(
    `ca` LowCardinality(String),
    `unit` LowCardinality(String),
    `scp` LowCardinality(String),
    `line_names` Array(LowCardinality(String)),
    `division` LowCardinality(String),
    `date_time` DateTime,
    `description` LowCardinality(String),
    `entries` UInt32,
    `exits` UInt32,
    `station` LowCardinality(String),
    `entries_change` UInt32,
    `exits_change` UInt32
)
ENGINE = MergeTree
ORDER BY (ca, unit, scp, date_time)

```

Using an `INSERT INTO SELECT`:



```
INSERT INTO mta.subway_transits_2014_2022_v2 WITH 2000 AS threshold_per_hour  SELECT
   ca, unit, scp, line_names, division, date_time, description, entries, exits,
   dictGet(station_names, 'station_name', (ca, unit, scp)) as station,
   entries_change, exits_change
FROM
(
  SELECT
       *,
       any(date_time) OVER (PARTITION BY ca, unit, scp ORDER BY date_time ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS p_date_time,
       any(entries) OVER (PARTITION BY ca, unit, scp ORDER BY date_time ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS p_entries,
       any(exits) OVER (PARTITION BY ca, unit, scp ORDER BY date_time ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS p_exits,
       dateDiff('hour', p_date_time, date_time) AS hours,
       if((entries < p_entries) OR (((entries - p_entries) / if(hours > 0, hours, 1)) > threshold_per_hour), 0, entries - p_entries) AS entries_change,
       if((exits < p_exits) OR (((exits - p_exits) / if(hours > 0, hours, 1)) > threshold_per_hour), 0, exits - p_exits) AS exits_change
   FROM subway_transits_2014_2022_v1
   ORDER BY
       ca ASC,
       unit ASC,
       scp ASC,
       date_time ASC
  
) SETTINGS max_insert_threads=16

0 rows in set. Elapsed: 24.305 sec. Processed 94.88 million rows, 2.76 GB (3.90 million rows/s., 113.67 MB/s.)


```

Our final table:



```
SELECT *
FROM mta.subway_transits_2014_2022_v2
LIMIT 1
FORMAT Vertical

Row 1:
──────
ca:             A002
unit:           R051
scp:            02-00-00
line_names:     ['4','5','6','N','Q','R']
division:       BMT
date_time:      2014-01-02 03:00:00
description:    REGULAR
entries:        4469306
exits:          1523801
station:        LEXINGTON AVE
entries_change: 0
exits_change:   0

1 rows in set. Elapsed: 0.005 sec.

```

## Sample queries for the MTA transit dataset [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#sample-queries-for-the-mta-transit-dataset)


You can run the following queries in the ClickHouse playground. We’ve provided some default charts for each query to get you started.


**If you’d like to suggest further queries or improvements, for the MTA dataset or others, please don’t hesitate to reach out and raise an issue on the [demo’s repo](https://github.com/ClickHouse/sql.clickhouse.com).**


Lets first confirm the most popular stations align with official figures. For example, we’ll use 2018:



```


SELECT
    station,
    sum(entries_change) AS total_entries,
    formatReadableQuantity(total_entries) AS total_entries_read
FROM mta.subway_transits_2014_2022_v2
WHERE toYear(date_time) = '2018'
GROUP BY station
ORDER BY sum(entries_change) DESC
LIMIT 10

 [✎](https://sql.clickhouse.com/?query_id=4MGH76GE6QN6WA6H8TCYKR&run_query=true&tab=charts)

```


![query_1.png](/uploads/query_1_cb5c5d11bc.png)
The quality of our results is impacted by both the data, which is extremely noisy, and the method we used to remove outliers. However, these do appear to align with the [high\-level numbers reported by MTA](https://new.mta.info/agency/new-york-city-transit/subway-bus-ridership-2022). Note also that some station entries, such as Times Square, have separate entry points in our data, i.e., '42 ST\-TIMES SQ' and 'TIMES SQ\-42 ST' to'TIMES SQ\`. We leave this cleanup exercise as a to\-do and currently resolve using conditionals at query time.


If we examine the traffic for the top 10 stations over the full period, the decline as a result of COVID is obvious:



```


SELECT
    station,
    toYear(date_time) AS year,
    sum(entries_change) AS total_entries
FROM mta.subway_transits_2014_2022_v2
WHERE station IN (
    SELECT station
    FROM mta.subway_transits_2014_2022_v2
    GROUP BY station
    ORDER BY sum(entries_change) DESC
    LIMIT 10
)
GROUP BY
    year,
    station
ORDER BY year ASC

 [✎](https://sql.clickhouse.com/?query_id=KADCUSBZG3UWVV2N4QUJXW&run_query=true&tab=charts)

```


![query_2.png](/uploads/query_2_cd8cd4544f.png)
Despite our efforts, this data still remains very noisy. There are obvious anomalies which require further efforts to remove \- we welcome suggestions on approaches. Conversely, the transit data from 2022 appears to be much more reliable and of higher quality. We’ve also loaded this into the `transit_data` table and provided some example queries.


Using this data, we can observe daily commuter patterns to show which stations are busy during which rush hour:



```


SELECT
    station_complex,
    toHour(hour_of_day) AS hour,
    CAST(avg(total_entries), 'UInt64') AS avg_entries
FROM
(
    SELECT
        toStartOfHour(transit_timestamp) AS hour_of_day,
        station_complex,
        sum(ridership) AS total_entries
    FROM mta.transit_data
    WHERE toDayOfWeek(transit_timestamp) <= 5
    GROUP BY
        station_complex,
        hour_of_day
)
GROUP BY
    hour,
    station_complex
ORDER BY
    hour ASC,
    avg_entries DESC
LIMIT 3 BY hour

 [✎](https://sql.clickhouse.com/?query_id=HPN5AHXEHK1NM2NB9S3AV2&run_query=true&tab=charts)

```


![query_3.png](/uploads/query_3_571e11865d.png)
We can also easily compare weekend vs weekday traffic. This highlights some obvious times of the year e.g. 4th July, when commuter traffic is significantly lower.



```


SELECT
    toStartOfWeek(transit_timestamp) AS week,
    'weekday' AS period,
    sum(ridership) AS total
FROM mta.transit_data
WHERE toDayOfWeek(transit_timestamp) <= 5
GROUP BY week
ORDER BY week ASC
UNION ALL
SELECT
    toStartOfWeek(transit_timestamp) AS week,
    'weekend' AS period,
    sum(ridership) AS total
FROM mta.transit_data
WHERE toDayOfWeek(transit_timestamp) > 5
GROUP BY week
ORDER BY week ASC

 [✎](https://sql.clickhouse.com/?query_id=STHDUVXOFZFGF2JCHJGB5Y&run_query=true&tab=charts)

```


![query_4.png](/uploads/query_4_07bce635ab.png)
## Conclusion [\#](/blog/clickhouse-mta-data-challenge-subway-transits-demo#conclusion)


We had fun working on the MTA challenge (at least as much fun as you can have when cleaning data!) and hope that our work has made it easier for everyone to do some fun analysis of the data.


We’d love it if you shared any queries (and charts) you came up with on the [demo repository](https://github.com/ClickHouse/sql.clickhouse.com).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
