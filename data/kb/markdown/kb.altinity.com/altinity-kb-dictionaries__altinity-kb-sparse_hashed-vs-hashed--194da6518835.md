# SPARSE\_HASHED VS HASHED vs HASHED\_ARRAY \| Altinity® Knowledge Base for ClickHouse®


1. [Dictionaries](/altinity-kb-dictionaries/)
2. SPARSE\_HASHED VS HASHED vs HASHED\_ARRAY
# SPARSE\_HASHED VS HASHED vs HASHED\_ARRAY

SPARSE\_HASHED VS HASHED VS HASHED\_ARRAYSparse\_hashed and hashed\_array layouts are supposed to save memory but has some downsides. We can test it with the following:


```
create table orders(id UInt64, price Float64)
Engine = MergeTree() order by id;

insert into orders select number, 0 from numbers(5000000);

CREATE DICTIONARY orders_hashed (id UInt64, price Float64)
PRIMARY KEY id SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000
TABLE orders DB 'default' USER 'default'))
LIFETIME(MIN 0 MAX 0) LAYOUT(HASHED());

CREATE DICTIONARY orders_sparse (id UInt64, price Float64)
PRIMARY KEY id SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000
TABLE orders DB 'default' USER 'default'))
LIFETIME(MIN 0 MAX 0) LAYOUT(SPARSE_HASHED());

CREATE DICTIONARY orders_hashed_array (id UInt64, price Float64)
PRIMARY KEY id SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000
TABLE orders DB 'default' USER 'default'))
LIFETIME(MIN 0 MAX 0) LAYOUT(HASHED_ARRAY());

SELECT
    name,
    type,
    status,
    element_count,
    formatReadableSize(bytes_allocated) AS RAM
FROM system.dictionaries
WHERE name LIKE 'orders%'
┌─name────────────────┬─type─────────┬─status─┬─element_count─┬─RAM────────┐
│ orders_hashed_array │ HashedArray  │ LOADED │       5000000 │ 68.77 MiB  │
│ orders_sparse       │ SparseHashed │ LOADED │       5000000 │ 76.30 MiB  │
│ orders_hashed       │ Hashed       │ LOADED │       5000000 │ 256.00 MiB │
└─────────────────────┴──────────────┴────────┴───────────────┴────────────┘

SELECT sum(dictGet('default.orders_hashed', 'price', toUInt64(number))) AS res
FROM numbers(10000000)
┌─res─┐
│   0 │
└─────┘
1 rows in set. Elapsed: 0.546 sec. Processed 10.01 million rows ...

SELECT sum(dictGet('default.orders_sparse', 'price', toUInt64(number))) AS res
FROM numbers(10000000)
┌─res─┐
│   0 │
└─────┘
1 rows in set. Elapsed: 1.422 sec. Processed 10.01 million rows ...

SELECT sum(dictGet('default.orders_hashed_array', 'price', toUInt64(number))) AS res
FROM numbers(10000000)
┌─res─┐
│   0 │
└─────┘
1 rows in set. Elapsed: 0.558 sec. Processed 10.01 million rows ...

```
As you can see **SPARSE\_HASHED** is memory efficient and use about 3 times less memory (!!!) but is almost 3 times slower as well. On the other side **HASHED\_ARRAY** is even more efficient in terms of memory usage and maintains almost the same performance as **HASHED** layout.

Last modified 2023\.01\.16: [Update altinity\-kb\-sparse\_hashed\-vs\-hashed.md (f047346\)](https://github.com/Altinity/altinityknowledgebase/commit/f047346f1a8dc17645102431bef41071c05fd03f)
