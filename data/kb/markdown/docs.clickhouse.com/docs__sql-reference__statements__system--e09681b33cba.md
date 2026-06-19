# SYSTEM Statements \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- SYSTEM
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/system.md)# SYSTEM Statements


## SYSTEM RELOAD EMBEDDED DICTIONARIES[​](#reload-embedded-dictionaries "Direct link to SYSTEM RELOAD EMBEDDED DICTIONARIES")


Reload all [Internal dictionaries](/docs/sql-reference/statements/create/dictionary).
By default, internal dictionaries are disabled.
Always returns `Ok.` regardless of the result of the internal dictionary update.


## SYSTEM RELOAD DICTIONARIES[​](#reload-dictionaries "Direct link to SYSTEM RELOAD DICTIONARIES")


The `SYSTEM RELOAD DICTIONARIES` query reloads dictionaries with a status of `LOADED` (see the `status` column of [`system.dictionaries`](/docs/operations/system-tables/dictionaries)), i.e dictionaries that have been successfully loaded before.
By default, dictionaries are loaded lazily (see [dictionaries\_lazy\_load](/docs/operations/server-configuration-parameters/settings#dictionaries_lazy_load)), so instead of being loaded automatically at startup, they are initialized on first access through use of the [`dictGet`](/docs/sql-reference/functions/ext-dict-functions#dictGet) function or use of `SELECT` from tables with `ENGINE = Dictionary`.


**Syntax**



```
SYSTEM RELOAD DICTIONARIES [ON CLUSTER cluster_name]

```

## SYSTEM RELOAD DICTIONARY[​](#reload-dictionary "Direct link to SYSTEM RELOAD DICTIONARY")


Completely reloads a dictionary `dictionary_name`, regardless of the state of the dictionary (LOADED / NOT\_LOADED / FAILED).
Always returns `Ok.` regardless of the result of updating the dictionary.



```
SYSTEM RELOAD DICTIONARY [ON CLUSTER cluster_name] dictionary_name

```

The status of the dictionary can be checked by querying the `system.dictionaries` table.



```
SELECT name, status FROM system.dictionaries;

```

## SYSTEM RELOAD MODELS[​](#reload-models "Direct link to SYSTEM RELOAD MODELS")


NoteThis statement and `SYSTEM RELOAD MODEL` merely unload catboost models from the clickhouse\-library\-bridge. The function `catboostEvaluate()`
loads a model upon first access if it is not loaded yet.


Unloads all CatBoost models.


**Syntax**



```
SYSTEM RELOAD MODELS [ON CLUSTER cluster_name]

```

## SYSTEM RELOAD MODEL[​](#reload-model "Direct link to SYSTEM RELOAD MODEL")


Unloads a CatBoost model at `model_path`.


**Syntax**



```
SYSTEM RELOAD MODEL [ON CLUSTER cluster_name] <model_path>

```

## SYSTEM RELOAD FUNCTIONS[​](#reload-functions "Direct link to SYSTEM RELOAD FUNCTIONS")


Reloads all registered [executable user defined functions](/docs/sql-reference/functions/udf#executable-user-defined-functions) or one of them from a configuration file.


**Syntax**



```
SYSTEM RELOAD FUNCTIONS [ON CLUSTER cluster_name]
SYSTEM RELOAD FUNCTION [ON CLUSTER cluster_name] function_name

```

## SYSTEM RELOAD ASYNCHRONOUS METRICS[​](#reload-asynchronous-metrics "Direct link to SYSTEM RELOAD ASYNCHRONOUS METRICS")


Re\-calculates all [asynchronous metrics](/docs/operations/system-tables/asynchronous_metrics). Since asynchronous metrics are periodically updated based on setting [asynchronous\_metrics\_update\_period\_s](/docs/operations/server-configuration-parameters/settings), updating them manually using this statement is typically not necessary.



```
SYSTEM RELOAD ASYNCHRONOUS METRICS [ON CLUSTER cluster_name]

```

## SYSTEM CLEAR\|DROP DNS CACHE[​](#drop-dns-cache "Direct link to SYSTEM CLEAR|DROP DNS CACHE")


Clears ClickHouse's internal DNS cache. Sometimes (for old ClickHouse versions) it is necessary to use this command when changing the infrastructure (changing the IP address of another ClickHouse server or the server used by dictionaries).


For more convenient (automatic) cache management, see `disable_internal_dns_cache`, `dns_cache_max_entries`, `dns_cache_update_period` parameters.


## SYSTEM CLEAR\|DROP MARK CACHE[​](#drop-mark-cache "Direct link to SYSTEM CLEAR|DROP MARK CACHE")


Clears the mark cache.


## SYSTEM CLEAR\|DROP ICEBERG METADATA CACHE[​](#drop-iceberg-metadata-cache "Direct link to SYSTEM CLEAR|DROP ICEBERG METADATA CACHE")


Clears the iceberg metadata cache.


## SYSTEM CLEAR\|DROP AVRO SCHEMA CACHE[​](#drop-avro-schema-cache "Direct link to SYSTEM CLEAR|DROP AVRO SCHEMA CACHE")


Clears the per\-URL Confluent Schema Registry caches used by the `AvroConfluent` format. This drops both the schema\-fetch cache (id → schema) and the schema\-registration cache (subject \+ schema → id), so subsequent reads and writes fall back to the registry server. Useful when a schema was deleted or rewritten on the registry side, or to verify the registry's idempotency in tests.


## SYSTEM DROP PARQUET METADATA CACHE[​](#drop-parquet-metadata-cache "Direct link to SYSTEM DROP PARQUET METADATA CACHE")


Clears the parquet metadata cache.


## SYSTEM CLEAR\|DROP TEXT INDEX CACHES[​](#drop-text-index-caches "Direct link to SYSTEM CLEAR|DROP TEXT INDEX CACHES")


Clears the text index's header, dictionary and postings caches.


If you like to drop one of these caches individually, you can run


- `SYSTEM CLEAR TEXT INDEX HEADER CACHE`,
- `SYSTEM CLEAR TEXT INDEX DICTIONARY CACHE`, or
- `SYSTEM CLEAR TEXT INDEX POSTINGS CACHE`


## SYSTEM DROP REPLICA[​](#drop-replica "Direct link to SYSTEM DROP REPLICA")


Dead replicas of `ReplicatedMergeTree` tables can be dropped using following syntax:



```
SYSTEM DROP REPLICA 'replica_name' FROM TABLE database.table;
SYSTEM DROP REPLICA 'replica_name' FROM DATABASE database;
SYSTEM DROP REPLICA 'replica_name';
SYSTEM DROP REPLICA 'replica_name' FROM ZKPATH '/path/to/table/in/zk';

```

Queries will remove the `ReplicatedMergeTree` replica path in ZooKeeper. It is useful when the replica is dead and its metadata cannot be removed from ZooKeeper by `DROP TABLE` because there is no such table anymore. It will only drop the inactive/stale replica, and it cannot drop local replica, please use `DROP TABLE` for that. `DROP REPLICA` does not drop any tables and does not remove any data or metadata from disk.


The first one removes metadata of `'replica_name'` replica of `database.table` table.
The second one does the same for all replicated tables in the database.
The third one does the same for all replicated tables on the local server.
The fourth one is useful to remove metadata of dead replica when all other replicas of a table were dropped. It requires the table path to be specified explicitly. It must be the same path as was passed to the first argument of `ReplicatedMergeTree` engine on table creation.


## SYSTEM DROP DATABASE REPLICA[​](#drop-database-replica "Direct link to SYSTEM DROP DATABASE REPLICA")


Dead replicas of `Replicated` databases can be dropped using following syntax:



```
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'] FROM DATABASE database;
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'];
SYSTEM DROP DATABASE REPLICA 'replica_name' [FROM SHARD 'shard_name'] FROM ZKPATH '/path/to/table/in/zk';

```

Similar to `SYSTEM DROP REPLICA`, but removes the `Replicated` database replica path from ZooKeeper when there's no database to run `DROP DATABASE`. Please note that it does not remove `ReplicatedMergeTree` replicas (so you may need `SYSTEM DROP REPLICA` as well). Shard and replica names are the names that were specified in `Replicated` engine arguments when creating the database. Also, these names can be obtained from `database_shard_name` and `database_replica_name` columns in `system.clusters`. If the `FROM SHARD` clause is missing, then `replica_name` must be a full replica name in `shard_name|replica_name` format.


## SYSTEM CLEAR\|DROP UNCOMPRESSED CACHE[​](#drop-uncompressed-cache "Direct link to SYSTEM CLEAR|DROP UNCOMPRESSED CACHE")


Clears the uncompressed data cache.
The uncompressed data cache is enabled/disabled with the query/user/profile\-level setting [`use_uncompressed_cache`](/docs/operations/settings/settings#use_uncompressed_cache).
Its size can be configured using the server\-level setting [`uncompressed_cache_size`](/docs/operations/server-configuration-parameters/settings#uncompressed_cache_size).


## SYSTEM CLEAR\|DROP COMPILED EXPRESSION CACHE[​](#drop-compiled-expression-cache "Direct link to SYSTEM CLEAR|DROP COMPILED EXPRESSION CACHE")


Clears the compiled expression cache.
The compiled expression cache is enabled/disabled with the query/user/profile\-level setting [`compile_expressions`](/docs/operations/settings/settings#compile_expressions).


## SYSTEM CLEAR\|DROP QUERY CONDITION CACHE[​](#drop-query-condition-cache "Direct link to SYSTEM CLEAR|DROP QUERY CONDITION CACHE")


Clears the query condition cache.


## SYSTEM CLEAR\|DROP QUERY CACHE[​](#drop-query-cache "Direct link to SYSTEM CLEAR|DROP QUERY CACHE")



```
SYSTEM CLEAR QUERY CACHE;
SYSTEM CLEAR QUERY CACHE TAG '<tag>'

```

Clears the [query cache](/docs/operations/query-cache).
If a tag is specified, only query cache entries with the specified tag are deleted.


## SYSTEM CLEAR\|DROP FORMAT SCHEMA CACHE[​](#system-drop-schema-format "Direct link to SYSTEM CLEAR|DROP FORMAT SCHEMA CACHE")


Clears cache for schemas loaded from [`format_schema_path`](/docs/operations/server-configuration-parameters/settings#format_schema_path).


Supported targets:


- Protobuf: Removes imported Protobuf message definitions from memory.
- Files: Deletes cached schema files stored locally in the [`format_schema_path`](/docs/operations/server-configuration-parameters/settings#format_schema_path), generated when `format_schema_source` is set to `query`.
Note: If no target is specified, both caches are cleared.



```
SYSTEM CLEAR|DROP FORMAT SCHEMA CACHE [FOR Protobuf/Files]

```

## SYSTEM FLUSH LOGS[​](#flush-logs "Direct link to SYSTEM FLUSH LOGS")


Flushes buffered log messages to system tables, e.g. system.query\_log. Mainly useful for debugging since most system tables have a default flush interval of 7\.5 seconds.
This will also create system tables even if message queue is empty.



```
SYSTEM FLUSH LOGS [ON CLUSTER cluster_name] [log_name|[database.table]] [, ...]

```

If you don't want to flush everything, you can flush one or more individual logs by passing either their name or their target table:



```
SYSTEM FLUSH LOGS query_log, system.query_views_log;

```

## SYSTEM RELOAD CONFIG[​](#reload-config "Direct link to SYSTEM RELOAD CONFIG")


Reloads ClickHouse configuration. Used when configuration is stored in ZooKeeper. Note that `SYSTEM RELOAD CONFIG` does not reload `USER` configuration stored in ZooKeeper, it only reloads `USER` configuration that is stored in `users.xml`. To reload all `USER` config use `SYSTEM RELOAD USERS`



```
SYSTEM RELOAD CONFIG [ON CLUSTER cluster_name]

```

## SYSTEM RELOAD USERS[​](#reload-users "Direct link to SYSTEM RELOAD USERS")


Reloads all access storages, including: users.xml, local disk access storage, replicated (in ZooKeeper) access storage.



```
SYSTEM RELOAD USERS [ON CLUSTER cluster_name]

```

## SYSTEM SHUTDOWN[​](#shutdown "Direct link to SYSTEM SHUTDOWN")


Not supported in ClickHouse Cloud
Normally shuts down ClickHouse (like `service clickhouse-server stop` / `kill {$pid_clickhouse-server}`)


## SYSTEM KILL[​](#kill "Direct link to SYSTEM KILL")


Aborts ClickHouse process (like `kill -9 {$ pid_clickhouse-server}`)


## SYSTEM INSTRUMENT[​](#instrument "Direct link to SYSTEM INSTRUMENT")


Manages instrumentation points using LLVM's XRay feature which is available when ClickHouse is built using `ENABLE_XRAY=1`.
This enables to debug and profile in production without modifying the source code and with minimal overhead.
When no instrumentation point is added, the performance penalty is negligible because it only adds an extra jump to a nearby
address at the prolog and epilog of those functions that are longer than 200 instructions.


### SYSTEM INSTRUMENT ADD[​](#instrument-add "Direct link to SYSTEM INSTRUMENT ADD")


Adds a new instrumentation point. Functions instrumented can be inspected in the [`system.instrumentation`](/docs/operations/system-tables/instrumentation) system table. More than one handler can be added for the same function, and they will be executed in the same order the instrumentation is added.
The functions to be instrumented can be collected from [`system.symbols`](/docs/operations/system-tables/symbols) system table.


There are three different kind of handlers to add to functions:


**Syntax**



```
SYSTEM INSTRUMENT ADD FUNCTION HANDLER [PARAMETERS]

```

where `FUNCTION` is any function or substring of a function such as `QueryMetricLog::startQuery`, and the handler one of the following


#### LOG[​](#instrument-add-log "Direct link to LOG")


Prints the text provided as an argument and the stack trace either on `ENTRY` or `EXIT` of the function.



```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' LOG ENTRY 'this is a log printed at entry'
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' LOG EXIT 'this is a log printed at exit'

```

#### SLEEP[​](#instrument-add-sleep "Direct link to SLEEP")


Sleeps for a number of fix amount of seconds either on `ENTRY` or `EXIT`:



```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' SLEEP ENTRY 0.5

```

or for a uniformly distributed random amount of seconds providing min and max separated by a whitespace:



```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' SLEEP ENTRY 0 1

```

#### PROFILE[​](#instrument-add-profile "Direct link to PROFILE")


Measures the time spent between `ENTRY` and `EXIT` of a function.
The result of the profiling is stored in [`system.trace_log`](/docs/operations/system-tables/trace_log) and can be converted
to [Chrome Event Trace Format](/docs/operations/system-tables/trace_log#chrome-event-trace-format).



```
SYSTEM INSTRUMENT ADD 'QueryMetricLog::startQuery' PROFILE

```

### SYSTEM INSTRUMENT REMOVE[​](#instrument-remove "Direct link to SYSTEM INSTRUMENT REMOVE")


Removes either a single instrumentation point with:



```
SYSTEM INSTRUMENT REMOVE ID

```

all of them using the `ALL` parameter:



```
SYSTEM INSTRUMENT REMOVE ALL

```

a set of IDs from a subquery:



```
SYSTEM INSTRUMENT REMOVE (SELECT id FROM system.instrumentation WHERE handler = 'log')

```

or all instrumentation points that match a given function\_name:



```
SYSTEM INSTRUMENT REMOVE 'QueryMetricLog::startQuery'

```

The instrumentation point information can be collected from [`system.instrumentation`](/docs/operations/system-tables/instrumentation) system table.


## Managing Distributed Tables[​](#managing-distributed-tables "Direct link to Managing Distributed Tables")


ClickHouse can manage [distributed](/docs/engines/table-engines/special/distributed) tables. When a user inserts data into these tables, ClickHouse first creates a queue of the data that should be sent to cluster nodes, then asynchronously sends it. You can manage queue processing with the [`STOP DISTRIBUTED SENDS`](#stop-distributed-sends), [FLUSH DISTRIBUTED](#flush-distributed), and [`START DISTRIBUTED SENDS`](#start-distributed-sends) queries. You can also synchronously insert distributed data with the [`distributed_foreground_insert`](/docs/operations/settings/settings#distributed_foreground_insert) setting.


### SYSTEM STOP DISTRIBUTED SENDS[​](#stop-distributed-sends "Direct link to SYSTEM STOP DISTRIBUTED SENDS")


Disables background data distribution when inserting data into distributed tables.



```
SYSTEM STOP DISTRIBUTED SENDS [db.]<distributed_table_name> [ON CLUSTER cluster_name]

```

NoteIn case of [`prefer_localhost_replica`](/docs/operations/settings/settings#prefer_localhost_replica) is enabled (the default), the data to local shard will be inserted anyway.


### SYSTEM FLUSH DISTRIBUTED[​](#flush-distributed "Direct link to SYSTEM FLUSH DISTRIBUTED")


Forces ClickHouse to send data to cluster nodes synchronously. If any nodes are unavailable, ClickHouse throws an exception and stops query execution. You can retry the query until it succeeds, which will happen when all nodes are back online.


You can also override some settings via `SETTINGS` clause, this can be useful to avoid some temporary limitations, like `max_concurrent_queries_for_all_users` or `max_memory_usage`.



```
SYSTEM FLUSH DISTRIBUTED [db.]<distributed_table_name> [ON CLUSTER cluster_name] [SETTINGS ...]

```

NoteEach pending block is stored in disk with settings from the initial INSERT query, so that is why sometimes you may want to override settings.


### SYSTEM START DISTRIBUTED SENDS[​](#start-distributed-sends "Direct link to SYSTEM START DISTRIBUTED SENDS")


Enables background data distribution when inserting data into distributed tables.



```
SYSTEM START DISTRIBUTED SENDS [db.]<distributed_table_name> [ON CLUSTER cluster_name]

```

### SYSTEM STOP LISTEN[​](#stop-listen "Direct link to SYSTEM STOP LISTEN")


Closes the socket and gracefully terminates the existing connections to the server on the specified port with the specified protocol.


However, if the corresponding protocol settings were not specified in the clickhouse\-server configuration, this command will have no effect.



```
SYSTEM STOP LISTEN [ON CLUSTER cluster_name] [QUERIES ALL | QUERIES DEFAULT | QUERIES CUSTOM | TCP | TCP WITH PROXY | TCP SECURE | HTTP | HTTPS | MYSQL | GRPC | POSTGRESQL | PROMETHEUS | CUSTOM 'protocol']

```

- If `CUSTOM 'protocol'` modifier is specified, the custom protocol with the specified name defined in the protocols section of the server configuration will be stopped.
- If `QUERIES ALL [EXCEPT .. [,..]]` modifier is specified, all protocols are stopped, unless specified with `EXCEPT` clause.
- If `QUERIES DEFAULT [EXCEPT .. [,..]]` modifier is specified, all default protocols are stopped, unless specified with `EXCEPT` clause.
- If `QUERIES CUSTOM [EXCEPT .. [,..]]` modifier is specified, all custom protocols are stopped, unless specified with `EXCEPT` clause.


### SYSTEM START LISTEN[​](#start-listen "Direct link to SYSTEM START LISTEN")


Allows new connections to be established on the specified protocols.


However, if the server on the specified port and protocol was not stopped using the SYSTEM STOP LISTEN command, this command will have no effect.



```
SYSTEM START LISTEN [ON CLUSTER cluster_name] [QUERIES ALL | QUERIES DEFAULT | QUERIES CUSTOM | TCP | TCP WITH PROXY | TCP SECURE | HTTP | HTTPS | MYSQL | GRPC | POSTGRESQL | PROMETHEUS | CUSTOM 'protocol']

```

## Managing MergeTree Tables[​](#managing-mergetree-tables "Direct link to Managing MergeTree Tables")


ClickHouse can manage background processes in [MergeTree](/docs/engines/table-engines/mergetree-family/mergetree) tables.


### SYSTEM STOP MERGES[​](#stop-merges "Direct link to SYSTEM STOP MERGES")


Not supported in ClickHouse Cloud
Provides possibility to stop background merges for tables in the MergeTree family:



```
SYSTEM STOP MERGES [ON CLUSTER cluster_name] [ON VOLUME <volume_name> | [db.]merge_tree_family_table_name]

```

Note`DETACH / ATTACH` table will start background merges for the table even in case when merges have been stopped for all MergeTree tables before.


### SYSTEM START MERGES[​](#start-merges "Direct link to SYSTEM START MERGES")


Not supported in ClickHouse Cloud
Provides possibility to start background merges for tables in the MergeTree family:



```
SYSTEM START MERGES [ON CLUSTER cluster_name] [ON VOLUME <volume_name> | [db.]merge_tree_family_table_name]

```

### SYSTEM STOP TTL MERGES[​](#stop-ttl-merges "Direct link to SYSTEM STOP TTL MERGES")


Not supported in ClickHouse Cloud
Provides possibility to stop background delete old data according to [TTL expression](/docs/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-ttl) for tables in the MergeTree family:
Returns `Ok.` even if table does not exist or table has not MergeTree engine. Returns error when database does not exist:



```
SYSTEM STOP TTL MERGES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```

### SYSTEM START TTL MERGES[​](#start-ttl-merges "Direct link to SYSTEM START TTL MERGES")


Not supported in ClickHouse Cloud
Provides possibility to start background delete old data according to [TTL expression](/docs/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-ttl) for tables in the MergeTree family:
Returns `Ok.` even if table does not exist. Returns error when database does not exist:



```
SYSTEM START TTL MERGES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```

### SYSTEM STOP MOVES[​](#stop-moves "Direct link to SYSTEM STOP MOVES")


Provides possibility to stop background move data according to [TTL table expression with TO VOLUME or TO DISK clause](/docs/engines/table-engines/mergetree-family/mergetree#mergetree-table-ttl) for tables in the MergeTree family:
Returns `Ok.` even if table does not exist. Returns error when database does not exist:



```
SYSTEM STOP MOVES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```

### SYSTEM START MOVES[​](#start-moves "Direct link to SYSTEM START MOVES")


Provides possibility to start background move data according to [TTL table expression with TO VOLUME and TO DISK clause](/docs/engines/table-engines/mergetree-family/mergetree#mergetree-table-ttl) for tables in the MergeTree family:
Returns `Ok.` even if table does not exist. Returns error when database does not exist:



```
SYSTEM START MOVES [ON CLUSTER cluster_name] [[db.]merge_tree_family_table_name]

```

### SYSTEM SYSTEM UNFREEZE[​](#query_language-system-unfreeze "Direct link to SYSTEM SYSTEM UNFREEZE")


Clears a frozen backup with the specified name from all the disks. See more about unfreezing separate parts in [ALTER TABLE table\_name UNFREEZE WITH NAME](/docs/sql-reference/statements/alter/partition#unfreeze-partition) 



```
SYSTEM UNFREEZE WITH NAME <backup_name>

```

### SYSTEM WAIT LOADING PARTS[​](#wait-loading-parts "Direct link to SYSTEM WAIT LOADING PARTS")


Wait until all asynchronously loading data parts of a table (outdated data parts) will became loaded.



```
SYSTEM WAIT LOADING PARTS [ON CLUSTER cluster_name] [db.]merge_tree_family_table_name

```

## Managing ReplicatedMergeTree Tables[​](#managing-replicatedmergetree-tables "Direct link to Managing ReplicatedMergeTree Tables")


ClickHouse can manage background replication related processes in [ReplicatedMergeTree](/docs/engines/table-engines/mergetree-family/replication) tables.


### SYSTEM STOP FETCHES[​](#stop-fetches "Direct link to SYSTEM STOP FETCHES")


Not supported in ClickHouse Cloud
Provides possibility to stop background fetches for inserted parts for tables in the `ReplicatedMergeTree` family:
Always returns `Ok.` regardless of the table engine and even if table or database does not exist.



```
SYSTEM STOP FETCHES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM START FETCHES[​](#start-fetches "Direct link to SYSTEM START FETCHES")


Not supported in ClickHouse Cloud
Provides possibility to start background fetches for inserted parts for tables in the `ReplicatedMergeTree` family:
Always returns `Ok.` regardless of the table engine and even if table or database does not exist.



```
SYSTEM START FETCHES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM STOP REPLICATED SENDS[​](#stop-replicated-sends "Direct link to SYSTEM STOP REPLICATED SENDS")


Provides possibility to stop background sends to other replicas in cluster for new inserted parts for tables in the `ReplicatedMergeTree` family:



```
SYSTEM STOP REPLICATED SENDS [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM START REPLICATED SENDS[​](#start-replicated-sends "Direct link to SYSTEM START REPLICATED SENDS")


Provides possibility to start background sends to other replicas in cluster for new inserted parts for tables in the `ReplicatedMergeTree` family:



```
SYSTEM START REPLICATED SENDS [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM STOP REPLICATION QUEUES[​](#stop-replication-queues "Direct link to SYSTEM STOP REPLICATION QUEUES")


Provides possibility to stop background fetch tasks from replication queues which stored in Zookeeper for tables in the `ReplicatedMergeTree` family. Possible background tasks types \- merges, fetches, mutation, DDL statements with ON CLUSTER clause:



```
SYSTEM STOP REPLICATION QUEUES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM START REPLICATION QUEUES[​](#start-replication-queues "Direct link to SYSTEM START REPLICATION QUEUES")


Provides possibility to start background fetch tasks from replication queues which stored in Zookeeper for tables in the `ReplicatedMergeTree` family. Possible background tasks types \- merges, fetches, mutation, DDL statements with ON CLUSTER clause:



```
SYSTEM START REPLICATION QUEUES [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM STOP PULLING REPLICATION LOG[​](#stop-pulling-replication-log "Direct link to SYSTEM STOP PULLING REPLICATION LOG")


Stops loading new entries from replication log to replication queue in a `ReplicatedMergeTree` table.



```
SYSTEM STOP PULLING REPLICATION LOG [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM START PULLING REPLICATION LOG[​](#start-pulling-replication-log "Direct link to SYSTEM START PULLING REPLICATION LOG")


Cancels `SYSTEM STOP PULLING REPLICATION LOG`.



```
SYSTEM START PULLING REPLICATION LOG [ON CLUSTER cluster_name] [[db.]replicated_merge_tree_family_table_name]

```

### SYSTEM SYNC REPLICA[​](#sync-replica "Direct link to SYSTEM SYNC REPLICA")


Wait until a `ReplicatedMergeTree` table will be synced with other replicas in a cluster, but no more than `receive_timeout` seconds.



```
SYSTEM SYNC REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name [IF EXISTS] [STRICT | LIGHTWEIGHT [FROM 'srcReplica1'[, 'srcReplica2'[, ...]]] | PULL]

```

After running this statement the `[db.]replicated_merge_tree_family_table_name` fetches commands from the common replicated log into its own replication queue, and then the query waits till the replica processes all of the fetched commands. The following modifiers are supported:


- With `IF EXISTS` (available since 25\.6\) the query won't throw an error if the table does not exists. This is useful when adding a new replica to a cluster, when it's already part of the cluster configuration but it is still in the process of creating and synchronizing the table.
- If a `STRICT` modifier was specified then the query waits for the replication queue to become empty. The `STRICT` version may never succeed if new entries constantly appear in the replication queue.
- If a `LIGHTWEIGHT` modifier was specified then the query waits only for `GET_PART`, `ATTACH_PART`, `DROP_RANGE`, `REPLACE_RANGE` and `DROP_PART` entries to be processed.
Additionally, the LIGHTWEIGHT modifier supports an optional FROM 'srcReplicas' clause, where 'srcReplicas' is a comma\-separated list of source replica names. This extension allows for more targeted synchronization by focusing only on replication tasks originating from the specified source replicas.
- If a `PULL` modifier was specified then the query pulls new replication queue entries from ZooKeeper, but does not wait for anything to be processed.


### SYNC DATABASE REPLICA[​](#sync-database-replica "Direct link to SYNC DATABASE REPLICA")


Waits until the specified [replicated database](/docs/engines/database-engines/replicated) applies all schema changes from the DDL queue of that database.


**Syntax**



```
SYSTEM SYNC DATABASE REPLICA replicated_database_name;

```

### SYSTEM RESTART REPLICA[​](#restart-replica "Direct link to SYSTEM RESTART REPLICA")


Provides possibility to reinitialize Zookeeper session's state for `ReplicatedMergeTree` table, will compare current state with Zookeeper as source of truth and add tasks to Zookeeper queue if needed.
Initialization of replication queue based on ZooKeeper data happens in the same way as for `ATTACH TABLE` statement. For a short time, the table will be unavailable for any operations.



```
SYSTEM RESTART REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name

```

### SYSTEM RESTORE REPLICA[​](#restore-replica "Direct link to SYSTEM RESTORE REPLICA")


Restores a replica if data is \[possibly] present but Zookeeper metadata is lost.


Works only on readonly `ReplicatedMergeTree` tables.


One may execute query after:


- ZooKeeper root `/` loss.
- Replicas path `/replicas` loss.
- Individual replica path `/replicas/replica_name/` loss.


Replica attaches locally found parts and sends info about them to Zookeeper.
Parts present on a replica before metadata loss are not re\-fetched from other ones if not being outdated (so replica restoration does not mean re\-downloading all data over the network).


NoteParts in all states are moved to `detached/` folder. Parts active before data loss (committed) are attached.


### SYSTEM RESTORE DATABASE REPLICA[​](#restore-database-replica "Direct link to SYSTEM RESTORE DATABASE REPLICA")


Restores a replica if data is \[possibly] present but Zookeeper metadata is lost.


**Syntax**



```
SYSTEM RESTORE DATABASE REPLICA repl_db [ON CLUSTER cluster]

```

**Example**



```
CREATE DATABASE repl_db
ENGINE=Replicated("/clickhouse/repl_db", shard1, replica1);

CREATE TABLE repl_db.test_table (n UInt32)
ENGINE = ReplicatedMergeTree
ORDER BY n PARTITION BY n % 10;

-- zookeeper_delete_path("/clickhouse/repl_db", recursive=True) <- root loss.

SYSTEM RESTORE DATABASE REPLICA repl_db;

```

**Syntax**



```
SYSTEM RESTORE REPLICA [db.]replicated_merge_tree_family_table_name [ON CLUSTER cluster_name]

```

Alternative syntax:



```
SYSTEM RESTORE REPLICA [ON CLUSTER cluster_name] [db.]replicated_merge_tree_family_table_name

```

**Example**


Creating a table on multiple servers. After the replica's metadata in ZooKeeper is lost, the table will attach as read\-only as metadata is missing. The last query needs to execute on every replica.



```
CREATE TABLE test(n UInt32)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/test/', '{replica}')
ORDER BY n PARTITION BY n % 10;

INSERT INTO test SELECT * FROM numbers(1000);

-- zookeeper_delete_path("/clickhouse/tables/test", recursive=True) <- root loss.

SYSTEM RESTART REPLICA test;
SYSTEM RESTORE REPLICA test;

```

Another way:



```
SYSTEM RESTORE REPLICA test ON CLUSTER cluster;

```

### SYSTEM RESTART REPLICAS[​](#restart-replicas "Direct link to SYSTEM RESTART REPLICAS")


Provides possibility to reinitialize Zookeeper sessions state for all `ReplicatedMergeTree` tables, will compare current state with Zookeeper as source of true and add tasks to Zookeeper queue if needed


### SYSTEM CLEAR\|DROP FILESYSTEM CACHE[​](#drop-filesystem-cache "Direct link to SYSTEM CLEAR|DROP FILESYSTEM CACHE")


Allows to drop filesystem cache.



```
SYSTEM CLEAR FILESYSTEM CACHE [ON CLUSTER cluster_name]

```

### SYSTEM SYNC FILE CACHE[​](#sync-file-cache "Direct link to SYSTEM SYNC FILE CACHE")


NoteIt's too heavy and has potential for misuse.


Will do sync syscall.



```
SYSTEM SYNC FILE CACHE [ON CLUSTER cluster_name]

```

### SYSTEM LOAD PRIMARY KEY[​](#load-primary-key "Direct link to SYSTEM LOAD PRIMARY KEY")


Load the primary keys for the given table or for all tables.



```
SYSTEM LOAD PRIMARY KEY [db.]name

```


```
SYSTEM LOAD PRIMARY KEY

```

### SYSTEM UNLOAD PRIMARY KEY[​](#unload-primary-key "Direct link to SYSTEM UNLOAD PRIMARY KEY")


Unload the primary keys for the given table or for all tables.



```
SYSTEM UNLOAD PRIMARY KEY [db.]name

```


```
SYSTEM UNLOAD PRIMARY KEY

```

## Managing Refreshable Materialized Views[​](#managing-refreshable-materialized-views "Direct link to Managing Refreshable Materialized Views")


Commands to control background tasks performed by [Refreshable Materialized Views](/docs/sql-reference/statements/create/view#refreshable-materialized-view)


Keep an eye on [`system.view_refreshes`](/docs/operations/system-tables/view_refreshes) while using them.


### SYSTEM STOP \[REPLICATED] VIEW, STOP VIEWS[​](#stop-view-stop-views "Direct link to SYSTEM STOP [REPLICATED] VIEW, STOP VIEWS")


Disable periodic refreshing of the given view or all refreshable views. If a refresh is in progress, cancel it too.


If the view is in a Replicated or Shared database, `STOP VIEW` only affects the current replica, while `STOP REPLICATED VIEW` affects all replicas.


NoteThe stopped state does not persist across server restarts. After a restart, views will resume their configured refresh schedules.
In Replicated or Shared databases, `SYSTEM STOP VIEW` only affects the current replica. Use `SYSTEM STOP REPLICATED VIEW` to stop refreshes on all replicas.



```
SYSTEM STOP VIEW [db.]name

```


```
SYSTEM STOP VIEWS

```

### SYSTEM START \[REPLICATED] VIEW, START VIEWS[​](#start-view-start-views "Direct link to SYSTEM START [REPLICATED] VIEW, START VIEWS")


Enable periodic refreshing for the given view or all refreshable views. No immediate refresh is triggered.


If the view is in a Replicated or Shared database, `START VIEW` undoes the effect of `STOP VIEW`, and `START REPLICATED VIEW` undoes the effect of `STOP REPLICATED VIEW`. `START VIEW` also undoes the effect of `PAUSE VIEW`.



```
SYSTEM START VIEW [db.]name

```


```
SYSTEM START VIEWS

```

### SYSTEM PAUSE VIEW, PAUSE VIEWS[​](#pause-view-pause-views "Direct link to SYSTEM PAUSE VIEW, PAUSE VIEWS")


Disable periodic refreshing of the given view or all refreshable views.
Unlike `SYSTEM STOP VIEW`, `SYSTEM PAUSE VIEW` does not interrupt a refresh that is already in progress: the running refresh is allowed to finish, and only subsequent refreshes are prevented.


Undo with `SYSTEM START VIEW` or `SYSTEM START VIEWS`.


NoteThe paused state does not persist across server restarts. After a restart, views will resume their configured refresh schedules.
In Replicated or Shared databases, `SYSTEM PAUSE VIEW` only affects the current replica.



```
SYSTEM PAUSE VIEW [db.]name

```


```
SYSTEM PAUSE VIEWS

```

### SYSTEM REFRESH VIEW[​](#refresh-view "Direct link to SYSTEM REFRESH VIEW")


Trigger an immediate out\-of\-schedule refresh of a given view.



```
SYSTEM REFRESH VIEW [db.]name

```

### SYSTEM WAIT VIEW[​](#wait-view "Direct link to SYSTEM WAIT VIEW")


Waits for the running refresh to complete. If no refresh is running, returns immediately. If the latest refresh attempt failed, reports an error.


Can be used right after creating a new refreshable materialized view (without EMPTY keyword) to wait for the initial refresh to complete.


If the view is in a Replicated or Shared database, and refresh is running on another replica, waits for that refresh to complete.



```
SYSTEM WAIT VIEW [db.]name

```

### SYSTEM CANCEL VIEW[​](#cancel-view "Direct link to SYSTEM CANCEL VIEW")


If there's a refresh in progress for the given view on the current replica, interrupt and cancel it. Otherwise do nothing.



```
SYSTEM CANCEL VIEW [db.]name

```

## SYSTEM FLUSH OBJECT STORAGE QUEUE[​](#flush-object-storage-queue "Direct link to SYSTEM FLUSH OBJECT STORAGE QUEUE")


Blocks until the given file has been processed or permanently failed by the given [S3Queue](/docs/engines/table-engines/integrations/s3queue) or [AzureQueue](/docs/engines/table-engines/integrations/azure-queue) table. Returns immediately if the file was already processed. Raises an error if the file has permanently failed (all retries exhausted).



```
SYSTEM FLUSH OBJECT STORAGE QUEUE [db.]table_name PATH 'path'

```
[PreviousDELETE](/docs/sql-reference/statements/delete)[NextSHOW](/docs/sql-reference/statements/show)- [SYSTEM RELOAD EMBEDDED DICTIONARIES](#reload-embedded-dictionaries)- [SYSTEM RELOAD DICTIONARIES](#reload-dictionaries)- [SYSTEM RELOAD DICTIONARY](#reload-dictionary)- [SYSTEM RELOAD MODELS](#reload-models)- [SYSTEM RELOAD MODEL](#reload-model)- [SYSTEM RELOAD FUNCTIONS](#reload-functions)- [SYSTEM RELOAD ASYNCHRONOUS METRICS](#reload-asynchronous-metrics)- [SYSTEM CLEAR\|DROP DNS CACHE](#drop-dns-cache)- [SYSTEM CLEAR\|DROP MARK CACHE](#drop-mark-cache)- [SYSTEM CLEAR\|DROP ICEBERG METADATA CACHE](#drop-iceberg-metadata-cache)- [SYSTEM CLEAR\|DROP AVRO SCHEMA CACHE](#drop-avro-schema-cache)- [SYSTEM DROP PARQUET METADATA CACHE](#drop-parquet-metadata-cache)- [SYSTEM CLEAR\|DROP TEXT INDEX CACHES](#drop-text-index-caches)- [SYSTEM DROP REPLICA](#drop-replica)- [SYSTEM DROP DATABASE REPLICA](#drop-database-replica)- [SYSTEM CLEAR\|DROP UNCOMPRESSED CACHE](#drop-uncompressed-cache)- [SYSTEM CLEAR\|DROP COMPILED EXPRESSION CACHE](#drop-compiled-expression-cache)- [SYSTEM CLEAR\|DROP QUERY CONDITION CACHE](#drop-query-condition-cache)- [SYSTEM CLEAR\|DROP QUERY CACHE](#drop-query-cache)- [SYSTEM CLEAR\|DROP FORMAT SCHEMA CACHE](#system-drop-schema-format)- [SYSTEM FLUSH LOGS](#flush-logs)- [SYSTEM RELOAD CONFIG](#reload-config)- [SYSTEM RELOAD USERS](#reload-users)- [SYSTEM SHUTDOWN](#shutdown)- [SYSTEM KILL](#kill)- [SYSTEM INSTRUMENT](#instrument)
	- [SYSTEM INSTRUMENT ADD](#instrument-add)- [SYSTEM INSTRUMENT REMOVE](#instrument-remove)- [Managing Distributed Tables](#managing-distributed-tables)
	- [SYSTEM STOP DISTRIBUTED SENDS](#stop-distributed-sends)- [SYSTEM FLUSH DISTRIBUTED](#flush-distributed)- [SYSTEM START DISTRIBUTED SENDS](#start-distributed-sends)- [SYSTEM STOP LISTEN](#stop-listen)- [SYSTEM START LISTEN](#start-listen)- [Managing MergeTree Tables](#managing-mergetree-tables)
	- [SYSTEM STOP MERGES](#stop-merges)- [SYSTEM START MERGES](#start-merges)- [SYSTEM STOP TTL MERGES](#stop-ttl-merges)- [SYSTEM START TTL MERGES](#start-ttl-merges)- [SYSTEM STOP MOVES](#stop-moves)- [SYSTEM START MOVES](#start-moves)- [SYSTEM SYSTEM UNFREEZE](#query_language-system-unfreeze)- [SYSTEM WAIT LOADING PARTS](#wait-loading-parts)- [Managing ReplicatedMergeTree Tables](#managing-replicatedmergetree-tables)
	- [SYSTEM STOP FETCHES](#stop-fetches)- [SYSTEM START FETCHES](#start-fetches)- [SYSTEM STOP REPLICATED SENDS](#stop-replicated-sends)- [SYSTEM START REPLICATED SENDS](#start-replicated-sends)- [SYSTEM STOP REPLICATION QUEUES](#stop-replication-queues)- [SYSTEM START REPLICATION QUEUES](#start-replication-queues)- [SYSTEM STOP PULLING REPLICATION LOG](#stop-pulling-replication-log)- [SYSTEM START PULLING REPLICATION LOG](#start-pulling-replication-log)- [SYSTEM SYNC REPLICA](#sync-replica)- [SYNC DATABASE REPLICA](#sync-database-replica)- [SYSTEM RESTART REPLICA](#restart-replica)- [SYSTEM RESTORE REPLICA](#restore-replica)- [SYSTEM RESTORE DATABASE REPLICA](#restore-database-replica)- [SYSTEM RESTART REPLICAS](#restart-replicas)- [SYSTEM CLEAR\|DROP FILESYSTEM CACHE](#drop-filesystem-cache)- [SYSTEM SYNC FILE CACHE](#sync-file-cache)- [SYSTEM LOAD PRIMARY KEY](#load-primary-key)- [SYSTEM UNLOAD PRIMARY KEY](#unload-primary-key)- [Managing Refreshable Materialized Views](#managing-refreshable-materialized-views)
	- [SYSTEM STOP \[REPLICATED] VIEW, STOP VIEWS](#stop-view-stop-views)- [SYSTEM START \[REPLICATED] VIEW, START VIEWS](#start-view-start-views)- [SYSTEM PAUSE VIEW, PAUSE VIEWS](#pause-view-pause-views)- [SYSTEM REFRESH VIEW](#refresh-view)- [SYSTEM WAIT VIEW](#wait-view)- [SYSTEM CANCEL VIEW](#cancel-view)- [SYSTEM FLUSH OBJECT STORAGE QUEUE](#flush-object-storage-queue)
Was this page helpful?
