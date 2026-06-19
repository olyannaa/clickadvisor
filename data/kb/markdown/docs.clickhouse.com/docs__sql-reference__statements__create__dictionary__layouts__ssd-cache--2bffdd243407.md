# ssd\_cache dictionary layout types \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- DICTIONARY- LAYOUT- ssd\_cache
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/dictionary/layouts/ssd-cache.md)# ssd\_cache dictionary layout types

## ssd\_cache[​](#ssd_cache "Direct link to ssd_cache")


Similar to `cache`, but stores data on SSD and index in RAM. All cache dictionary settings related to update queue can also be applied to SSD cache dictionaries.


The dictionary key has the [UInt64](/docs/sql-reference/data-types/int-uint) type.


- DDL- Configuration file


```
LAYOUT(SSD_CACHE(BLOCK_SIZE 4096 FILE_SIZE 16777216 READ_BUFFER_SIZE 1048576
    PATH '/var/lib/clickhouse/user_files/test_dict'))

```

```
<layout>
    <ssd_cache>
        <!-- Size of elementary read block in bytes. Recommended to be equal to SSD's page size. -->
        <block_size>4096</block_size>
        <!-- Max cache file size in bytes. -->
        <file_size>16777216</file_size>
        <!-- Size of RAM buffer in bytes for reading elements from SSD. -->
        <read_buffer_size>131072</read_buffer_size>
        <!-- Size of RAM buffer in bytes for aggregating elements before flushing to SSD. -->
        <write_buffer_size>1048576</write_buffer_size>
        <!-- Path where cache file will be stored. -->
        <path>/var/lib/clickhouse/user_files/test_dict</path>
    </ssd_cache>
</layout>

```

  

## complex\_key\_ssd\_cache[​](#complex_key_ssd_cache "Direct link to complex_key_ssd_cache")


This type of storage is for use with composite [keys](/docs/sql-reference/statements/create/dictionary/attributes#composite-key). Similar to `ssd_cache`.

[Previouscache](/docs/sql-reference/statements/create/dictionary/layouts/cache)[Nextdirect](/docs/sql-reference/statements/create/dictionary/layouts/direct)- [ssd\_cache](#ssd_cache)- [complex\_key\_ssd\_cache](#complex_key_ssd_cache)
Was this page helpful?
