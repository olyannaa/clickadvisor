---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/math-functions.md)#
topic: mathematical-functions-clickhouse-docs
ch_version_introduced: '0.5'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 10
---

# Mathematical functions \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Mathematical
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/math-functions.md)# Mathematical functions

## acos[​](#acos "Direct link to acos")

Introduced in: v1\.1\.0

Returns the arc cosine of the argument.

**Syntax**

```
acos(x)

```

**Arguments**

- `x` — The value for which to find arc cosine of. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)

**Returned value**

Returns the arc cosine of x [`Float*`](/docs/sql-reference/data-types/float)

**Examples**

**Usage example**

```
SELECT acos(0.5);

```

```
1.0471975511965979

```

## acosh[​](#acosh "Direct link to acosh")

Introduced in: v20\.12\.0

Returns the inverse hyperbolic cosine.

**Syntax**

```
acosh(x)

```

**Arguments**

- `x` — Hyperbolic cosine of angle. Values from the interval: `1 ≤ x < +∞`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)

**Returned value**

Returns the angle, in radians. Values from the interval: `0 ≤ acosh(x) < +∞`. [`Float64`](/docs/sql-reference/data-types/float)

**Examples**

**Usage example**

```
SELECT acosh(1)

```

```
0

```

## asin[​](#asin "Direct link to asin")

Introduced in: v1\.1\.0

Calculates the arcsine of the provided argument.
For arguments in the range `[-1, 1]` it returns the value in the range of `[-pi() / 2, pi() / 2]`.

**Syntax**

```
asin(x)

```

**Arguments**

- `x` — Argument for which to calculate arcsine of. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)

**Returned value**

Returns the arcsine value of the provided argument `x` [`Float64`](/docs/sql-reference/data-types/float)

**Examples**

**inverse**

```
SELECT asin(1.0) = pi() / 2, sin(asin(1)), asin(sin(1))

```

```
1 1 1

```

**float32**

```
SELECT toTypeName(asin(1.0::Float32))

```

```
Float64

```

**nan**

```
SELECT asin(1.1), asin(-2), asin(inf), asin(nan)

```

```
nan nan nan nan

```

## asinh[​](#asinh "Direct link to asinh")

Introduced in: v20\.12\.0

Returns the inverse hyperbolic sine.

**Syntax**

```
asinh(x)

```

**Arguments**

- `x` — Hyperbolic sine of angle. Values from the interval: `-∞ < x < +∞`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)

**Returned value**

Returns the angle, in radians. Values from the interval: `-∞ < asinh(x) < +∞`. [`Float64`](/docs/sql-reference/data-types/float)

**Examples**

**Basic usage**

```
SELECT asinh(0)

```

```
0

```

## atan[​](#atan "Direct link to atan")

Introduced in: v1\.1\.0

Returns the arc tangent of the argument.

**Syntax**

```
atan(x)

```

**Arguments**

- `x` — The value for which to find arc tangent of. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal*`](/docs/sql-reference/data-types/decimal)

**Returned value**

Returns the arc tangent of `x`. [`Float*`](/docs/sql-reference/data-types/float)

**Examples**

**Usage example**

```
SELECT atan(1);

```

```
0.7853981633974483

```

## atan2[​](#atan2 "Direct link to atan2")

Introduced in: v20\.12\.0
