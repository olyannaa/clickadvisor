---
source: blog
url: https://clickhouse.com/docs/guides/best-practices/sparse-primary-indexes#the-primary-index-has-one-entry-per-granule
topic: index-based-pruning-in-clickhouse
ch_version_introduced: '5.366'
last_updated: '2026-06-12'
chunk_index: 9
total_chunks_in_doc: 15
---

6 │ └─────────────────────────────────────────────────────────┘ ``` This output doesn’t help us as it only includes the base query plan with the primary key index information. We need to also add `projections=1` so that projection analysis is included in the output:

```

```
1EXPLAIN indexes=1, projections=1, pretty=1, compact= 1 
2SELECT town, count(), round(avg(price)) AS avgPrice, argAndMax(date, price)
3FROM uk_price_paid
4WHERE district = 'BURNLEY'
5GROUP BY ALL
6ORDER BY count() DESC LIMIT 10
7SETTINGS
8    use_query_condition_cache = 0,
9    optimize_use_projections = 1,
10    output_format_pretty_max_value_width=65,
11    output_format_pretty_row_numbers=1;
```

```

```
   ┌─explain───────────────────────────────────────────────────────────┐
 1. │ Output: town, count(), avgPrice, argAndMax(date, price)           │
 2. │                                                                   │
 3. │ Limit (preliminary LIMIT)                                         │
 4. │ └──Sorting (Sorting for ORDER BY)                                 │
 5. │    └──Aggregating                                                 │
 6. │       └──ReadFromMergeTree (default.uk_price_paid)                │
 7. │             Indexes:                                              │
 8. │               PrimaryKey                                          │
 9. │                 Condition: true                                   │
10. │                 Parts: 11/11                                      │
11. │                 Granules: 29744/29744                             │
12. │               Ranges: 11                                          │
13. │             Projections:                                          │
14. │               Name: by_district                                   │
15. │                 Description: Projection has been analyzed and wil⋯│
16. │                 Condition: (district in ['BURNLEY', 'BURNLEY'])   │
17. │                 Search Algorithm: binary search                   │
18. │                 Parts: 11                                         │
19. │                 Marks: 72                                         │
20. │                 Ranges: 11                                        │
21. │                 Rows: 589824                                      │
22. │                 Filtered Parts: 0                                 │
    └───────────────────────────────────────────────────────────────────┘

```

Let’s go through what’s happening here, starting with the **Indexes** section:

The primary key index couldn't help with this query \- `Condition: true` on Row 9 means it applied no filtering, so all 11 parts (Row 10\) and 29,744 granules (Row 11\) have to be considered.

Moving on to the **Projections** section

- `Filtered Parts: 0` on Row 22 indicates that no parts could be eliminated entirely, which means `BURNLEY` appears in all 11 parts.
- Row 19 narrows the search to 72 granules (or marks)
- Each granule contains 8,192 rows by default, which gives us the count on line 21 (72 \* 8,192\=589,824\)
- Those 72 granules are spread across 11 parts (Row 18\), and since `BURNLEY` rows are stored contiguously within each part, that gives us one continuous range per part \- 11 ranges in total (Row 20\).

The table below shows the times without projection and with projection for districts with both more and fewer properties sold than Burnley:
