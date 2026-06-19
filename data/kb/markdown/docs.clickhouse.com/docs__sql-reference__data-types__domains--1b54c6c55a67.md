# Domains \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- Domains
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/domains/index.md)# Domains

Domains are special\-purpose types that add extra features on top of existing base types, while leaving the on\-wire and on\-disk format of the underlying data type intact. Currently, ClickHouse does not support user\-defined domains.


You can use domains anywhere corresponding base type can be used, for example:


- Create a column of a domain type
- Read/write values from/to domain column
- Use it as an index if a base type can be used as an index
- Call functions with values of domain column


### Extra Features of Domains[​](#extra-features-of-domains "Direct link to Extra Features of Domains")


- Explicit column type name in `SHOW CREATE TABLE` or `DESCRIBE TABLE`
- Input from human\-friendly format with `INSERT INTO domain_table(domain_column) VALUES(...)`
- Output to human\-friendly format for `SELECT domain_column FROM domain_table`
- Loading data from an external source in the human\-friendly format: `INSERT INTO domain_table FORMAT CSV ...`


### Limitations[​](#limitations "Direct link to Limitations")


- Can't convert index column of base type to domain type via `ALTER TABLE`.
- Can't implicitly convert string values into domain values when inserting data from another column or table.
- Domain adds no constrains on stored values.
[PreviousData types binary encoding specification.](/docs/sql-reference/data-types/data-types-binary-encoding)[NextNested(Name1 Type1, Name2 Type2, ...)](/docs/sql-reference/data-types/nested-data-structures/nested)- [Extra Features of Domains](#extra-features-of-domains)- [Limitations](#limitations)
Was this page helpful?
