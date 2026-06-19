# ClickHouse Release 23\.5


\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 23\.5

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Jun 21, 2023 · 11 minutes readThe release train keeps on rolling.


We are super excited to share a bevy of amazing features in 23\.5\.


And, we already have a date for the 23\.6 release, please register now to join the community call on June 29th at 9 AM (PDT) / 6 PM (CEST).


## Release Summary [\#](/blog/clickhouse-release-23-05#release-summary)


29 new features.
22 performance optimizations.
85 bug fixes.


A small subset of highlighted features are below. But it is worth noting that several features are now production ready or have been enabled by default. You can find those at the end of this post.



## Azure Table Function (Alexander Sapin, Smita Kulkarni) [\#](/blog/clickhouse-release-23-05#azure-table-function-alexander-sapin-smita-kulkarni)


Experienced users of ClickHouse will be familiar with the [s3](https://clickhouse.com/docs/en/sql-reference/table-functions/s3) and [gcs](https://clickhouse.com/docs/en/sql-reference/table-functions/gcs) functions. These functions are almost identical from an implementation point of view, with the latter recently added simply to make it more intuitive for users looking to query Google GCS. Both allow the users to query files hosted in s3\-based blob storage, either to [query in\-place or to use as a source of data](https://clickhouse.com/blog/getting-data-into-clickhouse-part-3-s3) for insertion into a ClickHouse MergeTree table.


While GCS is almost [completely interoperable](https://cloud.google.com/storage/docs/interoperability) with S3, Azure’s equivalent blob storage offering deviates somewhat from the S3 specification and [requires significantly more work](https://github.com/ClickHouse/ClickHouse/pull/50604).


In 23\.5 we are pleased to announce the availability of the [azureBlobStorage](https://clickhouse.com/docs/en/sql-reference/table-functions/azureBlobStorage) table function for querying Azure Blob Storage. Users can now query files in any of the [supported formats](https://clickhouse.com/docs/en/sql-reference/formats) in Azure Blob Storage. This function differs a little in its parameters from the S3 and GCS functions, but delivers similar capabilities. Note below how we are required to specify a connection string, container and blob path to align with [Azure Blob storage concepts](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction#blob-storage-resources). In the examples below we query the [UK price paid dataset](https://clickhouse.com/docs/en/getting-started/example-datasets/uk-price-paid).



```
SELECT
	toYear(toDate(date)) AS year,
	round(avg(price)) AS price,
	bar(price, 0, 1000000, 80)
FROM azureBlobStorage('https://clickhousepublicdatasets.blob.core.windows.net/', 'ukpricepaid', 'uk_price_paid_*.parquet', 'clickhousepublicdatasets', '<key>')
GROUP BY year
ORDER BY year ASC

┌─year─┬──price─┬─bar(round(avg(price)), 0, 1000000, 80)─┐
│ 1995 │  67938 │ █████▍                             	│
│ 1996 │  71513 │ █████▋                             	│
│ 1997 │  78543 │ ██████▎                            	│
│ 1998 │  85443 │ ██████▊                            	│
│ 1999 │  96041 │ ███████▋                           	│
│ 2000 │ 107493 │ ████████▌                          	│
│ 2001 │ 118893 │ █████████▌                         	│
│ 2002 │ 137958 │ ███████████                        	│
│ 2003 │ 155894 │ ████████████▍                      	│
│ 2004 │ 178891 │ ██████████████▎                    	│
│ 2005 │ 189362 │ ███████████████▏                   	│
│ 2006 │ 203535 │ ████████████████▎                  	│
│ 2007 │ 219376 │ █████████████████▌                 	│
│ 2008 │ 217044 │ █████████████████▎                 	│
│ 2009 │ 213424 │ █████████████████                  	│
│ 2010 │ 236115 │ ██████████████████▉                	│
│ 2011 │ 232807 │ ██████████████████▌                	│
│ 2012 │ 238384 │ ███████████████████                	│
│ 2013 │ 256926 │ ████████████████████▌              	│
│ 2014 │ 280027 │ ██████████████████████▍            	│
│ 2015 │ 297287 │ ███████████████████████▊           	│
│ 2016 │ 313551 │ █████████████████████████          	│
│ 2017 │ 346516 │ ███████████████████████████▋       	│
│ 2018 │ 351101 │ ████████████████████████████       	│
│ 2019 │ 352923 │ ████████████████████████████▏      	│
│ 2020 │ 377673 │ ██████████████████████████████▏    	│
│ 2021 │ 383795 │ ██████████████████████████████▋    	│
│ 2022 │ 397233 │ ███████████████████████████████▊   	│
│ 2023 │ 358654 │ ████████████████████████████▋      	│
└──────┴────────┴────────────────────────────────────────┘

29 rows in set. Elapsed: 9.710 sec. Processed 28.28 million rows, 226.21 MB (2.91 million rows/s., 23.30 MB/s.)

```

With any table function, it often makes sense to expose an equivalent table engine for use cases where users wish to query a datasource like any other table. As shown, this simplifies subsequent queries:



```
CREATE TABLE uk_price_paid_azure
ENGINE = AzureBlobStorage('https://clickhousepublicdatasets.blob.core.windows.net/', 'ukpricepaid', 'uk_price_paid_*.parquet', 'clickhousepublicdatasets', '<key>')

SELECT
	toYear(toDate(date)) AS year,
	round(avg(price)) AS price,
	bar(price, 0, 1000000, 80)
FROM uk_price_paid_azure
GROUP BY year
ORDER BY year ASC

┌─year─┬──price─┬─bar(round(avg(price)), 0, 1000000, 80)─┐
│ 1995 │  67938 │ █████▍                             	│
│ 1996 │  71513 │ █████▋                             	│
│ 1997 │  78543 │ ██████▎                            	│

29 rows in set. Elapsed: 4.007 sec. Processed 28.28 million rows, 226.21 MB (7.06 million rows/s., 56.46 MB/s.)

```

Similar to the S3 and GCS functions, we can also use these functions to write ClickHouse data to an Azure Blob storage container, helping to address export and reverse ETL use cases.



```
INSERT INTO FUNCTION azureBlobStorage('https://clickhousepublicdatasets.blob.core.windows.net/', 'ukpricepaid', 'uk_price_paid_{_partition_id}.parquet', 'clickhousepublicdatasets', '<key>') PARTITION BY toYear(date) SELECT * FROM uk_price_paid;

```

In the above example, we use the `PARTITION BY` clause and `toYear` function and to create a Parquet file per year.


Hopefully this function unlocks projects for our users. The above function is limited in the sense it executes only on the receiving node, restricting the level of compute which can be assigned to a query. To address this we are actively working on an [azureBlobStorageCluster](https://github.com/ClickHouse/ClickHouse/pull/50795) function. This will be conceptually equivalent to [s3Cluster](https://clickhouse.com/docs/en/sql-reference/table-functions/s3Cluster) which distributes processing of files in an S3 bucket across a cluster by exploiting glob patterns. Stay tuned (and join release webinars) for updates!


We'd like to thank Jakub Kuklis who contributed the VFS level integration with Azure in 2021, with review and support provided by Kseniia Sumarokova.


## ClickHouse Keeper Client (Artem Brustovetskii) [\#](/blog/clickhouse-release-23-05#clickhouse-keeper-client-artem-brustovetskii)


Last year we released [ClickHouse Keeper](https://clickhouse.com/docs/en/guides/sre/keeper/clickhouse-keeper) to provide strongly consistent storage for data associated with ClickHouse's cluster coordination system and is fundamental to allowing ClickHouse to function as a distributed system. This supports services such as data replication, distributed DDL query execution, leadership elections, and service discovery. ClickHouse Keeper is compatible with ZooKeeper, the legacy component used for this functionality in ClickHouse.


**ClickHouse Keeper is production ready. ClickHouse Cloud is running clickhouse\-keeper at large scale to support thousands of ClickHouse deployments in a multi\-tenant environment.**


Until now users would communicate with ClickHouse Keeper by sending commands directly over TCP using tools such as `nc` or `zkCli.sh`. While sufficient for basic debugging, this made administrative tasks a less than ideal user experience and were far from convenient. To address this, in 23\.5 we introduce `keeper-client` \- a simple tool built into ClickHouse for introspecting your ClickHouse Keeper.


To experiment with the client we can use our recently [released docker compose files](/blog/clickhouse-architectures-with-docker-compose), courtesy of our support team, to quickly start a multi\-node ClickHouse cluster. In the example below, we start a 2 node deployment with a single replicated shard and 3 keeper instances:



```
git@github.com:ClickHouse/examples.git
export CHKVER=23.5
export CHVER=23.5
cd examples/docker-compose-recipes/recipes/cluster_1S_2R/
docker-compose up 

```

The above exposes our keeper instances on ports 9181, 9182 and 9183\. Connecting with the client is as simple as:



```
./clickhouse keeper-client -h 127.0.0.1 -p 9181
/ :) ruok
imok
/ :) ls
clickhouse keeper
/ :)

```

Users can also exploit a `--query` parameter, similar to the ClickHouse Client, for bash scripting.



```
./clickhouse keeper-client -h 127.0.0.1 -p 9181 --query "ls/"
clickhouse keeper

```

Further available options can be found [here](https://clickhouse.com/docs/en/operations/utilities/clickhouse-keeper-client).


## Parquet reading even faster (Michael Kolupaev) [\#](/blog/clickhouse-release-23-05#parquet-reading-even-faster-michael-kolupaev)


Recently we [blogged about the improvements](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups) we’ve made with respect to the querying of Parquet files. These were the start of what we consider to be a journey in making ClickHouse the world’s fastest tool for querying Parquet files, either via [ClickHouse Local](https://clickhouse.com/blog/extracting-converting-querying-local-files-with-sql-clickhouse-local) or ClickHouse Server. Unsatisfied with recent efforts to parallelise reading of Parquet, by exploiting row groups, 23\.5 adds further improvements.


Most of these improvements related to low level efforts to make parallel reading more efficient by [avoiding mutex locks](https://github.com/ClickHouse/ClickHouse/pull/49539). As noted in our blog, we also historically read Parquet rows in order which inherently limits reading speed. This limitation is now removed, with out of order reading the default. While this is not expected to impact most users (other than their queries being faster!), as analytical queries typically do not depend on read order, users can revert to the old behavior if required via the setting `input_format_parquet_preserve_order = true`.


As an example of the improvements, consider the following case of executing the earlier query over a single Parquet file containing all of the rows from the earlier UK price paid dataset \- this file can be downloaded from [here](https://datasets-documentation.s3.eu-west-3.amazonaws.com/uk-house-prices/parquet/house_prices.parquet).



```
--23.4

SELECT
	toYear(toDate(date)) AS year,
	round(avg(price)) AS price,
	bar(price, 0, 1000000, 80)
FROM file('house_prices.parquet')
GROUP BY year
ORDER BY year ASC

29 rows in set. Elapsed: 0.367 sec.

--23.5

SELECT
	toYear(toDate(date)) AS year,
	round(avg(price)) AS price,
	bar(price, 0, 1000000, 80)
FROM file('house_prices.parquet')
GROUP BY year
ORDER BY year ASC

29 rows in set. Elapsed: 0.240 sec.

```

For users writing Parquet files based on data in ClickHouse, there are three [main approaches](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing#writing-local-files) \- using `INTO OUTFILE`, `INSERT INTO FUNCTION` or by simply redirecting  `SELECT FORMAT Parquet` to a file. Historically we [have recommended users](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups) utilize the latter of these two approaches, principally because `INTO OUTFILE` could [reproduce very large row group](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups#importance-of-row-groups) sizes due to some less than ideal [internal behaviors](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups#importance-of-row-groups). This would [impact later read performance](https://clickhouse.com/blog/apache-parquet-clickhouse-local-querying-writing-internals-row-groups#importance-of-row-groups). This could be a complex issue to debug and would require a deep understanding of Parquet. Fortunately, this issue is [now addressed](https://github.com/ClickHouse/ClickHouse/pull/49325) \- feel free to use `INTO OUTFILE` as you might for other formats!


While the above all represent significant improvements, this journey is still not complete. There are still queries we need to further improve \- specifically the querying of single large Parquet files. For those interested, follow our open [benchmarks for Parquet at ClickBench](https://benchmark.clickhouse.com/#eyJzeXN0ZW0iOnsiQXRoZW5hIChwYXJ0aXRpb25lZCkiOmZhbHNlLCJBdGhlbmEgKHNpbmdsZSkiOmZhbHNlLCJBdXJvcmEgZm9yIE15U1FMIjpmYWxzZSwiQXVyb3JhIGZvciBQb3N0Z3JlU1FMIjpmYWxzZSwiQnl0ZUhvdXNlIjpmYWxzZSwiY2hEQiI6ZmFsc2UsIkNpdHVzIjpmYWxzZSwiQ2xpY2tIb3VzZSAoZGF0YSBsYWtlLCBwYXJ0aXRpb25lZCkiOmZhbHNlLCJDbGlja0hvdXNlIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOnRydWUsIkNsaWNrSG91c2UgKFBhcnF1ZXQsIHNpbmdsZSkiOnRydWUsIkNsaWNrSG91c2UiOmZhbHNlLCJDbGlja0hvdXNlICh0dW5lZCkiOmZhbHNlLCJDbGlja0hvdXNlICh6c3RkKSI6ZmFsc2UsIkNsaWNrSG91c2UgQ2xvdWQiOmZhbHNlLCJDbGlja0hvdXNlIENsb3VkIChBV1MpIjpmYWxzZSwiQ2xpY2tIb3VzZSBDbG91ZCAoR0NQKSI6ZmFsc2UsIkNsaWNrSG91c2UgKHdlYikiOmZhbHNlLCJDcmF0ZURCIjpmYWxzZSwiRGF0YWJlbmQiOmZhbHNlLCJEYXRhRnVzaW9uIChzaW5nbGUgcGFycXVldCkiOnRydWUsIkFwYWNoZSBEb3JpcyI6ZmFsc2UsIkRydWlkIjpmYWxzZSwiRHVja0RCIChQYXJxdWV0LCBwYXJ0aXRpb25lZCkiOnRydWUsIkR1Y2tEQiI6ZmFsc2UsIkVsYXN0aWNzZWFyY2giOmZhbHNlLCJFbGFzdGljc2VhcmNoICh0dW5lZCkiOmZhbHNlLCJHcmVlbnBsdW0iOmZhbHNlLCJIZWF2eUFJIjpmYWxzZSwiSHlkcmEiOmZhbHNlLCJJbmZvYnJpZ2h0IjpmYWxzZSwiS2luZXRpY2EiOmZhbHNlLCJNYXJpYURCIENvbHVtblN0b3JlIjpmYWxzZSwiTWFyaWFEQiI6ZmFsc2UsIk1vbmV0REIiOmZhbHNlLCJNb25nb0RCIjpmYWxzZSwiTXlTUUwgKE15SVNBTSkiOmZhbHNlLCJNeVNRTCI6ZmFsc2UsIlBpbm90IjpmYWxzZSwiUG9zdGdyZVNRTCI6ZmFsc2UsIlBvc3RncmVTUUwgKHR1bmVkKSI6ZmFsc2UsIlF1ZXN0REIgKHBhcnRpdGlvbmVkKSI6ZmFsc2UsIlF1ZXN0REIiOmZhbHNlLCJSZWRzaGlmdCI6ZmFsc2UsIlNlbGVjdERCIjpmYWxzZSwiU2luZ2xlU3RvcmUiOmZhbHNlLCJTbm93Zmxha2UiOmZhbHNlLCJTUUxpdGUiOmZhbHNlLCJTdGFyUm9ja3MiOmZhbHNlLCJUaW1lc2NhbGVEQiAoY29tcHJlc3Npb24pIjpmYWxzZSwiVGltZXNjYWxlREIiOmZhbHNlfSwidHlwZSI6eyJzdGF0ZWxlc3MiOnRydWUsIm1hbmFnZWQiOnRydWUsIkphdmEiOnRydWUsImNvbHVtbi1vcmllbnRlZCI6dHJ1ZSwiQysrIjp0cnVlLCJNeVNRTCBjb21wYXRpYmxlIjp0cnVlLCJyb3ctb3JpZW50ZWQiOnRydWUsIkMiOnRydWUsIlBvc3RncmVTUUwgY29tcGF0aWJsZSI6dHJ1ZSwiQ2xpY2tIb3VzZSBkZXJpdmF0aXZlIjp0cnVlLCJlbWJlZGRlZCI6dHJ1ZSwiYXdzIjp0cnVlLCJnY3AiOnRydWUsInNlcnZlcmxlc3MiOnRydWUsIlJ1c3QiOnRydWUsInNlYXJjaCI6dHJ1ZSwiZG9jdW1lbnQiOnRydWUsInRpbWUtc2VyaWVzIjp0cnVlfSwibWFjaGluZSI6eyJzZXJ2ZXJsZXNzIjp0cnVlLCIxNmFjdSI6dHJ1ZSwiTCI6dHJ1ZSwiTSI6dHJ1ZSwiUyI6dHJ1ZSwiWFMiOnRydWUsImM2YS40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsImM2YS5tZXRhbCwgNTAwZ2IgZ3AyIjp0cnVlLCJjNS40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsIjYwIHRocmVhZHMgKGlkZWFsKSI6dHJ1ZSwiNjAgdGhyZWFkcyAobG9jYWwpIjp0cnVlLCIxOTJHQiI6dHJ1ZSwiMjRHQiI6dHJ1ZSwiMzYwR0IiOnRydWUsIjQ4R0IiOnRydWUsIjcyMEdCIjp0cnVlLCI5NkdCIjp0cnVlLCI3MDhHQiI6dHJ1ZSwibTVkLjI0eGxhcmdlIjp0cnVlLCJtNmkuMzJ4bGFyZ2UiOnRydWUsImM1bi40eGxhcmdlLCA1MDBnYiBncDIiOnRydWUsImM2YS40eGxhcmdlLCAxNTAwZ2IgZ3AyIjp0cnVlLCJkYzIuOHhsYXJnZSI6dHJ1ZSwicmEzLjE2eGxhcmdlIjp0cnVlLCJyYTMuNHhsYXJnZSI6dHJ1ZSwicmEzLnhscGx1cyI6dHJ1ZSwiUzI0Ijp0cnVlLCJTMiI6dHJ1ZSwiMlhMIjp0cnVlLCIzWEwiOnRydWUsIjRYTCI6dHJ1ZSwiWEwiOnRydWV9LCJjbHVzdGVyX3NpemUiOnsiMSI6dHJ1ZSwiMiI6dHJ1ZSwiNCI6dHJ1ZSwiOCI6dHJ1ZSwiMTYiOnRydWUsIjMyIjp0cnVlLCI2NCI6dHJ1ZSwiMTI4Ijp0cnVlLCJzZXJ2ZXJsZXNzIjp0cnVlLCJ1bmRlZmluZWQiOnRydWV9LCJtZXRyaWMiOiJob3QiLCJxdWVyaWVzIjpbdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZSx0cnVlLHRydWUsdHJ1ZV19).


![clickbench_parquet.png](/uploads/clickbench_parquet_241e6e3bd1.png)
## Wrap up [\#](/blog/clickhouse-release-23-05#wrap-up)


As mentioned in the introduction, several features are now enabled by default or considered production ready (no longer experimental). In particular, geographical data types ([Point](https://clickhouse.com/docs/en/sql-reference/data-types/geo#point), [Ring](https://clickhouse.com/docs/en/sql-reference/data-types/geo#ring), [Polygon](https://clickhouse.com/docs/en/sql-reference/data-types/geo#polygon), [MultiPolygon](https://clickhouse.com/docs/en/sql-reference/data-types/geo#multipolygon)) and [functions](https://clickhouse.com/docs/en/sql-reference/functions/geo) (distance, area, perimeter, union, intersection, convex hull, etc) are now production ready in 23\.5!


In addition, compressed marks and indices on disk (first available in 22\.9\) are now available by default. The first query after server startup has never been faster.


Last, but definitely not least, the Query Results Cache is now considered ‘production ready’. We have written, at length, about the feature in a post titled *[Introducing the ClickHouse Query Cache](https://clickhouse.com/blog/introduction-to-the-clickhouse-query-cache-and-design)*. The query cache is based on the idea that sometimes there are situations where it is okay to cache the result of expensive `SELECT` queries such that further executions of the same queries can be served directly from the cache.


## New Contributors [\#](/blog/clickhouse-release-23-05#new-contributors)


A special welcome to all the new contributors to 23\.5! ClickHouse's popularity is, in large part, due to the efforts of the community who contributes. Seeing that community grow is always humbling.


If you see your name here, please reach out to us...but we will be finding you on twitter, etc as well.



> Alexey Gerasimchuck, Alexey Gerasimchuk, AnneClickHouse, Duyet Le, Eridanus, Feng Kaiyu, Ivan Takarlikov, Jordi, János Benjamin Antal, Kuba Kaflik, Li Shuai, Lucas Chang, M1eyu2018, Mal Curtis, Manas Alekar, Misz606, Mohammad Arab Anvari, Raqbit, Roman Vlasenko, Sergey Kazmin, Sergey Kislov, Shane Andrade, Sorck, Stanislav Dobrovolschii, Val Doroshchuk, Valentin Alexeev, Victor Krasnov, Vincent, Yusuke Tanaka, Ziy1\-Tan, alekar, auxten, cangyin, darkkeks, frinkr, ismailakpolat, johanngan, laimuxi, libin, lihaibo42, mauidude, merlllle, ongkong, sslouis, vitac, wangxiaobo, xmy, zy\-kkk, 你不要过来啊

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts

[View all Blogs](/blog)![](/_next/image?url=%2Fuploads%2FFINAL_1_0d999c9df8.jpg&w=828&q=75)Product### [Agents can now provision ClickHouse and Postgres on ClickHouse Cloud](/blog/stripe-projects)

Chloé Carasso dit Carson · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fdatadog_clickhouse_partnership_9b7ff1f4a5.png&w=828&q=75)Product### [Datadog and ClickHouse partner to bring full\-fidelity data to modern observability](/blog/datadog-and-clickhouse-partner)

ClickHouse · Jun 10, 2026![](/_next/image?url=%2Fuploads%2Fclickhouse_agents_jun2026_image7_e65251f928.png&w=828&q=75)Product### [ClickHouse Agents: Claude\-powered agentic analytics, now in public beta](/blog/clickhouse-agents-beta)

Ryadh Dahimene · Jun 9, 2026![](/_next/image?url=%2Fuploads%2FQRT_Customer_Story_Cover_cdf374dbd5.jpg&w=828&q=75)User stories### [How QRT powers real\-time research and risk management at petabyte scale](/blog/qrt)

ClickHouse · Jun 9, 2026Follow us[![X](/socials/x.svg)X](https://x.com/ClickhouseDB "X")[![Bluesky](/socials/bluesky.svg)Bluesky](https://bsky.app/profile/clickhouse.com "Bluesky")[![Slack](/socials/slack.svg)Slack](/slack "Slack")[![GitHub](/socials/github.svg)GitHub](https://github.com/ClickHouse/ClickHouse "GitHub")[![Telegram](/socials/telegram.svg)Telegram](https://telegram.me/clickhouse_en "Telegram")[![Meetup](/socials/meetup.svg)Meetup](https://www.meetup.com/pro/clickhouse "Meetup")[![Rss](/socials/rss.svg)Rss](/rss.xml "Rss")
