# System Tables and a Window into the Internals of ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Product](/blog?category=product)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# System Tables and a Window into the Internals of ClickHouse

![](/_next/image?url=%2Fuploads%2Fderek_chia_1e00192936.jpg&w=96&q=75)[Derek Chia](/authors/derek-chia)Dec 21, 2022 · 20 minutes read![system-tables-splash.jpg](/uploads/large_system_tables_splash_a1fc29fa1f.jpg)
Ever wondered how to debug an issue in ClickHouse? Need a specific statistic, or are you curious about the queries being executed by your users and those that are failing? Or maybe you need to identify the currently applied settings. Look no further than system tables! In this post, we explore the system tables in ClickHouse and show how we in ClickHouse support use them to debug issues and understand your cluster usage with practical examples.


## Introduction to System Tables [\#](/blog/clickhouse-debugging-issues-with-system-tables#introduction-to-system-tables)


System tables in ClickHouse are virtual tables that provide information about server states, processes, and the operating environment. These system tables are located in the system database and are only available for reading by the users. They cannot be dropped or altered, but their partition can be detached and old records can be removed using TTL. System tables offer great insight into the internal operations of ClickHouse and can be a valuable source of information when optimizing queries, monitoring system performance, or troubleshooting a system crash.


In general, there are a few types of system tables in ClickHouse, and some useful ones contain system information related to your [`database`](https://clickhouse.com/docs/en/operations/system-tables/databases), [`tables`](https://clickhouse.com/docs/en/operations/system-tables/tables), [`columns`](https://clickhouse.com/docs/en/operations/system-tables/columns), and [`parts`](https://clickhouse.com/docs/en/operations/system-tables/parts). There are also tables showing real\-time information such as [`metrics`](https://clickhouse.com/docs/en/operations/system-tables/metrics) and [`events`](https://clickhouse.com/docs/en/operations/system-tables/events), providing a snapshot view of the current system events. Users may also find historical records in system log tables such as [`metric_log`](https://clickhouse.com/docs/en/operations/system-tables/metric_log), [`query_log`](https://clickhouse.com/docs/en/operations/system-tables/query_log), [`part_log`](https://clickhouse.com/docs/en/operations/system-tables/part_log), etc. In a cluster, [`distribution_queue`](https://clickhouse.com/docs/en/operations/system-tables/distribution_queue) and [`replication_queue`](https://clickhouse.com/docs/en/operations/system-tables/replication_queue) can be used to troubleshoot a distributed setup. Tables related to [settings](https://clickhouse.com/docs/en/operations/system-tables/settings), [users](https://clickhouse.com/docs/en/operations/system-tables/users), and [roles](https://clickhouse.com/docs/en/operations/system-tables/roles) also provide information on the current configuration and user privileges.


Most system tables store their data in memory, but system log tables such as `metric_log`, `query_log` and `part_log` use the MergeTree table engine and store their data in the filesystem by default. This persistent storage ensures that logs are still available for analysis after a server restart.


## Where are the System Tables? [\#](/blog/clickhouse-debugging-issues-with-system-tables#where-are-the-system-tables)


The complete list of system tables is accessible via the `SHOW TABLES FROM system` statement. You can also find an expanded description for most system tables in our [documentation](https://clickhouse.com/docs/en/operations/system-tables/).



```

SHOW TABLES FROM system

┌─name───────────────────────────┐
│ aggregate_function_combinators │
│ asynchronous_inserts           │
│ asynchronous_metric_log        │
│ asynchronous_metric_log_0      │
│ asynchronous_metrics           │
│ backups                        │
│ build_options                  │
│ certificates                   │
│ clusters                       │
│ collations                     │
│ columns                        │
│ contributors                   │
│ current_roles                  │
│ data_skipping_indices          │
│ data_type_families             │
│ databases                      │



```


Like any other table, we can run typical select queries e.g. `SELECT * FROM system.databases`, to retrieve rows from a specified table.



```

SELECT *
FROM system.databases
LIMIT 2
FORMAT Vertical

Row 1:
──────
name:          INFORMATION_SCHEMA
engine:        Memory
data_path:     /var/lib/clickhouse/
metadata_path:
uuid:          00000000-0000-0000-0000-000000000000
comment:

Row 2:
──────
name:          blogs
engine:        Replicated
data_path:     /var/lib/clickhouse/store/
metadata_path: /var/lib/clickhouse/store/912/9125f586-0e3f-48f6-85b0-ccc76380e1a2/
uuid:          9125f586-0e3f-48f6-85b0-ccc76380e1a2
comment:

2 rows in set. Elapsed: 0.001 sec.


```


Aggregating on these tables enables us to write more complex queries and gain a deeper understanding of the state of ClickHouse.



```

SELECT
    engine,
    count() AS count
FROM system.databases
GROUP BY engine

┌─engine─────┬─count─┐
│ Memory     │     2 │
│ Atomic     │     1 │
│ Replicated │     8 │
└────────────┴───────┘

3 rows in set. Elapsed: 0.015 sec.


```


So, what are some of the valuable insights that we can gather from the system tables?


## Hot tips for querying system tables [\#](/blog/clickhouse-debugging-issues-with-system-tables#hot-tips-for-querying-system-tables)


In this section, we will highlight some useful system tables that can help answer the common questions we may have when using ClickHouse.


### What settings were changed from the default value? [\#](/blog/clickhouse-debugging-issues-with-system-tables#what-settings-were-changed-from-the-default-value)


First, we begin by reviewing the list of settings (using [system.settings](https://clickhouse.com/docs/en/operations/system-tables/settings)) that were changed from the default value. During troubleshooting, this is an excellent first step to analyze if the changed settings could affect system behavior.



```

SELECT *
FROM system.settings
WHERE changed
LIMIT 2
FORMAT Vertical

Row 1:
──────
name:        max_insert_threads
value:       4
changed:     1
description: The maximum number of threads to execute the INSERT SELECT query. Values 0 or 1 means that INSERT SELECT is not run in parallel. Higher values will lead to higher memory usage. Parallel INSERT SELECT has effect only if the SELECT part is run on parallel, see 'max_threads' setting.
min:         ᴺᵁᴸᴸ
max:         ᴺᵁᴸᴸ
readonly:    0
type:        UInt64

Row 2:
──────
name:        max_threads
value:       60
changed:     1
description: The maximum number of threads to execute the request. By default, it is determined automatically.
min:         ᴺᵁᴸᴸ
max:         ᴺᵁᴸᴸ
readonly:    0
type:        MaxThreads

2 rows in set. Elapsed: 0.003 sec.


```


### What are the long\-running queries? Which queries took up the most memory? [\#](/blog/clickhouse-debugging-issues-with-system-tables#what-are-the-long-running-queries-which-queries-took-up-the-most-memory)


Next, we dive into the query log table ([system.query\_log](https://clickhouse.com/docs/en/operations/system-tables/query_log/)) that holds a wealth of information about executed queries. It is often the go\-to table for identifying long\-running, memory\-intensive, or failed queries.


Using the query below, we can generate an overview of the queries that took the longest to execute. We also select other columns such as `memory_usage`, `userCPU`, and `systemCPU` to give us a glimpse of the resources utilized. On top of this, the function [normalizedQueryHash](https://clickhouse.com/docs/en/sql-reference/functions/string-functions/#normalizedqueryhash) hashes similar queries into identical 64\-bit hash values, allowing us to further aggregate the value and monitor performance for similar queries.


The same query below can also be used to find queries that took up the most memory. Simply replace the sorting key with `memory_usage`. Note that every successful query will result in two entries recorded in the `query_log`. The first query will have the type `QueryStart` and the last will be `QueryFinish`. We are particularly interested in the QueryFinish rows as these will record the timing and resources used to execute the queries.



```

SELECT
    type,
    event_time,
    query_duration_ms,
    initial_query_id,
    formatReadableSize(memory_usage) AS memory,
    `ProfileEvents.Values`[indexOf(`ProfileEvents.Names`, 'UserTimeMicroseconds')] AS userCPU,
    `ProfileEvents.Values`[indexOf(`ProfileEvents.Names`, 'SystemTimeMicroseconds')] AS systemCPU,
    normalizedQueryHash(query) AS normalized_query_hash,
    substring(normalizeQuery(query) AS query, 1, 100)
FROM system.query_log
ORDER BY query_duration_ms DESC
LIMIT 2
FORMAT Vertical

Row 1:
──────
type:                                     QueryFinish
event_time:                               2022-11-26 11:50:14
query_duration_ms:                        600802
initial_query_id:                         feb4c490-b420-47d3-a7ee-8c87fc68bf45
memory:                                   631.64 MiB
userCPU:                                  27404274713
systemCPU:                                234596117
normalized_query_hash:                    17959601262672325984
substring(normalizeQuery(query), 1, 100): SELECT count() AS c FROM wikistat GROUP BY time

Row 2:
──────
type:                                     QueryFinish
event_time:                               2022-11-26 15:05:39
query_duration_ms:                        545026
initial_query_id:                         8196b460-7a6a-434e-9324-14fc765a9a76
memory:                                   690.21 MiB
userCPU:                                  28103266351
systemCPU:                                324925435
normalized_query_hash:                    8457232685578498203
substring(normalizeQuery(query), 1, 100): SELECT `time`, count() AS `c` FROM `default`.`wikistat` GROUP BY `time` ORDER BY `time` ASC WITH FIL

2 rows in set. Elapsed: 0.244 sec. Processed 8.49 million rows, 4.70 GB (34.75 million rows/s., 19.22 GB/s.)


```


### Which queries have failed? [\#](/blog/clickhouse-debugging-issues-with-system-tables#which-queries-have-failed)


Not all queries are crafted perfectly with some failing to execute. `ExceptionBeforeStart` and `ExceptionWhileProcessing` are two types of exception events that could happen when executing a query. Below is a query that filters for these exceptions and displays the exception message and stack trace, along with columns such as `used_aggregate_functions`, etc. This information can be helpful for troubleshooting.



```

SELECT
    type,
    query_start_time,
    query_duration_ms,
    query_id,
    query_kind,
    is_initial_query,
    normalizeQuery(query) AS normalized_query,
    concat(toString(read_rows), ' rows / ', formatReadableSize(read_bytes)) AS read,
    concat(toString(written_rows), ' rows / ', formatReadableSize(written_bytes)) AS written,
    concat(toString(result_rows), ' rows / ', formatReadableSize(result_bytes)) AS result,
    formatReadableSize(memory_usage) AS `memory usage`,
    exception,
    concat('\n', stack_trace) AS stack_trace,
    user,
    initial_user,
    multiIf(empty(client_name), http_user_agent, concat(client_name, ' ', toString(client_version_major), '.', toString(client_version_minor), '.', toString(client_version_patch))) AS client,
    client_hostname,
    databases,
    tables,
    columns,
    used_aggregate_functions,
    used_aggregate_function_combinators,
    used_database_engines,
    used_data_type_families,
    used_dictionaries,
    used_formats,
    used_functions,
    used_storages,
    used_table_functions,
    thread_ids,
    ProfileEvents,
    Settings
FROM system.query_log
WHERE type IN ['3', '4']
ORDER BY query_start_time DESC
LIMIT 1
FORMAT Vertical

Row 1:
──────
type:                                ExceptionBeforeStart
query_start_time:                    2022-12-12 09:50:52
query_duration_ms:                   0
query_id:                            eec8ab27-51a6-4cde-ae3d-c306c13de5eb
query_kind:                          Select
is_initial_query:                    1
normalized_query:                    select x from taxi_zone_dictionary
read:                                0 rows / 0.00 B
written:                             0 rows / 0.00 B
result:                              0 rows / 0.00 B
memory usage:                        0.00 B
exception:                           Code: 47. DB::Exception: Missing columns: 'x' while processing query: 'SELECT x FROM taxi_zone_dictionary', required columns: 'x'. (UNKNOWN_IDENTIFIER) (version 22.11.1.1360 (official build))
stack_trace:
0. DB::Exception::Exception(std::__1::basic_string, std::__1::allocator> const&, int, bool) @ 0xbd145e8 in /usr/bin/clickhouse
1. DB::TreeRewriterResult::collectUsedColumns(std::__1::shared_ptr const&, bool, bool) @ 0x10ad376c in /usr/bin/clickhouse
2. DB::TreeRewriter::analyzeSelect(std::__1::shared_ptr&, DB::TreeRewriterResult&&, DB::SelectQueryOptions const&, std::__1::vector> const&, std::__1::vector, std::__1::allocator>, std::__1::allocator, std::__1::allocator>>> const&, std::__1::shared_ptr) const @ 0x10ad7fac in /usr/bin/clickhouse
3. ? @ 0x1083b550 in /usr/bin/clickhouse
4. DB::InterpreterSelectQuery::InterpreterSelectQuery(std::__1::shared_ptr const&, std::__1::shared_ptr const&, std::__1::optional, std::__1::shared_ptr const&, DB::SelectQueryOptions const&, std::__1::vector, std::__1::allocator>, std::__1::allocator, std::__1::allocator>>> const&, std::__1::shared_ptr const&, std::__1::shared_ptr) @ 0x10838454 in /usr/bin/clickhouse
5. DB::InterpreterSelectWithUnionQuery::
buildCurrentChildInterpreter(std::__1::shared_ptr const&, std::__1::vector, std::__1::allocator>, std::__1::allocator, std::__1::allocator>>> const&) @ 0x108d1dcc in /usr/bin/clickhouse
6. DB::InterpreterSelectWithUnionQuery::
InterpreterSelectWithUnionQuery(std::__1::shared_ptr const&, std::__1::shared_ptr, DB::SelectQueryOptions const&, std::__1::vector, std::__1::allocator>, std::__1::allocator, std::__1::allocator>>> const&) @ 0x108cfb68 in /usr/bin/clickhouse
7. DB::InterpreterFactory::get(std::__1::shared_ptr&, std::__1::shared_ptr, DB::SelectQueryOptions const&) @ 0x107fe174 in /usr/bin/clickhouse
8. ? @ 0x10b70ab8 in /usr/bin/clickhouse
9. DB::executeQuery(std::__1::basic_string, std::__1::allocator> const&, std::__1::shared_ptr, bool, DB::QueryProcessingStage::Enum) @ 0x10b6e684 in /usr/bin/clickhouse
10. DB::TCPHandler::runImpl() @ 0x11637db0 in /usr/bin/clickhouse
11. DB::TCPHandler::run() @ 0x11648ec4 in /usr/bin/clickhouse
12. Poco::Net::TCPServerConnection::start() @ 0x1225a98c in /usr/bin/clickhouse
13. Poco::Net::TCPServerDispatcher::run() @ 0x1225c520 in /usr/bin/clickhouse
14. Poco::PooledThread::run() @ 0x12416c5c in /usr/bin/clickhouse
15. Poco::ThreadImpl::runnableEntry(void*) @ 0x12414524 in /usr/bin/clickhouse
16. start_thread @ 0x7624 in /usr/lib/aarch64-linux-gnu/libpthread-2.31.so
17. ? @ 0xd149c in /usr/lib/aarch64-linux-gnu/libc-2.31.so

user:                                default
initial_user:                        default
client:                              ClickHouse 22.10.2
client_hostname:                     derek-clickhouse
databases:                           []
tables:                              []
columns:                             []
used_aggregate_functions:            []
used_aggregate_function_combinators: []
used_database_engines:               []
used_data_type_families:             []
used_dictionaries:                   []
used_formats:                        []
used_functions:                      []
used_storages:                       []
used_table_functions:                []
thread_ids:                          []
ProfileEvents:                       {}
Settings:                            {}

1 row in set. Elapsed: 0.019 sec.


```


### What are the common errors? [\#](/blog/clickhouse-debugging-issues-with-system-tables#what-are-the-common-errors)


Next, we explore the [system.errors](https://clickhouse.com/docs/en/operations/system-tables/errors) table. This table contains error codes and the number of times each error has been triggered. Furthermore, we can see when the error last occurred coupled with the exact error message. The `last_error_trace` column also contains a [stack trace](https://clickhouse.com/docs/en/operations/system-tables/stack_trace) for debugging and is helpful for introspecting the server state.



```

SELECT
    name,
    code,
    value,
    last_error_time,
    last_error_message,
    last_error_trace AS remote
FROM system.errors
LIMIT 1
FORMAT Vertical

Row 1:
──────
name:               CANNOT_READ_FROM_ISTREAM
code:               23
value:              1016
last_error_time:    2022-12-21 11:43:06
last_error_message: Cannot read from istream at offset 0
remote:             [228387450,270427334,306047695,310642709,310640492,
310861745,310860816,310860718,315390197,129746296,129744797,229143926,
229154103,229129110,229149953,140698656110089,140698655211827]

1 row in set. Elapsed: 0.002 sec.


```


### Are parts being created when the rows are inserted? [\#](/blog/clickhouse-debugging-issues-with-system-tables#are-parts-being-created-when-the-rows-are-inserted)


Engines in the MergeTree family are designed to write data quickly to a table in small parts, before [merging these into larger parts](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree/) in the background. To confirm that the rows inserted are successfully written into the disk as parts, we can review the [system.part\_log](https://clickhouse.com/docs/en/operations/system-tables/part_log/) and check that new parts are created in a timely manner.



```

SELECT
    event_time,
    event_time_microseconds,
    rows
FROM system.part_log
WHERE (database = 'default') AND (table = 'github_events') AND (event_type IN ['NewPart'])
ORDER BY event_time ASC
LIMIT 10 

┌──────────event_time─┬────event_time_microseconds─┬───rows─┐
│ 2022-12-12 10:54:42 │ 2022-12-12 10:54:42.373583 │ 573440 │
│ 2022-12-12 10:54:45 │ 2022-12-12 10:54:45.116786 │ 507904 │
│ 2022-12-12 10:54:47 │ 2022-12-12 10:54:47.374676 │ 312032 │
│ 2022-12-12 10:54:49 │ 2022-12-12 10:54:49.598769 │ 434176 │
│ 2022-12-12 10:54:51 │ 2022-12-12 10:54:51.824833 │ 368638 │
│ 2022-12-12 10:54:53 │ 2022-12-12 10:54:53.964555 │ 548864 │
│ 2022-12-12 10:54:56 │ 2022-12-12 10:54:56.286868 │ 524288 │
│ 2022-12-12 10:54:58 │ 2022-12-12 10:54:58.892573 │ 253948 │
│ 2022-12-12 10:55:01 │ 2022-12-12 10:55:01.404872 │ 450560 │
│ 2022-12-12 10:55:03 │ 2022-12-12 10:55:03.630993 │ 328850 │
└─────────────────────┴────────────────────────────┴────────┘

10 rows in set. Elapsed: 0.012 sec. Processed 4.96 thousand rows, 292.42 KB (404.05 thousand rows/s., 23.80 MB/s.)


```


### What is the status of the in\-progress merges? [\#](/blog/clickhouse-debugging-issues-with-system-tables#what-is-the-status-of-the-in-progress-merges)


As newly created parts are constantly merged in the background, we can watch for long\-running merges using the [system.merges](https://clickhouse.com/docs/en/operations/system-tables/merges) table. Merges that take a long time to complete could mean that certain system resources (e.g. CPU, disk IO) have reached a saturation point.



```

SELECT
    hostName(),
    database,
    table,
    round(elapsed, 0) AS time,
    round(progress, 4) AS percent,
    formatReadableTimeDelta((elapsed / progress) - elapsed) AS ETA,
    num_parts,
    formatReadableSize(memory_usage) AS memory_usage,
    result_part_name
FROM system.merges
ORDER BY (elapsed / percent) - elapsed ASC
FORMAT Vertical

Row 1:
──────
hostName():       c-mint-mb-85-server-0
database:         default
table:            minicrawl
time:             831
percent:          0.6428
ETA:              7 minutes and 41 seconds
num_parts:        6
memory_usage:     1.50 GiB
result_part_name: all_839_1124_4

2 rows in set. Elapsed: 0.360 sec.


```


### Are there parts with errors? [\#](/blog/clickhouse-debugging-issues-with-system-tables#are-there-parts-with-errors)


To identify errors during part merges, we can again examine the [system.part\_log](https://clickhouse.com/docs/en/operations/system-tables/part_log/) table to reveal the number of times a data part error occurred for a particular event type. The error codes are [resolved](https://clickhouse.com/docs/en/sql-reference/functions/other-functions/#errorcodetoname) to the respective error names and act as a feedback mechanism for us to adjust our queries or provide additional resources. A full list of error codes and names can be found [here](https://github.com/ClickHouse/ClickHouse/blob/master/src/Common/ErrorCodes.cpp).



```

SELECT
    event_date,
    event_type,
    table,
    error AS error_code,
    errorCodeToName(error) AS error_code_name,
    count() as c
FROM system.part_log
WHERE (error_code != 0) AND (event_date > (now() - toIntervalMonth(1)))
GROUP BY
    event_date,
    event_type,
    error,
    table
ORDER BY
    event_date DESC,
    event_type ASC,
    table ASC,
    error ASC

┌─event_date─┬─event_type───┬─table──┬─error_code─┬─error_code_name─────────┬────c────┐
│ 2022-12-12 │ MergeParts   │ events │        241 │ MEMORY_LIMIT_EXCEEDED   │      77 │
│ 2022-12-06 │ MergeParts   │ events │        241 │ MEMORY_LIMIT_EXCEEDED   │      16 │
│ 2022-11-28 │ NewPart      │ x      │        389 │ INSERT_WAS_DEDUPLICATED │      38 │
│ 2022-11-28 │ NewPart      │ x      │        394 │ QUERY_WAS_CANCELLED     │       1 │
│ 2022-11-28 │ MergeParts   │ events │        236 │ ABORTED                 │      25 │
│ 2022-11-28 │ MutatePart   │ events │        236 │ ABORTED                 │      68 │
│ 2022-11-27 │ MergeParts   │ events │        236 │ ABORTED                 │       1 │
│ 2022-11-27 │ MutatePart   │ events │        236 │ ABORTED                 │       9 │
│ 2022-11-26 │ MergeParts   │ events │        236 │ ABORTED                 │      26 │
│ 2022-11-26 │ MutatePart   │ events │        236 │ ABORTED                 │     282 │
│ 2022-11-25 │ NewPart      │ x      │        394 │ QUERY_WAS_CANCELLED     │       1 │
│ 2022-11-25 │ MutatePart   │ events │        236 │ ABORTED                 │      14 │
│ 2022-11-24 │ MergeParts   │ events │        236 │ ABORTED                 │      55 │
│ 2022-11-24 │ MergeParts   │ events │        241 │ MEMORY_LIMIT_EXCEEDED   │     158 │
│ 2022-11-24 │ DownloadPart │ events │       1000 │ POCO_EXCEPTION          │       4 │
│ 2022-11-24 │ MutatePart   │ events │        236 │ ABORTED                 │     119 │
│ 2022-11-23 │ MergeParts   │ events │        241 │ MEMORY_LIMIT_EXCEEDED   │     174 │
│ 2022-11-23 │ DownloadPart │ events │       1000 │ POCO_EXCEPTION          │      12 │
│ 2022-11-22 │ MergeParts   │ events │        241 │ MEMORY_LIMIT_EXCEEDED   │      70 │
└────────────┴──────────────┴────────┴────────────┴─────────────────────────┴─────────┘

19 rows in set. Elapsed: 0.008 sec. Processed 73.25 thousand rows, 1.61 MB (8.99 million rows/s., 198.00 MB/s.)


```


### Are there long\-running mutations that are stuck? [\#](/blog/clickhouse-debugging-issues-with-system-tables#are-there-long-running-mutations-that-are-stuck)


[ALTER](https://clickhouse.com/docs/en/sql-reference/statements/alter/) queries, also known as [mutations](https://clickhouse.com/docs/en/sql-reference/statements/alter/#mutations), manipulate table data by rewriting the whole data parts. Thus, this can be a resource\-intensive operation and can take a long time to complete if a large number of parts need to be modified and potentially impact normal merge operations. The query below lists the in\-progress mutations and displays the reason for failure, if any.



```

SELECT
    database,
    table,
    mutation_id,
    command,
    create_time,
    parts_to_do_names,
    parts_to_do,
    is_done,
    latest_failed_part,
    latest_fail_time,
    latest_fail_reason
FROM system.mutations
WHERE NOT is_done
ORDER BY create_time DESC


Row 1:
──────
database:           default
table:              events_wide_new
mutation_id:        0000000001
command:            DROP COLUMN col798
create_time:        2022-12-12 16:19:53
parts_to_do_names:  ['20221212_6_41_2_86','20221212_42_71_2_86','20221212_72_99_2_86','20221212_106_139_2']
parts_to_do:        4
is_done:            0
latest_failed_part:
latest_fail_time:   1970-01-01 00:00:00
latest_fail_reason:

1 row in set. Elapsed: 0.002 sec.


```


### How much disk space are the tables using? [\#](/blog/clickhouse-debugging-issues-with-system-tables#how-much-disk-space-are-the-tables-using)


ClickHouse compresses data really well with the use of [LZ4 compression codec](https://clickhouse.com/docs/en/native-protocol/compression) by default (in ClickHouse Cloud we actually use ZSTD \- see [here](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema) for more details why). However, there are times when we might be curious to find out how much disk space each table is using. The query below makes use of [`system.parts`](https://clickhouse.com/docs/en/operations/system-tables/parts) table to show us the disk space each non\-system table is taking up in total (`total_bytes_on_disk`), as well as the total size of compressed data parts (`data_compressed_bytes`) and also the size when these data parts are uncompressed (`data_uncompressed_bytes`). In the example below, we can observe from the `compression_ratio` column that the compressed data only take up less than 40% of disk space! For those interested in further minimizing your storage, check out our blog post on [Optimizing ClickHouse with Schemas and Codecs](https://clickhouse.com/blog/optimize-clickhouse-codecs-compression-schema).



```

SELECT
    hostName(),
    database,
    table,
    sum(rows) AS rows,
    formatReadableSize(sum(bytes_on_disk)) AS total_bytes_on_disk,
    formatReadableSize(sum(data_compressed_bytes)) AS total_data_compressed_bytes,
    formatReadableSize(sum(data_uncompressed_bytes)) AS total_data_uncompressed_bytes,
    round(sum(data_compressed_bytes) / sum(data_uncompressed_bytes), 3) AS compression_ratio
FROM system.parts
WHERE database != 'system'
GROUP BY
    hostName(),
    database,
    table
ORDER BY sum(bytes_on_disk) DESC FORMAT Vertical

Row 1:
──────
hostName():                    c-mint-mb-85-server-0
database:                      default
table:                         reddit
rows:                          9946243959
total_bytes_on_disk:           718.47 GiB
total_data_compressed_bytes:   717.39 GiB
total_data_uncompressed_bytes: 2.22 TiB
compression_ratio:             0.315

Row 2:
──────
hostName():                    c-mint-mb-85-server-0
database:                      default
table:                         wikistat
rows:                          417565645200
total_bytes_on_disk:           579.44 GiB
total_data_compressed_bytes:   554.31 GiB
total_data_uncompressed_bytes: 14.12 TiB
compression_ratio:             0.038

2 rows in set. Elapsed: 0.004 sec.


```


### What is the status of the parts that are moving? [\#](/blog/clickhouse-debugging-issues-with-system-tables#what-is-the-status-of-the-parts-that-are-moving)


Other than parts merging in the background, parts and partitions can also be moved between disks and volumes. For example, it is common to first store the recently written parts on a hot volume (SSD) and then move them automatically to a cold volume (HDD) when they have passed a certain age. This operation can be done using the [TTL clause](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree#table_engine-mergetree-ttl) or be triggered with the [ALTER statement](https://clickhouse.com/docs/en/sql-reference/statements/alter/partition/#move-partitionpart). When the parts are moving, we can monitor the status using the [recently introduced](https://clickhouse.com/docs/en/whats-new/changelog/#-clickhouse-release-2212-2022-12-15) `system.moves` table to watch for the elapsed time and the destination disk. The query below shows that a part (`all_1_22_2`) is in the process of moving to an s3 disk.



```

ALTER TABLE ontime MOVE PART 'all_1_22_2' TO VOLUME 'external';


```



```

SELECT *
FROM system.moves FORMAT Vertical

Row 1:
──────
database:                 default
table:                    ontime
elapsed:                  8.900590354
target_disk_name:         s3
target_disk_path:         /var/lib/clickhouse/disks/s3_disk/
part_name:                all_1_22_2
part_size:                1643771811
thread_id:                10071

1 row in set. Elapsed: 0.160 sec.


```


### Querying system tables from all nodes in a cluster [\#](/blog/clickhouse-debugging-issues-with-system-tables#querying-system-tables-from-all-nodes-in-a-cluster)


When querying for system tables in a cluster, take note that the query is only executed on the local node where the query is issued. To retrieve rows from all nodes in a cluster with shards and replicas, we need to use the [clusterAllReplicas](https://clickhouse.com/docs/en/sql-reference/table-functions/cluster/) table function. The query below is sent to a cluster with two shards, each with two replicas. Based on the [hostName](https://clickhouse.com/docs/en/sql-reference/functions/other-functions/#hostname), we can see that the resulting rows were gathered from all four nodes.



```

SELECT
    hostName(),
    is_initial_query,
    query_id,
    initial_query_id,
    query
FROM clusterAllReplicas('default', system.processes)
FORMAT Vertical

Row 1:
──────
hostName():       c-mint-mb-85-server-0
is_initial_query: 1
query_id:         c8f1cfb2-7eed-4ecd-a303-cc20ef5d9d0f
initial_query_id: c8f1cfb2-7eed-4ecd-a303-cc20ef5d9d0f
query:            SELECT
    hostName(),
    is_initial_query,
    query_id,
    initial_query_id,
    query
FROM clusterAllReplicas('default', system.processes) FORMAT Vertical

Row 2:
──────
hostName():       c-mint-mb-85-server-1
is_initial_query: 0
query_id:         e487bae2-0886-46ef-8510-87c218f45332
initial_query_id: c8f1cfb2-7eed-4ecd-a303-cc20ef5d9d0f
query:            SELECT hostName(), `is_initial_query`, `query_id`, `initial_query_id`, `query` FROM `system`.`processes`

Row 3:
──────
hostName():       c-mint-mb-85-server-2
is_initial_query: 0
query_id:         271abbde-64b9-46ea-9391-9f402cc013ef
initial_query_id: c8f1cfb2-7eed-4ecd-a303-cc20ef5d9d0f
query:            SELECT hostName(), `is_initial_query`, `query_id`, `initial_query_id`, `query` FROM `system`.`processes`

3 rows in set. Elapsed: 0.006 sec.


```


## Conclusion [\#](/blog/clickhouse-debugging-issues-with-system-tables#conclusion)


In this post, we’ve introduced how system tables can be used to query for the current and historical state of ClickHouse. We’ve provided examples using system tables to answer some common questions when using ClickHouse. In a future post, we’ll explore these tables in more detail and how they can be used to monitor ClickHouse for common challenges on INSERT and SELECT queries.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
