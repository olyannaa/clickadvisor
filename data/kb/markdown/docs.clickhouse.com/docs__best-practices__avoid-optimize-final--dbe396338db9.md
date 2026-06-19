# Avoid \`OPTIMIZE FINAL\` \| ClickHouse Docs


- - [Best practices](/docs/best-practices)- Avoid optimize final
[Edit this page](https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/avoid_optimize_final.md)ClickHouse tables using the **MergeTree engine** store data on disk as **immutable parts**, which are created every time data is inserted.


Each insert creates a new part containing sorted, compressed column files, along with metadata like indexes and checksums. For a detailed description of part structures and how they're formed we recommend this [guide](/docs/parts).


Over time, background processes merge smaller parts into larger ones to reduce fragmentation and improve query performance.


![Simple merges](/docs/assets/ideal-img/simple_merges.fe7fc38.48.png)
While it's tempting to manually trigger this merge using:



```
OPTIMIZE TABLE <table> FINAL;

```

**you should avoid the `OPTIMIZE FINAL` operation in most cases** as it initiates
resource intensive operations which may impact cluster performance.


OPTIMIZE FINAL vs FINAL`OPTIMIZE FINAL` isn't the same as `FINAL`, which is sometimes necessary to use
to get results without duplicates, such as with the `ReplacingMergeTree`. Generally,
`FINAL` is okay to use if your queries are filtering on the same columns as those
in your primary key.


## Why avoid?[​](#why-avoid "Direct link to Why avoid?")


### It's expensive[​](#its-expensive "Direct link to It's expensive")


Running `OPTIMIZE FINAL` forces ClickHouse to merge **all** active parts into a **single part**, even if large merges have already occurred. This involves:


1. **Decompressing** all parts
2. **Merging** the data
3. **Compressing** it again
4. **Writing** the final part to disk or object storage


These steps are **CPU and I/O\-intensive** and can put significant strain on your system, especially when large datasets are involved.


### It ignores safety limits[​](#it-ignores-safety-limits "Direct link to It ignores safety limits")


Normally, ClickHouse avoids merging parts larger than \~150 GB (configurable via [max\_bytes\_to\_merge\_at\_max\_space\_in\_pool](/docs/operations/settings/merge-tree-settings#max_bytes_to_merge_at_max_space_in_pool)). But `OPTIMIZE FINAL` **ignores this safeguard**, which means:


- It may try to merge **multiple 150 GB parts** into one massive part
- This could result in **long merge times**, **memory pressure**, or even **out\-of\-memory errors**
- These large parts may become challenging to merge, i.e. attempts to merge them further fails for the reasons stated above. In cases where merges are required for correct query time behavior, this can result in undesired consequences such as [duplicates accumulating for a ReplacingMergeTree](/docs/guides/developer/deduplication#using-replacingmergetree-for-upserts), diminishing query time performance.


## Let background merges do the work[​](#let-background-merges-do-the-work "Direct link to Let background merges do the work")


ClickHouse already performs smart background merges to optimize storage and query efficiency. These are incremental, resource\-aware, and respect configured thresholds. Unless you have a very specific need (e.g., finalizing data before freezing a table or exporting), **you're better off letting ClickHouse manage merges on its own**.

[PreviousAvoid mutations](/docs/best-practices/avoid-mutations)[NextUsing JSON](/docs/best-practices/use-json-where-appropriate)- [Why avoid?](#why-avoid)
	- [It's expensive](#its-expensive)- [It ignores safety limits](#it-ignores-safety-limits)- [Let background merges do the work](#let-background-merges-do-the-work)
Was this page helpful?
