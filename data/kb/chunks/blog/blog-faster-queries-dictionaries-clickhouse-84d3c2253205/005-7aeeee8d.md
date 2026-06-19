---
source: blog
url: https://clickhouse.com/blog/real-world-data-noaa-climate-data
topic: using-dictionaries-to-accelerate-queries
ch_version_introduced: '45.8'
last_updated: '2026-06-12'
chunk_index: 5
total_chunks_in_doc: 15
---

to avoid de\-duplication, and follow the principle of keeping it normalized and separate on the `stations` table we need a full join (in reality we would probably leave the `location` and `name` denormalized and accept the storage cost):

```

SELECT
    tempMax / 10 AS maxTemp,
    station_id,
    date,
    stations.name AS name,
    (stations.lat, stations.lon) AS location
FROM noaa
INNER JOIN stations ON noaa.station_id = stations.station_id
WHERE stations.country_code = 'PO'
ORDER BY tempMax DESC
LIMIT 5

┌─maxTemp─┬─station_id──┬───────date─┬─name───────────┬─location──────────┐
│    45.8 │ PO000008549 │ 1944-07-30 │ COIMBRA        │ (40.2,-8.4167)    │
│    45.4 │ PO000008562 │ 2003-08-01 │ BEJA           │ (38.0167,-7.8667) │
│    45.2 │ PO000008562 │ 1995-07-23 │ BEJA           │ (38.0167,-7.8667) │
│    44.5 │ POM00008558 │ 2003-08-01 │ EVORA/C. COORD │ (38.533,-7.9)     │
│    44.2 │ POM00008558 │ 2022-07-13 │ EVORA/C. COORD │ (38.533,-7.9)     │
└─────────┴─────────────┴────────────┴────────────────┴───────────────────┘

5 rows in set. Elapsed: 0.488 sec. Processed 1.08 billion rows, 14.06 GB (2.21 billion rows/s., 28.82 GB/s.)

 [✎](https://sql.clickhouse.com?query_id=W7QQFHSZVARIBM8FLCJFJF)

```

This is unfortunately slower than our previous denormalized approach as it requires a full table scan. The reason for this can be found in [our documentation](https://clickhouse.com/docs/en/sql-reference/statements/select/join/#performance).

> When running a JOIN, there is no optimization of the order of execution in relation to other stages of the query. The join (a search in the right table) is run before filtering in WHERE and before aggregation.”

The documentation also suggests dictionaries as a possible solution. Let's now demonstrate how we can improve this query performance using a dictionary now that the data is normalized.

## Creating a dictionary [\#](/blog/faster-queries-dictionaries-clickhouse#creating-a-dictionary)

Dictionaries provide us with an in\-memory key\-value pair representation of our data, optimized for low latent lookup queries. We can utilize this structure to improve the performance of queries in general, with JOINs particularly benefiting where one side of the JOIN represents a look\-up table that fits into memory.

### Choosing a source and key [\#](/blog/faster-queries-dictionaries-clickhouse#choosing-a-source-and-key)

In ClickHouse Cloud, the dictionary itself can currently be populated from two sources: local ClickHouse tables and HTTP URLs\*. The dictionary's contents can then be configured to reload periodically to reflect any changes in the source data.

> \* We anticipate expanding this in the future to include support for other sources supported in OSS.

Below we create our dictionary using the `stations` table as the source.
