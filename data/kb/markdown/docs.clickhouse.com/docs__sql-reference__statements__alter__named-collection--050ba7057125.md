# ALTER NAMED COLLECTION \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- NAMED COLLECTION
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/named-collection.md)Not supported in ClickHouse Cloud
# ALTER NAMED COLLECTION


This query intends to modify already existing named collections.


**Syntax**



```
ALTER NAMED COLLECTION [IF EXISTS] name [ON CLUSTER cluster]
[ SET
key_name1 = 'some value' [[NOT] OVERRIDABLE],
key_name2 = 'some value' [[NOT] OVERRIDABLE],
key_name3 = 'some value' [[NOT] OVERRIDABLE],
... ] |
[ DELETE key_name4, key_name5, ... ]

```

**Example**



```
CREATE NAMED COLLECTION foobar AS a = '1' NOT OVERRIDABLE, b = '2';

ALTER NAMED COLLECTION foobar SET a = '2' OVERRIDABLE, c = '3';

ALTER NAMED COLLECTION foobar DELETE b;

```
[PreviousALTER DATABASE ... MODIFY COMMENT](/docs/sql-reference/statements/alter/database-comment)[NextDELETE](/docs/sql-reference/statements/delete)Was this page helpful?
