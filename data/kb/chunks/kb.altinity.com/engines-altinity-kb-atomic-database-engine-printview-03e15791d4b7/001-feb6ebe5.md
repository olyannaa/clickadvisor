---
source: kb.altinity.com
url: https://github.com/ClickHouse/ClickHouse/issues/12135\#issuecomment\-653932557](https://github.com/ClickHouse/ClickHouse/issues/12135#issuecomment-653932557
topic: clickhouse-atomic-database-engine-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 5
---

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
