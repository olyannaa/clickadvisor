# ClickHouse projections now behave like true secondary indexes


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse projections now behave like true secondary indexes

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)Jan 13, 2026 · 8 minutes read
> **TL;DR**  
>   
> ClickHouse tables once had only *one* primary index.  
> Now they can have **many**, implemented as lightweight projections that behave like primary indexes, without duplicating data.


**Prefer a quick walkthrough?**  

Watch Mark explain how projections act as secondary indexes in ClickHouse:



  

## Why projections matter [\#](/blog/projections-secondary-indices#why-projections-matter)


[Primary indexes](https://clickhouse.com/docs/primary-indexes) are the most important mechanism ClickHouse uses to speed up filtered queries. By storing rows on disk in the order of the table’s sorting key, the engine maintains a sparse index that can quickly locate the relevant ranges of data. But because this index depends on the physical sort order of the table, **each table can have only one primary index**.


To accelerate queries whose filters do not align with that single index, ClickHouse offers [**projections**](https://clickhouse.com/docs/sql-reference/statements/alter/projection) \- automatically maintained, hidden table copies stored in a different sort order, and therefore with a different primary index. These alternative layouts can speed up queries that benefit from those orderings. The downside, historically, was storage cost: **projections duplicated the base table’s data on disk**.


## Lightweight projections as secondary indexes [\#](/blog/projections-secondary-indices#lightweight-projections-as-secondary-indexes)


Since release **25\.6**, however, ClickHouse can create much more lightweight [projections that behave like a **secondary index**](https://clickhouse.com/blog/clickhouse-release-25-06#filtering-by-multiple-projections) without duplicating full rows. Instead of storing complete data copies, they store only their sorting key plus a [\_part\_offset](https://clickhouse.com/docs/data-modeling/projections#smarter_storage_with_part_offset) pointer back into the base table, greatly reducing storage overhead.


When applicable, [ClickHouse uses such a projection’s primary index like a secondary index to locate matching rows](https://clickhouse.com/blog/clickhouse-release-25-06#smarter-storage-with-_part_offset), while still reading the actual row data from the base table. Multiple lightweight projections can work together, so a query with several filters can take advantage of every applicable projection, and if one of the filters also matches the base table’s primary index, **that index participates as well**.


## From part\-level to granule\-level pruning [\#](/blog/projections-secondary-indices#from-part-level-to-granule-level-pruning)


Until now, this mechanism could only prune entire parts; **granule\-level pruning** was not supported.


With this release, \_part\_offset\-based projections now behave like true secondary indexes with **granule\-level pruning**, enabling much finer filtering and dramatically faster queries.


## Example: combining multiple projection indexes [\#](/blog/projections-secondary-indices#example-combining-multiple-projection-indexes)


To demonstrate this, we’ll again use [the UK price paid dataset](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid), this time defining the table with two lightweight \_part\_offset\-based projections: by\_time and by\_town:



```

```
1CREATE OR REPLACE TABLE uk.uk_price_paid_with_proj
2(
3    price UInt32,
4    date Date,
5    postcode1 LowCardinality(String),
6    postcode2 LowCardinality(String),
7    type Enum8(
8      'terraced' = 1, 'semi-detached' = 2, 'detached' = 3, 'flat' = 4, 'other' = 0),
9    is_new UInt8,
10    duration Enum8('freehold' = 1, 'leasehold' = 2, 'unknown' = 0),
11    addr1 String,
12    addr2 String,
13    street LowCardinality(String),
14    locality LowCardinality(String),
15    town LowCardinality(String),
16    district LowCardinality(String),
17    county LowCardinality(String),
18    PROJECTION by_time (
19        SELECT _part_offset ORDER BY date
20    ),
21    PROJECTION by_town (
22        SELECT _part_offset ORDER BY town
23    )
24)
25ENGINE = MergeTree
26ORDER BY (postcode1, postcode2, addr1, addr2);
```

```

Then we load the data using the instructions [here](https://clickhouse.com/docs/getting-started/example-datasets/uk-price-paid).


The diagram below sketches the base table and its two lightweight \_part\_offset\-based projections:


![image6.png](/uploads/image6_c12f1d6103.png)
① The base table is sorted by (postcode1, postcode2, addr1, addr2\). This defines its primary index, making queries that filter by those columns fast and efficient.


② The by\_time and ③ by\_town projections store only their sorting key plus \_part\_offset, pointing back into the base table and greatly reducing data duplication. Their primary indexes act as secondary indexes for the base table, speeding up queries that filter on date and/or town.


*We benchmarked this on an AWS m6i.8xlarge EC2 instance (32 cores, 128 GB RAM) with a gp3 EBS volume (16k IOPS, 1000 MiB/s max throughput).*


We will run a query filtering on the date and town columns. Note that these columns are not part of the base table’s primary key.


First, we run the query with projection support disabled to get a baseline performance. Note that we disabled the [query condition cache](https://clickhouse.com/blog/introducing-the-clickhouse-query-condition-cache) and [PREWHERE](https://clickhouse.com/docs/optimize/prewhere) to fully isolate index\-based data pruning:



```

```
1SELECT *
2FROM uk.uk_price_paid_with_proj
3WHERE (date = '2008-09-26') AND (town = 'BARNARD CASTLE')
4FORMAT Null
5SETTINGS
6    use_query_condition_cache = 0,
7    optimize_move_to_prewhere = 0,
8    optimize_use_projections= 0;
```

```

The fastest of three runs finished in **0\.077 seconds**:



```
0 rows in set. Elapsed: 0.084 sec. Processed 30.73 million rows, 1.29 GB (363.92 million rows/s., 15.26 GB/s.)
Peak memory usage: 129.07 MiB.

0 rows in set. Elapsed: 0.076 sec. Processed 30.73 million rows, 1.29 GB (406.96 million rows/s., 17.07 GB/s.)
Peak memory usage: 129.29 MiB.

0 rows in set. Elapsed: 0.077 sec. Processed 30.73 million rows, 1.29 GB (398.51 million rows/s., 16.71 GB/s.)
Peak memory usage: 129.27 MiB.

```

Note that it was a full table scan, reading the whole table (\~30 million rows)


Now we run the query with enabled projection support:



```

```
1SELECT *
2FROM uk.uk_price_paid_with_proj
3WHERE (date = '2008-09-26') AND (town = 'BARNARD CASTLE')
4FORMAT Null
5SETTINGS
6    use_query_condition_cache = 0,
7    optimize_move_to_prewhere = 0,
8    optimize_use_projections= 1; -- default value
```

```

The fastest of three runs finished in **0\.010 seconds**:



```
0 rows in set. Elapsed: 0.010 sec. Processed 16.38 thousand rows, 644.86 KB (1.60 million rows/s., 63.06 MB/s.)
Peak memory usage: 4.89 MiB.

0 rows in set. Elapsed: 0.010 sec. Processed 16.38 thousand rows, 644.86 KB (1.69 million rows/s., 66.36 MB/s.)
Peak memory usage: 4.88 MiB.

0 rows in set. Elapsed: 0.011 sec. Processed 16.38 thousand rows, 644.86 KB (1.54 million rows/s., 60.57 MB/s.)
Peak memory usage: 4.89 MiB.

```

The result: **0\.077 s vs. 0\.010 s — roughly a 90% speedup.**


Also note that this time only \~16k rows instead of all \~30 million rows got scanned.


Via EXPLAIN we can see that ClickHouse is using the primary indexes of *both* projections as secondary indexes to prune base table granules:



```

```
1EXPLAIN projections = 1
2SELECT *
3FROM uk.uk_price_paid_with_proj
4WHERE (date = '2008-09-26') AND (town = 'BARNARD CASTLE')
5SETTINGS
6    use_query_condition_cache = 0,
7    optimize_move_to_prewhere = 0,
8    optimize_use_projections= 1; -- default value
```

```


```
    ┌─explain────────────────────────────────────────────────────────────┐
 1. │ Expression ((Project names + Projection))                          │
 2. │   Filter ((WHERE + Change column names to column identifiers))     │
 3. │     ReadFromMergeTree (uk.uk_price_paid_with_proj)                 │
 4. │     Projections:                                                   │
 5. │       Name: by_time                                                │
 6. │         Description: Projection has been analyzed...               │
 7. │         Condition: (date in [14148, 14148])                        │
 8. │         Search Algorithm: binary search                            │
 9. │         Parts: 5                                                   │
10. │         Marks: 7                                                   │
11. │         Ranges: 5                                                  │
12. │         Rows: 57344                                                │
13. │         Filtered Parts: 0                                          │
14. │       Name: by_town                                                │
15. │         Description: Projection has been analyzed...               │
16. │         Condition: (town in ['BARNARD CASTLE', 'BARNARD CASTLE'])  │
17. │         Search Algorithm: binary search                            │
18. │         Parts: 5                                                   │
19. │         Marks: 5                                                   │
20. │         Ranges: 5                                                  │
21. │         Rows: 40960                                                │
22. │         Filtered Parts: 0                                          │
    └────────────────────────────────────────────────────────────────────┘                     

```

Row 10 of the EXPLAIN output shows that the **by\_time** projection (specifically its primary index) first narrows the search to **7 granules** (“Marks”). Since each granule contains 8,192 rows, this corresponds to **7 × 8192 \= 57,344 rows** to scan (as shown in row 12\). Those 7 granules lie across **5 data parts** (row 9\), so the engine would need to read **5 corresponding data ranges (row 11\)**.


Then, starting at row 14, the **by\_town** projection’s primary index is applied. It filters out 2 of the 7 granules previously selected by the by\_time projection. The final result: the engine needs to scan **5 granules**, located in **5 data ranges** across **5 parts** of the base table, because those granules may contain rows matching the query’s time and town predicate.


Two new settings are introduced to control this optimization:


- max\_projection\_rows\_to\_use\_projection\_index: If the estimated number of rows to read from the projection is \<\= this value, projection index can be applied.
- min\_table\_rows\_to\_use\_projection\_index: If the estimated number of rows to read from the table is \>\= this value, projection index will be considered.


## A cleaner syntax in 26\.1 [\#](/blog/projections-secondary-indices#a-cleaner-syntax-in-261)


Starting with ClickHouse 26\.1, defining these lightweight \_part\_offset projections becomes even simpler.


Instead of writing:



```

```
1PROJECTION by_time (
2    SELECT _part_offset ORDER BY date
3),
4PROJECTION by_town (
5    SELECT _part_offset ORDER BY town
6)
```

```

You can now define them using a more compact syntax:



```

```
1PROJECTION by_time INDEX date TYPE basic,
2PROJECTION by_town INDEX town TYPE basic
```

```

This syntax expresses the same idea: we define a projection whose primary index behaves like a secondary index on the specified column.


Functionally, nothing changes; the projections still store only the sorting key and \_part\_offset, and they still participate in granule\-level pruning exactly as described above.


## Key takeaway [\#](/blog/projections-secondary-indices#key-takeaway)


ClickHouse tables once had only *one* primary index.


Now they can have **many**, each behaving like a primary index, and ClickHouse will use *all of them* when your query has multiple filters.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
