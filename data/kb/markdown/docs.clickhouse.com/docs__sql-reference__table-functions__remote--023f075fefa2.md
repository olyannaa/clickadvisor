# remote, remoteSecure \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- remote
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/remote.md)# remote, remoteSecure

Table function `remote` allows to access remote servers on\-the\-fly, i.e. without creating a [Distributed](/docs/engines/table-engines/special/distributed) table. Table function `remoteSecure` is same as `remote` but over a secure connection.


Both functions can be used in `SELECT` and `INSERT` queries.


## Syntax[​](#syntax "Direct link to Syntax")



```
remote(addresses_expr, [db, table, user [, password], sharding_key])
remote(addresses_expr, [db.table, user [, password], sharding_key])
remote(named_collection[, option=value [,..]])
remoteSecure(addresses_expr, [db, table, user [, password], sharding_key])
remoteSecure(addresses_expr, [db.table, user [, password], sharding_key])
remoteSecure(named_collection[, option=value [,..]])

```

## Parameters[​](#parameters "Direct link to Parameters")




| Argument Description| `addresses_expr` A remote server address or an expression that generates multiple addresses of remote servers. Format: `host` or `host:port`. The `host` can be specified as a server name, or as a IPv4 or IPv6 address. An IPv6 address must be specified in `[]`. The `port` is the TCP port on the remote server. If the port is omitted, it uses [tcp\_port](/docs/operations/server-configuration-parameters/settings#tcp_port) from the server config file for table function `remote` (by default, 9000\) and [tcp\_port\_secure](/docs/operations/server-configuration-parameters/settings#tcp_port_secure) for table function `remoteSecure` (by default, 9440\). For IPv6 addresses, a port is required. If only parameter `addresses_expr` is specified, `db` and `table` will use `system.one` by default. Type: [String](/docs/sql-reference/data-types/string).| `db` Database name. Type: [String](/docs/sql-reference/data-types/string).| `table` Table name. Type: [String](/docs/sql-reference/data-types/string).| `user` User name. If not specified, `default` is used. Type: [String](/docs/sql-reference/data-types/string).| `password` User password. If not specified, an empty password is used. Type: [String](/docs/sql-reference/data-types/string).| `sharding_key` Sharding key to support distributing data across nodes. For example: `insert into remote('127.0.0.1:9000,127.0.0.2', db, table, 'default', rand())`. Type: [UInt32](/docs/sql-reference/data-types/int-uint). | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Arguments also can be passed using [named collections](/docs/operations/named-collections).


## Returned value[​](#returned-value "Direct link to Returned value")


A table located on a remote server.


## Usage[​](#usage "Direct link to Usage")


As table functions `remote` and `remoteSecure` re\-establish the connection for each request, it is recommended to use a `Distributed` table instead. Also, if hostnames are set, the names are resolved, and errors are not counted when working with various replicas. When processing a large number of queries, always create the `Distributed` table ahead of time, and do not use the `remote` table function.


The `remote` table function can be useful in the following cases:


- One\-time data migration from one system to another
- Accessing a specific server for data comparison, debugging, and testing, i.e. ad\-hoc connections.
- Queries between various ClickHouse clusters for research purposes.
- Infrequent distributed requests that are made manually.
- Distributed requests where the set of servers is re\-defined each time.


### Addresses[​](#addresses "Direct link to Addresses")



```
example01-01-1
example01-01-1:9440
example01-01-1:9000
localhost
127.0.0.1
[::]:9440
[::]:9000
[2a02:6b8:0:1111::11]:9000

```

Multiple addresses can be comma\-separated. In this case, ClickHouse will use distributed processing and send the query to all specified addresses (like shards with different data). Example:



```
example01-01-1,example01-02-1

```

## Examples[​](#examples "Direct link to Examples")


### Selecting data from a remote server:[​](#selecting-data-from-a-remote-server "Direct link to Selecting data from a remote server:")



```
SELECT * FROM remote('127.0.0.1', db.remote_engine_table) LIMIT 3;

```

Or using [named collections](/docs/operations/named-collections):



```
CREATE NAMED COLLECTION creds AS
        host = '127.0.0.1',
        database = 'db';
SELECT * FROM remote(creds, table='remote_engine_table') LIMIT 3;

```

### Inserting data into a table on a remote server:[​](#inserting-data-into-a-table-on-a-remote-server "Direct link to Inserting data into a table on a remote server:")



```
CREATE TABLE remote_table (name String, value UInt32) ENGINE=Memory;
INSERT INTO FUNCTION remote('127.0.0.1', currentDatabase(), 'remote_table') VALUES ('test', 42);
SELECT * FROM remote_table;

```

### Migration of tables from one system to another:[​](#migration-of-tables-from-one-system-to-another "Direct link to Migration of tables from one system to another:")


This example uses one table from a sample dataset. The database is `imdb`, and the table is `actors`.


#### On the source ClickHouse system (the system that currently hosts the data)[​](#on-the-source-clickhouse-system-the-system-that-currently-hosts-the-data "Direct link to On the source ClickHouse system (the system that currently hosts the data)")


- Verify the source database and table name (`imdb.actors`)



```
show databases

```


```
show tables in imdb

```
- Get the CREATE TABLE statement from the source:



```
  SELECT create_table_query
  FROM system.tables
  WHERE database = 'imdb' AND table = 'actors'

```

Response



```
CREATE TABLE imdb.actors (`id` UInt32,
                          `first_name` String,
                          `last_name` String,
                          `gender` FixedString(1))
                ENGINE = MergeTree
                ORDER BY (id, first_name, last_name, gender);

```

#### On the destination ClickHouse system[​](#on-the-destination-clickhouse-system "Direct link to On the destination ClickHouse system")


- Create the destination database:



```
CREATE DATABASE imdb

```
- Using the CREATE TABLE statement from the source, create the destination:



```
CREATE TABLE imdb.actors (`id` UInt32,
                          `first_name` String,
                          `last_name` String,
                          `gender` FixedString(1))
                ENGINE = MergeTree
                ORDER BY (id, first_name, last_name, gender);

```


#### Back on the source deployment[​](#back-on-the-source-deployment "Direct link to Back on the source deployment")


Insert into the new database and table created on the remote system. You will need the host, port, username, password, destination database, and destination table.



```
INSERT INTO FUNCTION
remoteSecure('remote.clickhouse.cloud:9440', 'imdb.actors', 'USER', 'PASSWORD')
SELECT * from imdb.actors

```

## Globbing[​](#globs-in-addresses "Direct link to Globbing")


Patterns in `{ }` are used to generate a set of shards and to specify replicas. If there are multiple pairs of `{ }`, then the direct product of the corresponding sets is generated.


The following pattern types are supported.


- `{a,b,c}` \- Represents any of alternative strings `a`, `b` or `c`. The pattern is replaced with `a` in the first shard address and replaced with `b` in the second shard address and so on. For instance, `example0{1,2}-1` generates addresses `example01-1` and `example02-1`.
- `{N..M}` \- A range of numbers. This pattern generates shard addresses with incrementing indices from `N` to (and including) `M`. For instance, `example0{1..2}-1` generates `example01-1` and `example02-1`.
- `{0n..0m}` \- A range of numbers with leading zeroes. This pattern preserves leading zeroes in indices. For instance, `example{01..03}-1` generates `example01-1`, `example02-1` and `example03-1`.
- `{a|b}` \- Any number of variants separated by a `|`. The pattern specifies replicas. For instance, `example01-{1|2}` generates replicas `example01-1` and `example01-2`.


The query will be sent to the first healthy replica. However, for `remote` the replicas are iterated in the order currently set in the [load\_balancing](/docs/operations/settings/settings#load_balancing) setting.
The number of generated addresses is limited by [table\_function\_remote\_max\_addresses](/docs/operations/settings/settings#table_function_remote_max_addresses) setting.

[Previousredis](/docs/sql-reference/table-functions/redis)[Nexts3](/docs/sql-reference/table-functions/s3)- [Syntax](#syntax)- [Parameters](#parameters)- [Returned value](#returned-value)- [Usage](#usage)
	- [Addresses](#addresses)- [Examples](#examples)
	- [Selecting data from a remote server:](#selecting-data-from-a-remote-server)- [Inserting data into a table on a remote server:](#inserting-data-into-a-table-on-a-remote-server)- [Migration of tables from one system to another:](#migration-of-tables-from-one-system-to-another)- [Globbing](#globs-in-addresses)
Was this page helpful?
