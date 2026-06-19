---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/show.md)#
topic: show-statements-clickhouse-docs
ch_version_introduced: '127.0'
last_updated: '2026-06-12'
chunk_index: 11
total_chunks_in_doc: 11
---

10.25 MiB │ └────────────┴──────────┴───────────────────┴─────────┴──────────┴─────────────┴─────────────────┴──────────────┘ ``` ## SHOW CREATE MASKING POLICY[​](#show-create-masking-policy "Direct link to SHOW CREATE MASKING POLICY") The `SHOW CREATE MASKING POLICY` statement shows parameters which were used at [masking policy creation](/docs/sql-reference/statements/create/masking-policy). ### Syntax[​](#syntax-26 "Direct link to Syntax")

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
