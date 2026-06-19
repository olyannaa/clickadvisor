---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/engines/table-engines/mergetree-family/annindexes.md)#
topic: exact-and-approximate-vector-search-clickhouse-docs
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 3
total_chunks_in_doc: 19
---

in Euclidean space, - `cosineDistance`, the [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance), representing the angle between two non\-zero vectors, or - `dotProduct`, the [dot product](https://en.wikipedia.org/wiki/Dot_product) (inner product), representing the sum of element\-wise products of two vectors. Equivalent to `cosineDistance` on normalized data.

For normalized data, `L2Distance` is usually the best choice, otherwise `cosineDistance` is recommended to compensate for scale.

NoteFor distance functions `L2Distance` and `cosineDistance`, a smaller value means a higher similarity, whereas for `dotProduct`, a higher value means a higher similarity.
As a result, vector indexes with `L2Distance` and `cosineDistance` can only be used by `SELECT [...] ORDER BY [...] ASC` queries (`ASC` is the default for `ORDER BY`), whereas vector indexes built for `dotProduct` can only be used by `SELECT [...] ORDER BY [...] DESC` queries.

`<dimensions>` specifies the array cardinality (number of elements) in the underlying column.
If ClickHouse finds an array with a different cardinality during index creation, the index is discarded and an error is returned.

The optional GRANULARITY parameter `<N>` refers to the size of the index granules (see [here](/docs/optimize/skipping-indexes)).
Unlike regular skip indexes, which use a default index granularity of 1, vector similarity indexes use 100 million as default index granularity.
This value makes sure that only few indexes are build internally even for large parts.
We recommend changing the index granularity only for advanced users who understand the implications of what they are doing (see [below](#differences-to-regular-skipping-indexes)).

Vector similarity indexes are generic in the sense that they can accommodate different approximate search method.
The actually used method is specified by parameter `<type>`.
As of now, the only available method is HNSW ([academic paper](https://arxiv.org/abs/1603.09320)), a popular and state\-of\-the\-art technique for approximate vector search based on hierarchical proximity graphs.
If HNSW is used as type, users may optionally specify further HNSW\-specific parameters:

```
CREATE TABLE table
(
  [...],
  vectors Array(Float*),
  INDEX index_name vectors TYPE vector_similarity('hnsw', <distance_function>, <dimensions>[, <quantization>, <hnsw_max_connections_per_layer>, <hnsw_candidate_list_size_for_construction>]) [GRANULARITY N]
)
ENGINE = MergeTree
ORDER BY [...]

```

These HNSW\-specific parameters are available:
