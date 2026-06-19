# CREATE MASKING POLICY \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Statements](/docs/sql-reference/statements)- [CREATE](/docs/sql-reference/statements/create)- MASKING POLICY
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/statements/create/masking-policy.md)# CREATE MASKING POLICY

ClickHouse Cloud only
Creates a masking policy, which allows dynamically transforming or masking column values for specific users or roles when they query a table.


TipMasking policies provide column\-level data security by transforming sensitive data at query time without modifying the stored data.


Syntax:



```
CREATE MASKING POLICY [IF NOT EXISTS | OR REPLACE] policy_name ON [database.]table
    UPDATE column1 = expression1 [, column2 = expression2 ...]
    [WHERE condition]
    TO {role1 [, role2 ...] | ALL | ALL EXCEPT role1 [, role2 ...]}
    [PRIORITY priority_number]

```

## UPDATE Clause[​](#update-clause "Direct link to UPDATE Clause")


The `UPDATE` clause specifies which columns to mask and how to transform them. You can mask multiple columns in a single policy.


Examples:


- Simple masking: `UPDATE email = '***masked***'`
- Partial masking: `UPDATE email = concat(substring(email, 1, 3), '***@***.***')`
- Hash\-based masking: `UPDATE email = concat('masked_', substring(hex(cityHash64(email)), 1, 8))`
- Multiple columns: `UPDATE email = '***@***.***', phone = '***-***-****'`


## WHERE Clause[​](#where-clause "Direct link to WHERE Clause")


The optional `WHERE` clause allows conditional masking based on row values. Only rows matching the condition will have the masking applied.


Example:



```
CREATE MASKING POLICY mask_high_salaries ON employees
UPDATE salary = 0
WHERE salary > 100000
TO analyst;

```

## TO Clause[​](#to-clause "Direct link to TO Clause")


In the `TO` section, specify which users and roles the policy should apply to.


- `TO user1, user2`: Apply to specific users/roles
- `TO ALL`: Apply to all users
- `TO ALL EXCEPT user1, user2`: Apply to all users except specified ones


NoteUnlike row policies, masking policies do not affect users who don't have the policy applied. If no masking policy applies to a user, they see the original data.


## PRIORITY Clause[​](#priority-clause "Direct link to PRIORITY Clause")


When multiple masking policies target the same column for a user, the `PRIORITY` clause determines the application order. Policies are applied in order from highest to lowest priority.


Default priority is 0\. Policies with the same priority are applied in an undefined order.


Example:



```
-- Applied second (lower priority)
CREATE MASKING POLICY mask1 ON users
UPDATE email = '[[email protected]](/cdn-cgi/l/email-protection)'
TO analyst
PRIORITY 1;

-- Applied first (higher priority)
CREATE MASKING POLICY mask2 ON users
UPDATE email = '[[email protected]](/cdn-cgi/l/email-protection)'
TO analyst
PRIORITY 10;

-- analyst sees '[[email protected]](/cdn-cgi/l/email-protection)' because it's applied last

```

Performance Considerations- Masking policies may impact query performance depending on expression complexity
- Some optimizations may be disabled for tables with active masking policies
[PreviousROW POLICY](/docs/sql-reference/statements/create/row-policy)[NextQUOTA](/docs/sql-reference/statements/create/quota)- [UPDATE Clause](#update-clause)- [WHERE Clause](#where-clause)- [TO Clause](#to-clause)- [PRIORITY Clause](#priority-clause)
Was this page helpful?
