---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Change
topic: change-data-capture-cdc-with-postgresql-and-clickhouse-part-2-clickhouse
ch_version_introduced: '80.885'
last_updated: '2026-09-07'
chunk_index: 9
total_chunks_in_doc: 19
---

rows in set. Elapsed: 80.885 sec. Processed 27.73 million rows, 5.63 GB (342.89 thousand rows/s., 69.60 MB/s.) ``` Copy command With no tuning we are able to load all 28m rows in 80 seconds. #### Materialized views \#

Debezium uses a nested JSON format to send messages. If configured appropriately (see below), with the `REPLICA IDENTITY` set to the `FULL`, change events will include the before and after values for a row's columns as nested JSON. Full examples of these messages can be found [here](https://github.com/ClickHouse/examples/tree/main/blog-examples/postgresql-cdc/messages), including if `REPLICA IDENTITY` is set to `DEFAULT` when delete support is not required.

As an example we show an update message below (`REPLICA IDENTITY=Full`).

```
1{
2  "before": {
3	"id": 50658675,
4	"price": 227500,
5	"date": 11905,
6	"postcode1": "SP2",
7	"postcode2": "7EN",
8	"type": "detached",
9	"is_new": 0,
10	"duration": "freehold",
11	"addr1": "31",
12	"addr2": "",
13	"street": "CHRISTIE MILLER ROAD",
14	"locality": "SALISBURY",
15	"town": "SALISBURY",
16	"district": "SALISBURY",
17	"county": "WILTSHIRE"
18  },
19  "after": {
20	"id": 50658675,
21	"price": 227500,
22	"date": 11905,
23	"postcode1": "SP2",
24	"postcode2": "7EN",
25	"type": "terraced",
26	"is_new": 0,
27	"duration": "freehold",
28	"addr1": "31",
29	"addr2": "",
30	"street": "CHRISTIE MILLER ROAD",
31	"locality": "SALISBURY",
32	"town": "SALISBURY",
33	"district": "SALISBURY",
34	"county": "WILTSHIRE"
35  },
36  "source": {
37	"version": "1.9.6.Final",
38	"connector": "postgresql",
39	"name": "postgres_server",
40	"ts_ms": 1685378780355,
41	"snapshot": "false",
42	"db": "postgres",
43	"sequence": "[\"247833040488\",\"247833042536\"]",
44	"schema": "public",
45	"table": "uk_price_paid",
46	"txId": 106940,
47	"lsn": 247833042536,
48	"xmin": null
49  },
50  "op": "u",
51  "ts_ms": 1685378780514,
52  "transaction": null
53}
```
Copy command
The `op` field here indicates the operation, with the values `u`, `d`, and `c` indicating an update, delete and insert operation, respectively. The `source.lsn` field provides our version value. For delete events, the `after` fields are null. Conversely, for insert events, the `before` fields are null.

This message format is not compatible with our destination table `uk_price_paid` in ClickHouse. We can use a materialized view for transforming these messages at insert time. We show this below:
