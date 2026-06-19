# JSONAsString and Mat. View as JSON parser \| Altinity® Knowledge Base for ClickHouse®


1. [Schema design](/altinity-kb-schema-design/)
2. JSONAsString and Mat. View as JSON parser
# JSONAsString and Mat. View as JSON parser

Tables with engine Null don’t store data but can be used as a source for materialized views.

JSONAsString a special input format which allows to ingest JSONs into a String column. If the input has several JSON objects (comma separated) they will be interpreted as separate rows. JSON can be multiline.


```
create table entrypoint(J String) Engine=Null;
create table datastore(a String, i Int64, f Float64) Engine=MergeTree order by a;

create materialized view jsonConverter to datastore
as select (JSONExtract(J, 'Tuple(String,Tuple(Int64,Float64))') as x),
        x.1 as a,
        x.2.1 as i,
        x.2.2 as f
from entrypoint;

$ echo '{"s": "val1", "b2": {"i": 42, "f": 0.1}}' | \
    clickhouse-client -q "insert into entrypoint format JSONAsString"

$ echo '{"s": "val1","b2": {"i": 33, "f": 0.2}},{"s": "val1","b2": {"i": 34, "f": 0.2}}' | \
   clickhouse-client -q "insert into entrypoint format JSONAsString"

SELECT * FROM datastore;
┌─a────┬──i─┬───f─┐
│ val1 │ 42 │ 0.1 │
└──────┴────┴─────┘
┌─a────┬──i─┬───f─┐
│ val1 │ 33 │ 0.2 │
│ val1 │ 34 │ 0.2 │
└──────┴────┴─────┘

```
See also: [JSONExtract to parse many attributes at a time](/altinity-kb-queries-and-syntax/jsonextract-to-parse-many-attributes-at-a-time/)

Last modified 2024\.02\.01: [Fixed broken links, other housekeeping (33dff8b)](https://github.com/Altinity/altinityknowledgebase/commit/33dff8b40c62828a1baf7b31d3a22f87a0950e8c)
