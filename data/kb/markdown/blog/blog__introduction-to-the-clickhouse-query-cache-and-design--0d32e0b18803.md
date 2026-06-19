# Introducing the ClickHouse Query Cache


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Introducing the ClickHouse Query Cache

![](/_next/image?url=%2Fuploads%2Frobert_schulze_fc3979ae99.png&w=96&q=75)[Robert Schulze](/authors/robert-schulze)Feb 9, 2023 · 12 minutes read![Cache2.png](/uploads/Cache2_1bcf1b8ff3.png)
To achieve maximum performance, analytical databases optimize every step of their internal data storage and processing pipeline. But the best kind of work performed by a database is work that is not done at all! Caching is an especially popular technique for avoiding unnecessary work by storing the results of earlier computation or remote data, which is expensive to access. ClickHouse uses caching [extensively](https://clickhouse.com/docs/en/operations/caches/), for example, to cache DNS records, local and remote (S3\) data, inferred schemas, compiled queries, and regular expressions. In today's blog post, we introduce the newest member of ClickHouse's cache family, the [query cache](https://clickhouse.com/docs/en/operations/query-cache/), which was recently [added with v23\.1](https://github.com/ClickHouse/ClickHouse/pull/43797) as an experimental preview feature.


## The Query Cache [\#](/blog/introduction-to-the-clickhouse-query-cache-and-design#the-query-cache)


The query cache is based on the idea that sometimes there are situations where it is okay to cache the result of expensive `SELECT` queries such that further executions of the same queries can be served directly from the cache. Depending on the type of queries, this can dramatically reduce the latency and resource consumption of the ClickHouse server. As an example, consider a data visualization tool like Grafana or Apache Superset, which displays a report of aggregated sales figures for the last 24 hours. In most cases, sales numbers within a day will change rather slowly, and we can afford to refresh the report only (for example) every three hours. Starting with ClickHouse v23\.1, `SELECT` queries can be provided with a "time\-to\-live" during which the server will only compute the first execution of the query, and further executions are answered without further computation directly from the cache.


After this brief introduction, let's give the query cache a try. For this, we will use the [GitHub Events](https://ghe.clickhouse.tech/) dataset, which contains all events on the GitHub platform since 2011, comprising 3\.1 billion rows in total. If you want to follow along, please make sure to have the dataset imported into ClickHouse using the [import instructions](https://ghe.clickhouse.tech/#download-the-dataset).


Since the query cache is still experimental, we first need to enable it. This step will become obsolete once the query cache is GA.



```

SET allow_experimental_query_cache = true


```


As an example for an expensive query, we now compute the ["repositories with the most stars over one day"](https://ghe.clickhouse.tech/#repositories-with-the-most-stars-over-one-day). On my 32\-core server, this query takes about 8 seconds to complete:



```

SELECT
    repo_name,
    toDate(created_at) AS day,
    count() AS stars
FROM github_events
WHERE event_type = 'WatchEvent'
GROUP BY
    repo_name,
    day
ORDER BY count() DESC
LIMIT 1 BY repo_name
LIMIT 50


┌─repo_name──────────────────────────────────────┬────────day─┬─stars─┐
│ 996icu/996.ICU                                 │ 2019-03-28 │ 76056 │
│ M4cs/BabySploit                                │ 2019-09-08 │ 46985 │
│ x64dbg/x64dbg                                  │ 2018-01-06 │ 26459 │
│ [...]                                          │ [...]      │ [...] │
└────────────────────────────────────────────────┴────────────┴───────┘


50 rows in set. Elapsed: 8.998 sec. Processed 232.12 million rows, 2.73 GB (25.80 million rows/s., 303.90 MB/s.)


```


To enable caching for a query, run it with the setting [`use_query_cache`](https://clickhouse.com/docs/en/operations/settings/settings#use-query-cache). The query cache uses a default time\-to\-live (TTL) of 60 seconds for query results. This timeout works just fine for the purpose of this example, but if needed, a different TTL can be specified using setting [`query_cache_ttl`](https://clickhouse.com/docs/en/operations/settings/settings#query-cache-ttl), either at query level (`SELECT ... SETTINGS query_cache_ttl = 300`) or at session level (`SET query_cache_ttl = 300`).



```

SELECT
    repo_name,
    toDate(created_at) AS day,
    count() AS stars
FROM github_events
WHERE event_type = 'WatchEvent'
GROUP BY
    repo_name,
    day
ORDER BY count() DESC
LIMIT 1 BY repo_name
LIMIT 50
SETTINGS use_query_cache = true


┌─repo_name──────────────────────────────────────┬────────day─┬─stars─┐
│ 996icu/996.ICU                                 │ 2019-03-28 │ 76056 │
│ [...]                                          │ [...]      │ [...] │
└────────────────────────────────────────────────┴────────────┴───────┘


50 rows in set. Elapsed: 8.577 sec. Processed 232.12 million rows, 2.73 GB (27.06 million rows/s., 318.81 MB/s.)


```


The first run of the query with `SETTINGS use_query_result_cache = true` stores the query results in the query cache. Subsequent executions of the same query (also with setting `use_query_cache = true`) and within the query time\-to\-live will read the previously computed result from the cache and return it immediately. Let's run the query again:



```

SELECT
    repo_name,
    toDate(created_at) AS day,
    count() AS stars
FROM github_events
WHERE event_type = 'WatchEvent'
GROUP BY
    repo_name,
    day
ORDER BY count() DESC
LIMIT 1 BY repo_name
LIMIT 50
SETTINGS use_query_cache = true


┌─repo_name──────────────────────────────────────┬────────day─┬─stars─┐
│ 996icu/996.ICU                                 │ 2019-03-28 │ 76056 │
│ [...]                                          │ [...]      │ [...] │
└────────────────────────────────────────────────┴────────────┴───────┘


50 rows in set. Elapsed: 8.451 sec. Processed 232.12 million rows, 2.73 GB (27.47 million rows/s., 323.56 MB/s.)


```


To our surprise, the second execution of the query took more than 8 seconds again. Apparently, the query cache was not used. Let's dig a bit deeper to understand what happened. To that end, we first check the system table `system.query_cache` to find out which query results are stored in the cache.



```

SELECT *
FROM system.query_cache

Ok.

0 rows in set. Elapsed: 0.001 sec. 


```


The query cache is indeed empty! Running the query again after executing `SET send_logs_level = 'trace'` quickly points to the issue.



```

2023.01.29 12:15:26.592519 [ 1371064 ] {a645c5b7-09a2-456c-bc8b-c506828d3b69}  QueryCache: Skipped insert (query result too big), new_entry_size_in_bytes: 1328640, new_entry_size_in_rows: 50, query: SELECT repo_name, toDate(created_at) AS day, count() AS stars FROM github_events WHERE event_type = 'WatchEvent' GROUP BY repo_name, day ORDER BY count() DESC LIMIT 1 BY repo_name LIMIT 50 SETTINGS
[...]
2023.01.29 12:15:40.697761 [ 1373583 ] {af02656c-e3e4-41c9-8f48-b8a1db145841}  QueryCache: No entry found for query SELECT repo_name, toDate(created_at) AS day, count() AS stars FROM github_events WHERE event_type = 'WatchEvent' GROUP BY repo_name, day ORDER BY count() DESC LIMIT 1 BY repo_name LIMIT 50 SETTINGS


```


A cache entry would be at least 1328640 bytes (\= ca. 1\.26 MiB) in size, whereas the default maximum cache entry size is 1048576 bytes (\= 1 MiB). Therefore, the cache considered the query result too big by a narrow margin and did not store it. Fortunately, we can change the size threshold. It is currently available as a server\-level setting in ClickHouse's server configuration file:



```
<query_cache>
    <size>1073741824</size>
    <max_entries>1024</max_entries>
    <max_entry_size>1048576</max_entry_size>
    <max_entry_records>30000000</max_entry_records>
</query_cache>

```

For the purpose of demonstration, let's change the maximum cache entry size in bytes, i.e., `max_entry_size`, from 1 MiB (\= `1'048'576` bytes) to the total query cache size of 1 GiB (\= `1'073'741'824` bytes). The new settings take effect after the server restarts. As you can see, we could configure the maximum total cache size in bytes, the maximum number of cache entries, and the maximum number of records per cache entry in the same manner.


If we run our query again, we see that the second invocation is served from the cache and returns immediately.



```

SELECT
    repo_name,
    toDate(created_at) AS day,
    count() AS stars
FROM github_events
WHERE event_type = 'WatchEvent'
GROUP BY
    repo_name,
    day
ORDER BY count() DESC
LIMIT 1 BY repo_name
LIMIT 50
SETTINGS use_query_cache = true


┌─repo_name──────────────────────────────────────┬────────day─┬─stars─┐
│ 996icu/996.ICU                                 │ 2019-03-28 │ 76056 │
│ [...]                                          │ [...]      │ [...] │
└────────────────────────────────────────────────┴────────────┴───────┘


50 rows in set. Elapsed: 0.04 sec.


```


## Using logs and settings [\#](/blog/introduction-to-the-clickhouse-query-cache-and-design#using-logs-and-settings)


We can also investigate the query log for query cache hits and misses and look at `system.query_cache` again:



```

SELECT                                                                                                                   
    query,                                                                                                               
    ProfileEvents['QueryCacheHits']                                                                                
FROM system.query_log                                                                                                                                                                                            
WHERE (type = 'QueryFinish') AND (query LIKE '%github_events%')

[...]

Row 8:                                              
──────                                              
query:                                               
SELECT                                             
    repo_name,                                      
    toDate(created_at) AS day,                                                                          
    count() AS stars                                
FROM github_events                                  
WHERE event_type = 'WatchEvent'                                                                         
GROUP BY                                            
    repo_name,                                      
    day                                             
ORDER BY count() DESC                               
LIMIT 1 BY repo_name                                
LIMIT 50                                            
SETTINGS use_query_cache = true                                                  
arrayElement(ProfileEvents, 'QueryCacheHits'): 1    

SELECT * FROM system.query_cache

Row 1:
──────
key_hash:    SELECT repo_name, toDate(created_at) AS day, count() AS stars FROM github_events WHERE event_type = 'WatchEvent' GROUP BY repo_name, day ORDER BY count() DESC LIMIT 1 BY repo_name LIMIT 50 SETTINGS
expires_at:  2023-01-29 17:55:29
stale:       1
shared:      0
result_size: 1328640

1 row in set. Elapsed: 0.005 sec.


```


As we can see, `system.query_log` now also shows an entry for our query. However, because the time passed since the query result was cached is bigger than the cache entry time\-to\-live (60 seconds by default), the entry is marked "stale". This means that further runs of the query will not use the cached query result but refresh the cache entry instead. Also, note that the `SETTINGS` clause provided with the query is only shown partially. This is caused by an internal pruning of all query\-cache\-related settings before the query is used as a key for the query cache. This can be a bit confusing but leads to a more natural caching behavior.


If needed, the cache behavior can be controlled in more detail using the following configuration settings. Unlike the maximum cache entry size, these settings are either per query or per session:


- It is sometimes desirable to utilize the cache only passively (\= try to read from it but not write to it) or only actively (\= try to write to it but not read from it). This can be achieved using settings `enable_writes_to_query_cache` and
`enable_reads_from_query_cache` which are both `true` by default.
- To cache only expensive (in terms of runtime) or frequent queries, you can specify how long (in milliseconds) and how often queries need to run at least such that their result is cached using the settings `use_query_cache_min_query_duration` and `use_query_cache_min_query_runs`.
- Results of queries with non\-deterministic functions such as `rand()` and `now()` are by default not cached. If desired, this can be changed using the setting `query_cache_store_results_of_queries_with_nondeterministic_functions`.
- Finally, entries in the query cache are, by default, not shared between users due to security reasons. However, individual cache entries can be marked readable for other users by running them with the setting `query_cache_share_between_users`.


## Design [\#](/blog/introduction-to-the-clickhouse-query-cache-and-design#design)


Generally speaking, one can distinguish transactionally consistent and inconsistent query caching.


In transactionally consistent caching, the database invalidates a cache entry if the result of the associated `SELECT` query changes or even changes potentially. Obvious operations that can change query results include inserts, updates, and deletes of table data. ClickHouse also has certain housekeeping operations, such as collapsing merges, that potentially modify table data. The concept of transactionally consistent caching especially makes sense for OLTP databases such as MySQL, Postgresql, and Oracle which have strict consistency expectations.


In contrast, ClickHouse, as an OLAP database, uses a query cache that is transactionally inconsistent by design. Slightly inaccurate query results are tolerated, assuming that cache entries are associated with a time\-to\-live after which they expire and that the underlying data changes only a little during this period. Inserts, updates, deletes, and internal housekeeping operations do not invalidate cache entries. As a result, this design avoids the scalability issues that plagued [MySQL's query cache](https://dev.mysql.com/doc/refman/5.7/en/query-cache.html) in high\-throughput scenarios.


Another difference to MySQL's query cache is that ClickHouse's query cache references query results using the [Abstract Syntax Tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) of the `SELECT` query instead of their query text. This means that caching is agnostic to upper and lowercase changes e.g. `SELECT 1` and `select 1` are treated as the same query.


## Future improvements [\#](/blog/introduction-to-the-clickhouse-query-cache-and-design#future-improvements)


Currently, the cache stores its entries in a simple hash table with at most 1024 elements by default (the exact capacity is configurable). If a new entry is inserted, but the cache is already full, then the map is iterated, and all stale entries are removed. If there is still not enough space, the new entry will not be inserted. Users can also clear the cache's content manually using the statement `SYSTEM DROP QUERY CACHE`. It is planned that we will support more sophisticated eviction strategies in the future, for example, Least Recently Used (LRU) or size\-based eviction. This will allow users to specify a minimum "freshness level" for `SELECT` queries reading from the cache (as opposed to specifying a maximum time\-to\-live for queries writing to the cache) and additionally provide better handling of highly skewed query streams.


Further planned improvements to the query cache are:


1. an ability to compress cache entries, e.g., with the ZSTD codec,
2. paging of cache entries on disk such that they survive server restarts,
3. caching of subqueries and intermediate query results, and
4. more configuration settings to tailor the cache to specific use cases, e.g., per\-user cache sizes or partitioned caches.


The feedback on the query cache has been really positive so far, and exciting things lie ahead, stay tuned!

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
