# fuzzQuery \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- fuzzQuery
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/fuzzQuery.md)# fuzzQuery

Perturbs the given query string with random variations.


## Syntax[​](#syntax "Direct link to Syntax")



```
fuzzQuery(query[, max_query_length[, random_seed]])

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `query` (String) \- The source query to perform the fuzzing on.| `max_query_length` (UInt64\) \- A maximum length the query can get during the fuzzing process.| `random_seed` (UInt64\) \- A random seed for producing stable results. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |


## Returned value[​](#returned_value "Direct link to Returned value")


A table object with a single column containing perturbed query strings.


## Usage Example[​](#usage-example "Direct link to Usage Example")



```
SELECT * FROM fuzzQuery('SELECT materialize(\'a\' AS key) GROUP BY key') LIMIT 2;

```


```
   ┌─query──────────────────────────────────────────────────────────┐
1. │ SELECT 'a' AS key GROUP BY key                                 │
2. │ EXPLAIN PIPELINE compact = true SELECT 'a' AS key GROUP BY key │
   └────────────────────────────────────────────────────────────────┘

```
[PreviousfuzzJSON](/docs/sql-reference/table-functions/fuzzJSON)[NextgenerateRandom](/docs/sql-reference/table-functions/generate)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Usage Example](#usage-example)
Was this page helpful?
