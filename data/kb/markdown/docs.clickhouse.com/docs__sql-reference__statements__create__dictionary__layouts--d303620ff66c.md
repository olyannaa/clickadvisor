# Dictionary layouts \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- LAYOUT- Overview
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/layouts/overview.md)# Dictionary layouts

## Dictionary layout types[​](#storing-dictionaries-in-memory "Direct link to Dictionary layout types")


There are a variety of ways to store dictionaries in memory, each with CPU and RAM\-usage trade\-offs.




| Layout Description| [flat](/docs/sql-reference/statements/create/dictionary/layouts/flat) Stores data in flat arrays indexed by key. Fastest layout, but keys must be `UInt64` and bounded by `max_array_size`.| [hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed) Stores data in a hash table. No key size limit, supports any number of elements.| [sparse\_hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed#sparse_hashed) Like `hashed`, but trades CPU for lower memory usage.| [complex\_key\_hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed#complex_key_hashed) Like `hashed`, for composite keys.| [complex\_key\_sparse\_hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed#complex_key_sparse_hashed) Like `sparse_hashed`, for composite keys.| [hashed\_array](/docs/sql-reference/statements/create/dictionary/layouts/hashed-array) Attributes stored in arrays with a hash table mapping keys to array indices. Memory\-efficient for many attributes.| [complex\_key\_hashed\_array](/docs/sql-reference/statements/create/dictionary/layouts/hashed-array#complex_key_hashed_array) Like `hashed_array`, for composite keys.| [range\_hashed](/docs/sql-reference/statements/create/dictionary/layouts/range-hashed) Hash table with ordered ranges. Supports lookups by key \+ date/time range.| [complex\_key\_range\_hashed](/docs/sql-reference/statements/create/dictionary/layouts/range-hashed#complex_key_range_hashed) Like `range_hashed`, for composite keys.| [cache](/docs/sql-reference/statements/create/dictionary/layouts/cache) Fixed\-size in\-memory cache. Only frequently accessed keys are stored.| [complex\_key\_cache](/docs/sql-reference/statements/create/dictionary/layouts/hashed#complex_key_hashed) Like `cache`, for composite keys.| [ssd\_cache](/docs/sql-reference/statements/create/dictionary/layouts/ssd-cache) Like `cache`, but stores data on SSD with an in\-memory index.| [complex\_key\_ssd\_cache](/docs/sql-reference/statements/create/dictionary/layouts/ssd-cache#complex_key_ssd_cache) Like `ssd_cache`, for composite keys.| [direct](/docs/sql-reference/statements/create/dictionary/layouts/direct) No in\-memory storage — queries the source directly for each request.| [complex\_key\_direct](/docs/sql-reference/statements/create/dictionary/layouts/direct#complex_key_direct) Like `direct`, for composite keys.| [ip\_trie](/docs/sql-reference/statements/create/dictionary/layouts/ip-trie) Trie structure for fast IP prefix lookups (CIDR\-based). | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |


Recommended layouts[flat](/docs/sql-reference/statements/create/dictionary/layouts/flat), [hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed), and [complex\_key\_hashed](/docs/sql-reference/statements/create/dictionary/layouts/hashed#complex_key_hashed) provide the best query performance.
Caching layouts are not recommended due to potentially poor performance and difficulty tuning parameters — see [cache](/docs/sql-reference/statements/create/dictionary/layouts/cache) for details.


## Specify dictionary layout[​](#specify-dictionary-layout "Direct link to Specify dictionary layout")


TipIf you are using a dictionary with ClickHouse Cloud please use the DDL query option to create your dictionaries, and create your dictionary as user `default`.
Also, verify the list of supported dictionary sources in the [Cloud Compatibility guide](/docs/whats-new/cloud-compatibility).


You can configure a dictionary layout with the `LAYOUT` clause (for DDL) or the `layout` setting for configuration file definitions.


- DDL- Configuration file


```
CREATE DICTIONARY (...)
...
LAYOUT(LAYOUT_TYPE(param value)) -- layout settings
...

```

```
<clickhouse>
    <dictionary>
        ...
        <layout>
            <layout_type>
                <!-- layout settings -->
            </layout_type>
        </layout>
        ...
    </dictionary>
</clickhouse>

```

  

See also [CREATE DICTIONARY](/docs/sql-reference/statements/create/dictionary) for the full DDL syntax.


Dictionaries without word `complex-key*` in a layout have a key with [UInt64](/docs/sql-reference/data-types/int-uint) type, `complex-key*` dictionaries have a composite key (complex, with arbitrary types).


**Numeric key example** (column key\_column has [UInt64](/docs/sql-reference/data-types/int-uint) type):


- DDL- Configuration file


```
CREATE DICTIONARY dict_name (
    key_column UInt64,
    ...
)
PRIMARY KEY key_column

```

```
<structure>
    <id>
        <name>key_column</name>
    </id>
    ...
</structure>

```

  

**Composite key example** (key has one element with [String](/docs/sql-reference/data-types/string) type):


- DDL- Configuration file


```
CREATE DICTIONARY dict_name (
    country_code String,
    ...
)
PRIMARY KEY country_code

```

```
<structure>
    <key>
        <attribute>
            <name>country_code</name>
            <type>String</type>
        </attribute>
    </key>
    ...
</structure>

```

## Improve dictionary performance[​](#improve-performance "Direct link to Improve dictionary performance")


There are several ways to improve dictionary performance:


- Call the function for working with the dictionary after `GROUP BY`.
- Mark attributes to extract as injective.
An attribute is called injective if different keys correspond to different attribute values.
So when `GROUP BY` uses a function that fetches an attribute value by the key, this function is automatically taken out of `GROUP BY`.


ClickHouse generates an exception for errors with dictionaries.
Examples of errors can be:


- The dictionary being accessed could not be loaded.
- Error querying a `cached` dictionary.


You can view the list of dictionaries and their statuses in the [system.dictionaries](/docs/operations/system-tables/dictionaries) table.

[PreviousYAMLRegExpTree](/docs/sql-reference/statements/create/dictionary/sources/yamlregexptree)[Nextflat](/docs/sql-reference/statements/create/dictionary/layouts/flat)- [Dictionary layout types](#storing-dictionaries-in-memory)- [Specify dictionary layout](#specify-dictionary-layout)- [Improve dictionary performance](#improve-performance)
Was this page helpful?
