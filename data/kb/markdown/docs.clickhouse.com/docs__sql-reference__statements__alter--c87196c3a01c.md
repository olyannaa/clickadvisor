# ALTER \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- ALTER
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/index.md)# ALTER

Most `ALTER TABLE` queries modify table settings or data:




| Modifier| [COLUMN](/docs/sql-reference/statements/alter/column)| [PARTITION](/docs/sql-reference/statements/alter/partition)| [DELETE](/docs/sql-reference/statements/alter/delete)| [UPDATE](/docs/sql-reference/statements/alter/update)| [ORDER BY](/docs/sql-reference/statements/alter/order-by)| [INDEX](/docs/sql-reference/statements/alter/skipping-index)| [CONSTRAINT](/docs/sql-reference/statements/alter/constraint)| [TTL](/docs/sql-reference/statements/alter/ttl)| [STATISTICS](/docs/sql-reference/statements/alter/statistics)| [APPLY DELETED MASK](/docs/sql-reference/statements/alter/apply-deleted-mask)| [APPLY PATCHES](/docs/sql-reference/statements/alter/apply-patches) | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


NoteMost `ALTER TABLE` queries are supported only for [\*MergeTree](/docs/engines/table-engines/mergetree-family), [Merge](/docs/engines/table-engines/special/merge) and [Distributed](/docs/engines/table-engines/special/distributed) tables.


These `ALTER` statements manipulate views:




| Statement Description| [ALTER TABLE ... MODIFY QUERY](/docs/sql-reference/statements/alter/view) Modifies a [Materialized view](/docs/sql-reference/statements/create/view) structure. | | | --- | --- | | |
| --- | --- | --- | --- |


These `ALTER` statements modify entities related to role\-based access control:




| Statement| [USER](/docs/sql-reference/statements/alter/user)| [ROLE](/docs/sql-reference/statements/alter/role)| [QUOTA](/docs/sql-reference/statements/alter/quota)| [ROW POLICY](/docs/sql-reference/statements/alter/row-policy)| [SETTINGS PROFILE](/docs/sql-reference/statements/alter/settings-profile) | | | | | | --- | --- | --- | --- | --- | |
| --- | --- | --- | --- | --- | --- |




| Statement Description| [ALTER TABLE ... MODIFY COMMENT](/docs/sql-reference/statements/alter/comment) Adds, modifies, or removes comments to the table, regardless if it was set before or not.| [ALTER NAMED COLLECTION](/docs/sql-reference/statements/alter/named-collection) Modifies [Named Collections](/docs/operations/named-collections). | | | | | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- |


## Mutations[​](#mutations "Direct link to Mutations")


`ALTER` queries that are intended to manipulate table data are implemented with a mechanism called "mutations", most notably [ALTER TABLE ... DELETE](/docs/sql-reference/statements/alter/delete) and [ALTER TABLE ... UPDATE](/docs/sql-reference/statements/alter/update). They are asynchronous background processes similar to merges in [MergeTree](/docs/engines/table-engines/mergetree-family) tables that to produce new "mutated" versions of parts.


For `*MergeTree` tables mutations execute by **rewriting whole data parts**.
There is no atomicity — parts are substituted for mutated parts as soon as they are ready and a `SELECT` query that started executing during a mutation will see data from parts that have already been mutated along with data from parts that have not been mutated yet.


Mutations are totally ordered by their creation order and are applied to each part in that order. Mutations are also partially ordered with `INSERT INTO` queries: data that was inserted into the table before the mutation was submitted will be mutated and data that was inserted after that will not be mutated. Note that mutations do not block inserts in any way.


A mutation query returns immediately after the mutation entry is added (in case of replicated tables to ZooKeeper, for non\-replicated tables \- to the filesystem). The mutation itself executes asynchronously using the system profile settings. To track the progress of mutations you can use the [`system.mutations`](/docs/operations/system-tables/mutations) table. A mutation that was successfully submitted will continue to execute even if ClickHouse servers are restarted. There is no way to roll back the mutation once it is submitted, but if the mutation is stuck for some reason it can be cancelled with the [`KILL MUTATION`](/docs/sql-reference/statements/kill#kill-mutation) query.


Entries for finished mutations are not deleted right away (the number of preserved entries is determined by the `finished_mutations_to_keep` storage engine parameter). Older mutation entries are deleted.


## Synchronicity of ALTER Queries[​](#synchronicity-of-alter-queries "Direct link to Synchronicity of ALTER Queries")


For non\-replicated tables, all `ALTER` queries are performed synchronously. For replicated tables, the query just adds instructions for the appropriate actions to `ZooKeeper`, and the actions themselves are performed as soon as possible. However, the query can wait for these actions to be completed on all the replicas.


For `ALTER` queries that creates mutations (e.g.: including, but not limited to `UPDATE`, `DELETE`, `MATERIALIZE INDEX`, `MATERIALIZE PROJECTION`, `MATERIALIZE COLUMN`, `APPLY DELETED MASK`, `APPLY PATCHES`, `CLEAR STATISTIC`, `MATERIALIZE STATISTIC`) the synchronicity is defined by the [mutations\_sync](/docs/operations/settings/settings#mutations_sync) setting.


For other `ALTER` queries which only modify the metadata, you can use the [alter\_sync](/docs/operations/settings/settings#alter_sync) setting to set up waiting.


You can specify how long (in seconds) to wait for inactive replicas to execute all `ALTER` queries with the [replication\_wait\_for\_inactive\_replica\_timeout](/docs/operations/settings/settings#replication_wait_for_inactive_replica_timeout) setting.


NoteFor all `ALTER` queries, if `alter_sync = 2` and some replicas are not active for more than the time, specified in the `replication_wait_for_inactive_replica_timeout` setting, then an exception `UNFINISHED` is thrown.


## Related content[​](#related-content "Direct link to Related content")


- Blog: [Handling Updates and Deletes in ClickHouse](https://clickhouse.com/blog/handling-updates-and-deletes-in-clickhouse)
[PreviousNAMED COLLECTION](/docs/sql-reference/statements/create/named-collection)[NextCOLUMN](/docs/sql-reference/statements/alter/column)- [Mutations](#mutations)- [Synchronicity of ALTER Queries](#synchronicity-of-alter-queries)- [Related content](#related-content)
Was this page helpful?
