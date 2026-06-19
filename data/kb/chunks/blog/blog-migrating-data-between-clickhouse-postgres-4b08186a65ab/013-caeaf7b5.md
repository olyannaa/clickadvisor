---
source: blog
url: https://clickhouse.com/docs/integrations/clickpipes/postgres
topic: clickhouse-and-postgresql-a-match-made-in-data-heaven-part-1
ch_version_introduced: '28535.465'
last_updated: '2026-06-12'
chunk_index: 13
total_chunks_in_doc: 14
---

requires the user to split their data on a column of appropriate cardinality. However, other services, or self\-managed instances, may not impose this restriction. Using our new MergeTree table, we can execute our earlier queries directly in ClickHouse.

### The average price per year for flats in the UK [\#](/blog/migrating-data-between-clickhouse-postgres#the-average-price-per-year-for-flats-in-the-uk)

```

SELECT
	toYear(date) AS year,
	round(avg(price)) AS price
FROM uk_price_paid
WHERE type = 'flat'
GROUP BY year
ORDER BY year ASC

┌─year─┬──price─┐
│ 1995 │  59004 │
│ 1996 │  63913 │
│ 1997 │  72302 │
│ 1998 │  80775 │
│ 1999 │  93646 │
...
│ 2019 │ 300938 │
│ 2020 │ 319547 │
│ 2021 │ 310626 │
│ 2022 │ 298977 │
└──────┴────────┘

28 rows in set. Elapsed: 0.079 sec. Processed 5.01 million rows, 35.07 MB (63.05 million rows/s., 441.37 MB/s.)
[✎](https://sql.clickhouse.com?query_id=3CQY9DMYYK7PJSDRPGBJAE)

```

### Most expensive postcodes in a city [\#](/blog/migrating-data-between-clickhouse-postgres#most-expensive-postcodes-in-a-city-2)

```

SELECT
	postcode1,
	round(avg(price)) AS price
FROM uk_price_paid
WHERE (town = 'BRISTOL') AND (postcode1 != '')
GROUP BY postcode1
ORDER BY price DESC
LIMIT 10

┌─postcode1─┬──price─┐
│ BS1   	│ 410726 │
│ BS19  	│ 369000 │
│ BS18  	│ 337000 │
│ BS40  	│ 323854 │
│ BS9   	│ 313248 │
│ BS8   	│ 301595 │
│ BS41  	│ 300802 │
│ BS6   	│ 272332 │
│ BS35  	│ 260563 │
│ BS36  	│ 252943 │
└───────────┴────────┘

10 rows in set. Elapsed: 0.077 sec. Processed 27.69 million rows, 30.21 MB (358.86 million rows/s., 391.49 MB/s.)

[✎](https://sql.clickhouse.com?query_id=VX9XNLHPDAU9BROIOJNFXH)

```

### Postcodes in London with the largest percentage price change in the last 20 yrs [\#](/blog/migrating-data-between-clickhouse-postgres#postcodes-in-london-with-the-largest-percentage-price-change-in-the-last-20-yrs-2)

```

SELECT
	postcode1,
	medianIf(price, toYear(date) = 2002) AS median_2002,
	medianIf(price, toYear(date) = 2022) AS median_2022,
	round(((median_2022 - median_2002) / median_2002) * 100) AS percent_change
FROM uk_price_paid
WHERE town = 'LONDON'
GROUP BY postcode1
ORDER BY percent_change DESC

┌─postcode1─┬─median_2002─┬─median_2022─┬─percent_change─┐
│ EC3A  	│  	260000 │	16000000 │       	6054 │
│ SW1A  	│  	525000 │	17500000 │       	3233 │
│ EC2M  	│  	250000 │   4168317.5 │       	1567 │
│ EC3R  	│  	230000 │ 	2840000 │       	1135 │
│ W1S   	│  	590000 │ 	6410000 │        	986 │

191 rows in set. Elapsed: 0.062 sec. Processed 2.62 million rows, 19.45 MB (41.98 million rows/s., 311.48 MB/s.)

[✎](https://sql.clickhouse.com?query_id=7PEVSKK5MBGK5PTEQ6FUOD)

```
