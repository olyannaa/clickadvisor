---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-25-10-clickhouse
ch_version_introduced: '25.10'
last_updated: '2026-09-07'
chunk_index: 13
total_chunks_in_doc: 14
---

that contains around 40,000 embeddings: ``` 1wget https://huggingface.co/api/datasets/Qdrant/dbpedia-entities-openai3-text-embedding-3-large-1536-1M/parquet/default/train/0.parquet ``` Copy command Now let’s insert those records into our table: ``` 1INSERT INTO dbpedia 2SELECT `_id` AS id, title, text, 3 `text-embedding-3-large-1536-embedding` AS vector 4FROM file('0.parquet'); ``` Copy command

```
10 rows in set. Elapsed: 6.161 sec. Processed 38.46 thousand rows, 367.26 MB (6.24 thousand rows/s., 59.61 MB/s.)
2Peak memory usage: 932.41 MiB.
```
Copy command
It takes just over 6 seconds to ingest the records, while also materializing the HNSW index.

Let’s now create a copy of the `dbpedia` table:

```
1create table dbpedia2 as dbpedia;
```
Copy command
We can now choose to delay the point at which index materialization happens by configuring the following setting:

```
1SET exclude_materialize_skip_indexes_on_insert='vector_idx';
```
Copy command
If we repeat our earlier insert statement, but on `dbpedia2`:

```
1INSERT INTO dbpedia2
2SELECT `_id` AS id, title, text, 
3       `text-embedding-3-large-1536-embedding` AS vector
4FROM file('0.parquet');
```
Copy command
We can see it’s significantly quicker:

```
10 rows in set. Elapsed: 0.522 sec. Processed 38.46 thousand rows, 367.26 MB (73.68 thousand rows/s., 703.59 MB/s.)
2Peak memory usage: 931.08 MiB.
```
Copy command
We can see whether the index has been materialized by writing the following query:

```
1SELECT table, data_compressed_bytes, data_uncompressed_bytes, marks_bytes FROM system.data_skipping_indices
2WHERE name = 'vector_idx';
```
Copy command

```
1┌─table────┬─data_compressed_bytes─┬─data_uncompressed_bytes─┬─marks_bytes─┐
2│ dbpedia  │             124229003 │               128770836 │          50 │
3│ dbpedia2 │                     0 │                       0 │           0 │
4└──────────┴───────────────────────┴─────────────────────────┴─────────────┘
```
Copy command
In `dbpedia2`, we can see that the number of bytes taken is 0, which is what we’d expect. The index will be materialized in the background merge process, but if we want to make it happen immediately, we can run this query:

```
1ALTER TABLE dbpedia2 MATERIALIZE INDEX vector_idx 
2SETTINGS mutations_sync = 2;
```
Copy command
Re\-running the query against the `data_skipping_indices` table will return the following output:

```
1┌─table────┬─data_compressed_bytes─┬─data_uncompressed_bytes─┬─marks_bytes─┐
2│ dbpedia  │             124229003 │               128770836 │          50 │
3│ dbpedia2 │             124237137 │               128769912 │          50 │
4└──────────┴───────────────────────┴─────────────────────────┴─────────────┘
```
Copy command
Alternatively, we can query the `system.parts` table if we want to see whether any indices have been materialized for a given part:

```
1SELECT name, table, secondary_indices_compressed_bytes, secondary_indices_uncompressed_bytes, secondary_indices_marks_bytes 
2FROM system.parts;
```
Copy command
