---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/settings-profile.md)#
topic: create-settings-profile-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# CREATE SETTINGS PROFILE \| ClickHouse Docs

- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- SETTINGS PROFILE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/settings-profile.md)# CREATE SETTINGS PROFILE

Creates [settings profiles](/docs/operations/access-rights#settings-profiles-management) that can be assigned to a user or a role.

Syntax:

```
CREATE SETTINGS PROFILE [IF NOT EXISTS | OR REPLACE] name1 [, name2 [,...]] 
    [ON CLUSTER cluster_name]
    [IN access_storage_type]
    [SETTINGS variable [= value] [MIN [=] min_value] [MAX [=] max_value] [CONST|READONLY|WRITABLE|CHANGEABLE_IN_READONLY] | INHERIT 'profile_name'] [,...]
    [TO {{role1 | user1 [, role2 | user2 ...]} | NONE | ALL | ALL EXCEPT {role1 | user1 [, role2 | user2 ...]}}]

```

`ON CLUSTER` clause allows creating settings profiles on a cluster, see [Distributed DDL](/docs/sql-reference/distributed-ddl).

## Example[​](#example "Direct link to Example")

Create a user:

```
CREATE USER robin IDENTIFIED BY 'password';

```

Create the `max_memory_usage_profile` settings profile with value and constraints for the `max_memory_usage` setting and assign it to user `robin`:

```
CREATE
SETTINGS PROFILE max_memory_usage_profile SETTINGS max_memory_usage = 100000001 MIN 90000000 MAX 110000000
TO robin

```
[PreviousQUOTA](/docs/sql-reference/statements/create/quota)[NextNAMED COLLECTION](/docs/sql-reference/statements/create/named-collection)- [Example](#example)
Was this page helpful?
