# Avoid nullable columns \| ClickHouse Docs


- - [Performance and optimizations](/docs/operations/overview)- Avoid nullable columns
[Edit this page](https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/best-practices/avoidnullablecolumns.md)# Avoid nullable columns

[`Nullable` column](/docs/sql-reference/data-types/nullable) (e.g. `Nullable(String)`) creates a separate column of `UInt8` type. This additional column has to be processed every time a user works with a Nullable column. This leads to additional storage space used and almost always negatively affects performance.


To avoid `Nullable` columns, consider setting a default value for that column. For example, instead of:



```
CREATE TABLE default.sample
(
    `x` Int8,
    -- highlight-next-line
    `y` Nullable(Int8)
)
ENGINE = MergeTree
ORDER BY x

```

use



```
CREATE TABLE default.sample2
(
    `x` Int8,
    -- highlight-next-line
    `y` Int8 DEFAULT 0
)
ENGINE = MergeTree
ORDER BY x

```

Consider your use case; a default value may be inappropriate.

[PreviousAvoid mutations](/docs/optimize/avoid-mutations)[NextAvoid optimize final](/docs/optimize/avoidoptimizefinal)Was this page helpful?
