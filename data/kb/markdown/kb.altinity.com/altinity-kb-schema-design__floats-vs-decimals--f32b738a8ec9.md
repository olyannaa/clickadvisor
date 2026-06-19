# Floats vs Decimals \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. Floats vs Decimals
# Floats vs Decimals

Float arithmetics is not accurate: [https://floating\-point\-gui.de/](https://floating-point-gui.de/)

In case you need accurate calculations you should use Decimal datatypes.

### Operations on floats are not associative


```
SELECT (toFloat64(100000000000000000.) + toFloat64(7.5)) - toFloat64(100000000000000000.) AS res

┌─res─┐
│   0 │
└─────┘


SELECT (toFloat64(100000000000000000.) - toFloat64(100000000000000000.)) + toFloat64(7.5) AS res

┌─res─┐
│ 7.5 │
└─────┘

```
### No problem with Decimals:


```
SELECT (toDecimal64(100000000000000000., 1) + toDecimal64(7.5, 1)) - toDecimal64(100000000000000000., 1) AS res

┌─res─┐
│ 7.5 │
└─────┘


SELECT (toDecimal64(100000000000000000., 1) - toDecimal64(100000000000000000., 1)) + toDecimal64(7.5, 1) AS res

┌─res─┐
│ 7.5 │
└─────┘

```
#### Warning

Because ClickHouse® uses MPP order of execution of a single query can vary on each run, and you can get slightly different results from the float column every time you run the query.

Usually, this deviation is small, but it can be significant when some kind of arithmetic operation is performed on very large and very small numbers at the same time.

### Some decimal numbers has no accurate float representation


```
SELECT sum(toFloat64(0.45)) AS res
FROM numbers(10000)

┌───────────────res─┐
│ 4499.999999999948 │
└───────────────────┘


SELECT sumKahan(toFloat64(0.45)) AS res
FROM numbers(10000)

┌──res─┐
│ 4500 │
└──────┘


SELECT toFloat32(0.6) * 6 AS res

┌────────────────res─┐
│ 3.6000001430511475 │
└────────────────────┘

```
### No problem with Decimal:


```
SELECT sum(toDecimal64(0.45, 2)) AS res
FROM numbers(10000)

┌──res─┐
│ 4500 │
└──────┘


SELECT toDecimal32(0.6, 1) * 6 AS res

┌─res─┐
│ 3.6 │
└─────┘

```
### Direct comparisons of floats may be impossible

The same number can have several floating\-point representations and because of that you should not compare Floats directly


```
SELECT (toFloat32(0.1) * 10) = (toFloat32(0.01) * 100) AS res

┌─res─┐
│   0 │
└─────┘


SELECT
    sumIf(0.1, number < 10) AS a,
    sumIf(0.01, number < 100) AS b,
    a = b AS a_eq_b
FROM numbers(100)

┌──────────────────a─┬──────────────────b─┬─a_eq_b─┐
│ 0.9999999999999999 │ 1.0000000000000004 │      0 │
└────────────────────┴────────────────────┴────────┘

```
See also

[https://randomascii.wordpress.com/2012/02/25/comparing\-floating\-point\-numbers\-2012\-edition/](https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/)
[https://stackoverflow.com/questions/4915462/how\-should\-i\-do\-floating\-point\-comparison](https://stackoverflow.com/questions/4915462/how-should-i-do-floating-point-comparison)
[https://stackoverflow.com/questions/2100490/floating\-point\-inaccuracy\-examples](https://stackoverflow.com/questions/2100490/floating-point-inaccuracy-examples)
[https://stackoverflow.com/questions/10371857/is\-floating\-point\-addition\-and\-multiplication\-associative](https://stackoverflow.com/questions/10371857/is-floating-point-addition-and-multiplication-associative)

But:

<https://github.com/ClickHouse/ClickHouse/issues/24909>

Last modified 2024\.07\.30: [Site cleanup, mostly minor changes (a4a9639\)](https://github.com/Altinity/altinityknowledgebase/commit/a4a96398d6e97ac2935110b426947487e2e202d9)
