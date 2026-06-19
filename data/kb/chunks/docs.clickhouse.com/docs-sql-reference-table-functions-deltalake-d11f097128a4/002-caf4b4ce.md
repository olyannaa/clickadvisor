---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/deltalake.md)#
topic: deltalake-clickhouse-docs
ch_version_introduced: '3.426'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

'<access_key>', '<secret>') WHERE (firstname = 'John') AND (lastname = 'Smith') ``` ``` Query id: 65032944-bed6-4d45-86b3-a71205a2b659 ┌────id─┬─firstname─┬─lastname─┬─gender─┬─age─┐ 1. │ 10001 │ John │ Smith │ Male │ 30 │ └───────┴───────────┴──────────┴────────┴─────┘ ``` ## Virtual Columns[​](#virtual-columns "Direct link to Virtual Columns")

- `_path` — Path to the file. Type: `LowCardinality(String)`.
- `_file` — Name of the file. Type: `LowCardinality(String)`.
- `_size` — Size of the file in bytes. Type: `Nullable(UInt64)`. If the file size is unknown, the value is `NULL`.
- `_time` — Last modified time of the file. Type: `Nullable(DateTime)`. If the time is unknown, the value is `NULL`.
- `_etag` — The etag of the file. Type: `LowCardinality(String)`. If the etag is unknown, the value is `NULL`.

## Related[​](#related "Direct link to Related")

- [DeltaLake engine](/docs/engines/table-engines/integrations/deltalake)
- [DeltaLake cluster table function](/docs/sql-reference/table-functions/deltalakeCluster)
[Previouscluster](/docs/sql-reference/table-functions/cluster)[NextdeltaLakeCluster](/docs/sql-reference/table-functions/deltalakeCluster)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Examples](#examples)
	- [Reading data](#reading-data)- [Inserting data](#inserting-data)- [Virtual Columns](#virtual-columns)- [Related](#related)
Was this page helpful?
