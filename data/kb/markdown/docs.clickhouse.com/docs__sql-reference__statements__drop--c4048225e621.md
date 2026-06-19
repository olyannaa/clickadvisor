# DROP Statements \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- DROP
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/drop.md)# DROP Statements

Deletes existing entity. If the `IF EXISTS` clause is specified, these queries do not return an error if the entity does not exist. If the `SYNC` modifier is specified, the entity is dropped without delay.


## DROP DATABASE[​](#drop-database "Direct link to DROP DATABASE")


Deletes all tables inside the `db` database, then deletes the `db` database itself.


Syntax:



```
DROP DATABASE [IF EXISTS] db [ON CLUSTER cluster] [SYNC]

```

## DROP TABLE[​](#drop-table "Direct link to DROP TABLE")


Deletes one or more tables.


TipTo undo the deletion of a table, please see [UNDROP TABLE](/docs/sql-reference/statements/undrop)


Syntax:



```
DROP [TEMPORARY] TABLE [IF EXISTS] [IF EMPTY]  [db1.]name_1[, [db2.]name_2, ...] [ON CLUSTER cluster] [SYNC]

```

Limitations:


- If the clause `IF EMPTY` is specified, the server checks the emptiness of the table only on the replica which received the query.
- Deleting multiple tables at once is not an atomic operation, i.e. if the deletion of a table fails, subsequent tables will not be deleted.


## DROP DICTIONARY[​](#drop-dictionary "Direct link to DROP DICTIONARY")


Deletes the dictionary.


Syntax:



```
DROP DICTIONARY [IF EXISTS] [db.]name [SYNC]

```

## DROP USER[​](#drop-user "Direct link to DROP USER")


Deletes a user.


Syntax:



```
DROP USER [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```

## DROP ROLE[​](#drop-role "Direct link to DROP ROLE")


Deletes a role. The deleted role is revoked from all the entities where it was assigned.


Syntax:



```
DROP ROLE [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```

## DROP ROW POLICY[​](#drop-row-policy "Direct link to DROP ROW POLICY")


Deletes a row policy. Deleted row policy is revoked from all the entities where it was assigned.


Syntax:



```
DROP [ROW] POLICY [IF EXISTS] name [,...] ON [database.]table [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```

## DROP MASKING POLICY[​](#drop-masking-policy "Direct link to DROP MASKING POLICY")


Deletes a masking policy.


Syntax:



```
DROP MASKING POLICY [IF EXISTS] name ON [database.]table [ON CLUSTER cluster_name] [FROM access_storage_type]

```

## DROP QUOTA[​](#drop-quota "Direct link to DROP QUOTA")


Deletes a quota. The deleted quota is revoked from all the entities where it was assigned.


Syntax:



```
DROP QUOTA [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```

## DROP SETTINGS PROFILE[​](#drop-settings-profile "Direct link to DROP SETTINGS PROFILE")


Deletes a settings profile. The deleted settings profile is revoked from all the entities where it was assigned.


Syntax:



```
DROP [SETTINGS] PROFILE [IF EXISTS] name [,...] [ON CLUSTER cluster_name] [FROM access_storage_type]

```

## DROP VIEW[​](#drop-view "Direct link to DROP VIEW")


Deletes a view. Views can be deleted by a `DROP TABLE` command as well but `DROP VIEW` checks that `[db.]name` is a view.


Syntax:



```
DROP VIEW [IF EXISTS] [db.]name [ON CLUSTER cluster] [SYNC]

```

## DROP FUNCTION[​](#drop-function "Direct link to DROP FUNCTION")


Deletes a user defined function created by [CREATE FUNCTION](/docs/sql-reference/statements/create/function).
System functions can not be dropped.


**Syntax**



```
DROP FUNCTION [IF EXISTS] function_name [on CLUSTER cluster]

```

**Example**



```
CREATE FUNCTION linear_equation AS (x, k, b) -> k*x + b;
DROP FUNCTION linear_equation;

```

## DROP NAMED COLLECTION[​](#drop-named-collection "Direct link to DROP NAMED COLLECTION")


Deletes a named collection.


**Syntax**



```
DROP NAMED COLLECTION [IF EXISTS] name [on CLUSTER cluster]

```

**Example**



```
CREATE NAMED COLLECTION foobar AS a = '1', b = '2';
DROP NAMED COLLECTION foobar;

```
[PreviousDETACH](/docs/sql-reference/statements/detach)[NextEXISTS](/docs/sql-reference/statements/exists)- [DROP DATABASE](#drop-database)- [DROP TABLE](#drop-table)- [DROP DICTIONARY](#drop-dictionary)- [DROP USER](#drop-user)- [DROP ROLE](#drop-role)- [DROP ROW POLICY](#drop-row-policy)- [DROP MASKING POLICY](#drop-masking-policy)- [DROP QUOTA](#drop-quota)- [DROP SETTINGS PROFILE](#drop-settings-profile)- [DROP VIEW](#drop-view)- [DROP FUNCTION](#drop-function)- [DROP NAMED COLLECTION](#drop-named-collection)
Was this page helpful?
