# CREATE FUNCTION \-user defined function (UDF) \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- FUNCTION
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/function.md)# CREATE FUNCTION \-user defined function (UDF)

Creates a user defined function (UDF) from a lambda expression. The expression must consist of function parameters, constants, operators, or other function calls.


**Syntax**



```
CREATE [OR REPLACE] FUNCTION name [ON CLUSTER cluster] AS (parameter0, ...) -> expression

```

A function can have an arbitrary number of parameters.


There are a few restrictions:


- The name of a function must be unique among user defined and system functions.
- Recursive functions are not allowed.
- All variables used by a function must be specified in its parameter list.


If any restriction is violated then an exception is raised.


**Example**



```
CREATE FUNCTION linear_equation AS (x, k, b) -> k*x + b;
SELECT number, linear_equation(number, 2, 1) FROM numbers(3);

```


```
┌─number─┬─plus(multiply(2, number), 1)─┐
│      0 │                            1 │
│      1 │                            3 │
│      2 │                            5 │
└────────┴──────────────────────────────┘

```

A [conditional function](/docs/sql-reference/functions/conditional-functions) is called in a user defined function in the following query:



```
CREATE FUNCTION parity_str AS (n) -> if(n % 2, 'odd', 'even');
SELECT number, parity_str(number) FROM numbers(3);

```


```
┌─number─┬─if(modulo(number, 2), 'odd', 'even')─┐
│      0 │ even                                 │
│      1 │ odd                                  │
│      2 │ even                                 │
└────────┴──────────────────────────────────────┘

```

Replace an existing UDF:



```
CREATE FUNCTION exampleReplaceFunction AS frame -> frame;
SELECT create_query FROM system.functions WHERE name = 'exampleReplaceFunction';
CREATE OR REPLACE FUNCTION exampleReplaceFunction AS frame -> frame + 1;
SELECT create_query FROM system.functions WHERE name = 'exampleReplaceFunction';

```


```
┌─create_query─────────────────────────────────────────────┐
│ CREATE FUNCTION exampleReplaceFunction AS frame -> frame │
└──────────────────────────────────────────────────────────┘

┌─create_query───────────────────────────────────────────────────┐
│ CREATE FUNCTION exampleReplaceFunction AS frame -> (frame + 1) │
└────────────────────────────────────────────────────────────────┘

```

## Related Content[​](#related-content "Direct link to Related Content")


### [Executable UDFs](/docs/sql-reference/functions/udf).[​](#executable-udfs "Direct link to executable-udfs")


### [User\-defined functions in ClickHouse Cloud](https://clickhouse.com/blog/user-defined-functions-clickhouse-udfs)[​](#user-defined-functions-in-clickhouse-cloud "Direct link to user-defined-functions-in-clickhouse-cloud")

[PreviousVIEW](/docs/sql-reference/statements/create/view)[NextUSER](/docs/sql-reference/statements/create/user)- [Related Content](#related-content)
	- [Executable UDFs.](#executable-udfs)- [User\-defined functions in ClickHouse Cloud](#user-defined-functions-in-clickhouse-cloud)
Was this page helpful?
