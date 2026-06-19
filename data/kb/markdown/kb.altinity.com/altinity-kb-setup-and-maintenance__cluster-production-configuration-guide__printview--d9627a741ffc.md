# Production Cluster Configuration Guide \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-setup-and-maintenance/cluster-production-configuration-guide/).

# Production Cluster Configuration Guide

Production Cluster Configuration Guide- 1: [Backups](#pg-202b7e3651622a4779b38f52cef739a7)
- 2: [Cluster Configuration FAQ](#pg-8064c7d414e643fb87b3e0939260d98f)
- 3: [Cluster Configuration Process](#pg-839cbf636b5f8a35c6823f41977447f7)
- 4: [Hardware Requirements](#pg-3754a72a1a168184ed696d361b761145)
- 5: [Network Configuration](#pg-414e2937f5573cccbd17d35a64e42c62)

Moving from a single ClickHouse® server to a clustered format provides several benefits:

- Replication guarantees data integrity.
- Provides redundancy.
- Failover by being able to restart half of the nodes without encountering downtime.

Moving from an unsharded ClickHouse environment to a sharded cluster requires redesign of schema and queries. Starting with a sharded cluster from the beginning makes it easier in the future to scale the cluster up.

Setting up a ClickHouse cluster for a production environment requires the following stages:

- Hardware Requirements
- Network Configuration
- Create Host Names
- Monitoring Considerations
- Configuration Steps
- Setting Up Backups
- Staging Plans
- Upgrading The Cluster
# 1 \- Backups

BackupsClickHouse® is currently at the design stage of creating some universal backup solution. Some custom backup strategies are:

1. Each shard is backed up separately.
2. FREEZE the table/partition. For more information, see [Alter Freeze Partition](https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_freeze-partition)
.
	1. This creates hard links in shadow subdirectory.
3. rsync that directory to a backup location, then remove that subfolder from shadow.
	1. Cloud users are recommended to use [Rclone](https://rclone.org/)
	.
4. Always add the full contents of the metadata subfolder that contains the current DB schema and ClickHouse configs to your backup.
5. For a second replica, it’s enough to copy metadata and configuration.
6. Data in ClickHouse is already compressed with lz4, backup can be compressed bit better, but avoid using cpu\-heavy compression algorithms like gzip, use something like zstd instead.

The tool automating that process: [Altinity Backup for ClickHouse](https://github.com/Altinity/clickhouse-backup)
.

# 2 \- Cluster Configuration FAQ

Cluster Configuration FAQ## ClickHouse® does not start, some other unexpected behavior happening

Check ClickHouse logs, they are your friends:

tail \-n 1000 /var/log/clickhouse\-server/clickhouse\-server.err.log \| less
tail \-n 10000 /var/log/clickhouse\-server/clickhouse\-server.log \| less

## How Do I Restrict Memory Usage?

See [our knowledge base article](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-memory-configuration-settings/)
and [official documentation](https://clickhouse.tech/docs/en/operations/settings/query-complexity/#settings_max_memory_usage)
for more information.

## ClickHouse died during big query execution

Misconfigured ClickHouse can try to allocate more RAM than is available on the system.

In that case an OS component called oomkiller can kill the ClickHouse process.

That event leaves traces inside system logs (can be checked by running dmesg command).

## How Do I make huge ‘Group By’ queries use less RAM?

Enable on disk GROUP BY (it is slower, so is disabled by default)

Set [max\_bytes\_before\_external\_group\_by](https://clickhouse.tech/docs/en/operations/settings/query-complexity/#settings-max_bytes_before_external_group_by)
to a value about 70\-80% of your max\_memory\_usage value.

## Data returned in chunks by clickhouse\-client

See [altinity\-kb\-clickhouse\-client](http://kb.altinity.com/altinity-kb-interfaces/altinity-kb-clickhouse-client/)

## I Can’t Connect From Other Hosts. What do I do?

Check the settings in config.xml. Verify that the connection can connect on both IPV4 and IPV6\.

# 3 \- Cluster Configuration Process

Cluster Configuration ProcessSo you set up 3 nodes with zookeeper (zookeeper1, zookeeper2, zookeeper3 \- [How to install zookeeper?](https://docs.altinity.com/operationsguide/clickhouse-zookeeper/)
), and and 4 nodes with ClickHouse® (clickhouse\-sh1r1,clickhouse\-sh1r2,clickhouse\-sh2r1,clickhouse\-sh2r2 \- [how to install ClickHouse?](https://docs.altinity.com/altinitystablerelease/stablequickstartguide/)
). Now we need to make them work together.

Use ansible/puppet/salt or other systems to control the servers’ configurations.

1. Configure ClickHouse access to Zookeeper by adding the file zookeeper.xml in /etc/clickhouse\-server/config.d/ folder. This file must be placed on all ClickHouse servers.


```
<yandex>
    <zookeeper>
        <node>
            <host>zookeeper1</host>
            <port>2181</port>
        </node>
        <node>
            <host>zookeeper2</host>
            <port>2181</port>
        </node>
        <node>
            <host>zookeeper3</host>
            <port>2181</port>
        </node>
    </zookeeper>
</yandex>

```
1. On each server put the file macros.xml in `/etc/clickhouse-server/config.d/` folder.


```
<yandex>
    <!--
        That macros are defined per server,
        and they can be used in DDL, to make the DB schema cluster/server neutral
    -->
    <macros>
        <cluster>prod_cluster</cluster>
        <shard>01</shard>
        <replica>clickhouse-sh1r1</replica> <!-- better - use the same as hostname  -->
    </macros>
</yandex>

```
1. On each server place the file cluster.xml in /etc/clickhouse\-server/config.d/ folder. Before 20\.10 ClickHouse will use default user to connect to other nodes (configurable, other users can be used), since 20\.10 we recommend to use passwordless intercluster authentication based on common secret (HMAC auth)


```
<yandex>
    <remote_servers>
        <prod_cluster> <!-- you need to give a some name for a cluster -->

            <!--
                <secret>some_random_string, same on all cluster nodes, keep it safe</secret>
            -->
            <shard>
                <internal_replication>true</internal_replication>
                <replica>
                    <host>clickhouse-sh1r1</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-sh1r2</host>
                    <port>9000</port>
                </replica>
            </shard>
            <shard>
                <internal_replication>true</internal_replication>
                <replica>
                    <host>clickhouse-sh2r1</host>
                    <port>9000</port>
                </replica>
                <replica>
                    <host>clickhouse-sh2r2</host>
                    <port>9000</port>
                </replica>
            </shard>
        </prod_cluster>
    </remote_servers>
</yandex>

```
1. A good practice is to create 2 additional cluster configurations similar to prod\_cluster above with the following distinction: but listing all nodes of single shard (all are replicas) and as nodes of 6 different shards (no replicas)
	1. all\-replicated: All nodes are listed as replicas in a single shard.
	2. all\-sharded: All nodes are listed as separate shards with no replicas.

Once this is complete, other queries that span nodes can be performed. For example:


```
CREATE TABLE test_table_local ON CLUSTER '{cluster}'
(
  id UInt8
)
Engine=ReplicatedMergeTree('/clickhouse/tables/{database}/{table}/{shard}', '{replica}')
ORDER BY (id);

```
That will create a table on all servers in the cluster. You can insert data into this table and it will be replicated automatically to the other shards.To store the data or read the data from all shards at the same time, create a Distributed table that links to the replicatedMergeTree table.


```
CREATE TABLE test_table ON CLUSTER '{cluster}'
Engine=Distributed('{cluster}', 'default', '

```
#### **Hardening ClickHouse Security**

**See** <https://docs.altinity.com/operationsguide/security/>

### Additional Settings

See [altinity\-kb\-settings\-to\-adjust](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-settings-to-adjust/)

#### Users

Disable or add password for the default users default and readonly if your server is accessible from non\-trusted networks.

If you add password to the default user, you will need to adjust cluster configuration, since the other servers need to know the default user’s should know the default user’s to connect to each other.

If you’re inside a trusted network, you can leave default user set to nothing to allow the ClickHouse nodes to communicate with each other.

#### Engines \& ClickHouse building blocks

For general explanations of roles of different engines \- check the post [Distributed vs Shard vs Replicated ahhh, help me!!!](https://github.com/yandex/ClickHouse/issues/2161)
.

#### Zookeeper Paths

Use conventions for zookeeper paths. For example, use:

ReplicatedMergeTree(’/clickhouse/{cluster}/tables/{shard}/table\_name’, ‘{replica}’)

for:

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

This way you have full flexibility; you’re not limited to the settings described in the template. You can change any settings per server or data center just by assigning files with some settings to that server or server group. It becomes easy to navigate, edit, and assign files.

### Other Configuration Recommendations

Other configurations that should be evaluated:

- in config.xml: Determines which IP addresses and ports the ClickHouse servers listen for incoming communications.
- \<max\_memory\_..\> and \<max\_bytes\_before\_external\_…\> in users.xml. These are part of the profile .
- \<max\_execution\_time\>
- \<log\_queries\>

The following extra debug logs should be considered:

- part\_log
- text\_log

### Understanding The Configuration

ClickHouse configuration stores most of its information in two files:

- config.xml: Stores [Server configuration parameters](https://clickhouse.yandex/docs/en/operations/server_settings/)
. They are server wide, some are hierarchical , and most of them can’t be changed in runtime. The list of settings to apply without a restart changes from version to version. Some settings can be verified using system tables, for example:
	- macros (system.macros)
	- remote\_servers (system.clusters)
- users.xml: Configure users, and user level / session level [settings](https://clickhouse.yandex/docs/en/operations/settings/settings/)
.
	- Each user can change these during their session by:
		- Using parameter in http query
		- By using parameter for clickhouse\-client
		- Sending query like set allow\_experimental\_data\_skipping\_indices\=1\.
	- Those settings and their current values are visible in system.settings. You can make some settings global by editing default profile in users.xml, which does not need restart.
	- You can forbid users to change their settings by using readonly\=2 for that user, or using [setting constraints](https://clickhouse.yandex/docs/en/operations/settings/constraints_on_settings/)
	.
	- Changes in users.xml are applied w/o restart.

For both config.xml and users.xml, it’s preferable to put adjustments in the config.d and users.d subfolders instead of editing config.xml and users.xml directly.

You can check if the config file was reread by checking /var/lib/clickhouse/preprocessed\_configs/ folder.

# 4 \- Hardware Requirements

Hardware Requirements### ClickHouse®

ClickHouse will use all available hardware to maximize performance. So the more hardware \- the better. As of this publication, the hardware requirements are:

- Minimum Hardware: 4\-core CPU with support of SSE4\.2, 16 Gb RAM, 1Tb HDD.
	- Recommended for development and staging environments.
	- SSE4\.2 is required, and going below 4 Gb of RAM is not recommended.
- Recommended Hardware: \>\=16\-cores, \>\=64Gb RAM, HDD\-raid or SSD.
	- For processing up to hundreds of millions / billions of rows.

For clouds: disk throughput is the more important factor compared to IOPS. Be aware of burst / baseline disk speed difference.

See also: <https://benchmark.clickhouse.com/hardware/>

### **Zookeeper**

Zookeeper requires separate servers from those used for ClickHouse. Zookeeper has poor performance when installed on the same node as ClickHouse.

Hardware Requirements for Zookeeper:

- Fast disk speed (ideally NVMe, 128Gb should be enough).
- Any modern CPU (one core, better 2\)
- 4Gb of RAM

For clouds \- be careful with burstable network disks (like gp2 on aws): you may need up to 1000 IOPs on the disk for on a long run, so gp3 with 3000 IOPs baseline is a better choice.

The number of Zookeeper instances depends on the environment:

- Production: 3 is an optimal number of zookeeper instances.
- Development and Staging: 1 zookeeper instance is sufficient.

See also:

- [https://docs.altinity.com/operationsguide/clickhouse\-zookeeper/](https://docs.altinity.com/operationsguide/clickhouse-zookeeper/)
- [altinity\-kb\-proper\-setup](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/altinity-kb-proper-setup/)
- [zookeeper\-monitoring](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-zookeeper/zookeeper-monitoring/)

#### ClickHouse Hardware Configuration

Configure the servers according to those recommendations on the [ClickHouse Usage Recommendations](https://clickhouse.com/docs/en/operations/tips/)
.

#### **Test Your Hardware**

Be sure to test the following:

- RAM speed.
- Network speed.
- Storage speed.

It’s better to find any performance issues before installing ClickHouse.

# 5 \- Network Configuration

Network Configuration### **Networking And Server Room Planning**

The network used for your ClickHouse® cluster should be a fast network, ideally 10 Gbit or more.
ClickHouse nodes generate a lot of traffic to exchange the data between nodes (port 9009 for replication, and 9000 for distributed queries).
Zookeeper traffic in normal circumstances is moderate, but in some special cases can also be very significant.

For the zookeeper low latency is more important than bandwidth.

Keep the replicas isolated on the hardware level. This allows for cluster failover from possible outages.

- For Physical Environments: Avoid placing 2 ClickHouse replicas on the same server rack. Ideally, they should be on isolated network switches and an isolated power supply.
- For Clouds Environments: Use different availability zones between the ClickHouse replicas when possible (but be aware of the interzone traffic costs)

These considerations are the same as the Zookeeper nodes.

For example:



| **Rack** | **Server** | **Server** | **Server** | **Server** |
| --- | --- | --- | --- | --- |
| **Rack 1** | **CH\_SHARD1\_R1** | **CH\_SHARD2\_R1** | **CH\_SHARD3\_R1** | **ZOO\_1** |
| **Rack 2** | **CH\_SHARD1\_R2** | **CH\_SHARD2\_R2** | **CH\_SHARD3\_R2** | **ZOO\_2** |
| **Rack 3** | **ZOO3** |  |  |  |

#### **Network Ports And Firewall**

ClickHouse listens the following ports:

- 9000: clickhouse\-client, native clients, other clickhouse\-servers connect to here.
- 8123: HTTP clients
- 9009: Other replicas will connect here to download data.

For more information, see [CLICKHOUSE NETWORKING, PART 1](https://www.altinity.com/blog/2019/3/15/clickhouse-networking-part-1)
.

Zookeeper listens the following ports:

- 2181: Client connections.
- 2888: Inter\-ensemble connections.
- 3888: Leader election.

Outbound traffic from ClickHouse connects to the following ports:

- ZooKeeper: On port 2181\.
- Other CH nodes in the cluster: On port 9000 and 9009\.
- Dictionary sources: Depending on what was configured such as HTTP, MySQL, Mongo, etc.
- Kafka or Hadoop: If those integrations were enabled.

### **SSL**

For non\-trusted networks enable SSL/HTTPS. If acceptable, it is better to keep interserver communications unencrypted for performance reasons.

### **Naming Schema**

The best time to start creating a naming schema for the servers is before they’re created and configured.

There are a few features based on good server naming in ClickHouse:

- clickhouse\-client prompts: Allows a different prompt for clickhouse\-client per server hostname.
- Nearest hostname load balancing: For more information, see [Nearest Hostname](https://clickhouse.yandex/docs/en/operations/settings/settings/#load_balancing-nearest_hostname)
.

A good option is to use the following:

{datacenter}\-{serverroom}\-{rack identifier}\-{clickhouse cluster identifier}\-{shard number or server number}.

Other examples:

- rxv\-olap\-ch\-master\-sh01\-r01:
	- rxv \- location (rack\#15\)
	- olap \- product name
	- ch \= clickhouse
	- master \= stage
	- sh01 \= shard 1
	- r01 \= replica 1
- hetnzerde1\-ch\-prod\-01\.local:
	- hetnzerde1 \- location (also replica id)
	- ch \= clickhouse
	- prod \= stage
	- 01 \- server number / shard number in that DC
- sh01\.ch\-front.dev.aws\-east1a.example.com:
	- sh01 \- shard 01
	- ch\-front \- cluster name
	- dev \= stage
	- aws \= cloud provider
	- east1a \= region and availability zone

#### **Host Name References**

- [What are the best practices for domain names (dev, staging, production)?](https://stackoverflow.com/a/39336460/1555175)
- [9 Best Practices and Examples for Working with Kubernetes Labels](https://www.replex.io/blog/9-best-practices-and-examples-for-working-with-kubernetes-labels)
- [Thoughts On Hostname Nomenclature](https://devcentral.f5.com/s/articles/thoughts-on-hostname-nomenclature)

### **Additional Hostname Tips**

- Hostnames configured on the server should not change. If you do need to change the host name, one reference to use is [How to Change Hostname on Ubuntu 18\.04](https://linuxize.com/post/how-to-change-hostname-on-ubuntu-18-04/)
.
- The server should be accessible to other servers in the cluster via it’s hostname. Otherwise you will need to configure interserver\_hostname in your config.
- Ensure that `hostname --fqdn` and `getent hosts $(hostname --fqdn)` return the correct name and ip.
