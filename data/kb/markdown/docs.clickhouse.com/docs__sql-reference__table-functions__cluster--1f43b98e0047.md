# clusterAllReplicas \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- cluster
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/cluster.md)# clusterAllReplicas

Allows accessing all shards (configured in the `remote_servers` section) of a cluster without creating a [Distributed](/docs/engines/table-engines/special/distributed) table. Only one replica of each shard is queried.


`clusterAllReplicas` function — same as `cluster`, but all replicas are queried. Each replica in a cluster is used as a separate shard/connection.


NoteAll available clusters are listed in the [system.clusters](/docs/operations/system-tables/clusters) table.


## Syntax[​](#syntax "Direct link to Syntax")



```
cluster(['cluster_name', db.table, sharding_key])
cluster(['cluster_name', db, table, sharding_key])
clusterAllReplicas(['cluster_name', db.table, sharding_key])
clusterAllReplicas(['cluster_name', db, table, sharding_key])

```

## Arguments[​](#arguments "Direct link to Arguments")




| Arguments Type| `cluster_name` Name of a cluster that is used to build a set of addresses and connection parameters to remote and local servers, set `default` if not specified.| `db.table` or `db`, `table` Name of a database and a table.| `sharding_key` A sharding key. Optional. Needs to be specified if the cluster has more than one shard. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |


## Returned value[​](#returned_value "Direct link to Returned value")


The dataset from clusters.


## Using macros[​](#using_macros "Direct link to Using macros")


`cluster_name` can contain macros — substitution in `{}`. The substituted value is taken from the [macros](/docs/operations/server-configuration-parameters/settings#macros) section of the server configuration file.


Example:



```
SELECT * FROM cluster('{cluster}', default.example_table);

```

## Usage and recommendations[​](#usage_recommendations "Direct link to Usage and recommendations")


Using the `cluster` and `clusterAllReplicas` table functions are less efficient than creating a `Distributed` table because in this case, the server connection is re\-established for every request. When processing a large number of queries, please always create the `Distributed` table ahead of time, and do not use the `cluster` and `clusterAllReplicas` table functions.


The `cluster` and `clusterAllReplicas` table functions can be useful in the following cases:


- Accessing a specific cluster for data comparison, debugging, and testing.
- Queries to various ClickHouse clusters and replicas for research purposes.
- Infrequent distributed requests that are made manually.


Connection settings like `host`, `port`, `user`, `password`, `compression`, `secure` are taken from `<remote_servers>` config section. See details in [Distributed engine](/docs/engines/table-engines/special/distributed).


## Related[​](#related "Direct link to Related")


- [skip\_unavailable\_shards](/docs/operations/settings/settings#skip_unavailable_shards)
- [load\_balancing](/docs/operations/settings/settings#load_balancing)
[PreviousazureBlobStorageCluster](/docs/sql-reference/table-functions/azureBlobStorageCluster)[NextdeltaLake](/docs/sql-reference/table-functions/deltalake)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Using macros](#using_macros)- [Usage and recommendations](#usage_recommendations)- [Related](#related)
Was this page helpful?
