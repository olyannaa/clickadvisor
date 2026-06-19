---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/topKWeighted.md)#
topic: topkweighted-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# topKWeighted \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- topKWeighted
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/topKWeighted.md)# topKWeighted

## topKWeighted[​](#topKWeighted "Direct link to topKWeighted")

Introduced in: v1\.1\.0

Returns an array of the approximately most frequent values in the specified column.
The resulting array is sorted in descending order of approximate frequency of values (not by the values themselves).
Additionally, the weight of the value is taken into account.

**See Also**

- [topK](/docs/sql-reference/aggregate-functions/reference/topk)
- [approx\_top\_k](/docs/sql-reference/aggregate-functions/reference/approxtopk)
- [approx\_top\_sum](/docs/sql-reference/aggregate-functions/reference/approxtopsum)

**Syntax**

```
topKWeighted(N)(column, weight)
topKWeighted(N, load_factor)(column, weight)
topKWeighted(N, load_factor, 'counts')(column, weight)

```

**Parameters**

- `N` — The number of elements to return. Default value: 10\. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `load_factor` — Optional. Defines, how many cells reserved for values. If `uniq(column) > N * load_factor`, result of topK function will be approximate. Default value: 3\. [`UInt64`](/docs/sql-reference/data-types/int-uint)
- `counts` — Optional. Defines whether the result should contain an approximate count and error value. [`Bool`](/docs/sql-reference/data-types/boolean)

**Arguments**

- `column` — The name of the column for which to find the most frequent values. \- `weight` — The weight. Every value is accounted `weight` times for frequency calculation. [`UInt64`](/docs/sql-reference/data-types/int-uint)

**Returned value**

Returns an array of the values with maximum approximate sum of weights. [`Array`](/docs/sql-reference/data-types/array)

**Examples**

**Usage example**

```
SELECT topKWeighted(2)(k, w) FROM
VALUES('k Char, w UInt64', ('y', 1), ('y', 1), ('x', 5), ('y', 1), ('z', 10));

```

```
┌─topKWeighted(2)(k, w)──┐
│ ['z','x']              │
└────────────────────────┘

```

**With counts parameter**

```
SELECT topKWeighted(2, 10, 'counts')(k, w)
FROM VALUES('k Char, w UInt64', ('y', 1), ('y', 1), ('x', 5), ('y', 1), ('z', 10));

```

```
┌─topKWeighted(2, 10, 'counts')(k, w)─┐
│ [('z',10,0),('x',5,0)]              │
└─────────────────────────────────────┘

```

**See Also**

- [topK](/docs/sql-reference/aggregate-functions/reference/topk)
- [approx\_top\_k](/docs/sql-reference/aggregate-functions/reference/approxtopk)
- [approx\_top\_sum](/docs/sql-reference/aggregate-functions/reference/approxtopsum)
[PrevioustopK](/docs/sql-reference/aggregate-functions/reference/topk)[Nextuniq](/docs/sql-reference/aggregate-functions/reference/uniq)- [topKWeighted](#topKWeighted)
Was this page helpful?
