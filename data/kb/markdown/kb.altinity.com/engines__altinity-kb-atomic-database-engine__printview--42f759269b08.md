# ClickHouse® Atomic Database Engine \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/engines/altinity-kb-atomic-database-engine/).

# ClickHouse® Atomic Database Engine

Capabilities of the Atomic database engine- 1: [How to Convert Ordinary to Atomic](#pg-7e67c7ea6f6b30f9350b23cdf9c765e8)
- 2: [How to Convert Atomic to Ordinary](#pg-094af220e72e8217a5c6408e9fb28441)

In version 20\.5, ClickHouse® first introduced `database engine=Atomic`.

Since version 20\.10 it is a default database engine (before engine\=Ordinary was used).

Those 2 database engine differs in a way how they store data on a filesystem, and engine Atomic allows to resolve some of the issues existed in engine\=Ordinary.

`engine=Atomic` supports

- non\-blocking drop table / rename table
- tables delete (\&detach) async (wait for selects finish but invisible for new selects)
- atomic drop table (all files / folders removed)
- atomic table swap (table swap by “EXCHANGE TABLES t1 AND t2;”)
- rename dictionary / rename database
- unique automatic UUID paths in FS and ZK for Replicated

## FAQ

### **Q. Data is not removed immediately**

A. Use`DROP TABLE t SYNC;`

Or use parameter (user level) database\_atomic\_wait\_for\_drop\_and\_detach\_synchronously`:`


```
SET database_atomic_wait_for_drop_and_detach_synchronously = 1;

```
Also, you can decrease the delay used by Atomic for real table drop (it’s 8 minutes by default)


```
cat /etc/clickhouse-server/config.d/database_atomic_delay_before_drop_table.xml
<clickhouse>
    <database_atomic_delay_before_drop_table_sec>1</database_atomic_delay_before_drop_table_sec>
</clickhouse>

```
### **Q. I cannot reuse zookeeper path after dropping the table.**

A. This happens because real table deletion occurs with a controlled delay. See the previous question to remove the table immediately.

With engine\=Atomic it’s possible (and is a good practice if you do it correctly) to include UUID into zookeeper path, i.e. :


```
CREATE ...
ON CLUSTER ...
ENGINE=ReplicatedMergeTree('/clickhouse/tables/{uuid}/{shard}/', '{replica}')

```
See also: [https://github.com/ClickHouse/ClickHouse/issues/12135\#issuecomment\-653932557](https://github.com/ClickHouse/ClickHouse/issues/12135#issuecomment-653932557)

It’s very important that the table will have the same UUID cluster\-wide.

When the table is created using *ON CLUSTER* \- all tables will get the same UUID automatically.
When it needs to be done manually (for example \- you need to add one more replica), pick CREATE TABLE statement with UUID from one of the existing replicas.


```
set show_table_uuid_in_table_create_qquery_if_not_nil=1　;
SHOW CREATE TABLE xxx; /* or SELECT create_table_query FROM system.tables WHERE ... */

```
### Q. Should I use Atomic or Ordinary for new setups?

All things inside ClickHouse itself should work smoothly with `Atomic`.

But some external tools \- backup tools, things involving other kinds of direct manipulations with ClickHouse files \& folders may have issues with `Atomic`.

`Ordinary` layout on the filesystem is simpler. And the issues which address Atomic (lock\-free renames, drops, atomic exchange of table) are not so critical in most cases.



|  | Ordinary | Atomic |
| --- | --- | --- |
| filesystem layout | very simple | more complicated |
| external tool support(like `clickhouse-backup`) | good / mature | good / mature |
| some DDL queries (DROP / RENAME) mayhang for a long time (waiting for some other things) | yes 👎 | no 👍 |
| Possibility to swap 2 tables | renamea to a\_old,b to a,a\_old to b;Operation is not atomic, andcan break in the middle (while chances are low). | EXCHANGE TABLES t1 AND t2Atomic, have no intermediate states. |
| uuid in zookeeper path | Not possible to use.The typical pattern is to add version suffix to zookeeper path when you need to createthe new version of the same table. | You can use uuid in zookeeper paths.That requires some extra care when you expand the cluster, and makes zookeeper paths harder to map to real table.But allows to to do any kind of manipulations on tables (rename, recreate with same name etc). |
| Materialized view without TO syntax(!we recommend using TO syntax always!) | .inner.mv\_nameThe name is predictable, easy to match with MV. | .inner\_id.{uuid}The name is unpredictable, hard to match with MV (maybe problematic for MV chains, and similar scenarios) |

## Using Ordinary by default instead of Atomic


```
---
title: "cat /etc/clickhouse-server/users.d/disable_atomic_database.xml "
linkTitle: "cat /etc/clickhouse-server/users.d/disable_atomic_database.xml "
description: >
    cat /etc/clickhouse-server/users.d/disable_atomic_database.xml
---
<?xml version="1.0"?>
<clickhouse>
    <profiles>
        <default>
            <default_database_engine>Ordinary</default_database_engine>
        </default>
    </profiles>
</clickhouse>

```
## Other sources

Presentation [https://youtu.be/1LVJ\_WcLgF8?t\=2744](https://youtu.be/1LVJ_WcLgF8?t=2744)

[https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup46/database\_engines.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup46/database_engines.pdf)

# 1 \- How to Convert Ordinary to Atomic

## New, official way

- Implemented automatic conversion of database engine from `Ordinary` to `Atomic` (ClickHouse® Server 22\.8\+). Create empty `convert_ordinary_to_atomic` file in `flags` directory and all `Ordinary` databases will be converted automatically on next server start.
- The conversion is not automatic between upgrades, you need to set the flag as explained below:


```
Warnings:
 * Server has databases (for example `test`) with Ordinary engine, which was deprecated. To convert this database to the new Atomic engine, create a flag /var/lib/clickhouse/flags/convert_ordinary_to_atomic and make sure that ClickHouse has write permission for it.
Example: sudo touch '/var/lib/clickhouse/flags/convert_ordinary_to_atomic' && sudo chmod 666 '/var/lib/clickhouse/flags/convert_ordinary_to_atomic'

```
- Resolves [\#39546](https://github.com/ClickHouse/ClickHouse/issues/39546)
. [\#39933](https://github.com/ClickHouse/ClickHouse/pull/39933)
([Alexander Tokmakov](https://github.com/tavplubix)
)
- There can be some problems if the `default` database is Ordinary and fails for some reason. You can add:


```
<clickhouse>
     <allow_reserved_database_name_tmp_convert>1</allow_reserved_database_name_tmp_convert>
</clickhouse>

```
[More detailed info here](https://github.com/ClickHouse/ClickHouse/blob/f01a285f6091265cfae72bb7fbf3186269804891/src/Interpreters/loadMetadata.cpp#L150)

Don’t forget to remove detached parts from all Ordinary databases, or you can get the error:


```
│ 2025.01.28 11:34:57.510330 [ 7 ] {} <Error> Application: Code: 219. DB::Exception: Cannot drop: filesystem error: in remove: Directory not empty ["/var/lib/clickhouse/data/db/"]. Probably data │
│ base contain some detached tables or metadata leftovers from Ordinary engine. If you want to remove all data anyway, try to attach database back and drop it again with enabled force_remove_data_recursively_ │

```
# 2 \- How to Convert Atomic to Ordinary

How to Convert Atomic to OrdinaryThe following instructions are an example on how to convert a database with the Engine type **Atomic** to a database with the Engine type **Ordinary**.

#### Warning

That can be used only for simple schemas. Schemas with MATERIALIZED views will require extra manipulations.
```
CREATE DATABASE atomic_db ENGINE = Atomic;
CREATE DATABASE ordinary_db ENGINE = Ordinary;
CREATE TABLE atomic_db.x ENGINE = MergeTree ORDER BY tuple() AS system.numbers;
INSERT INTO atomic_db.x SELECT number FROM numbers(100000);
RENAME TABLE atomic_db.x TO ordinary_db.x;

```

```
ls -1 /var/lib/clickhouse/data/ordinary_db/x
all_1_1_0
detached
format_version.txt

```

```
DROP DATABASE atomic_db;
DETACH DATABASE ordinary_db;

```

```
mv /var/lib/clickhouse/metadata/ordinary_db.sql /var/lib/clickhouse/metadata/atomic_db.sql
vi /var/lib/clickhouse/metadata/atomic_db.sql
mv /var/lib/clickhouse/metadata/ordinary_db /var/lib/clickhouse/metadata/atomic_db
mv /var/lib/clickhouse/data/ordinary_db /var/lib/clickhouse/data/atomic_db

```

```
ATTACH DATABASE atomic_db;
SELECT count() FROM atomic_db.x
┌─count()─┐
│  100000 │
└─────────┘
SHOW CREATE DATABASE atomic_db
┌─statement──────────────────────────────────┐
│ CREATE DATABASE atomic_db
ENGINE = Ordinary │
└────────────────────────────────────────────┘

```
## Schemas with Materialized VIEW


```
DROP DATABASE IF EXISTS atomic_db;
DROP DATABASE IF EXISTS ordinary_db;

CREATE DATABASE atomic_db engine=Atomic;
CREATE DATABASE ordinary_db engine=Ordinary;

CREATE TABLE atomic_db.x ENGINE = MergeTree ORDER BY tuple() AS system.numbers;
CREATE MATERIALIZED VIEW atomic_db.x_mv ENGINE = MergeTree ORDER BY tuple() AS SELECT * FROM atomic_db.x;
CREATE MATERIALIZED VIEW atomic_db.y_mv ENGINE = MergeTree ORDER BY tuple() AS SELECT * FROM atomic_db.x;
CREATE TABLE atomic_db.z ENGINE = MergeTree ORDER BY tuple() AS system.numbers;
CREATE MATERIALIZED VIEW atomic_db.z_mv TO atomic_db.z AS SELECT * FROM atomic_db.x;

INSERT INTO atomic_db.x SELECT * FROM numbers(100);

--- USE atomic_db;
---
--- Query id: 28af886d-a339-4e9c-979c-8bdcfb32fd95
---
--- ┌─name───────────────────────────────────────────┐
--- │ .inner_id.b7906fec-f4b2-455b-bf9b-2b18ca64842c │
--- │ .inner_id.bd32d79b-272d-4710-b5ad-bca78d09782f │
--- │ x                                              │
--- │ x_mv                                           │
--- │ y_mv                                           │
--- │ z                                              │
--- │ z_mv                                           │
--- └────────────────────────────────────────────────┘


SELECT mv_storage.database, mv_storage.name, mv.database, mv.name
FROM system.tables AS mv_storage
LEFT JOIN system.tables AS mv ON substring(mv_storage.name, 11) = toString(mv.uuid)
WHERE mv_storage.name LIKE '.inner_id.%' AND mv_storage.database = 'atomic_db';

-- ┌─database──┬─name───────────────────────────────────────────┬─mv.database─┬─mv.name─┐
-- │ atomic_db │ .inner_id.81e1a67d-3d02-4b2a-be17-84d8626d2328 │ atomic_db   │ y_mv    │
-- │ atomic_db │ .inner_id.e428225c-982a-4859-919b-ba5026db101d │ atomic_db   │ x_mv    │
-- └───────────┴────────────────────────────────────────────────┴─────────────┴─────────┘




/* STEP 1: prepare rename statements, also to rename implicit mv storage table to explicit one */

SELECT
if(
   t.name LIKE '.inner_id.%',
  'RENAME TABLE `' || t.database || '`.`' ||  t.name || '` TO `ordinary_db`.`' || mv.name || '_storage`;',
   'RENAME TABLE `' || t.database || '`.`' ||  t.name || '` TO `ordinary_db`.`' || t.name || '`;'
)
FROM system.tables as t
LEFT JOIN system.tables mv ON (substring(t.name,11) = toString(mv.uuid) AND t.database =  mv.database )
WHERE t.database = 'atomic_db' AND t.engine <> 'MaterializedView'
FORMAT TSVRaw;

-- RENAME TABLE `atomic_db`.`.inner_id.b7906fec-f4b2-455b-bf9b-2b18ca64842c` TO `ordinary_db`.`y_mv_storage`;
-- RENAME TABLE `atomic_db`.`.inner_id.bd32d79b-272d-4710-b5ad-bca78d09782f` TO `ordinary_db`.`x_mv_storage`;
-- RENAME TABLE `atomic_db`.`x` TO `ordinary_db`.`x`;
-- RENAME TABLE `atomic_db`.`z` TO `ordinary_db`.`z`;


/* STEP 2: prepare statements to reattach MV */
-- Can be done manually: pick existing MV definition (SHOW CREATE TABLE), and change it in the following way:
-- 1) add TO keyword 2) remove column names and engine settings after mv name


SELECT
if(
   t.name LIKE '.inner_id.%',
   replaceRegexpOne(mv.create_table_query, '^CREATE MATERIALIZED VIEW ([^ ]+) (.*? AS ', 'CREATE MATERIALIZED VIEW \\1 TO \\1_storage AS '),
   mv.create_table_query
)
FROM system.tables as mv
LEFT JOIN system.tables t ON (substring(t.name,11) = toString(mv.uuid) AND t.database =  mv.database)
WHERE mv.database = 'atomic_db' AND mv.engine='MaterializedView'
FORMAT TSVRaw;

-- CREATE MATERIALIZED VIEW atomic_db.x_mv TO atomic_db.x_mv_storage AS SELECT * FROM atomic_db.x
-- CREATE MATERIALIZED VIEW atomic_db.y_mv TO atomic_db.y_mv_storage AS SELECT * FROM atomic_db.x

/* STEP 3: stop inserts, fire renames statements prepared at the step 1 (hint: use clickhouse-client -mn) */

RENAME ...

/* STEP 4: ensure that only MaterializedView left in source db, and drop it.  */

SELECT * FROM system.tables WHERE database = 'atomic_db' and engine <> 'MaterializedView';
DROP DATABASE atomic_db;


/* STEP 4. rename table to old name: */

DETACH DATABASE ordinary_db;

-- rename files / folders:

mv /var/lib/clickhouse/metadata/ordinary_db.sql /var/lib/clickhouse/metadata/atomic_db.sql
vi /var/lib/clickhouse/metadata/atomic_db.sql
mv /var/lib/clickhouse/metadata/ordinary_db /var/lib/clickhouse/metadata/atomic_db
mv /var/lib/clickhouse/data/ordinary_db /var/lib/clickhouse/data/atomic_db

-- attach database atomic_db;

ATTACH DATABASE atomic_db;

/* STEP 5. restore MV using statements created on STEP 2 */

```
