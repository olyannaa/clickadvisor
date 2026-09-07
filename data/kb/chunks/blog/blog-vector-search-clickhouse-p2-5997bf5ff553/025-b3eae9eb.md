---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Vector
topic: vector-search-with-clickhouse-part-2-clickhouse
ch_version_introduced: '0.33110910654067993'
last_updated: '2026-09-07'
chunk_index: 25
total_chunks_in_doc: 29
---

point number, assuming the latter uses the IEE\-754 encoding. ![Bfloat16.png](/_next/image?url=%2Fuploads%2FBfloat16_a2059b234a.png&w=2048&q=75) *Credit: <https://cloud.google.com/tpu/docs/bfloat16>* While bfloat16 is [not currently native to ClickHouse](https://github.com/ClickHouse/ClickHouse/issues/44206), it can easily be replicated with other functions. We do so below for the `image_embedding` and `text_embedding` columns.

To do so, all rows from the table `laion_100m` (containing 100m rows) are selected, and inserted into the table `laion_100m_bfloat16` using an `INSERT INTO SELECT` clause. During the `SELECT`, we transform the values in the embeddings to a BFloat16 representation.

This bfloat16 conversion is achieved using an `arrayMap` function, i.e., `arrayMap(x -> reinterpretAsFloat32(bitAnd(reinterpretAsUInt32(x), 4294901760)), image_embedding)`.

This iterates over every value `x` in a vector embedding, executing the transformation  `reinterpretAsFloat32(bitAnd(reinterpretAsUInt32(x), 4294901760))` \- this interprets the binary sequence as an Int32 using the function `reinterpretAsUInt32` and performs a `bitAnd` with the value `4294901760`. This latter value is the binary sequence `000000000000000001111111111111111`. This operation, therefore, zeros the trailing 16 bits, performing an effective truncation. The resulting binary value is then re\-interpreted as a float32\.

We illustrate this process below:

```
1INSERT INTO default.laion_1m_bfloat16 SELECT
2	_file,
3	key,
4	url,
5	caption,
6	similarity,
7	width,
8	height,
9	original_width,
10	original_height,
11	status,
12	NSFW,
13	exif,
14	arrayMap(x -> reinterpretAsFloat32(bitAnd(reinterpretAsUInt32(x), 4294901760)), text_embedding) AS text_embedding,
15	arrayMap(x -> reinterpretAsFloat32(bitAnd(reinterpretAsUInt32(x), 4294901760)), image_embedding) AS image_embedding,
16	orientation,
17	software,
18	copyright,
19	image_make,
20	image_model
21FROM laion_1m
```
Copy command
![bfloat16_process.png](/_next/image?url=%2Fuploads%2Fbfloat16_process_ea6a655b7b.png&w=2048&q=75)

As shown below, this has the effect of reducing our compressed data by over 35% \- 0s compress really well.
