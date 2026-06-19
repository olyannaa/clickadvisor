---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/layouts/hierarchical.md)#
topic: hierarchical-dictionaries-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 1
---

# Hierarchical dictionaries \| ClickHouse Docs

- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- LAYOUT- Hierarchical
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/layouts/hierarchical.md)# Hierarchical dictionaries

## Hierarchical dictionaries[​](#hierarchical-dictionaries "Direct link to Hierarchical dictionaries")

ClickHouse supports hierarchical dictionaries with a [numeric key](/docs/sql-reference/statements/create/dictionary/attributes#numeric-key).

Look at the following hierarchical structure:

```
0 (Common parent)
│
├── 1 (Russia)
│   │
│   └── 2 (Moscow)
│       │
│       └── 3 (Center)
│
└── 4 (Great Britain)
    │
    └── 5 (London)

```

This hierarchy can be expressed as the following dictionary table.

| region\_id parent\_region region\_name| 1 0 Russia| 2 1 Moscow| 3 2 Center| 4 0 Great Britain| 5 4 London | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


This table contains a column `parent_region` that contains the key of the nearest parent for the element.

ClickHouse supports the hierarchical property for external dictionary attributes. This property allows you to configure the hierarchical dictionary similar to described above.

The [dictGetHierarchy](/docs/sql-reference/functions/ext-dict-functions#dictGetHierarchy) function allows you to get the parent chain of an element.

For our example, the structure of the dictionary can be the following:

- DDL- Configuration file

```
CREATE DICTIONARY regions_dict
(
    region_id UInt64,
    parent_region UInt64 DEFAULT 0 HIERARCHICAL,
    region_name String DEFAULT ''
)
PRIMARY KEY region_id
SOURCE(...)
LAYOUT(HASHED())
LIFETIME(3600);

```

```
<dictionary>
    <structure>
        <id>
            <name>region_id</name>
        </id>

        <attribute>
            <name>parent_region</name>
            <type>UInt64</type>
            <null_value>0</null_value>
            <hierarchical>true</hierarchical>
        </attribute>

        <attribute>
            <name>region_name</name>
            <type>String</type>
            <null_value></null_value>
        </attribute>

    </structure>
</dictionary>

```

[Previousdirect](/docs/sql-reference/statements/create/dictionary/layouts/direct)[Nextip\_trie](/docs/sql-reference/statements/create/dictionary/layouts/ip-trie)- [Hierarchical dictionaries](#hierarchical-dictionaries)
Was this page helpful?
