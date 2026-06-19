---
source: blog
url: https://clickhouse.com/blog/cloud-data-warehouses-cost-performance-comparison
topic: agentic-analytics-starts-with-query-ready-data-the-write-side-cost-of-snowflake-vs-clickhouse
ch_version_introduced: '17.47'
last_updated: '2026-06-12'
chunk_index: 12
total_chunks_in_doc: 18
---

by outcome and cost: the write warehouse sustained the same 1 million rows per second ingest rate, and the consumed warehouse credits capture the cost. A comparable CPU/memory saturation chart is not available through Snowflake’s native observability surface.

With ingest, part counts, CPU, and memory all under control, the important question becomes when fresh data is actually ready for efficient queries.

### Query\-ready immediately vs. waiting for clustering [\#](/blog/write-side-cost-performance-snowflake-clickhouse#query-ready-immediately-vs-waiting-for-clustering)

Both systems aim for the same outcome: ordered data that can be pruned efficiently. The difference is when fresh data reaches that state.

#### ClickHouse does not wait for a background process to make fresh data useful [\#](/blog/write-side-cost-performance-snowflake-clickhouse#clickhouse-does-not-wait-for-a-background-process-to-make-fresh-data-useful)

Write\-time ordering enables immediate range pruning, while background merges incrementally improve the layout over time. In the part\-count chart above, the maximum stays roughly between 100 and 150 parts per partition, showing a healthy, query\-efficient layout for this workload **at each point in time** \- because ingest is continuous, merges are never “finished” \- and they do not need to be. Queries benefit from ordering immediately; merges simply improve that layout over time.

#### Snowflake has a different dependency: clustering has to catch up [\#](/blog/write-side-cost-performance-snowflake-clickhouse#snowflake-has-a-different-dependency-clustering-has-to-catch-up)

After the first 100B rows, the table contained roughly [540K micro\-partitions](https://pastila.nl/?00db95cf/9f9564e8c1a40280202cb42a1cc5fe3a#t333fd+A8Pbp3ETGsJij8A==GCM). Starting from an empty table, automatic clustering [began 1\.3 hours after ingest started](https://pastila.nl/?0072b6ca/8482376483432dc23da61bc133f645c7#BHBfsRbJCmJ5pWByqlcpyg==GCM) and [finished 6\.7 hours after the 100 billionth row was ingested](https://pastila.nl/?0072b6ca/8482376483432dc23da61bc133f645c7#BHBfsRbJCmJ5pWByqlcpyg==GCM).

That lag matters for real\-time analytics: fresh data may be present in the table before it is fully organized for fast pruning.

Alternative to automatic clustering (click to expand)

 As an alternative to automatic clustering, Snowflake users can manually rewrite tables, for example via  

`CREATE TABLE sorted_table AS SELECT * FROM unsorted_table ORDER BY sorting_column`.
 

 This rewrite runs on warehouse compute, processes the full dataset, and does not provide incremental
 locality maintenance. Under continuous ingest, the rewrite must be repeated, turning it into an ongoing task.
 

 This approach can work for periodic batch refreshes, but becomes operationally heavy for continuously growing tables.
 

The setup above gives us all the pieces. Now we combine the write and ordering costs across the 100B, 200B, and 300B row checkpoints.

## The cost of obtaining query\-ready data [\#](/blog/write-side-cost-performance-snowflake-clickhouse#the-cost-of-obtaining-query-ready-data)
