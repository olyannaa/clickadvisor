---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/best-practices/prewhere.md)#
topic: how-does-the-prewhere-optimization-work-clickhouse-docs
ch_version_introduced: '0.056'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 5
---

predicate. Now, thanks to the PREWHERE clause, the next step differs: Instead of reading all relevant columns up front, ClickHouse filters data column by column, only loading what's truly needed. This drastically reduces I/O, especially for wide tables.

With each step, it only loads granules that contain at least one row that survived—i.e., matched—the previous filter. As a result, the number of granules to load and evaluate for each filter decreases monotonically:

**Step 1: Filtering by town**  

ClickHouse begins PREWHERE processing by ① reading the selected granules from the `town` column and checking which ones actually contain rows matching `London`.

In our example, all selected granules do match, so ② the corresponding positionally aligned granules for the next filter column—`date`—are then selected for processing:

![Step 1: Filtering by town](/docs/assets/images/prewhere_03-42f88b0b26d08c29b483dbbccf88ebc6.gif)
  

**Step 2: Filtering by date**  

Next, ClickHouse ① reads the selected `date` column granules to evaluate the filter `date > '2024-12-31'`.

In this case, two out of three granules contain matching rows, so ② only their positionally aligned granules from the next filter column—`price`—are selected for further processing:

![Step 2: Filtering by date](/docs/assets/images/prewhere_04-40ad308e646679570273fa9b6a59d35c.gif)
  

**Step 3: Filtering by price**  

Finally, ClickHouse ① reads the two selected granules from the `price` column to evaluate the last filter `price > 10_000`.

Only one of the two granules contains matching rows, so ② just its positionally aligned granule from the `SELECT` column—`street`—needs to be loaded for further processing:

![Step 2: Filtering by price](/docs/assets/images/prewhere_05-70191eda3b5ae415dbe99e12d5321b72.gif)
  

By the final step, only the minimal set of column granules, those containing matching rows, are loaded. This leads to lower memory usage, less disk I/O, and faster query execution.

PREWHERE reduces data read, not rows processedNote that ClickHouse processes the same number of rows in both the PREWHERE and non\-PREWHERE versions of the query. However, with PREWHERE optimizations applied, not all column values need to be loaded for every processed row.

## PREWHERE optimization is automatically applied[​](#prewhere-optimization-is-automatically-applied "Direct link to PREWHERE optimization is automatically applied")

The PREWHERE clause can be added manually, as shown in the example above. However, you don't need to write PREWHERE manually. When the setting [`optimize_move_to_prewhere`](/docs/operations/settings/settings#optimize_move_to_prewhere) is enabled (true by default), ClickHouse automatically moves filter conditions from WHERE to PREWHERE, prioritizing those that will reduce read volume the most.
