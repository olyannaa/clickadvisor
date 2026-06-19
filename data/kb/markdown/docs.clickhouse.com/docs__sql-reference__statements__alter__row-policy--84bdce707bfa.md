# ALTER ROW POLICY \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- ROW POLICY
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/row-policy.md)# ALTER ROW POLICY

Changes row policy.


Syntax:



```
ALTER [ROW] POLICY [IF EXISTS] name1 [ON CLUSTER cluster_name1] ON [database1.]table1 [RENAME TO new_name1]
        [, name2 [ON CLUSTER cluster_name2] ON [database2.]table2 [RENAME TO new_name2] ...]
    [AS {PERMISSIVE | RESTRICTIVE}]
    [FOR SELECT]
    [USING {condition | NONE}][,...]
    [TO {role [,...] | ALL | ALL EXCEPT role [,...]}]

```
[PreviousAPPLY PATCHES](/docs/sql-reference/statements/alter/apply-patches)[NextMASKING POLICY](/docs/sql-reference/statements/alter/masking-policy)Was this page helpful?
