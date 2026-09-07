---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ANN
topic: ann-vector-search-with-sql-powered-lsh-random-projections-clickhouse
ch_version_introduced: '0.933'
last_updated: '2026-09-07'
chunk_index: 13
total_chunks_in_doc: 23
---

function. For the same query, we need to construct the bit hash above for our term using our index.For our hamming distance calculation between our target vector’s bit and those in each row, we use the [bitHammingDistance](https://clickhouse.com/docs/en/sql-reference/functions/bit-functions#bithammingdistance) function.

***The use of the bitHammingDistance function for UInt128 [requires ClickHouse 23\.11](https://github.com/ClickHouse/ClickHouse/pull/57073). Users on earlier versions should use `bitCount(bitXor(bits, target))` for hammingDistance on UInt128s.***

```
1WITH 'dog' AS search_term,
2   (
3       SELECT vector
4       FROM glove
5       WHERE word = search_term
6       LIMIT 1
7   ) AS target_vector,
8   128 AS num_bits,
9   (
10       SELECT
11           groupArray(normal) AS normals,
12           groupArray(offset) AS offsets
13       FROM
14       (
15           SELECT *
16           FROM planes
17           LIMIT num_bits
18       )
19   ) AS partition,
20   partition.1 AS normals,
21   partition.2 AS offsets,
22   (
23       SELECT arraySum((normal, offset, bit) -> bitShiftLeft(toUInt128(dotProduct(target_vector - offset, normal) > 0), bit), normals, offsets, range(num_bits))
24   ) AS target
25SELECT word
26FROM glove_lsh WHERE word != search_term
27ORDER BY bitHammingDistance(bits, target) ASC
28LIMIT 5
29
30┌─word─────┐
31│ animal   │
32│ pup 	   │
33│ pet 	   │
34│ kennel   │
35│ neutered │
36└──────────
37
385 rows in set. Elapsed: 0.086 sec. Processed 2.21 million rows, 81.42 MB (25.75 million rows/s., 947.99 MB/s.)
39Peak memory usage: 60.40 MiB.
```
Copy command
A lot faster! The results are different from the exact results returned by the [cosineDistance](https://clickhouse.com/docs/en/sql-reference/functions/distance-functions#cosinedistance) function but seem to make sense largely.

The quality returned by this distance estimation will likely vary on the vector space itself and how well the random places partition it. There are also cases where an estimation of quality is insufficient. Should quality be poor, or we need a more precise ordering, this index can also be used to pre\-filter the result set before the matching results are rescored and possibly restricted to those that satisfy a threshold. This is a common technique and, historically, the approach in many traditional search systems where a term lookup is used, and a window is rescored with a vector (or other relevance) function.
