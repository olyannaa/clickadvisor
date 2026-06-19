# MergeTree tables settings \| ClickHouse Docs


- - [Settings](/docs/operations/settings)- MergeTree tables settings
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/operations/settings/merge-tree-settings.md)# MergeTree tables settings

System table `system.merge_tree_settings` shows the globally set MergeTree settings.


MergeTree settings can be set in the `merge_tree` section of the server config file, or specified for each `MergeTree` table individually in
the `SETTINGS` clause of the `CREATE TABLE` statement.


Example for customizing setting `max_suspicious_broken_parts`:


Configure the default for all `MergeTree` tables in the server configuration file:



```
<merge_tree>
    <max_suspicious_broken_parts>5</max_suspicious_broken_parts>
</merge_tree>

```

Set for a particular table:



```
CREATE TABLE tab
(
    `A` Int64
)
ENGINE = MergeTree
ORDER BY tuple()
SETTINGS max_suspicious_broken_parts = 500;

```

Change the settings for a particular table using `ALTER TABLE ... MODIFY SETTING`:



```
ALTER TABLE tab MODIFY SETTING max_suspicious_broken_parts = 100;

-- reset to global default (value from system.merge_tree_settings)
ALTER TABLE tab RESET SETTING max_suspicious_broken_parts;

```

## MergeTree settings[​](#mergetree-settings "Direct link to MergeTree settings")


## adaptive\_write\_buffer\_initial\_size[​](#adaptive_write_buffer_initial_size "Direct link to adaptive_write_buffer_initial_size")



Initial size of an adaptive write buffer


## add\_implicit\_sign\_column\_constraint\_for\_collapsing\_engine[​](#add_implicit_sign_column_constraint_for_collapsing_engine "Direct link to add_implicit_sign_column_constraint_for_collapsing_engine")



If true, adds an implicit constraint for the `sign` column of a CollapsingMergeTree
or VersionedCollapsingMergeTree table to allow only valid values (`1` and `-1`).


## add\_minmax\_index\_for\_block\_number\_column[​](#add_minmax_index_for_block_number_column "Direct link to add_minmax_index_for_block_number_column")




When enabled, an implicit min\-max (skipping) index is added for the persistent virtual column `_block_number`.
Requires `enable_block_number_column = 1` to take effect. The index is built only during merges,
not during inserts: at insert time the block number is provisional and would index a constant.


## add\_minmax\_index\_for\_block\_offset\_column[​](#add_minmax_index_for_block_offset_column "Direct link to add_minmax_index_for_block_offset_column")




When enabled, an implicit min\-max (skipping) index is added for the persistent virtual column `_block_offset`.
Requires `enable_block_offset_column = 1` to take effect. The index is built only during merges,
not during inserts.


## add\_minmax\_index\_for\_numeric\_columns[​](#add_minmax_index_for_numeric_columns "Direct link to add_minmax_index_for_numeric_columns")




When enabled, min\-max (skipping) indices are added for all numeric columns
of the table.


## add\_minmax\_index\_for\_string\_columns[​](#add_minmax_index_for_string_columns "Direct link to add_minmax_index_for_string_columns")




When enabled, min\-max (skipping) indices are added for all string columns of the table.


## add\_minmax\_index\_for\_temporal\_columns[​](#add_minmax_index_for_temporal_columns "Direct link to add_minmax_index_for_temporal_columns")




When enabled, min\-max (skipping) indices are added for all Date, Date32, Time, Time64, DateTime and DateTime64 columns of the table


## allow\_coalescing\_columns\_in\_partition\_or\_order\_key[​](#allow_coalescing_columns_in_partition_or_order_key "Direct link to allow_coalescing_columns_in_partition_or_order_key")




When enabled, allows coalescing columns in a CoalescingMergeTree table to be used in
the partition or sorting key.


## allow\_commit\_order\_projection[​](#allow_commit_order_projection "Direct link to allow_commit_order_projection")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Enables commit\-order projections that store `_block_number` and `_block_offset` virtual columns, preserving original insertion order through merges.
Requires `enable_block_number_column` and `enable_block_offset_column` to be enabled.


## allow\_experimental\_replacing\_merge\_with\_cleanup[​](#allow_experimental_replacing_merge_with_cleanup "Direct link to allow_experimental_replacing_merge_with_cleanup")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Allow experimental CLEANUP merges for ReplacingMergeTree with `is_deleted`
column. When enabled, allows using `OPTIMIZE ... FINAL CLEANUP` to manually
merge all parts in a partition down to a single part and removing any
deleted rows.


Also allows enabling such merges to happen automatically in the background
with settings `min_age_to_force_merge_seconds`,
`min_age_to_force_merge_on_partition_only` and
`enable_replacing_merge_with_cleanup_for_min_age_to_force_merge`.


## allow\_experimental\_reverse\_key[​](#allow_experimental_reverse_key "Direct link to allow_experimental_reverse_key")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Enables support for descending sort order in MergeTree sorting keys. This
setting is particularly useful for time series analysis and Top\-N queries,
allowing data to be stored in reverse chronological order to optimize query
performance.


With `allow_experimental_reverse_key` enabled, you can define descending sort
orders within the `ORDER BY` clause of a MergeTree table. This enables the
use of more efficient `ReadInOrder` optimizations instead of `ReadInReverseOrder`
for descending queries.


**Example**



```
CREATE TABLE example
(
time DateTime,
key Int32,
value String
) ENGINE = MergeTree
ORDER BY (time DESC, key)  -- Descending order on 'time' field
SETTINGS allow_experimental_reverse_key = 1;

SELECT * FROM example WHERE key = 'xxx' ORDER BY time DESC LIMIT 10;

```

By using `ORDER BY time DESC` in the query, `ReadInOrder` is applied.


**Default Value:** false


## allow\_floating\_point\_partition\_key[​](#allow_floating_point_partition_key "Direct link to allow_floating_point_partition_key")



Enables to allow floating\-point number as a partition key.


Possible values:


- `0` — Floating\-point partition key not allowed.
- `1` — Floating\-point partition key allowed.


## allow\_nullable\_key[​](#allow_nullable_key "Direct link to allow_nullable_key")



Allow Nullable types as primary keys.


## allow\_part\_offset\_column\_in\_projections[​](#allow_part_offset_column_in_projections "Direct link to allow_part_offset_column_in_projections")




Allow usage of '\_part\_offset' column in projections select query.


## allow\_reduce\_blocking\_parts\_task[​](#allow_reduce_blocking_parts_task "Direct link to allow_reduce_blocking_parts_task")




Background task which reduces blocking parts for shared merge tree tables.
Only in ClickHouse Cloud


## allow\_remote\_fs\_zero\_copy\_replication[​](#allow_remote_fs_zero_copy_replication "Direct link to allow_remote_fs_zero_copy_replication")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Don't use this setting in production, because it is not ready.


## allow\_summing\_columns\_in\_partition\_or\_order\_key[​](#allow_summing_columns_in_partition_or_order_key "Direct link to allow_summing_columns_in_partition_or_order_key")




When enabled, allows summing columns in a SummingMergeTree table to be used in
the partition or sorting key.


## allow\_suspicious\_indices[​](#allow_suspicious_indices "Direct link to allow_suspicious_indices")



Reject primary/secondary indexes and sorting keys with identical expressions


## allow\_vertical\_merges\_from\_compact\_to\_wide\_parts[​](#allow_vertical_merges_from_compact_to_wide_parts "Direct link to allow_vertical_merges_from_compact_to_wide_parts")



Allows vertical merges from compact to wide parts. This settings must have
the same value on all replicas.


## alter\_column\_secondary\_index\_mode[​](#alter_column_secondary_index_mode "Direct link to alter_column_secondary_index_mode")




Configures whether to allow `ALTER` commands that modify columns covered by secondary indices, and what action to take if
they are allowed. By default, such `ALTER` commands are allowed and the indices are rebuilt.


Possible values:


- `rebuild` (default): Rebuilds any secondary indices affected by the column in the `ALTER` command.
- `throw`: Prevents any `ALTER` of columns covered by **explicit** secondary indices by throwing an exception. Implicit indices are excluded from this restriction and will be rebuilt.
- `drop`: Drop the dependent secondary indices. The new parts won't have the indices, requiring `MATERIALIZE INDEX` to recreate them.
- `compatibility`: Matches the original behaviour: `throw` on `ALTER ... MODIFY COLUMN` and `rebuild` on `ALTER ... UPDATE/DELETE`.
- `ignore`: Intended for expert usage. It will leave the indices in an inconsistent state, allowing incorrect query results.


## always\_fetch\_merged\_part[​](#always_fetch_merged_part "Direct link to always_fetch_merged_part")



If true, this replica never merges parts and always downloads merged parts
from other replicas.


Possible values:


- true, false


## always\_use\_copy\_instead\_of\_hardlinks[​](#always_use_copy_instead_of_hardlinks "Direct link to always_use_copy_instead_of_hardlinks")



Always copy data instead of hardlinking during mutations/replaces/detaches
and so on.


## apply\_patches\_on\_merge[​](#apply_patches_on_merge "Direct link to apply_patches_on_merge")




If true patch parts are applied on merges


## assign\_part\_uuids[​](#assign_part_uuids "Direct link to assign_part_uuids")



When enabled, a unique part identifier will be assigned for every new part.
Before enabling, check that all replicas support UUID version 4\.


## async\_block\_ids\_cache\_update\_wait\_ms[​](#async_block_ids_cache_update_wait_ms "Direct link to async_block_ids_cache_update_wait_ms")



How long each insert iteration will wait for async\_block\_ids\_cache update


## async\_insert[​](#async_insert "Direct link to async_insert")



If true, data from INSERT query is stored in queue and later flushed to
table in background.


## auto\_statistics\_types[​](#auto_statistics_types "Direct link to auto_statistics_types")




Comma\-separated list of statistics types to calculate automatically on all suitable columns.
Supported statistics types: tdigest, countmin, minmax, uniq.


## background\_task\_preferred\_step\_execution\_time\_ms[​](#background_task_preferred_step_execution_time_ms "Direct link to background_task_preferred_step_execution_time_ms")



Target time to execution of one step of merge or mutation. Can be exceeded if
one step takes longer time


## cache\_populated\_by\_fetch[​](#cache_populated_by_fetch "Direct link to cache_populated_by_fetch")



NoteThis setting applies only to ClickHouse Cloud.


When `cache_populated_by_fetch` is disabled (the default setting), new data
parts are loaded into the filesystem cache only when a query is run that requires
those parts.


If enabled, `cache_populated_by_fetch` will instead cause all nodes to load
new data parts from storage into their filesystem cache without requiring a query
to trigger such an action.


**See Also**


- [ignore\_cold\_parts\_seconds](/docs/operations/settings/settings#ignore_cold_parts_seconds)
- [prefer\_warmed\_unmerged\_parts\_seconds](/docs/operations/settings/settings#prefer_warmed_unmerged_parts_seconds)
- [cache\_warmer\_threads](/docs/operations/settings/settings#cache_warmer_threads)


## cache\_populated\_by\_fetch\_filename\_regexp[​](#cache_populated_by_fetch_filename_regexp "Direct link to cache_populated_by_fetch_filename_regexp")



NoteThis setting applies only to ClickHouse Cloud.


If not empty, only files that match this regex will be prewarmed into the cache after fetch (if `cache_populated_by_fetch` is enabled).


## check\_delay\_period[​](#check_delay_period "Direct link to check_delay_period")



Obsolete setting, does nothing.


## check\_sample\_column\_is\_correct[​](#check_sample_column_is_correct "Direct link to check_sample_column_is_correct")



Enables the check at table creation, that the data type of a column for s
ampling or sampling expression is correct. The data type must be one of unsigned
[integer types](/docs/sql-reference/data-types/int-uint): `UInt8`, `UInt16`,
`UInt32`, `UInt64`.


Possible values:


- `true` — The check is enabled.
- `false` — The check is disabled at table creation.


Default value: `true`.


By default, the ClickHouse server checks at table creation the data type of
a column for sampling or sampling expression. If you already have tables with
incorrect sampling expression and do not want the server to raise an exception
during startup, set `check_sample_column_is_correct` to `false`.


## clean\_deleted\_rows[​](#clean_deleted_rows "Direct link to clean_deleted_rows")



Obsolete setting, does nothing.


## cleanup\_delay\_period[​](#cleanup_delay_period "Direct link to cleanup_delay_period")



Minimum period to clean old queue logs, blocks hashes and parts.


## cleanup\_delay\_period\_random\_add[​](#cleanup_delay_period_random_add "Direct link to cleanup_delay_period_random_add")



Add uniformly distributed value from 0 to x seconds to cleanup\_delay\_period
to avoid thundering herd effect and subsequent DoS of ZooKeeper in case of
very large number of tables.


## cleanup\_thread\_preferred\_points\_per\_iteration[​](#cleanup_thread_preferred_points_per_iteration "Direct link to cleanup_thread_preferred_points_per_iteration")



Preferred batch size for background cleanup (points are abstract but 1 point
is approximately equivalent to 1 inserted block).


## cleanup\_threads[​](#cleanup_threads "Direct link to cleanup_threads")



Obsolete setting, does nothing.


## clone\_replica\_zookeeper\_create\_get\_part\_batch\_size[​](#clone_replica_zookeeper_create_get_part_batch_size "Direct link to clone_replica_zookeeper_create_get_part_batch_size")




Batch size for ZooKeeper multi\-create get\-part requests when cloning replica.


## columns\_and\_secondary\_indices\_sizes\_lazy\_calculation[​](#columns_and_secondary_indices_sizes_lazy_calculation "Direct link to columns_and_secondary_indices_sizes_lazy_calculation")




Calculate columns and secondary indices sizes lazily on first request instead
of on table initialization.


## columns\_to\_prewarm\_mark\_cache[​](#columns_to_prewarm_mark_cache "Direct link to columns_to_prewarm_mark_cache")


List of columns to prewarm mark cache for (if enabled). Empty means all columns


## compact\_parts\_max\_bytes\_to\_buffer[​](#compact_parts_max_bytes_to_buffer "Direct link to compact_parts_max_bytes_to_buffer")



Only available in ClickHouse Cloud. Maximal number of bytes to write in a
single stripe in compact parts


## compact\_parts\_max\_granules\_to\_buffer[​](#compact_parts_max_granules_to_buffer "Direct link to compact_parts_max_granules_to_buffer")



Only available in ClickHouse Cloud. Maximal number of granules to write in a
single stripe in compact parts


## compact\_parts\_merge\_max\_bytes\_to\_prefetch\_part[​](#compact_parts_merge_max_bytes_to_prefetch_part "Direct link to compact_parts_merge_max_bytes_to_prefetch_part")



Only available in ClickHouse Cloud. Maximal size of compact part to read it
in a whole to memory during merge.


## compatibility\_allow\_sampling\_expression\_not\_in\_primary\_key[​](#compatibility_allow_sampling_expression_not_in_primary_key "Direct link to compatibility_allow_sampling_expression_not_in_primary_key")



Allow to create a table with sampling expression not in primary key. This is
needed only to temporarily allow to run the server with wrong tables for
backward compatibility.


## compress\_marks[​](#compress_marks "Direct link to compress_marks")



Marks support compression, reduce mark file size and speed up network
transmission.


## compress\_per\_column\_in\_compact\_parts[​](#compress_per_column_in_compact_parts "Direct link to compress_per_column_in_compact_parts")




Controls the physical layout of Compact parts. If true (default), each column in a granule
starts a new compressed block, allowing ClickHouse to skip reading unnecessary columns
from disk. If false, all columns within a granule are packed into the same compressed block,
improving compression ratio but requiring more data to be decompressed during reads.
This is beneficial for workloads that always read all columns (e.g. projections).


## compress\_primary\_key[​](#compress_primary_key "Direct link to compress_primary_key")



Primary key support compression, reduce primary key file size and speed up
network transmission.


## concurrent\_part\_removal\_threshold[​](#concurrent_part_removal_threshold "Direct link to concurrent_part_removal_threshold")



Activate concurrent part removal (see 'max\_part\_removal\_threads') only if
the number of inactive data parts is at least this.


## concurrent\_part\_removal\_threshold\_for\_remote\_disk[​](#concurrent_part_removal_threshold_for_remote_disk "Direct link to concurrent_part_removal_threshold_for_remote_disk")




Same as `concurrent_part_removal_threshold`, but used when at least one
part being removed is stored on a remote disk. The default is lower
because each part removal on remote storage typically requires a network
round\-trip (e.g. one HTTP `DELETE` per part on object storage), so a
serial removal of even 100 parts can stall a `DROP TABLE` for tens of
seconds.


## deduplicate\_merge\_projection\_mode[​](#deduplicate_merge_projection_mode "Direct link to deduplicate_merge_projection_mode")




Whether to allow create projection for the table with non\-classic MergeTree,
that is not (Replicated, Shared) MergeTree. Ignore option is purely for
compatibility which might result in incorrect answer. Otherwise, if allowed,
what is the action when merge projections, either drop or rebuild. So classic
MergeTree would ignore this setting. It also controls `OPTIMIZE DEDUPLICATE`
as well, but has effect on all MergeTree family members. Similar to the
option `lightweight_mutation_projection_mode`, it is also part level.


Possible values:


- `ignore`
- `throw`
- `drop`
- `rebuild`


## default\_compression\_codec[​](#default_compression_codec "Direct link to default_compression_codec")



Specifies the default compression codec to be used if none is defined for a particular column in the table declaration.
Compression codec selecting order for a column:


1. Compression codec defined for the column in the table declaration
2. Compression codec defined in `default_compression_codec` (this setting)
3. Default compression codec defined in `compression` settings
Default value: an empty string (not defined).


## detach\_not\_byte\_identical\_parts[​](#detach_not_byte_identical_parts "Direct link to detach_not_byte_identical_parts")



Enables or disables detaching a data part on a replica after a merge or a
mutation, if it is not byte\-identical to data parts on other replicas. If
disabled, the data part is removed. Activate this setting if you want to
analyze such parts later.


The setting is applicable to `MergeTree` tables with enabled
[data replication](/docs/engines/table-engines/mergetree-family/replacingmergetree).


Possible values:


- `0` — Parts are removed.
- `1` — Parts are detached.


## detach\_old\_local\_parts\_when\_cloning\_replica[​](#detach_old_local_parts_when_cloning_replica "Direct link to detach_old_local_parts_when_cloning_replica")



Do not remove old local parts when repairing lost replica.


Possible values:


- `true`
- `false`


## disable\_detach\_partition\_for\_zero\_copy\_replication[​](#disable_detach_partition_for_zero_copy_replication "Direct link to disable_detach_partition_for_zero_copy_replication")



Disable DETACH PARTITION query for zero copy replication.


## disable\_fetch\_partition\_for\_zero\_copy\_replication[​](#disable_fetch_partition_for_zero_copy_replication "Direct link to disable_fetch_partition_for_zero_copy_replication")



Disable FETCH PARTITION query for zero copy replication.


## disable\_freeze\_partition\_for\_zero\_copy\_replication[​](#disable_freeze_partition_for_zero_copy_replication "Direct link to disable_freeze_partition_for_zero_copy_replication")



Disable FREEZE PARTITION query for zero copy replication.


## disk[​](#disk "Direct link to disk")


Name of storage disk. Can be specified instead of storage policy.


## distributed\_index\_analysis\_min\_indexes\_bytes\_to\_activate[​](#distributed_index_analysis_min_indexes_bytes_to_activate "Direct link to distributed_index_analysis_min_indexes_bytes_to_activate")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Minimal index sizes (data skipping and primary key) on disk (but uncompressed) to activated distributed index analysis


## distributed\_index\_analysis\_min\_parts\_to\_activate[​](#distributed_index_analysis_min_parts_to_activate "Direct link to distributed_index_analysis_min_parts_to_activate")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Minimal number of parts to activated distributed index analysis


## dynamic\_serialization\_version[​](#dynamic_serialization_version "Direct link to dynamic_serialization_version")




Serialization version for Dynamic data type. Required for compatibility.


Possible values:


- `v1`
- `v2`
- `v3`


## enable\_block\_number\_column[​](#enable_block_number_column "Direct link to enable_block_number_column")



Enable persisting column \_block\_number for each row.


## enable\_block\_offset\_column[​](#enable_block_offset_column "Direct link to enable_block_offset_column")



Persists virtual column `_block_offset` on merges.


## enable\_index\_granularity\_compression[​](#enable_index_granularity_compression "Direct link to enable_index_granularity_compression")



Compress in memory values of index granularity if it is possible


## enable\_max\_bytes\_limit\_for\_min\_age\_to\_force\_merge[​](#enable_max_bytes_limit_for_min_age_to_force_merge "Direct link to enable_max_bytes_limit_for_min_age_to_force_merge")




If settings `min_age_to_force_merge_seconds` and
`min_age_to_force_merge_on_partition_only` should respect setting
`max_bytes_to_merge_at_max_space_in_pool`.


Possible values:


- `true`
- `false`


## enable\_mixed\_granularity\_parts[​](#enable_mixed_granularity_parts "Direct link to enable_mixed_granularity_parts")



Enables or disables transitioning to control the granule size with the
`index_granularity_bytes` setting. Before version 19\.11, there was only the
`index_granularity` setting for restricting granule size. The
`index_granularity_bytes` setting improves ClickHouse performance when
selecting data from tables with big rows (tens and hundreds of megabytes).
If you have tables with big rows, you can enable this setting for the tables
to improve the efficiency of `SELECT` queries.


## enable\_replacing\_merge\_with\_cleanup\_for\_min\_age\_to\_force\_merge[​](#enable_replacing_merge_with_cleanup_for_min_age_to_force_merge "Direct link to enable_replacing_merge_with_cleanup_for_min_age_to_force_merge")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Whether to use CLEANUP merges for ReplacingMergeTree when merging partitions
down to a single part. Requires `allow_experimental_replacing_merge_with_cleanup`,
`min_age_to_force_merge_seconds` and `min_age_to_force_merge_on_partition_only`
to be enabled.


Possible values:


- `true`
- `false`


## enable\_the\_endpoint\_id\_with\_zookeeper\_name\_prefix[​](#enable_the_endpoint_id_with_zookeeper_name_prefix "Direct link to enable_the_endpoint_id_with_zookeeper_name_prefix")



Enable the endpoint id with zookeeper name prefix for the replicated merge
tree table.


## enable\_vertical\_merge\_algorithm[​](#enable_vertical_merge_algorithm "Direct link to enable_vertical_merge_algorithm")



Enable usage of Vertical merge algorithm.


## enforce\_index\_structure\_match\_on\_partition\_manipulation[​](#enforce_index_structure_match_on_partition_manipulation "Direct link to enforce_index_structure_match_on_partition_manipulation")




If this setting is enabled for destination table of a partition manipulation
query (`ATTACH/MOVE/REPLACE PARTITION`), the indices and projections must be
identical between the source and destination tables. Otherwise, the destination
table can have a superset of the source table's indices and projections.


## escape\_index\_filenames[​](#escape_index_filenames "Direct link to escape_index_filenames")




Prior to 26\.1 we didn't escape special symbols in filenames created for secondary indices, which could lead to issues with some
characters in index names producing broken parts. This is added purely for compatibility reasons. It should not be changed unless you
are reading old parts with indices using non\-ascii characters in their names.


## escape\_variant\_subcolumn\_filenames[​](#escape_variant_subcolumn_filenames "Direct link to escape_variant_subcolumn_filenames")




Escape special symbols in filenames created for subcolumns of Variant data type in Wide parts of MergeTree table. Needed for compatibility.


## exclude\_deleted\_rows\_for\_part\_size\_in\_merge[​](#exclude_deleted_rows_for_part_size_in_merge "Direct link to exclude_deleted_rows_for_part_size_in_merge")



If enabled, estimated actual size of data parts (i.e., excluding those rows
that have been deleted through `DELETE FROM`) will be used when selecting
parts to merge. Note that this behavior is only triggered for data parts
affected by `DELETE FROM` executed after this setting is enabled.


Possible values:


- `true`
- `false`


**See Also**


- [load\_existing\_rows\_count\_for\_old\_parts](#load_existing_rows_count_for_old_parts)
setting


## exclude\_materialize\_skip\_indexes\_on\_merge[​](#exclude_materialize_skip_indexes_on_merge "Direct link to exclude_materialize_skip_indexes_on_merge")



Excludes provided comma delimited list of skip indexes from being built and stored during merges. Has no effect if
[materialize\_skip\_indexes\_on\_merge](#materialize_skip_indexes_on_merge) is false.


The excluded skip indexes will still be built and stored by an explicit
[MATERIALIZE INDEX](/docs/sql-reference/statements/alter/skipping-index#materialize-index) query or during INSERTs depending on
the [materialize\_skip\_indexes\_on\_insert](/docs/operations/settings/settings#materialize_skip_indexes_on_insert)
session setting.


Example:



```
CREATE TABLE tab
(
a UInt64,
b UInt64,
INDEX idx_a a TYPE minmax,
INDEX idx_b b TYPE set(3)
)
ENGINE = MergeTree ORDER BY tuple() SETTINGS exclude_materialize_skip_indexes_on_merge = 'idx_a';

INSERT INTO tab SELECT number, number / 50 FROM numbers(100); -- setting has no effect on INSERTs

-- idx_a will be excluded from update during background or explicit merge via OPTIMIZE TABLE FINAL

-- can exclude multiple indexes by providing a list
ALTER TABLE tab MODIFY SETTING exclude_materialize_skip_indexes_on_merge = 'idx_a, idx_b';

-- default setting, no indexes excluded from being updated during merge
ALTER TABLE tab MODIFY SETTING exclude_materialize_skip_indexes_on_merge = '';

```

## execute\_merges\_on\_single\_replica\_time\_threshold[​](#execute_merges_on_single_replica_time_threshold "Direct link to execute_merges_on_single_replica_time_threshold")



When this setting has a value greater than zero, only a single replica starts
the merge immediately, and other replicas wait up to that amount of time to
download the result instead of doing merges locally. If the chosen replica
doesn't finish the merge during that amount of time, fallback to standard
behavior happens.


Possible values:


- Any positive integer.


## fault\_probability\_after\_part\_commit[​](#fault_probability_after_part_commit "Direct link to fault_probability_after_part_commit")



For testing. Do not change it.


## fault\_probability\_before\_part\_commit[​](#fault_probability_before_part_commit "Direct link to fault_probability_before_part_commit")



For testing. Do not change it.


## finished\_mutations\_to\_keep[​](#finished_mutations_to_keep "Direct link to finished_mutations_to_keep")



How many records about mutations that are done to keep. If zero, then keep
all of them.


## force\_read\_through\_cache\_for\_merges[​](#force_read_through_cache_for_merges "Direct link to force_read_through_cache_for_merges")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Force read\-through filesystem cache for merges


## fsync\_after\_insert[​](#fsync_after_insert "Direct link to fsync_after_insert")



Do fsync for every inserted part. Significantly decreases performance of
inserts, not recommended to use with wide parts.


## fsync\_part\_directory[​](#fsync_part_directory "Direct link to fsync_part_directory")



Do fsync for part directory after all part operations (writes, renames, etc.).


## in\_memory\_parts\_enable\_wal[​](#in_memory_parts_enable_wal "Direct link to in_memory_parts_enable_wal")



Obsolete setting, does nothing.


## in\_memory\_parts\_insert\_sync[​](#in_memory_parts_insert_sync "Direct link to in_memory_parts_insert_sync")



Obsolete setting, does nothing.


## inactive\_parts\_to\_delay\_insert[​](#inactive_parts_to_delay_insert "Direct link to inactive_parts_to_delay_insert")



If the number of inactive parts in a single partition in the table exceeds
the `inactive_parts_to_delay_insert` value, an `INSERT` is artificially
slowed down.


TipIt is useful when a server fails to clean up parts quickly enough.


Possible values:


- Any positive integer.


## inactive\_parts\_to\_throw\_insert[​](#inactive_parts_to_throw_insert "Direct link to inactive_parts_to_throw_insert")



If the number of inactive parts in a single partition more than the
`inactive_parts_to_throw_insert` value, `INSERT` is interrupted with the
following error:



> "Too many inactive parts (N). Parts cleaning are processing significantly
> slower than inserts" exception."


Possible values:


- Any positive integer.


## index\_granularity[​](#index_granularity "Direct link to index_granularity")



Maximum number of data rows between the marks of an index. I.e how many rows
correspond to one primary key value.


## index\_granularity\_bytes[​](#index_granularity_bytes "Direct link to index_granularity_bytes")



Maximum size of data granules in bytes.


To restrict the granule size only by number of rows, set to `0` (not recommended).


## initialization\_retry\_period[​](#initialization_retry_period "Direct link to initialization_retry_period")



Retry period for table initialization, in seconds.


## kill\_delay\_period[​](#kill_delay_period "Direct link to kill_delay_period")



Obsolete setting, does nothing.


## kill\_delay\_period\_random\_add[​](#kill_delay_period_random_add "Direct link to kill_delay_period_random_add")



Obsolete setting, does nothing.


## kill\_threads[​](#kill_threads "Direct link to kill_threads")



Obsolete setting, does nothing.


## lightweight\_mutation\_projection\_mode[​](#lightweight_mutation_projection_mode "Direct link to lightweight_mutation_projection_mode")



By default, lightweight delete `DELETE` does not work for tables with
projections. This is because rows in a projection may be affected by a
`DELETE` operation. So the default value would be `throw`. However, this
option can change the behavior. With the value either `drop` or `rebuild`,
deletes will work with projections. `drop` would delete the projection so it
might be fast in the current query as projection gets deleted but slow in
future queries as no projection attached. `rebuild` would rebuild the
projection which might affect the performance of the current query, but
might speedup for future queries. A good thing is that these options would
only work in the part level, which means projections in the part that don't
get touched would stay intact instead of triggering any action like
drop or rebuild.


Possible values:


- `throw`
- `drop`
- `rebuild`


## load\_existing\_rows\_count\_for\_old\_parts[​](#load_existing_rows_count_for_old_parts "Direct link to load_existing_rows_count_for_old_parts")



If enabled along with [exclude\_deleted\_rows\_for\_part\_size\_in\_merge](#exclude_deleted_rows_for_part_size_in_merge),
deleted rows count for existing data parts will be calculated during table
starting up. Note that it may slow down start up table loading.


Possible values:


- `true`
- `false`


**See Also**


- [exclude\_deleted\_rows\_for\_part\_size\_in\_merge](#exclude_deleted_rows_for_part_size_in_merge) setting


## lock\_acquire\_timeout\_for\_background\_operations[​](#lock_acquire_timeout_for_background_operations "Direct link to lock_acquire_timeout_for_background_operations")



For background operations like merges, mutations etc. How many seconds before
failing to acquire table locks.


## map\_buckets\_coefficient[​](#map_buckets_coefficient "Direct link to map_buckets_coefficient")




The coefficient used in `sqrt` and `linear` [map\_buckets\_strategy](#map_buckets_strategy) to calculate the number of buckets from the average map size.
For `sqrt` strategy: `round(map_buckets_coefficient * sqrt(avg_map_size))`.
For `linear` strategy: `round(map_buckets_coefficient * avg_map_size)`.
Ignored when `map_buckets_strategy` is `constant`.


## map\_buckets\_min\_avg\_size[​](#map_buckets_min_avg_size "Direct link to map_buckets_min_avg_size")




The minimum average map size (number of keys per row) required to apply `with_buckets` serialization.
If the average map size is less than this value, a single bucket is used regardless of other bucket settings.
A value of `0` disables the threshold and always applies the bucketing strategy.
This setting is useful to avoid the overhead of bucketed serialization for small maps where the benefit is negligible.


## map\_buckets\_strategy[​](#map_buckets_strategy "Direct link to map_buckets_strategy")




Controls the strategy for choosing the number of buckets in `with_buckets` `Map` serialization based on the average map size.


Possible values:


- constant — Always use [max\_buckets\_in\_map](#max_buckets_in_map) as the number of buckets, regardless of the average map size.
- sqrt — Use `round(map_buckets_coefficient * sqrt(avg_map_size))` as the number of buckets, clamped to `[1, max_buckets_in_map]`.
- linear — Use `round(map_buckets_coefficient * avg_map_size)` as the number of buckets, clamped to `[1, max_buckets_in_map]`.


## map\_serialization\_version[​](#map_serialization_version "Direct link to map_serialization_version")




Controls the serialization method used for `Map` columns.


Possible values:


- basic — Use the standard serialization for `Map`.
- with\_buckets — Split keys into buckets during serialization. Using buckets improves reading individual keys from the Map.


The number of buckets in `with_buckets` serialization is determined by [max\_buckets\_in\_map](#max_buckets_in_map) and [map\_buckets\_strategy](#map_buckets_strategy).


## map\_serialization\_version\_for\_zero\_level\_parts[​](#map_serialization_version_for_zero_level_parts "Direct link to map_serialization_version_for_zero_level_parts")




This setting allows to specify a different serialization version of
`Map` columns for zero level parts that are created during inserts.
It can be useful to keep `basic` serialization for zero level parts to avoid
performance degradation during inserts, while using `with_buckets` for merged parts.


## marks\_compress\_block\_size[​](#marks_compress_block_size "Direct link to marks_compress_block_size")



Mark compress block size, the actual size of the block to compress.


## marks\_compression\_codec[​](#marks_compression_codec "Direct link to marks_compression_codec")



Compression encoding used by marks, marks are small enough and cached, so
the default compression is ZSTD(3\).


## materialize\_skip\_indexes\_on\_merge[​](#materialize_skip_indexes_on_merge "Direct link to materialize_skip_indexes_on_merge")




When enabled, merges build and store skip indices for new parts.
Otherwise they can be created/stored by explicit [MATERIALIZE INDEX](/docs/sql-reference/statements/alter/skipping-index#materialize-index)
or [during INSERTs](/docs/operations/settings/settings#materialize_skip_indexes_on_insert).


See also [exclude\_materialize\_skip\_indexes\_on\_merge](#exclude_materialize_skip_indexes_on_merge) for more fine\-grained control.


## materialize\_statistics\_on\_merge[​](#materialize_statistics_on_merge "Direct link to materialize_statistics_on_merge")




When enabled, merges will build and store statistics for new parts.
Otherwise they can be created/stored by explicit [MATERIALIZE STATISTICS](/docs/sql-reference/statements/alter/statistics)
or [during INSERTs](/docs/operations/settings/settings#materialize_statistics_on_insert)


## materialize\_ttl\_recalculate\_only[​](#materialize_ttl_recalculate_only "Direct link to materialize_ttl_recalculate_only")



Only recalculate ttl info when MATERIALIZE TTL


## max\_avg\_part\_size\_for\_too\_many\_parts[​](#max_avg_part_size_for_too_many_parts "Direct link to max_avg_part_size_for_too_many_parts")



The 'too many parts' check according to 'parts\_to\_delay\_insert' and
'parts\_to\_throw\_insert' will be active only if the average part size (in the
relevant partition) is not larger than the specified threshold. If it is
larger than the specified threshold, the INSERTs will be neither delayed or
rejected. This allows to have hundreds of terabytes in a single table on a
single server if the parts are successfully merged to larger parts. This
does not affect the thresholds on inactive parts or total parts.


## max\_buckets\_in\_map[​](#max_buckets_in_map "Direct link to max_buckets_in_map")




The maximum number of buckets for `Map` serialization. Works with `with_buckets` `Map` serialization.
The actual number of buckets is determined by [map\_buckets\_strategy](#map_buckets_strategy).
The maximum allowed value is 256\.


## max\_bytes\_to\_merge\_at\_max\_space\_in\_pool[​](#max_bytes_to_merge_at_max_space_in_pool "Direct link to max_bytes_to_merge_at_max_space_in_pool")



The maximum total parts size (in bytes) to be merged into one part, if there
are enough resources available. Corresponds roughly to the maximum possible
part size created by an automatic background merge. (0 means merges will be disabled)


Possible values:


- Any non\-negative integer.


The merge scheduler periodically analyzes the sizes and number of parts in
partitions, and if there are enough free resources in the pool, it starts
background merges. Merges occur until the total size of the source parts is
larger than `max_bytes_to_merge_at_max_space_in_pool`.


Merges initiated by [OPTIMIZE FINAL](/docs/sql-reference/statements/optimize)
ignore `max_bytes_to_merge_at_max_space_in_pool` (only the free disk space
is taken into account).


## max\_bytes\_to\_merge\_at\_min\_space\_in\_pool[​](#max_bytes_to_merge_at_min_space_in_pool "Direct link to max_bytes_to_merge_at_min_space_in_pool")



The maximum total part size (in bytes) to be merged into one part, with the
minimum available resources in the background pool.


Possible values:


- Any positive integer.


`max_bytes_to_merge_at_min_space_in_pool` defines the maximum total size of
parts which can be merged despite the lack of available disk space (in pool).
This is necessary to reduce the number of small parts and the chance of
`Too many parts` errors.
Merges book disk space by doubling the total merged parts sizes.
Thus, with a small amount of free disk space, a situation may occur in which
there is free space, but this space is already booked by ongoing large merges,
so other merges are unable to start, and the number of small parts grows
with every insert.


## max\_cleanup\_delay\_period[​](#max_cleanup_delay_period "Direct link to max_cleanup_delay_period")



Maximum period to clean old queue logs, blocks hashes and parts.


## max\_compress\_block\_size[​](#max_compress_block_size "Direct link to max_compress_block_size")



The maximum size of blocks of uncompressed data before compressing for writing
to a table. You can also specify this setting in the global settings
(see [max\_compress\_block\_size](/docs/operations/settings/merge-tree-settings#max_compress_block_size)
setting). The value specified when the table is created overrides the global
value for this setting.


## max\_concurrent\_queries[​](#max_concurrent_queries "Direct link to max_concurrent_queries")



Max number of concurrently executed queries related to the MergeTree table.
Queries will still be limited by other `max_concurrent_queries` settings.


Possible values:


- Positive integer.
- `0` — No limit.


Default value: `0` (no limit).


**Example**



```
<max_concurrent_queries>50</max_concurrent_queries>

```

## max\_delay\_to\_insert[​](#max_delay_to_insert "Direct link to max_delay_to_insert")



The value in seconds, which is used to calculate the `INSERT` delay, if the
number of active parts in a single partition exceeds the
[parts\_to\_delay\_insert](#parts_to_delay_insert) value.


Possible values:


- Any positive integer.


The delay (in milliseconds) for `INSERT` is calculated by the formula:



```
max_k = parts_to_throw_insert - parts_to_delay_insert
k = 1 + parts_count_in_partition - parts_to_delay_insert
delay_milliseconds = pow(max_delay_to_insert * 1000, k / max_k)

```

For example, if a partition has 299 active parts and parts\_to\_throw\_insert
\= 300, parts\_to\_delay\_insert \= 150, max\_delay\_to\_insert \= 1, `INSERT` is
delayed for `pow( 1 * 1000, (1 + 299 - 150) / (300 - 150) ) = 1000`
milliseconds.


Starting from version 23\.1 formula has been changed to:



```
allowed_parts_over_threshold = parts_to_throw_insert - parts_to_delay_insert
parts_over_threshold = parts_count_in_partition - parts_to_delay_insert + 1
delay_milliseconds = max(min_delay_to_insert_ms, (max_delay_to_insert * 1000)
* parts_over_threshold / allowed_parts_over_threshold)

```

For example, if a partition has 224 active parts and parts\_to\_throw\_insert
\= 300, parts\_to\_delay\_insert \= 150, max\_delay\_to\_insert \= 1,
min\_delay\_to\_insert\_ms \= 10, `INSERT` is delayed for `max( 10, 1 * 1000 * (224 - 150 + 1) / (300 - 150) ) = 500` milliseconds.


## max\_delay\_to\_mutate\_ms[​](#max_delay_to_mutate_ms "Direct link to max_delay_to_mutate_ms")



Max delay of mutating MergeTree table in milliseconds, if there are a lot of
unfinished mutations


## max\_digestion\_size\_per\_segment[​](#max_digestion_size_per_segment "Direct link to max_digestion_size_per_segment")




Obsolete setting, does nothing.


## max\_file\_name\_length[​](#max_file_name_length "Direct link to max_file_name_length")



The maximal length of the file name to keep it as is without hashing.
Takes effect only if setting `replace_long_file_name_to_hash` is enabled.
The value of this setting does not include the length of file extension. So,
it is recommended to set it below the maximum filename length (usually 255
bytes) with some gap to avoid filesystem errors.


## max\_files\_to\_modify\_in\_alter\_columns[​](#max_files_to_modify_in_alter_columns "Direct link to max_files_to_modify_in_alter_columns")



Do not apply ALTER if number of files for modification(deletion, addition)
is greater than this setting.


Possible values:


- Any positive integer.


Default value: 75


## max\_files\_to\_remove\_in\_alter\_columns[​](#max_files_to_remove_in_alter_columns "Direct link to max_files_to_remove_in_alter_columns")



Do not apply ALTER, if the number of files for deletion is greater than this
setting.


Possible values:


- Any positive integer.


## max\_merge\_delayed\_streams\_for\_parallel\_write[​](#max_merge_delayed_streams_for_parallel_write "Direct link to max_merge_delayed_streams_for_parallel_write")




The maximum number of streams (columns) that can be flushed in parallel
(analog of max\_insert\_delayed\_streams\_for\_parallel\_write for merges). Works
only for Vertical merges.


## max\_merge\_selecting\_sleep\_ms[​](#max_merge_selecting_sleep_ms "Direct link to max_merge_selecting_sleep_ms")



Maximum time to wait before trying to select parts to merge again after no
parts were selected. A lower setting will trigger selecting tasks in
background\_schedule\_pool frequently which result in large amount of
requests to zookeeper in large\-scale clusters


## max\_number\_of\_merges\_with\_ttl\_in\_pool[​](#max_number_of_merges_with_ttl_in_pool "Direct link to max_number_of_merges_with_ttl_in_pool")



When there is
more than specified number of merges with TTL entries in pool, do not assign
new merge with TTL. This is to leave free threads for regular merges and
avoid "Too many parts"


## max\_number\_of\_mutations\_for\_replica[​](#max_number_of_mutations_for_replica "Direct link to max_number_of_mutations_for_replica")



Limit the number of part mutations per replica to the specified amount.
Zero means no limit on the number of mutations per replica (the execution can
still be constrained by other settings).


## max\_part\_loading\_threads[​](#max_part_loading_threads "Direct link to max_part_loading_threads")



Obsolete setting, does nothing.


## max\_part\_removal\_threads[​](#max_part_removal_threads "Direct link to max_part_removal_threads")



Obsolete setting, does nothing.


## max\_partitions\_to\_read[​](#max_partitions_to_read "Direct link to max_partitions_to_read")



Limits the maximum number of partitions that can be accessed in one query.


The setting value specified when the table is created can be overridden via
query\-level setting.


Possible values:


- Any positive integer.


You can also specify a query complexity setting [max\_partitions\_to\_read](/docs/operations/settings/settings#max_partitions_to_read)
at a query / session / profile level.


## max\_parts\_in\_total[​](#max_parts_in_total "Direct link to max_parts_in_total")



If the total number of active parts in all partitions of a table exceeds the
`max_parts_in_total` value `INSERT` is interrupted with the `Too many parts (N)` exception.


Possible values:


- Any positive integer.


A large number of parts in a table reduces performance of ClickHouse queries
and increases ClickHouse boot time. Most often this is a consequence of an
incorrect design (mistakes when choosing a partitioning strategy \- too small
partitions).


## max\_parts\_to\_merge\_at\_once[​](#max_parts_to_merge_at_once "Direct link to max_parts_to_merge_at_once")



Max amount of parts which can be merged at once (0 \- disabled). Doesn't affect
OPTIMIZE FINAL query.


## max\_postpone\_time\_for\_failed\_mutations\_ms[​](#max_postpone_time_for_failed_mutations_ms "Direct link to max_postpone_time_for_failed_mutations_ms")



The maximum postpone time for failed mutations.


## max\_postpone\_time\_for\_failed\_replicated\_fetches\_ms[​](#max_postpone_time_for_failed_replicated_fetches_ms "Direct link to max_postpone_time_for_failed_replicated_fetches_ms")




The maximum postpone time for failed replicated fetches.


## max\_postpone\_time\_for\_failed\_replicated\_merges\_ms[​](#max_postpone_time_for_failed_replicated_merges_ms "Direct link to max_postpone_time_for_failed_replicated_merges_ms")




The maximum postpone time for failed replicated merges.


## max\_postpone\_time\_for\_failed\_replicated\_tasks\_ms[​](#max_postpone_time_for_failed_replicated_tasks_ms "Direct link to max_postpone_time_for_failed_replicated_tasks_ms")




The maximum postpone time for failed replicated task. The value is used if the task is not a fetch, merge or mutation.


## max\_projections[​](#max_projections "Direct link to max_projections")



The maximum number of merge tree projections.


## max\_replicated\_fetches\_network\_bandwidth[​](#max_replicated_fetches_network_bandwidth "Direct link to max_replicated_fetches_network_bandwidth")



Limits the maximum speed of data exchange over the network in bytes per
second for [replicated](/docs/engines/table-engines/mergetree-family/replication)
fetches. This setting is applied to a particular table, unlike the
[`max_replicated_fetches_network_bandwidth_for_server`](/docs/operations/settings/merge-tree-settings#max_replicated_fetches_network_bandwidth)
setting, which is applied to the server.


You can limit both server network and network for a particular table, but for
this the value of the table\-level setting should be less than server\-level
one. Otherwise the server considers only the
`max_replicated_fetches_network_bandwidth_for_server` setting.


The setting isn't followed perfectly accurately.


Possible values:


- Positive integer.
- `0` — Unlimited.


Default value: `0`.


**Usage**


Could be used for throttling speed when replicating data to add or replace
new nodes.


## max\_replicated\_logs\_to\_keep[​](#max_replicated_logs_to_keep "Direct link to max_replicated_logs_to_keep")



How many records may be in the ClickHouse Keeper log if there is inactive
replica. An inactive replica becomes lost when when this number exceed.


Possible values:


- Any positive integer.


## max\_replicated\_merges\_in\_queue[​](#max_replicated_merges_in_queue "Direct link to max_replicated_merges_in_queue")



How many tasks of merging and mutating parts are allowed simultaneously in
ReplicatedMergeTree queue.


## max\_replicated\_merges\_with\_ttl\_in\_queue[​](#max_replicated_merges_with_ttl_in_queue "Direct link to max_replicated_merges_with_ttl_in_queue")



How many tasks of merging parts with TTL are allowed simultaneously in
ReplicatedMergeTree queue.


## max\_replicated\_mutations\_in\_queue[​](#max_replicated_mutations_in_queue "Direct link to max_replicated_mutations_in_queue")



How many tasks of mutating parts are allowed simultaneously in
ReplicatedMergeTree queue.


## max\_replicated\_sends\_network\_bandwidth[​](#max_replicated_sends_network_bandwidth "Direct link to max_replicated_sends_network_bandwidth")



Limits the maximum speed of data exchange over the network in bytes per
second for [replicated](/docs/engines/table-engines/mergetree-family/replacingmergetree)
sends. This setting is applied to a particular table, unlike the
[`max_replicated_sends_network_bandwidth_for_server`](/docs/operations/settings/merge-tree-settings#max_replicated_sends_network_bandwidth)
setting, which is applied to the server.


You can limit both server network and network for a particular table, but
for this the value of the table\-level setting should be less than
server\-level one. Otherwise the server considers only the
`max_replicated_sends_network_bandwidth_for_server` setting.


The setting isn't followed perfectly accurately.


Possible values:


- Positive integer.
- `0` — Unlimited.


**Usage**


Could be used for throttling speed when replicating data to add or replace
new nodes.


## max\_suspicious\_broken\_parts[​](#max_suspicious_broken_parts "Direct link to max_suspicious_broken_parts")



If the number of broken parts in a single partition exceeds the
`max_suspicious_broken_parts` value, automatic deletion is denied.


Possible values:


- Any positive integer.


## max\_suspicious\_broken\_parts\_bytes[​](#max_suspicious_broken_parts_bytes "Direct link to max_suspicious_broken_parts_bytes")



Max size of all broken parts, if more \- deny automatic deletion.


Possible values:


- Any positive integer.


## max\_uncompressed\_bytes\_in\_patches[​](#max_uncompressed_bytes_in_patches "Direct link to max_uncompressed_bytes_in_patches")




The maximum uncompressed size of data in all patch parts in bytes.
If amount of data in all patch parts exceeds this value, lightweight updates will be rejected.
0 \- unlimited.


## merge\_max\_block\_size[​](#merge_max_block_size "Direct link to merge_max_block_size")



The number of rows that are read from the merged parts into memory.


Possible values:


- Any positive integer.


Merge reads rows from parts in blocks of `merge_max_block_size` rows, then
merges and writes the result into a new part. The read block is placed in RAM,
so `merge_max_block_size` affects the size of the RAM required for the merge.
Thus, merges can consume a large amount of RAM for tables with very wide rows
(if the average row size is 100kb, then when merging 10 parts,
(100kb \* 10 \* 8192\) \= \~ 8GB of RAM). By decreasing `merge_max_block_size`,
you can reduce the amount of RAM required for a merge but slow down a merge.


## merge\_max\_block\_size\_bytes[​](#merge_max_block_size_bytes "Direct link to merge_max_block_size_bytes")



How many bytes in blocks should be formed for merge operations. By default
has the same value as `index_granularity_bytes`.


## merge\_max\_bytes\_to\_prewarm\_cache[​](#merge_max_bytes_to_prewarm_cache "Direct link to merge_max_bytes_to_prewarm_cache")




Only available in ClickHouse Cloud. Maximal size of part (compact or packed)
to prewarm cache during merge.


## merge\_max\_dynamic\_subcolumns\_in\_compact\_part[​](#merge_max_dynamic_subcolumns_in_compact_part "Direct link to merge_max_dynamic_subcolumns_in_compact_part")




The maximum number of dynamic subcolumns that can be created in every column in the Compact data part after merge.
It allows to control the number of dynamic subcolumns in Compact part regardless of dynamic parameters specified in the data type.


For example, if the table has a column with the JSON(max\_dynamic\_paths\=1024\) type and the setting merge\_max\_dynamic\_subcolumns\_in\_compact\_part is set to 128,
after merge into the Compact data part number of dynamic paths will be decreased to 128 in this part and only 128 paths will be written as dynamic subcolumns.


## merge\_max\_dynamic\_subcolumns\_in\_wide\_part[​](#merge_max_dynamic_subcolumns_in_wide_part "Direct link to merge_max_dynamic_subcolumns_in_wide_part")




The maximum number of dynamic subcolumns that can be created in every column in the Wide data part after merge.
It allows to reduce number of files created in Wide data part regardless of dynamic parameters specified in the data type.


For example, if the table has a column with the JSON(max\_dynamic\_paths\=1024\) type and the setting merge\_max\_dynamic\_subcolumns\_in\_wide\_part is set to 128,
after merge into the Wide data part number of dynamic paths will be decreased to 128 in this part and only 128 paths will be written as dynamic subcolumns.


## merge\_selecting\_sleep\_ms[​](#merge_selecting_sleep_ms "Direct link to merge_selecting_sleep_ms")



Minimum time to wait before trying to select parts to merge again after no
parts were selected. A lower setting will trigger selecting tasks in
background\_schedule\_pool frequently which result in large amount of requests
to zookeeper in large\-scale clusters


## merge\_selecting\_sleep\_slowdown\_factor[​](#merge_selecting_sleep_slowdown_factor "Direct link to merge_selecting_sleep_slowdown_factor")



The sleep time for merge selecting task is multiplied by this factor when
there's nothing to merge and divided when a merge was assigned


## merge\_selector\_algorithm[​](#merge_selector_algorithm "Direct link to merge_selector_algorithm")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

The algorithm to select parts for merges assignment


## merge\_selector\_base[​](#merge_selector_base "Direct link to merge_selector_base")



Affects write amplification of
assigned merges (expert level setting, don't change if you don't understand
what it is doing). Works for Simple and StochasticSimple merge selectors


## merge\_selector\_blurry\_base\_scale\_factor[​](#merge_selector_blurry_base_scale_factor "Direct link to merge_selector_blurry_base_scale_factor")



Controls when the logic kicks in relatively to the number of parts in
partition. The bigger the factor the more belated reaction will be.


## merge\_selector\_enable\_heuristic\_to\_lower\_max\_parts\_to\_merge\_at\_once[​](#merge_selector_enable_heuristic_to_lower_max_parts_to_merge_at_once "Direct link to merge_selector_enable_heuristic_to_lower_max_parts_to_merge_at_once")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Enable heuristic for simple merge selector which will lower maximum limit for merge choice.
By doing so number of concurrent merges will increase which can help with TOO\_MANY\_PARTS
errors but at the same time this will increase the write amplification.


## merge\_selector\_enable\_heuristic\_to\_remove\_small\_parts\_at\_right[​](#merge_selector_enable_heuristic_to_remove_small_parts_at_right "Direct link to merge_selector_enable_heuristic_to_remove_small_parts_at_right")



Enable heuristic for selecting parts for merge which removes parts from right
side of range, if their size is less than specified ratio (0\.01\) of sum\_size.
Works for Simple and StochasticSimple merge selectors


## merge\_selector\_heuristic\_to\_lower\_max\_parts\_to\_merge\_at\_once\_exponent[​](#merge_selector_heuristic_to_lower_max_parts_to_merge_at_once_exponent "Direct link to merge_selector_heuristic_to_lower_max_parts_to_merge_at_once_exponent")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Controls the exponent value used in formulae building lowering curve. Lowering exponent will
lower merge widths which will trigger increase in write amplification. The reverse is also true.


## merge\_selector\_window\_size[​](#merge_selector_window_size "Direct link to merge_selector_window_size")



How many parts to look at once.


## merge\_total\_max\_bytes\_to\_prewarm\_cache[​](#merge_total_max_bytes_to_prewarm_cache "Direct link to merge_total_max_bytes_to_prewarm_cache")




Only available in ClickHouse Cloud. Maximal size of parts in total to prewarm
cache during merge.


## merge\_tree\_clear\_old\_broken\_detached\_parts\_ttl\_timeout\_seconds[​](#merge_tree_clear_old_broken_detached_parts_ttl_timeout_seconds "Direct link to merge_tree_clear_old_broken_detached_parts_ttl_timeout_seconds")



Obsolete setting, does nothing.


## merge\_tree\_clear\_old\_parts\_interval\_seconds[​](#merge_tree_clear_old_parts_interval_seconds "Direct link to merge_tree_clear_old_parts_interval_seconds")



Sets the interval in seconds for ClickHouse to execute the cleanup of old
parts, WALs, and mutations.


Possible values:


- Any positive integer.


## merge\_tree\_clear\_old\_temporary\_directories\_interval\_seconds[​](#merge_tree_clear_old_temporary_directories_interval_seconds "Direct link to merge_tree_clear_old_temporary_directories_interval_seconds")



Sets the interval in seconds for ClickHouse to execute the cleanup of old
temporary directories.


Possible values:


- Any positive integer.


## merge\_tree\_enable\_clear\_old\_broken\_detached[​](#merge_tree_enable_clear_old_broken_detached "Direct link to merge_tree_enable_clear_old_broken_detached")



Obsolete setting, does nothing.


## merge\_with\_recompression\_ttl\_timeout[​](#merge_with_recompression_ttl_timeout "Direct link to merge_with_recompression_ttl_timeout")



Minimum delay in seconds before repeating a merge with recompression TTL.


## merge\_with\_ttl\_timeout[​](#merge_with_ttl_timeout "Direct link to merge_with_ttl_timeout")



Minimum delay in seconds before repeating a merge with delete TTL.


## merge\_workload[​](#merge_workload "Direct link to merge_workload")


Used to regulate how resources are utilized and shared between merges and
other workloads. Specified value is used as `workload` setting value for
background merges of this table. If not specified (empty string), then
server setting `merge_workload` is used instead.


**See Also**


- [Workload Scheduling](/docs/operations/workload-scheduling)


## min\_absolute\_delay\_to\_close[​](#min_absolute_delay_to_close "Direct link to min_absolute_delay_to_close")



Minimal absolute delay to close, stop serving requests and not
return Ok during status check.


## min\_age\_to\_force\_merge\_on\_partition\_only[​](#min_age_to_force_merge_on_partition_only "Direct link to min_age_to_force_merge_on_partition_only")



Whether `min_age_to_force_merge_seconds` should be applied only on the entire
partition and not on subset.


By default, ignores setting `max_bytes_to_merge_at_max_space_in_pool` (see
`enable_max_bytes_limit_for_min_age_to_force_merge`).


Possible values:


- true, false


## min\_age\_to\_force\_merge\_seconds[​](#min_age_to_force_merge_seconds "Direct link to min_age_to_force_merge_seconds")



Merge parts if every part in the range is older than the value of
`min_age_to_force_merge_seconds`.


By default, ignores setting `max_bytes_to_merge_at_max_space_in_pool`
(see `enable_max_bytes_limit_for_min_age_to_force_merge`).


Possible values:


- Positive integer.


## min\_bytes\_for\_compact\_part[​](#min_bytes_for_compact_part "Direct link to min_bytes_for_compact_part")



Obsolete setting, does nothing.


## min\_bytes\_for\_full\_part\_storage[​](#min_bytes_for_full_part_storage "Direct link to min_bytes_for_full_part_storage")



Only available in ClickHouse Cloud. Minimal uncompressed size in bytes to
use full type of storage for data part instead of packed


## min\_bytes\_for\_wide\_part[​](#min_bytes_for_wide_part "Direct link to min_bytes_for_wide_part")



Minimum number of bytes/rows in a data part that can be stored in `Wide`
format. You can set one, both or none of these settings.


## min\_bytes\_to\_prewarm\_caches[​](#min_bytes_to_prewarm_caches "Direct link to min_bytes_to_prewarm_caches")




Minimal size (uncompressed bytes) to prewarm mark cache and primary index cache
for new parts


## min\_bytes\_to\_rebalance\_partition\_over\_jbod[​](#min_bytes_to_rebalance_partition_over_jbod "Direct link to min_bytes_to_rebalance_partition_over_jbod")



Sets minimal amount of bytes to enable balancing when distributing new big
parts over volume disks [JBOD](https://en.wikipedia.org/wiki/Non-RAID_drive_architectures).


Possible values:


- Positive integer.
- `0` — Balancing is disabled.


**Usage**


The value of the `min_bytes_to_rebalance_partition_over_jbod` setting should
not be less than the value of the
[max\_bytes\_to\_merge\_at\_max\_space\_in\_pool](/docs/operations/settings/merge-tree-settings#max_bytes_to_merge_at_max_space_in_pool)
/ 1024\. Otherwise, ClickHouse throws an exception.


## min\_columns\_to\_activate\_adaptive\_write\_buffer[​](#min_columns_to_activate_adaptive_write_buffer "Direct link to min_columns_to_activate_adaptive_write_buffer")




Allow to reduce memory usage for tables with lots of columns by using adaptive writer buffers.


Possible values:


- 0 \- unlimited
- 1 \- always enabled


## min\_compress\_block\_size[​](#min_compress_block_size "Direct link to min_compress_block_size")



Minimum size of blocks of uncompressed data required for compression when
writing the next mark. You can also specify this setting in the global settings
(see [min\_compress\_block\_size](/docs/operations/settings/merge-tree-settings#min_compress_block_size)
setting). The value specified when the table is created overrides the global value
for this setting.


## min\_compressed\_bytes\_to\_fsync\_after\_fetch[​](#min_compressed_bytes_to_fsync_after_fetch "Direct link to min_compressed_bytes_to_fsync_after_fetch")



Minimal number of compressed bytes to do fsync for part after fetch (0 \- disabled)


## min\_compressed\_bytes\_to\_fsync\_after\_merge[​](#min_compressed_bytes_to_fsync_after_merge "Direct link to min_compressed_bytes_to_fsync_after_merge")



Minimal number of compressed bytes to do fsync for part after merge (0 \- disabled)


## min\_delay\_to\_insert\_ms[​](#min_delay_to_insert_ms "Direct link to min_delay_to_insert_ms")



Min delay of inserting data into MergeTree table in milliseconds, if there
are a lot of unmerged parts in single partition.


## min\_delay\_to\_mutate\_ms[​](#min_delay_to_mutate_ms "Direct link to min_delay_to_mutate_ms")



Min delay of mutating MergeTree table in milliseconds, if there are a lot of
unfinished mutations


## min\_free\_disk\_bytes\_to\_perform\_insert[​](#min_free_disk_bytes_to_perform_insert "Direct link to min_free_disk_bytes_to_perform_insert")



The minimum number of bytes that should be free in disk space in order to
insert data. If the number of available free bytes is less than
`min_free_disk_bytes_to_perform_insert` then an exception is thrown and the
insert is not executed. Note that this setting:


- takes into account the `keep_free_space_bytes` setting.
- does not take into account the amount of data that will be written by the
`INSERT` operation.
- is only checked if a positive (non\-zero) number of bytes is specified


Possible values:


- Any positive integer.


NoteIf both `min_free_disk_bytes_to_perform_insert` and `min_free_disk_ratio_to_perform_insert`
are specified, ClickHouse will count on the value that will allow to perform
inserts on a bigger amount of free memory.


## min\_free\_disk\_ratio\_to\_perform\_insert[​](#min_free_disk_ratio_to_perform_insert "Direct link to min_free_disk_ratio_to_perform_insert")



The minimum free to total disk space ratio to perform an `INSERT`. Must be a
floating point value between 0 and 1\. Note that this setting:


- takes into account the `keep_free_space_bytes` setting.
- does not take into account the amount of data that will be written by the
`INSERT` operation.
- is only checked if a positive (non\-zero) ratio is specified


Possible values:


- Float, 0\.0 \- 1\.0


Note that if both `min_free_disk_ratio_to_perform_insert` and
`min_free_disk_bytes_to_perform_insert` are specified, ClickHouse will count
on the value that will allow to perform inserts on a bigger amount of free
memory.


## min\_index\_granularity\_bytes[​](#min_index_granularity_bytes "Direct link to min_index_granularity_bytes")



Min allowed size of data granules in bytes.


To provide a safeguard against accidentally creating tables with very low
`index_granularity_bytes`.


## min\_level\_for\_full\_part\_storage[​](#min_level_for_full_part_storage "Direct link to min_level_for_full_part_storage")




Only available in ClickHouse Cloud. Minimal part level to
use full type of storage for data part instead of packed


## min\_level\_for\_wide\_part[​](#min_level_for_wide_part "Direct link to min_level_for_wide_part")




Minimal part level to create a data part in `Wide` format instead of `Compact`.


## min\_marks\_to\_honor\_max\_concurrent\_queries[​](#min_marks_to_honor_max_concurrent_queries "Direct link to min_marks_to_honor_max_concurrent_queries")



The minimal number of marks read by the query for applying the [max\_concurrent\_queries](#max_concurrent_queries)
setting.


NoteQueries will still be limited by other `max_concurrent_queries` settings.


Possible values:


- Positive integer.
- `0` — Disabled (`max_concurrent_queries` limit applied to no queries).


**Example**



```
<min_marks_to_honor_max_concurrent_queries>10</min_marks_to_honor_max_concurrent_queries>

```

## min\_merge\_bytes\_to\_use\_direct\_io[​](#min_merge_bytes_to_use_direct_io "Direct link to min_merge_bytes_to_use_direct_io")



The minimum data volume for merge operation that is required for using direct
I/O access to the storage disk. When merging data parts, ClickHouse calculates
the total storage volume of all the data to be merged. If the volume exceeds
`min_merge_bytes_to_use_direct_io` bytes, ClickHouse reads and writes the
data to the storage disk using the direct I/O interface (`O_DIRECT` option).
If `min_merge_bytes_to_use_direct_io = 0`, then direct I/O is disabled.


## min\_parts\_to\_merge\_at\_once[​](#min_parts_to_merge_at_once "Direct link to min_parts_to_merge_at_once")



Minimal amount of data parts which merge selector can pick to merge at once
(expert level setting, don't change if you don't understand what it is doing).
0 \- disabled. Works for Simple and StochasticSimple merge selectors.


## min\_relative\_delay\_to\_close[​](#min_relative_delay_to_close "Direct link to min_relative_delay_to_close")



Minimal delay from other replicas to close, stop serving
requests and not return Ok during status check.


## min\_relative\_delay\_to\_measure[​](#min_relative_delay_to_measure "Direct link to min_relative_delay_to_measure")



Calculate relative replica delay only if absolute delay is not less that
this value.


## min\_relative\_delay\_to\_yield\_leadership[​](#min_relative_delay_to_yield_leadership "Direct link to min_relative_delay_to_yield_leadership")



Obsolete setting, does nothing.


## min\_replicated\_logs\_to\_keep[​](#min_replicated_logs_to_keep "Direct link to min_replicated_logs_to_keep")



Keep about this number of last records in ZooKeeper log, even if they are
obsolete. It doesn't affect work of tables: used only to diagnose ZooKeeper
log before cleaning.


Possible values:


- Any positive integer.


## min\_rows\_for\_compact\_part[​](#min_rows_for_compact_part "Direct link to min_rows_for_compact_part")



Obsolete setting, does nothing.


## min\_rows\_for\_full\_part\_storage[​](#min_rows_for_full_part_storage "Direct link to min_rows_for_full_part_storage")



Only available in ClickHouse Cloud. Minimal number of rows to use full type
of storage for data part instead of packed


## min\_rows\_for\_wide\_part[​](#min_rows_for_wide_part "Direct link to min_rows_for_wide_part")



Minimal number of rows to create a data part in `Wide` format instead of `Compact`.


## min\_rows\_to\_fsync\_after\_merge[​](#min_rows_to_fsync_after_merge "Direct link to min_rows_to_fsync_after_merge")



Minimal number of rows to do fsync for part after merge (0 \- disabled)


## mutation\_workload[​](#mutation_workload "Direct link to mutation_workload")


Used to regulate how resources are utilized and shared between mutations and
other workloads. Specified value is used as `workload` setting value for
background mutations of this table. If not specified (empty string), then
server setting `mutation_workload` is used instead.


**See Also**


- [Workload Scheduling](/docs/operations/workload-scheduling)


## non\_replicated\_deduplication\_window[​](#non_replicated_deduplication_window "Direct link to non_replicated_deduplication_window")



The number of the most recently inserted blocks in the non\-replicated
[MergeTree](/docs/engines/table-engines/mergetree-family/mergetree) table
for which hash sums are stored to check for duplicates.


Possible values:


- Any positive integer.
- `0` (disable deduplication).


A deduplication mechanism is used, similar to replicated tables (see
[replicated\_deduplication\_window](#replicated_deduplication_window) setting).
The hash sums of the created parts are written to a local file on a disk.


## notify\_newest\_block\_number[​](#notify_newest_block_number "Direct link to notify_newest_block_number")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


Notify newest block number to SharedJoin or SharedSet. Only in ClickHouse Cloud.


## nullable\_serialization\_version[​](#nullable_serialization_version "Direct link to nullable_serialization_version")




Controls the serialization method used for `Nullable(T)` columns.


Possible values:


- basic — Use the standard serialization for `Nullable(T)`.
- allow\_sparse — Permit `Nullable(T)` to use sparse encoding.


## number\_of\_free\_entries\_in\_pool\_to\_execute\_mutation[​](#number_of_free_entries_in_pool_to_execute_mutation "Direct link to number_of_free_entries_in_pool_to_execute_mutation")



When there is less than specified number of free entries in pool, do not
execute part mutations. This is to leave free threads for regular merges and
to avoid "Too many parts" errors.


Possible values:


- Any positive integer.


**Usage**


The value of the `number_of_free_entries_in_pool_to_execute_mutation` setting
should be less than the value of the [background\_pool\_size](/docs/operations/server-configuration-parameters/settings#background_pool_size)


- [background\_merges\_mutations\_concurrency\_ratio](/docs/operations/server-configuration-parameters/settings#background_merges_mutations_concurrency_ratio).
Otherwise, ClickHouse will throw an exception.


## number\_of\_free\_entries\_in\_pool\_to\_execute\_optimize\_entire\_partition[​](#number_of_free_entries_in_pool_to_execute_optimize_entire_partition "Direct link to number_of_free_entries_in_pool_to_execute_optimize_entire_partition")



When there is less than specified number of free entries in pool, do not
execute optimizing entire partition in the background (this task generated
when set `min_age_to_force_merge_seconds` and enable
`min_age_to_force_merge_on_partition_only`). This is to leave free threads
for regular merges and avoid "Too many parts".


Possible values:


- Positive integer.


The value of the `number_of_free_entries_in_pool_to_execute_optimize_entire_partition`
setting should be less than the value of the
[background\_pool\_size](/docs/operations/server-configuration-parameters/settings#background_pool_size)


- [background\_merges\_mutations\_concurrency\_ratio](/docs/operations/server-configuration-parameters/settings#background_merges_mutations_concurrency_ratio).
Otherwise, ClickHouse throws an exception.


## number\_of\_free\_entries\_in\_pool\_to\_lower\_max\_size\_of\_merge[​](#number_of_free_entries_in_pool_to_lower_max_size_of_merge "Direct link to number_of_free_entries_in_pool_to_lower_max_size_of_merge")



When there is less than the specified number of free entries in pool
(or replicated queue), start to lower maximum size of merge to process
(or to put in queue).
This is to allow small merges to process \- not filling the pool with long
running merges.


Possible values:


- Any positive integer.


## number\_of\_mutations\_to\_delay[​](#number_of_mutations_to_delay "Direct link to number_of_mutations_to_delay")



If table has at least
that many unfinished mutations, artificially slow down mutations of table.
Disabled if set to 0


## number\_of\_mutations\_to\_throw[​](#number_of_mutations_to_throw "Direct link to number_of_mutations_to_throw")



If table has at least that many unfinished mutations, throw 'Too many mutations'
exception. Disabled if set to 0


## number\_of\_partitions\_to\_consider\_for\_merge[​](#number_of_partitions_to_consider_for_merge "Direct link to number_of_partitions_to_consider_for_merge")




Only available in ClickHouse Cloud. Up to top N partitions which we will
consider for merge. Partitions picked in a random weighted way where weight
is amount of data parts which can be merged in this partition.


## object\_serialization\_version[​](#object_serialization_version "Direct link to object_serialization_version")




Serialization version for JSON data type. Required for compatibility.


Possible values:


- `v1`
- `v2`
- `v3`


Only version `v3` supports changing the shared data serialization version.


## object\_shared\_data\_buckets\_for\_compact\_part[​](#object_shared_data_buckets_for_compact_part "Direct link to object_shared_data_buckets_for_compact_part")




The number of buckets for JSON shared data serialization in Compact parts. Works with `map_with_buckets` and `advanced` shared data serializations.
The maximum allowed value is 256\.


## object\_shared\_data\_buckets\_for\_wide\_part[​](#object_shared_data_buckets_for_wide_part "Direct link to object_shared_data_buckets_for_wide_part")




The number of buckets for JSON shared data serialization in Wide parts. Works with `map_with_buckets` and `advanced` shared data serializations.
The maximum allowed value is 256\.


## object\_shared\_data\_serialization\_version[​](#object_shared_data_serialization_version "Direct link to object_shared_data_serialization_version")




Serialization version for shared data inside JSON data type.


Possible values:


- `map` \- store shared data as `Map(String, String)`
- `map_with_buckets` \- store shared data as several separate `Map(String, String)` columns. Using buckets improves reading individual paths from shared data.
- `advanced` \- special serialization of shared data designed to significantly improve reading of individual paths from shared data.
Note that this serialization increases the shared data storage size on disk because we store a lot of additional information.


The number of buckets for `map_with_buckets` and `advanced` serializations is determined by settings
[object\_shared\_data\_buckets\_for\_compact\_part](#object_shared_data_buckets_for_compact_part)/[object\_shared\_data\_buckets\_for\_wide\_part](#object_shared_data_buckets_for_wide_part).


## object\_shared\_data\_serialization\_version\_for\_zero\_level\_parts[​](#object_shared_data_serialization_version_for_zero_level_parts "Direct link to object_shared_data_serialization_version_for_zero_level_parts")




This setting allows to specify different serialization version of the
shared data inside JSON type for zero level parts that are created during inserts.
It's recommended not to use `advanced` shared data serialization for zero level parts because it can increase
the insertion time significantly.


## old\_parts\_lifetime[​](#old_parts_lifetime "Direct link to old_parts_lifetime")



The time (in seconds) of storing inactive parts to protect against data loss
during spontaneous server reboots.


Possible values:


- Any positive integer.


After merging several parts into a new part, ClickHouse marks the original
parts as inactive and deletes them only after `old_parts_lifetime` seconds.
Inactive parts are removed if they are not used by current queries, i.e. if
the `refcount` of the part is 1\.


`fsync` is not called for new parts, so for some time new parts exist only
in the server's RAM (OS cache). If the server is rebooted spontaneously, new
parts can be lost or damaged. To protect data inactive parts are not deleted
immediately.


During startup ClickHouse checks the integrity of the parts. If the merged
part is damaged ClickHouse returns the inactive parts to the active list,
and later merges them again. Then the damaged part is renamed (the `broken_`
prefix is added) and moved to the `detached` folder. If the merged part is
not damaged, then the original inactive parts are renamed (the `ignored_`
prefix is added) and moved to the `detached` folder.


The default `dirty_expire_centisecs` value (a Linux kernel setting) is 30
seconds (the maximum time that written data is stored only in RAM), but under
heavy loads on the disk system data can be written much later. Experimentally,
a value of 480 seconds was chosen for `old_parts_lifetime`, during which a
new part is guaranteed to be written to disk.


## optimize\_row\_order[​](#optimize_row_order "Direct link to optimize_row_order")



Controls if the row order should be optimized during inserts to improve the
compressability of the newly inserted table part.


Only has an effect for ordinary MergeTree\-engine tables. Does nothing for
specialized MergeTree engine tables (e.g. CollapsingMergeTree).


MergeTree tables are (optionally) compressed using [compression codecs](/docs/sql-reference/statements/create/table#column_compression_codec).
Generic compression codecs such as LZ4 and ZSTD achieve maximum compression
rates if the data exposes patterns. Long runs of the same value typically
compress very well.


If this setting is enabled, ClickHouse attempts to store the data in newly
inserted parts in a row order that minimizes the number of equal\-value runs
across the columns of the new table part.
In other words, a small number of equal\-value runs mean that individual runs
are long and compress well.


Finding the optimal row order is computationally infeasible (NP hard).
Therefore, ClickHouse uses a heuristics to quickly find a row order which
still improves compression rates over the original row order.


Heuristics for finding a row orderIt is generally possible to shuffle the rows of a table (or table part)
freely as SQL considers the same table (table part) in different row order
equivalent.This freedom of shuffling rows is restricted when a primary key is defined
for the table. In ClickHouse, a primary key `C1, C2, ..., CN` enforces that
the table rows are sorted by columns `C1`, `C2`, ... `Cn` ([clustered index](https://en.wikipedia.org/wiki/Database_index#Clustered)).
As a result, rows can only be shuffled within "equivalence classes" of row,
i.e. rows which have the same values in their primary key columns.
The intuition is that primary keys with high\-cardinality, e.g. primary keys
involving a `DateTime64` timestamp column, lead to many small equivalence
classes. Likewise, tables with a low\-cardinality primary key, create few and
large equivalence classes. A table with no primary key represents the extreme
case of a single equivalence class which spans all rows.The fewer and the larger the equivalence classes are, the higher the degree
of freedom when re\-shuffling rows.The heuristics applied to find the best row order within each equivalence
class is suggested by D. Lemire, O. Kaser in
[Reordering columns for smaller indexes](https://doi.org/10.1016/j.ins.2011.02.002)
and based on sorting the rows within each equivalence class by ascending
cardinality of the non\-primary key columns.It performs three steps:1. Find all equivalence classes based on the row values in primary key columns.
2. For each equivalence class, calculate (usually estimate) the cardinalities
of the non\-primary\-key columns.
3. For each equivalence class, sort the rows in order of ascending
non\-primary\-key column cardinality.











If enabled, insert operations incur additional CPU costs to analyze and
optimize the row order of the new data. INSERTs are expected to take 30\-50%
longer depending on the data characteristics.
Compression rates of LZ4 or ZSTD improve on average by 20\-40%.


This setting works best for tables with no primary key or a low\-cardinality
primary key, i.e. a table with only few distinct primary key values.
High\-cardinality primary keys, e.g. involving timestamp columns of type
`DateTime64`, are not expected to benefit from this setting.


## part\_minmax\_index\_columns[​](#part_minmax_index_columns "Direct link to part_minmax_index_columns")




Selects which columns the per\-part min\-max index covers. Each value enables an additional group of columns on top of the previous one.


Possible values:


- `partition_key_only` — only the partition\-key columns are tracked.
- `with_block_number_offset` — partition\-key columns plus the persisted `_block_number` and `_block_offset` virtual columns. Enables part\-level pruning by these columns.


## part\_moves\_between\_shards\_delay\_seconds[​](#part_moves_between_shards_delay_seconds "Direct link to part_moves_between_shards_delay_seconds")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Time to wait before/after moving parts between shards.


## part\_moves\_between\_shards\_enable[​](#part_moves_between_shards_enable "Direct link to part_moves_between_shards_enable")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Experimental/Incomplete feature to move parts between shards. Does not take
into account sharding expressions.


## parts\_to\_delay\_insert[​](#parts_to_delay_insert "Direct link to parts_to_delay_insert")



If the number of active parts in a single partition exceeds the
`parts_to_delay_insert` value, an `INSERT` is artificially slowed down.


Possible values:


- Any positive integer.


ClickHouse artificially executes `INSERT` longer (adds 'sleep') so that the
background merge process can merge parts faster than they are added.


## parts\_to\_throw\_insert[​](#parts_to_throw_insert "Direct link to parts_to_throw_insert")



If the number of active parts in a single partition exceeds the
`parts_to_throw_insert` value, `INSERT` is interrupted with the `Too many parts (N). Merges are processing significantly slower than inserts`
exception.


Possible values:


- Any positive integer.


To achieve maximum performance of `SELECT` queries, it is necessary to
minimize the number of parts processed, see [Merge Tree](/docs/development/architecture#merge-tree).


Prior to version 23\.6 this setting was set to 300\. You can set a higher
different value, it will reduce the probability of the `Too many parts`
error, but at the same time `SELECT` performance might degrade. Also in case
of a merge issue (for example, due to insufficient disk space) you will
notice it later than you would with the original 300\.


## prefer\_fetch\_merged\_part\_size\_threshold[​](#prefer_fetch_merged_part_size_threshold "Direct link to prefer_fetch_merged_part_size_threshold")



If the sum of the size of parts exceeds this threshold and the time since a
replication log entry creation is greater than
`prefer_fetch_merged_part_time_threshold`, then prefer fetching merged part
from a replica instead of doing merge locally. This is to speed up very long
merges.


Possible values:


- Any positive integer.


## prefer\_fetch\_merged\_part\_time\_threshold[​](#prefer_fetch_merged_part_time_threshold "Direct link to prefer_fetch_merged_part_time_threshold")



If the time passed since a replication log (ClickHouse Keeper or ZooKeeper)
entry creation exceeds this threshold, and the sum of the size of parts is
greater than `prefer_fetch_merged_part_size_threshold`, then prefer fetching
merged part from a replica instead of doing merge locally. This is to speed
up very long merges.


Possible values:


- Any positive integer.


## prewarm\_mark\_cache[​](#prewarm_mark_cache "Direct link to prewarm_mark_cache")



If true mark cache will be
prewarmed by saving marks to mark cache on inserts, merges, fetches and on
startup of server


## prewarm\_primary\_key\_cache[​](#prewarm_primary_key_cache "Direct link to prewarm_primary_key_cache")




If true primary index
cache will be prewarmed by saving marks to mark cache on inserts, merges,
fetches and on startup of server


## primary\_key\_compress\_block\_size[​](#primary_key_compress_block_size "Direct link to primary_key_compress_block_size")



Primary compress block size, the actual size of the block to compress.


## primary\_key\_compression\_codec[​](#primary_key_compression_codec "Direct link to primary_key_compression_codec")



Compression encoding used by primary, primary key is small enough and cached,
so the default compression is ZSTD(3\).


## primary\_key\_lazy\_load[​](#primary_key_lazy_load "Direct link to primary_key_lazy_load")



Load primary key in memory on
first use instead of on table initialization. This can save memory in the
presence of a large number of tables.


## primary\_key\_ratio\_of\_unique\_prefix\_values\_to\_skip\_suffix\_columns[​](#primary_key_ratio_of_unique_prefix_values_to_skip_suffix_columns "Direct link to primary_key_ratio_of_unique_prefix_values_to_skip_suffix_columns")



If the value of a column of the primary key in data part changes at least in
this ratio of times, skip loading next columns in memory. This allows to save
memory usage by not loading useless columns of the primary key.


## propagate\_types\_serialization\_versions\_to\_nested\_types[​](#propagate_types_serialization_versions_to_nested_types "Direct link to propagate_types_serialization_versions_to_nested_types")




If true, serialization versions like string\_serialization\_version will be propagated inside nested types like Array/Map/Nullable/JSON/etc. If disabled, the serialization version will take affect only to top\-level columns of this type and Tuple el


## ratio\_of\_defaults\_for\_sparse\_serialization[​](#ratio_of_defaults_for_sparse_serialization "Direct link to ratio_of_defaults_for_sparse_serialization")



Minimal ratio of the number of *default* values to the number of *all* values
in a column. Setting this value causes the column to be stored using sparse
serializations.


If a column is sparse (contains mostly zeros), ClickHouse can encode it in
a sparse format and automatically optimize calculations \- the data does not
require full decompression during queries. To enable this sparse
serialization, define the `ratio_of_defaults_for_sparse_serialization`
setting to be less than 1\.0\. If the value is greater than or equal to 1\.0,
then the columns will be always written using the normal full serialization.


Possible values:


- Float between `0` and `1` to enable sparse serialization
- `1.0` (or greater) if you do not want to use sparse serialization


**Example**


Notice the `s` column in the following table is an empty string for 95% of
the rows. In `my_regular_table` we do not use sparse serialization, and in
`my_sparse_table` we set `ratio_of_defaults_for_sparse_serialization` to
0\.95:



```
CREATE TABLE my_regular_table
(
`id` UInt64,
`s` String
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO my_regular_table
SELECT
number AS id,
number % 20 = 0 ? toString(number): '' AS s
FROM
numbers(10000000);


CREATE TABLE my_sparse_table
(
`id` UInt64,
`s` String
)
ENGINE = MergeTree
ORDER BY id
SETTINGS ratio_of_defaults_for_sparse_serialization = 0.95;

INSERT INTO my_sparse_table
SELECT
number,
number % 20 = 0 ? toString(number): ''
FROM
numbers(10000000);

```

Notice the `s` column in `my_sparse_table` uses less storage space on disk:



```
SELECT table, name, data_compressed_bytes, data_uncompressed_bytes FROM system.columns
WHERE table LIKE 'my_%_table';

```


```
┌─table────────────┬─name─┬─data_compressed_bytes─┬─data_uncompressed_bytes─┐
│ my_regular_table │ id   │              37790741 │                75488328 │
│ my_regular_table │ s    │               2451377 │                12683106 │
│ my_sparse_table  │ id   │              37790741 │                75488328 │
│ my_sparse_table  │ s    │               2283454 │                 9855751 │
└──────────────────┴──────┴───────────────────────┴─────────────────────────┘

```

You can verify if a column is using the sparse encoding by viewing the
`serialization_kind` column of the `system.parts_columns` table:



```
SELECT column, serialization_kind FROM system.parts_columns
WHERE table LIKE 'my_sparse_table';

```

You can see which parts of `s` were stored using the sparse serialization:



```
┌─column─┬─serialization_kind─┐
│ id     │ Default            │
│ s      │ Default            │
│ id     │ Default            │
│ s      │ Default            │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
│ id     │ Default            │
│ s      │ Sparse             │
└────────┴────────────────────┘

```

## reduce\_blocking\_parts\_sleep\_ms[​](#reduce_blocking_parts_sleep_ms "Direct link to reduce_blocking_parts_sleep_ms")




Only available in ClickHouse Cloud. Minimum time to wait before trying to
reduce blocking parts again after no ranges were dropped/replaced. A lower
setting will trigger tasks in background\_schedule\_pool frequently which
results in large amount of requests to zookeeper in large\-scale clusters


## refresh\_parts\_interval[​](#refresh_parts_interval "Direct link to refresh_parts_interval")




If it is greater than zero \- refresh the list of data parts from the underlying filesystem to check if the data was updated under the hood.
It can be set only if the table is located on readonly disks (which means that this is a readonly replica, while data is being written by another replica).


## refresh\_statistics\_interval[​](#refresh_statistics_interval "Direct link to refresh_statistics_interval")




The interval of refreshing statistics cache in seconds. If it is set to zero, the refreshing will be disabled.


## remote\_fs\_execute\_merges\_on\_single\_replica\_time\_threshold[​](#remote_fs_execute_merges_on_single_replica_time_threshold "Direct link to remote_fs_execute_merges_on_single_replica_time_threshold")



When this setting has a value greater than zero only a single replica starts
the merge immediately if merged part on shared storage.


NoteZero\-copy replication is not ready for production
Zero\-copy replication is disabled by default in ClickHouse version 22\.8 and
higher.This feature is not recommended for production use.




Possible values:


- Any positive integer.


## remote\_fs\_zero\_copy\_path\_compatible\_mode[​](#remote_fs_zero_copy_path_compatible_mode "Direct link to remote_fs_zero_copy_path_compatible_mode")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Run zero\-copy in compatible mode during conversion process.


## remote\_fs\_zero\_copy\_zookeeper\_path[​](#remote_fs_zero_copy_zookeeper_path "Direct link to remote_fs_zero_copy_zookeeper_path")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

ZooKeeper path for zero\-copy table\-independent info.


## remove\_empty\_parts[​](#remove_empty_parts "Direct link to remove_empty_parts")



Remove empty parts after they were pruned by TTL, mutation, or collapsing
merge algorithm.


## remove\_rolled\_back\_parts\_immediately[​](#remove_rolled_back_parts_immediately "Direct link to remove_rolled_back_parts_immediately")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)

Setting for an incomplete experimental feature.


## remove\_unused\_patch\_parts[​](#remove_unused_patch_parts "Direct link to remove_unused_patch_parts")




Remove in background patch parts which are applied for all active parts.


## replace\_long\_file\_name\_to\_hash[​](#replace_long_file_name_to_hash "Direct link to replace_long_file_name_to_hash")



If the file name for column is too long (more than 'max\_file\_name\_length'
bytes) replace it to SipHash128


## replicated\_can\_become\_leader[​](#replicated_can_become_leader "Direct link to replicated_can_become_leader")



If true, replicated tables replicas on this node will try to acquire
leadership.


Possible values:


- `true`
- `false`


## replicated\_deduplication\_window[​](#replicated_deduplication_window "Direct link to replicated_deduplication_window")




The number of most recently inserted blocks for which ClickHouse Keeper stores
hash sums to check for duplicates.


Possible values:


- Any positive integer.
- 0 (disable deduplication)


The `Insert` command creates one or more blocks (parts). For
[insert deduplication](/docs/engines/table-engines/mergetree-family/replication),
when writing into replicated tables, ClickHouse writes the hash sums of the
created parts into ClickHouse Keeper. Hash sums are stored only for the most
recent `replicated_deduplication_window` blocks. The oldest hash sums are
removed from ClickHouse Keeper.


A large number for `replicated_deduplication_window` slows down `Inserts`
because more entries need to be compared. The hash sum is calculated from
the composition of the field names and types and the data of the inserted
part (stream of bytes).


## replicated\_deduplication\_window\_for\_async\_inserts[​](#replicated_deduplication_window_for_async_inserts "Direct link to replicated_deduplication_window_for_async_inserts")



The number of most recently async inserted blocks for which ClickHouse Keeper
stores hash sums to check for duplicates.


Possible values:


- Any positive integer.
- 0 (disable deduplication for async\_inserts)


The [Async Insert](/docs/operations/settings/settings#async_insert) command will
be cached in one or more blocks (parts). For [insert deduplication](/docs/engines/table-engines/mergetree-family/replication),
when writing into replicated tables, ClickHouse writes the hash sums of each
insert into ClickHouse Keeper. Hash sums are stored only for the most recent
`replicated_deduplication_window_for_async_inserts` blocks. The oldest hash
sums are removed from ClickHouse Keeper.
A large number of `replicated_deduplication_window_for_async_inserts` slows
down `Async Inserts` because it needs to compare more entries.
The hash sum is calculated from the composition of the field names and types
and the data of the insert (stream of bytes).


## replicated\_deduplication\_window\_seconds[​](#replicated_deduplication_window_seconds "Direct link to replicated_deduplication_window_seconds")




The number of seconds after which the hash sums of the inserted blocks are
removed from ClickHouse Keeper.


Possible values:


- Any positive integer.


Similar to [replicated\_deduplication\_window](#replicated_deduplication_window),
`replicated_deduplication_window_seconds` specifies how long to store hash
sums of blocks for insert deduplication. Hash sums older than
`replicated_deduplication_window_seconds` are removed from ClickHouse Keeper,
even if they are less than  `replicated_deduplication_window`.


The time is relative to the time of the most recent record, not to the wall
time. If it's the only record it will be stored forever.


## replicated\_deduplication\_window\_seconds\_for\_async\_inserts[​](#replicated_deduplication_window_seconds_for_async_inserts "Direct link to replicated_deduplication_window_seconds_for_async_inserts")



The number of seconds after which the hash sums of the async inserts are
removed from ClickHouse Keeper.


Possible values:


- Any positive integer.


Similar to [replicated\_deduplication\_window\_for\_async\_inserts](#replicated_deduplication_window_for_async_inserts),
`replicated_deduplication_window_seconds_for_async_inserts` specifies how
long to store hash sums of blocks for async insert deduplication. Hash sums
older than `replicated_deduplication_window_seconds_for_async_inserts` are
removed from ClickHouse Keeper, even if they are less than
`replicated_deduplication_window_for_async_inserts`.


The time is relative to the time of the most recent record, not to the wall
time. If it's the only record it will be stored forever.


## replicated\_fetches\_http\_connection\_timeout[​](#replicated_fetches_http_connection_timeout "Direct link to replicated_fetches_http_connection_timeout")



Obsolete setting, does nothing.


## replicated\_fetches\_http\_receive\_timeout[​](#replicated_fetches_http_receive_timeout "Direct link to replicated_fetches_http_receive_timeout")



Obsolete setting, does nothing.


## replicated\_fetches\_http\_send\_timeout[​](#replicated_fetches_http_send_timeout "Direct link to replicated_fetches_http_send_timeout")



Obsolete setting, does nothing.


## replicated\_fetches\_min\_part\_level[​](#replicated_fetches_min_part_level "Direct link to replicated_fetches_min_part_level")




Minimum part level to fetch from other replicas. Parts with level below this threshold are postponed
(kept in the replication queue and re\-evaluated each scheduling cycle, not permanently skipped).
Use 1 to postpone fetching level\-0 (unmerged) parts, reducing replication overhead during heavy ingestion.
Default: 0 (fetch all parts regardless of level).


## replicated\_fetches\_min\_part\_level\_timeout\_seconds[​](#replicated_fetches_min_part_level_timeout_seconds "Direct link to replicated_fetches_min_part_level_timeout_seconds")




Timeout in seconds after which a part below replicated\_fetches\_min\_part\_level will be fetched anyway.
Use 0 to disable the timeout (parts below the minimum level are postponed indefinitely until merged).
Default: 300 (force fetch after 5 minutes).


## replicated\_max\_mutations\_in\_one\_entry[​](#replicated_max_mutations_in_one_entry "Direct link to replicated_max_mutations_in_one_entry")



Max number of mutation commands that can be merged together and executed in
one MUTATE\_PART entry (0 means unlimited)


## replicated\_max\_parallel\_fetches[​](#replicated_max_parallel_fetches "Direct link to replicated_max_parallel_fetches")



Obsolete setting, does nothing.


## replicated\_max\_parallel\_fetches\_for\_host[​](#replicated_max_parallel_fetches_for_host "Direct link to replicated_max_parallel_fetches_for_host")



Obsolete setting, does nothing.


## replicated\_max\_parallel\_fetches\_for\_table[​](#replicated_max_parallel_fetches_for_table "Direct link to replicated_max_parallel_fetches_for_table")



Obsolete setting, does nothing.


## replicated\_max\_parallel\_sends[​](#replicated_max_parallel_sends "Direct link to replicated_max_parallel_sends")



Obsolete setting, does nothing.


## replicated\_max\_parallel\_sends\_for\_table[​](#replicated_max_parallel_sends_for_table "Direct link to replicated_max_parallel_sends_for_table")



Obsolete setting, does nothing.


## replicated\_max\_ratio\_of\_wrong\_parts[​](#replicated_max_ratio_of_wrong_parts "Direct link to replicated_max_ratio_of_wrong_parts")



If the ratio of wrong parts to total number of parts is less than this \-
allow to start.


Possible values:


- Float, 0\.0 \- 1\.0


## search\_orphaned\_parts\_disks[​](#search_orphaned_parts_disks "Direct link to search_orphaned_parts_disks")




ClickHouse scans all disks for orphaned parts upon any ATTACH or CREATE table
in order to not allow to miss data parts at undefined (not included in policy) disks.
Orphaned parts originates from potentially unsafe storage reconfiguration, e.g. if a disk was excluded from storage policy.
This setting limits scope of disks to search by traits of the disks.


Possible values:


- any \- scope is not limited.
- local \- scope is limited by local disks .
- none \- empty scope, do not search


## serialization\_info\_version[​](#serialization_info_version "Direct link to serialization_info_version")




Serialization info version used when writing `serialization.json`.
This setting is required for compatibility during cluster upgrades.


Possible values:


- `basic` \- Basic format.
- `with_types` \- Format with additional `types_serialization_versions` field, allowing per\-type serialization versions.
This makes settings like `string_serialization_version` effective.


During rolling upgrades, set this to `basic` so that new servers produce
data parts compatible with old servers. After the upgrade completes,
switch to `WITH_TYPES` to enable per\-type serialization versions.


## share\_nested\_offsets[​](#share_nested_offsets "Direct link to share_nested_offsets")




When enabled (default), Array columns with dotted names that share a common prefix (e.g. n.a and n.b)
are treated as part of a Nested structure: they share a single offsets file on disk (e.g. n.size0\),
and their array sizes are validated to be equal during INSERT.
When disabled, each Array column gets its own independent offset file, dotted names carry no special
semantics, and a scalar column may coexist with dotted Array columns sharing the same prefix
(e.g. n UInt32 alongside n.a Array(String)). This setting is immutable after table creation.


## shared\_merge\_tree\_activate\_coordinated\_merges\_tasks[​](#shared_merge_tree_activate_coordinated_merges_tasks "Direct link to shared_merge_tree_activate_coordinated_merges_tasks")




Activates rescheduling of coordinated merges tasks. It can be useful even when
shared\_merge\_tree\_enable\_coordinated\_merges\=0 because this will populate merge coordinator
statistics and help with cold start.


## shared\_merge\_tree\_create\_per\_replica\_metadata\_nodes[​](#shared_merge_tree_create_per_replica_metadata_nodes "Direct link to shared_merge_tree_create_per_replica_metadata_nodes")




Enables creation of per\-replica /metadata and /columns nodes in ZooKeeper.
Only available in ClickHouse Cloud


## shared\_merge\_tree\_disable\_merges\_and\_mutations\_assignment[​](#shared_merge_tree_disable_merges_and_mutations_assignment "Direct link to shared_merge_tree_disable_merges_and_mutations_assignment")



Stop merges assignment for shared merge tree. Only available in ClickHouse
Cloud


## shared\_merge\_tree\_empty\_partition\_lifetime[​](#shared_merge_tree_empty_partition_lifetime "Direct link to shared_merge_tree_empty_partition_lifetime")




How many seconds partition will be stored in keeper if it has no parts.


## shared\_merge\_tree\_enable\_automatic\_empty\_partitions\_cleanup[​](#shared_merge_tree_enable_automatic_empty_partitions_cleanup "Direct link to shared_merge_tree_enable_automatic_empty_partitions_cleanup")




Enabled cleanup of Keeper entries of empty partition.


## shared\_merge\_tree\_enable\_coordinated\_merges[​](#shared_merge_tree_enable_coordinated_merges "Direct link to shared_merge_tree_enable_coordinated_merges")




Enables coordinated merges strategy


## shared\_merge\_tree\_enable\_keeper\_parts\_extra\_data[​](#shared_merge_tree_enable_keeper_parts_extra_data "Direct link to shared_merge_tree_enable_keeper_parts_extra_data")




Enables writing attributes into virtual parts and committing blocks in keeper


## shared\_merge\_tree\_enable\_outdated\_parts\_check[​](#shared_merge_tree_enable_outdated_parts_check "Direct link to shared_merge_tree_enable_outdated_parts_check")




Enable outdated parts check. Only available in ClickHouse Cloud


## shared\_merge\_tree\_idle\_parts\_update\_seconds[​](#shared_merge_tree_idle_parts_update_seconds "Direct link to shared_merge_tree_idle_parts_update_seconds")




Interval in seconds for parts update without being triggered by ZooKeeper
watch in the shared merge tree. Only available in ClickHouse Cloud


## shared\_merge\_tree\_initial\_parts\_update\_backoff\_ms[​](#shared_merge_tree_initial_parts_update_backoff_ms "Direct link to shared_merge_tree_initial_parts_update_backoff_ms")




Initial backoff for parts update. Only available in ClickHouse Cloud


## shared\_merge\_tree\_interserver\_http\_connection\_timeout\_ms[​](#shared_merge_tree_interserver_http_connection_timeout_ms "Direct link to shared_merge_tree_interserver_http_connection_timeout_ms")




Timeouts for interserver HTTP connection. Only available in ClickHouse Cloud


## shared\_merge\_tree\_interserver\_http\_timeout\_ms[​](#shared_merge_tree_interserver_http_timeout_ms "Direct link to shared_merge_tree_interserver_http_timeout_ms")




Timeouts for interserver HTTP communication. Only available in ClickHouse
Cloud


## shared\_merge\_tree\_leader\_update\_period\_random\_add\_seconds[​](#shared_merge_tree_leader_update_period_random_add_seconds "Direct link to shared_merge_tree_leader_update_period_random_add_seconds")




Add uniformly distributed value from 0 to x seconds to
shared\_merge\_tree\_leader\_update\_period to avoid thundering
herd effect. Only available in ClickHouse Cloud


## shared\_merge\_tree\_leader\_update\_period\_seconds[​](#shared_merge_tree_leader_update_period_seconds "Direct link to shared_merge_tree_leader_update_period_seconds")




Maximum period to recheck leadership for parts update. Only available in
ClickHouse Cloud


## shared\_merge\_tree\_max\_outdated\_parts\_to\_process\_at\_once[​](#shared_merge_tree_max_outdated_parts_to_process_at_once "Direct link to shared_merge_tree_max_outdated_parts_to_process_at_once")




Maximum amount of outdated parts leader will try to confirm for removal at
one HTTP request. Only available in ClickHouse Cloud.


## shared\_merge\_tree\_max\_parts\_update\_backoff\_ms[​](#shared_merge_tree_max_parts_update_backoff_ms "Direct link to shared_merge_tree_max_parts_update_backoff_ms")




Max backoff for parts update. Only available in ClickHouse Cloud


## shared\_merge\_tree\_max\_parts\_update\_leaders\_in\_total[​](#shared_merge_tree_max_parts_update_leaders_in_total "Direct link to shared_merge_tree_max_parts_update_leaders_in_total")




Maximum number of parts update leaders. Only available in ClickHouse Cloud


## shared\_merge\_tree\_max\_parts\_update\_leaders\_per\_az[​](#shared_merge_tree_max_parts_update_leaders_per_az "Direct link to shared_merge_tree_max_parts_update_leaders_per_az")




Maximum number of parts update leaders. Only available in ClickHouse Cloud


## shared\_merge\_tree\_max\_replicas\_for\_parts\_deletion[​](#shared_merge_tree_max_replicas_for_parts_deletion "Direct link to shared_merge_tree_max_replicas_for_parts_deletion")




Max replicas which will participate in parts deletion (killer thread). Only
available in ClickHouse Cloud


## shared\_merge\_tree\_max\_replicas\_to\_merge\_parts\_for\_each\_parts\_range[​](#shared_merge_tree_max_replicas_to_merge_parts_for_each_parts_range "Direct link to shared_merge_tree_max_replicas_to_merge_parts_for_each_parts_range")




Max replicas which will try to assign potentially conflicting merges (allow
to avoid redundant conflicts in merges assignment). 0 means disabled. Only
available in ClickHouse Cloud


## shared\_merge\_tree\_max\_suspicious\_broken\_parts[​](#shared_merge_tree_max_suspicious_broken_parts "Direct link to shared_merge_tree_max_suspicious_broken_parts")




Max broken parts for SMT, if more \- deny automatic detach.


## shared\_merge\_tree\_max\_suspicious\_broken\_parts\_bytes[​](#shared_merge_tree_max_suspicious_broken_parts_bytes "Direct link to shared_merge_tree_max_suspicious_broken_parts_bytes")




Max size of all broken parts for SMT, if more \- deny automatic detach.


## shared\_merge\_tree\_memo\_ids\_remove\_timeout\_seconds[​](#shared_merge_tree_memo_ids_remove_timeout_seconds "Direct link to shared_merge_tree_memo_ids_remove_timeout_seconds")




How long we store insert memoization ids to avoid wrong actions during
insert retries. Only available in ClickHouse Cloud


## shared\_merge\_tree\_merge\_coordinator\_election\_check\_period\_ms[​](#shared_merge_tree_merge_coordinator_election_check_period_ms "Direct link to shared_merge_tree_merge_coordinator_election_check_period_ms")




Time between runs of merge coordinator election thread


## shared\_merge\_tree\_merge\_coordinator\_factor[​](#shared_merge_tree_merge_coordinator_factor "Direct link to shared_merge_tree_merge_coordinator_factor")




Time changing factor for delay of coordinator thread


## shared\_merge\_tree\_merge\_coordinator\_fetch\_fresh\_metadata\_period\_ms[​](#shared_merge_tree_merge_coordinator_fetch_fresh_metadata_period_ms "Direct link to shared_merge_tree_merge_coordinator_fetch_fresh_metadata_period_ms")




How often merge coordinator should sync with zookeeper to take fresh metadata


## shared\_merge\_tree\_merge\_coordinator\_max\_merge\_request\_size[​](#shared_merge_tree_merge_coordinator_max_merge_request_size "Direct link to shared_merge_tree_merge_coordinator_max_merge_request_size")




Number of merges that coordinator can request from MergerMutator at once


## shared\_merge\_tree\_merge\_coordinator\_max\_period\_ms[​](#shared_merge_tree_merge_coordinator_max_period_ms "Direct link to shared_merge_tree_merge_coordinator_max_period_ms")




Maximum time between runs of merge coordinator thread


## shared\_merge\_tree\_merge\_coordinator\_merges\_prepare\_count[​](#shared_merge_tree_merge_coordinator_merges_prepare_count "Direct link to shared_merge_tree_merge_coordinator_merges_prepare_count")




Number of merge entries that coordinator should prepare and distribute across workers.
When set to 'auto', equals the max number of merge tasks allowed on a single replica multiplied by the number of active replicas.


## shared\_merge\_tree\_merge\_coordinator\_min\_period\_ms[​](#shared_merge_tree_merge_coordinator_min_period_ms "Direct link to shared_merge_tree_merge_coordinator_min_period_ms")




Minimum time between runs of merge coordinator thread


## shared\_merge\_tree\_merge\_worker\_fast\_timeout\_ms[​](#shared_merge_tree_merge_worker_fast_timeout_ms "Direct link to shared_merge_tree_merge_worker_fast_timeout_ms")




Timeout that merge worker thread will use if it is needed to update it's state after immediate action


## shared\_merge\_tree\_merge\_worker\_regular\_timeout\_ms[​](#shared_merge_tree_merge_worker_regular_timeout_ms "Direct link to shared_merge_tree_merge_worker_regular_timeout_ms")




Time between runs of merge worker thread


## shared\_merge\_tree\_outdated\_parts\_group\_size[​](#shared_merge_tree_outdated_parts_group_size "Direct link to shared_merge_tree_outdated_parts_group_size")




How many replicas will be in the same rendezvous hash group for outdated parts cleanup.
Only available in ClickHouse Cloud.


## shared\_merge\_tree\_partitions\_hint\_ratio\_to\_reload\_merge\_pred\_for\_mutations[​](#shared_merge_tree_partitions_hint_ratio_to_reload_merge_pred_for_mutations "Direct link to shared_merge_tree_partitions_hint_ratio_to_reload_merge_pred_for_mutations")



Will reload merge predicate in merge/mutate selecting task when `<candidate partitions for mutations only (partitions that cannot be merged)>/<candidate partitions for mutations>` ratio is higher than the setting. Only available
in ClickHouse Cloud


## shared\_merge\_tree\_parts\_load\_batch\_size[​](#shared_merge_tree_parts_load_batch_size "Direct link to shared_merge_tree_parts_load_batch_size")



Amount of fetch parts metadata jobs to schedule at once. Only available in
ClickHouse Cloud


## shared\_merge\_tree\_postpone\_next\_merge\_for\_locally\_merged\_parts\_ms[​](#shared_merge_tree_postpone_next_merge_for_locally_merged_parts_ms "Direct link to shared_merge_tree_postpone_next_merge_for_locally_merged_parts_ms")




Time to keep a locally merged part without starting a new merge containing
this part. Gives other replicas a chance fetch the part and start this merge.
Only available in ClickHouse Cloud.


## shared\_merge\_tree\_postpone\_next\_merge\_for\_locally\_merged\_parts\_rows\_threshold[​](#shared_merge_tree_postpone_next_merge_for_locally_merged_parts_rows_threshold "Direct link to shared_merge_tree_postpone_next_merge_for_locally_merged_parts_rows_threshold")




Minimum size of part (in rows) to postpone assigning a next merge just after
merging it locally. Only available in ClickHouse Cloud.


## shared\_merge\_tree\_range\_for\_merge\_window\_size[​](#shared_merge_tree_range_for_merge_window_size "Direct link to shared_merge_tree_range_for_merge_window_size")




Time to keep a locally merged part without starting a new merge containing
this part. Gives other replicas a chance fetch the part and start this merge.
Only available in ClickHouse Cloud


## shared\_merge\_tree\_read\_virtual\_parts\_from\_leader[​](#shared_merge_tree_read_virtual_parts_from_leader "Direct link to shared_merge_tree_read_virtual_parts_from_leader")




Read virtual parts from leader when possible. Only available in ClickHouse
Cloud


## shared\_merge\_tree\_replica\_set\_max\_lifetime\_seconds[​](#shared_merge_tree_replica_set_max_lifetime_seconds "Direct link to shared_merge_tree_replica_set_max_lifetime_seconds")




How often replicas will try to update replica set in background. Next run is jittered
uniformly in \[0, value] seconds. Exception: value \= 0 does not follow that contract;
the implementation applies a minimum of 200 ms, so the next run is jittered in \[0, 200] ms.


## shared\_merge\_tree\_try\_fetch\_part\_in\_memory\_data\_from\_replicas[​](#shared_merge_tree_try_fetch_part_in_memory_data_from_replicas "Direct link to shared_merge_tree_try_fetch_part_in_memory_data_from_replicas")




If enabled all the replicas try to fetch part in memory data (like primary
key, partition info and so on) from other replicas where it already exists.


## shared\_merge\_tree\_update\_replica\_flags\_delay\_ms[​](#shared_merge_tree_update_replica_flags_delay_ms "Direct link to shared_merge_tree_update_replica_flags_delay_ms")




How often replica will try to reload it's flags according to background schedule.


## shared\_merge\_tree\_use\_metadata\_hints\_cache[​](#shared_merge_tree_use_metadata_hints_cache "Direct link to shared_merge_tree_use_metadata_hints_cache")




Enables requesting FS cache hints from in\-memory
cache on other replicas. Only available in ClickHouse Cloud


## shared\_merge\_tree\_use\_outdated\_parts\_compact\_format[​](#shared_merge_tree_use_outdated_parts_compact_format "Direct link to shared_merge_tree_use_outdated_parts_compact_format")




Use compact format for outdated parts: reduces load to Keeper, improves
outdated parts processing. Only available in ClickHouse Cloud


## shared\_merge\_tree\_use\_too\_many\_parts\_count\_from\_virtual\_parts[​](#shared_merge_tree_use_too_many_parts_count_from_virtual_parts "Direct link to shared_merge_tree_use_too_many_parts_count_from_virtual_parts")




If enabled too many parts counter will rely on shared data in Keeper, not on
local replica state. Only available in ClickHouse Cloud


## shared\_merge\_tree\_use\_zookeeper\_connection\_pool[​](#shared_merge_tree_use_zookeeper_connection_pool "Direct link to shared_merge_tree_use_zookeeper_connection_pool")




If enabled, SharedMergeTree uses one of server\-level pooled ZooKeeper sessions.


## shared\_merge\_tree\_virtual\_parts\_discovery\_batch[​](#shared_merge_tree_virtual_parts_discovery_batch "Direct link to shared_merge_tree_virtual_parts_discovery_batch")


Experimental feature. [Learn more.](/docs/beta-and-experimental-features#experimental-features)


How many partition discoveries should be packed into batch


## simultaneous\_parts\_removal\_limit[​](#simultaneous_parts_removal_limit "Direct link to simultaneous_parts_removal_limit")



If there are a lot of outdated parts cleanup thread will try to delete up to
`simultaneous_parts_removal_limit` parts during one iteration.
`simultaneous_parts_removal_limit` set to `0` means unlimited.


## sleep\_before\_commit\_local\_part\_in\_replicated\_table\_ms[​](#sleep_before_commit_local_part_in_replicated_table_ms "Direct link to sleep_before_commit_local_part_in_replicated_table_ms")



For testing. Do not change it.


## sleep\_before\_loading\_outdated\_parts\_ms[​](#sleep_before_loading_outdated_parts_ms "Direct link to sleep_before_loading_outdated_parts_ms")



For testing. Do not change it.


## storage\_policy[​](#storage_policy "Direct link to storage_policy")



Name of storage disk policy


## string\_serialization\_version[​](#string_serialization_version "Direct link to string_serialization_version")




Controls the serialization format for top\-level `String` columns.


This setting is only effective when `serialization_info_version` is set to "with\_types".
When set to `with_size_stream`, top\-level `String` columns are serialized with a separate
`.size` subcolumn storing string lengths, rather than inline. This allows real `.size`
subcolumns and can improve compression efficiency.


Nested `String` types (e.g., inside `Nullable`, `LowCardinality`, `Array`, or `Map`)
are not affected, except when they appear in a `Tuple`.


Possible values:


- `single_stream` — Use the standard serialization format with inline sizes.
- `with_size_stream` — Use a separate size stream for top\-level `String` columns.


## table\_disk[​](#table_disk "Direct link to table_disk")




This is table disk, the path/endpoint should point to the table data, not to
the database data. Can be set only for s3\_plain/s3\_plain\_rewritable/web.


## table\_readonly[​](#table_readonly "Direct link to table_readonly")




If set to true, the table is in read\-only mode. Any attempts to insert data or modify the table will fail.


## temporary\_directories\_lifetime[​](#temporary_directories_lifetime "Direct link to temporary_directories_lifetime")



How many seconds to keep tmp\_\-directories. You should not lower this value
because merges and mutations may not be able to work with low value of this
setting.


## try\_fetch\_recompressed\_part\_timeout[​](#try_fetch_recompressed_part_timeout "Direct link to try_fetch_recompressed_part_timeout")



Timeout (in seconds) before starting merge with recompression. During this
time ClickHouse tries to fetch recompressed part from replica which assigned
this merge with recompression.


Recompression works slow in most cases, so we don't start merge with
recompression until this timeout and trying to fetch recompressed part from
replica which assigned this merge with recompression.


Possible values:


- Any positive integer.


## ttl\_only\_drop\_parts[​](#ttl_only_drop_parts "Direct link to ttl_only_drop_parts")



Controls whether data parts are fully dropped in MergeTree tables when all
rows in that part have expired according to their `TTL` settings.


When `ttl_only_drop_parts` is disabled (by default), only the rows that have
expired based on their TTL settings are removed.


When `ttl_only_drop_parts` is enabled, the entire part is dropped if all
rows in that part have expired according to their `TTL` settings.


## use\_adaptive\_write\_buffer\_for\_dynamic\_subcolumns[​](#use_adaptive_write_buffer_for_dynamic_subcolumns "Direct link to use_adaptive_write_buffer_for_dynamic_subcolumns")



Allow to use adaptive writer buffers during writing dynamic subcolumns to
reduce memory usage


## use\_async\_block\_ids\_cache[​](#use_async_block_ids_cache "Direct link to use_async_block_ids_cache")



If true, we cache the hash sums of the async inserts.


Possible values:


- `true`
- `false`


A block bearing multiple async inserts will generate multiple hash sums.
When some of the inserts are duplicated, keeper will only return one
duplicated hash sum in one RPC, which will cause unnecessary RPC retries.
This cache will watch the hash sums path in Keeper. If updates are watched
in the Keeper, the cache will update as soon as possible, so that we are
able to filter the duplicated inserts in the memory.


## use\_compact\_variant\_discriminators\_serialization[​](#use_compact_variant_discriminators_serialization "Direct link to use_compact_variant_discriminators_serialization")



Enables compact mode for binary serialization of discriminators in Variant
data type.
This mode allows to use significantly less memory for storing discriminators
in parts when there is mostly one variant or a lot of NULL values.


## use\_const\_adaptive\_granularity[​](#use_const_adaptive_granularity "Direct link to use_const_adaptive_granularity")



Always use constant granularity for whole part. It allows to compress in
memory values of index granularity. It can be useful in extremely large
workloads with thin tables.


## use\_metadata\_cache[​](#use_metadata_cache "Direct link to use_metadata_cache")



Obsolete setting, does nothing.


## use\_minimalistic\_checksums\_in\_zookeeper[​](#use_minimalistic_checksums_in_zookeeper "Direct link to use_minimalistic_checksums_in_zookeeper")



Use small format (dozens bytes) for part checksums in ZooKeeper instead of
ordinary ones (dozens KB). Before enabling check that all replicas support
new format.


## use\_minimalistic\_part\_header\_in\_zookeeper[​](#use_minimalistic_part_header_in_zookeeper "Direct link to use_minimalistic_part_header_in_zookeeper")



Storage method of the data parts headers in ZooKeeper. If enabled, ZooKeeper
stores less data. For details, see [here](/docs/operations/server-configuration-parameters/settings#use_minimalistic_part_header_in_zookeeper).


## use\_primary\_key\_cache[​](#use_primary_key_cache "Direct link to use_primary_key_cache")




Use cache for primary index
instead of saving all indexes in memory. Can be useful for very large tables


## vertical\_merge\_algorithm\_min\_bytes\_to\_activate[​](#vertical_merge_algorithm_min_bytes_to_activate "Direct link to vertical_merge_algorithm_min_bytes_to_activate")



Minimal (approximate) uncompressed size in bytes in merging parts to activate
Vertical merge algorithm.


## vertical\_merge\_algorithm\_min\_columns\_to\_activate[​](#vertical_merge_algorithm_min_columns_to_activate "Direct link to vertical_merge_algorithm_min_columns_to_activate")



Minimal amount of non\-PK columns to activate Vertical merge algorithm.


## vertical\_merge\_algorithm\_min\_rows\_to\_activate[​](#vertical_merge_algorithm_min_rows_to_activate "Direct link to vertical_merge_algorithm_min_rows_to_activate")



Minimal (approximate) sum of rows in
merging parts to activate Vertical merge algorithm.


## vertical\_merge\_optimize\_lightweight\_delete[​](#vertical_merge_optimize_lightweight_delete "Direct link to vertical_merge_optimize_lightweight_delete")




If true, lightweight delete is optimized on vertical merge.


## vertical\_merge\_optimize\_ttl\_delete[​](#vertical_merge_optimize_ttl_delete "Direct link to vertical_merge_optimize_ttl_delete")




If true, rows TTL delete is optimized on vertical merge. Instead of forcing horizontal merge,
the TTL filter is evaluated and passed to the merging algorithm which sets skip flags in row sources.


## vertical\_merge\_remote\_filesystem\_prefetch[​](#vertical_merge_remote_filesystem_prefetch "Direct link to vertical_merge_remote_filesystem_prefetch")



If true prefetching of data from remote filesystem is used for the next
column during merge


## wait\_for\_unique\_parts\_send\_before\_shutdown\_ms[​](#wait_for_unique_parts_send_before_shutdown_ms "Direct link to wait_for_unique_parts_send_before_shutdown_ms")



Before shutdown table will wait for required amount time for unique parts
(exist only on current replica) to be fetched by other replicas (0 means
disabled).


## write\_ahead\_log\_bytes\_to\_fsync[​](#write_ahead_log_bytes_to_fsync "Direct link to write_ahead_log_bytes_to_fsync")



Obsolete setting, does nothing.


## write\_ahead\_log\_interval\_ms\_to\_fsync[​](#write_ahead_log_interval_ms_to_fsync "Direct link to write_ahead_log_interval_ms_to_fsync")



Obsolete setting, does nothing.


## write\_ahead\_log\_max\_bytes[​](#write_ahead_log_max_bytes "Direct link to write_ahead_log_max_bytes")



Obsolete setting, does nothing.


## write\_final\_mark[​](#write_final_mark "Direct link to write_final_mark")



Obsolete setting, does nothing.


## write\_marks\_for\_substreams\_in\_compact\_parts[​](#write_marks_for_substreams_in_compact_parts "Direct link to write_marks_for_substreams_in_compact_parts")




Enables writing marks per each substream instead of per each column in Compact parts.
It allows to read individual subcolumns from the data part efficiently.


For example, column `t Tuple(a String, b UInt32, c Array(Nullable(UInt32)))` is serialized in the next substreams:


- `t.a` for String data of tuple element `a`
- `t.b` for UInt32 data of tuple element `b`
- `t.c.size0` for array sizes of tuple element `c`
- `t.c.null` for null map of nested array elements of tuple element `c`
- `t.c` for UInt32 data pf nested array elements of tuple element `c`


When this setting is enabled, we will write a mark for each of these 5 substreams, which means that we will be able to read
the data of each individual substream from the granule separately if needed. For example, if we want to read the subcolumn `t.c` we will read only data of
substreams `t.c.size0`, `t.c.null` and `t.c` and won't read data from substreams `t.a` and `t.b`. When this setting is disabled,
we will write a mark only for top\-level column `t`, which means that we will always read the whole column data from the granule, even if we need only data of some substreams.


## zero\_copy\_concurrent\_part\_removal\_max\_postpone\_ratio[​](#zero_copy_concurrent_part_removal_max_postpone_ratio "Direct link to zero_copy_concurrent_part_removal_max_postpone_ratio")



Max percentage of top level parts to postpone removal in order to get
smaller independent ranges. Recommended not to change.


## zero\_copy\_concurrent\_part\_removal\_max\_split\_times[​](#zero_copy_concurrent_part_removal_max_split_times "Direct link to zero_copy_concurrent_part_removal_max_split_times")



Max recursion depth for splitting independent Outdated parts ranges into
smaller subranges. Recommended not to change.


## zero\_copy\_merge\_mutation\_min\_parts\_size\_sleep\_before\_lock[​](#zero_copy_merge_mutation_min_parts_size_sleep_before_lock "Direct link to zero_copy_merge_mutation_min_parts_size_sleep_before_lock")



If zero copy replication is enabled sleep random amount of time before trying
to lock depending on parts size for merge or mutation


## zero\_copy\_merge\_mutation\_min\_parts\_size\_sleep\_no\_scale\_before\_lock[​](#zero_copy_merge_mutation_min_parts_size_sleep_no_scale_before_lock "Direct link to zero_copy_merge_mutation_min_parts_size_sleep_no_scale_before_lock")




If zero copy replication is enabled sleep random amount of time up to 500ms
before trying to lock for merge or mutation.


## zookeeper\_session\_expiration\_check\_period[​](#zookeeper_session_expiration_check_period "Direct link to zookeeper_session_expiration_check_period")



ZooKeeper session expiration check period, in seconds.


Possible values:


- Any positive integer.
[PreviousSession Settings](/docs/operations/settings/settings)[NextFormat Settings](/docs/operations/settings/formats)- [MergeTree settings](#mergetree-settings)- [adaptive\_write\_buffer\_initial\_size](#adaptive_write_buffer_initial_size)- [add\_implicit\_sign\_column\_constraint\_for\_collapsing\_engine](#add_implicit_sign_column_constraint_for_collapsing_engine)- [add\_minmax\_index\_for\_block\_number\_column](#add_minmax_index_for_block_number_column)- [add\_minmax\_index\_for\_block\_offset\_column](#add_minmax_index_for_block_offset_column)- [add\_minmax\_index\_for\_numeric\_columns](#add_minmax_index_for_numeric_columns)- [add\_minmax\_index\_for\_string\_columns](#add_minmax_index_for_string_columns)- [add\_minmax\_index\_for\_temporal\_columns](#add_minmax_index_for_temporal_columns)- [allow\_coalescing\_columns\_in\_partition\_or\_order\_key](#allow_coalescing_columns_in_partition_or_order_key)- [allow\_commit\_order\_projection](#allow_commit_order_projection)- [allow\_experimental\_replacing\_merge\_with\_cleanup](#allow_experimental_replacing_merge_with_cleanup)- [allow\_experimental\_reverse\_key](#allow_experimental_reverse_key)- [allow\_floating\_point\_partition\_key](#allow_floating_point_partition_key)- [allow\_nullable\_key](#allow_nullable_key)- [allow\_part\_offset\_column\_in\_projections](#allow_part_offset_column_in_projections)- [allow\_reduce\_blocking\_parts\_task](#allow_reduce_blocking_parts_task)- [allow\_remote\_fs\_zero\_copy\_replication](#allow_remote_fs_zero_copy_replication)- [allow\_summing\_columns\_in\_partition\_or\_order\_key](#allow_summing_columns_in_partition_or_order_key)- [allow\_suspicious\_indices](#allow_suspicious_indices)- [allow\_vertical\_merges\_from\_compact\_to\_wide\_parts](#allow_vertical_merges_from_compact_to_wide_parts)- [alter\_column\_secondary\_index\_mode](#alter_column_secondary_index_mode)- [always\_fetch\_merged\_part](#always_fetch_merged_part)- [always\_use\_copy\_instead\_of\_hardlinks](#always_use_copy_instead_of_hardlinks)- [apply\_patches\_on\_merge](#apply_patches_on_merge)- [assign\_part\_uuids](#assign_part_uuids)- [async\_block\_ids\_cache\_update\_wait\_ms](#async_block_ids_cache_update_wait_ms)- [async\_insert](#async_insert)- [auto\_statistics\_types](#auto_statistics_types)- [background\_task\_preferred\_step\_execution\_time\_ms](#background_task_preferred_step_execution_time_ms)- [cache\_populated\_by\_fetch](#cache_populated_by_fetch)- [cache\_populated\_by\_fetch\_filename\_regexp](#cache_populated_by_fetch_filename_regexp)- [check\_delay\_period](#check_delay_period)- [check\_sample\_column\_is\_correct](#check_sample_column_is_correct)- [clean\_deleted\_rows](#clean_deleted_rows)- [cleanup\_delay\_period](#cleanup_delay_period)- [cleanup\_delay\_period\_random\_add](#cleanup_delay_period_random_add)- [cleanup\_thread\_preferred\_points\_per\_iteration](#cleanup_thread_preferred_points_per_iteration)- [cleanup\_threads](#cleanup_threads)- [clone\_replica\_zookeeper\_create\_get\_part\_batch\_size](#clone_replica_zookeeper_create_get_part_batch_size)- [columns\_and\_secondary\_indices\_sizes\_lazy\_calculation](#columns_and_secondary_indices_sizes_lazy_calculation)- [columns\_to\_prewarm\_mark\_cache](#columns_to_prewarm_mark_cache)- [compact\_parts\_max\_bytes\_to\_buffer](#compact_parts_max_bytes_to_buffer)- [compact\_parts\_max\_granules\_to\_buffer](#compact_parts_max_granules_to_buffer)- [compact\_parts\_merge\_max\_bytes\_to\_prefetch\_part](#compact_parts_merge_max_bytes_to_prefetch_part)- [compatibility\_allow\_sampling\_expression\_not\_in\_primary\_key](#compatibility_allow_sampling_expression_not_in_primary_key)- [compress\_marks](#compress_marks)- [compress\_per\_column\_in\_compact\_parts](#compress_per_column_in_compact_parts)- [compress\_primary\_key](#compress_primary_key)- [concurrent\_part\_removal\_threshold](#concurrent_part_removal_threshold)- [concurrent\_part\_removal\_threshold\_for\_remote\_disk](#concurrent_part_removal_threshold_for_remote_disk)- [deduplicate\_merge\_projection\_mode](#deduplicate_merge_projection_mode)- [default\_compression\_codec](#default_compression_codec)- [detach\_not\_byte\_identical\_parts](#detach_not_byte_identical_parts)- [detach\_old\_local\_parts\_when\_cloning\_replica](#detach_old_local_parts_when_cloning_replica)- [disable\_detach\_partition\_for\_zero\_copy\_replication](#disable_detach_partition_for_zero_copy_replication)- [disable\_fetch\_partition\_for\_zero\_copy\_replication](#disable_fetch_partition_for_zero_copy_replication)- [disable\_freeze\_partition\_for\_zero\_copy\_replication](#disable_freeze_partition_for_zero_copy_replication)- [disk](#disk)- [distributed\_index\_analysis\_min\_indexes\_bytes\_to\_activate](#distributed_index_analysis_min_indexes_bytes_to_activate)- [distributed\_index\_analysis\_min\_parts\_to\_activate](#distributed_index_analysis_min_parts_to_activate)- [dynamic\_serialization\_version](#dynamic_serialization_version)- [enable\_block\_number\_column](#enable_block_number_column)- [enable\_block\_offset\_column](#enable_block_offset_column)- [enable\_index\_granularity\_compression](#enable_index_granularity_compression)- [enable\_max\_bytes\_limit\_for\_min\_age\_to\_force\_merge](#enable_max_bytes_limit_for_min_age_to_force_merge)- [enable\_mixed\_granularity\_parts](#enable_mixed_granularity_parts)- [enable\_replacing\_merge\_with\_cleanup\_for\_min\_age\_to\_force\_merge](#enable_replacing_merge_with_cleanup_for_min_age_to_force_merge)- [enable\_the\_endpoint\_id\_with\_zookeeper\_name\_prefix](#enable_the_endpoint_id_with_zookeeper_name_prefix)- [enable\_vertical\_merge\_algorithm](#enable_vertical_merge_algorithm)- [enforce\_index\_structure\_match\_on\_partition\_manipulation](#enforce_index_structure_match_on_partition_manipulation)- [escape\_index\_filenames](#escape_index_filenames)- [escape\_variant\_subcolumn\_filenames](#escape_variant_subcolumn_filenames)- [exclude\_deleted\_rows\_for\_part\_size\_in\_merge](#exclude_deleted_rows_for_part_size_in_merge)- [exclude\_materialize\_skip\_indexes\_on\_merge](#exclude_materialize_skip_indexes_on_merge)- [execute\_merges\_on\_single\_replica\_time\_threshold](#execute_merges_on_single_replica_time_threshold)- [fault\_probability\_after\_part\_commit](#fault_probability_after_part_commit)- [fault\_probability\_before\_part\_commit](#fault_probability_before_part_commit)- [finished\_mutations\_to\_keep](#finished_mutations_to_keep)- [force\_read\_through\_cache\_for\_merges](#force_read_through_cache_for_merges)- [fsync\_after\_insert](#fsync_after_insert)- [fsync\_part\_directory](#fsync_part_directory)- [in\_memory\_parts\_enable\_wal](#in_memory_parts_enable_wal)- [in\_memory\_parts\_insert\_sync](#in_memory_parts_insert_sync)- [inactive\_parts\_to\_delay\_insert](#inactive_parts_to_delay_insert)- [inactive\_parts\_to\_throw\_insert](#inactive_parts_to_throw_insert)- [index\_granularity](#index_granularity)- [index\_granularity\_bytes](#index_granularity_bytes)- [initialization\_retry\_period](#initialization_retry_period)- [kill\_delay\_period](#kill_delay_period)- [kill\_delay\_period\_random\_add](#kill_delay_period_random_add)- [kill\_threads](#kill_threads)- [lightweight\_mutation\_projection\_mode](#lightweight_mutation_projection_mode)- [load\_existing\_rows\_count\_for\_old\_parts](#load_existing_rows_count_for_old_parts)- [lock\_acquire\_timeout\_for\_background\_operations](#lock_acquire_timeout_for_background_operations)- [map\_buckets\_coefficient](#map_buckets_coefficient)- [map\_buckets\_min\_avg\_size](#map_buckets_min_avg_size)- [map\_buckets\_strategy](#map_buckets_strategy)- [map\_serialization\_version](#map_serialization_version)- [map\_serialization\_version\_for\_zero\_level\_parts](#map_serialization_version_for_zero_level_parts)- [marks\_compress\_block\_size](#marks_compress_block_size)- [marks\_compression\_codec](#marks_compression_codec)- [materialize\_skip\_indexes\_on\_merge](#materialize_skip_indexes_on_merge)- [materialize\_statistics\_on\_merge](#materialize_statistics_on_merge)- [materialize\_ttl\_recalculate\_only](#materialize_ttl_recalculate_only)- [max\_avg\_part\_size\_for\_too\_many\_parts](#max_avg_part_size_for_too_many_parts)- [max\_buckets\_in\_map](#max_buckets_in_map)- [max\_bytes\_to\_merge\_at\_max\_space\_in\_pool](#max_bytes_to_merge_at_max_space_in_pool)- [max\_bytes\_to\_merge\_at\_min\_space\_in\_pool](#max_bytes_to_merge_at_min_space_in_pool)- [max\_cleanup\_delay\_period](#max_cleanup_delay_period)- [max\_compress\_block\_size](#max_compress_block_size)- [max\_concurrent\_queries](#max_concurrent_queries)- [max\_delay\_to\_insert](#max_delay_to_insert)- [max\_delay\_to\_mutate\_ms](#max_delay_to_mutate_ms)- [max\_digestion\_size\_per\_segment](#max_digestion_size_per_segment)- [max\_file\_name\_length](#max_file_name_length)- [max\_files\_to\_modify\_in\_alter\_columns](#max_files_to_modify_in_alter_columns)- [max\_files\_to\_remove\_in\_alter\_columns](#max_files_to_remove_in_alter_columns)- [max\_merge\_delayed\_streams\_for\_parallel\_write](#max_merge_delayed_streams_for_parallel_write)- [max\_merge\_selecting\_sleep\_ms](#max_merge_selecting_sleep_ms)- [max\_number\_of\_merges\_with\_ttl\_in\_pool](#max_number_of_merges_with_ttl_in_pool)- [max\_number\_of\_mutations\_for\_replica](#max_number_of_mutations_for_replica)- [max\_part\_loading\_threads](#max_part_loading_threads)- [max\_part\_removal\_threads](#max_part_removal_threads)- [max\_partitions\_to\_read](#max_partitions_to_read)- [max\_parts\_in\_total](#max_parts_in_total)- [max\_parts\_to\_merge\_at\_once](#max_parts_to_merge_at_once)- [max\_postpone\_time\_for\_failed\_mutations\_ms](#max_postpone_time_for_failed_mutations_ms)- [max\_postpone\_time\_for\_failed\_replicated\_fetches\_ms](#max_postpone_time_for_failed_replicated_fetches_ms)- [max\_postpone\_time\_for\_failed\_replicated\_merges\_ms](#max_postpone_time_for_failed_replicated_merges_ms)- [max\_postpone\_time\_for\_failed\_replicated\_tasks\_ms](#max_postpone_time_for_failed_replicated_tasks_ms)- [max\_projections](#max_projections)- [max\_replicated\_fetches\_network\_bandwidth](#max_replicated_fetches_network_bandwidth)- [max\_replicated\_logs\_to\_keep](#max_replicated_logs_to_keep)- [max\_replicated\_merges\_in\_queue](#max_replicated_merges_in_queue)- [max\_replicated\_merges\_with\_ttl\_in\_queue](#max_replicated_merges_with_ttl_in_queue)- [max\_replicated\_mutations\_in\_queue](#max_replicated_mutations_in_queue)- [max\_replicated\_sends\_network\_bandwidth](#max_replicated_sends_network_bandwidth)- [max\_suspicious\_broken\_parts](#max_suspicious_broken_parts)- [max\_suspicious\_broken\_parts\_bytes](#max_suspicious_broken_parts_bytes)- [max\_uncompressed\_bytes\_in\_patches](#max_uncompressed_bytes_in_patches)- [merge\_max\_block\_size](#merge_max_block_size)- [merge\_max\_block\_size\_bytes](#merge_max_block_size_bytes)- [merge\_max\_bytes\_to\_prewarm\_cache](#merge_max_bytes_to_prewarm_cache)- [merge\_max\_dynamic\_subcolumns\_in\_compact\_part](#merge_max_dynamic_subcolumns_in_compact_part)- [merge\_max\_dynamic\_subcolumns\_in\_wide\_part](#merge_max_dynamic_subcolumns_in_wide_part)- [merge\_selecting\_sleep\_ms](#merge_selecting_sleep_ms)- [merge\_selecting\_sleep\_slowdown\_factor](#merge_selecting_sleep_slowdown_factor)- [merge\_selector\_algorithm](#merge_selector_algorithm)- [merge\_selector\_base](#merge_selector_base)- [merge\_selector\_blurry\_base\_scale\_factor](#merge_selector_blurry_base_scale_factor)- [merge\_selector\_enable\_heuristic\_to\_lower\_max\_parts\_to\_merge\_at\_once](#merge_selector_enable_heuristic_to_lower_max_parts_to_merge_at_once)- [merge\_selector\_enable\_heuristic\_to\_remove\_small\_parts\_at\_right](#merge_selector_enable_heuristic_to_remove_small_parts_at_right)- [merge\_selector\_heuristic\_to\_lower\_max\_parts\_to\_merge\_at\_once\_exponent](#merge_selector_heuristic_to_lower_max_parts_to_merge_at_once_exponent)- [merge\_selector\_window\_size](#merge_selector_window_size)- [merge\_total\_max\_bytes\_to\_prewarm\_cache](#merge_total_max_bytes_to_prewarm_cache)- [merge\_tree\_clear\_old\_broken\_detached\_parts\_ttl\_timeout\_seconds](#merge_tree_clear_old_broken_detached_parts_ttl_timeout_seconds)- [merge\_tree\_clear\_old\_parts\_interval\_seconds](#merge_tree_clear_old_parts_interval_seconds)- [merge\_tree\_clear\_old\_temporary\_directories\_interval\_seconds](#merge_tree_clear_old_temporary_directories_interval_seconds)- [merge\_tree\_enable\_clear\_old\_broken\_detached](#merge_tree_enable_clear_old_broken_detached)- [merge\_with\_recompression\_ttl\_timeout](#merge_with_recompression_ttl_timeout)- [merge\_with\_ttl\_timeout](#merge_with_ttl_timeout)- [merge\_workload](#merge_workload)- [min\_absolute\_delay\_to\_close](#min_absolute_delay_to_close)- [min\_age\_to\_force\_merge\_on\_partition\_only](#min_age_to_force_merge_on_partition_only)- [min\_age\_to\_force\_merge\_seconds](#min_age_to_force_merge_seconds)- [min\_bytes\_for\_compact\_part](#min_bytes_for_compact_part)- [min\_bytes\_for\_full\_part\_storage](#min_bytes_for_full_part_storage)- [min\_bytes\_for\_wide\_part](#min_bytes_for_wide_part)- [min\_bytes\_to\_prewarm\_caches](#min_bytes_to_prewarm_caches)- [min\_bytes\_to\_rebalance\_partition\_over\_jbod](#min_bytes_to_rebalance_partition_over_jbod)- [min\_columns\_to\_activate\_adaptive\_write\_buffer](#min_columns_to_activate_adaptive_write_buffer)- [min\_compress\_block\_size](#min_compress_block_size)- [min\_compressed\_bytes\_to\_fsync\_after\_fetch](#min_compressed_bytes_to_fsync_after_fetch)- [min\_compressed\_bytes\_to\_fsync\_after\_merge](#min_compressed_bytes_to_fsync_after_merge)- [min\_delay\_to\_insert\_ms](#min_delay_to_insert_ms)- [min\_delay\_to\_mutate\_ms](#min_delay_to_mutate_ms)- [min\_free\_disk\_bytes\_to\_perform\_insert](#min_free_disk_bytes_to_perform_insert)- [min\_free\_disk\_ratio\_to\_perform\_insert](#min_free_disk_ratio_to_perform_insert)- [min\_index\_granularity\_bytes](#min_index_granularity_bytes)- [min\_level\_for\_full\_part\_storage](#min_level_for_full_part_storage)- [min\_level\_for\_wide\_part](#min_level_for_wide_part)- [min\_marks\_to\_honor\_max\_concurrent\_queries](#min_marks_to_honor_max_concurrent_queries)- [min\_merge\_bytes\_to\_use\_direct\_io](#min_merge_bytes_to_use_direct_io)- [min\_parts\_to\_merge\_at\_once](#min_parts_to_merge_at_once)- [min\_relative\_delay\_to\_close](#min_relative_delay_to_close)- [min\_relative\_delay\_to\_measure](#min_relative_delay_to_measure)- [min\_relative\_delay\_to\_yield\_leadership](#min_relative_delay_to_yield_leadership)- [min\_replicated\_logs\_to\_keep](#min_replicated_logs_to_keep)- [min\_rows\_for\_compact\_part](#min_rows_for_compact_part)- [min\_rows\_for\_full\_part\_storage](#min_rows_for_full_part_storage)- [min\_rows\_for\_wide\_part](#min_rows_for_wide_part)- [min\_rows\_to\_fsync\_after\_merge](#min_rows_to_fsync_after_merge)- [mutation\_workload](#mutation_workload)- [non\_replicated\_deduplication\_window](#non_replicated_deduplication_window)- [notify\_newest\_block\_number](#notify_newest_block_number)- [nullable\_serialization\_version](#nullable_serialization_version)- [number\_of\_free\_entries\_in\_pool\_to\_execute\_mutation](#number_of_free_entries_in_pool_to_execute_mutation)- [number\_of\_free\_entries\_in\_pool\_to\_execute\_optimize\_entire\_partition](#number_of_free_entries_in_pool_to_execute_optimize_entire_partition)- [number\_of\_free\_entries\_in\_pool\_to\_lower\_max\_size\_of\_merge](#number_of_free_entries_in_pool_to_lower_max_size_of_merge)- [number\_of\_mutations\_to\_delay](#number_of_mutations_to_delay)- [number\_of\_mutations\_to\_throw](#number_of_mutations_to_throw)- [number\_of\_partitions\_to\_consider\_for\_merge](#number_of_partitions_to_consider_for_merge)- [object\_serialization\_version](#object_serialization_version)- [object\_shared\_data\_buckets\_for\_compact\_part](#object_shared_data_buckets_for_compact_part)- [object\_shared\_data\_buckets\_for\_wide\_part](#object_shared_data_buckets_for_wide_part)- [object\_shared\_data\_serialization\_version](#object_shared_data_serialization_version)- [object\_shared\_data\_serialization\_version\_for\_zero\_level\_parts](#object_shared_data_serialization_version_for_zero_level_parts)- [old\_parts\_lifetime](#old_parts_lifetime)- [optimize\_row\_order](#optimize_row_order)- [part\_minmax\_index\_columns](#part_minmax_index_columns)- [part\_moves\_between\_shards\_delay\_seconds](#part_moves_between_shards_delay_seconds)- [part\_moves\_between\_shards\_enable](#part_moves_between_shards_enable)- [parts\_to\_delay\_insert](#parts_to_delay_insert)- [parts\_to\_throw\_insert](#parts_to_throw_insert)- [prefer\_fetch\_merged\_part\_size\_threshold](#prefer_fetch_merged_part_size_threshold)- [prefer\_fetch\_merged\_part\_time\_threshold](#prefer_fetch_merged_part_time_threshold)- [prewarm\_mark\_cache](#prewarm_mark_cache)- [prewarm\_primary\_key\_cache](#prewarm_primary_key_cache)- [primary\_key\_compress\_block\_size](#primary_key_compress_block_size)- [primary\_key\_compression\_codec](#primary_key_compression_codec)- [primary\_key\_lazy\_load](#primary_key_lazy_load)- [primary\_key\_ratio\_of\_unique\_prefix\_values\_to\_skip\_suffix\_columns](#primary_key_ratio_of_unique_prefix_values_to_skip_suffix_columns)- [propagate\_types\_serialization\_versions\_to\_nested\_types](#propagate_types_serialization_versions_to_nested_types)- [ratio\_of\_defaults\_for\_sparse\_serialization](#ratio_of_defaults_for_sparse_serialization)- [reduce\_blocking\_parts\_sleep\_ms](#reduce_blocking_parts_sleep_ms)- [refresh\_parts\_interval](#refresh_parts_interval)- [refresh\_statistics\_interval](#refresh_statistics_interval)- [remote\_fs\_execute\_merges\_on\_single\_replica\_time\_threshold](#remote_fs_execute_merges_on_single_replica_time_threshold)- [remote\_fs\_zero\_copy\_path\_compatible\_mode](#remote_fs_zero_copy_path_compatible_mode)- [remote\_fs\_zero\_copy\_zookeeper\_path](#remote_fs_zero_copy_zookeeper_path)- [remove\_empty\_parts](#remove_empty_parts)- [remove\_rolled\_back\_parts\_immediately](#remove_rolled_back_parts_immediately)- [remove\_unused\_patch\_parts](#remove_unused_patch_parts)- [replace\_long\_file\_name\_to\_hash](#replace_long_file_name_to_hash)- [replicated\_can\_become\_leader](#replicated_can_become_leader)- [replicated\_deduplication\_window](#replicated_deduplication_window)- [replicated\_deduplication\_window\_for\_async\_inserts](#replicated_deduplication_window_for_async_inserts)- [replicated\_deduplication\_window\_seconds](#replicated_deduplication_window_seconds)- [replicated\_deduplication\_window\_seconds\_for\_async\_inserts](#replicated_deduplication_window_seconds_for_async_inserts)- [replicated\_fetches\_http\_connection\_timeout](#replicated_fetches_http_connection_timeout)- [replicated\_fetches\_http\_receive\_timeout](#replicated_fetches_http_receive_timeout)- [replicated\_fetches\_http\_send\_timeout](#replicated_fetches_http_send_timeout)- [replicated\_fetches\_min\_part\_level](#replicated_fetches_min_part_level)- [replicated\_fetches\_min\_part\_level\_timeout\_seconds](#replicated_fetches_min_part_level_timeout_seconds)- [replicated\_max\_mutations\_in\_one\_entry](#replicated_max_mutations_in_one_entry)- [replicated\_max\_parallel\_fetches](#replicated_max_parallel_fetches)- [replicated\_max\_parallel\_fetches\_for\_host](#replicated_max_parallel_fetches_for_host)- [replicated\_max\_parallel\_fetches\_for\_table](#replicated_max_parallel_fetches_for_table)- [replicated\_max\_parallel\_sends](#replicated_max_parallel_sends)- [replicated\_max\_parallel\_sends\_for\_table](#replicated_max_parallel_sends_for_table)- [replicated\_max\_ratio\_of\_wrong\_parts](#replicated_max_ratio_of_wrong_parts)- [search\_orphaned\_parts\_disks](#search_orphaned_parts_disks)- [serialization\_info\_version](#serialization_info_version)- [share\_nested\_offsets](#share_nested_offsets)- [shared\_merge\_tree\_activate\_coordinated\_merges\_tasks](#shared_merge_tree_activate_coordinated_merges_tasks)- [shared\_merge\_tree\_create\_per\_replica\_metadata\_nodes](#shared_merge_tree_create_per_replica_metadata_nodes)- [shared\_merge\_tree\_disable\_merges\_and\_mutations\_assignment](#shared_merge_tree_disable_merges_and_mutations_assignment)- [shared\_merge\_tree\_empty\_partition\_lifetime](#shared_merge_tree_empty_partition_lifetime)- [shared\_merge\_tree\_enable\_automatic\_empty\_partitions\_cleanup](#shared_merge_tree_enable_automatic_empty_partitions_cleanup)- [shared\_merge\_tree\_enable\_coordinated\_merges](#shared_merge_tree_enable_coordinated_merges)- [shared\_merge\_tree\_enable\_keeper\_parts\_extra\_data](#shared_merge_tree_enable_keeper_parts_extra_data)- [shared\_merge\_tree\_enable\_outdated\_parts\_check](#shared_merge_tree_enable_outdated_parts_check)- [shared\_merge\_tree\_idle\_parts\_update\_seconds](#shared_merge_tree_idle_parts_update_seconds)- [shared\_merge\_tree\_initial\_parts\_update\_backoff\_ms](#shared_merge_tree_initial_parts_update_backoff_ms)- [shared\_merge\_tree\_interserver\_http\_connection\_timeout\_ms](#shared_merge_tree_interserver_http_connection_timeout_ms)- [shared\_merge\_tree\_interserver\_http\_timeout\_ms](#shared_merge_tree_interserver_http_timeout_ms)- [shared\_merge\_tree\_leader\_update\_period\_random\_add\_seconds](#shared_merge_tree_leader_update_period_random_add_seconds)- [shared\_merge\_tree\_leader\_update\_period\_seconds](#shared_merge_tree_leader_update_period_seconds)- [shared\_merge\_tree\_max\_outdated\_parts\_to\_process\_at\_once](#shared_merge_tree_max_outdated_parts_to_process_at_once)- [shared\_merge\_tree\_max\_parts\_update\_backoff\_ms](#shared_merge_tree_max_parts_update_backoff_ms)- [shared\_merge\_tree\_max\_parts\_update\_leaders\_in\_total](#shared_merge_tree_max_parts_update_leaders_in_total)- [shared\_merge\_tree\_max\_parts\_update\_leaders\_per\_az](#shared_merge_tree_max_parts_update_leaders_per_az)- [shared\_merge\_tree\_max\_replicas\_for\_parts\_deletion](#shared_merge_tree_max_replicas_for_parts_deletion)- [shared\_merge\_tree\_max\_replicas\_to\_merge\_parts\_for\_each\_parts\_range](#shared_merge_tree_max_replicas_to_merge_parts_for_each_parts_range)- [shared\_merge\_tree\_max\_suspicious\_broken\_parts](#shared_merge_tree_max_suspicious_broken_parts)- [shared\_merge\_tree\_max\_suspicious\_broken\_parts\_bytes](#shared_merge_tree_max_suspicious_broken_parts_bytes)- [shared\_merge\_tree\_memo\_ids\_remove\_timeout\_seconds](#shared_merge_tree_memo_ids_remove_timeout_seconds)- [shared\_merge\_tree\_merge\_coordinator\_election\_check\_period\_ms](#shared_merge_tree_merge_coordinator_election_check_period_ms)- [shared\_merge\_tree\_merge\_coordinator\_factor](#shared_merge_tree_merge_coordinator_factor)- [shared\_merge\_tree\_merge\_coordinator\_fetch\_fresh\_metadata\_period\_ms](#shared_merge_tree_merge_coordinator_fetch_fresh_metadata_period_ms)- [shared\_merge\_tree\_merge\_coordinator\_max\_merge\_request\_size](#shared_merge_tree_merge_coordinator_max_merge_request_size)- [shared\_merge\_tree\_merge\_coordinator\_max\_period\_ms](#shared_merge_tree_merge_coordinator_max_period_ms)- [shared\_merge\_tree\_merge\_coordinator\_merges\_prepare\_count](#shared_merge_tree_merge_coordinator_merges_prepare_count)- [shared\_merge\_tree\_merge\_coordinator\_min\_period\_ms](#shared_merge_tree_merge_coordinator_min_period_ms)- [shared\_merge\_tree\_merge\_worker\_fast\_timeout\_ms](#shared_merge_tree_merge_worker_fast_timeout_ms)- [shared\_merge\_tree\_merge\_worker\_regular\_timeout\_ms](#shared_merge_tree_merge_worker_regular_timeout_ms)- [shared\_merge\_tree\_outdated\_parts\_group\_size](#shared_merge_tree_outdated_parts_group_size)- [shared\_merge\_tree\_partitions\_hint\_ratio\_to\_reload\_merge\_pred\_for\_mutations](#shared_merge_tree_partitions_hint_ratio_to_reload_merge_pred_for_mutations)- [shared\_merge\_tree\_parts\_load\_batch\_size](#shared_merge_tree_parts_load_batch_size)- [shared\_merge\_tree\_postpone\_next\_merge\_for\_locally\_merged\_parts\_ms](#shared_merge_tree_postpone_next_merge_for_locally_merged_parts_ms)- [shared\_merge\_tree\_postpone\_next\_merge\_for\_locally\_merged\_parts\_rows\_threshold](#shared_merge_tree_postpone_next_merge_for_locally_merged_parts_rows_threshold)- [shared\_merge\_tree\_range\_for\_merge\_window\_size](#shared_merge_tree_range_for_merge_window_size)- [shared\_merge\_tree\_read\_virtual\_parts\_from\_leader](#shared_merge_tree_read_virtual_parts_from_leader)- [shared\_merge\_tree\_replica\_set\_max\_lifetime\_seconds](#shared_merge_tree_replica_set_max_lifetime_seconds)- [shared\_merge\_tree\_try\_fetch\_part\_in\_memory\_data\_from\_replicas](#shared_merge_tree_try_fetch_part_in_memory_data_from_replicas)- [shared\_merge\_tree\_update\_replica\_flags\_delay\_ms](#shared_merge_tree_update_replica_flags_delay_ms)- [shared\_merge\_tree\_use\_metadata\_hints\_cache](#shared_merge_tree_use_metadata_hints_cache)- [shared\_merge\_tree\_use\_outdated\_parts\_compact\_format](#shared_merge_tree_use_outdated_parts_compact_format)- [shared\_merge\_tree\_use\_too\_many\_parts\_count\_from\_virtual\_parts](#shared_merge_tree_use_too_many_parts_count_from_virtual_parts)- [shared\_merge\_tree\_use\_zookeeper\_connection\_pool](#shared_merge_tree_use_zookeeper_connection_pool)- [shared\_merge\_tree\_virtual\_parts\_discovery\_batch](#shared_merge_tree_virtual_parts_discovery_batch)- [simultaneous\_parts\_removal\_limit](#simultaneous_parts_removal_limit)- [sleep\_before\_commit\_local\_part\_in\_replicated\_table\_ms](#sleep_before_commit_local_part_in_replicated_table_ms)- [sleep\_before\_loading\_outdated\_parts\_ms](#sleep_before_loading_outdated_parts_ms)- [storage\_policy](#storage_policy)- [string\_serialization\_version](#string_serialization_version)- [table\_disk](#table_disk)- [table\_readonly](#table_readonly)- [temporary\_directories\_lifetime](#temporary_directories_lifetime)- [try\_fetch\_recompressed\_part\_timeout](#try_fetch_recompressed_part_timeout)- [ttl\_only\_drop\_parts](#ttl_only_drop_parts)- [use\_adaptive\_write\_buffer\_for\_dynamic\_subcolumns](#use_adaptive_write_buffer_for_dynamic_subcolumns)- [use\_async\_block\_ids\_cache](#use_async_block_ids_cache)- [use\_compact\_variant\_discriminators\_serialization](#use_compact_variant_discriminators_serialization)- [use\_const\_adaptive\_granularity](#use_const_adaptive_granularity)- [use\_metadata\_cache](#use_metadata_cache)- [use\_minimalistic\_checksums\_in\_zookeeper](#use_minimalistic_checksums_in_zookeeper)- [use\_minimalistic\_part\_header\_in\_zookeeper](#use_minimalistic_part_header_in_zookeeper)- [use\_primary\_key\_cache](#use_primary_key_cache)- [vertical\_merge\_algorithm\_min\_bytes\_to\_activate](#vertical_merge_algorithm_min_bytes_to_activate)- [vertical\_merge\_algorithm\_min\_columns\_to\_activate](#vertical_merge_algorithm_min_columns_to_activate)- [vertical\_merge\_algorithm\_min\_rows\_to\_activate](#vertical_merge_algorithm_min_rows_to_activate)- [vertical\_merge\_optimize\_lightweight\_delete](#vertical_merge_optimize_lightweight_delete)- [vertical\_merge\_optimize\_ttl\_delete](#vertical_merge_optimize_ttl_delete)- [vertical\_merge\_remote\_filesystem\_prefetch](#vertical_merge_remote_filesystem_prefetch)- [wait\_for\_unique\_parts\_send\_before\_shutdown\_ms](#wait_for_unique_parts_send_before_shutdown_ms)- [write\_ahead\_log\_bytes\_to\_fsync](#write_ahead_log_bytes_to_fsync)- [write\_ahead\_log\_interval\_ms\_to\_fsync](#write_ahead_log_interval_ms_to_fsync)- [write\_ahead\_log\_max\_bytes](#write_ahead_log_max_bytes)- [write\_final\_mark](#write_final_mark)- [write\_marks\_for\_substreams\_in\_compact\_parts](#write_marks_for_substreams_in_compact_parts)- [zero\_copy\_concurrent\_part\_removal\_max\_postpone\_ratio](#zero_copy_concurrent_part_removal_max_postpone_ratio)- [zero\_copy\_concurrent\_part\_removal\_max\_split\_times](#zero_copy_concurrent_part_removal_max_split_times)- [zero\_copy\_merge\_mutation\_min\_parts\_size\_sleep\_before\_lock](#zero_copy_merge_mutation_min_parts_size_sleep_before_lock)- [zero\_copy\_merge\_mutation\_min\_parts\_size\_sleep\_no\_scale\_before\_lock](#zero_copy_merge_mutation_min_parts_size_sleep_no_scale_before_lock)- [zookeeper\_session\_expiration\_check\_period](#zookeeper_session_expiration_check_period)
Was this page helpful?
