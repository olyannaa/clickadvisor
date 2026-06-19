# CollapsingMergeTree vs ReplacingMergeTree \| Altinity® Knowledge Base for ClickHouse®


1. [Engines](/engines/)
2. [MergeTree table engine family](/engines/mergetree-table-engine-family/)
3. CollapsingMergeTree vs ReplacingMergeTree
# CollapsingMergeTree vs ReplacingMergeTree

## CollapsingMergeTree vs ReplacingMergeTree



| ReplacingMergeTree | CollapsingMergeTree |
| --- | --- |
| \+ very easy to use (always replace) | \- more complex (accounting\-alike, put ‘rollback’ records to fix something) |
| \+ you don’t need to store the previous state of the row | \- you need to the store (somewhere) the previous state of the row, OR extract it from the table itself (point queries is not nice for ClickHouse®) |
| \- no deletes | \+ support deletes |
| \- w/o FINAL \- you can can always see duplicates, you need always to ‘pay’ FINAL performance penalty | \+ properly crafted query can give correct results without final (i.e. `sum(amount * sign)` will be correct, no matter of you have duplicated or not) |
| \- only `uniq()`\-alike things can be calculated in materialized views | \+ you can do basic counts \& sums in materialized views |

Last modified 2025\.01\.16: [Streamlined page metadata, simplified directory structure (afe0f3c)](https://github.com/Altinity/altinityknowledgebase/commit/afe0f3c3e76e848e6941903e93f05dd41fccfea0)
