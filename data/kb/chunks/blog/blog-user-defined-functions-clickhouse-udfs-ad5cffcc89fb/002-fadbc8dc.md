---
source: blog
url: https://schema.org","@type":"BlogPosting","headline":"User\-defined
topic: user-defined-functions-in-clickhouse-cloud-clickhouse
ch_version_introduced: '0.011'
last_updated: '2026-09-07'
chunk_index: 2
total_chunks_in_doc: 6
---

UDF Refresher \# User\-defined functions (UDF) allow users to extend the behavior of ClickHouse, by creating lambda expressions that can utilize SQL constructs and functions. These functions can then be used like any in\-built function in a query.

To create our UDF, we use the `CREATE FUNCTION <name>` syntax and specify our method signature as a lambda expression. In it its simplest form, this might look like the following, which returns the string `odd` or `even` depending on the parity of the number:

```

CREATE FUNCTION parity_str AS (n) -> if(n % 2, 'odd', 'even');

SELECT
    number,
    parity_str(number)
FROM numbers(5)


┌─number─┬─if(modulo(number, 2), 'odd', 'even')─┐
│      0 │ even                                 │
│      1 │ odd                                  │
│      2 │ even                                 │
│      3 │ odd                                  │
│      4 │ even                                 │
└────────┴──────────────────────────────────────┘
 [✎](https://sql.clickhouse.com?query_id=3ZBX6XXPDY7TNOP7QOWHAB)

```

This is deliberately simple. As we’ll demonstrate, these can get considerably more complex.

## The Problem \#

Our `git-import` generates data for several tables from the git commit history of a repository. One of these, `file_changes`, contains a row for every file changed in a commit. A commit that modifies more than one file will therefore generate multiple rows, allowing us to construct the [history of a file](https://clickhouse.com/docs/en/getting-started/example-datasets/github/#history-of-a-single-file) with a simple SELECT statement. For example, below, we look at the recent commits to our ReplicatedMergeTree:

```

SELECT
    time,
    substring(commit_hash, 1, 11) AS commit,
    change_type,
    author,
    lines_added AS added,
    lines_deleted AS deleted
FROM git.file_changes
WHERE path = 'src/Storages/StorageReplicatedMergeTree.cpp'
ORDER BY time DESC
LIMIT 5



┌────────────────time─┬─commit──────┬─change_type─┬─author─────────────┬─added─┬─deleted─┐
│ 2022-10-30 16:30:51 │ c68ab231f91 │ Modify      │ Alexander Tokmakov │    13 │      10 │
│ 2022-10-23 16:24:20 │ b40d9200d20 │ Modify      │ Anton Popov        │    28 │      30 │
│ 2022-10-23 01:23:15 │ 56e5daba0c9 │ Modify      │ Anton Popov        │    28 │      44 │
│ 2022-10-21 13:35:37 │ 851f556d65a │ Modify      │ Igor Nikonov       │     3 │       2 │
│ 2022-10-21 13:02:52 │ 13d31eefbc3 │ Modify      │ Igor Nikonov       │     4 │       4 │
└─────────────────────┴─────────────┴─────────────┴────────────────────┴───────┴─────────┘


5 rows in set. Elapsed: 0.011 sec. Processed 3.91 thousand rows, 704.14 KB (350.59 thousand rows/s., 63.19 MB/s.)


```
