# ClickHouse® Atomic Database Engine \| Altinity® Knowledge Base for ClickHouse®


1. [Engines](/engines/)
2. Atomic Database Engine
# ClickHouse® Atomic Database Engine

Capabilities of the Atomic database engineIn version 20\.5, ClickHouse® first introduced `database engine=Atomic`.

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



---

##### [How to Convert Ordinary to Atomic](/engines/altinity-kb-atomic-database-engine/how-to-convert-ordinary-to-atomic/)

##### [How to Convert Atomic to Ordinary](/engines/altinity-kb-atomic-database-engine/altinity-kb-how-to-convert-atomic-to-ordinary/)

Last modified 2025\.06\.26: [Update information about clickhouse\-backup Atomic support (1863dd9\)](https://github.com/Altinity/altinityknowledgebase/commit/1863dd9a5bb04c2eb26d7ed83024a2227486b00b)
