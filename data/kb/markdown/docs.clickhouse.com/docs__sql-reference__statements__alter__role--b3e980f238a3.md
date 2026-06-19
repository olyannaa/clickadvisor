# ALTER ROLE \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [ALTER](/docs/sql-reference/statements/alter)- ROLE
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/alter/role.md)# ALTER ROLE

Changes roles.


Syntax:



```
ALTER ROLE [IF EXISTS] name1 [RENAME TO new_name |, name2 [,...]] 
    [ON CLUSTER cluster_name]
    [DROP ALL PROFILES]
    [DROP ALL SETTINGS]
    [DROP PROFILES 'profile_name' [,...] ]
    [DROP SETTINGS variable [,...] ]
    [ADD|MODIFY SETTINGS variable [= value] [MIN [=] min_value] [MAX [=] max_value] [CONST|READONLY|WRITABLE|CHANGEABLE_IN_READONLY] | PROFILE 'profile_name'] [,...]
    [ADD PROFILES 'profile_name' [,...] ]

```
[PreviousQUOTA](/docs/sql-reference/statements/alter/quota)[NextAPPLY PATCHES](/docs/sql-reference/statements/alter/apply-patches)Was this page helpful?
