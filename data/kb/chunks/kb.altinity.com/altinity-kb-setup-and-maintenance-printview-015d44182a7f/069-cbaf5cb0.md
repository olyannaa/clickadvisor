---
source: kb.altinity.com
url: http://s3.us-east-1.amazonaws.com/BUCKET_NAME/test_s3_disk/</endpoint>
topic: setup-maintenance-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '98.091'
last_updated: '2026-06-12'
chunk_index: 69
total_chunks_in_doc: 186
---

Zookeeper side [to values about 8M](https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/jvm-sizes-and-garbage-collector-settings/) 3. use IN PARTITION clause for mutations (where applicable) \- since [20\.12](https://github.com/ClickHouse/ClickHouse/pull/13403) 4. switch to clickhouse\-keeper > **Q. “Zookeeper session has expired and also Operation timeout” happens when reading blocks from Zookeeper**:

```
2024.02.22 07:20:39.222171 [ 1047 ] {} <Error> ZooKeeperClient: Code: 999. Coordination::Exception: Operation timeout (no response) for request List for path: 
/clickhouse/tables/github_events/block_numbers/20240205105000 (Operation timeout). (KEEPER_EXCEPTION), 
2024.02.22 07:20:39.223293 [ 246 ] {} <Error> default.github_events : void DB::StorageReplicatedMergeTree::mergeSelectingTask(): 
Code: 999. Coordination::Exception: /clickhouse/tables/github_events/block_numbers/20240205105000 (Connection loss). 

```
Sometimes these `Session expired` and `operation timeout` are common, because of merges that read all the blocks in Zookeeper for a table and if there are many blocks (and partitions) read time can be longer than the 10 secs default [operation timeout](https://clickhouse.com/docs/en/operations/server-configuration-parameters/settings#server-settings_zookeeper)
.
When dropping a partition, ClickHouse never drops old block numbers from Zookeeper, so the list grows indefinitely. It is done as a precaution against race between DROP PARTITION and INSERT. It is safe to clean those old blocks manually

This is being addressed in **[\#59507 Add \<code\>FORGET PARTITION\</code\> query to remove old partition nodes from](https://github.com/ClickHouse/ClickHouse/pull/59507)**

Solutions:
Manually remove old/forgotten blocks [https://kb.altinity.com/altinity\-kb\-useful\-queries/remove\_unneeded\_block\_numbers/](https://kb.altinity.com/altinity-kb-useful-queries/remove_unneeded_block_numbers/)

Related issues:

- <https://github.com/ClickHouse/ClickHouse/issues/16307>
- <https://github.com/ClickHouse/ClickHouse/issues/11933>
- <https://github.com/ClickHouse/ClickHouse/issues/32646>
- <https://github.com/ClickHouse/ClickHouse/issues/15882>
# 34 \- Server configuration files

How to organize configuration files in ClickHouse® and how to manage changes## Сonfig management (recommended structure)

ClickHouse® server config consists of two parts server settings (config.xml) and users settings (users.xml).

By default they are stored in the folder **/etc/clickhouse\-server/** in two files config.xml \& users.xml.

We suggest never change vendor config files and place your changes into separate .xml files in sub\-folders. This way is easier to maintain and ease ClickHouse upgrades.

**/etc/clickhouse\-server/users.d** – sub\-folder for [user settings](/altinity-kb-setup-and-maintenance/rbac/)
(derived from `users.xml` filename).

**/etc/clickhouse\-server/config.d** – sub\-folder for server settings (derived from `config.xml` filename).

**/etc/clickhouse\-server/conf.d** – sub\-folder for any (both) settings.

If the root config (xml or yaml) has a different name, such as `keeper_config.xml` or `config_instance_66.xml`, then the `keeper_config.d` and `config_instance_66.d` folders will be used. But `conf.d` is always used and processed last.

File names of your xml files can be arbitrary but they are applied in alphabetical order.

Examples:
