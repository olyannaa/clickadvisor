---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-release-24-5-clickhouse
ch_version_introduced: '23.5'
last_updated: '2026-09-07'
chunk_index: 5
total_chunks_in_doc: 9
---

3629. │ umbrella-static/top-1m-2024-01-29.csv.zip::top-1m.csv │ 3730. │ umbrella-static/top-1m-2024-01-30.csv.zip::top-1m.csv │ 3831. │ umbrella-static/top-1m-2024-01-31.csv.zip::top-1m.csv │ 39 └───────────────────────────────────────────────────────┘ ``` Copy command So, we have 31 files to work with. Let’s next compute how many rows of data there are across those files:

```
1SELECT
2    _path,
3    count()
4FROM s3('s3://umbrella-static/top-1m-2024-01-*.csv.zip :: *.csv', CSV)
5GROUP BY _path
6
7Query id: 07de510c-229f-4223-aeb9-b2cd36224228
8
9    ┌─_path─────────────────────────────────────────────────┬─count()─┐
10 1. │ umbrella-static/top-1m-2024-01-21.csv.zip::top-1m.csv │ 1000000 │
11 2. │ umbrella-static/top-1m-2024-01-07.csv.zip::top-1m.csv │ 1000000 │
12 3. │ umbrella-static/top-1m-2024-01-30.csv.zip::top-1m.csv │ 1000000 │
13 4. │ umbrella-static/top-1m-2024-01-16.csv.zip::top-1m.csv │ 1000000 │
14 5. │ umbrella-static/top-1m-2024-01-10.csv.zip::top-1m.csv │ 1000000 │
15 6. │ umbrella-static/top-1m-2024-01-27.csv.zip::top-1m.csv │ 1000000 │
16 7. │ umbrella-static/top-1m-2024-01-01.csv.zip::top-1m.csv │ 1000000 │
17 8. │ umbrella-static/top-1m-2024-01-29.csv.zip::top-1m.csv │ 1000000 │
18 9. │ umbrella-static/top-1m-2024-01-13.csv.zip::top-1m.csv │ 1000000 │
1910. │ umbrella-static/top-1m-2024-01-24.csv.zip::top-1m.csv │ 1000000 │
2011. │ umbrella-static/top-1m-2024-01-02.csv.zip::top-1m.csv │ 1000000 │
2112. │ umbrella-static/top-1m-2024-01-22.csv.zip::top-1m.csv │ 1000000 │
2213. │ umbrella-static/top-1m-2024-01-18.csv.zip::top-1m.csv │ 1000000 │
2314. │ umbrella-static/top-1m-2024-01-04.csv.zip::top-1m.csv │ 1000001 │
2415. │ umbrella-static/top-1m-2024-01-15.csv.zip::top-1m.csv │ 1000000 │
2516. │ umbrella-static/top-1m-2024-01-09.csv.zip::top-1m.csv │ 1000000 │
2617. │ umbrella-static/top-1m-2024-01-06.csv.zip::top-1m.csv │ 1000000 │
2718. │ umbrella-static/top-1m-2024-01-20.csv.zip::top-1m.csv │ 1000000 │
2819. │ umbrella-static/top-1m-2024-01-17.csv.zip::top-1m.csv │ 1000000 │
2920. │ umbrella-static/top-1m-2024-01-31.csv.zip::top-1m.csv │ 1000000 │
3021. │ umbrella-static/top-1m-2024-01-11.csv.zip::top-1m.csv │ 1000000 │
3122. │ umbrella-static/top-1m-2024-01-26.csv.zip::top-1m.csv │ 1000000 │
3223. │ umbrella-static/top-1m-2024-01-12.csv.zip::top-1m.csv │ 1000000 │
3324. │ umbrella-static/top-1m-2024-01-28.csv.zip::top-1m.csv │ 1000000 │
3425. │ umbrella-static/top-1m-2024-01-03.csv.zip::top-1m.csv │ 1000001 │
3526. │ umbrella-static/top-1m-2024-01-25.csv.zip::top-1m.csv │ 1000000 │
3627. │ umbrella-static/top-1m-2024-01-05.csv.zip::top-1m.csv │ 1000000 │
3728. │ umbrella-static/top-1m-2024-01-19.csv.zip::top-1m.csv │ 1000000 │
3829. │ umbrella-static/top-1m-2024-01-23.csv.zip::top-1m.csv │ 1000000 │
3930. │ umbrella-static/top-1m-2024-01-08.csv.zip::top-1m.csv │ 1000000 │
4031. │ umbrella-static/top-1m-2024-01-14.csv.zip::top-1m.csv │ 1000000 │
41    └───────────────────────────────────────────────────────┴─────────┘
```
Copy command
We have more or less 1 million rows per file. Let’s have a look at some of the rows. We can use the `DESCRIBE` clause to understand the structure of the data:

```
1DESCRIBE TABLE s3('s3://umbrella-static/top-1m-2024-01-*.csv.zip :: *.csv', CSV)
2SETTINGS describe_compact_output = 1
3
4Query id: d5afed03-6c51-40f4-b457-1065479ef1a8
5
6   ┌─name─┬─type─────────────┐
71. │ c1   │ Nullable(Int64)  │
82. │ c2   │ Nullable(String) │
9   └──────┴──────────────────┘
```
Copy command
Finally, let’s have a look at a few of the rows themselves:
