# PARALLEL WITH Clause \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- PARALLEL WITH
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/parallel_with.md)# PARALLEL WITH Clause

Allows to execute multiple statements in parallel.


## Syntax[​](#syntax "Direct link to Syntax")



```
statement1 PARALLEL WITH statement2 [PARALLEL WITH statement3 ...]

```

Executes statements `statement1`, `statement2`, `statement3`, ... in parallel with each other. The output of those statements is discarded.


Executing statements in parallel may be faster than just a sequence of the same statements in many cases. For example, `statement1 PARALLEL WITH statement2 PARALLEL WITH statement3` is likely to be faster than `statement1; statement2; statement3`.


## Examples[​](#examples "Direct link to Examples")


Creates two tables in parallel:



```
CREATE TABLE table1(x Int32) ENGINE = MergeTree ORDER BY tuple()
PARALLEL WITH
CREATE TABLE table2(y String) ENGINE = MergeTree ORDER BY tuple();

```

Drops two tables in parallel:



```
DROP TABLE table1
PARALLEL WITH
DROP TABLE table2;

```

## Settings[​](#settings "Direct link to Settings")


Setting [max\_threads](/docs/operations/settings/settings#max_threads) controls how many threads are spawned.


## Comparison with UNION[​](#comparison-with-union "Direct link to Comparison with UNION")


The `PARALLEL WITH` clause is a bit similar to [UNION](/docs/sql-reference/statements/select/union), which also executes its operands in parallel. However there are some differences:


- `PARALLEL WITH` doesn't return any results from executing its operands, it can only rethrow an exception from them if any;
- `PARALLEL WITH` doesn't require its operands to have the same set of result columns;
- `PARALLEL WITH` can execute any statements (not just `SELECT`).
[PreviousEXECUTE AS](/docs/sql-reference/statements/execute_as)[NextUSE](/docs/sql-reference/statements/use)- [Syntax](#syntax)- [Examples](#examples)- [Settings](#settings)- [Comparison with UNION](#comparison-with-union)
Was this page helpful?
