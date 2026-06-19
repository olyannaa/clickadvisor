---
source: blog
url: https://clickhouse.com/blog/getting-data-into-clickhouse-part-1
topic: getting-data-into-clickhouse-part-2-a-json-detour
ch_version_introduced: '3.456'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 8
---

single comment with 2 likes, our new column will be initially represented as an Int8\. ``` INSERT INTO hackernews(post, type, time) FORMAT JSONEachRow {"post":{"by":"zX41ZdbW","id":20684796,"text":"ClickHouse is happy to use multiple cores if the query is heavy enough.","likes":2},"type":"comment","time":"2022-08-12 11:48:08"}; ```

```

DESCRIBE TABLE hackernews
FORMAT Vertical
SETTINGS describe_extend_object_types = 1

Query id: c1a80073-b5c3-48c1-aa77-7cef5f3eb2d1

Row 1:
──────
name:               post
type:               Tuple(by String, dead Int8, deleted Int8, descendants Int16, id Int32, kids Array(Int32), likes Int8, parent Int32, parts Array(Int32), poll Int32, score Int16, text String, time String, title String, type String, url String)
default_type:
default_expression:
comment:
codec_expression:
ttl_expression:



```

However, suppose a 2nd comment receives several thousand likes.

```

INSERT INTO hackernews(post, type, time) FORMAT JSONEachRow {"post":{"by":"dalem","id":1111111,"text":"ClickHouse is just the best OLAP DB ever!!!!!.","likes":2000000},"type":"comment","time":"2022-08-13 11:48:08"};


```

```

DESCRIBE TABLE hackernews
FORMAT Vertical
SETTINGS describe_extend_object_types = 1

Query id: 3056120f-1e7c-4494-b43a-510518c93380

Row 1:
──────
name:               post
type:               Tuple(by String, dead Int8, deleted Int8, descendants Int16, id Int32, kids Array(Int32), likes Int32, parent Int32, parts Array(Int32), poll Int32, score Int16, text String, time String, title String, type String, url String)
default_type:
default_expression:
comment:
codec_expression:
ttl_expression:


```

Our column has been transparently mapped to a UInt32\.

This functionality rarely impacts queries. However, if the value is sent as a string (e.g. due to a single “dirty” document), it will transparently convert the column to a String type. This potentially could break queries that rely on numeric values. Either cleanse your data diligently or explicitly declare columns outside of the JSON to enforce type correctness.

## Summary [\#](/blog/getting-data-into-clickhouse-part-2-json#summary)

In this post, we have explored reading JSON datasets and the JSON object type. We have demonstrated the flexibility of this type and its ability to adapt to changing data, as well as some limitations and how to overcome them. Future posts will utilize this capability more fully, once it is no longer experimental, for addressing problems such as using ClickHouse as a log store.

For users looking for more information on the JSON capabilities of ClickHouse, we have updated our [documentation](https://clickhouse.com/docs/en/guides/developer/working-with-json) to describe the alternative approaches to dealing with semi\-structured data.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts
