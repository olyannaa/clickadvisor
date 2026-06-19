# Dictionaries \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-dictionaries/).

# Dictionaries

All you need to know about creating and using ClickHouse® dictionaries.- 1: [Dictionaries \& arrays](#pg-7c23334e7ea6259092cf879644c13202)
- 2: [Dictionary on the top of several tables using VIEW](#pg-c6ab71f7b0464306ca8e92cd1b20a16f)
- 3: [Dimension table design](#pg-2117d04b5ec50d240f3b8d4771f4e0cf)
- 4: [Example of PostgreSQL dictionary](#pg-5a4c8ba666fe62e656f9162f029567b5)
- 5: [MySQL8 source for dictionaries](#pg-fbd7b5147bf5a7fd7cea90035d5bd64f)
- 6: [Partial updates](#pg-1144a6bdbea0340938bf342303bf558b)
- 7: [range\_hashed example \- open intervals](#pg-db7055c09ac5c6fe393fe6f28ca762fd)
- 8: [Security named collections](#pg-a0c02f36f9f6b73008baf83f1e1839a0)
- 9: [SPARSE\_HASHED VS HASHED vs HASHED\_ARRAY](#pg-93e3691f2e69dd66e3f5d00be522ba05)

For more information on ClickHouse® Dictionaries, see

the presentation [https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup34/clickhouse\_integration.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup34/clickhouse_integration.pdf)
, slides 82\-95, video [https://youtu.be/728Yywcd5ys?t\=10642](https://youtu.be/728Yywcd5ys?t=10642)

We have also couple of articles about dictionaries in our blog:
[https://altinity.com/blog/dictionaries\-explained](https://altinity.com/blog/dictionaries-explained)
[https://altinity.com/blog/2020/5/19/clickhouse\-dictionaries\-reloaded](https://altinity.com/blog/2020/5/19/clickhouse-dictionaries-reloaded)

And some videos:
[https://www.youtube.com/watch?v\=FsVrFbcyb84](https://www.youtube.com/watch?v=FsVrFbcyb84)

# 1 \- Dictionaries \& arrays

Dictionaries \& arrays## Dictionary with ClickHouse® table as a source

### Test data


```
DROP TABLE IF EXISTS arr_src;
CREATE TABLE arr_src
(
    key UInt64,
    array_int Array(Int64),
    array_str Array(String)
) ENGINE = MergeTree order by key;

INSERT INTO arr_src SELECT
    number,
    arrayMap(i -> (number * i), range(5)),
    arrayMap(i -> concat('str', toString(number * i)), range(5))
FROM numbers(1000);

```
### Dictionary


```
DROP DICTIONARY IF EXISTS arr_dict;
CREATE DICTIONARY arr_dict
(
    key UInt64,
    array_int Array(Int64) DEFAULT [1,2,3],
    array_str Array(String) DEFAULT ['1','2','3']
)
PRIMARY KEY key
SOURCE(CLICKHOUSE(DATABASE 'default' TABLE 'arr_src'))
LIFETIME(120)
LAYOUT(HASHED());

SELECT
    dictGet('arr_dict', 'array_int', toUInt64(42)) AS res_int,
    dictGetOrDefault('arr_dict', 'array_str', toUInt64(424242), ['none']) AS res_str

┌─res_int───────────┬─res_str──┐
│ [0,42,84,126,168] │ ['none'] │
└───────────────────┴──────────┘

```
## Dictionary with PostgreSQL as a source

### Test data in PG


```
create user ch;
create database ch;
GRANT ALL PRIVILEGES ON DATABASE ch TO ch;
ALTER USER ch WITH PASSWORD 'chch';

CREATE TABLE arr_src (
    key int,
    array_int   integer[],
    array_str   text[]
);

INSERT INTO arr_src VALUES
  (42, '{0,42,84,126,168}','{"str0","str42","str84","str126","str168"}'),
  (66, '{0,66,132,198,264}','{"str0","str66","str132","str198","str264"}');

```
### Dictionary Example


```
CREATE DICTIONARY pg_arr_dict
(
    key UInt64,
    array_int Array(Int64) DEFAULT [1,2,3],
    array_str Array(String) DEFAULT ['1','2','3']
)
PRIMARY KEY key
SOURCE(POSTGRESQL(PORT 5432 HOST 'pg-host'
         user 'ch' password 'chch'  DATABASE  'ch' TABLE 'arr_src'))
LIFETIME(120)
LAYOUT(HASHED());

select * from pg_arr_dict;
┌─key─┬─array_int──────────┬─array_str───────────────────────────────────┐
│  66 │ [0,66,132,198,264] │ ['str0','str66','str132','str198','str264'] │
│  42 │ [0,42,84,126,168]  │ ['str0','str42','str84','str126','str168']  │
└─────┴────────────────────┴─────────────────────────────────────────────┘

SELECT
    dictGet('pg_arr_dict', 'array_int', toUInt64(42)) AS res_int,
    dictGetOrDefault('pg_arr_dict', 'array_str', toUInt64(424242), ['none']) AS res_str

┌─res_int───────────┬─res_str──┐
│ [0,42,84,126,168] │ ['none'] │
└───────────────────┴──────────┘

```
## Dictionary with MySQL as a source

### Test data in MySQL


```
-- casted into CH Arrays

create table arr_src(
   _key bigint(20) NOT NULL, 
   _array_int text, 
   _array_str text, 
   PRIMARY KEY(_key)
);

INSERT INTO arr_src VALUES 
  (42, '[0,42,84,126,168]','[''str0'',''str42'',''str84'',''str126'',''str168'']'),
  (66, '[0,66,132,198,264]','[''str0'',''str66'',''str132'',''str198'',''str264'']');

```
### Dictionary in MySQL


```
-- supporting table to cast data
CREATE TABLE arr_src
(
    `_key` UInt8,
    `_array_int` String,
    `array_int` Array(Int32) ALIAS cast(_array_int, 'Array(Int32)'),
    `_array_str` String,
    `array_str` Array(String) ALIAS cast(_array_str, 'Array(String)')
)
ENGINE = MySQL('mysql_host', 'ch', 'arr_src', 'ch', 'pass');

-- dictionary fetches data from the supporting table
CREATE DICTIONARY mysql_arr_dict
(
    _key UInt64,
    array_int Array(Int64) DEFAULT [1,2,3],
    array_str Array(String) DEFAULT ['1','2','3']
)
PRIMARY KEY _key
SOURCE(CLICKHOUSE(DATABASE 'default' TABLE 'arr_src'))
LIFETIME(120)
LAYOUT(HASHED());


select * from mysql_arr_dict;
┌─_key─┬─array_int──────────┬─array_str───────────────────────────────────┐
│   66 │ [0,66,132,198,264] │ ['str0','str66','str132','str198','str264'] │
│   42 │ [0,42,84,126,168]  │ ['str0','str42','str84','str126','str168']  │
└──────┴────────────────────┴─────────────────────────────────────────────┘


SELECT
    dictGet('mysql_arr_dict', 'array_int', toUInt64(42)) AS res_int,
    dictGetOrDefault('mysql_arr_dict', 'array_str', toUInt64(424242), ['none']) AS res_str

┌─res_int───────────┬─res_str──┐
│ [0,42,84,126,168] │ ['none'] │
└───────────────────┴──────────┘

SELECT
    dictGet('mysql_arr_dict', 'array_int', toUInt64(66)) AS res_int,
    dictGetOrDefault('mysql_arr_dict', 'array_str', toUInt64(66), ['none']) AS res_str

┌─res_int────────────┬─res_str─────────────────────────────────────┐
│ [0,66,132,198,264] │ ['str0','str66','str132','str198','str264'] │
└────────────────────┴─────────────────────────────────────────────┘

```
# 2 \- Dictionary on the top of several tables using VIEW

Dictionary on the top of several tables using VIEW
```

DROP TABLE IF EXISTS dictionary_source_en;
DROP TABLE IF EXISTS dictionary_source_ru;
DROP TABLE IF EXISTS dictionary_source_view;
DROP DICTIONARY IF EXISTS flat_dictionary;

CREATE TABLE dictionary_source_en
(
    id UInt64,
    value String
) ENGINE = TinyLog;

INSERT INTO dictionary_source_en VALUES (1, 'One'), (2,'Two'), (3, 'Three');

CREATE TABLE dictionary_source_ru
(
    id UInt64,
    value String
) ENGINE = TinyLog;

INSERT INTO dictionary_source_ru VALUES (1, 'Один'), (2,'Два'), (3, 'Три');

CREATE VIEW dictionary_source_view AS  SELECT id, dictionary_source_en.value as value_en, dictionary_source_ru.value as value_ru  FROM  dictionary_source_en LEFT JOIN dictionary_source_ru USING (id);

select * from dictionary_source_view;

CREATE DICTIONARY flat_dictionary
(
    id UInt64,
    value_en String,
    value_ru String
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' PASSWORD '' TABLE 'dictionary_source_view'))
LIFETIME(MIN 1 MAX 1000)
LAYOUT(FLAT());

SELECT
    dictGet(concat(currentDatabase(), '.flat_dictionary'), 'value_en', number + 1),
    dictGet(concat(currentDatabase(), '.flat_dictionary'), 'value_ru', number + 1)
FROM numbers(3);

```
# 3 \- Dimension table design

Dimension table design## Dimension table design considerations

### Choosing storage Engine

To optimize the performance of reporting queries, dimensional tables should be loaded into RAM as ClickHouse Dictionaries whenever feasible. It’s becoming increasingly common to allocate 100\-200GB of RAM per server specifically for these Dictionaries. Implementing sharding by tenant can further reduce the size of these dimension tables, enabling a greater portion of them to be stored in RAM and thus enhancing query speed.

Different Dictionary Layouts can take more or less RAM (in trade for speed).

- The cached dictionary layout is ideal for minimizing the amount of RAM required to store dimensional data when the hit ratio is high. This layout allows frequently accessed data to be kept in RAM while less frequently accessed data is stored on disk, thereby optimizing memory usage without sacrificing performance.
- HASHED\_ARRAY or SPARSE\_HASHED dictionary layouts take less RAM than HASHED. See tests [here](https://kb.altinity.com/altinity-kb-dictionaries/altinity-kb-sparse_hashed-vs-hashed/)
.
- Normalization techniques can be used to lower RAM usage (see below)

If the amount of data is so high that it does not fit in the RAM even after suitable sharding, a disk\-based table with an appropriate engine and its parameters can be used for accessing dimensional data in report queries.

MergeTree engines (including Replacing or Aggregating) are not tuned by default for point queries due to the high index granularity (8192\) and the necessity of using FINAL (or GROUP BY) when accessing mutated data.

When using the MergeTree engine for Dimensions, the table’s index granularity should be lowered to 256\. More RAM will be used for PK, but it’s a reasonable price for reading less data from the disk and making report queries faster, and that amount can be lowered by lightweight PK design (see below).

The `EmbeddedRocksDB` engine could be used as an alternative. It performs much better than ReplacingMergeTree for highly mutated data, as it is tuned by design for random point queries and high\-frequency updates. However, EmbeddedRocksDB does not support Replication, so INSERTing data to such tables should be done over a Distributed table with `internal_replication` set to false, which is vulnerable to different desync problems. Some “sync” procedures should be designed, developed, and applied after serious data ingesting incidents (like ETL crashes).

When the Dimension table is built on several incoming event streams, `AggregatingMergeTree` is preferable to `ReplacingMergeTree`, as it allows putting data from different event streams without external ETL processes:


```
CREATE TABLE table_C (
    id      UInt64,
    colA    SimpleAggregatingFunction(any,Nullable(UInt32)),
    colB    SimpleAggregatingFunction(max, String)
) ENGINE = AggregatingMergeTree()
PARTITION BY intDiv(id, 0x800000000000000) /* 32 bucket*/
ORDER BY id;

CREATE MATERIALIZED VIEW mv_A TO table_C AS SELECT id,colA FROM Kafka_A;
CREATE MATERIALIZED VIEW mv_B TO table_C AS SELECT id,colB FROM Kafka_B;

```
EmbeddedRocksDB natively supports UPDATEs without any complications with AggregatingFunctions.

For dimensions where some “start date” column is used in filtering, the [Range\_Hashed](https://kb.altinity.com/altinity-kb-dictionaries/altinity-kb-range_hashed-example-open-intervals/)
dictionary layout can be used if it is acceptable for RAM usage. For MergeTree variants, ASOF JOIN in queries is needed. Such types of dimensions are the first candidates for placement into RAM.

EmbeddedRocksDB is not suitable here.

### Primary Key

To increase query performance, I recommend using a single UInt64 (not String) column for PK, where the upper 32 bits are reserved for tenant\_id (shop\_id) and the lower 32 bits for actual object\_id (like customer\_id, product\_id, etc.)

That benefits both EmbeddedRocksDB Engine (it can have only one Primary Key column) and ReplacingMergeTree, as FINAL processing will work much faster with a light ORDER BY column of a single UInt64 value.

### Direct Dictionary and UDFs

To make the SQL code of report queries more readable and manageable, I recommend always using Dictionaries to access dimensions. A `direct dictionary layout` should be used for disk\-stored dimensions (EmbeddedRocksDB or \*MergeTree).

When Clickhouse builds a query to Direct Dictionary, it automatically creates a filter with a list of all needed ID values. There is no need to write code to filter necessary dimension rows to reduce the hash table for the right join table.

Another trick for code manageability is creating an interface function for every dimension to place here all the complexity of managing IDs by packing several values into a single PK value:


```
create or replace function getCustomer as (shop, id, attr) ->
    dictGetOrNull('dict_Customers', attr, bitOr((bitShiftLeft(toUInt64(shop),32)),id));

```
It also allows the flexibility of changing dictionary names when testing different types of Engines or can be used to spread dimensional data to several dictionaries. F.e. most active tenants can be served by expensive in\-RAM dictionary, while others (not active) tenants will be served from disk.


```
create or replace function getCustomer as (shop, id, attr) ->
    dictGetOrDefault('dict_Customers_RAM', attr, bitOr((bitShiftLeft(toUInt64(shop),32)),id) as key,
    dictGetOrNull('dict_Customers_MT', attr, key));

```
We always recommended DENORMALIZATION for Fact tables. However, NORMALIZATION is still a usable approach for taking less RAM for Dimension data stored as dictionaries.

Example of storing a long company name (String) in a separate dictionary:


```
create or replace function getCustomer as (shop, id, attr) ->
    if(attr='company_name', 
        dictGetOrDefault('dict_Company_name', 'name',
         dictGetOrNull('dict_Customers', 'company_id', 
            bitOr((bitShiftLeft(toUInt64(shop),32)),id)) as key),
        dictGetOrNull('dict_Customers', attr, key)
    );

```
Example of combining Hash and Direct Dictionaries. Allows to increase lifetime without losing consistency.


```
CREATE OR REPLACE FUNCTION getProduct AS (product_id, attr) ->
    dictGetOrDefault('hashed_dictionary', attr,(shop_id, product_id),
        dictGet('direct_dictionary',attr,(shop_id, product_id) )
    );

```
### Tests/Examples

EmbeddedRocksDB


```
CREATE TABLE Dim_Customers (
    id UInt64,
    name String,
    new_or_returning bool
) ENGINE = EmbeddedRocksDB()
PRIMARY KEY (id);

INSERT INTO Dim_Customers
SELECT bitShiftLeft(3648061509::UInt64,32)+number,
  ['Customer A', 'Customer B', 'Customer C', 'Customer D', 'Customer E'][number % 5 + 1],
  number % 2 = 0
FROM numbers(100);

CREATE DICTIONARY dict_Customers
(
    id UInt64,
    name String,
    new_or_returning bool
)
PRIMARY KEY id
LAYOUT(DIRECT())
SOURCE(CLICKHOUSE(TABLE 'Dim_Customers'));

select dictGetOrNull('dict_Customers', 'name', 
  bitOr((bitShiftLeft(toUInt64(shop_id),32)),customer_id));

```
ReplacingMergeTree


```
CREATE TABLE Dim_Customers (
    id UInt64, 
    name String,
    new_or_returning bool
) ENGINE = ReplacingMergeTree()
ORDER BY id
PARTITION BY intDiv(id, 0x800000000000000) /* 32 buckets by shop_id */
settings index_granularity=256;

CREATE DICTIONARY dict_Customers
(
    id UInt64,
    name String,
    new_or_returning bool
)
PRIMARY KEY id
LAYOUT(DIRECT())
SOURCE(CLICKHOUSE(query 'select * from Dim_Customers FINAL'));

set do_not_merge_across_partitions_select_final=1; -- or place it to profile
select dictGet('dict_Customers','name',bitShiftLeft(3648061509::UInt64,32)+1);

```
Tests 1M random reads over 10M entries per shop\_id in the Dimension table

- [EmbeddedRocksDB](https://fiddle.clickhouse.com/c304d0cc-f1c2-4323-bd65-ab82165aecb6)
\- 0\.003s
- [ReplacingMergeTree](https://fiddle.clickhouse.com/093fc133-0685-4c97-aa90-d38200f93f9f)
\- 0\.003s

There is no difference in SELECT on that synthetic test with all MergeTree optimizations applied. The test must be rerun on actual data with the expected update volume. The difference could be seen on a table with high\-volume real\-time updates.

# 4 \- Example of PostgreSQL dictionary

Example of PostgreSQL dictionary
```
CREATE DICTIONARY postgres_dict
(
    id UInt32,
    value String
)
PRIMARY KEY id
SOURCE(
    POSTGRESQL(
        port 5432
        host 'postgres1'
        user  'postgres'
        password 'mysecretpassword'
        db 'clickhouse'
        table 'test_schema.test_table'
    )
)
LIFETIME(MIN 300 MAX 600)
LAYOUT(HASHED());

```
and later do


```
SELECT dictGetString(postgres_dict, 'value', toUInt64(1))

```
# 5 \- MySQL8 source for dictionaries

MySQL8 source for dictionaries#### Authorization

MySQL8 used default authorization plugin `caching_sha2_password`. Unfortunately, `libmysql` which currently used (21\.4\-) in ClickHouse® is not.

You can fix it during create custom user with `mysql_native_password` authentication plugin.


```
CREATE USER IF NOT EXISTS 'clickhouse'@'%'
IDENTIFIED WITH mysql_native_password BY 'clickhouse_user_password';

CREATE DATABASE IF NOT EXISTS test;

GRANT ALL PRIVILEGES ON test.* TO 'clickhouse'@'%';

```
#### Table schema changes

As an example, in ClickHouse, run `SHOW TABLE STATUS LIKE 'table_name'` and try to figure out was table schema changed or not from MySQL response field `Update_time`.

By default, to properly data loading from MySQL8 source to dictionaries, please turn off the `information_schema` cache.

You can change default behavior with create `/etc/mysql/conf.d/information_schema_cache.cnf`with following content:


```
[mysqld]
information_schema_stats_expiry=0

```
Or setup it via SQL query:


```
SET GLOBAL information_schema_stats_expiry=0;

```
# 6 \- Partial updates

Partial updatesClickHouse® is able to fetch from a source only updated rows. You need to define `update_field` section.

As an example, We have a table in an external source MySQL, PG, HTTP, … defined with the following code sample:


```
CREATE TABLE cities
(
    `polygon` Array(Tuple(Float64, Float64)),
    `city` String,
    `updated_at` DateTime DEFAULT now()
)
ENGINE = MergeTree ORDER BY city

```
When you add new row and `update` some rows in this table you should update `updated_at` with the new timestamp.


```
-- fetch updated rows every 30 seconds

CREATE DICTIONARY cities_dict (
    polygon Array(Tuple(Float64, Float64)),
    city String
)
PRIMARY KEY polygon
SOURCE(CLICKHOUSE( TABLE cities DB 'default'
                    update_field 'updated_at'))
LAYOUT(POLYGON())
LIFETIME(MIN 30 MAX 30)

```
A dictionary with **update\_field** `updated_at` will fetch only updated rows. A dictionary saves the current time (now) time of the last successful update and queries the source `where updated_at >= previous_update - 1` (shift \= 1 sec.).

In case of HTTP source ClickHouse will send get requests with **update\_field** as an URL parameter `&updated_at=2020-01-01%2000:01:01`

# 7 \- range\_hashed example \- open intervals

range\_hashed example \- open intervalsThe following example shows a `range_hashed` example at open intervals.


```
DROP TABLE IF EXISTS rates;

DROP DICTIONARY IF EXISTS rates_dict;

CREATE TABLE rates (
  id UInt64,
  date_start Nullable(Date),
  date_end Nullable(Date),
  rate Decimal64(4)
) engine=Log;

INSERT INTO rates VALUES (1, Null, '2021-03-13',99), (1, '2021-03-14','2021-03-16',100), (1, '2021-03-17', Null, 101), (2, '2021-03-14', Null, 200), (3, Null, '2021-03-14', 300), (4, '2021-03-14', '2021-03-14', 400);

CREATE DICTIONARY rates_dict
(
  id UInt64,
  date_start Date,
  date_end Date,
  rate Decimal64(4)
)
PRIMARY KEY id
SOURCE(CLICKHOUSE(HOST 'localhost' PORT 9000 USER 'default' TABLE 'rates'))
LIFETIME(MIN 1 MAX 1000)
LAYOUT(RANGE_HASHED())
RANGE(MIN date_start MAX date_end);

SELECT * FROM rates_dict order by id, date_start;

┌─id─┬─date_start─┬───date_end─┬─────rate─┐
│  1 │ 1970-01-01 │ 2021-03-13 │  99.0000 │
│  1 │ 2021-03-14 │ 2021-03-16 │ 100.0000 │
│  1 │ 2021-03-17 │ 1970-01-01 │ 101.0000 │
│  2 │ 2021-03-14 │ 1970-01-01 │ 200.0000 │
│  3 │ 1970-01-01 │ 2021-03-14 │ 300.0000 │
│  4 │ 2021-03-14 │ 2021-03-14 │ 400.0000 │
└────┴────────────┴────────────┴──────────┘

WITH
  toDate('2021-03-10') + INTERVAL number DAY as date
select
  date,
  dictGet(currentDatabase() || '.rates_dict', 'rate', toUInt64(1), date) as rate1,
  dictGet(currentDatabase() || '.rates_dict', 'rate', toUInt64(2), date) as rate2,
  dictGet(currentDatabase() || '.rates_dict', 'rate', toUInt64(3), date) as rate3,
  dictGet(currentDatabase() || '.rates_dict', 'rate', toUInt64(4), date) as rate4
FROM numbers(10);

┌───────date─┬────rate1─┬────rate2─┬────rate3─┬────rate4─┐
│ 2021-03-10 │  99.0000 │   0.0000 │ 300.0000 │   0.0000 │
│ 2021-03-11 │  99.0000 │   0.0000 │ 300.0000 │   0.0000 │
│ 2021-03-12 │  99.0000 │   0.0000 │ 300.0000 │   0.0000 │
│ 2021-03-13 │  99.0000 │   0.0000 │ 300.0000 │   0.0000 │
│ 2021-03-14 │ 100.0000 │ 200.0000 │ 300.0000 │ 400.0000 │
│ 2021-03-15 │ 100.0000 │ 200.0000 │   0.0000 │   0.0000 │
│ 2021-03-16 │ 100.0000 │ 200.0000 │   0.0000 │   0.0000 │
│ 2021-03-17 │ 101.0000 │ 200.0000 │   0.0000 │   0.0000 │
│ 2021-03-18 │ 101.0000 │ 200.0000 │   0.0000 │   0.0000 │
│ 2021-03-19 │ 101.0000 │ 200.0000 │   0.0000 │   0.0000 │
└────────────┴──────────┴──────────┴──────────┴──────────┘

```
# 8 \- Security named collections

Security named collections## Dictionary with ClickHouse® table as a source with named collections

### Data for connecting to external sources can be stored in named collections


```
<clickhouse>
    <named_collections>
        <local_host>
            <host>localhost</host>
            <port>9000</port>
            <database>default</database>
            <user>ch_dict</user>
            <password>mypass</password>
        </local_host>
    </named_collections>
</clickhouse>

```
### Dictionary


```
DROP DICTIONARY IF EXISTS named_coll_dict;
CREATE DICTIONARY named_coll_dict
(
    key UInt64,
    val String
)
PRIMARY KEY key
SOURCE(CLICKHOUSE(NAME local_host TABLE my_table DB default))
LIFETIME(MIN 1 MAX 2)
LAYOUT(HASHED());

INSERT INTO my_table(key, val) VALUES(1, 'first row');

SELECT dictGet('named_coll_dict', 'b', 1);
┌─dictGet('named_coll_dict', 'b', 1)─┐
│ first row                          │
└────────────────────────────────────┘

```
# 9 \- SPARSE\_HASHED VS HASHED vs HASHED\_ARRAY

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
