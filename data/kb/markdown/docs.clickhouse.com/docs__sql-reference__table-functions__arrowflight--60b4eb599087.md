# arrowFlight \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- arrowFlight
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/arrowflight.md)# arrowFlight

Allows to perform queries on data exposed via an [Apache Arrow Flight](/docs/interfaces/arrowflight) server.


**Syntax**



```
arrowFlight('host:port', 'dataset_name' [, 'username', 'password'])

```

**Arguments**


- `host:port` — Address of the Arrow Flight server. [String](/docs/sql-reference/data-types/string).
- `dataset_name` — Name of the dataset or descriptor available on the Arrow Flight server. [String](/docs/sql-reference/data-types/string).
- `username` \- Username to use with basic HTTP style authentication.
- `password` \- Password to use with basic HTTP style authentication.
If `username` and `password` are not specified, it means that authentication is not used
(that will work only if the Arrow Flight server allows it).


**Returned value**


- A table object representing the remote dataset. The schema is inferred from the Arrow Flight response.


**Example**



```
SELECT * FROM arrowFlight('127.0.0.1:9005', 'sample_dataset') ORDER BY id;

```


```
┌─id─┬─name────┬─value─┐
│  1 │ foo     │ 42.1  │
│  2 │ bar     │ 13.3  │
│  3 │ baz     │ 77.0  │
└────┴─────────┴───────┘

```

**See Also**


- [Arrow Flight](/docs/engines/table-engines/integrations/arrowflight) table engine
- [Apache Arrow Flight SQL](https://arrow.apache.org/docs/format/FlightSql.html)
[Previoussqlite](/docs/sql-reference/table-functions/sqlite)[Nexturl](/docs/sql-reference/table-functions/url)Was this page helpful?
