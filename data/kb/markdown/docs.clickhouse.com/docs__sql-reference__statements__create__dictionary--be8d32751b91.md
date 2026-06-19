# CREATE DICTIONARY \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- Overview
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/overview.md)# CREATE DICTIONARY


A dictionary is a mapping (`key -> attributes`) that is convenient for various types of reference lists.
ClickHouse supports special functions for working with dictionaries that can be used in queries. It is easier and more efficient to use dictionaries with functions than a `JOIN` with reference tables.


Dictionaries can be created in two ways:


- [With a DDL query](#creating-a-dictionary-with-a-ddl-query) (recommended)
- [With a configuration file](#creating-a-dictionary-with-a-configuration-file)


## Creating a dictionary with a DDL query[​](#creating-a-dictionary-with-a-ddl-query "Direct link to Creating a dictionary with a DDL query")


Supported in ClickHouse Cloud
Dictionaries can be created with DDL queries.
This is the recommended method because with DDL created dictionaries:


- No additional records are added to server configuration files.
- Dictionaries can be used like first\-class entities such as tables or views.
- Data can be read directly, using familiar `SELECT` syntax rather than dictionary table functions. Note that when accessing a dictionary directly via a `SELECT` statement, cached dictionary will return only cached data, while for a non\-cached dictionary it will return all the data that it stores.
- Dictionaries can be easily renamed.


### Syntax[​](#syntax "Direct link to Syntax")



```
CREATE [OR REPLACE] DICTIONARY [IF NOT EXISTS] [db.]dictionary_name [ON CLUSTER cluster]
(
    key1  type1  [DEFAULT | EXPRESSION expr1] [IS_OBJECT_ID],
    key2  type2  [DEFAULT | EXPRESSION expr2],
    attr1 type2  [DEFAULT | EXPRESSION expr3] [HIERARCHICAL|INJECTIVE],
    attr2 type2  [DEFAULT | EXPRESSION expr4] [HIERARCHICAL|INJECTIVE]
)
PRIMARY KEY key1, key2
SOURCE(SOURCE_NAME([param1 value1 ... paramN valueN]))
LAYOUT(LAYOUT_NAME([param_name param_value]))
LIFETIME({MIN min_val MAX max_val | max_val})
SETTINGS(setting_name = setting_value, setting_name = setting_value, ...)
COMMENT 'Comment'

```



| Clause Description| [Attributes](/docs/sql-reference/statements/create/dictionary/attributes) Dictionary attributes are specified similarly to table columns. The only required property is the type, all others may have default values.| PRIMARY KEY Defines the key column(s) for dictionary lookups. Depending on the layout, one or more attributes can be specified as keys.| [`SOURCE`](/docs/sql-reference/statements/create/dictionary/sources) Defines the data source for the dictionary (e.g. ClickHouse table, HTTP, PostgreSQL).| [`LAYOUT`](/docs/sql-reference/statements/create/dictionary/layouts) Controls how the dictionary is stored in memory (e.g. `FLAT`, `HASHED`, `CACHE`).| [`LIFETIME`](/docs/sql-reference/statements/create/dictionary/lifetime) Sets the refresh interval for the dictionary.| [`ON CLUSTER`](/docs/sql-reference/distributed-ddl) Creates the dictionary on a cluster. Optional.| `SETTINGS` Additional dictionary settings. Optional.| `COMMENT` Adds a text comment to the dictionary. Optional. | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


## Creating a dictionary with a configuration file[​](#creating-a-dictionary-with-a-configuration-file "Direct link to Creating a dictionary with a configuration file")


Not supported in ClickHouse Cloud
NoteCreating a dictionary with a configuration file is not applicable to ClickHouse Cloud. Please use DDL (see above), and create your dictionary as the `default` user.


The dictionary configuration file has the following format:



```
<clickhouse>
    <comment>An optional element with any content. Ignored by the ClickHouse server.</comment>

    <!--Optional element. File name with substitutions-->
    <include_from>/etc/metrika.xml</include_from>


    <dictionary>
        <!-- Dictionary configuration. -->
        <!-- There can be any number of dictionary sections in a configuration file. -->
    </dictionary>

</clickhouse>

```

You can configure any number of dictionaries in the same file.


## Related content[​](#related-content "Direct link to Related content")


- [Layouts](/docs/sql-reference/statements/create/dictionary/layouts) — How dictionaries are stored in memory
- [Sources](/docs/sql-reference/statements/create/dictionary/sources) — Connecting to data sources
- [Lifetime](/docs/sql-reference/statements/create/dictionary/lifetime) — Automatic refresh configuration
- [Attributes](/docs/sql-reference/statements/create/dictionary/attributes) — Key and attribute configuration
- [Embedded Dictionaries](/docs/sql-reference/statements/create/dictionary/embedded) — Built\-in geobase dictionaries
- [system.dictionaries](/docs/operations/system-tables/dictionaries) — System table with dictionary information
[PreviousCREATE](/docs/sql-reference/statements/create)[NextAttributes](/docs/sql-reference/statements/create/dictionary/attributes)- [Creating a dictionary with a DDL query](#creating-a-dictionary-with-a-ddl-query)
	- [Syntax](#syntax)- [Creating a dictionary with a configuration file](#creating-a-dictionary-with-a-configuration-file)- [Related content](#related-content)
Was this page helpful?
