# Use JSON where appropriate \| ClickHouse Docs


- - [Best practices](/docs/best-practices)- Using JSON
[Edit this page](https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/best-practices/json_type.md)# Use JSON where appropriate

ClickHouse now offers a native JSON column type designed for semi\-structured and dynamic data. It's important to clarify that **this is a column type, not a data format**—you can insert JSON into ClickHouse as a string or via supported formats like [JSONEachRow](/docs/interfaces/formats/JSONEachRow), but that doesn't imply using the JSON column type. You should only use the JSON type when the structure of your data is dynamic, not when you simply happen to store JSON.


## When to use the `JSON` Type[​](#when-to-use-json-type "Direct link to when-to-use-json-type")


The `JSON` type is designed for querying, filtering, and aggregating specific fields within JSON objects that have dynamic or unpredictable structures. It achieves this by splitting JSON objects into separate sub\-columns, which dramatically reduces data read and speeds up queries on selected fields compared to alternatives like `Map` or parsing strings.


**However, this comes with important trade\-offs:**


- Slower `INSERT`s \- Splitting JSON into sub\-columns, performing type inference, and managing flexible storage structures makes inserts slower compared to storing JSON as a simple `String` column.
- Slower when reading entire objects \- If you need to retrieve complete JSON documents (rather than specific fields), the `JSON` type is slower than reading from a `String` column. The overhead of reconstructing objects from separate sub\-columns provides no benefit when you're not doing field\-level queries.
- Storage overhead \- Maintaining separate sub\-columns adds structural overhead compared to storing JSON as a single string value.


### Use the `JSON` type when:[​](#use-json-type "Direct link to use-json-type")


- Your data has a dynamic or unpredictable structure with varying keys across documents
- Field types or schemas change over time or vary between records
- You need to query, filter, or aggregate on specific paths within JSON objects whose structure you can't predict upfront
- Your use case involves semi\-structured data like logs, events, or user\-generated content with inconsistent schemas


### Use a `String` column (or structured types) when:[​](#use-string-type "Direct link to use-string-type")


- Your data structure is known and consistent \- in this case, use normal columns, `Tuple`, `Array`, `Dynamic`, or `Variant` types instead
- `JSON` documents are treated as opaque blobs that are only stored and retrieved in their entirety without field\-level analysis
- You don't need to query or filter on individual JSON fields within the database
- The `JSON` is simply a transport/storage format, not analyzed within ClickHouse


TipIf `JSON` is an opaque document that isn't analyzed inside the database, and only stored and retrieved back, it should be stored as a `String` field. The `JSON` type's benefits only materialize when you need to efficiently query, filter, or aggregate on specific fields within dynamic `JSON` structures.You can also mix approaches—use standard columns for predictable top\-level fields and a `JSON` column for dynamic sections of the payload.




## Considerations and tips for using JSON[​](#considerations-and-tips-for-using-json "Direct link to Considerations and tips for using JSON")


The JSON type enables efficient columnar storage by flattening paths into subcolumns. But with flexibility comes responsibility. To use it effectively:


- **Specify path types** using [hints in the column definition](/docs/sql-reference/data-types/newjson) to specify types for known subcolumns, avoiding unnecessary type inference.
- **Skip paths** if you don't need the values, with [SKIP and SKIP REGEXP](/docs/sql-reference/data-types/newjson) to reduce storage and improve performance.
- **Avoid setting [`max_dynamic_paths`](/docs/sql-reference/data-types/newjson#reaching-the-limit-of-dynamic-paths-inside-json) too high**—large values increase resource consumption and reduce efficiency. As a rule of thumb, keep it below 10,000\.


Type hintsType hints offer more than just a way to avoid unnecessary type inference—they eliminate storage and processing indirection entirely. JSON paths with type hints are always stored just like traditional columns, bypassing the need for [**discriminator columns**](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#storage-extension-for-dynamically-changing-data) or dynamic resolution during query time. This means that with well\-defined type hints, nested JSON fields achieve the same performance and efficiency as if they were modeled as top\-level fields from the outset. As a result, for datasets that are mostly consistent but still benefit from the flexibility of JSON, type hints provide a convenient way to preserve performance without needing to restructure your schema or ingest pipeline.


## Advanced features[​](#advanced-features "Direct link to Advanced features")


- JSON columns **can be used in primary keys** like any other columns. Codecs can't be specified for a subcolumn.
- They support introspection via functions like [`JSONAllPathsWithTypes()` and `JSONDynamicPaths()`](/docs/sql-reference/data-types/newjson#introspection-functions).
- You can read nested sub\-objects using the `.^` syntax.
- Query syntax may differ from standard SQL and may require special casting or operators for nested fields.


For additional guidance, see [ClickHouse JSON documentation](/docs/sql-reference/data-types/newjson) or explore our blog post [A New Powerful JSON Data Type for ClickHouse](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse).


## Examples[​](#examples "Direct link to Examples")


Consider the following JSON sample, representing a row from the [Python PyPI dataset](https://clickpy.clickhouse.com/):



```
{
  "date": "2022-11-15",
  "country_code": "ES",
  "project": "clickhouse-connect",
  "type": "bdist_wheel",
  "installer": "pip",
  "python_minor": "3.9",
  "system": "Linux",
  "version": "0.3.0"
}

```

Lets assume this schema is static and the types can be well defined. Even if the data is in NDJSON format (JSON row per line), there is no need to use the JSON type for such a schema. Simply define the schema with classic types.



```
CREATE TABLE pypi (
  `date` Date,
  `country_code` String,
  `project` String,
  `type` String,
  `installer` String,
  `python_minor` String,
  `system` String,
  `version` String
)
ENGINE = MergeTree
ORDER BY (project, date)

```

and insert JSON rows:



```
INSERT INTO pypi FORMAT JSONEachRow
{"date":"2022-11-15","country_code":"ES","project":"clickhouse-connect","type":"bdist_wheel","installer":"pip","python_minor":"3.9","system":"Linux","version":"0.3.0"}

```

Consider the [arXiv dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv?resource=download) containing 2\.5m scholarly papers. Each row in this dataset, distributed as NDJSON, represents a published academic paper. An example row is shown below:



```
{
  "id": "2101.11408",
  "submitter": "Daniel Lemire",
  "authors": "Daniel Lemire",
  "title": "Number Parsing at a Gigabyte per Second",
  "comments": "Software at https://github.com/fastfloat/fast_float and\n  https://github.com/lemire/simple_fastfloat_benchmark/",
  "journal-ref": "Software: Practice and Experience 51 (8), 2021",
  "doi": "10.1002/spe.2984",
  "report-no": null,
  "categories": "cs.DS cs.MS",
  "license": "http://creativecommons.org/licenses/by/4.0/",
  "abstract": "With disks and networks providing gigabytes per second ....\n",
  "versions": [
    {
      "created": "Mon, 11 Jan 2021 20:31:27 GMT",
      "version": "v1"
    },
    {
      "created": "Sat, 30 Jan 2021 23:57:29 GMT",
      "version": "v2"
    }
  ],
  "update_date": "2022-11-07",
  "authors_parsed": [
    [
      "Lemire",
      "Daniel",
      ""
    ]
  ]
}

```

While the JSON here is complex, with nested structures, it is predictable. The number and type of the fields won't change. While we could use the JSON type for this example, we can also just define the structure explicitly using [Tuples](/docs/sql-reference/data-types/tuple) and [Nested](/docs/sql-reference/data-types/nested-data-structures/nested) types:



```
CREATE TABLE arxiv
(
  `id` String,
  `submitter` String,
  `authors` String,
  `title` String,
  `comments` String,
  `journal-ref` String,
  `doi` String,
  `report-no` String,
  `categories` String,
  `license` String,
  `abstract` String,
  `versions` Array(Tuple(created String, version String)),
  `update_date` Date,
  `authors_parsed` Array(Array(String))
)
ENGINE = MergeTree
ORDER BY update_date

```

Again we can insert the data as JSON:



```
INSERT INTO arxiv FORMAT JSONEachRow 
{"id":"2101.11408","submitter":"Daniel Lemire","authors":"Daniel Lemire","title":"Number Parsing at a Gigabyte per Second","comments":"Software at https://github.com/fastfloat/fast_float and\n  https://github.com/lemire/simple_fastfloat_benchmark/","journal-ref":"Software: Practice and Experience 51 (8), 2021","doi":"10.1002/spe.2984","report-no":null,"categories":"cs.DS cs.MS","license":"http://creativecommons.org/licenses/by/4.0/","abstract":"With disks and networks providing gigabytes per second ....\n","versions":[{"created":"Mon, 11 Jan 2021 20:31:27 GMT","version":"v1"},{"created":"Sat, 30 Jan 2021 23:57:29 GMT","version":"v2"}],"update_date":"2022-11-07","authors_parsed":[["Lemire","Daniel",""]]}

```

Suppose another column called `tags` is added. If this was simply a list of strings we could model this as an `Array(String)`, but let's assume you can add arbitrary tag structures with mixed types (notice `score` is a string or integer). Our modified JSON document:



```
{
 "id": "2101.11408",
 "submitter": "Daniel Lemire",
 "authors": "Daniel Lemire",
 "title": "Number Parsing at a Gigabyte per Second",
 "comments": "Software at https://github.com/fastfloat/fast_float and\n  https://github.com/lemire/simple_fastfloat_benchmark/",
 "journal-ref": "Software: Practice and Experience 51 (8), 2021",
 "doi": "10.1002/spe.2984",
 "report-no": null,
 "categories": "cs.DS cs.MS",
 "license": "http://creativecommons.org/licenses/by/4.0/",
 "abstract": "With disks and networks providing gigabytes per second ....\n",
 "versions": [
 {
   "created": "Mon, 11 Jan 2021 20:31:27 GMT",
   "version": "v1"
 },
 {
   "created": "Sat, 30 Jan 2021 23:57:29 GMT",
   "version": "v2"
 }
 ],
 "update_date": "2022-11-07",
 "authors_parsed": [
 [
   "Lemire",
   "Daniel",
   ""
 ]
 ],
 "tags": {
   "tag_1": {
     "name": "ClickHouse user",
     "score": "A+",
     "comment": "A good read, applicable to ClickHouse"
   },
   "28_03_2025": {
     "name": "professor X",
     "score": 10,
     "comment": "Didn't learn much",
     "updates": [
       {
         "name": "professor X",
         "comment": "Wolverine found more interesting"
       }
     ]
   }
 }
}

```

In this case, we could model the arXiv documents as either all JSON or simply add a JSON `tags` column. We provide both examples below:



```
CREATE TABLE arxiv
(
  `doc` JSON(update_date Date)
)
ENGINE = MergeTree
ORDER BY doc.update_date

```

NoteWe provide a type hint for the `update_date` column in the JSON definition, as we use it in the ordering/primary key. This helps ClickHouse to know that this column won't be null and ensures it knows which `update_date` subcolumn to use (there may be multiple for each type, so this is ambiguous otherwise).


We can insert into this table and view the subsequently inferred schema using the [`JSONAllPathsWithTypes`](/docs/sql-reference/functions/json-functions#JSONAllPathsWithTypes) function and [`PrettyJSONEachRow`](/docs/interfaces/formats/PrettyJSONEachRow) output format:



```
INSERT INTO arxiv FORMAT JSONAsObject 
{"id":"2101.11408","submitter":"Daniel Lemire","authors":"Daniel Lemire","title":"Number Parsing at a Gigabyte per Second","comments":"Software at https://github.com/fastfloat/fast_float and\n  https://github.com/lemire/simple_fastfloat_benchmark/","journal-ref":"Software: Practice and Experience 51 (8), 2021","doi":"10.1002/spe.2984","report-no":null,"categories":"cs.DS cs.MS","license":"http://creativecommons.org/licenses/by/4.0/","abstract":"With disks and networks providing gigabytes per second ....\n","versions":[{"created":"Mon, 11 Jan 2021 20:31:27 GMT","version":"v1"},{"created":"Sat, 30 Jan 2021 23:57:29 GMT","version":"v2"}],"update_date":"2022-11-07","authors_parsed":[["Lemire","Daniel",""]],"tags":{"tag_1":{"name":"ClickHouse user","score":"A+","comment":"A good read, applicable to ClickHouse"},"28_03_2025":{"name":"professor X","score":10,"comment":"Didn't learn much","updates":[{"name":"professor X","comment":"Wolverine found more interesting"}]}}}

```


```
SELECT JSONAllPathsWithTypes(doc)
FROM arxiv
FORMAT PrettyJSONEachRow

{
  "JSONAllPathsWithTypes(doc)": {
    "abstract": "String",
    "authors": "String",
    "authors_parsed": "Array(Array(Nullable(String)))",
    "categories": "String",
    "comments": "String",
    "doi": "String",
    "id": "String",
    "journal-ref": "String",
    "license": "String",
    "submitter": "String",
    "tags.28_03_2025.comment": "String",
    "tags.28_03_2025.name": "String",
    "tags.28_03_2025.score": "Int64",
    "tags.28_03_2025.updates": "Array(JSON(max_dynamic_types=16, max_dynamic_paths=256))",
    "tags.tag_1.comment": "String",
    "tags.tag_1.name": "String",
    "tags.tag_1.score": "String",
    "title": "String",
    "update_date": "Date",
    "versions": "Array(JSON(max_dynamic_types=16, max_dynamic_paths=256))"
  }
}

1 row in set. Elapsed: 0.003 sec.

```

Alternatively, we could model this using our earlier schema and a JSON `tags` column. This is generally preferred, minimizing the inference required by ClickHouse:



```
CREATE TABLE arxiv
(
    `id` String,
    `submitter` String,
    `authors` String,
    `title` String,
    `comments` String,
    `journal-ref` String,
    `doi` String,
    `report-no` String,
    `categories` String,
    `license` String,
    `abstract` String,
    `versions` Array(Tuple(created String, version String)),
    `update_date` Date,
    `authors_parsed` Array(Array(String)),
    `tags` JSON()
)
ENGINE = MergeTree
ORDER BY update_date

```


```
INSERT INTO arxiv FORMAT JSONEachRow 
{"id":"2101.11408","submitter":"Daniel Lemire","authors":"Daniel Lemire","title":"Number Parsing at a Gigabyte per Second","comments":"Software at https://github.com/fastfloat/fast_float and\n  https://github.com/lemire/simple_fastfloat_benchmark/","journal-ref":"Software: Practice and Experience 51 (8), 2021","doi":"10.1002/spe.2984","report-no":null,"categories":"cs.DS cs.MS","license":"http://creativecommons.org/licenses/by/4.0/","abstract":"With disks and networks providing gigabytes per second ....\n","versions":[{"created":"Mon, 11 Jan 2021 20:31:27 GMT","version":"v1"},{"created":"Sat, 30 Jan 2021 23:57:29 GMT","version":"v2"}],"update_date":"2022-11-07","authors_parsed":[["Lemire","Daniel",""]],"tags":{"tag_1":{"name":"ClickHouse user","score":"A+","comment":"A good read, applicable to ClickHouse"},"28_03_2025":{"name":"professor X","score":10,"comment":"Didn't learn much","updates":[{"name":"professor X","comment":"Wolverine found more interesting"}]}}}

```

We can now infer the types of the subcolumn `tags`.



```
SELECT JSONAllPathsWithTypes(tags)
FROM arxiv
FORMAT PrettyJSONEachRow

{
  "JSONAllPathsWithTypes(tags)": {
    "28_03_2025.comment": "String",
    "28_03_2025.name": "String",
    "28_03_2025.score": "Int64",
    "28_03_2025.updates": "Array(JSON(max_dynamic_types=16, max_dynamic_paths=256))",
    "tag_1.comment": "String",
    "tag_1.name": "String",
    "tag_1.score": "String"
  }
}

1 row in set. Elapsed: 0.002 sec.

```
[PreviousAvoid optimize final](/docs/best-practices/avoid-optimize-final)[NextUse case guides](/docs/use-cases)- [When to use the `JSON` Type](#when-to-use-json-type)
	- [Use the `JSON` type when:](#use-json-type)- [Use a `String` column (or structured types) when:](#use-string-type)- [Considerations and tips for using JSON](#considerations-and-tips-for-using-json)- [Advanced features](#advanced-features)- [Examples](#examples)
Was this page helpful?
