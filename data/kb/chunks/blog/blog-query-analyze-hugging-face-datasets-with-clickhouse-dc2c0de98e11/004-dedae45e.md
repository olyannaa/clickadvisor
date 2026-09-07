---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Analyzing
topic: analyzing-hugging-face-datasets-with-clickhouse-clickhouse
ch_version_introduced: '1.220'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 20
---

= 0`, introduced in 23\.7, ensures no decoding is applied to the URL \- the escape characters in the path are intentional and should be preserved. **For all subsequent queries assume these parameters are set in the session.**

> As well as requiring the addition of the parameter [enable\_url\_encoding for this blog post](https://github.com/ClickHouse/ClickHouse/pull/52337), we also found reading of Hugging Face Parquet files to be slower than expected with ClickHouse. This was attributed to small row groups, with a separate HTTP request made for each row group. This was resolved in issue [53069](https://github.com/ClickHouse/ClickHouse/issues/).

To simplify subsequent requests, we can create a url table engine to abstract the url. This allows us to query the dataset with the table `spotify` in all subsequent queries. This table will exist for the lifetime of the `clickhouse-local` session.

```
1SET max_http_get_redirects = 1
2SET enable_url_encoding = 0
3
4CREATE TABLE spotify
5ENGINE=URL('https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet') 
6
7SELECT count()
8FROM spotify
9
10┌─count()─┐
11│  114000 │
12└─────────┘
13
141 row in set. Elapsed: 0.838 sec. Processed 39.00 thousand rows, 4.51 MB (46.52 thousand rows/s., 5.37 MB/s.)
```
Copy command
**All queries below use the `spotify` table created above.**

### Exploring the dataset \#

To identify the columns available, we can rely on ClickHouse’s type inference capabilities and issue a [DESCRIBE](https://clickhouse.com/docs/en/sql-reference/statements/describe-table) query.

```
1DESCRIBE TABLE spotify
2
3┌─name─────────────┬─type──────────────┬
4│ Unnamed: 0   	│ Nullable(Int64)      │
5│ track_id     	│ Nullable(String)     │
6│ artists      	│ Nullable(String)     │
7│ album_name   	│ Nullable(String)     │
8│ track_name   	│ Nullable(String)     │
9│ popularity   	│ Nullable(Int64)      │
10│ duration_ms  	│ Nullable(Int64)      │
11│ explicit     	│ Nullable(Bool)	   │
12│ danceability 	│ Nullable(Float64)    │
13│ energy       	│ Nullable(Float64)    │
14│ key          	│ Nullable(Int64)      │
15│ loudness     	│ Nullable(Float64)    │
16│ mode         	│ Nullable(Int64)      │
17│ speechiness  	│ Nullable(Float64)    │
18│ acousticness 	│ Nullable(Float64)    │
19│ instrumentalness │ Nullable(Float64) │
20│ liveness     	│ Nullable(Float64)    │
21│ valence      	│ Nullable(Float64)    │
22│ tempo        	│ Nullable(Float64)    │
23│ time_signature   │ Nullable(Int64)   │
24│ track_genre  	│ Nullable(String)     │
25└──────────────────┴───────────────────┴
26
2721 rows in set. Elapsed: 0.000 sec.
```
Copy command
A full description of these columns is available [here](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset) for those interested. We’ll provide descriptions when using a column below and its content is not obvious.

## Simple queries \#
