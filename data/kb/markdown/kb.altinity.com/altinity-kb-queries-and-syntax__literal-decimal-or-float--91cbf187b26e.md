# Imprecise parsing of literal Decimal or Float64 \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. Imprecise literal Decimal or Float64 values
# Imprecise parsing of literal Decimal or Float64

## Decimal


```
SELECT
    9.2::Decimal64(2) AS postgresql_cast,
    toDecimal64(9.2, 2) AS to_function,
    CAST(9.2, 'Decimal64(2)') AS cast_float_literal,
    CAST('9.2', 'Decimal64(2)') AS cast_string_literal

┌─postgresql_cast─┬─to_function─┬─cast_float_literal─┬─cast_string_literal─┐
│             9.2 │        9.19 │               9.19 │                 9.2 │
└─────────────────┴─────────────┴────────────────────┴─────────────────────┘

```

> When we try to type cast 64\.32 to Decimal128(2\) the resulted value is 64\.31\.

When it sees a number with a decimal separator it interprets as `Float64` literal (where `64.32` have no accurate representation, and actually you get something like `64.319999999999999999`) and later that Float is casted to Decimal by removing the extra precision.

Workaround is very simple \- wrap the number in quotes (and it will be considered as a string literal by query parser, and will be transformed to Decimal directly), or use postgres\-alike casting syntax:


```
select cast(64.32,'Decimal128(2)') a, cast('64.32','Decimal128(2)') b, 64.32::Decimal128(2) c;

┌─────a─┬─────b─┬─────c─┐
│ 64.31 │ 64.32 │ 64.32 │
└───────┴───────┴───────┘

```
## Float64


```
SELECT
    toFloat64(15008753.) AS to_func,
    toFloat64('1.5008753E7') AS to_func_scientific,
    CAST('1.5008753E7', 'Float64') AS cast_scientific

┌──to_func─┬─to_func_scientific─┬────cast_scientific─┐
│ 15008753 │ 15008753.000000002 │ 15008753.000000002 │
└──────────┴────────────────────┴────────────────────┘

```
Last modified 2023\.01\.12: [Update literal\-decimal\-or\-float.md (8753c34\)](https://github.com/Altinity/altinityknowledgebase/commit/8753c34078655df0313b59631cec725b0676b33d)
