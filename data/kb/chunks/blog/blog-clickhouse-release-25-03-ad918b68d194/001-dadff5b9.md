---
source: blog
url: https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9
topic: clickhouse-release-25-3
ch_version_introduced: '25.3'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 7
---

# ClickHouse Release 25\.3

\-\>Scroll to topBack- [Blog](/blog)
- /
- [Engineering](/blog?category=engineering)

Copy pageCopied!More actions- ![View as Markdown](/_next/static/media/icon-markdown.c048adbf.svg)**View as Markdown** Open this page in Markdown
- ![Open in ChatGPT](/_next/static/media/icon-chatgpt.f6a7ebb4.svg)**Open in ChatGPT** Ask questions about this page
- ![Open in Claude](/_next/static/media/icon-claude.18912ab9.svg)**Open in Claude** Ask questions about this page
- ![Open in v0](/_next/static/media/icon-v0.2caf962b.svg)**Open in v0** Ask questions about this page
# ClickHouse Release 25\.3

![](/_next/image?url=%2Fuploads%2Fneutral_avatar_400804ae96_5c370e757b.png&w=96&q=75)[ClickHouse](/authors/clickhouse)Mar 27, 2025 · 11 minutes read
pre div.p\-2 {
 margin\-bottom: 2rem;
}

Another month goes by, which means it’s time for another release!

ClickHouse version 25\.3 contains 18 new features 🌱 13 performance optimizations 🐣 48 bug fixes 🌦️

This release brings query support for the AWS Glue and Unity catalogs, the new query condition cache, automatic parallelization when querying S3, and new array functions!

## New Contributors [\#](/blog/clickhouse-release-25-03#new-contributors)

A special welcome to all the new contributors in 25\.3! The growth of ClickHouse's community is humbling, and we are always grateful for the contributions that have made ClickHouse so popular.

Below are the names of the new contributors:

*Andrey Nehaychik, Arnaud Briche, Cheryl Tuquib, Didier Franc, Filipp Abapolov, Ilya Kataev, Jason Wong, Jimmy Aguilar Mena, Mark Roberts, Onkar Deshpande, Shankar Iyer, Tariq Almawash, Vico.Wu, f.abapolov, flyaways, otlxm, pheepa, rienath, talmawash*

Hint: if you’re curious how we generate this list… [here](https://gist.github.com/gingerwizard/5a9a87a39ba93b422d8640d811e269e9).

You can also [view the slides from the presentation](https://presentations.clickhouse.com/2025-release-25.3/).

## AWS Glue and Unity catalogs [\#](/blog/clickhouse-release-25-03#aws-glue-and-unity-catalogs)

### Contributed by Alexander Sapin [\#](/blog/clickhouse-release-25-03#contributed-by-alexander-sapin)

This release adds support for more Lakehouse catalogs \- AWS Glue and Unity.

You can query Apache Iceberg tables via AWS Glue by first creating a database engine:

```

```
1CREATE DATABASE demo_catalog 
2ENGINE = DataLakeCatalog
3SETTINGS catalog_type = 'glue', region = 'us-west-2',
4    aws_access_key_id = 'AKIA...', aws_secret_access_key = '...';
```

```

And then querying the data:

```

```
1SHOW TABLES 
2FROM demo_catalog;
3
4SELECT * 
5FROM "demo_catalog"."db.table";
```

```

There’s support for Apache Iceberg and Delta Lake tables via the Unit catalog. Again, you’ll need to create a database engine:

```

```
1CREATE DATABASE unity_demo
2ENGINE = DataLakeCatalog(
3    'https://endpoint.cloud.databricks.com/api/2.1/unity-catalog')
4SETTINGS catalog_type = 'unity',
5    warehouse = 'workspace', catalog_credential = '...'
```

```

And then you can query it like a normal table:

```

```
1SHOW TABLES 
2FROM unity_demo;
3
4SELECT * 
5FROM "unity_demo"."db.table";
```


```

## JSON data type is production\-ready [\#](/blog/clickhouse-release-25-03#json-data-type-is-production-ready)
