# Comparison Functions \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Comparison
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/comparison-functions.md)# Comparison Functions

## Comparison rules[​](#comparison-rules "Direct link to Comparison rules")


The comparison functions below return `0` or `1` with type [UInt8](/docs/sql-reference/data-types/int-uint). Only values within the same group can be
compared (e.g. `UInt16` and `UInt64`) but not across groups (e.g. `UInt16` and `DateTime`).
Comparison of numbers and strings are possible, as is comparison of strings with dates and dates with times.
For tuples and arrays, the comparison is lexicographic meaning that the comparison is made for each corresponding
element of the left side and right side tuple/array.


The following types can be compared:


- numbers and decimals
- strings and fixed strings
- dates
- dates with times
- tuples (lexicographic comparison)
- arrays (lexicographic comparison)


NoteStrings are compared byte\-by\-byte. This may lead to unexpected results if one of the strings contains UTF\-8 encoded multi\-byte characters.
A string S1 which has another string S2 as prefix is considered longer than S2\.


## equals[​](#equals "Direct link to equals")


Introduced in: v1\.1\.0


Compares two values for equality.


**Syntax**



```
equals(a, b)
        -- a = b
        -- a == b

```

**Arguments**


- `a` — First value.[\*](#comparison-rules) \- `b` — Second value.[\*](#comparison-rules)


**Returned value**


Returns `1` if `a` is equal to `b`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 1 = 1, 1 = 2;

```


```
┌─equals(1, 1)─┬─equals(1, 2)─┐
│            1 │            0 │
└──────────────┴──────────────┘

```

## globalIn[​](#globalIn "Direct link to globalIn")


Introduced in: v1\.1\.0


Same as `in`, but uses global set distribution in distributed queries. The set is sent to all remote servers.


**Syntax**



```
globalIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 1 IN (1, 2, 3)

```


```
1

```

## globalInIgnoreSet[​](#globalInIgnoreSet "Direct link to globalInIgnoreSet")


Introduced in: v1\.1\.0


Same as `in`, but uses global set distribution in distributed queries. The set is sent to all remote servers.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
globalIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 1 IN (1, 2, 3)

```


```
1

```

## globalNotIn[​](#globalNotIn "Direct link to globalNotIn")


Introduced in: v1\.1\.0


Same as `notIn`, but uses global set distribution in distributed queries. The set is sent to all remote servers.


**Syntax**



```
globalNotIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 4 NOT IN (1, 2, 3)

```


```
1

```

## globalNotInIgnoreSet[​](#globalNotInIgnoreSet "Direct link to globalNotInIgnoreSet")


Introduced in: v1\.1\.0


Same as `notIn`, but uses global set distribution in distributed queries. The set is sent to all remote servers.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
globalNotIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 4 NOT IN (1, 2, 3)

```


```
1

```

## globalNotNullIn[​](#globalNotNullIn "Direct link to globalNotNullIn")


Introduced in: v1\.1\.0


Same as `notNullIn`, but uses global set distribution in distributed queries. The set is sent to all remote servers.


**Syntax**



```
globalNotNullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT notNullIn(NULL, tuple(1, NULL))

```


```
0

```

## globalNotNullInIgnoreSet[​](#globalNotNullInIgnoreSet "Direct link to globalNotNullInIgnoreSet")


Introduced in: v1\.1\.0


Same as `notNullIn`, but uses global set distribution in distributed queries. The set is sent to all remote servers.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
globalNotNullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT notNullIn(NULL, tuple(1, NULL))

```


```
0

```

## globalNullIn[​](#globalNullIn "Direct link to globalNullIn")


Introduced in: v1\.1\.0


Same as `nullIn`, but uses global set distribution in distributed queries. The set is sent to all remote servers.


**Syntax**



```
globalNullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT nullIn(NULL, tuple(1, NULL))

```


```
1

```

## globalNullInIgnoreSet[​](#globalNullInIgnoreSet "Direct link to globalNullInIgnoreSet")


Introduced in: v1\.1\.0


Same as `nullIn`, but uses global set distribution in distributed queries. The set is sent to all remote servers.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
globalNullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT nullIn(NULL, tuple(1, NULL))

```


```
1

```

## greater[​](#greater "Direct link to greater")


Introduced in: v1\.1\.0


Compares two values for greater\-than relation.


**Syntax**



```
greater(a, b)
    -- a > b

```

**Arguments**


- `a` — First value.[\*](#comparison-rules) \- `b` — Second value.[\*](#comparison-rules)


**Returned value**


Returns `1` if `a` is greater than `b`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 2 > 1, 1 > 2;

```


```
┌─greater(2, 1)─┬─greater(1, 2)─┐
│             1 │             0 │
└───────────────┴───────────────┘

```

## greaterOrEquals[​](#greaterOrEquals "Direct link to greaterOrEquals")


Introduced in: v1\.1\.0


Compares two values for greater\-than\-or\-equal\-to relation.


**Syntax**



```
greaterOrEquals(a, b)
    -- a >= b

```

**Arguments**


- `a` — First value.[\*](#comparison-rules) \- `b` — Second value.[\*](#comparison-rules)


**Returned value**


Returns `1` if `a` is greater than or equal to `b`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 2 >= 1, 2 >= 2, 1 >= 2;

```


```
┌─greaterOrEquals(2, 1)─┬─greaterOrEquals(2, 2)─┬─greaterOrEquals(1, 2)─┐
│                     1 │                     1 │                     0 │
└───────────────────────┴───────────────────────┴───────────────────────┘

```

## in[​](#in "Direct link to in")


Introduced in: v1\.1\.0


Checks if the left operand is a member of the right operand set. Returns 1 if it is, 0 otherwise. NULL values in the left operand are skipped (treated as not in the set).


**Syntax**



```
in(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 1 IN (1, 2, 3)

```


```
1

```

## inIgnoreSet[​](#inIgnoreSet "Direct link to inIgnoreSet")


Introduced in: v1\.1\.0


Checks if the left operand is a member of the right operand set. Returns 1 if it is, 0 otherwise. NULL values in the left operand are skipped (treated as not in the set).
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
in(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 1 IN (1, 2, 3)

```


```
1

```

## isDistinctFrom[​](#isDistinctFrom "Direct link to isDistinctFrom")


Introduced in: v25\.11\.0


Performs a null\-safe "not equals" comparison between two values.
Returns `true` if the values are distinct (not equal), including when one value is NULL and the other is not.
Returns `false` if the values are equal, or if both are NULL.


**Syntax**



```
isDistinctFrom(x, y)

```

**Arguments**


- `x` — First value to compare. Can be any ClickHouse data type. [`Any`](/docs/sql-reference/data-types)
- `y` — Second value to compare. Can be any ClickHouse data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `true` if the two values are different, treating NULLs as comparable:


- Returns `true` if x !\= y.
- Returns `true` if exactly one of x or y is NULL.
- Returns `false` if x \= y, or both x and y are NULL. [`Bool`](/docs/sql-reference/data-types/boolean)


**Examples**


**Basic usage with numbers and NULLs**



```
SELECT
    isDistinctFrom(1, 2) AS result_1,
    isDistinctFrom(1, 1) AS result_2,
    isDistinctFrom(NULL, 1) AS result_3,
    isDistinctFrom(NULL, NULL) AS result_4

```


```
┌─result_1─┬─result_2─┬─result_3─┬─result_4─┐
│        1 │        0 │        1 │        0 │
└──────────┴──────────┴──────────┴──────────┘

```

## isNotDistinctFrom[​](#isNotDistinctFrom "Direct link to isNotDistinctFrom")


Introduced in: v23\.8\.0


Performs a null\-safe "equals" comparison between two values.
Returns `true` if the values are equal, including when both are NULL.
Returns `false` if the values are different, or if exactly one of them is NULL.


**Syntax**



```
isNotDistinctFrom(x, y)

```

**Arguments**


- `x` — First value to compare. Can be any ClickHouse data type. [`Any`](/docs/sql-reference/data-types)
- `y` — Second value to compare. Can be any ClickHouse data type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns `true` if the two values are equal, treating NULLs as comparable:


- Returns `true` if x \= y.
- Returns `true` if both x and y are NULL.
- Returns `false` if x !\= y, or exactly one of x or y is NULL. [`Bool`](/docs/sql-reference/data-types/boolean)


**Examples**


**Basic usage with numbers and NULLs**



```
SELECT
    isNotDistinctFrom(1, 1) AS result_1,
    isNotDistinctFrom(1, 2) AS result_2,
    isNotDistinctFrom(NULL, NULL) AS result_3,
    isNotDistinctFrom(NULL, 1) AS result_4

```


```
┌─result_1─┬─result_2─┬─result_3─┬─result_4─┐
│        1 │        0 │        1 │        0 │
└──────────┴──────────┴──────────┴──────────┘

```

## less[​](#less "Direct link to less")


Introduced in: v1\.1\.0


Compares two values for less\-than relation.


**Syntax**



```
less(a, b)
    -- a < b

```

**Arguments**


- `a` — First value.[\*](#comparison-rules) \- `b` — Second value.[\*](#comparison-rules)


**Returned value**


Returns `1` if `a` is less than `b`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 1 < 2, 2 < 1;

```


```
┌─less(1, 2)─┬─less(2, 1)─┐
│          1 │          0 │
└────────────┴────────────┘

```

## lessOrEquals[​](#lessOrEquals "Direct link to lessOrEquals")


Introduced in: v1\.1\.0


Compares two values for less\-than\-or\-equal\-to relation.


**Syntax**



```
lessOrEquals(a, b)
-- a <= b

```

**Arguments**


- `a` — First value.[\*](#comparison-rules) \- `b` — Second value.[\*](#comparison-rules)


**Returned value**


Returns `1` if `a` is less than or equal to `b`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 1 <= 2, 2 <= 2, 3 <= 2;

```


```
┌─lessOrEquals(1, 2)─┬─lessOrEquals(2, 2)─┬─lessOrEquals(3, 2)─┐
│                  1 │                  1 │                  0 │
└────────────────────┴────────────────────┴────────────────────┘

```

## notEquals[​](#notEquals "Direct link to notEquals")


Introduced in: v1\.1\.0


Compares two values for inequality.


**Syntax**



```
notEquals(a, b)
    -- a != b
    -- a <> b

```

**Arguments**


- `a` — First value.[\*](#comparison-rules) \- `b` — Second value.[\*](#comparison-rules)


**Returned value**


Returns `1` if `a` is not equal to `b`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT 1 != 2, 1 != 1;

```


```
┌─notEquals(1, 2)─┬─notEquals(1, 1)─┐
│               1 │               0 │
└─────────────────┴─────────────────┘

```

## notIn[​](#notIn "Direct link to notIn")


Introduced in: v1\.1\.0


Checks if the left operand is NOT a member of the right operand set. Returns 1 if it is not in the set, 0 otherwise. NULL values in the left operand are skipped.


**Syntax**



```
notIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 4 NOT IN (1, 2, 3)

```


```
1

```

## notInIgnoreSet[​](#notInIgnoreSet "Direct link to notInIgnoreSet")


Introduced in: v1\.1\.0


Checks if the left operand is NOT a member of the right operand set. Returns 1 if it is not in the set, 0 otherwise. NULL values in the left operand are skipped.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
notIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT 4 NOT IN (1, 2, 3)

```


```
1

```

## notNullIn[​](#notNullIn "Direct link to notNullIn")


Introduced in: v1\.1\.0


Checks if the left operand is NOT a member of the right operand set. Unlike `notIn`, NULL values are not skipped: NULL is compared with set elements, and NULL \= NULL evaluates to true.


**Syntax**



```
notNullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT notNullIn(NULL, tuple(1, NULL))

```


```
0

```

## notNullInIgnoreSet[​](#notNullInIgnoreSet "Direct link to notNullInIgnoreSet")


Introduced in: v1\.1\.0


Checks if the left operand is NOT a member of the right operand set. Unlike `notIn`, NULL values are not skipped: NULL is compared with set elements, and NULL \= NULL evaluates to true.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
notNullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is not in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT notNullIn(NULL, tuple(1, NULL))

```


```
0

```

## nullIn[​](#nullIn "Direct link to nullIn")


Introduced in: v1\.1\.0


Checks if the left operand is a member of the right operand set. Unlike `in`, NULL values are not skipped: NULL is compared with set elements, and NULL \= NULL evaluates to true.


**Syntax**



```
nullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT nullIn(NULL, tuple(1, NULL))

```


```
1

```

## nullInIgnoreSet[​](#nullInIgnoreSet "Direct link to nullInIgnoreSet")


Introduced in: v1\.1\.0


Checks if the left operand is a member of the right operand set. Unlike `in`, NULL values are not skipped: NULL is compared with set elements, and NULL \= NULL evaluates to true.
This is the IgnoreSet variant used for type analysis without creating the set.


**Syntax**



```
nullIn(x, set)

```

**Arguments**


- `x` — The value to check. \- `set` — The set of values.


**Returned value**


Returns 1 if x is in the set, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT nullIn(NULL, tuple(1, NULL))

```


```
1

```
[PreviousBitmap](/docs/sql-reference/functions/bitmap-functions)[NextConditional](/docs/sql-reference/functions/conditional-functions)- [Comparison rules](#comparison-rules)- [equals](#equals)- [globalIn](#globalIn)- [globalInIgnoreSet](#globalInIgnoreSet)- [globalNotIn](#globalNotIn)- [globalNotInIgnoreSet](#globalNotInIgnoreSet)- [globalNotNullIn](#globalNotNullIn)- [globalNotNullInIgnoreSet](#globalNotNullInIgnoreSet)- [globalNullIn](#globalNullIn)- [globalNullInIgnoreSet](#globalNullInIgnoreSet)- [greater](#greater)- [greaterOrEquals](#greaterOrEquals)- [in](#in)- [inIgnoreSet](#inIgnoreSet)- [isDistinctFrom](#isDistinctFrom)- [isNotDistinctFrom](#isNotDistinctFrom)- [less](#less)- [lessOrEquals](#lessOrEquals)- [notEquals](#notEquals)- [notIn](#notIn)- [notInIgnoreSet](#notInIgnoreSet)- [notNullIn](#notNullIn)- [notNullInIgnoreSet](#notNullInIgnoreSet)- [nullIn](#nullIn)- [nullInIgnoreSet](#nullInIgnoreSet)
Was this page helpful?
