# Making complex JSON 58x faster, use 3,300x less memory, in ClickHouse


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# Making complex JSON 58x faster, use 3,300x less memory, in ClickHouse

![pavel.png](/_next/image?url=%2Fuploads%2Fpavel_52fa6ba078.png&w=96&q=75)[Pavel Kruglov](/authors/pavel-kruglov)Oct 9, 2025 · 9 minutes readIn August 2024, ClickHouse v24\.8 introduced a [powerful **JSON data type** to ClickHouse](https://clickhouse.com/docs/sql-reference/data-types/newjson). Since then, we’ve continuously improved it with new features and optimizations.


In this post, we’ll show how **we’ve just made it even better** in ClickHouse v25\.8\.


ClickHouse is already the industry leader in analytical performance, and **the latest changes in v25\.8 make ClickHouse the leader in analytics over JSON data**, too.


## How the JSON type worked in v24\.8 [\#](/blog/json-data-type-gets-even-better#how-the-json-type-worked-in-v248)


Let’s start with a quick recap of [how JSON data is stored in MergeTree parts](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) as designed in ClickHouse v24\.8\.


In the illustration below, we have JSON data with K unique paths with string values. The first **N paths** are stored as subcolumns in *dynamic paths*. All remaining **K – N paths** are stored in a *shared data* structure, which is represented as a `Map(String, String)` column containing both paths and values.


![json_type_update_image1.png](/uploads/json_type_update_image1_min_e5ac49a759.png)
For example, if we query the data of the path `key1`, ClickHouse first checks metadata to see whether `key1` is in *dynamic paths* or *shared data*. In this example path `key1` is in *dynamic paths*, so its values are stored in dedicated data files, which can be read directly and efficiently.


![json_type_update_image2.png](/uploads/json_type_update_image2_min_5b0c0617cb.png)
Now, if we query `key_n+1`, the metadata shows that it’s *not* part of *dynamic paths*. Instead, it resides in *shared data*. To extract its values, ClickHouse must read the **entire** `Map(String, String)` column and filter it in memory. This is much less efficient.


![json_type_update_image3.png](/uploads/json_type_update_image3_min_820f9daa60.png)
By default, the limit on dynamic paths is **1024**. Raising this limit to handle more paths is usually a bad idea, especially when using remote storage like S3, because creating thousands of files per part increases memory usage during merges and complicates reads.


As a result, workloads with thousands or tens of thousands of unique JSON paths suffer from poor performance.


This is the challenge we set out to solve.


## New serializations for shared data in v25\.8 [\#](/blog/json-data-type-gets-even-better#new-serializations-for-shared-data-in-v258)


**ClickHouse v25\.8** introduces [two new serialization formats for *shared data*](https://github.com/ClickHouse/ClickHouse/pull/83777) that dramatically improve the efficiency of reading specific paths.


1. ### Bucketed shared data [\#](/blog/json-data-type-gets-even-better#bucketed-shared-data)


The first new serialization splits *shared data* into **N buckets**. Each bucket contains its own `Map(String, String)` column, with a deterministic assignment of paths to buckets.


![json_type_update_image4.png](/uploads/json_type_update_image4_min_7b81db8ed5.png)
When querying a path like `key_m1`, ClickHouse can immediately determine which bucket contains the requested path. Only that bucket is read, while the rest are skipped.


![json_type_update_image5.png](/uploads/json_type_update_image5_min_ce58cd599c.png)
This **reduces the amount of data scanned and improves performance** compared to reading the entire *shared data*. However, increasing the number of buckets too far creates too many files and reintroduces file\-system overhead.


2. ### Advanced shared data [\#](/blog/json-data-type-gets-even-better#advanced-shared-data)


The second and more powerful approach is the **advanced serialization format**.


Here, each bucket contains 3 files:


- **`.structure`** – metadata for each granule: number of rows, list of paths in the granule, and offset in the `.paths_marks` file.
- **`.data`** – the actual path data stored in columnar format per granule.
- **`.paths_marks`** – offsets pointing to the start of each path’s data in the `.data` file.


![json_type_update_image6.png](/uploads/json_type_update_image6_min_aba69b1ac7.png)
When querying the path `key_m1` ,ClickHouse first checks the `.structure` file to see if the granule contains `key_m1`. If not, the granule is skipped entirely. If it does, ClickHouse looks up the offset in the `.paths_marks` file and jumps directly to the `key_m1` path’s data in the `.data` file and reads it.


![json_type_update_image7.png](/uploads/json_type_update_image7_min_9ec2b127d6.png)
This **avoids reading the data of unrelated paths into memory and significantly improves query performance**.


### Supporting nested paths [\#](/blog/json-data-type-gets-even-better#supporting-nested-paths)


Many JSON documents contain nested structures like arrays of objects. Extracting a nested path from such structures using the above approach still requires reading the entire array, which is inefficient for large payloads.


To address this, **the advanced format was extended with additional files for subcolumn handling**.


Here each bucket has 6 files:


- **`.structure`** – metadata for each granule: number of rows, list of paths in the granule and offsets in files  `.paths_marks` and  `.substreams_metadata`.
- **`.data`** – the actual path data stored in columnar format per granule, but split into substreams. A single path may have multiple substreams. This structure allows ClickHouse to read only the substreams needed to reconstruct the requested subcolumn, rather than scanning the entire path value.
- **`.paths_marks`** – offsets pointing to the start of each path’s data in the  `.data` file.
- **`.substreams_marks`** – offsets pointing to the start of each path’s substream in the `.data` file.
- **`.substreams`** – list of substreams present for each path in a granule. This may differ across granules (e.g., some arrays may contain objects with different nested fields).
- **`.substreams_metadata`** – for each path, stores offsets in the  `.substreams` and  `.substreams_marks` files, effectively linking a path to its subcolumns and their data locations.


![json_type_update_image8.png](/uploads/json_type_update_image8_min_bad57854bf.png)
When querying the subcolumn of path `key_m1`, ClickHouse first reads data from the `.structure` file and checks if this granule contains the requested path `key_m1`. If not, the granule is skipped entirely. If it does, ClickHouse uses the offset stored in the  `.structure` file to read the corresponding entry in `.substreams_metadata` and obtain the offsets for `key_m1`.


Using the first offset, ClickHouse then reads the list of substreams for this path in the granule. If this list does not include the substreams required for the requested subcolumn, the granule is skipped. If the required substreams are present, ClickHouse uses the second offset to read their positions from `.substreams_marks` and then reads only the data of those substreams from the `.data` file.


After reconstructing the requested subcolumn, ClickHouse proceeds to the next granule.


![json_type_update_image9.png](/uploads/json_type_update_image9_min_11de95296c.png)
This avoids reading the data of unrelated paths and unrelated substreams of the requested path in the granule in memory. This **significantly improves the performance of nested subcolumn reading**.


## Balancing efficiency and compatibility [\#](/blog/json-data-type-gets-even-better#balancing-efficiency-and-compatibility)


The **advanced format is** **excellent for selective reads**, but it doesn’t come for free: **reading the entire JSON column or performing merges becomes slower**, because the in\-memory representation of the shared data (`Map(String, String)`) is very different from its storage layout, resulting in expensive conversions during entire JSON column reading.


To address this, ClickHouse v25\.8 makes a trade\-off by **storing a copy of the data in the original format alongside the advanced one**. This effectively doubles the storage requirement, but you get all the benefits of the new format without the sacrifices noted above.


In the below illustration, you can see the copy is stored in three extra files:


- **`.copy.offsets`** – offsets of the original `Map(String, String)` column.
- **`.copy.indexes`** – indexes into the combined list of paths across buckets (avoids storing all paths again).
- **`.copy.values`** \- values of the original `Map(String, String)` column.


![json_type_update_image10.png](/uploads/json_type_update_image10_min_67dddd93b4.png)
This makes **reading full JSON columns and performing merges as fast as before**, while still **keeping the benefits of the advanced format for selective reads**.


## Performance [\#](/blog/json-data-type-gets-even-better#performance)


[We benchmarked the new serialization formats with JSON data containing **10, 100, 1000, and 10,000 unique paths**](https://github.com/ClickHouse/ClickHouse/pull/83777#issuecomment-3073272839).


The new advanced shared data serialization delivers **performance close to storing all paths as dynamic subcolumns** both in query speed and memory usage, **while scaling to tens of thousands of unique paths**.


Below we highlight some of the results for the 10,000 path tests, which demonstrate the improvements from the new serialization formats in v25\.8\.


### Performance test 1 (selective reads) [\#](/blog/json-data-type-gets-even-better#performance-test-1-selective-reads)


In this test, we compare reading a single JSON key from a table of 200k rows, each row containing a JSON document with 10k paths, using wide parts.


Using the **advanced serialization** format dramatically improves both time (\~58x) and memory (\~3,300x) performance compared to the original JSON serialization.




| Data type | Time (seconds) | Memory usage (MiB) |
| --- | --- | --- |
| JSON no shared data | 0\.027 | 18\.64 MiB |
| JSON shared data "advanced" | 0\.063 | 3\.89 MiB |
| JSON shared data "map\_with\_buckets" | 0\.087 | 403\.55 MiB |
| String | 3\.216 | 582\.70 MiB |
| Map | 3\.594 | 538\.37 MiB |
| JSON shared data "map" | 3\.63 | 12\.53 GiB |


### Performance test 2 (reading the whole JSON object) [\#](/blog/json-data-type-gets-even-better#performance-test-2-reading-the-whole-json-object)


In this test, we compare reading the full JSON document from a table of 200k rows, each row containing a JSON document with 10k paths, using wide parts.


Using the **advanced serialization** is practically equivalent to the original JSON serialization. This shows that the advanced serialization delivers huge gains to selective reads without sacrificing performance when reading the whole document.




| table\_type | time\_sec | memory\_usage |
| --- | --- | --- |
| String | 2\.734 | 581\.15 MiB |
| Map | 3\.869 | 550\.14 MiB |
| JSON shared data "map" | 4\.182 | 618\.78 MiB |
| JSON shared data "advanced" | 4\.774 | 683\.27 MiB |
| JSON shared data "map\_with\_buckets" | 15\.271 | 1\.45 GiB |
| JSON no shared data | \- | OOM |


## Conclusion [\#](/blog/json-data-type-gets-even-better#conclusion)


The new *shared data* serialization takes JSON support in ClickHouse to the next level. You can now efficiently query JSON documents with tens of thousands of unique paths while maintaining excellent performance for selective reads.


This enhancement makes ClickHouse an even stronger choice for workloads dealing with semi\-structured JSON data at scale.

### Get started today


Interested in seeing how ClickHouse works on your data? Get started with ClickHouse Cloud in minutes and receive $300 in free credits.

[Sign up](https://clickhouse.cloud/signUp?loc=blog-global-cta&utm_source=clickhouse&utm_medium=web&utm_campaign=blog)Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
