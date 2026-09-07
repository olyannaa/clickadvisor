---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"ClickHouse
topic: clickhouse-newsletter-april-2022-json-json-json-clickhouse
ch_version_introduced: '26.8'
last_updated: '2026-09-07'
chunk_index: 3
total_chunks_in_doc: 5
---

not the case, especially if it is logs from different applications and services, for example. To get this kind of “semi\-structured” data into ClickHouse, it was often necessary to develop [sophisticated data schemas](https://eng.uber.com/logging/) involving arrays and materialized columns.

No longer! Now it can all just go into one column of type JSON. It’s a really powerful feature and we’re very excited about it, so give it a go and let us know what you think.
2. **ARM** builds are now available [as Docker images](https://hub.docker.com/r/clickhouse/clickhouse-server/tags)! For example, you can run ClickHouse on macOS using Docker with `docker run clickhouse/clickhouse-server`. All functional tests are now passing for ARM builds in our CI. In addition you can now obtain deb, rpm, apk, and binary packages.
3. **[S3 disks](https://clickhouse.com/docs/en/engines/table-engines/mergetree-family/mergetree/#table_engine-mergetree-s3)** as storage for ClickHouse are now fully tested as well. You can configure using S3 for storage in the `<storage_configuration>` section of the ClickHouse configuration file. Note: There are still some performance issues that we are working on.
4. The **[Hive table function](https://github.com/ClickHouse/ClickHouse/pull/34946)** allows you to read data from Apache Hive tables directly and combine it with data in ClickHouse. Or insert the data into ClickHouse using `INSERT INTO clickhouse_table SELECT * FROM hive(...)`.

For more details including live demos have a look at the release webinar recording [here](https://www.youtube.com/watch?v=GzeANZzPras). Also, [register](https://clickhouse.com/company/events/v22-4-release-webinar/) for the April release webinar of version 22\.4 on Thursday, April 21 @ 9 am PST / 5 pm GMT.

We hope you enjoy this release and please upgrade!

## **Query of the Month: JSON, JSON, JSON** \#

Let’s take the new JSON data type for a spin:

```
1SET allow_experimental_object_type = 1;
2CREATE TABLE json (o JSON) ENGINE = Memory
3INSERT INTO json VALUES ('{"a": 1, "b": { "c": 2, "d": [1, 2, 3] }}')
4SELECT o.a, o.b.c, o.b.d[3] FROM json
```
Copy command
The select statement will return 1, 2, 3 and you can see how JSON objects in ClickHouse support nested objects and arrays and how neat the query syntax is.

You might already have JSON data in a file somewhere. To insert it into a JSON column ClickHouse, you can run something like:
