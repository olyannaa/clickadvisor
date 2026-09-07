---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Building
topic: building-single-page-applications-with-clickhouse-clickhouse
ch_version_introduced: '1.1'
last_updated: '2026-09-07'
chunk_index: 6
total_chunks_in_doc: 16
---

GROUP BY project ORDER BY c DESC LIMIT 3 FORMAT JSON', 5 headers: { 6 'Authorization': `Basic ,[object Object],`, 7 'Content-Type': 'application/x-www-form-urlencoded' 8 } 9 }); 10 11const data = await response.json(); 12console.log(JSON.stringify(data, null, 2)); ``` Copy command

```
1{
2  "meta": [
3    {
4      "name": "project",
5      "type": "String"
6    },
7    {
8      "name": "c",
9      "type": "Int64"
10    }
11  ],
12  "data": [
13    {
14      "project": "boto3",
15      "c": "27234697969"
16    },
17    {
18      "project": "urllib3",
19      "c": "17015345004"
20    },
21    {
22      "project": "botocore",
23      "c": "15812406924"
24    }
25  ],
26  "rows": 3,
27  "rows_before_limit_at_least": 695858,
28  "statistics": {
29    "elapsed": 0.057031395,
30    "rows_read": 1046002,
31    "bytes_read": 32165070
32  }
33}
```
Copy command
There are variants of this format, such as <JSONObjectEachRow> and [JSONColumnsWithMetadata](https://clickhouse.com/docs/en/interfaces/formats#jsoncolumnsmonoblock), that users find easier to parse for their use case. These formats all return the response within an outer JSON object and thus require the entire payload to be parsed and loaded into memory. For smaller responses, this is rarely a concern. For larger formats, users may wish to consider a format from the `EachRow` family, which is more easily parsed with the [Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API) as shown in [this simple example](https://gist.github.com/gingerwizard/7ed6ffd76fb568ee8e24bce38ca9ce8a). These formats, such as [JSONEachRow](https://clickhouse.com/docs/en/interfaces/formats#jsoneachrow), [JSONCompactEachRow](https://clickhouse.com/docs/en/interfaces/formats#jsoncompacteachrow), and [JSONEachRowWithProgress](https://clickhouse.com/docs/en/interfaces/formats#jsoneachrowwithprogress), are not strictly well\-formatted JSON \- more representing NDJSON \- more can be read.

Other formats are variants of TSV and CSV, allowing data to be easily downloaded. For users requiring high performance on large data volumes, e.g., rendering in web assembly libraries such as [Perspective](https://perspective.finos.org/), ClickHouse additionally supports the Arrow and ArrowStream formats. For an example, see [here](https://clickhouse.com/blog/streaming-real-time-visualizations-clickhouse-apache-arrow-perpsective).

### Query statistics, sessions \& error handling \#

The ClickHouse HTTP interface allows query statistics to be sent as response headers describing the progress of the query. These can be tricky to read, and generally, we recommend using the format [`JSONEachRowWithProgress`](https://clickhouse.com/docs/en/interfaces/formats#jsoneachrowwithprogress) to obtain statistics on the progress of running queries.

Users can also read an `X-ClickHouse-Summary` header, which summarizes the read rows, bytes, and execution time.
