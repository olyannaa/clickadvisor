# timeSeriesMetrics \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- timeSeriesMetrics
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/timeSeriesMetrics.md)# timeSeriesMetrics

`timeSeriesMetrics(db_name.time_series_table)` \- Returns the [metrics](/docs/engines/table-engines/special/time_series#metrics-table) table
used by table `db_name.time_series_table` whose table engine is the [TimeSeries](/docs/engines/table-engines/special/time_series) engine:



```
CREATE TABLE db_name.time_series_table ENGINE=TimeSeries METRICS metrics_table

```

The function also works if the *metrics* table is inner:



```
CREATE TABLE db_name.time_series_table ENGINE=TimeSeries METRICS INNER UUID '01234567-89ab-cdef-0123-456789abcdef'

```

The following queries are equivalent:



```
SELECT * FROM timeSeriesMetrics(db_name.time_series_table);
SELECT * FROM timeSeriesMetrics('db_name.time_series_table');
SELECT * FROM timeSeriesMetrics('db_name', 'time_series_table');

```
[PrevioustimeSeriesData](/docs/sql-reference/table-functions/timeSeriesData)[NexttimeSeriesSelector](/docs/sql-reference/table-functions/timeSeriesSelector)Was this page helpful?
