# ClickHouse vs. Elasticsearch: The Mechanics of Count Aggregations


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse vs. Elasticsearch: The Mechanics of Count Aggregations

![](/_next/image?url=%2Fuploads%2Ftom_schreiber_headshot_a0cb0ce627.jpeg&w=96&q=75)[Tom Schreiber](/authors/tom-schreiber)May 7, 2024 · 27 minutes read## Introduction [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#introduction)


![Elasticsearch_blog2_header.png](/uploads/Elasticsearch_blog2_header_34fa3d5ee0.png)
In another blog post, we [examined](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup) the performance of ClickHouse vs. Elasticsearch on a workload commonly present in large\-scale data analytics and observability use cases – count(\*) aggregations over billions of table rows. We showed that ClickHouse vastly outperforms Elasticsearch for running aggregation queries over large data volumes. Specifically:


Count(\*) aggregation queries in ClickHouse utilize hardware highly efficiently, [resulting](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#summary) in **at least 5 times lower latencies** for aggregating large data sets compared to Elasticsearch. This requires smaller and **4 times cheaper hardware** for comparable Elasticsearch latencies.


For these above\-mentioned reasons, we increasingly see users migrating from Elasticsearch to ClickHouse, with customer stories highlighting:


- Highly reduced costs in petabyte\-scale observability use cases:



> “Migrating from Elasticsearch to ClickHouse, reduced the cost of our Observability hardware by over 30%.” [Didi Tech](https://clickhouse.com/blog/didi-migrates-from-elasticsearch-to-clickHouse-for-a-new-generation-log-storage-system)


- Lifts in technical limitations of data analytics applications:



> “This unleashed potential for new features, growth and easier scaling.” [Contentsquare](https://clickhouse.com/blog/contentsquare-migration-from-elasticsearch-to-clickhouse)


- Drastic improvements in scalability and query latencies for monitoring platforms:



> “ClickHouse helped us to scale from millions to billions of rows monthly.”   
>  “After the switch, we saw a 100x improvement on average read latencies” [The Guild](https://clickhouse.com/blog/100x-faster-graphql-hive-migration-from-elasticsearch-to-clickhouse)


You will likely wonder, "Why is ClickHouse so much faster and more efficient than Elasticsearch?" This blog will give you an in\-depth technical answer to this question.


## Count aggregations in ClickHouse and Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#count-aggregations-in-clickhouse-and-elasticsearch)


A common use case for aggregation in data analytics scenarios is calculating and ranking the frequency of values in a dataset. As an example, all data visualizations in this screenshot from the [ClickPy application](https://clickpy.clickhouse.com/) (analyzing almost 900 billion rows of [Python package download events](https://packaging.python.org/en/latest/guides/analyzing-pypi-package-downloads/#id10)) use a SQL `GROUP BY` clause in combination with a `count(*)` aggregation [under the hood](https://youtu.be/j_kKKX1bguw?si=8-kFAU9aaBJjVtlJ):
![Elasticsearch_blog2_01.png](/uploads/Elasticsearch_blog2_01_8f28278d09.png)


Similarly, in [logging use cases](https://clickhouse.com/blog/building-a-logging-platform-with-clickhouse-and-saving-millions-over-datadog) (or more generally [observability use cases](https://clickhouse.com/blog/overview-of-highlightio)), one of the most common applications for aggregations is to count how often specific log messages or events occur (and alerting in case the frequency is [unusual](https://grafana.com/docs/grafana-cloud/alerting-and-irm/machine-learning/configure/outlier-detection/)).


The equivalent to a ClickHouse `SELECT count(*) FROM ... GROUP BY ...` SQL query in Elasticsearch is the [terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html), which is an Elasticsearch [bucket aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket.html).


ClickHouse’s `GROUP BY` with a `count(*)` and Elasticsearch’s `terms aggregation` are generally equivalent in terms of functionality, but they differ widely in their implementation, performance, and result quality, as described below.


We compare the performance of count aggregations in an [accompanying blog post](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup).



> In addition to bucket aggregations, Elasticsearch also provides [metric aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics.html). We will leave a comparison of ClickHouse and Elasticsearch for metric use cases for another blog.


## Count aggregation approaches [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#count-aggregation-approaches)


### Parallelization [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#parallelization)


#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse)


ClickHouse was built from the [very beginning](https://youtu.be/ZOZQCQEtrz8?si=XrQ-vMDiHEsgsrYq&t=103) to filter and **aggregate** internet\-scale data as quickly and [efficiently](https://clickhouse.com/docs/en/faq/general/why-clickhouse-is-so-fast) as possible. To do so, ClickHouse parallelizes SELECT queries, including aggregation functions like `count(*)` and all other [90\+](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference) aggregation functions at the level of ① column values, ② table chunks, and ③ table shards:
![Elasticsearch_blog2_02.png](/uploads/Elasticsearch_blog2_02_fd9e5b0dd8.png)


##### ① SIMD parallelization [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-simd-parallelization)


ClickHouse utilizes the CPU's [SIMD units](https://en.wikipedia.org/wiki/Single_instruction,_multiple_data) (e.g. [AVX512](https://en.wikipedia.org/wiki/AVX-512)) to apply the same operations to consecutive values in a column. [This](https://clickhouse.com/blog/cpu-dispatch-in-clickhouse) blog post details how this works.


##### ② Multi\-Core parallelization [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization)


On a single machine with `n` CPU cores, ClickHouse runs an aggregation query with `n` [parallel execution lanes](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/query-processing/README.md#clickhouse) (or fewer or more, if requested by the user via [max\_threads](https://clickhouse.com/docs/en/operations/settings/settings#max_threads) setting):
![Elasticsearch_blog2_03.png](/uploads/Elasticsearch_blog2_03_2f10f45c58.png)


The figure above shows how ClickHouse processes `n` non\-overlapping data ranges in parallel. These data ranges can be arbitrary, e.g. they don’t need to be based on the grouping key. When the aggregation query contains a filter in the form of a `WHERE` clause, and the [primary index](https://clickhouse.com/docs/en/optimize/sparse-primary-indexes) can be utilized to evaluate this filter, ClickHouse locates matching table data ranges and spreads these [dynamically](https://youtu.be/hP6G2Nlz_cA?si=FeCadjUfzgiw-Qph&t=633) among the `n` execution lanes.


This parallelization approach is enabled using [partial aggregation states](https://www.google.com/url?q=https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states%23working-with-aggregation-states&sa=D&source=docs&ust=1714996294648579&usg=AOvVaw3syvRuV3_D61ogmWRv-PDF): each of the `n` execution lanes produces partial aggregation states. These partial aggregation states are eventually merged into the final aggregation result.


For the `count(*)` aggregation, the partial aggregation state is simply an incrementally updated count variable. In fact, `count(*)` aggregation is the simplest kind of aggregation and could be parallelized internally, even without the concept of partial aggregation states. To give a concrete example where partial aggregation states enable parallelization, we use this aggregation query to [calculate](https://sql.clickhouse.com?query_id=EAI3T1FVZSGSRJFSSDCCQP) average house prices per town based on the [UK property prices dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid):



```
SELECT
    town,
    avg(price) AS avg_price
FROM uk_price_paid
GROUP BY town;

```

Assume the database wants to calculate the average house prices in `London` using two parallel execution lanes:
![Elasticsearch_blog2_04.png](/uploads/Elasticsearch_blog2_04_cffa2ff47a.png)


Execution lane 1 averages the house prices of all rows in its data range consisting of two records for London. The resulting `partial aggregation state` for `avg` generally consists of


- a `sum` (here for execution lane 1: `500,000` as the summarized house prices in `London`) and
- a `count` (here for execution lane 1: `2` as the number of processed records for `London`).


Execution lane 2 calculates a similar partial aggregation state. These two partial aggregation states are merged, and with that, the final result can be produced: The average house price for the `London` records is `(500,000 + 400,000) / (2 + 1)` \= `900,000 / 3` \= `300,000`.


Partial aggregation states are necessary to compute correct results. Simply averaging the averages of sub\-ranges produces incorrect results. For example, if we average the average of the first sub\-range (`250,000`) with the average of the second sub\-range (`400,000`), we obtain `(650,000 / 2)` \= `325,000`, which is incorrect.


ClickHouse parallelizes all of its supported [90\+ aggregation functions](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference) plus their combinations with [aggregate function combinators](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators) across all available CPU cores.


##### ③ Multi\-Node parallelization [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-node-parallelization)


If the source table of an aggregation query is [sharded](https://youtu.be/vBjCJtw_Ei0?si=lZYrLGN04R7l0Uhq) and spread over multiple nodes, then ClickHouse parallelizes aggregation functions across all available CPU cores of all available nodes.


Each node (in parallel) performs the aggregation locally using the aforementioned multi\-core parallelization technique. The resulting partial aggregation states are streamed to and merged by the initiator node (the node that initially received the aggregation query):


![Elasticsearch_blog2_05.png](/uploads/Elasticsearch_blog2_05_8cba60d720.png)
As an [optimization](https://clickhouse.com/docs/en/operations/settings/settings#distributed-group-by-no-merge), if the aggregation query’s GROUP BY key is a prefix of the [sharding key](https://clickhouse.com/docs/en/architecture/horizontal-scaling#shard), then the initiator node doesn’t need to merge partial aggregation states, and the merge happens as a last step on each node, and the final results are streamed back to the initiator node instead.


##### Incremental aggregation [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#incremental-aggregation)


All techniques discussed so far are applied at "query time", i.e. when the user runs `SELECT count(*) FROM ... GROUP BY ...` queries. If the same expensive aggregation query is run repeatedly, e.g. hourly, or if sub\-second latencies are required, but the queried data set is too large for that, then ClickHouse provides an additional optimization that shifts the load from the query time to the insert time and (mostly) the background merge time. Specifically, the [above\-mentioned](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization) partial aggregation technique (based on `partial aggregation states`) can also be used at the [data part](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#logical-and-physical-on-disk-data-structures-1) level during ([parallel](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#background_pool_size)) [background part merges](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#insert-processing-1).


This yields a powerful, highly scalable [continuous data summarization technique](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#approaches-for-continuous-data-summarization), with the result that aggregation queries will find the majority of the data already aggregated. The following diagram sketches this:
![Elasticsearch_blog2_06.png](/uploads/Elasticsearch_blog2_06_8a694b0035.png)


① The [\-State](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-state) aggregate function combinator can be used to instruct the ClickHouse query engine to only combine the partial aggregation states ([produced](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization) by the parallel execution lanes) [instead](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization) of combining and calculating the final result:



```
 SELECT
    town,
    avgState(price) AS avg_price_state
FROM uk_price_paid
GROUP BY town;

```


> When you [run](https://sql.clickhouse.com?query_id=EAI3T1FVZSGSRJFSSDCCQP) this query, the partial aggregation states in `avg_price_state` are not really meant to be printed on the screen.


These combined partial aggregation states can then be written as [data parts](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#logical-and-physical-on-disk-data-structures-1) into a table with the [AggregatingMergeTree](https://youtu.be/QDAJTKZT8y4) table engine:



```
INSERT INTO <table with AggregatingMergeTree engine>
SELECT
    town,
    avgState(price) AS avg_price_state
FROM uk_price_paid
GROUP BY town;

```

② This table engine [continues](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#clickhouse) the partial aggregation [incrementally](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#clickhouse) (and [parallelized](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#background_pool_size)) during background part merges. The merged result is the equivalent of running the aggregation query over all of the original data.



> A [materialized view](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse-3) does the insert step above automatically. [Here](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#clickhouse-materialized-views)'s a concrete example based on the `average house price per town` example we used above.


③ At query time, the [\-Merge](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators#-merge) aggregate function combinator can be used to combine the partial aggregation states into the final result aggregation values:



```
SELECT
    town,
    avgMerge(avg_price_state) AS avg_price
FROM <table with AggregatingMergeTree engine>
GROUP BY town;

```

#### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch)


Compared with ClickHouse, Elasticsearch leverages a completely different parallelization approach for its [terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) (which is [used](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#count-aggregations-in-clickhouse-and-elasticsearch) to calculate counts in Elasticsearch). This leads to less efficient hardware utilization than ClickHouse:
![Elasticsearch_blog2_07.png](/uploads/Elasticsearch_blog2_07_fc1d7751f7.png)
The `terms aggregation` always needs a size parameter (called `n` in the following), and Elasticsearch runs this aggregation with [one](https://www.elastic.co/guide/en/elasticsearch/reference/8.12/size-your-shards.html#single-thread-per-shard) CPU thread per [shard](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#elasticsearch), independent of the number of CPU cores. Each thread calculates shard\-local `top n` results (based on the largest `count` values per group by [default](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-order)) from its processed shard. Shard\-local results are eventually consolidated into a global `top n` final result.


Elasticsearch’s multi\-node parallelization of the `terms aggregation` works similarly. When the shards are spread over multiple nodes, each node produces (with the technique explained above) a node\-local `top n` result, and these node\-local results are consolidated into the final global result by the coordinating node (the node that initially received the aggregation query).


Based on how the data is spread over shards, this parallelization approach potentially has a precision issue. We illustrate this with an example:
![Elasticsearch_blog2_08.png](/uploads/Elasticsearch_blog2_08_3f35a3f165.png)
We assume, based on the [UK property prices dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid), that we want to calculate the top two towns with the most sold properties. The data is spread over two shards. The figure above shows abstractly ① the shard\-local counts of property sale records per town. Each processing thread ② returns a shard\-local `top 2` result, which is consolidated ③ into the final global `top 2` result. This result is incorrect, though. Based on the shard\-global data, this is the correct count of records per town:


- `Town 1`: `11`
- `Town 2`: `8`
- `Town 3`: `9`
- `Town 4`: `9`


The ③ result calculated by Elasticsearch has both the count value and ranking for `Town 2` wrong. Precision can be increased by analyzing returned [count errors](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#terms-agg-doc-count-error) and adjusting the [shard size](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-shard-size) parameter \- this commands each processing thread to return a larger `top n` result from each shard than requested by the query, increasing memory requirements and runtimes.



> Elasticsearch also leverages SIMD hardware units [based](https://cr.openjdk.org/~vlivanov/talks/2019_CodeOne_MTE_Vectors.pdf) on the JVM's auto\-vectorization and the Java [Panama Vector API](https://github.com/apache/lucene/pull/12311). Additionally, [since](https://www.elastic.co/blog/whats-new-elasticsearch-platform-8-12-0) Elasticsearch 8\.12 [segments](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#elasticsearch) can be searched in parallel by query processing threads, with the [exception](https://www.elastic.co/blog/whats-new-elasticsearch-platform-8-12-0) of the `terms aggregation`. Because applying the above\-mentioned technique to segments instead of shards has the same issue with precision. As a shard consists of multiple segments, this would also multiply the work per processing thread with an increased `shard size parameter`.


### Precision [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#precision)


#### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch-1)


As described [above](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch), count values in Elasticsearch's [terms aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html) are [approximate](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#terms-agg-doc-count-error) by default when the queried data is split over more than one [shard](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#elasticsearch). The accuracy of results can be improved by analyzing returned [count errors](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#terms-agg-doc-count-error) and adjusting the [shard size](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-shard-size) parameter, but that increases runtimes and memory requirements.


#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse-1)


The `count(*)` aggregation function in ClickHouse calculates fully accurate results.


ClickHouse `count(*)` aggregations are easy to use and don't require additional configuration like in Elasticsearch.


### (No) limit clause [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#no-limit-clause)


#### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch-2)


Because of its [execution model](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch), count aggregations without a limit clause are impossible in Elasticsearch — users must always specify a [size](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-size) setting. Even with large size values, bucket aggregations over high\-cardinality data sets are restricted by the [max\_buckets](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-settings.html#search-settings-max-buckets) setting or require paginating through results using an [expensive](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html) [composite aggregation](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-composite-aggregation.html).


#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse-2)


ClickHouse `count(*)` aggregations are not limited by size restrictions. They additionally [support](https://clickhouse.com/docs/en/sql-reference/statements/select/group-by#group-by-in-external-memory) spilling temporary results to disk if the query memory consumption exceeds an (optional) user\-specified maximum memory [threshold](https://clickhouse.com/docs/en/operations/settings/query-complexity#settings-max_bytes_before_external_group_by). In addition, independent of data set size, ClickHouse [can](https://clickhouse.com/docs/en/sql-reference/statements/select/group-by#group-by-optimization-depending-on-table-sorting-key) run aggregations with minimal memory requirements if the grouping columns in an aggregation form a prefix of the primary key.


Again, ClickHouse `count(*)` aggregations have a lower degree of complexity compared to Elasticsearch.


## Approaches for continuous data summarization [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#approaches-for-continuous-data-summarization)


No matter how efficient the aggregation and query processing in a database is, aggregating [billions](https://clickhouse.com/blog/clickhouse-one-billion-row-challenge) or [trillions](https://clickhouse.com/blog/clickhouse-1-trillion-row-challenge) of rows (typical in [modern data analytics](https://clickhouse.com/blog/the-unbundling-of-the-cloud-data-warehouse) use cases) will always be inherently costly due to the sheer amount of data that must be processed.


Therefore, databases specializing in analytical workloads often provide data summarization as a building block for users to automatically transform incoming data to a summarized data set, representing the original data in a [pre\-aggregated](https://www.youtube.com/watch?v=QUigKP7iy7Y&t=1s) and usually [significantly small](https://youtu.be/QUigKP7iy7Y?si=1QyGJdYTdE7q16gH&t=179) format. Queries will utilize the precomputed data to provide sub\-second latencies in interactive use cases, like the above\-mentioned [ClickPy application](https://clickpy.clickhouse.com/).


Both Elasticsearch and ClickHouse provide built\-in techniques for automatic continuous data summarization. Their techniques have the same functional capabilities but drastically differ in implementation, efficiency, and with that, computing costs.


### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch-3)


Elasticsearch provides a mechanism called [transforms](https://www.elastic.co/guide/en/elasticsearch/reference/current/transforms.html) for batch\-converting existing indices into summarized indices or continuously converting ingested data.


Based on the Elasticsearch [on\-disk format](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#elasticsearch), we describe how transforms work [here](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#elasticsearch) in detail.


We note three downsides of the Elasticsearch approach, namely:


- **The requirement to retain old raw data**: otherwise, transforms can’t correctly recalculate aggregations.
- **Poor scalability and high computing costs**: Whenever new raw data documents are detected for buckets after a [checkpoint](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#elasticsearch), all of the bucket data is queried from the ever\-growing raw data source index and reaggregated. This doesn’t scale to billion, let alone trillion\-scale document sets, and results in high computing costs.
- **Not real\-time**: The transforms pre\-aggregation target index is only up to date with the raw data source index after the next [check interval](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#elasticsearch).



> Exclusively for time series metric data, Elasticsearch also provides a [downsampling](https://www.elastic.co/guide/en/elasticsearch/reference/current/downsampling.html) technique for reducing the footprint of that data by storing it at reduced granularity. Downsampling is the successor of [rollups](https://www.elastic.co/guide/en/elasticsearch/reference/8.13/xpack-rollup.html) and equivalent to a transform that groups metrics data documents by their timestamp casted to a fixed time interval (e.g. hour, day, month, or year) and then applies a fixed set of aggregations ( `min`, `max`, `sum`, `value_count`, and `average`). A comparison with ClickHouse [chained materialized views](https://clickhouse.com/blog/chaining-materialized-views) could be the topic of a future blog.


### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse-3)


ClickHouse uses [materialized views](https://clickhouse.com/docs/en/guides/developer/cascading-materialized-views) in combination with the [AggregatingMergeTree](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/aggregatingmergetree#aggregatingmergetree) table engine and [partial aggregation states](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization) for automatic and (in contrast to Elasticsearch) **incremental** data transformation.


Based on ClickHouse’s [on\-disk format](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#clickhouse), we explain the mechanics of incremental materialized views in detail [here](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#clickhouse).


ClickHouse materialized views have three key advantages over Elasticsearch transforms:


- **No raw data dependency**: Raw data in source tables is never queried, not even when the user wants to perform an exact aggregation calculation. This allows different [TTL](https://clickhouse.com/docs/en/guides/developer/ttl) settings to be applied to the source and the pre\-aggregated target table. Furthermore, in scenarios where only the same set of aggregation queries should be performed, users can choose to ditch the source data after pre\-aggregation completely (using the [Null table engine](https://clickhouse.com/docs/en/engines/table-engines/special/null)).
- **High scalability and low computing costs**: Incremental aggregation is engineered especially for scenarios where raw data source tables contain billions or trillions of rows. Instead of querying the ever\-growing source table repeatedly and recalculating aggregate values from all existing rows belonging to the same group when new raw data rows for that group exist, ClickHouse simply calculates a [partial aggregation state](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-multi-core-parallelization) from (only) the values of the newly inserted raw data rows. This state is incrementally [merged](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/continuous-data-transformation/README.md#clickhouse) with the previously calculated states in the background. In other words \- each raw data value is aggregated with other raw data values exactly once. This results in dramatically lower computing costs compared to aggregation by brute force over the raw data.
- **Real\-time**: When an insert into the raw data source table is successfully acknowledged, the pre\-aggregation target table is guaranteed to be up\-to\-date.


### Backfilling pre\-aggregations [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#backfilling-pre-aggregations)


In our [accompanying benchmark blog post](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup), we use continuous transforms in Elasticsearch and equivalent materialized views in ClickHouse to pre\-aggregate ingested data on the fly into separate data sets. Sometimes, this is not feasible. For example, when a large portion of the data is already ingested, re\-ingesting is not possible or too expensive, and queries that would benefit from running over this data in a pre\-aggregated format are introduced.


#### Elasticsearch [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#elasticsearch-4)


We simulated this scenario in Elasticsearch by running a `batch` transform over the already ingested [10 billion rows data set](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup#data), pre\-calculating counts into a separate data set to speed up an aggregation query that we use as part of our benchmark. Both `continuous` and `batch` transforms use the same checkpoints\-based mechanism described above. Because of the downsides of this mechanism, where the same values are queried and aggregated repeatedly at checkpoints:


**Backfilling via the batch transform took 5 full days** (using significant computing costs). It is a long time to wait until queries can benefit from the pre\-aggregated data.


#### ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse-4)


In ClickHouse, backfilling pre\-aggregations works by using an [INSERT INTO SELECT](https://clickhouse.com/docs/en/sql-reference/statements/insert-into#inserting-the-results-of-select) statement to insert directly into the materialized view’s target table [using](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch#variant-1---directly-inserting-into-the-target-table-by-using-the-materialized-views-transformation-query) the view's SELECT query (transformation) :


**For the 10 billion rows data set, this takes [20 seconds](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch#variant-1---directly-inserting-into-the-target-table-by-using-the-materialized-views-transformation-query) instead of 5 full days**.


These 20 seconds include aggregating the full 10 billion row data set and writing the result (as partial aggregation states) into the target table, which will be used subsequently for the materialized view to handle additional incoming data. Depending on the cardinality of the raw data set, this can be a memory\-intensive approach, as the complete raw data set is ad\-hoc aggregated. Alternatively, users can utilize a [variant](https://github.com/ClickHouse/examples/tree/main/blog-examples/clickhouse-vs-elasticsearch#variant-2---table-to-table-copy-into-a-null-table-engine-table-with-a-connected-materialized-view) that requires minimal memory.


Note that the `20 seconds ClickHouse approach` of manually aggregating the raw data set and directly inserting the result into the target table is not feasible in Elasticsearch. Theoretically, this could work with a [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) (index to index copy) operation. However, this would require keeping the [\_source](https://github.com/ClickHouse/examples/blob/main/blog-examples/clickhouse-vs-elasticsearch/on-disk-format-and-insert-processing/README.md#elasticsearch) data in the raw data set (requiring drastically more storage space). It would also require a mechanism to manually create the necessary checkpoints to correctly continue the pre\-aggregation process when streaming data starts. In ClickHouse, the materialized views will just continue with the incremental aggregation process for new incoming data after we run the backfilling as described above.


## High\-performance aggregations in ClickHouse [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#high-performance-aggregations-in-clickhouse)


Most databases, including ClickHouse, implement `GROUP BY` using some variant of the hash aggregation algorithm in which the aggregation values of input rows are stored and updated in a [hash table](https://en.wikipedia.org/wiki/Hash_table) with the grouping columns as key. Choosing the right kind of hash table is critical for performance. Under the hood, ClickHouse utilizes a sophisticated [hash table framework](https://clickhouse.com/blog/hash-tables-in-clickhouse-and-zero-cost-abstractions) to implement aggregations. Depending on the data type of the grouping columns, the estimated cardinality, and other factors, the fastest hash table is selected individually for each aggregation query from over 30 (as of April 2024\) different implementations. ClickHouse was purposely built for high\-performance aggregations over vast data amounts.


ClickHouse is today amongst the [fastest](https://benchmark.clickhouse.com/) databases on the market, with distinctive features for data analytics:


- State\-of\-the\-art [vectorized](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#-simd-parallelization) query engine with [parallelized execution](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#clickhouse) across all server and cluster resources, [utilizing](https://clickhouse.com/blog/testing-the-performance-of-click-house) hardware up to the theoretical limits
- [Modern SQL](https://www.youtube.com/watch?v=zhrOYQpgvkk) dialect and [rich data types](https://clickhouse.com/docs/en/sql-reference/data-types), including maps and arrays (plus over 80 functions for [working](https://clickhouse.com/docs/en/sql-reference/functions/array-functions) with arrays) for modeling and [solving](https://clickhouse.com/blog/clickhouse-release-23-10#arrayfold) a wide range of problems elegantly and simply
- Over 90 pre\-built [aggregation functions](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference) with support for incremental aggregation of large data sets, plus powerful [aggregation combinators](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/combinators) for [extending](https://www.youtube.com/watch?v=7ApwD0cfAFI) the behavior of other aggregation functions
- Over 1000 regular data processing [functions](https://clickhouse.com/docs/en/sql-reference/functions) for domains like mathematics, geo, machine learning, time series, and more
- Fully [parallelized window functions](https://clickhouse.com/blog/clickhouse-release-23-11#parallel-window-functions)
- [Parallel join algorithms](https://clickhouse.com/blog/clickhouse-fully-supports-joins-hash-joins-part2#parallel-hash-join)
- Native support for loading data in [90\+ file formats](https://clickhouse.com/docs/en/interfaces/formats) from virtually [any data source](https://clickhouse.com/docs/en/engines/table-engines/integrations)


## Summary [\#](/blog/clickhouse_vs_elasticsearch_mechanics_of_count_aggregations#summary)


In this blog post, we provided an in\-depth technical answer to the question of why ClickHouse is so much [faster and more efficient](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup) than Elasticsearch for processing count aggregations, which are commonly needed in data analytics and logging/observability use cases.


We explained parallelization approaches and the difference in result quality and usability complexity of count aggregations in ClickHouse and Elasticsearch. We explored Elasticsearch and ClickHouse's built\-in mechanisms for pre\-calculating counts. We highlighted why ClickHouse materialized views are much more efficient and better suited for processing billion/trillion\-scale row sets than Elasticsearch transforms.


We suggest reading our accompanying blog post [ClickHouse vs. Elasticsearch: The Billion\-Row Matchup](/blog/clickhouse_vs_elasticsearch_the_billion_row_matchup) to see ClickHouse high\-performance aggregations in action. As a teaser, we include some of the benchmark results here:


![Elasticsearch_blog2_09.png](/uploads/Elasticsearch_blog2_09_1eb54d8d50.png)
![Elasticsearch_blog2_10.png](/uploads/Elasticsearch_blog2_10_6046d8912e.png)
![Elasticsearch_blog2_11.png](/uploads/Elasticsearch_blog2_11_554086f6b8.png)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
