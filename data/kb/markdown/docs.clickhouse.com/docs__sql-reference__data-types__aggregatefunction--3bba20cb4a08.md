# AggregateFunction Type \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- AggregateFunction
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/aggregatefunction.md)# AggregateFunction Type

## Description[​](#description "Direct link to Description")


All [Aggregate functions](/docs/sql-reference/aggregate-functions) in ClickHouse have
an implementation\-specific intermediate state that can be serialized to an
`AggregateFunction` data type and stored in a table. This is usually done by
means of a [materialized view](/docs/sql-reference/statements/create/view).


There are two aggregate function [combinators](/docs/sql-reference/aggregate-functions/combinators)
commonly used with the `AggregateFunction` type:


- The [`-State`](/docs/sql-reference/aggregate-functions/combinators#-state) aggregate function combinator, which when appended to an aggregate
function name, produces `AggregateFunction` intermediate states.
- The [`-Merge`](/docs/sql-reference/aggregate-functions/combinators#-merge) aggregate
function combinator, which is used to get the final result of an aggregation
from the intermediate states.


## Syntax[​](#syntax "Direct link to Syntax")



```
AggregateFunction(aggregate_function_name, types_of_arguments...)

```

**Parameters**


- `aggregate_function_name` \- The name of an aggregate function. If the function
is parametric, then its parameters should be specified too.
- `types_of_arguments` \- The types of the aggregate function arguments.


for example:



```
CREATE TABLE t
(
    column1 AggregateFunction(uniq, UInt64),
    column2 AggregateFunction(anyIf, String, UInt8),
    column3 AggregateFunction(quantiles(0.5, 0.9), UInt64)
) ENGINE = ...

```

## Usage[​](#usage "Direct link to Usage")


### Data Insertion[​](#data-insertion "Direct link to Data Insertion")


To insert data into a table with columns of type `AggregateFunction`, you can
use `INSERT SELECT` with aggregate functions and the
[`-State`](/docs/sql-reference/aggregate-functions/combinators#-state) aggregate
function combinator.


For example, to insert into columns of type `AggregateFunction(uniq, UInt64)` and
`AggregateFunction(quantiles(0.5, 0.9), UInt64)` you would use the following
aggregate functions with combinators.



```
uniqState(UserID)
quantilesState(0.5, 0.9)(SendTiming)

```

In contrast to functions `uniq` and `quantiles`, `uniqState` and `quantilesState`
(with `-State` combinator appended) return the state, rather than the final value.
In other words, they return a value of `AggregateFunction` type.


In the results of the `SELECT` query, values of type `AggregateFunction` have
implementation\-specific binary representations for all of the ClickHouse output
formats.


There is a special Session level setting `aggregate_function_input_format` that allows to build state from the input values.
It supports the following formats:


- `state` \- binary string with the serialized state (the default).
If you dump data into, for example, the `TabSeparated` format with a `SELECT`
query, then this dump can be loaded back using the `INSERT` query.
- `value` \- the format will expect a single value of the argument of the aggregate function, or in the case of multiple arguments, a tuple of them; that will be deserialized to form the relevant state
- `array` \- the format will expect an Array of values, as described in the values option above; all the elements of the array will be aggregated to form the state


### Data Selection[​](#data-selection "Direct link to Data Selection")


When selecting data from `AggregatingMergeTree` table, use the `GROUP BY` clause
and the same aggregate functions as for when you inserted the data, but use the
[`-Merge`](/docs/sql-reference/aggregate-functions/combinators#-merge) combinator.


An aggregate function with the `-Merge` combinator appended to it takes a set of
states, combines them, and returns the result of the complete data aggregation.


For example, the following two queries return the same result:



```
SELECT uniq(UserID) FROM table

SELECT uniqMerge(state) FROM (SELECT uniqState(UserID) AS state FROM table GROUP BY RegionID)

```

## Usage Example[​](#usage-example "Direct link to Usage Example")


See [AggregatingMergeTree](/docs/engines/table-engines/mergetree-family/aggregatingmergetree) engine description.


## Related Content[​](#related-content "Direct link to Related Content")


- Blog: [Using Aggregate Combinators in ClickHouse](https://clickhouse.com/blog/aggregate-functions-combinators-in-clickhouse-for-arrays-maps-and-states)
- [MergeState](/docs/sql-reference/aggregate-functions/combinators#-mergestate)
combinator.
- [State](/docs/sql-reference/aggregate-functions/combinators#-state) combinator.
[PreviousNullable(T)](/docs/sql-reference/data-types/nullable)[NextSimpleAggregateFunction](/docs/sql-reference/data-types/simpleaggregatefunction)- [Description](#description)- [Syntax](#syntax)- [Usage](#usage)
	- [Data Insertion](#data-insertion)- [Data Selection](#data-selection)- [Usage Example](#usage-example)- [Related Content](#related-content)
Was this page helpful?
