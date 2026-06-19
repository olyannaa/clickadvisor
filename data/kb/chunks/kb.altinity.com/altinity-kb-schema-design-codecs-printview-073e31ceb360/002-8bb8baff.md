---
source: kb.altinity.com
url: https://userweb.cs.txstate.edu/~burtscher/papers/dcc07a.pdf
topic: codecs-altinity-knowledge-base-for-clickhouse
ch_version_introduced: '3.386'
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 4
---

cardinality | | NONE | Non\-compressable data with very high entropy, like some random string, or some AggregateFunction states | No compression at all. Can be used on the columns that can not be compressed anyway. | See

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
