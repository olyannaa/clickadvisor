# Manipulating Constraints \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- CONSTRAINT
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/constraint.md)# Manipulating Constraints

Constraints could be added or deleted using following syntax:



```
ALTER TABLE [db].name [ON CLUSTER cluster] ADD CONSTRAINT [IF NOT EXISTS] constraint_name CHECK expression;
ALTER TABLE [db].name [ON CLUSTER cluster] DROP CONSTRAINT [IF EXISTS] constraint_name;

```

See more on [constraints](/docs/sql-reference/statements/create/table#constraints).


Queries will add or remove metadata about constraints from table, so they are processed immediately.


TipConstraint check **will not be executed** on existing data if it was added.


All changes on replicated tables are broadcast to ZooKeeper and will be applied on other replicas as well.

[PreviousINDEX](/docs/sql-reference/statements/alter/skipping-index)[NextTTL](/docs/sql-reference/statements/alter/ttl)Was this page helpful?
