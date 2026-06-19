# Array(T) \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- Array(T)
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/array.md)# Array(T)

An array of `T`\-type items, with the starting array index as 1\. `T` can be any data type, including an array.


## Creating an Array[​](#creating-an-array "Direct link to Creating an Array")


You can use a function to create an array:



```
array(T)

```

You can also use `[]`.



```
[]

```

Example of creating an array:



```
SELECT array(1, 2) AS x, toTypeName(x)

```


```
┌─x─────┬─toTypeName(array(1, 2))─┐
│ [1,2] │ Array(UInt8)            │
└───────┴─────────────────────────┘

```


```
SELECT [1, 2] AS x, toTypeName(x)

```


```
┌─x─────┬─toTypeName([1, 2])─┐
│ [1,2] │ Array(UInt8)       │
└───────┴────────────────────┘

```

## Working with Data Types[​](#working-with-data-types "Direct link to Working with Data Types")


When creating an array on the fly, ClickHouse automatically defines the argument type as the narrowest data type that can store all the listed arguments. If there are any [Nullable](/docs/sql-reference/data-types/nullable) or literal [NULL](/docs/operations/settings/formats#input_format_null_as_default) values, the type of an array element also becomes [Nullable](/docs/sql-reference/data-types/nullable).


If ClickHouse couldn't determine the data type, it generates an exception. For instance, this happens when trying to create an array with strings and numbers simultaneously (`SELECT array(1, 'a')`).


Examples of automatic data type detection:



```
SELECT array(1, 2, NULL) AS x, toTypeName(x)

```


```
┌─x──────────┬─toTypeName(array(1, 2, NULL))─┐
│ [1,2,NULL] │ Array(Nullable(UInt8))        │
└────────────┴───────────────────────────────┘

```

If you try to create an array of incompatible data types, ClickHouse throws an exception:



```
SELECT array(1, 'a')

```


```
Received exception from server (version 1.1.54388):
Code: 386. DB::Exception: Received from localhost:9000, 127.0.0.1. DB::Exception: There is no supertype for types UInt8, String because some of them are String/FixedString and some of them are not.

```

## Array Size[​](#array-size "Direct link to Array Size")


It is possible to find the size of an array by using the `size0` subcolumn without reading the whole column. For multi\-dimensional arrays you can use `sizeN-1`, where `N` is the wanted dimension.


**Example**



```
CREATE TABLE t_arr (`arr` Array(Array(Array(UInt32)))) ENGINE = MergeTree ORDER BY tuple();

INSERT INTO t_arr VALUES ([[[12, 13, 0, 1],[12]]]);

SELECT arr.size0, arr.size1, arr.size2 FROM t_arr;

```


```
┌─arr.size0─┬─arr.size1─┬─arr.size2─┐
│         1 │ [2]       │ [[4,1]]   │
└───────────┴───────────┴───────────┘

```

## Reading nested subcolumns from Array[​](#reading-nested-subcolumns-from-array "Direct link to Reading nested subcolumns from Array")


If nested type `T` inside `Array` has subcolumns (for example, if it's a [named tuple](/docs/sql-reference/data-types/tuple)), you can read its subcolumns from an `Array(T)` type with the same subcolumn names. The type of a subcolumn will be `Array` of the type of original subcolumn.


**Example**



```
CREATE TABLE t_arr (arr Array(Tuple(field1 UInt32, field2 String))) ENGINE = MergeTree ORDER BY tuple();
INSERT INTO t_arr VALUES ([(1, 'Hello'), (2, 'World')]), ([(3, 'This'), (4, 'is'), (5, 'subcolumn')]);
SELECT arr.field1, toTypeName(arr.field1), arr.field2, toTypeName(arr.field2) from t_arr;

```


```
┌─arr.field1─┬─toTypeName(arr.field1)─┬─arr.field2────────────────┬─toTypeName(arr.field2)─┐
│ [1,2]      │ Array(UInt32)          │ ['Hello','World']         │ Array(String)          │
│ [3,4,5]    │ Array(UInt32)          │ ['This','is','subcolumn'] │ Array(String)          │
└────────────┴────────────────────────┴───────────────────────────┴────────────────────────┘

```
[PreviousIPv6](/docs/sql-reference/data-types/ipv6)[NextBoolean](/docs/sql-reference/data-types/boolean)- [Creating an Array](#creating-an-array)- [Working with Data Types](#working-with-data-types)- [Array Size](#array-size)- [Reading nested subcolumns from Array](#reading-nested-subcolumns-from-array)
Was this page helpful?
