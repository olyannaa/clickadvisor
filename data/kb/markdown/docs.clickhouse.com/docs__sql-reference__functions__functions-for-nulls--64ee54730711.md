# Functions for working with nullable values \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Nullable
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/functions-for-nulls.md)# Functions for working with nullable values

## assumeNotNull[​](#assumeNotNull "Direct link to assumeNotNull")


Introduced in: v1\.1\.0


Returns the corresponding non\-`Nullable` value for a value of type [`Nullable`](/docs/sql-reference/data-types/nullable).
If the original value is `NULL`, an arbitrary result can be returned.


See also: functions [`ifNull`](#ifNull) and [`coalesce`](#coalesce).


**Syntax**



```
assumeNotNull(x)

```

**Arguments**


- `x` — The original value of any nullable type. [`Nullable(T)`](/docs/sql-reference/data-types/nullable)


**Returned value**


Returns the non\-nullable value, if the original value was not `NULL`, otherwise an arbitrary value, if the input value is `NULL`. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Usage example**



```
CREATE TABLE t_null (x Int8, y Nullable(Int8))
ENGINE=MergeTree()
ORDER BY x;

INSERT INTO t_null VALUES (1, NULL), (2, 3);

SELECT assumeNotNull(y) FROM table;
SELECT toTypeName(assumeNotNull(y)) FROM t_null;

```


```
┌─assumeNotNull(y)─┐
│                0 │
│                3 │
└──────────────────┘
┌─toTypeName(assumeNotNull(y))─┐
│ Int8                         │
│ Int8                         │
└──────────────────────────────┘

```

## coalesce[​](#coalesce "Direct link to coalesce")


Introduced in: v1\.1\.0


Returns the leftmost non\-`NULL` argument.


**Syntax**



```
coalesce(x[, y, ...])

```

**Arguments**


- `x[, y, ...]` — Any number of parameters of non\-compound type. All parameters must be of mutually compatible data types. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the first non\-`NULL` argument, otherwise `NULL`, if all arguments are `NULL`. [`Any`](/docs/sql-reference/data-types) or [`NULL`](/docs/sql-reference/syntax#null)


**Examples**


**Usage example**



```
-- Consider a list of contacts that may specify multiple ways to contact a customer.

CREATE TABLE aBook
(
    name String,
    mail Nullable(String),
    phone Nullable(String),
    telegram Nullable(UInt32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO aBook VALUES ('client 1', NULL, '123-45-67', 123), ('client 2', NULL, NULL, NULL);

-- The mail and phone fields are of type String, but the telegram field is UInt32 so it needs to be converted to String.

-- Get the first available contact method for the customer from the contact list

SELECT name, coalesce(mail, phone, CAST(telegram,'Nullable(String)')) FROM aBook;

```


```
┌─name─────┬─coalesce(mail, phone, CAST(telegram, 'Nullable(String)'))─┐
│ client 1 │ 123-45-67                                                 │
│ client 2 │ ᴺᵁᴸᴸ                                                      │
└──────────┴───────────────────────────────────────────────────────────┘

```

## firstNonDefault[​](#firstNonDefault "Direct link to firstNonDefault")


Introduced in: v25\.9\.0


Returns the first non\-default value from a set of arguments


**Syntax**



```
firstNonDefault(arg1[, arg2[ ...]])

```

**Arguments**


- `arg1` — The first argument to check \- `arg2` — The second argument to check \- `...` — Additional arguments to check


**Returned value**


Result type is the supertype of all arguments


**Examples**


**integers**



```
SELECT firstNonDefault(0, 1, 2)

```


```
1

```

**strings**



```
SELECT firstNonDefault('', 'hello', 'world')

```


```
'hello'

```

**nulls**



```
SELECT firstNonDefault(NULL, 0 :: UInt8, 1 :: UInt8)

```


```
1

```

**nullable zero**



```
SELECT firstNonDefault(NULL, 0 :: Nullable(UInt8), 1 :: Nullable(UInt8))

```


```
0

```

## ifNull[​](#ifNull "Direct link to ifNull")


Introduced in: v1\.1\.0


Returns an alternative value if the first argument is `NULL`.


**Syntax**



```
ifNull(x, alt)

```

**Arguments**


- `x` — The value to check for `NULL`. [`Any`](/docs/sql-reference/data-types)
- `alt` — The value that the function returns if `x` is `NULL`. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the value of `x` if it is not `NULL`, otherwise `alt`. [`Any`](/docs/sql-reference/data-types)


**Examples**


**Usage example**



```
SELECT ifNull('a', 'b'), ifNull(NULL, 'b');

```


```
┌─ifNull('a', 'b')─┬─ifNull(NULL, 'b')─┐
│ a                │ b                 │
└──────────────────┴───────────────────┘

```

## isNotNull[​](#isNotNull "Direct link to isNotNull")


Introduced in: v1\.1\.0


Checks if the argument is not `NULL`.


Also see: operator [`IS NOT NULL`](/docs/sql-reference/operators#is_not_null).


**Syntax**



```
isNotNull(x)

```

**Arguments**


- `x` — A value of non\-compound data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `1` if `x` is not `NULL`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE t_null
(
  x Int32,
  y Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO t_null VALUES (1, NULL), (2, 3);

SELECT x FROM t_null WHERE isNotNull(y);

```


```
┌─x─┐
│ 2 │
└───┘

```

## isNull[​](#isNull "Direct link to isNull")


Introduced in: v1\.1\.0


Checks if the argument is `NULL`.


Also see: operator [`IS NULL`](/docs/sql-reference/operators#is_null).


**Syntax**



```
isNull(x)

```

**Arguments**


- `x` — A value of non\-compound data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `1` if `x` is `NULL`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE t_null
(
  x Int32,
  y Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO t_null VALUES (1, NULL), (2, 3);

SELECT x FROM t_null WHERE isNull(y);

```


```
┌─x─┐
│ 1 │
└───┘

```

## isNullable[​](#isNullable "Direct link to isNullable")


Introduced in: v22\.7\.0


Checks whether the argument's data type is `Nullable` (i.e it allows `NULL` values).


**Syntax**



```
isNullable(x)

```

**Arguments**


- `x` — A value of any data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `1` if `x` is of a `Nullable` data type, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
CREATE TABLE tab (
    ordinary_col UInt32,
    nullable_col Nullable(UInt32)
)
ENGINE = MergeTree
ORDER BY tuple();
INSERT INTO tab (ordinary_col, nullable_col) VALUES (1,1), (2, 2), (3,3);
SELECT isNullable(ordinary_col), isNullable(nullable_col) FROM tab;

```


```
┌───isNullable(ordinary_col)──┬───isNullable(nullable_col)──┐
│                           0 │                           1 │
│                           0 │                           1 │
│                           0 │                           1 │
└─────────────────────────────┴─────────────────────────────┘

```

## isZeroOrNull[​](#isZeroOrNull "Direct link to isZeroOrNull")


Introduced in: v20\.3\.0


Checks if the argument is either zero (`0`) or `NULL`.


**Syntax**



```
isZeroOrNull(x)

```

**Arguments**


- `x` — A numeric value. [`UInt`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns `1` if `x` is `NULL` or equal to zero, otherwise `0`. [`UInt8/16/32/64`](/docs/sql-reference/data-types/int-uint) or [`Float32/Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
CREATE TABLE t_null
(
  x Int32,
  y Nullable(Int32)
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO t_null VALUES (1, NULL), (2, 0), (3, 3);

SELECT x FROM t_null WHERE isZeroOrNull(y);

```


```
┌─x─┐
│ 1 │
│ 2 │
└───┘

```

## nullIf[​](#nullIf "Direct link to nullIf")


Introduced in: v1\.1\.0


Returns `NULL` if both arguments are equal.


**Syntax**



```
nullIf(x, y)

```

**Arguments**


- `x` — The first value. [`Any`](/docs/sql-reference/data-types)
- `y` — The second value. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `NULL` if both arguments are equal, otherwise returns the first argument. [`NULL`](/docs/sql-reference/syntax#null) or [`Nullable(x)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT nullIf(1, 1), nullIf(1, 2);

```


```
┌─nullIf(1, 1)─┬─nullIf(1, 2)─┐
│         ᴺᵁᴸᴸ │            1 │
└──────────────┴──────────────┘

```

## toNullable[​](#toNullable "Direct link to toNullable")


Introduced in: v1\.1\.0


Converts the provided argument type to `Nullable`.


**Syntax**



```
toNullable(x)

```

**Arguments**


- `x` — A value of any non\-compound type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the input value but of `Nullable` type. [`Nullable(Any)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT toTypeName(10), toTypeName(toNullable(10));

```


```
┌─toTypeName(10)─┬─toTypeName(toNullable(10))─┐
│ UInt8          │ Nullable(UInt8)            │
└────────────────┴────────────────────────────┘

```
[PreviousFinancial](/docs/sql-reference/functions/financial-functions)[NextGeo](/docs/sql-reference/functions/geo)- [assumeNotNull](#assumeNotNull)- [coalesce](#coalesce)- [firstNonDefault](#firstNonDefault)- [ifNull](#ifNull)- [isNotNull](#isNotNull)- [isNull](#isNull)- [isNullable](#isNullable)- [isZeroOrNull](#isZeroOrNull)- [nullIf](#nullIf)- [toNullable](#toNullable)
Was this page helpful?
