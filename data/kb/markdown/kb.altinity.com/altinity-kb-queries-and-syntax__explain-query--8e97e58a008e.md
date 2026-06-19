# EXPLAIN query \| Altinity® Knowledge Base for ClickHouse®


1. [Queries \& Syntax](/altinity-kb-queries-and-syntax/)
2. EXPLAIN query
# EXPLAIN query

### EXPLAIN types


```
EXPLAIN AST
        SYNTAX
        PLAN indexes = 0,
             header = 0,
             description = 1,
             actions = 0,
             optimize = 1
             json = 0
        PIPELINE header = 0,
                 graph = 0,
                 compact = 1
        ESTIMATE
SELECT ...

```
- `AST` \- abstract syntax tree
- `SYNTAX` \- query text after AST\-level optimizations
- `PLAN` \- query execution plan
- `PIPELINE` \- query execution pipeline
- `ESTIMATE` \- See [Estimates for select query](https://github.com/ClickHouse/ClickHouse/pull/26131)
, available since ClickHouse® 21\.9
- `indexes=1` supported starting from 21\.6 (<https://github.com/ClickHouse/ClickHouse/pull/22352>
)
- `json=1` supported starting from 21\.6 (<https://github.com/ClickHouse/ClickHouse/pull/23082>
)

References

- [https://clickhouse.com/docs/en/sql\-reference/statements/explain/](https://clickhouse.com/docs/en/sql-reference/statements/explain/)
- Nikolai Kochetov from Yandeх. EXPLAIN query in ClickHouse. [slides](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup47/explain.pdf)
, [video](https://youtu.be/ckChUkC3Pns?t=1387)
- [https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup39/query\-profiling.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup39/query-profiling.pdf)
- <https://github.com/ClickHouse/ClickHouse/issues/28847>

Last modified 2024\.07\.29: [Site cleanup, mostly minor changes (3e41a19\)](https://github.com/Altinity/altinityknowledgebase/commit/3e41a19644b66d46db743db20321bd5b94b545df)
