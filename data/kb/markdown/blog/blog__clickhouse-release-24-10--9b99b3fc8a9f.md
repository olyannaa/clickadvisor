# ClickHouse Release 24\.10


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 24\.10

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Nov 6, 2024 · 17 minutes readAnother month goes by, which means it’s time for another release!



ClickHouse version 24\.10 contains **25 new features 🌰 15 performance optimizations 🐿 60 bug fixes 🎃**



In this release, clickhouse\-local gets even more useful with new copy and calculator modes. Refreshable Materialized Views are production\-ready, remote files can now be cached, and table cloning has been simplified.


## New Contributors [\#](/blog/clickhouse-release-24-10#new-contributors)


As always, we send a special welcome to all the new contributors in 24\.9! ClickHouse's popularity is, in large part, due to the efforts of the community that contributes. Seeing that community grow is always humbling.


Below are the names of the new contributors:


*Alsu Giliazova, Baitur, Baitur Ulukbekov, Damian Kula, DamianMaslanka5, Daniil Gentili, David Tsukernik, Dergousov Maxim, Diana Carroll, Faizan Patel, Hung Duong, Jiří Kozlovský, Kaushik Iska, Konstantin Vedernikov, Lionel Palacin, Mariia Khristenko, Miki Matsumoto, Oleg Galizin, Patrick Druley, SayeedKhan21, Sharath K S, Shichao, Shichao Jin, Vladimir Cherkasov, Vladimir Valerianov, Z.H., aleksey, alsu, johnnyfish, kurikuQwQ, kylhuk, lwz9103, scanhex12, sharathks118, singhksandeep25, sum12, tuanpach*


Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).



You can also [view the slides from the presentation](https://presentations.clickhouse.com/release_24.10/).


## clickhouse\-local simplifies file conversion [\#](/blog/clickhouse-release-24-10#clickhouse-local-simplifies-file-conversion)


### Contributed by Denis Hananein [\#](/blog/clickhouse-release-24-10#contributed-by-denis-hananein)


ClickHouse comes in many forms. One of these is [clickhouse\-local](https://clickhouse.com/docs/en/operations/utilities/clickhouse-local), which lets you perform fast processing on local and remote files using SQL without installing the database server. Below is a diagram showing the ClickHouse variants:


![Google Keep Note (1).png](/uploads/Google_Keep_Note_1_f4b29eae30.png)
clickhouse\-local now has a new flag,`—-copy`, a shortcut for `SELECT * FROM table`. This means it’s super easy to transform data from one format to another.


We’ll download the 1 million people CSV file from the [datablist/sample\-csv\-files](https://github.com/datablist/sample-csv-files?tab=readme-ov-file) GitHub repository, and then we can run the following query to create a Parquet version of the file:



```
clickhouse -t --copy < people-1000000.csv > people.parquet

```

We can run the following query to explore our new file:



```
clickhouse -f PrettyCompact \
"SELECT \"Job Title\", count()
 FROM 'people.parquet'
 GROUP BY ALL
 ORDER BY count() DESC
 LIMIT 10"

    ┌─Job Title───────────────────────────────────┬─count()─┐
 1. │ Dealer                                      │    1684 │
 2. │ IT consultant                               │    1678 │
 3. │ Designer, ceramics/pottery                  │    1676 │
 4. │ Pathologist                                 │    1673 │
 5. │ Pharmacist, community                       │    1672 │
 6. │ Biochemist, clinical                        │    1669 │
 7. │ Chief Strategy Officer                      │    1663 │
 8. │ Armed forces training and education officer │    1661 │
 9. │ Archaeologist                               │    1657 │
10. │ Education officer, environmental            │    1657 │
    └─────────────────────────────────────────────┴─────────┘

```

If, instead, we want to convert the data from CSV to JSON lines format, we can do the following:



```
clickhouse -t --copy < people-1000000.csv > people.jsonl

```

Let’s have a look at our new file:



```
head -n3 people.jsonl

{"Index":"1","User Id":"9E39Bfc4fdcc44e","First Name":"Diamond","Last Name":"Dudley","Sex":"Male","Email":"teresa26@example.org","Phone":"922.460.8218x66252","Date of birth":"1970-01-01","Job Title":"Photographer"}
{"Index":"2","User Id":"32C079F2Bad7e6F","First Name":"Ethan","Last Name":"Hanson","Sex":"Female","Email":"ufrank@example.com","Phone":"(458)005-8931x2478","Date of birth":"1985-03-08","Job Title":"Actuary"}
{"Index":"3","User Id":"a1F7faeBf5f7A3a","First Name":"Grace","Last Name":"Huerta","Sex":"Female","Email":"tiffany51@example.com","Phone":"(720)205-4521x7811","Date of birth":"1970-01-01","Job Title":"Visual merchandiser"}

```

## clickhouse\-local calculator mode [\#](/blog/clickhouse-release-24-10#clickhouse-local-calculator-mode)


### Contributed by Alexey Milovidov [\#](/blog/clickhouse-release-24-10#contributed-by-alexey-milovidov)


clickhouse\-local also now has a ‘calculator mode’. You can use the `--implicit-select` flag to have it run expressions without a need for a `SELECT` prefix.


For example, the following expression finds the time 23 minutes before now:



```
clickhouse --implicit-select -q "now() - INTERVAL 23 MINUTES"

2024-11-04 10:32:58

```

## Table cloning [\#](/blog/clickhouse-release-24-10#table-cloning)


### Contributed by Tuan Pach [\#](/blog/clickhouse-release-24-10#contributed-by-tuan-pach)


Imagine if you could create a one\-to\-one copy of a large table almost instantly and without requiring additional storage. This could be useful in scenarios where you want to do risk\-free experiments on your data.


With the [CLONE AS](https://clickhouse.com/docs/en/sql-reference/statements/create/table#with-a-schema-and-data-cloned-from-another-table) clause, this is now easier than ever. Using this clause is the same as creating an empty table and attaching all the source table’s partitions.


When we run the clone operation, ClickHouse doesn’t create a copy of the data for the new table. Instead, it creates new parts for the new table that are hard links to the existing table parts.


Data parts in ClickHouse are immutable, which means that if we add new data or modify existing data in either of the tables, the other table will not be affected.


For example, let’s say we have a table called `people` based on the CSV file mentioned earlier:



```
CREATE TABLE people 
ORDER BY Index AS
SELECT * 
FROM 'people*.csv'
SETTINGS schema_inference_make_columns_nullable=0;

```

We can clone this table to another table called `people2` by running the following query:



```
CREATE TABLE people2 CLONE AS people;

```

The two tables now contain the same data.



```
SELECT count()
FROM people

   ┌─count()─┐
1. │ 1000000 │
   └─────────┘

SELECT count()
FROM people2

   ┌─count()─┐
1. │ 1000000 │
   └─────────┘

```

But we can still add data to them independently. For example, let’s add all the rows from the CSV file to the `people2` table:



```
INSERT INTO people2 
SELECT * 
FROM 'people*.csv';

```

Now, let’s count the number of records in each table:



```
SELECT count()
FROM people

   ┌─count()─┐
1. │ 1000000 │
   └─────────┘

SELECT count()
FROM people2

   ┌─count()─┐
1. │ 2000000 │
   └─────────┘

```

## Real\-time metrics in the client [\#](/blog/clickhouse-release-24-10#real-time-metrics-in-the-client)


### Contributed by Maria Khristenko, Julia Kartseva [\#](/blog/clickhouse-release-24-10#contributed-by-maria-khristenko-julia-kartseva)


When running queries from the ClickHouse Client or with clickhouse\-local, we can get a more fine\-grained view of what’s happening by pressing the space bar.


For example, let’s say we run the following query:



```
SELECT product_category, count() AS reviews, 
       round(avg(star_rating), 2) as avg
FROM s3(
  's3://datasets-documentation/amazon_reviews/amazon_reviews_2015.snappy.parquet'
)
GROUP BY ALL
LIMIT 10;

```

If we press the space bar while the query’s running, we’ll see the following:




Your browser does not support the video tag.

Then, when the query finishes, it will show the following stats:



```
Event name                            Value
AddressesMarkedAsFailed               2
ContextLock                           32
InitialQuery                          1
QueriesWithSubqueries                 1
Query                                 1
S3Clients                             1
S3HeadObject                          2
S3ReadMicroseconds                    9.15 s
S3ReadRequestsCount                   52
S3WriteRequestsCount                  2
S3WriteRequestsErrors                 2
SchemaInferenceCacheHits              1
SchemaInferenceCacheSchemaHits        1
SelectQueriesWithSubqueries           1
SelectQuery                           1
StorageConnectionsCreated             17
StorageConnectionsElapsedMicroseconds 5.02 s
StorageConnectionsErrors              2
StorageConnectionsExpired             12
StorageConnectionsPreserved           47
StorageConnectionsReset               7
StorageConnectionsReused              35
TableFunctionExecute                  1

```

## Caching remote files [\#](/blog/clickhouse-release-24-10#caching-remote-files)


### Contributed by Kseniia Sumarokova [\#](/blog/clickhouse-release-24-10#contributed-by-kseniia-sumarokova)


If you’ve ever run a query like the following:



```
SELECT
    product_category,
    count() AS reviews,
    round(avg(star_rating), 2) AS avg
FROM s3('s3://datasets-documentation/amazon_reviews/amazon_reviews_2015.snappy.parquet')
GROUP BY ALL
LIMIT 10;

```

You’ll notice that the query is slightly quicker on subsequent runs but not much quicker.


No more! Starting from 24\.10, ClickHouse offers a cache of directly accessed files  

and data lake tables on S3 and Azure.


The cache entries are identified by path \+ ETag, and ClickHouse will cache data for the columns referenced in the query. To enable it, you’ll need to add the following entry in your ClickHouse Server config file (this feature doesn’t currently work for ClickHouse Local):



```
   <filesystem_caches>
        <cache_for_s3>
                <path>/data/s3_cache_clickhouse</path>
            <max_size>10Gi</max_size>
        </cache_for_s3>
    </filesystem_caches>

```

You can check that ClickHouse has picked up your filesystem cache by running `SHOW FILESYSTEM CACHES`. You’ll then need to enable the cache and provide your cache name when running the query:



```
SELECT
    product_category,
    count() AS reviews,
    round(avg(star_rating), 2) AS avg
FROM s3('s3://datasets-documentation/amazon_reviews/amazon_reviews_2015.snappy.parquet')
GROUP BY ALL
LIMIT 10
SETTINGS enable_filesystem_cache = 1, filesystem_cache_name = 'cache_for_s3'

```

Apart from looking at the query time, you can also view the `S3*` real\-time metrics by pressing the spacebar while the query runs. Below are the metrics of the above query without the cache:



```
S3Clients                                  1
S3GetObject                                186
S3ListObjects                              2
S3ReadMicroseconds                         16.21 s
S3ReadRequestsCount                        192
S3ReadRequestsErrors                       1
S3WriteMicroseconds                        475.00 us
S3WriteRequestsCount                       1

```

And with the cache:



```
S3Clients                                 1
S3ListObjects                             2
S3ReadMicroseconds                        122.66 ms
S3ReadRequestsCount                       6
S3ReadRequestsErrors                      1
S3WriteMicroseconds                       487.00 us
S3WriteRequestsCount                      1

```

The big difference is the number of `S3GetObject` requests, which was 186 without the cache and 0 with the cache.


The cache uses an LRU eviction policy.


## Refreshable Materialized Views production ready [\#](/blog/clickhouse-release-24-10#refreshable-materialized-views-production-ready)


### Contributed by Michael Kolupaev [\#](/blog/clickhouse-release-24-10#contributed-by-michael-kolupaev)


We discussed Refreshable Materialized Views in the [23\.12](https://clickhouse.com/blog/clickhouse-release-23-12) and [24\.9](https://clickhouse.com/blog/clickhouse-release-24-09) release blog posts when it was still an experimental feature.


In 24\.10, this feature supports the Replicated database engine and is also production\-ready!


## Improvements for querying MongoDB [\#](/blog/clickhouse-release-24-10#improvements-for-querying-mongodb)


### Contributed by Kirill Nikiforov [\#](/blog/clickhouse-release-24-10#contributed-by-kirill-nikiforov)


ClickHouse comes with [50\+](https://sql.clickhouse.com/?tab=result&run_query=true&query=V0lUSCBib3RoIEFTICgKICAgICAgICBTRUxFQ1QgbmFtZSwgJ1RhYmxlIGZ1bmN0aW9uJyBhcyBjYXRlZ29yeQogICAgICAgIEZST00gc3lzdGVtLnRhYmxlX2Z1bmN0aW9ucyAKICAgIFVOSU9OIEFMTAogICAgICAgIFNFTEVDVCBuYW1lLCAnVGFibGUgZW5naW5lJyBhcyBjYXRlZ29yeQogICAgICAgIEZST00gc3lzdGVtLnRhYmxlX2VuZ2luZXMKKQpTRUxFQ1QgKiAKRlJPTSBib3RoCldIRVJFIAogICAgTk9UIG5hbWUgaWxpa2UgJyVtZXJnZVRyZWUlJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICcldmlldyUnIEFORAogICAgTk9UIG5hbWUgaWxpa2UgJyV2YWx1ZXMlJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclemVyb3MlJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclY29zbiUnIEFORAogICAgTk9UIG5hbWUgaWxpa2UgJyVjb3NuJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJWJ1ZmZlciUnIEFORAogICAgTk9UIG5hbWUgaWxpa2UgJyVyZXBsaWNhJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJWRpc3RyaWJ1dGVkJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJWpzb24lJyBBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclcmFuZG9tJScgQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJW1lcmdlJSdBTkQKICAgIE5PVCBuYW1lIGlsaWtlICclbnVsbCUnQU5ECiAgICBOT1QgbmFtZSBpbGlrZSAnJW51bWJlcnMlJ0FORAogICAgTk9UIG5hbWUgaWxpa2UgJyVvc3MlJ0FORAogICAgTk9UIG5hbWUgSU4gWydjbHVzdGVyJywgJ2Zvcm1hdCcsICdpbnB1dCcsICdKb2luJywgJ0tlZXBlck1hcCcsICdMb2cnLCAnTWVtb3J5JywgJ1NldCcsICdTdHJpcGVMb2cnLCAnVGlueUxvZyddICAgIApPUkRFUiBCWSBsb3dlcihuYW1lKQ&chart=eyJ0eXBlIjoibGluZSIsImNvbmZpZyI6eyJ4YXhpcyI6Im1vbnRoIiwieWF4aXMiOiJwcmljZSIsInNlcmllcyI6InR5cGUifX0&_gl=1*1fodtkk*_gcl_aw*R0NMLjE3MjcxODU3NzAuQ2owS0NRand4c20zQmhEckFSSXNBTXRWejZPNzNBaGcxRUR2Vlo4MXJHUzRndG9GREdTc0w5amc0ZUFfV2ViZlViaEhMNTlQb3FaTjMwQWFBcWMxRUFMd193Y0I.*_gcl_au*ODk5Mzg5Nzk0LjE3Mjk3MDI4NTQ.) built\-in integrations of external systems, including [MongoDB](https://www.mongodb.com/).


MongoDB can be directly queried from ClickHouse using either the [MongoDB table function](https://clickhouse.com/docs/en/sql-reference/table-functions/mongodb) or the [MongoDB table engine](https://clickhouse.com/docs/en/engines/table-engines/integrations/mongodb). The latter can be used to create a permanent proxy table for querying a remote MongoDB collection, whereas the table function allows ad\-hoc querying of remote MongoDB collections.


Both integrations had some significant limitations before. For example, not all [MongoDB data types](https://www.mongodb.com/docs/manual/reference/bson-types/) were supported, and a query’s `WHERE` and `ORDER BY` conditions were applied on the ClickHouse side after reading all data unfiltered and unsorted from a MongoDB collection first.


ClickHouse 24\.10 now comes with refactored and much improved MongoDB integration support:


- support for all MongoDB data types
- push down of `WHERE` conditions and `ORDER BY`
- connection strings with the `mongodb://` schema


To demonstrate the improved MongoDB integration, we [installed](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/) MongoDB 8\.0 Community Edition on an AWS EC2 machine, loaded some [data](https://www.gharchive.org/), and ran the following in `mongosh` (the MongoDB Shell) to see one of the ingested JSON documents:



```
github> db.events.aggregate([{ $sample: { size: 1 } }]);
[
  {
    _id: ObjectId('672a3659366c7681f18c5334'),
    id: '29478055921',
    type: 'PushEvent',
    actor: {
      id: 82174588,
      login: 'denys-kosyriev',
      display_login: 'denys-kosyriev',
      gravatar_id: '',
      url: 'https://api.github.com/users/denys-kosyriev',
      avatar_url: 'https://avatars.githubusercontent.com/u/82174588?'
    },
    repo: {
      id: 637899002,
      name: 'denys-kosyriev/gulp-vector',
      url: 'https://api.github.com/repos/denys-kosyriev/gulp-vector'
    },
    payload: {
      repository_id: 637899002,
      push_id: Long('13843301463'),
      size: 1,
      distinct_size: 1,
      ref: 'refs/heads/create-settings-page',
      head: 'dfa3d843b579b7d403884ff7c14b1c0100e6ba2c',
      before: '3a5211f72354fb85567179018ad559fef77eec4a',
      commits: [
        {
          sha: 'dfa3d843b579b7d403884ff7c14b1c0100e6ba2c',
          author: { email: 'utross2241@gmail.com', name: 'denys_kosyriev' },
          message: "feature: setting js radio-buttons 'connection' page",
          distinct: true,
          url: 'https://api.github.com/repos/denys-kosyriev/gulp-vector/commits/dfa3d843b579b7d403884ff7c14b1c0100e6ba2c'
        }
      ]
    },
    public: true,
    created_at: '2023-06-02T01:15:20Z'
  }
]


```

Then we started a ClickHouse instance, where we set `<use_legacy_mongodb_integration>` to `0` in the [server config file](https://clickhouse.com/docs/en/operations/configuration-files), which is currently necessary to enable the refactored and improved MongoDB integration.


Now we query the `events` collection in the `github` databases on our MongoDB instance from above with the following command, which we can run in `clickhouse-client`:



```
SELECT *
FROM mongodb(
    '<HOST>:<PORT>',
    'github',
    'events',
    '<USER>',
    '<PASSWORD>',
    'id String, type String, actor String')
LIMIT 1
FORMAT Vertical

Row 1:
──────
id:    26163418664
type:  WatchEvent
actor: {"id":89544871,"login":"Aziz403","display_login":"Aziz403","gravatar_id":"","url":"https:\/\/api.github.com\/users\/Aziz403","avatar_url":"https:\/\/avatars.githubusercontent.com\/u\/89544871?"}

```

## Bonus: JSON data type in action [\#](/blog/clickhouse-release-24-10#bonus-json-data-type-in-action)


As a reminder, because of some fundamental design [flaws](https://github.com/ClickHouse/ClickHouse/issues/54864) with the previous experimental implementation, [we built a new powerful JSON data type for ClickHouse](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse) from the ground up.


The new JSON type is purpose\-built to deliver high\-performance handling of JSON data and stands out as the best possible implementation of JSON on top of columnar storage featuring support for:


- **Dynamically changing data:** allow values with different data types (possibly incompatible and not known beforehand) for the same JSON paths without unification into a least common type, preserving the integrity of mixed\-type data.
- **High performance and dense, true column\-oriented storage:** store and read any inserted JSON key path as a native, dense subcolumn, allowing high data compression and maintaining query performance seen on classic types.
- **Scalability:** allow limiting the number of subcolumns that are stored separately, to scale JSON storage for high\-performance analytics over PB datasets.
- **Tuning:** allow hints for JSON parsing (explicit types for JSON paths, paths that should be skipped during parsing, etc).


While this release comes with a [list](https://clickhouse.com/docs/en/whats-new/changelog#-clickhouse-release-2410-2024-10-31) of smaller performance and usability improvements, we [announced](https://clickhouse.com/blog/clickhouse-release-24-08#json-data-type) in 24\.8 that this JSON rewrite was largely complete and was on the path to being beta with a high degree of confidence its implementation was as good as theoretically possible.


ClickHouse is now a powerful alternative to specialized [document databases](https://clickhouse.com/engineering-resources/json-database#document-databases) like MongoDB.


As a bonus, we did a quick benchmarking test and loaded the first six months of 2023 [GitHub event data](https://ghe.clickhouse.tech/) (which is [provided in JSON format only](https://www.gharchive.org/)) into MongoDB 8\.0 Community Edition and ClickHouse 24\.10, both running on their own AWS EC2 m6i.8xlarge machine with 32 CPU cores, 128 GB of RAM, 5 TB EBS gp3 volume, with Ubuntu 24\.04 LTS ("Noble") as operating system. The uncompressed data size of the ingested GitHub event data is \~2\.4 TB.


Our use case was to load and analyze the data ad\-hocly without creating any schemas or indexes upfront. For example, in ClickHouse, we created the following database and table and used a simple [script](https://gist.github.com/tom-clickhouse/f993107ffd3fb4756c4125594014f79c) to load the data:



```
CREATE DATABASE github;

USE github;
SET allow_experimental_json_type = 1;

CREATE TABLE events
(
    docs JSON()
)
ENGINE = MergeTree
ORDER BY ();

```

After loading the first six months of the 2023 GitHub event data, the above table contains \~700 million JSON documents:



```
SELECT count()
FROM events;

   ┌───count()─┐
1. │ 693137012 │ -- 693.14 million
   └───────────┘


```

And the size on disk is \~675 GiB:



```
SELECT 
  formatReadableSize(sum(bytes_on_disk)) AS size_on_disk
FROM system.parts
WHERE active AND (database = 'github') AND (`table` = 'events')


   ┌─size_on_disk─┐
1. │ 674.25 GiB   │
   └──────────────┘

```

We can check the structure of one of the stored JSON documents:



```
SELECT docs
FROM events
LIMIT 1
FORMAT PrettyJSONEachRow;

{
    "docs": {
        "actor" : {
            "avatar_url" : "https:\/\/avatars.githubusercontent.com\/u\/119809980?",
            "display_login" : "ehwu106",
            "gravatar_id" : "",
            "id" : "119809980",
            "login" : "ehwu106",
            "url" : "https:\/\/api.github.com\/users\/ehwu106"
        },
        "created_at" : "2023-01-01T00:00:00Z",
        "id" : "26163418658",
        "payload" : {
            "before" : "27e76fd2920c98cf825daefa9469cb202944d96d",
            "commits" : [
                {
                    "author" : {
                        "email" : "howard.wu@travasecurity.com",
                        "name" : "Howard Wu"
                    },
                    "distinct" : 1,
                    "message" : "pushing",
                    "sha" : "01882b15808c6cc63f4075eea105de4f608e23aa",
                    "url" : "https:\/\/api.github.com\/repos\/ehwu106\/Gmail-Filter-Solution\/commits\/01882b15808c6cc63f4075eea105de4f608e23aa"
                },
                {
                    "author" : {
                        "email" : "hwu106@ucsc.edu",
                        "name" : "hwu106"
                    },
                    "distinct" : 1,
                    "message" : "push",
                    "sha" : "8fbcb0a5be7f1ae98c620ffc445f8212da279c4b",
                    "url" : "https:\/\/api.github.com\/repos\/ehwu106\/Gmail-Filter-Solution\/commits\/8fbcb0a5be7f1ae98c620ffc445f8212da279c4b"
                }
            ],
            "distinct_size" : "2",
            "head" : "8fbcb0a5be7f1ae98c620ffc445f8212da279c4b",
            "push_id" : "12147229638",
            "ref" : "refs\/heads\/main",
            "size" : "2"
        },
        "public" : 1,
        "repo" : {
            "id" : "582174284",
            "name" : "ehwu106\/Gmail-Filter-Solution",
            "url" : "https:\/\/api.github.com\/repos\/ehwu106\/Gmail-Filter-Solution"
        },
        "type" : "PushEvent"
    }
}


```

For MongoDB, we used a similar [script](https://gist.github.com/tom-clickhouse/d48fd00b09a3974e5ba392aca415c8bd) to load the same data set into a collection (without any extra indexes or schema hints), and we check the number of stored JSON documents and size on disk with a command in `mongosh`:



```
github> db.events.stats();
...
count: 693137012,
storageSize: 746628136960

```

The document count is the same as in ClickHouse, and the storage size is slightly larger, at 695\.35 GiB.


We can also check the structure of one of the stored JSON documents:



```
github> db.events.aggregate([{ $sample: { size: 1 } }]);
[
  {
    _id: ObjectId('672ab1430e44c2d6ce0433ee'),
    id: '28105983813',
    type: 'DeleteEvent',
    actor: {
      id: 10810283,
      login: 'direwolf-github',
      display_login: 'direwolf-github',
      gravatar_id: '',
      url: 'https://api.github.com/users/direwolf-github',
      avatar_url: 'https://avatars.githubusercontent.com/u/10810283?'
    },
    repo: {
      id: 183051410,
      name: 'direwolf-github/my-app',
      url: 'https://api.github.com/repos/direwolf-github/my-app'
    },
    payload: { ref: 'branch-58838bda', ref_type: 'branch', pusher_type: 'user' },
    public: true,
    created_at: '2023-03-31T00:43:36Z'
  }
]


```

Now we want to analyze the data set and get an overview of the different GitHub event types and rank them by their document count. In ClickHouse, this can be done with a simple Aggregation SQL query:



```
SELECT
    docs.type,
    count() AS count
FROM events
GROUP BY docs.type
ORDER BY count DESC

    ┌─docs.type─────────────────────┬─────count─┐
 1. │ PushEvent                     │ 378108538 │
 2. │ CreateEvent                   │  95054342 │
 3. │ PullRequestEvent              │  55578642 │
 4. │ WatchEvent                    │  41269499 │
 5. │ IssueCommentEvent             │  32985638 │
 6. │ DeleteEvent                   │  22395484 │
 7. │ PullRequestReviewEvent        │  17029889 │
 8. │ IssuesEvent                   │  14236189 │
 9. │ PullRequestReviewCommentEvent │  10285596 │
10. │ ForkEvent                     │   9926485 │
11. │ CommitCommentEvent            │   6569455 │
12. │ ReleaseEvent                  │   3804539 │
13. │ PublicEvent                   │   2352553 │
14. │ MemberEvent                   │   2304020 │
15. │ GollumEvent                   │   1235200 │
    └───────────────────────────────┴───────────┘

15 rows in set. Elapsed: 7.324 sec. Processed 693.14 million rows, 20.18 GB (94.63 million rows/s., 2.76 GB/s.)
Peak memory usage: 7.33 MiB.

```

The query aggregates and sorts the complete data set (\~700 million JSON documents). The query's runtime is 7\.3 seconds, and the peak memory usage is 7\.33 MiB. This low memory usage is attributed to ClickHouse’s [true column\-oriented storage](https://clickhouse.com/blog/a-new-powerful-json-data-type-for-clickhouse#challenge-1-true-column-oriented-storage) for JSON documents, enabling independent access to sub\-columns for JSON paths. Additionally, ClickHouse retrieves only the columns required for a query. In our example, it reads, aggregates, and sorts data exclusively from the `docs.type` column. Also note the query throughput of 94 million rows/s., and 2\.76 GB/s.


An [aggregation pipeline](https://www.mongodb.com/resources/products/capabilities/aggregation-pipeline) is the recommended way of doing aggregations in MongoDB. We ran an aggregation pipeline in MongoDB that is equivalent to our ClickHouse SQL query from above:



```
github> start = new Date();
ISODate('2024-11-06T09:33:11.295Z')
github> db.events.aggregate([
{
  $group: {
    _id: "$type",       // Group by docs.type
    count: { $sum: 1 }  // Count each occurrence
  }
},
{
  $sort: { count: -1 }  // Sort by count in descending order
},
{
  $project: {  // Project the fields to match SQL output
    type: "$_id",
    count: 1,
    _id: 0
  }
}
]);

[
  { count: 378108538, type: 'PushEvent' },
  { count: 95054342, type: 'CreateEvent' },
  { count: 55578642, type: 'PullRequestEvent' },
  { count: 41269499, type: 'WatchEvent' },
  { count: 32985638, type: 'IssueCommentEvent' },
  { count: 22395484, type: 'DeleteEvent' },
  { count: 17030832, type: 'PullRequestReviewEvent' },
  { count: 14236189, type: 'IssuesEvent' },
  { count: 10285596, type: 'PullRequestReviewCommentEvent' },
  { count: 9926485, type: 'ForkEvent' },
  { count: 6569455, type: 'CommitCommentEvent' },
  { count: 3804539, type: 'ReleaseEvent' },
  { count: 2352553, type: 'PublicEvent' },
  { count: 2304020, type: 'MemberEvent' },
  { count: 1235200, type: 'GollumEvent' }
]
github> print(EJSON.stringify({t: new Date().getTime() - start.getTime()}));
{"t":13779342}

```

The query's runtime on MongoDB (running on exactly the same hardware as ClickHouse) with the same data set is 1377934 milliseconds which is \~4 hours and \~2000 times slower than ClickHouse.


By default (for its [WiredTiger storage engine](https://www.mongodb.com/docs/manual/core/wiredtiger/)), MongoDB will reserve 50% of the available memory. On our test machine, this is \~60 GB (half of the available 128 GB), which we could verify with `top`. In contrast to ClickHouse, MongoDB doesn’t directly track queries' peak memory consumptions within its engine. The ClickHouse server process needs about 1 GB of RAM plus the peak memory usage of executed queries. In sum, for running our test query, the memory consumption of MongoDB is about 7000 times higher than the memory usage of ClickHouse.

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
