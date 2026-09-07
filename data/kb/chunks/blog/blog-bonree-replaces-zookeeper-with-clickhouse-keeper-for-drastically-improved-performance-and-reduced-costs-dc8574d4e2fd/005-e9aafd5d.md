---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Bonree
topic: bonree-replaces-zookeeper-with-clickhouse-keeper-for-drastically-improved-performance-and-reduced-costs-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 9
---

and increased migration time. To address this, we developed an automated migration tool based on Ansible, an IT automation tool used for configuration management, software deployment, and advanced task orchestration like seamless rolling updates. The migration steps were:

1. Stop data ingestion.
2. Stop ClickHouse's merge and other background tasks.
3. Record comparison metrics.
4. Restart each ZooKeeper cluster to obtain the latest snapshot files.
5. Copy and convert snapshot files from ZooKeeper to ClickHouse Keeper.
6. Load snapshot files into ClickHouse Keeper and sample compare ZooKeeper and ClickHouse\-Keeper node contents.
7. Switch ClickHouse metadata storage from ZooKeeper to ClickHouse Keeper.
8. Compare metrics with step 3\.
9. Start ClickHouse's merge and background tasks and data ingestion.

Automating the migration avoided operational errors, significantly reducing the migration time from 2\-3 hours manually to a few minutes, minimizing the impact on business queries during the migration. The core automated process included:

```
1// Stop ClickHouse schema creation and table operations
2stopClickHouseManagers()
```
Copy command

```
1// Stop ClickHouse data write operations
2stopClickHouseConsumers()
```
Copy command

```
1// Stop ClickHouse merge and other background tasks
2ClickHouseStopMerges()
```
Copy command

```
1// Obtain the latest snapshot information from ZooKeeper clusters
2getNewZookeeperSnap()
```
Copy command

```
1// Convert ZooKeeper snapshots to ClickHouse-Keeper snapshots
2createAndExecConvertShell(housekeeperClusterName)
```
Copy command

```
1// Start ClickHouse clusters
2startClickHouses()
```
Copy command

```
1// Compare data before and after the migration
2checkClickHouseSelectData()
```
Copy command
## Challenges \#

The migration process described above is quite basic. Still, the environment was more complex, involving multiple clusters, various ZooKeeper node sets, and issues such as multi\-ZooKeeper to single ClickHouse\-Keeper transitions (the community version only supports one\-to\-one), encryption and authentication problems, and data verification efficiency challenges.

### Migrating multiple ZooKeeper clusters to a single ClickHouse Keeper cluster \#

ClickHouse Keeper significantly outperformed ZooKeeper in performance tests, and required much fewer resources. Therefore, multiple ZooKeeper clusters had to be reduced to a single cluster to avoid resource waste. The official `clickHouse-keeper-converter` tool supports only a one\-to\-one ZooKeeper to ClickHouse Keeper conversion. We solved this by:
