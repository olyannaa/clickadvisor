# distinctDynamicTypes \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- distinctDynamicTypes
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/distinctDynamicTypes.md)# distinctDynamicTypes

## distinctDynamicTypes[​](#distinctDynamicTypes "Direct link to distinctDynamicTypes")


Introduced in: v24\.9\.0


Calculates the list of distinct data types stored in [Dynamic](https://clickhouse.com/docs/sql-reference/data-types/dynamic) column.


**Syntax**



```
distinctDynamicTypes(dynamic)

```

**Arguments**


- `dynamic` — Dynamic column. [`Dynamic`](/docs/sql-reference/data-types/dynamic)


**Returned value**


Returns the sorted list of data type names. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Basic usage with mixed types**



```
DROP TABLE IF EXISTS test_dynamic;
CREATE TABLE test_dynamic(d Dynamic) ENGINE = Memory;
INSERT INTO test_dynamic VALUES (42), (NULL), ('Hello'), ([1, 2, 3]), ('2020-01-01'), (map(1, 2)), (43), ([4, 5]), (NULL), ('World'), (map(3, 4));

SELECT distinctDynamicTypes(d) FROM test_dynamic;

```


```
┌─distinctDynamicTypes(d)──────────────────────────────────────────┐
│ ['Array(Int64)', 'Date', 'Int64', 'Map(UInt8, UInt8)', 'String'] │
└──────────────────────────────────────────────────────────────────┘

```
[PreviousdeltaSumTimestamp](/docs/sql-reference/aggregate-functions/reference/deltasumtimestamp)[NextdistinctJSONPaths](/docs/sql-reference/aggregate-functions/reference/distinctjsonpaths)- [distinctDynamicTypes](#distinctDynamicTypes)
Was this page helpful?
