---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"Window
topic: window-and-array-functions-for-git-commit-sequences-clickhouse
ch_version_introduced: '9.1'
last_updated: '2026-09-07'
chunk_index: 4
total_chunks_in_doc: 6
---

2021-05-11 00:00:00 │ │ ANDREI STAROVEROV │ 2021-05-13 00:00:00 │ │ ANDREI STAROVEROV │ 2021-05-14 00:00:00 │ └─────────────────────────────┴─────────────────────┘ 10 rows in set. Elapsed: 0.362 sec. Processed 61.90 thousand rows, 389.87 KB (171.06 thousand rows/s., 1.08 MB/s.) [✎](https://sql.clickhouse.com?query_id=5AUH3VVENJ6CFEFWDKW5ZH) ```

For each row, we now need to determine if it's consecutive, i.e., 1 day after the previous value. For this, we need to create a window per author via a `PARTITION BY`, and simply grab the preceding row using the [any](https://clickhouse.com/docs/en/sql-reference/aggregate-functions/reference/any/) function i.e.,

```
1any(day) OVER (PARTITION BY author ORDER BY day ASC ROWS BETWEEN 1
2PRECEDING AND CURRENT ROW) AS previous_commit
```
Copy command
We visualize this step below. Note the importance of the `ORDER BY`, which sorts the values within each partition’s window:

![window-function-example-2.png](/_next/image?url=%2Fuploads%2Fwindow_function_example_2_9dd318d7f0.png&w=2048&q=75)

Now that we have the previous day as a column `previous_commit`, we can compute the difference in days with the current value using the [dateDiff](https://clickhouse.com/docs/en/sql-reference/functions/date-time-functions/#date_diff) function. Finally, we add a `consecutive` column [using a conditional](https://clickhouse.com/docs/en/sql-reference/functions/conditional-functions/#if) \- set to 1 if the difference is 1, 0 otherwise.

```

SELECT
    author,
    toDate(day) as day,
    any(day) OVER (PARTITION BY author ORDER BY day ASC ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS previous_commit,
    dateDiff('day', previous_commit, day) AS day_diff,
    if(day_diff = 1, 1, 0) AS consecutive
FROM
(
   SELECT author, toStartOfDay(time) AS day FROM git.commits GROUP BY author, day ORDER BY author ASC, day ASC
)
LIMIT 10
 [✎](https://sql.clickhouse.com?query_id=1BSPOBWAT6PUOCYXYNPNML)

```

```


┌─author──────────────────────┬────────day─┬─previous_commit─┬─day_diff─┬─consecutive─┐
│ 1lann                       │ 2022-03-07 │      2022-03-07 │        0 │           0 │
│ 20018712                    │ 2020-09-17 │      2020-09-17 │        0 │           0 │
│ 243f6a8885a308d313198a2e037 │ 2020-12-10 │      2020-12-10 │        0 │           0 │
│ 3ldar-nasyrov               │ 2021-03-16 │      2021-03-16 │        0 │           0 │
│ 821008736@qq.com            │ 2019-04-26 │      2019-04-26 │        0 │           0 │
│ ANDREI STAROVEROV           │ 2021-05-09 │      2021-05-09 │        0 │           0 │
│ ANDREI STAROVEROV           │ 2021-05-10 │      2021-05-09 │        1 │           1 │
│ ANDREI STAROVEROV           │ 2021-05-11 │      2021-05-10 │        1 │           1 │
│ ANDREI STAROVEROV           │ 2021-05-13 │      2021-05-11 │        2 │           0 │
│ ANDREI STAROVEROV           │ 2021-05-14 │      2021-05-13 │        1 │           1 │
└─────────────────────────────┴────────────┴─────────────────┴──────────┴─────────────┘


10 rows in set. Elapsed: 0.020 sec. Processed 61.90 thousand rows, 389.87 KB (3.04 million rows/s., 19.17 MB/s.)


```
