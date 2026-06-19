# Page for Distributed DDL \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Operators](/docs/sql-reference/operators)- Distributed DDL
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/operators/distributed-ddl.md)# Page for Distributed DDL

By default, the `CREATE`, `DROP`, `ALTER`, and `RENAME` queries affect only the current server where they are executed. In a cluster setup, it is possible to run such queries in a distributed manner with the `ON CLUSTER` clause.


For example, the following query creates the `all_hits` `Distributed` table on each host in `cluster`:



```
CREATE TABLE IF NOT EXISTS all_hits ON CLUSTER cluster (p Date, i Int32) ENGINE = Distributed(cluster, default, hits)

```

In order to run these queries correctly, each host must have the same cluster definition (to simplify syncing configs, you can use substitutions from ZooKeeper). They must also connect to the ZooKeeper servers.


The local version of the query will eventually be executed on each host in the cluster, even if some hosts are currently not available.


ReferencesThe order for executing queries within a single host is guaranteed.

[PreviousOperators](/docs/sql-reference/operators)[NextEXISTS](/docs/sql-reference/operators/exists)Was this page helpful?
