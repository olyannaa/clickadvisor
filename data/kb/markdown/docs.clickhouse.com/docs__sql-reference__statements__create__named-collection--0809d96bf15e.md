# CREATE NAMED COLLECTION \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- NAMED COLLECTION
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/named-collection.md)Not supported in ClickHouse Cloud
# CREATE NAMED COLLECTION


Creates a new named collection.


**Syntax**



```
CREATE NAMED COLLECTION [IF NOT EXISTS] name [ON CLUSTER cluster] AS
key_name1 = 'some value' [[NOT] OVERRIDABLE],
key_name2 = 'some value' [[NOT] OVERRIDABLE],
key_name3 = 'some value' [[NOT] OVERRIDABLE],
...

```

**Example**



```
CREATE NAMED COLLECTION foobar AS a = '1', b = '2' OVERRIDABLE;

```

**Related statements**


- [CREATE NAMED COLLECTION](/docs/sql-reference/statements/alter/named-collection)
- [DROP NAMED COLLECTION](/docs/sql-reference/statements/drop#drop-function)


**See Also**


- [Named collections guide](/docs/operations/named-collections)
[PreviousSETTINGS PROFILE](/docs/sql-reference/statements/create/settings-profile)[NextALTER](/docs/sql-reference/statements/alter)Was this page helpful?
