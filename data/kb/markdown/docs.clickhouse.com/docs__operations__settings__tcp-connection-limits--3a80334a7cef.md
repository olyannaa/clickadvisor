# TCP connection limits \| ClickHouse Docs


- - [Settings](/docs/operations/settings)- TCP connection limits
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/operations/settings/tcp-connection-limits.md)# TCP connection limits

## Overview[​](#overview "Direct link to Overview")


You may have a ClickHouse TCP connection (i.e., one through the [command\-line client](https://clickhouse.com/docs/interfaces/client))
disconnect automatically after some number of queries or duration.
After disconnecting, no automatic reconnection occurs (unless triggered through something else,
such as sending another query in the command\-line client).


Connection limits are enabled by setting the server settings
`tcp_close_connection_after_queries_num` (for the query limit)
or `tcp_close_connection_after_queries_seconds` (for the duration limit) to greater than 0\.
If both limits are enabled, the connection closes when either limit is hit first.


Upon hitting a limit and disconnecting, the client receives a
`TCP_CONNECTION_LIMIT_REACHED` exception, and **the query that causes the disconnect is never processed**.


## Query limits[​](#query-limits "Direct link to Query limits")


Assuming `tcp_close_connection_after_queries_num` is set to N, then the connection allows
N successful queries. Then on query N \+ 1, the client disconnects.


Every query processed counts towards the query limit. So when connecting a command\-line client,
there may be an automatic initial system warnings query which counts towards the limit.


When a TCP connection is idle (i.e., has not processed queries for some duration of time,
specified by the session setting `poll_interval`), the number of queries counted so far resets to 0\.
This means the number of total queries in a single connection can exceed
`tcp_close_connection_after_queries_num` if idle occurs.


## Duration limits[​](#duration-limits "Direct link to Duration limits")


The connection duration is measured starting as soon as the client connects.
The client is disconnected on the first query after `tcp_close_connection_after_queries_seconds` seconds has passed.

[PreviousConfiguration Files](/docs/operations/configuration-files)[NextOverview](/docs/operations/system-tables)- [Overview](#overview)- [Query limits](#query-limits)- [Duration limits](#duration-limits)
Was this page helpful?
