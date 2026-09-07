---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Exploring
topic: exploring-global-internet-speeds-using-apache-iceberg-and-clickhouse-clickhouse
ch_version_introduced: '0.216'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 21
---

ability to query Iceberg files from ClickHouse. As a lake house format, this is currently supported through a dedicated table [iceberg](https://clickhouse.com/docs/en/sql-reference/table-functions/iceberg) function. This assumes the data is hosted on an S3\-compliant service such as AWS S3 or Minio.

For our examples, we’ve made the Ookla dataset available in the following public S3 bucket for users to experiment.

[s3://datasets\-documentation/ookla/iceberg/](https://datasets-documentation.s3.eu-west-3.amazonaws.com/ookla/iceberg/)

We can describe the schema of the Ookla data using a DESCRIBE query with the iceberg function replacing our table name. Unlike Parquet, which relies on sampling the actual data, the schema is read from the Iceberg metadata files.

```
1DESCRIBE TABLE iceberg('https://datasets-documentation.s3.eu-west-3.amazonaws.com/ookla/iceberg/')
2SETTINGS describe_compact_output = 1
3
4┌─name────────────┬─type─────────────┐
5│ quadkey     	  │ Nullable(String) │
6│ tile        	  │ Nullable(String) │
7│ avg_d_kbps  	  │ Nullable(Int32)  │
8│ avg_u_kbps  	  │ Nullable(Int32)  │
9│ avg_lat_ms  	  │ Nullable(Int32)  │
10│ avg_lat_down_ms │ Nullable(Int32)  │
11│ avg_lat_up_ms   │ Nullable(Int32)  │
12│ tests       	  │ Nullable(Int32)  │
13│ devices     	  │ Nullable(Int32)  │
14│ year_month  	  │ Nullable(Date)   │
15└─────────────────┴──────────────────┘
16
1710 rows in set. Elapsed: 0.216 sec.
```
Copy command
Similarly, querying rows can be performed with standard SQL with the table function replacing the table name. In the following, we sample some rows and count the total size of the data set.

```
1SELECT *
2FROM iceberg('https://datasets-documentation.s3.eu-west-3.amazonaws.com/ookla/iceberg/')
3LIMIT 1
4FORMAT Vertical
5
6Row 1:
7──────
8quadkey:     	1202021303331311
9tile:        	POLYGON((4.9163818359375 51.2206474303833, 4.921875 51.2206474303833, 4.921875 51.2172068072334, 4.9163818359375 51.2172068072334, 4.9163818359375 51.2206474303833))
10avg_d_kbps:  	109291
11avg_u_kbps:  	15426
12avg_lat_ms:  	12
13avg_lat_down_ms: ᴺᵁᴸᴸ
14avg_lat_up_ms:   ᴺᵁᴸᴸ
15tests:       	6
16devices:     	4
17year_month:  	2021-06-01
18
191 row in set. Elapsed: 2.100 sec. Processed 8.19 thousand rows, 232.12 KB (3.90 thousand rows/s., 110.52 KB/s.)
20Peak memory usage: 4.09 MiB.
21
22
23SELECT count()
24FROM iceberg('https://datasets-documentation.s3.eu-west-3.amazonaws.com/ookla/iceberg/')
25
26┌───count()─┐
27│ 128006990 │
28└───────────┘
29
301 row in set. Elapsed: 0.701 sec. Processed 128.01 million rows, 21.55 KB (182.68 million rows/s., 30.75 KB/s.)
31Peak memory usage: 4.09 MiB
```
Copy command
We can see that Ookla divides the surface of the earth into Polygons using the [WKT format](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry). We’ll delve into this in the 2nd half of the blog; for now, we’ll complete our simple examples with an aggregation computing the average number of devices per polygon and the median, 90th, 99th, and 99\.9th quantiles for download speed.
