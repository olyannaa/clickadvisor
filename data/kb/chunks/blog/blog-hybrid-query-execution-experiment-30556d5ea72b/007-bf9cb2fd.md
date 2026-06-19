---
source: blog
url: https://www.youtube.com/watch?v=Rhe-kUyrFUE&list=PL0Z2YDlm0b3gcY5R_MUo4fT5bPqUQ66ep
topic: a-hybrid-query-execution-experiment
ch_version_introduced: '0.140'
last_updated: '2026-06-12'
chunk_index: 7
total_chunks_in_doc: 8
---

we could restrict the number of records being returned by the remote join, as shown in the diagram below: ![Hybrid Query Execution Diagram (1).png](/uploads/Hybrid_Query_Execution_Diagram_1_787e121532.png) Let’s restrict the number of records to 1,000, as shown in the query below:

```
WITH pypiProjects AS (
  SELECT home_page, projects.name, sum(count) AS count
  FROM remoteSecure(
    'clickpy-clickhouse.clickhouse.com',
    'pypi.pypi_downloads',
    'mark', {password:String}
  ) AS pypi_downloads
  INNER JOIN
  (
    SELECT name, argMax(home_page, version) AS home_page
    FROM remoteSecure(
      'clickpy-clickhouse.clickhouse.com',
      'pypi.projects',
      'mark', {password:String}
    )
    GROUP BY name
  ) AS projects ON projects.name = pypi_downloads.project
  GROUP BY ALL 
  ORDER BY count DESC 
  LIMIT 1000
) 
SELECT
    name,
    replaceOne(home_page, 'https://github.com/', '') AS repository,
    count,
    gh.stargazers_count AS stars
FROM pypiProjects
INNER JOIN
(
    SELECT *
    FROM file('data/*.json', JSONEachRow)
) AS gh ON gh.svn_url = pypiProjects.home_page
GROUP BY ALL
ORDER BY count DESC
LIMIT 10;

┌─name───────────────┬─repository─────────────────┬───────count─┬─stars─┐
│ boto3              │ boto/boto3                 │ 16031894410 │  8440 │
│ botocore           │ boto/botocore              │ 11033306159 │  1352 │
│ certifi            │ certifi/python-certifi     │  8606959885 │   707 │
│ s3transfer         │ boto/s3transfer            │  8575775398 │   189 │
│ python-dateutil    │ dateutil/dateutil          │  8144178765 │  2164 │
│ charset-normalizer │ Ousret/charset_normalizer  │  5891178066 │   448 │
│ jmespath           │ jmespath/jmespath.py       │  5405618311 │  1975 │
│ pyasn1             │ pyasn1/pyasn1              │  5378303214 │    18 │
│ google-api-core    │ googleapis/python-api-core │  5022394699 │    98 │
│ importlib-metadata │ python/importlib_metadata  │  4353215364 │   101 │
└────────────────────┴────────────────────────────┴─────────────┴───────┘
10 rows in set. Elapsed: 1.758 sec. Processed 2.08 thousand rows, 14.97 MB (1.18 thousand rows/s., 8.51 MB/s.)

Peak memory usage: 448.22 MiB.

```

This time it takes just under 2 seconds because we aren’t streaming so many records to ClickHouse Local before doing the join with the GitHub data. This isn’t a perfect solution, however, because we could have ended up with fewer than 10 records if more than 990 of our 1,000 records didn’t have a match in the GitHub dataset.

## Summary [\#](/blog/hybrid-query-execution-experiment#summary)

And that’s about it for now. I’d be curious to know what you all think? Can you see a real use case for this functionality? If so let us know in the comments or on [ClickHouse Slack](https://clickhouse.com/slack).

Share this postCopy URLShare on Y CombinatorShare on TwitterShare on BlueSkyShare on FacebookShare on LinkedIn### Subscribe to our newsletter

Stay informed on feature releases, product roadmap, support, and cloud offerings!Loading form...## Recent posts
