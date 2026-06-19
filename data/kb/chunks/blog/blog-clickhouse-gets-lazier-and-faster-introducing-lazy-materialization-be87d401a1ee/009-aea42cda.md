---
source: blog
url: https://clickhouse.com/docs/parts)**
topic: clickhouse-gets-lazier-and-faster-introducing-lazy-materialization
ch_version_introduced: '150.96'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 14
---

## ② Adding PREWHERE [\#](/blog/clickhouse-gets-lazier-and-faster-introducing-lazy-materialization#-adding-prewhere) We run the same query again, this time with [PREWHERE](https://clickhouse.com/docs/optimize/prewhere) enabled (but still without lazy materialization). PREWHERE adds an additional layer of efficiency filtering out irrelevant data before reading non\-filter columns from disk:

```

```
SELECT
    helpful_votes,
    product_title,
    review_headline,
    review_body
FROM amazon.amazon_reviews
WHERE review_date >= '2010-01-01'
AND product_category = 'Digital_Ebook_Purchase'
AND verified_purchase
AND star_rating > 4
ORDER BY helpful_votes DESC
LIMIT 3
FORMAT Null
SETTINGS
    optimize_move_to_prewhere = true,
    query_plan_optimize_lazy_materialization = false;
```

```

```

```
0 rows in set. Elapsed: 61.148 sec. Processed 53.01 million rows, 16.28 GB (866.94 thousand rows/s., 266.24 MB/s.)
Peak memory usage: 583.30 MiB.
```

```

With PREWHERE enabled, the query processed the same 53 million rows but read significantly less column data, 16\.28 GB vs. 27\.67 GB, and completed 36% faster (61 seconds vs. 96 seconds), while also slightly reducing peak memory usage.

To understand this improvement, let’s briefly walk through how PREWHERE changes the way ClickHouse processes the query.

Instead of streaming all selected column granules up front, ClickHouse begins PREWHERE processing by ① loading only the primary key column granules identified by the index analysis to check which ones actually contain matches. In this case, all selected granules do match, so ② the positionally aligned granules for the next filter column—`verified_purchase`—are selected to be loaded for further filtering:

![03-PW-01.gif](/uploads/03_PW_01_1992a16e83.gif)
Next, ClickHouse ① reads the selected `verified_purchase` column granules to evaluate the filter `verified_purchase` (which is a shortcut for `verified_purchase == True` ).

In this case, three out of four granules contain matching rows, so only ② their positionally aligned granules from the next filter column—`star_rating`—are selected for further processing:

![03-PW-02.gif](/uploads/03_PW_02_7d17b6f283.gif)
Finally, ClickHouse reads the three selected granules from the `star_rating` column to evaluate the last filter `star_rating > 4`.

Two of the three granules contain matching rows, so just the positionally aligned granules from the remaining columns—`helpful_votes`, `product_title`, `review_headline`, and `review_body`—are selected to be loaded for further processing:

![03-PW-03.gif](/uploads/03_PW_03_08d41def52.gif)
With that, PREWHERE processing is complete.
