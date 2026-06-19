---
source: kb.altinity.com
url: https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_freeze-partition
topic: production-cluster-configuration-guide-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 4
total_chunks_in_doc: 8
---

ClickHouse building blocks For general explanations of roles of different engines \- check the post [Distributed vs Shard vs Replicated ahhh, help me!!!](https://github.com/yandex/ClickHouse/issues/2161) . #### Zookeeper Paths Use conventions for zookeeper paths. For example, use: ReplicatedMergeTree(’/clickhouse/{cluster}/tables/{shard}/table\_name’, ‘{replica}’) for:

SELECT \* FROM system.zookeeper WHERE path\=’/ …';

#### Configuration Best Practices

| AttributionModified by a post \[on GitHub by Mikhail Filimonov](https://github.com/ClickHouse/ClickHouse/issues/3607\#issuecomment\-440235298\). |
| --- |

The following are recommended Best Practices when it comes to setting up a ClickHouse Cluster with Zookeeper:

1. Don’t edit/overwrite default configuration files. Sometimes a newer version of ClickHouse introduces some new settings or changes the defaults in config.xml and users.xml.
	1. Set configurations via the extra files in conf.d directory. For example, to overwrite the interface save the file config.d/listen.xml, with the following:

```
<?xml version="1.0"?>
<yandex>
    <listen_host replace="replace">::</listen_host>
</yandex>

```
1. The same is true for users. For example, change the default profile by putting the file in users.d/profile\_default.xml:

```
<?xml version="1.0"?>
<yandex>
    <profiles>
        <default replace="replace">
            <max_memory_usage>15000000000</max_memory_usage>
            <max_bytes_before_external_group_by>12000000000</max_bytes_before_external_group_by>
            <max_bytes_before_external_sort>12000000000</max_bytes_before_external_sort>
            <distributed_aggregation_memory_efficient>1</distributed_aggregation_memory_efficient>
            <use_uncompressed_cache>0</use_uncompressed_cache>
            <load_balancing>random</load_balancing>
            <log_queries>1</log_queries>
            <max_execution_time>600</max_execution_time>
        </default>
    </profiles>
</yandex>

```
1. Or you can create a user by putting a file users.d/user\_xxx.xml (since 20\.5 you can also use CREATE USER)

```
<?xml version="1.0"?>
<yandex>
    <users>
        <xxx>
            <!-- PASSWORD=$(base64 < /dev/urandom | head -c8); echo "$PASSWORD"; echo -n "$PASSWORD" | sha256sum | tr -d '-' -->
            <password_sha256_hex>...</password_sha256_hex>
            <networks incl="networks" />
            <profile>readonly</profile>
            <quota>default</quota>
            <allow_databases incl="allowed_databases" />
        </xxx>
    </users>
</yandex>

```
1. Some parts of configuration will contain repeated elements (like allowed ips for all the users). To avoid repeating that \- use substitutions file. By default its /etc/metrika.xml, but you can change it for example to /etc/clickhouse\-server/substitutions.xml with the \<include\_from\> section of the main config. Put the repeated parts into substitutions file, like this:

```
<?xml version="1.0"?>
<yandex>
    <networks>
        <ip>::1</ip>
        <ip>127.0.0.1</ip>
        <ip>10.42.0.0/16</ip>
        <ip>192.168.0.0/24</ip>
    </networks>
</yandex>

```
These files can be common for all the servers inside the cluster or can be individualized per server. If you choose to use one substitutions file per cluster, not per node, you will also need to generate the file with macros, if macros are used.
