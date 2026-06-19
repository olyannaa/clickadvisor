# Logical functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Logical
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/logical-functions.md)# Logical functions

The functions below perform logical operations on arguments of arbitrary numeric types.
They return either `0` or `1` as [`UInt8`](/docs/sql-reference/data-types/int-uint) or in some cases `NULL`.


Zero as an argument is considered `false`, non\-zero values are considered `true`.


## and[​](#and "Direct link to and")


Introduced in: v1\.1\.0


Calculates the logical conjunction of two or more values.


Setting [`short_circuit_function_evaluation`](/docs/operations/settings/settings#short_circuit_function_evaluation) controls whether short\-circuit evaluation is used.
If enabled, `val_i` is evaluated only if `(val_1 AND val_2 AND ... AND val_{i-1})` is `true`.


For example, with short\-circuit evaluation, no division\-by\-zero exception is thrown when executing the query `SELECT and(number = 2, intDiv(1, number)) FROM numbers(5)`.
Zero as an argument is considered `false`, non\-zero values are considered `true`.


**Syntax**



```
and(val1, val2[, ...])

```

**Arguments**


- `val1, val2[, ...]` — List of at least two values. [`Nullable((U)Int*)`](/docs/sql-reference/data-types/nullable) or [`Nullable(Float*)`](/docs/sql-reference/data-types/nullable)


**Returned value**


Returns:


- `0`, if at least one argument evaluates to `false`
- `NULL`, if no argument evaluates to `false` and at least one argument is `NULL`
- `1`, otherwise
[`Nullable(UInt8)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Basic usage**



```
SELECT and(0, 1, -2);

```


```
0

```

**With NULL**



```
SELECT and(NULL, 1, 10, -2);

```


```
ᴺᵁᴸᴸ

```

## not[​](#not "Direct link to not")


Introduced in: v1\.1\.0


Calculates the logical negation of a value.
Zero as an argument is considered `false`, non\-zero values are considered `true`.


**Syntax**



```
not(val)

```

**Arguments**


- `val` — The value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float)


**Returned value**


Returns:


- `1`, if `val` evaluates to `false`
- `0`, if `val` evaluates to `true`
- `NULL`, if `val` is `NULL`.
[`Nullable(UInt8)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Basic usage**



```
SELECT NOT(1);

```


```
0

```

## or[​](#or "Direct link to or")


Introduced in: v1\.1\.0


Calculates the logical disjunction of two or more values.


Setting [`short_circuit_function_evaluation`](https://clickhouse.com/docs/operations/settings/settings#short_circuit_function_evaluation) controls whether short\-circuit evaluation is used.
If enabled, `val_i` is evaluated only if `((NOT val_1) AND (NOT val_2) AND ... AND (NOT val_{i-1}))` is `true`.


For example, with short\-circuit evaluation, no division\-by\-zero exception is thrown when executing the query `SELECT or(number = 0, intDiv(1, number) != 0) FROM numbers(5)`.
Zero as an argument is considered `false`, non\-zero values are considered `true`.


**Syntax**



```
or(val1, val2[, ...])

```

**Arguments**


- `val1, val2[, ...]` — List of at least two values. [`Nullable((U)Int*)`](/docs/sql-reference/data-types/nullable) or [`Nullable(Float*)`](/docs/sql-reference/data-types/nullable)


**Returned value**


Returns:


- `1`, if at least one argument evaluates to `true`
- `0`, if all arguments evaluate to `false`
- `NULL`, if all arguments evaluate to `false` and at least one argument is `NULL`
[`Nullable(UInt8)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Basic usage**



```
SELECT or(1, 0, 0, 2, NULL);

```


```
1

```

**With NULL**



```
SELECT or(0, NULL);

```


```
ᴺᵁᴸᴸ

```

## xor[​](#xor "Direct link to xor")


Introduced in: v1\.1\.0


Calculates the logical exclusive disjunction of two or more values.
For more than two input values, the function first xor\-s the first two values, then xor\-s the result with the third value etc.
Zero as an argument is considered `false`, non\-zero values are considered `true`.


**Syntax**



```
xor(val1, val2[, ...])

```

**Arguments**


- `val1, val2[, ...]` — List of at least two values. [`Nullable((U)Int*)`](/docs/sql-reference/data-types/nullable) or [`Nullable(Float*)`](/docs/sql-reference/data-types/nullable)


**Returned value**


Returns:


- `1`, for two values: if one of the values evaluates to `false` and other does not
- `0`, for two values: if both values evaluate to `false` or to both `true`
- `NULL`, if at least one of the inputs is `NULL`.
[`Nullable(UInt8)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Basic usage**



```
SELECT xor(0, 1, 1);

```


```
0

```
[PreviousJSON](/docs/sql-reference/functions/json-functions)[NextMachine Learning](/docs/sql-reference/functions/machine-learning-functions)- [and](#and)- [not](#not)- [or](#or)- [xor](#xor)
Was this page helpful?
