# EXCHANGE Statement \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- EXCHANGE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/exchange.md)# EXCHANGE Statement

Exchanges the names of two tables or dictionaries atomically.
This task can also be accomplished with a [`RENAME`](/docs/sql-reference/statements/rename) query using a temporary name, but the operation is not atomic in that case.


NoteThe `EXCHANGE` query is supported by the [`Atomic`](/docs/engines/database-engines/atomic) and [`Shared`](/docs/cloud/reference/shared-catalog#shared-database-engine) database engines only.


**Syntax**



```
EXCHANGE TABLES|DICTIONARIES [db0.]name_A AND [db1.]name_B [ON CLUSTER cluster]

```

## EXCHANGE TABLES[​](#exchange-tables "Direct link to EXCHANGE TABLES")


Exchanges the names of two tables.


**Syntax**



```
EXCHANGE TABLES [db0.]table_A AND [db1.]table_B [ON CLUSTER cluster]

```

### EXCHANGE MULTIPLE TABLES[​](#exchange-multiple-tables "Direct link to EXCHANGE MULTIPLE TABLES")


You can exchange multiple table pairs in a single query by separating them with commas.


NoteWhen exchanging multiple table pairs, the exchanges are performed **sequentially, not atomically**. If an error occurs during the operation, some table pairs may have been exchanged while others have not.


**Example**



```
-- Create tables
CREATE TABLE a (a UInt8) ENGINE=Memory;
CREATE TABLE b (b UInt8) ENGINE=Memory;
CREATE TABLE c (c UInt8) ENGINE=Memory;
CREATE TABLE d (d UInt8) ENGINE=Memory;

-- Exchange two pairs of tables in one query
EXCHANGE TABLES a AND b, c AND d;

SHOW TABLE a;
SHOW TABLE b;
SHOW TABLE c;
SHOW TABLE d;

```


```
-- Now table 'a' has the structure of 'b', and table 'b' has the structure of 'a'
┌─statement──────────────┐
│ CREATE TABLE default.a↴│
│↳(                     ↴│
│↳    `b` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘
┌─statement──────────────┐
│ CREATE TABLE default.b↴│
│↳(                     ↴│
│↳    `a` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘

-- Now table 'c' has the structure of 'd', and table 'd' has the structure of 'c'
┌─statement──────────────┐
│ CREATE TABLE default.c↴│
│↳(                     ↴│
│↳    `d` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘
┌─statement──────────────┐
│ CREATE TABLE default.d↴│
│↳(                     ↴│
│↳    `c` UInt8         ↴│
│↳)                     ↴│
│↳ENGINE = Memory        │
└────────────────────────┘

```

## EXCHANGE DICTIONARIES[​](#exchange-dictionaries "Direct link to EXCHANGE DICTIONARIES")


Exchanges the names of two dictionaries.


**Syntax**



```
EXCHANGE DICTIONARIES [db0.]dict_A AND [db1.]dict_B [ON CLUSTER cluster]

```

**See Also**


- [Dictionaries](/docs/sql-reference/statements/create/dictionary)
[PreviousRENAME](/docs/sql-reference/statements/rename)[NextSET](/docs/sql-reference/statements/set)- [EXCHANGE TABLES](#exchange-tables)
	- [EXCHANGE MULTIPLE TABLES](#exchange-multiple-tables)- [EXCHANGE DICTIONARIES](#exchange-dictionaries)
Was this page helpful?
