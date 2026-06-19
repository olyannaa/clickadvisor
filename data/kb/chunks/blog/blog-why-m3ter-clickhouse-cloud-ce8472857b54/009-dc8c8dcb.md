---
source: blog
url: https://www.m3ter.com/guides/usage-based-pricing
topic: why-m3ter-chose-clickhouse-cloud
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 14
---

even if not every column of data was needed to fulfil the query. Solutions such as ClickHouse Cloud and Snowflake performed well here \- we easily achieved our target, with sustained rates of hundreds of queries per second.

Redshift was more of a struggle \- although we did hit our target, we couldn’t get a high degree of confidence that we could continue to scale this in future. Redshift is geared more towards traditional OLAP queries \- that is, a smaller number of very complex queries. Our tests involved a large number of simple queries (where by "simple", I mean that relative to the big beasts I’ve seen before in some OLAP workloads). We also had a concern about the vacuuming process that Redshift uses in the background \- this can result in occasional "blips" in service throughput whilst significant resource is spent on this process. Although all mature databases have some similar or equivalent background processes running, we didn’t experience any performance degradation from ClickHouse Cloud or Snowflake caused by this.

Firebolt similarly achieved the query throughput target, but we found that although scaling the service horizontally did increase the throughput we could achieve, it didn’t scale as well as some other services managed. Although this means we could continue to scale out as our workload grew, we would see diminishing returns on the extra hardware we were paying for. (To be fair, no service scales perfectly, and all of them will exhibit some diminishing returns \- but some services were notably better than others in this particular respect).

## Data Export [\#](/blog/why-m3ter-clickhouse-cloud#data-export)

It was possible to export data (e.g. as the result of a query) from all of the candidates being tested. However, some services made this much easier and more efficient than others. For example, ClickHouse Cloud offers an [S3 table function](https://clickhouse.com/docs/en/sql-reference/table-functions/s3), allowing export of query results directly to files in S3\. Some of the other options would require us to write some export code to achieve the same result, which would mean higher maintenance and operational costs (in terms of human resource).

## Data Deletion [\#](/blog/why-m3ter-clickhouse-cloud#data-deletion)

All of the databases supported data deletion, although some were more performant than others.
