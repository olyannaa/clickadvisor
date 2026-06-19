# SHOW Statements \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- SHOW
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/show.md)# SHOW Statements

Note`SHOW CREATE (TABLE|DATABASE|USER)` hides secrets unless the following settings are turned on:- [`display_secrets_in_show_and_select`](/docs/operations/server-configuration-parameters/settings#display_secrets_in_show_and_select) (server setting)
- [`format_display_secrets_in_show_and_select`](/docs/operations/settings/formats#format_display_secrets_in_show_and_select)  (format setting)

Additionally, the user should have the [`displaySecretsInShowAndSelect`](/docs/sql-reference/statements/grant#displaysecretsinshowandselect) privilege.




## SHOW CREATE TABLE \| DICTIONARY \| VIEW \| DATABASE[​](#show-create-table--dictionary--view--database "Direct link to SHOW CREATE TABLE | DICTIONARY | VIEW | DATABASE")


These statements return a single column of type String,
containing the `CREATE` query used for creating the specified object.


### Syntax[​](#syntax "Direct link to Syntax")



```
SHOW [CREATE] TABLE | TEMPORARY TABLE | DICTIONARY | VIEW | DATABASE [db.]table|view [INTO OUTFILE filename] [FORMAT format]

```

NoteIf you use this statement to get the `CREATE` query of system tables,
you will get a *fake* query, which only declares the table structure,
but cannot be used to create a table.


## SHOW DATABASES[​](#show-databases "Direct link to SHOW DATABASES")


This statement prints a list of all databases.


### Syntax[​](#syntax-1 "Direct link to Syntax")



```
SHOW DATABASES [[NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE filename] [FORMAT format]

```

It is identical to the query:



```
SELECT name FROM system.databases [WHERE name [NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE filename] [FORMAT format]

```

### Examples[​](#examples "Direct link to Examples")


In this example we use `SHOW` to obtain database names containing the symbol sequence 'de' in their names:



```
SHOW DATABASES LIKE '%de%'

```


```
┌─name────┐
│ default │
└─────────┘

```

We can also do so in a case\-insensitive manner:



```
SHOW DATABASES ILIKE '%DE%'

```


```
┌─name────┐
│ default │
└─────────┘

```

Or get database names which do not contain 'de' in their names:



```
SHOW DATABASES NOT LIKE '%de%'

```


```
┌─name───────────────────────────┐
│ _temporary_and_external_tables │
│ system                         │
│ test                           │
│ tutorial                       │
└────────────────────────────────┘

```

Finally, we can get the names of only the first two databases:



```
SHOW DATABASES LIMIT 2

```


```
┌─name───────────────────────────┐
│ _temporary_and_external_tables │
│ default                        │
└────────────────────────────────┘

```

### See also[​](#see-also "Direct link to See also")


- [`CREATE DATABASE`](/docs/sql-reference/statements/create/database)


## SHOW TABLES[​](#show-tables "Direct link to SHOW TABLES")


The `SHOW TABLES` statement displays a list of tables.


### Syntax[​](#syntax-2 "Direct link to Syntax")



```
SHOW [FULL] [TEMPORARY] TABLES [{FROM | IN} <db>] [[NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

If the `FROM` clause is not specified, the query returns a list of tables from the current database.


This statement is identical to the query:



```
SELECT name FROM system.tables [WHERE name [NOT] LIKE | ILIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

### Examples[​](#examples-1 "Direct link to Examples")


In this example we use the `SHOW TABLES` statement to find all tables containing 'user' in their names:



```
SHOW TABLES FROM system LIKE '%user%'

```


```
┌─name─────────────┐
│ user_directories │
│ users            │
└──────────────────┘

```

We can also do so in a case\-insensitive manner:



```
SHOW TABLES FROM system ILIKE '%USER%'

```


```
┌─name─────────────┐
│ user_directories │
│ users            │
└──────────────────┘

```

Or to find tables which don't contain the letter 's' in their names:



```
SHOW TABLES FROM system NOT LIKE '%s%'

```


```
┌─name─────────┐
│ metric_log   │
│ metric_log_0 │
│ metric_log_1 │
└──────────────┘

```

Finally, we can get the names of only the first two tables:



```
SHOW TABLES FROM system LIMIT 2

```


```
┌─name───────────────────────────┐
│ aggregate_function_combinators │
│ asynchronous_metric_log        │
└────────────────────────────────┘

```

### See also[​](#see-also-1 "Direct link to See also")


- [`Create Tables`](/docs/sql-reference/statements/create/table)
- [`SHOW CREATE TABLE`](#show-create-table--dictionary--view--database)


## SHOW COLUMNS[​](#show_columns "Direct link to SHOW COLUMNS")


The `SHOW COLUMNS` statement displays a list of columns.


### Syntax[​](#syntax-3 "Direct link to Syntax")



```
SHOW [EXTENDED] [FULL] COLUMNS {FROM | IN} <table> [{FROM | IN} <db>] [{[NOT] {LIKE | ILIKE} '<pattern>' | WHERE <expr>}] [LIMIT <N>] [INTO
OUTFILE <filename>] [FORMAT <format>]

```

The database and table name can be specified in abbreviated form as `<db>.<table>`,
meaning that `FROM tab FROM db` and `FROM db.tab` are equivalent.
If no database is specified, the query returns the list of columns from the current database.


There are also two optional keywords: `EXTENDED` and `FULL`. The `EXTENDED` keyword currently has no effect,
and exists for MySQL compatibility. The `FULL` keyword causes the output to include the collation, comment and privilege columns.


The `SHOW COLUMNS` statement produces a result table with the following structure:




| Column Description Type| `field` The name of the column `String`| `type` The column data type. If the query was made through the MySQL wire protocol, then the equivalent type name in MySQL is shown. `String`| `null` `YES` if the column data type is Nullable, `NO` otherwise `String`| `key` `PRI` if the column is part of the primary key, `SOR` if the column is part of the sorting key, empty otherwise `String`| `default` Default expression of the column if it is of type `ALIAS`, `DEFAULT`, or `MATERIALIZED`, otherwise `NULL`. `Nullable(String)`| `extra` Additional information, currently unused `String`| `collation` (only if `FULL` keyword was specified) Collation of the column, always `NULL` because ClickHouse has no per\-column collations `Nullable(String)`| `comment` (only if `FULL` keyword was specified) Comment on the column `String`| `privilege` (only if `FULL` keyword was specified) The privilege you have on this column, currently not available `String` | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


### Examples[​](#examples-2 "Direct link to Examples")


In this example we'll use the `SHOW COLUMNS` statement to get information about all columns in table 'orders',
starting from 'delivery\_':



```
SHOW COLUMNS FROM 'orders' LIKE 'delivery_%'

```


```
┌─field───────────┬─type─────┬─null─┬─key─────┬─default─┬─extra─┐
│ delivery_date   │ DateTime │    0 │ PRI SOR │ ᴺᵁᴸᴸ    │       │
│ delivery_status │ Bool     │    0 │         │ ᴺᵁᴸᴸ    │       │
└─────────────────┴──────────┴──────┴─────────┴─────────┴───────┘

```

### See also[​](#see-also-2 "Direct link to See also")


- [`system.columns`](/docs/operations/system-tables/columns)


## SHOW DICTIONARIES[​](#show-dictionaries "Direct link to SHOW DICTIONARIES")


The `SHOW DICTIONARIES` statement displays a list of [Dictionaries](/docs/sql-reference/statements/create/dictionary).


### Syntax[​](#syntax-4 "Direct link to Syntax")



```
SHOW DICTIONARIES [FROM <db>] [LIKE '<pattern>'] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

If the `FROM` clause is not specified, the query returns the list of dictionaries from the current database.


You can get the same results as the `SHOW DICTIONARIES` query in the following way:



```
SELECT name FROM system.dictionaries WHERE database = <db> [AND name LIKE <pattern>] [LIMIT <N>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

### Examples[​](#examples-3 "Direct link to Examples")


The following query selects the first two rows from the list of tables in the `system` database, whose names contain `reg`.



```
SHOW DICTIONARIES FROM db LIKE '%reg%' LIMIT 2

```


```
┌─name─────────┐
│ regions      │
│ region_names │
└──────────────┘

```

## SHOW INDEX[​](#show-index "Direct link to SHOW INDEX")


Displays a list of primary and data skipping indexes of a table.


This statement mostly exists for compatibility with MySQL. System tables [`system.tables`](/docs/operations/system-tables/tables) (for
primary keys) and [`system.data_skipping_indices`](/docs/operations/system-tables/data_skipping_indices) (for data skipping indices)
provide equivalent information but in a fashion more native to ClickHouse.


### Syntax[​](#syntax-5 "Direct link to Syntax")



```
SHOW [EXTENDED] {INDEX | INDEXES | INDICES | KEYS } {FROM | IN} <table> [{FROM | IN} <db>] [WHERE <expr>] [INTO OUTFILE <filename>] [FORMAT <format>]

```

The database and table name can be specified in abbreviated form as `<db>.<table>`, i.e. `FROM tab FROM db` and `FROM db.tab` are
equivalent. If no database is specified, the query assumes the current database as database.


The optional keyword `EXTENDED` currently has no effect, and exists for MySQL compatibility.


The statement produces a result table with the following structure:




| Column Description Type| `table` The name of the table. `String`| `non_unique` Always `1` as ClickHouse does not support uniqueness constraints. `UInt8`| `key_name` The name of the index, `PRIMARY` if the index is a primary key index. `String`| `seq_in_index` For a primary key index, the position of the column starting from `1`. For a data skipping index: always `1`. `UInt8`| `column_name` For a primary key index, the name of the column. For a data skipping index: `''` (empty string), see field "expression". `String`| `collation` The sorting of the column in the index: `A` if ascending, `D` if descending, `NULL` if unsorted. `Nullable(String)`| `cardinality` An estimation of the index cardinality (number of unique values in the index). Currently always 0\. `UInt64`| `sub_part` Always `NULL` because ClickHouse does not support index prefixes like MySQL. `Nullable(String)`| `packed` Always `NULL` because ClickHouse does not support packed indexes (like MySQL). `Nullable(String)`| `null` Currently unused | `index_type` The index type, e.g. `PRIMARY`, `MINMAX`, `BLOOM_FILTER` etc. `String`| `comment` Additional information about the index, currently always `''` (empty string). `String`| `index_comment` `''` (empty string) because indexes in ClickHouse cannot have a `COMMENT` field (like in MySQL). `String`| `visible` If the index is visible to the optimizer, always `YES`. `String`| `expression` For a data skipping index, the index expression. For a primary key index: `''` (empty string). `String` | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


### Examples[​](#examples-4 "Direct link to Examples")


In this example we use the `SHOW INDEX` statement to get information about all indexes in table 'tbl'



```
SHOW INDEX FROM 'tbl'

```


```
┌─table─┬─non_unique─┬─key_name─┬─seq_in_index─┬─column_name─┬─collation─┬─cardinality─┬─sub_part─┬─packed─┬─null─┬─index_type───┬─comment─┬─index_comment─┬─visible─┬─expression─┐
│ tbl   │          1 │ blf_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ BLOOM_FILTER │         │               │ YES     │ d, b       │
│ tbl   │          1 │ mm1_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ MINMAX       │         │               │ YES     │ a, c, d    │
│ tbl   │          1 │ mm2_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ MINMAX       │         │               │ YES     │ c, d, e    │
│ tbl   │          1 │ PRIMARY  │ 1            │ c           │ A         │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ PRIMARY      │         │               │ YES     │            │
│ tbl   │          1 │ PRIMARY  │ 2            │ a           │ A         │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ PRIMARY      │         │               │ YES     │            │
│ tbl   │          1 │ set_idx  │ 1            │ 1           │ ᴺᵁᴸᴸ      │ 0           │ ᴺᵁᴸᴸ     │ ᴺᵁᴸᴸ   │ ᴺᵁᴸᴸ │ SET          │         │               │ YES     │ e          │
└───────┴────────────┴──────────┴──────────────┴─────────────┴───────────┴─────────────┴──────────┴────────┴──────┴──────────────┴─────────┴───────────────┴─────────┴────────────┘

```

### See also[​](#see-also-3 "Direct link to See also")


- [`system.tables`](/docs/operations/system-tables/tables)
- [`system.data_skipping_indices`](/docs/operations/system-tables/data_skipping_indices)


## SHOW PROCESSLIST[​](#show-processlist "Direct link to SHOW PROCESSLIST")


Outputs the content of the [`system.processes`](/docs/operations/system-tables/processes) table, that contains a list of queries that are being processed at the moment, excluding `SHOW PROCESSLIST` queries.


### Syntax[​](#syntax-6 "Direct link to Syntax")



```
SHOW PROCESSLIST [INTO OUTFILE filename] [FORMAT format]

```

The `SELECT * FROM system.processes` query returns data about all the current queries.


TipExecute in the console:
```
$ watch -n1 "clickhouse-client --query='SHOW PROCESSLIST'"

```



## SHOW GRANTS[​](#show-grants "Direct link to SHOW GRANTS")


The `SHOW GRANTS` statement shows privileges for a user.


### Syntax[​](#syntax-7 "Direct link to Syntax")



```
SHOW GRANTS [FOR user1 [, user2 ...]] [WITH IMPLICIT] [FINAL]

```

If the user is not specified, the query returns privileges for the current user.


The `WITH IMPLICIT` modifier allows showing the implicit grants (e.g., `GRANT SELECT ON system.one`)


The `FINAL` modifier merges all grants from the user and its granted roles (with inheritance)


## SHOW CREATE USER[​](#show-create-user "Direct link to SHOW CREATE USER")


The `SHOW CREATE USER` statement shows parameters which were used at [user creation](/docs/sql-reference/statements/create/user).


### Syntax[​](#syntax-8 "Direct link to Syntax")



```
SHOW CREATE USER [name1 [, name2 ...] | CURRENT_USER]

```

## SHOW CREATE ROLE[​](#show-create-role "Direct link to SHOW CREATE ROLE")


The `SHOW CREATE ROLE` statement shows parameters which were used at [role creation](/docs/sql-reference/statements/create/role).


### Syntax[​](#syntax-9 "Direct link to Syntax")



```
SHOW CREATE ROLE name1 [, name2 ...]

```

## SHOW CREATE ROW POLICY[​](#show-create-row-policy "Direct link to SHOW CREATE ROW POLICY")


The `SHOW CREATE ROW POLICY` statement shows parameters which were used at [row policy creation](/docs/sql-reference/statements/create/row-policy).


### Syntax[​](#syntax-10 "Direct link to Syntax")



```
SHOW CREATE [ROW] POLICY name ON [database1.]table1 [, [database2.]table2 ...]

```

## SHOW CREATE QUOTA[​](#show-create-quota "Direct link to SHOW CREATE QUOTA")


The `SHOW CREATE QUOTA` statement shows parameters which were used at [quota creation](/docs/sql-reference/statements/create/quota).


### Syntax[​](#syntax-11 "Direct link to Syntax")



```
SHOW CREATE QUOTA [name1 [, name2 ...] | CURRENT]

```

## SHOW CREATE SETTINGS PROFILE[​](#show-create-settings-profile "Direct link to SHOW CREATE SETTINGS PROFILE")


The `SHOW CREATE SETTINGS PROFILE` statement shows parameters which were used at [settings profile creation](/docs/sql-reference/statements/create/settings-profile).


### Syntax[​](#syntax-12 "Direct link to Syntax")



```
SHOW CREATE [SETTINGS] PROFILE name1 [, name2 ...]

```

## SHOW USERS[​](#show-users "Direct link to SHOW USERS")


The `SHOW USERS` statement returns a list of [user account](/docs/operations/access-rights#user-account-management) names.
To view user accounts parameters, see the system table [`system.users`](/docs/operations/system-tables/users).


### Syntax[​](#syntax-13 "Direct link to Syntax")



```
SHOW USERS

```

## SHOW ROLES[​](#show-roles "Direct link to SHOW ROLES")


The `SHOW ROLES` statement returns a list of [roles](/docs/operations/access-rights#role-management).
To view other parameters,
see system tables [`system.roles`](/docs/operations/system-tables/roles) and [`system.role_grants`](/docs/operations/system-tables/role_grants).


### Syntax[​](#syntax-14 "Direct link to Syntax")



```
SHOW [CURRENT|ENABLED] ROLES

```

## SHOW PROFILES[​](#show-profiles "Direct link to SHOW PROFILES")


The `SHOW PROFILES` statement returns a list of [setting profiles](/docs/operations/access-rights#settings-profiles-management).
To view user accounts parameters, see system table [`settings_profiles`](/docs/operations/system-tables/settings_profiles).


### Syntax[​](#syntax-15 "Direct link to Syntax")



```
SHOW [SETTINGS] PROFILES

```

## SHOW POLICIES[​](#show-policies "Direct link to SHOW POLICIES")


The `SHOW POLICIES` statement returns a list of [row policies](/docs/operations/access-rights#row-policy-management) for the specified table.
To view user accounts parameters, see system table [`system.row_policies`](/docs/operations/system-tables/row_policies).


### Syntax[​](#syntax-16 "Direct link to Syntax")



```
SHOW [ROW] POLICIES [ON [db.]table]

```

## SHOW QUOTAS[​](#show-quotas "Direct link to SHOW QUOTAS")


The `SHOW QUOTAS` statement returns a list of [quotas](/docs/operations/access-rights#quotas-management).
To view quotas parameters, see the system table [`system.quotas`](/docs/operations/system-tables/quotas).


### Syntax[​](#syntax-17 "Direct link to Syntax")



```
SHOW QUOTAS

```

## SHOW QUOTA[​](#show-quota "Direct link to SHOW QUOTA")


The `SHOW QUOTA` statement returns a [quota](/docs/operations/quotas) consumption for all users or for current user.
To view other parameters, see system tables [`system.quotas_usage`](/docs/operations/system-tables/quotas_usage) and [`system.quota_usage`](/docs/operations/system-tables/quota_usage).


### Syntax[​](#syntax-18 "Direct link to Syntax")



```
SHOW [CURRENT] QUOTA

```

## SHOW ACCESS[​](#show-access "Direct link to SHOW ACCESS")


The `SHOW ACCESS` statement shows all [users](/docs/operations/access-rights#user-account-management), [roles](/docs/operations/access-rights#role-management), [profiles](/docs/operations/access-rights#settings-profiles-management), etc. and all their [grants](/docs/sql-reference/statements/grant#privileges).


### Syntax[​](#syntax-19 "Direct link to Syntax")



```
SHOW ACCESS

```

## SHOW CLUSTER(S)[​](#show-clusters "Direct link to SHOW CLUSTER(S)")


The `SHOW CLUSTER(S)` statement returns a list of clusters.
All available clusters are listed in the [`system.clusters`](/docs/operations/system-tables/clusters) table.


NoteThe `SHOW CLUSTER name` query displays `cluster`, `shard_num`, `replica_num`, `host_name`, `host_address`, and `port` of the `system.clusters` table for the specified cluster name.


### Syntax[​](#syntax-20 "Direct link to Syntax")



```
SHOW CLUSTER '<name>'
SHOW CLUSTERS [[NOT] LIKE|ILIKE '<pattern>'] [LIMIT <N>]

```

### Examples[​](#examples-5 "Direct link to Examples")



```
SHOW CLUSTERS;

```


```
┌─cluster──────────────────────────────────────┐
│ test_cluster_two_shards                      │
│ test_cluster_two_shards_internal_replication │
│ test_cluster_two_shards_localhost            │
│ test_shard_localhost                         │
│ test_shard_localhost_secure                  │
│ test_unavailable_shard                       │
└──────────────────────────────────────────────┘

```


```
SHOW CLUSTERS LIKE 'test%' LIMIT 1;

```


```
┌─cluster─────────────────┐
│ test_cluster_two_shards │
└─────────────────────────┘

```


```
SHOW CLUSTER 'test_shard_localhost' FORMAT Vertical;

```


```
Row 1:
──────
cluster:                 test_shard_localhost
shard_num:               1
replica_num:             1
host_name:               localhost
host_address:            127.0.0.1
port:                    9000

```

## SHOW SETTINGS[​](#show-settings "Direct link to SHOW SETTINGS")


The `SHOW SETTINGS` statement returns a list of system settings and their values.
It selects data from the [`system.settings`](/docs/operations/system-tables/settings) table.


### Syntax[​](#syntax-21 "Direct link to Syntax")



```
SHOW [CHANGED] SETTINGS LIKE|ILIKE <name>

```

### Clauses[​](#clauses "Direct link to Clauses")


`LIKE|ILIKE` allow to specify a matching pattern for the setting name. It can contain globs such as `%` or `_`. `LIKE` clause is case\-sensitive, `ILIKE` — case insensitive.


When the `CHANGED` clause is used, the query returns only settings changed from their default values.


### Examples[​](#examples-6 "Direct link to Examples")


Query with the `LIKE` clause:



```
SHOW SETTINGS LIKE 'send_timeout';

```


```
┌─name─────────┬─type────┬─value─┐
│ send_timeout │ Seconds │ 300   │
└──────────────┴─────────┴───────┘

```

Query with the `ILIKE` clause:



```
SHOW SETTINGS ILIKE '%CONNECT_timeout%'

```


```
┌─name────────────────────────────────────┬─type─────────┬─value─┐
│ connect_timeout                         │ Seconds      │ 10    │
│ connect_timeout_with_failover_ms        │ Milliseconds │ 50    │
│ connect_timeout_with_failover_secure_ms │ Milliseconds │ 100   │
└─────────────────────────────────────────┴──────────────┴───────┘

```

Query with the `CHANGED` clause:



```
SHOW CHANGED SETTINGS ILIKE '%MEMORY%'

```


```
┌─name─────────────┬─type───┬─value───────┐
│ max_memory_usage │ UInt64 │ 10000000000 │
└──────────────────┴────────┴─────────────┘

```

## SHOW SETTING[​](#show-setting "Direct link to SHOW SETTING")


The `SHOW SETTING` statement outputs setting value for specified setting name.


### Syntax[​](#syntax-22 "Direct link to Syntax")



```
SHOW SETTING <name>

```

### See also[​](#see-also-4 "Direct link to See also")


- [`system.settings`](/docs/operations/system-tables/settings) table


## SHOW FILESYSTEM CACHES[​](#show-filesystem-caches "Direct link to SHOW FILESYSTEM CACHES")


### Examples[​](#examples-7 "Direct link to Examples")



```
SHOW FILESYSTEM CACHES

```


```
┌─Caches────┐
│ s3_cache  │
└───────────┘

```

### See also[​](#see-also-5 "Direct link to See also")


- [`system.settings`](/docs/operations/system-tables/settings) table


## SHOW ENGINES[​](#show-engines "Direct link to SHOW ENGINES")


The `SHOW ENGINES` statement outputs the content of the [`system.table_engines`](/docs/operations/system-tables/table_engines) table,
that contains description of table engines supported by server and their feature support information.


### Syntax[​](#syntax-23 "Direct link to Syntax")



```
SHOW ENGINES [INTO OUTFILE filename] [FORMAT format]

```

### See also[​](#see-also-6 "Direct link to See also")


- [system.table\_engines](/docs/operations/system-tables/table_engines) table


## SHOW FUNCTIONS[​](#show-functions "Direct link to SHOW FUNCTIONS")


The `SHOW FUNCTIONS` statement outputs the content of the [`system.functions`](/docs/operations/system-tables/functions) table.


### Syntax[​](#syntax-24 "Direct link to Syntax")



```
SHOW FUNCTIONS [LIKE | ILIKE '<pattern>']

```

If either `LIKE` or `ILIKE` clause is specified, the query returns a list of system functions whose names match the provided `<pattern>`.


### See Also[​](#see-also-7 "Direct link to See Also")


- [`system.functions`](/docs/operations/system-tables/functions) table


## SHOW MERGES[​](#show-merges "Direct link to SHOW MERGES")


The `SHOW MERGES` statement returns a list of merges.
All merges are listed in the [`system.merges`](/docs/operations/system-tables/merges) table:




| Column Description| `table` Table name.| `database` The name of the database the table is in.| `estimate_complete` The estimated time to complete (in seconds).| `elapsed` The time elapsed (in seconds) since the merge started.| `progress` The percentage of completed work (0\-100 percent).| `is_mutation` 1 if this process is a part mutation.| `size_compressed` The total size of the compressed data of the merged parts.| `memory_usage` Memory consumption of the merge process. | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


### Syntax[​](#syntax-25 "Direct link to Syntax")



```
SHOW MERGES [[NOT] LIKE|ILIKE '<table_name_pattern>'] [LIMIT <N>]

```

### Examples[​](#examples-8 "Direct link to Examples")



```
SHOW MERGES;

```


```
┌─table──────┬─database─┬─estimate_complete─┬─elapsed─┬─progress─┬─is_mutation─┬─size_compressed─┬─memory_usage─┐
│ your_table │ default  │              0.14 │    0.36 │    73.01 │           0 │        5.40 MiB │    10.25 MiB │
└────────────┴──────────┴───────────────────┴─────────┴──────────┴─────────────┴─────────────────┴──────────────┘

```


```
SHOW MERGES LIKE 'your_t%' LIMIT 1;

```


```
┌─table──────┬─database─┬─estimate_complete─┬─elapsed─┬─progress─┬─is_mutation─┬─size_compressed─┬─memory_usage─┐
│ your_table │ default  │              0.14 │    0.36 │    73.01 │           0 │        5.40 MiB │    10.25 MiB │
└────────────┴──────────┴───────────────────┴─────────┴──────────┴─────────────┴─────────────────┴──────────────┘

```

## SHOW CREATE MASKING POLICY[​](#show-create-masking-policy "Direct link to SHOW CREATE MASKING POLICY")


The `SHOW CREATE MASKING POLICY` statement shows parameters which were used at [masking policy creation](/docs/sql-reference/statements/create/masking-policy).


### Syntax[​](#syntax-26 "Direct link to Syntax")



```
SHOW CREATE MASKING POLICY name ON [database.]table

```
[PreviousSYSTEM](/docs/sql-reference/statements/system)[NextGRANT](/docs/sql-reference/statements/grant)- [SHOW CREATE TABLE \| DICTIONARY \| VIEW \| DATABASE](#show-create-table--dictionary--view--database)
	- [Syntax](#syntax)- [SHOW DATABASES](#show-databases)
	- [Syntax](#syntax-1)- [Examples](#examples)- [See also](#see-also)- [SHOW TABLES](#show-tables)
	- [Syntax](#syntax-2)- [Examples](#examples-1)- [See also](#see-also-1)- [SHOW COLUMNS](#show_columns)
	- [Syntax](#syntax-3)- [Examples](#examples-2)- [See also](#see-also-2)- [SHOW DICTIONARIES](#show-dictionaries)
	- [Syntax](#syntax-4)- [Examples](#examples-3)- [SHOW INDEX](#show-index)
	- [Syntax](#syntax-5)- [Examples](#examples-4)- [See also](#see-also-3)- [SHOW PROCESSLIST](#show-processlist)
	- [Syntax](#syntax-6)- [SHOW GRANTS](#show-grants)
	- [Syntax](#syntax-7)- [SHOW CREATE USER](#show-create-user)
	- [Syntax](#syntax-8)- [SHOW CREATE ROLE](#show-create-role)
	- [Syntax](#syntax-9)- [SHOW CREATE ROW POLICY](#show-create-row-policy)
	- [Syntax](#syntax-10)- [SHOW CREATE QUOTA](#show-create-quota)
	- [Syntax](#syntax-11)- [SHOW CREATE SETTINGS PROFILE](#show-create-settings-profile)
	- [Syntax](#syntax-12)- [SHOW USERS](#show-users)
	- [Syntax](#syntax-13)- [SHOW ROLES](#show-roles)
	- [Syntax](#syntax-14)- [SHOW PROFILES](#show-profiles)
	- [Syntax](#syntax-15)- [SHOW POLICIES](#show-policies)
	- [Syntax](#syntax-16)- [SHOW QUOTAS](#show-quotas)
	- [Syntax](#syntax-17)- [SHOW QUOTA](#show-quota)
	- [Syntax](#syntax-18)- [SHOW ACCESS](#show-access)
	- [Syntax](#syntax-19)- [SHOW CLUSTER(S)](#show-clusters)
	- [Syntax](#syntax-20)- [Examples](#examples-5)- [SHOW SETTINGS](#show-settings)
	- [Syntax](#syntax-21)- [Clauses](#clauses)- [Examples](#examples-6)- [SHOW SETTING](#show-setting)
	- [Syntax](#syntax-22)- [See also](#see-also-4)- [SHOW FILESYSTEM CACHES](#show-filesystem-caches)
	- [Examples](#examples-7)- [See also](#see-also-5)- [SHOW ENGINES](#show-engines)
	- [Syntax](#syntax-23)- [See also](#see-also-6)- [SHOW FUNCTIONS](#show-functions)
	- [Syntax](#syntax-24)- [See Also](#see-also-7)- [SHOW MERGES](#show-merges)
	- [Syntax](#syntax-25)- [Examples](#examples-8)- [SHOW CREATE MASKING POLICY](#show-create-masking-policy)
	- [Syntax](#syntax-26)
Was this page helpful?
