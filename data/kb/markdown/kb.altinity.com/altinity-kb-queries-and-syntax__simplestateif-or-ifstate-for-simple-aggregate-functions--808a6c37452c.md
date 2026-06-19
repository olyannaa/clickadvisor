# Simple aggregate functions \& combinators \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. Simple aggregate functions \& combinators
# Simple aggregate functions \& combinators

### Q. What is SimpleAggregateFunction? Are there advantages to use it instead of AggregateFunction in AggregatingMergeTree?

The ClickHouse® SimpleAggregateFunction can be used for those aggregations when the function state is exactly the same as the resulting function value. Typical example is `max` function: it only requires storing the single value which is already maximum, and no extra steps needed to get the final value. In contrast `avg` need to store two numbers \- sum \& count, which should be divided to get the final value of aggregation (done by the `-Merge` step at the very end).



|  | SimpleAggregateFunction | AggregateFunction |
| --- | --- | --- |
| inserting | accepts the value of underlying type ORa value of corresponding SimpleAggregateFunction type`CREATE TABLE saf_test( x SimpleAggregateFunction(max, UInt64) )ENGINE=AggregatingMergeTreeORDER BY tuple();INSERT INTO saf_test VALUES (1);INSERT INTO saf_test SELECT max(number) FROM numbers(10);INSERT INTO saf_test SELECT maxSimpleState(number) FROM numbers(20);` | ONLY accepts the state of same aggregate function calculated using \-State combinator |
| storing | Internally store just a value of underlying type | function\-specific state |
| storage usage | typically is much better due to better compression/codecs | in very rare cases it can be more optimal than raw valuesadaptive granularity doesn't work for large states |
| reading raw value per row | you can access it directly | you need to use `finalizeAggregation` function |
| using aggregated value | just`select max(x) from test;` | you need to use `-Merge` combinator`select maxMerge(x) from test;` |
| memory usage | typically less memory needed (in some corner cases even 10 times) | typically uses more memory, as every state can be quite complex |
| performance | typically better, due to lower overhead | worse |

See also:

- [Altinity Knowledge Base article on AggregatingMergeTree](../../engines/mergetree-table-engine-family/aggregatingmergetree/)
- <https://github.com/ClickHouse/ClickHouse/pull/4629>
- <https://github.com/ClickHouse/ClickHouse/issues/3852>

### Q. How maxSimpleState combinator result differs from plain max?

They produce the same result, but types differ (the first have `SimpleAggregateFunction` datatype). Both can be pushed to SimpleAggregateFunction or to the underlying type. So they are interchangeable.

#### Info

`-SimpleState` is useful for implicit Materialized View creation, like
`CREATE MATERIALIZED VIEW mv ENGINE = AggregatingMergeTree ORDER BY date AS SELECT date, sumSimpleState(1) AS cnt, sumSimpleState(revenue) AS rev FROM table GROUP BY date`#### Warning

`-SimpleState` supported since 21\.1\.
See [https://github.com/ClickHouse/ClickHouse/pull/16853/](https://github.com/ClickHouse/ClickHouse/pull/16853/commits/5b1e5679b4a292e33ee5e60c0ba9cefa1e8388bd)### Q. Can I use \-If combinator with SimpleAggregateFunction?

Something like `SimpleAggregateFunction(maxIf, UInt64, UInt8)` is NOT possible. But is 100% ok to push `maxIf` (or `maxSimpleStateIf`) into `SimpleAggregateFunction(max, UInt64)`

There is one problem with that approach:
`-SimpleStateIf` Would produce 0 as result in case of no\-match, and it can mess up some aggregate functions state. It wouldn’t affect functions like `max/argMax/sum`, but could affect functions like `min/argMin/any/anyLast`


```
SELECT
    minIfMerge(state_1),
    min(state_2)
FROM
(
    SELECT
        minIfState(number, number > 5) AS state_1,
        minSimpleStateIf(number, number > 5) AS state_2
    FROM numbers(5)
    UNION ALL
    SELECT
        minIfState(toUInt64(2), 2),
        minIf(2, 2)
)

┌─minIfMerge(state_1)─┬─min(state_2)─┐
│                   2 │            0 │
└─────────────────────┴──────────────┘

```
You can easily workaround that:

1. Using Nullable datatype.
2. Set result to some big number in case of no\-match, which would be bigger than any possible value, so it would be safe to use. But it would work only for `min/argMin`


```
SELECT
    min(state_1),
    min(state_2)
FROM
(
    SELECT
        minSimpleState(if(number > 5, number, 1000)) AS state_1,
        minSimpleStateIf(toNullable(number), number > 5) AS state_2
    FROM numbers(5)
    UNION ALL
    SELECT
        minIf(2, 2),
        minIf(2, 2)
)

┌─min(state_1)─┬─min(state_2)─┐
│            2 │            2 │
└──────────────┴──────────────┘

```
### Extra example


```
WITH
    minIfState(number, number > 5) AS state_1,
    minSimpleStateIf(number, number > 5) AS state_2
SELECT
    byteSize(state_1),
    toTypeName(state_1),
    byteSize(state_2),
    toTypeName(state_2)
FROM numbers(10)
FORMAT Vertical

-- For UInt64
Row 1:
──────
byteSize(state_1):   24
toTypeName(state_1): AggregateFunction(minIf, UInt64, UInt8)
byteSize(state_2):   8
toTypeName(state_2): SimpleAggregateFunction(min, UInt64)

-- For UInt32
──────
byteSize(state_1):   16
byteSize(state_2):   4

-- For UInt16
──────
byteSize(state_1):   12
byteSize(state_2):   2

-- For UInt8
──────
byteSize(state_1):   10
byteSize(state_2):   1

```
See also <https://gist.github.com/filimonov/a4f6754497f02fcef78e9f23a4d170ee>

Last modified 2024\.08\.13: [Fixed multiple typos here and there (9fb2290\)](https://github.com/Altinity/altinityknowledgebase/commit/9fb2290fbebcd92a3f79a7f321f13960ea89ebec)
