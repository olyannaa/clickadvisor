---
source: blog
url: https://www.elastic.co/
topic: clickhouse-vs-elasticsearch-the-billion-row-matchup
ch_version_introduced: '8.5'
last_updated: '2026-06-12'
chunk_index: 12
total_chunks_in_doc: 21
---

and calculate the aggregation result from scratch. ### Query Runtimes [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#query-runtimes) We run all [benchmark queries](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#benchmark-queries) over the data sets that: - Are compressed with the Elasticsearch and ClickHouse standard `LZ4` codec - Don’t store `_source` in Elasticsearch

All queries are executed three times with cold caches. We execute one query at a time i.e., measure latency only. In our charts in this blog, we take the average execution time as the final result and link to the detailed benchmark run results.

#### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#elasticsearch-1)

We run Elasticsearch queries (DSL) via the [Search REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/search.html) and use the JSON response body’s [took](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html#search-api-response-body) time, representing the total server\-side execution time.

ESQL queries are executed with the [ESQL REST API](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-query-api.html). Responses of Elasticsearch ESQL queries don’t include any runtime information. Server\-side execution times for ESQL queries are logged in Elasticsearch’s [log file](https://www.elastic.co/guide/en/elasticsearch/reference/current/logging.html), though.

We know that query runtimes are also available in the [search slow log](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-slowlog.html#search-slow-log), but only on a per\-shard level and not in consolidated form for the complete query execution over all involved shards.

#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#clickhouse-1)

All ClickHouse SQL queries are executed via [ClickHouse client](https://clickhouse.com/docs/en/interfaces/cli), and the server\-side execution time is taken from the [query\_log](https://clickhouse.com/docs/en/operations/system-tables/query_log) system table (from the `query_duration_ms` field).

### Disabling caches [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#disabling-caches)

#### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#elasticsearch-2)

For query processing, Elasticsearch [leverages](https://www.elastic.co/blog/elasticsearch-caching-deep-dive-boosting-query-speed-one-cache-at-a-time) the operating\-system\-level [filesystem cache](https://en.wikipedia.org/wiki/Page_cache), the shard\-level [request cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html), and the segment\-level [query cache](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-cache.html).

For DSL queries, we disabled the `request cache` on a per\-request basis with the request\_cache\-[query\-string parameter](https://www.elastic.co/guide/en/elasticsearch/reference/current/shard-request-cache.html#_enabling_and_disabling_caching_per_request). For ESQL queries, this is not possible, though.

The `query cache` can only be enabled or disabled [per](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-cache.html#query-cache-index-settings) index, but not per request. Instead, we manually dropped the request and query caches via the [clear cache API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-clearcache.html) before each query run.

There is no Elasticsearch API or setting for dropping or ignoring the `filesystem cache`, so we drop it manually using a simple [process](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch#process-for-dropping-filesystem-cache-for-elasticsearch).

#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#clickhouse-2)

Like Elasticsearch, ClickHouse utilizes the OS `filesystem cache` and a [query cache](https://clickhouse.com/docs/en/operations/query-cache) for query processing.

Both caches can be manually dropped with a [SYSTEM DROP CACHE statement](https://clickhouse.com/docs/en/sql-reference/statements/system).

We disabled both caches per query with the query’s [SETTINGS clause](https://clickhouse.com/docs/en/sql-reference/statements/select#settings-in-select-query):

`… SETTINGS enable_filesystem_cache=0, use_query_cache=0;`

### Query peak memory usages [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#query-peak-memory-usages)

#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#clickhouse-3)
