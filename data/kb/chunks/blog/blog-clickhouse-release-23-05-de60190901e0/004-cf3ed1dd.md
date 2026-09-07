---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-23-5-clickhouse
ch_version_introduced: '9.710'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 7
---

ClickHouse to function as a distributed system. This supports services such as data replication, distributed DDL query execution, leadership elections, and service discovery. ClickHouse Keeper is compatible with ZooKeeper, the legacy component used for this functionality in ClickHouse.

**ClickHouse Keeper is production ready. ClickHouse Cloud is running clickhouse\-keeper at large scale to support thousands of ClickHouse deployments in a multi\-tenant environment.**

Until now users would communicate with ClickHouse Keeper by sending commands directly over TCP using tools such as `nc` or `zkCli.sh`. While sufficient for basic debugging, this made administrative tasks a less than ideal user experience and were far from convenient. To address this, in 23\.5 we introduce `keeper-client` \- a simple tool built into ClickHouse for introspecting your ClickHouse Keeper.

To experiment with the client we can use our recently [released docker compose files](/blog/clickhouse-architectures-with-docker-compose), courtesy of our support team, to quickly start a multi\-node ClickHouse cluster. In the example below, we start a 2 node deployment with a single replicated shard and 3 keeper instances:

```
1git@github.com:ClickHouse/examples.git
2export CHKVER=23.5
3export CHVER=23.5
4cd examples/docker-compose-recipes/recipes/cluster_1S_2R/
5docker-compose up
```
Copy command
The above exposes our keeper instances on ports 9181, 9182 and 9183\. Connecting with the client is as simple as:

```
1./clickhouse keeper-client -h 127.0.0.1 -p 9181
2/ :) ruok
3imok
4/ :) ls
5clickhouse keeper
6/ :)
```
Copy command
Users can also exploit a `--query` parameter, similar to the ClickHouse Client, for bash scripting.

```
1./clickhouse keeper-client -h 127.0.0.1 -p 9181 --query "ls/"
2clickhouse keeper
```
Copy command
Further available options can be found [here](https://clickhouse.com/docs/en/operations/utilities/clickhouse-keeper-client).

## Parquet reading even faster (Michael Kolupaev) \#

Recently we [blogged about the improvements](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups) we’ve made with respect to the querying of Parquet files. These were the start of what we consider to be a journey in making ClickHouse the world’s fastest tool for querying Parquet files, either via [ClickHouse Local](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local) or ClickHouse Server. Unsatisfied with recent efforts to parallelise reading of Parquet, by exploiting row groups, 23\.5 adds further improvements.
