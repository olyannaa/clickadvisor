---
source: kb.altinity.com
url: https://clickhouse.com/docs/en/sql-reference/statements/alter/partition
topic: backfill-populate-mv-in-a-controlled-manner-altinity-knowledge-base-for-clickhouse
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 2
---

the table’s ORDER BY expression. All such rows are aggregated to only one rows using the aggregating functions defined in the column definitions. There are two “special” column types, designed specifically for that purpose: - [AggregatingFunction](https://clickhouse.com/docs/en/sql-reference/data-types/aggregatefunction) - [SimpleAggregatingFunction](https://clickhouse.com/docs/en/sql-reference/data-types/simpleaggregatefunction)

INSERT … SELECT operating over the very large partition will create data parts by 1M rows (min\_insert\_block\_size\_rows), those parts will be aggregated during the merge process the same way as GROUP BY do it, but the number of rows will be much less than the total rows in the partition and RAM usage too. Merge combined with GROUP BY will create a new part with a much less number of rows. That data part possibly will be merged again with other data, but the number of rows will be not too big.

```
CREATE TABLE mv_import (
  id UInt64,
  ts SimpleAggregatingFunction(max,DateTime),         -- most fresh
  v1 SimpleAggregatingFunction(sum,UInt64),           -- just sum
  v2 SimpleAggregatingFunction(max,String),           -- some not empty string
  v3 AggregatingFunction(argMax,String,ts)            -- last value
) ENGINE = AggregatingMergeTree()
ORDER BY id;

INSERT INTO mv_import
SELECT id,                              -- ORDER BY column
   ts,v1,v2,                            -- state for SimpleAggregatingFunction the same as value
   initializeAggregation('argMaxState',v3,ts)  -- we need to convert from values to States for columns with AggregatingFunction type
FROM huge_table
WHERE toYYYYMM(ts) = 202105;

```
Actually, the first GROUP BY run will happen just before 1M rows will be stored on disk as a data part. You may disable that behavior by switching off [optimize\_on\_insert](https://clickhouse.com/docs/en/operations/settings/settings#optimize-on-insert)
setting if you have heavy calculations during aggregation.

You may attach such a table (with AggregatingFunction columns) to the main table as in the example above, but if you don’t like having States in the Materialized Table, data should be finalized and converted back to normal values. In that case, you have to move data by INSERT … SELECT again:

```
INSERT INTO MV
SELECT id,ts,v1,v2,  -- nothing special for SimpleAggregatingFunction columns
  finalizeAggregation(v3)
from mv_import FINAL

```
The last run of GROUP BY will happen during FINAL execution and AggregatingFunction types converted back to normal values. To simplify retries after failures an additional temporary table and the same trick with ATTACH could be applied.

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)
