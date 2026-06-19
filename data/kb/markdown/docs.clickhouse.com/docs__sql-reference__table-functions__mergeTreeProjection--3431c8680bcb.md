# mergeTreeProjection \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- mergeTreeProjection
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/mergeTreeProjection.md)# mergeTreeProjection

Represents the contents of some projection in MergeTree tables. It can be used for introspection.


## Syntax[​](#syntax "Direct link to Syntax")



```
mergeTreeProjection(database, table, projection)

```

## Arguments[​](#arguments "Direct link to Arguments")




| Argument Description| `database` The database name to read projection from.| `table` The table name to read projection from.| `projection` The projection to read from. | | | | | | | --- | --- | --- | --- | --- | --- | | |
| --- | --- | --- | --- | --- | --- | --- | --- |


## Returned value[​](#returned_value "Direct link to Returned value")


A table object with columns provided by given projection.


## Usage Example[​](#usage-example "Direct link to Usage Example")



```
CREATE TABLE test
(
    `user_id` UInt64,
    `item_id` UInt64,
    PROJECTION order_by_item_id
    (
        SELECT _part_offset
        ORDER BY item_id
    )
)
ENGINE = MergeTree
ORDER BY user_id;

INSERT INTO test SELECT number, 100 - number FROM numbers(5);

```


```
SELECT *, _part_offset FROM mergeTreeProjection(currentDatabase(), test, order_by_item_id);

```


```
   ┌─item_id─┬─_parent_part_offset─┬─_part_offset─┐
1. │      96 │                   4 │            0 │
2. │      97 │                   3 │            1 │
3. │      98 │                   2 │            2 │
4. │      99 │                   1 │            3 │
5. │     100 │                   0 │            4 │
   └─────────┴─────────────────────┴──────────────┘

```


```
DESCRIBE mergeTreeProjection(currentDatabase(), test, order_by_item_id) SETTINGS describe_compact_output = 1;

```


```
   ┌─name────────────────┬─type───┐
1. │ item_id             │ UInt64 │
2. │ _parent_part_offset │ UInt64 │
   └─────────────────────┴────────┘

```
[PreviousmergeTreeIndex](/docs/sql-reference/table-functions/mergeTreeIndex)[NextmergeTreeTextIndex](/docs/sql-reference/table-functions/mergeTreeTextIndex)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Usage Example](#usage-example)
Was this page helpful?
