# ALTER MASKING POLICY \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- MASKING POLICY
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/masking-policy.md)ClickHouse Cloud only
# ALTER MASKING POLICY


Modifies an existing masking policy.


Syntax:



```
ALTER MASKING POLICY [IF EXISTS] policy_name ON [database.]table
    [UPDATE column1 = expression1 [, column2 = expression2 ...]]
    [WHERE condition]
    [TO {role1 [, role2 ...] | ALL | ALL EXCEPT role1 [, role2 ...]}]
    [PRIORITY priority_number]

```

All clauses are optional. Only the specified clauses will be updated.

[PreviousROW POLICY](/docs/sql-reference/statements/alter/row-policy)[NextSETTINGS PROFILE](/docs/sql-reference/statements/alter/settings-profile)Was this page helpful?
