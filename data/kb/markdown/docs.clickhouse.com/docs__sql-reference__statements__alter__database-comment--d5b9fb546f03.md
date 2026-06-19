# ALTER DATABASE ... MODIFY COMMENT Statements \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- ALTER DATABASE ... MODIFY COMMENT
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/database-comment.md)# ALTER DATABASE ... MODIFY COMMENT Statements

Adds, modifies, or removes a database comment, regardless of whether it was set
before or not. The comment change is reflected in both [`system.databases`](/docs/operations/system-tables/databases)
and the `SHOW CREATE DATABASE` query.


## Syntax[​](#syntax "Direct link to Syntax")



```
ALTER DATABASE [db].name [ON CLUSTER cluster] MODIFY COMMENT 'Comment'

```

## Examples[​](#examples "Direct link to Examples")


To create a `DATABASE` with a comment:



```
CREATE DATABASE database_with_comment ENGINE = Memory COMMENT 'The temporary database';

```

To modify the comment:



```
ALTER DATABASE database_with_comment 
MODIFY COMMENT 'new comment on a database';

```

To view the modified comment:



```
SELECT comment 
FROM system.databases 
WHERE name = 'database_with_comment';

```


```
┌─comment─────────────────┐
│ new comment on database │
└─────────────────────────┘

```

To remove the database comment:



```
ALTER DATABASE database_with_comment 
MODIFY COMMENT '';

```

To verify that the comment was removed:



```
SELECT comment 
FROM system.databases 
WHERE  name = 'database_with_comment';

```


```
┌─comment─┐
│         │
└─────────┘

```

## Related content[​](#related-content "Direct link to Related content")


- [`COMMENT`](/docs/sql-reference/statements/create/table#comment-clause) clause
- [`ALTER TABLE ... MODIFY COMMENT`](/docs/sql-reference/statements/alter/comment)
[PreviousALTER TABLE ... MODIFY COMMENT](/docs/sql-reference/statements/alter/comment)[NextNAMED COLLECTION](/docs/sql-reference/statements/alter/named-collection)- [Syntax](#syntax)- [Examples](#examples)- [Related content](#related-content)
Was this page helpful?
