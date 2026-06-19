# Codecs \| Altinity® Knowledge Base for ClickHouse®


This is the multi\-page printable view of this section.
[Click here to print](#).

[Return to the regular view of this page](/altinity-kb-schema-design/codecs/).

# Codecs

Codecs- 1: [Codecs on array columns](#pg-969f346c16e2b280e2aa45ba85b689be)
- 2: [Codecs speed](#pg-dce00b858322605f3f48434154a40251)
- 3: [How to test different compression codecs](#pg-d7d0b3e12d54a31abbccb07fd95ecf8d)



| Codec Name | Recommended Data Types | Performance Notes |
| --- | --- | --- |
| LZ4 | Any | Used by default. Extremely fast; good compression; balanced speed and efficiency |
| ZSTD(level) | Any | Good compression; pretty fast; best for high compression needs. Don’t use levels higher than 3\. |
| LZ4HC(level) | Any | LZ4 High Compression algorithm with configurable level; slower but better compression than LZ4, but decompression is still fast. |
| Delta | Integer Types, Time Series Data, Timestamps | Preprocessor (should be followed by some compression codec). Stores difference between neighboring values; good for monotonically increasing data. |
| DoubleDelta | Integer Types, Time Series Data | Stores difference between neighboring delta values; suitable for time series data |
| Gorilla | Floating Point Types | Calculates XOR between current and previous value; suitable for slowly changing numbers |
| T64 | Integer, Time Series Data, Timestamps | Preprocessor (should be followed by some compression codec). Crops unused high bits; puts them into a 64x64 bit matrix; optimized for 64\-bit data types |
| GCD | Integer Numbers | Preprocessor (should be followed by some compression codec). Greatest common divisor compression; divides values by a common divisor; effective for divisible integer sequences |
| FPC | Floating Point Numbers | Designed for Float64; Algorithm detailed in [FPC paper](https://userweb.cs.txstate.edu/~burtscher/papers/dcc07a.pdf) , [ClickHouse® PR \#37553](https://github.com/ClickHouse/ClickHouse/pull/37553) |
| ZSTD\_QAT | Any | Requires hardware support for QuickAssist Technology (QAT) hardware; provides accelerated compression tasks |
| DEFLATE\_QPL | Any | Requires hardware support for Intel’s QuickAssist Technology for DEFLATE compression; enhanced performance for specific hardware |
| LowCardinality | String | It’s not a codec, but a datatype modifier. Reduces representation size; effective for columns with low cardinality |
| NONE | Non\-compressable data with very high entropy, like some random string, or some AggregateFunction states | No compression at all. Can be used on the columns that can not be compressed anyway. |

See

[How to test different compression codecs](altinity-kb-how-to-test-different-compression-codecs)

[https://altinity.com/blog/2019/7/new\-encodings\-to\-improve\-clickhouse](https://altinity.com/blog/2019/7/new-encodings-to-improve-clickhouse)

[https://www.percona.com/sites/default/files/ple19\-slides/day1\-pm/clickhouse\-for\-timeseries.pdf](https://www.percona.com/sites/default/files/ple19-slides/day1-pm/clickhouse-for-timeseries.pdf)

# 1 \- Codecs on array columns

Codecs on array columns#### Info

Supported since 20\.10 (PR [\#15089](https://github.com/ClickHouse/ClickHouse/pull/15089)
). On older versions you will get exception:
`DB::Exception: Codec Delta is not applicable for Array(UInt64) because the data type is not of fixed size.`
```
DROP TABLE IF EXISTS array_codec_test SYNC

create table array_codec_test( number UInt64, arr Array(UInt64) ) Engine=MergeTree ORDER BY number;
INSERT INTO array_codec_test SELECT number,  arrayMap(i -> number + i, range(100)) from numbers(10000000);


/****  Default LZ4  *****/

OPTIMIZE TABLE array_codec_test FINAL;
--- Elapsed: 3.386 sec.


SELECT * FROM system.columns WHERE (table = 'array_codec_test') AND (name = 'arr')
/*
Row 1:
──────
database:                default
table:                   array_codec_test
name:                    arr
type:                    Array(UInt64)
position:                2
default_kind:         
default_expression:   
data_compressed_bytes:   173866750
data_uncompressed_bytes: 8080000000
marks_bytes:             58656
comment:              
is_in_partition_key:     0
is_in_sorting_key:       0
is_in_primary_key:       0
is_in_sampling_key:      0
compression_codec:    
*/



/****** Delta, LZ4 ******/

ALTER TABLE array_codec_test MODIFY COLUMN arr Array(UInt64) CODEC (Delta, LZ4);

OPTIMIZE TABLE array_codec_test FINAL
--0 rows in set. Elapsed: 4.577 sec.

SELECT * FROM system.columns WHERE (table = 'array_codec_test') AND (name = 'arr')

/*
Row 1:
──────
database:                default
table:                   array_codec_test
name:                    arr
type:                    Array(UInt64)
position:                2
default_kind:         
default_expression:   
data_compressed_bytes:   32458310
data_uncompressed_bytes: 8080000000
marks_bytes:             58656
comment:              
is_in_partition_key:     0
is_in_sorting_key:       0
is_in_primary_key:       0
is_in_sampling_key:      0
compression_codec:       CODEC(Delta(8), LZ4)
*/

```
# 2 \- Codecs speed

Codecs speed
```
create table test_codec_speed engine=MergeTree
ORDER BY tuple()
as select cast(now() + rand()%2000 + number, 'DateTime') as x from numbers(1000000000);

option 1: CODEC(LZ4) (same as default)
option 2: CODEC(DoubleDelta) (`alter table test_codec_speed modify column x DateTime CODEC(DoubleDelta)`);
option 3: CODEC(T64, LZ4) (`alter table test_codec_speed modify column x DateTime CODEC(T64, LZ4)`)
option 4: CODEC(Delta, LZ4) (`alter table test_codec_speed modify column x DateTime CODEC(Delta, LZ4)`)
option 5: CODEC(ZSTD(1)) (`alter table test_codec_speed modify column x DateTime CODEC(ZSTD(1))`)
option 6: CODEC(T64, ZSTD(1)) (`alter table test_codec_speed modify column x DateTime CODEC(T64, ZSTD(1))`)
option 7: CODEC(Delta, ZSTD(1)) (`alter table test_codec_speed modify column x DateTime CODEC(Delta, ZSTD(1))`)
option 8: CODEC(T64, LZ4HC(1)) (`alter table test_codec_speed modify column x DateTime CODEC(T64, LZ4HC(1))`)
option 9: CODEC(Gorilla) (`alter table test_codec_speed modify column x DateTime CODEC(Gorilla)`)

Result may be not 100% reliable (checked on my laptop, need to be repeated in lab environment)


OPTIMIZE TABLE test_codec_speed FINAL (second run - i.e. read + write the same data)
1) 17 sec.
2) 30 sec.
3) 16 sec
4) 17 sec
5) 29 sec
6) 24 sec
7) 31 sec
8) 35 sec
9) 19 sec

compressed size
1) 3181376881
2) 2333793699
3) 1862660307
4) 3408502757
5) 2393078266
6) 1765556173
7) 2176080497
8) 1810471247
9) 2109640716

select max(x) from test_codec_speed
1) 0.597
2) 2.756 :(
3) 1.168
4) 0.752
5) 1.362
6) 1.364
7) 1.752
8) 1.270
9) 1.607

```
# 3 \- How to test different compression codecs

How to test different compression codecs## Example

Create test\_table based on the source table.


```
CREATE TABLE test_table AS source_table ENGINE=MergeTree() PARTITION BY ...;

```
If the source table has Replicated\*MergeTree engine, you would need to change it to non\-replicated.

Attach one partition with data from the source table to test\_table.


```
ALTER TABLE test_table ATTACH PARTITION ID '20210120' FROM source_table;

```
You can modify the column or create a new one based on the old column value.


```
ALTER TABLE test_table MODIFY COLUMN column_a CODEC(ZSTD(2));
ALTER TABLE test_table ADD COLUMN column_new UInt32
                         DEFAULT toUInt32OrZero(column_old) CODEC(T64,LZ4);

```
After that, you would need to populate changed columns with data.


```
ALTER TABLE test_table UPDATE column_a=column_a, column_new=column_new WHERE 1;

```
You can look status of mutation via the `system.mutations` table


```
SELECT * FROM system.mutations;

```
And it’s also possible to kill mutation if there are some problems with it.


```
KILL MUTATION WHERE ...

```
## Useful queries


```
SELECT
    database,
    table,
    count() AS parts,
    uniqExact(partition_id) AS partition_cnt,
    sum(rows),
    formatReadableSize(sum(data_compressed_bytes) AS comp_bytes) AS comp,
    formatReadableSize(sum(data_uncompressed_bytes) AS uncomp_bytes) AS uncomp,
    uncomp_bytes / comp_bytes AS ratio
FROM system.parts
WHERE active
GROUP BY
    database,
    table
ORDER BY comp_bytes DESC

```

```
SELECT
  database,
  table,
  column,
  type,
  sum(rows) AS rows,
  sum(column_data_compressed_bytes) AS compressed_bytes,
  formatReadableSize(compressed_bytes) AS compressed,
  formatReadableSize(sum(column_data_uncompressed_bytes)) AS uncompressed,
  sum(column_data_uncompressed_bytes) / compressed_bytes AS ratio,
  any(compression_codec) AS codec
FROM system.parts_columns AS pc
LEFT JOIN system.columns AS c
ON (pc.database = c.database) AND (c.table = pc.table) AND (c.name = pc.column)
WHERE (database LIKE '%') AND (table LIKE '%') AND active
GROUP BY
  database,
  table,
  column,
  type
ORDER BY database, table, sum(column_data_compressed_bytes) DESC

```
