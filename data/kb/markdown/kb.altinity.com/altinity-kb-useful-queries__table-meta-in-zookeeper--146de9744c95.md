# Check table metadata in zookeeper \| Altinity® Knowledge Base for ClickHouse®


1. [Useful queries](/altinity-kb-useful-queries/)
2. Check table metadata in zookeeper
# Check table metadata in zookeeper

Check table metadata in zookeeper.## Compare table metadata of different replicas in zookeeper


> Check if a table is consistent across all zookeeper replicas. From each replica, returns metdadata, columns, and is\_active nodes. Checks whether each replica’s value matches the previous replica’s value, and flags any mismatches (looks\_good \= 0\).


```
SELECT
    *,
    if(
        prev_name = name AND name != 'is_active',
        prev_value = value,
        1
    ) AS looks_good
FROM (
    SELECT
        name,
        path,
        ctime,
        mtime,
        value,
        lagInFrame(name)  OVER w AS prev_name,
        lagInFrame(value) OVER w AS prev_value
    FROM system.zookeeper
    WHERE (path IN (
        SELECT arrayJoin(groupUniqArray(if(path LIKE '%/replicas', concat(path, '/', name), path)))
        FROM system.zookeeper
        WHERE path IN (
            SELECT arrayJoin([zookeeper_path, concat(zookeeper_path, '/replicas')])
            FROM system.replicas
            WHERE table = 'test_repl'
        )
    )) AND (name IN ('metadata', 'columns', 'is_active'))
    WINDOW w AS (ORDER BY name = 'is_active', name ASC, path ASC
                 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
)

```

> Returns a table’s create\_table\_query, and the last time the table’s metadata was modified


```
SELECT metadata_modification_time, create_table_query
FROM system.tables
WHERE name = 'test_repl'

```
Last modified 2026\.02\.25: [Added explanations for multiple Useful Queries pages, fixed some non\-functional queries (7840c77\)](https://github.com/Altinity/altinityknowledgebase/commit/7840c77f02f0318484e2f093bffb58849f8ed250)
