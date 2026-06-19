# Shutting down a node \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. Shutting down a node
# Shutting down a node

It’s possible to shutdown server on fly, but that would lead to failure of some queries.

More safer way:

- Remove server (which is going to be disabled) from remote\_server section of config.xml on all servers.


	- avoid removing the last replica of the shard (that can lead to incorrect data placement if you use non\-random distribution)
- Remove server from load balancer, so new queries wouldn’t hit it.
- Detach Kafka / Rabbit / Buffer tables (if used), and Materialized\* databases.
- Wait until all already running queries would finish execution on it.
It’s possible to check it via query:


```
SHOW PROCESSLIST;

```
- Ensure there is no pending data in distributed tables


```
SELECT * FROM system.distribution_queue;
SYSTEM FLUSH DISTRIBUTED <table_name>;

```
- Run sync replica query in related shard replicas (others than the one you remove) via query:


```
SYSTEM SYNC REPLICA db.table;

```
- Shutdown server.

`SYSTEM SHUTDOWN` query by default doesn’t wait until query completion and tries to kill all queries immediately after receiving signal, if you want to change this behavior, you need to enable setting `shutdown_wait_unfinished_queries`.

[https://github.com/ClickHouse/ClickHouse/blob/d705f8ead4bdc837b8305131844f558ec002becc/programs/server/Server.cpp\#L1682](https://github.com/ClickHouse/ClickHouse/blob/d705f8ead4bdc837b8305131844f558ec002becc/programs/server/Server.cpp#L1682)

Last modified 2022\.12\.05: [Update altinity\-kb\-shutting\-down\-a\-node.md (26fcf4f)](https://github.com/Altinity/altinityknowledgebase/commit/26fcf4f66e49af563946b677783e38a0d41160c9)
