---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/engines/table-engines/mergetree-family/textindexes.md)#
topic: full-text-search-with-text-indexes-clickhouse-docs
ch_version_introduced: '192.168'
last_updated: '2026-06-12'
chunk_index: 21
total_chunks_in_doc: 24
---

and union operations, the posting lists are stored as [roaring bitmaps](https://roaringbitmap.org/). If the posting list is larger than `posting_list_block_size`, it is split into multiple blocks that are stored sequentially to the postings lists file. **Merging of text indexes**

When data parts are merged, the text index does not need to be rebuilt from scratch; instead, it can be merged efficiently in a separate step of the merge process.
During this step, the sorted dictionaries of the text indexes of each input part are read and combined into a new unified dictionary.
The row numbers in the postings lists are also recalculated to reflect their new positions in the merged data part, using a mapping of old to new row numbers that is created during the initial merge phase.
This method of merging text indexes is similar to how [projections](/docs/sql-reference/statements/alter/projection#projection-indexes) with `_part_offset` column are merged.
If index is not materialized in the source part, it is built, written into a temporary file and then merged together with indexes from the other parts and from other temporary index files.

**Debugging**

Table function [mergeTreeTextIndex](/docs/sql-reference/table-functions/mergeTreeTextIndex) can be used to introspect text indexes.

## Example: Hackernews dataset[​](#hacker-news-dataset "Direct link to Example: Hackernews dataset")

Let's look at the performance improvements of text indexes on a large dataset with lots of text.
We will use 28\.7M rows of comments on the popular Hacker News website.
Here is the table without text index:

```
CREATE TABLE hackernews (
    id UInt64,
    deleted UInt8,
    type String,
    author String,
    timestamp DateTime,
    comment String,
    dead UInt8,
    parent UInt64,
    poll UInt64,
    children Array(UInt32),
    url String,
    score UInt32,
    title String,
    parts Array(UInt32),
    descendants UInt32
)
ENGINE = MergeTree
ORDER BY (type, author);

```

The 28\.7M rows are in a Parquet file in S3 \- let's insert them into the `hackernews` table:

```
INSERT INTO hackernews
    SELECT * FROM s3Cluster(
        'default',
        'https://datasets-documentation.s3.eu-west-3.amazonaws.com/hackernews/hacknernews.parquet',
        'Parquet',
        '
    id UInt64,
    deleted UInt8,
    type String,
    by String,
    time DateTime,
    text String,
    dead UInt8,
    parent UInt64,
    poll UInt64,
    kids Array(UInt32),
    url String,
    score UInt32,
    title String,
    parts Array(UInt32),
    descendants UInt32');

```

We will use `ALTER TABLE` and add a text index on comment column, then materialize it:
