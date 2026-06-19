# exponentialTimeDecayedMax \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Aggregate functions](/docs/sql-reference/aggregate-functions)- [Aggregate Functions](/docs/sql-reference/aggregate-functions/reference)- exponentialTimeDecayedMax
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/aggregate-functions/reference/exponentialTimeDecayedMax.md)# exponentialTimeDecayedMax

## exponentialTimeDecayedMax[​](#exponentialTimeDecayedMax "Direct link to exponentialTimeDecayedMax")


Introduced in: v21\.12\.0


Returns the maximum of the computed exponentially smoothed moving average at index `t` in time with that at `t-1`.


**Syntax**



```
exponentialTimeDecayedMax(x)(value, timeunit)

```

**Parameters**


- `x` — Half\-life period. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)


**Arguments**


- `value` — Value. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal)
- `timeunit` — Timeunit. [`(U)Int*`](/docs/sql-reference/data-types/int-uint) or [`Float*`](/docs/sql-reference/data-types/float) or [`Decimal`](/docs/sql-reference/data-types/decimal) or [`DateTime`](/docs/sql-reference/data-types/datetime) or [`DateTime64`](/docs/sql-reference/data-types/datetime64)


**Returned value**


Returns the maximum of the exponentially smoothed weighted moving average at `t` and `t-1`. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Window function usage with visual representation**



```
SELECT
    value,
    time,
    round(exp_smooth, 3),
    bar(exp_smooth, 0, 5, 50) AS bar
FROM
    (
    SELECT
    (number = 0) OR (number >= 25) AS value,
    number AS time,
    exponentialTimeDecayedMax(10)(value, time) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS exp_smooth
    FROM numbers(50)
    );

```


```
┌─value─┬─time─┬─round(exp_smooth, 3)─┬─bar────────┐
│     1 │    0 │                    1 │ ██████████ │
│     0 │    1 │                0.905 │ █████████  │
│     0 │    2 │                0.819 │ ████████▏  │
│     0 │    3 │                0.741 │ ███████▍   │
│     0 │    4 │                 0.67 │ ██████▋    │
│     0 │    5 │                0.607 │ ██████     │
│     0 │    6 │                0.549 │ █████▍     │
│     0 │    7 │                0.497 │ ████▉      │
│     0 │    8 │                0.449 │ ████▍      │
│     0 │    9 │                0.407 │ ████       │
│     0 │   10 │                0.368 │ ███▋       │
│     0 │   11 │                0.333 │ ███▎       │
│     0 │   12 │                0.301 │ ███        │
│     0 │   13 │                0.273 │ ██▋        │
│     0 │   14 │                0.247 │ ██▍        │
│     0 │   15 │                0.223 │ ██▏        │
│     0 │   16 │                0.202 │ ██         │
│     0 │   17 │                0.183 │ █▊         │
│     0 │   18 │                0.165 │ █▋         │
│     0 │   19 │                 0.15 │ █▍         │
│     0 │   20 │                0.135 │ █▎         │
│     0 │   21 │                0.122 │ █▏         │
│     0 │   22 │                0.111 │ █          │
│     0 │   23 │                  0.1 │ █          │
│     0 │   24 │                0.091 │ ▉          │
│     1 │   25 │                    1 │ ██████████ │
│     1 │   26 │                    1 │ ██████████ │
│     1 │   27 │                    1 │ ██████████ │
│     1 │   28 │                    1 │ ██████████ │
│     1 │   29 │                    1 │ ██████████ │
│     1 │   30 │                    1 │ ██████████ │
│     1 │   31 │                    1 │ ██████████ │
│     1 │   32 │                    1 │ ██████████ │
│     1 │   33 │                    1 │ ██████████ │
│     1 │   34 │                    1 │ ██████████ │
│     1 │   35 │                    1 │ ██████████ │
│     1 │   36 │                    1 │ ██████████ │
│     1 │   37 │                    1 │ ██████████ │
│     1 │   38 │                    1 │ ██████████ │
│     1 │   39 │                    1 │ ██████████ │
│     1 │   40 │                    1 │ ██████████ │
│     1 │   41 │                    1 │ ██████████ │
│     1 │   42 │                    1 │ ██████████ │
│     1 │   43 │                    1 │ ██████████ │
│     1 │   44 │                    1 │ ██████████ │
│     1 │   45 │                    1 │ ██████████ │
│     1 │   46 │                    1 │ ██████████ │
│     1 │   47 │                    1 │ ██████████ │
│     1 │   48 │                    1 │ ██████████ │
│     1 │   49 │                    1 │ ██████████ │
└───────┴──────┴──────────────────────┴────────────┘

```
[PreviousexponentialTimeDecayedCount](/docs/sql-reference/aggregate-functions/reference/exponentialTimeDecayedCount)[NextexponentialTimeDecayedSum](/docs/sql-reference/aggregate-functions/reference/exponentialTimeDecayedSum)- [exponentialTimeDecayedMax](#exponentialTimeDecayedMax)
Was this page helpful?
