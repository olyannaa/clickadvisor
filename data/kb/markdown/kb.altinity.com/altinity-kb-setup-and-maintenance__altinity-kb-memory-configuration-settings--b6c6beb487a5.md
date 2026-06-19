# memory configuration settings \| Altinity® Knowledge Base for ClickHouse®


1. [Setup \& maintenance](/altinity-kb-setup-and-maintenance/)
2. memory configuration settings
# memory configuration settings

## max\_memory\_usage. Single query memory usage

max\_memory\_usage \- the maximum amount of memory allowed for **a single query** to take. By default, it’s 10Gb. The default value is good, don’t adjust it in advance.

There are scenarios when you need to relax the limit for particular queries (if you hit ‘Memory limit (for query) exceeded’), or use a lower limit if you need to discipline the users or increase the number of simultaneous queries.

## Server memory usage

Server memory usage \= constant memory footprint (used by different caches, dictionaries, etc) \+ sum of memory temporary used by running queries (a theoretical limit is a number of simultaneous queries multiplied by max\_memory\_usage).

Since 20\.4 you can set up a global limit using the `max_server_memory_usage` setting. If **something** will hit that limit you will see ‘Memory limit (total) exceeded’ in **random places**.

By default it 90% of the physical RAM of the server.
[https://clickhouse.tech/docs/en/operations/server\-configuration\-parameters/settings/\#max\_server\_memory\_usage](https://clickhouse.tech/docs/en/operations/server-configuration-parameters/settings/#max_server_memory_usage)
[https://github.com/ClickHouse/ClickHouse/blob/e5b96bd93b53d2c1130a249769be1049141ef386/programs/server/config.xml\#L239\-L250](https://github.com/ClickHouse/ClickHouse/blob/e5b96bd93b53d2c1130a249769be1049141ef386/programs/server/config.xml#L239-L250)

You can decrease that in some scenarios (like you need to leave more free RAM for page cache or to some other software).

### Limits?


```
select metric, formatReadableSize(value) from system.asynchronous_metrics where metric ilike '%MemoryTotal%'
union all 
select name, formatReadableSize(toUInt64(value)) from system.server_settings where name='max_server_memory_usage'
FORMAT PrettyCompactMonoBlock

```
### How to check what is using my RAM?

[altinity\-kb\-who\-ate\-my\-memory.md](http://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-who-ate-my-memory/)

### Mark cache

[https://github.com/ClickHouse/clickhouse\-presentations/blob/master/meetup39/mark\-cache.pdf](https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup39/mark-cache.pdf)

Last modified 2025\.12\.29: [Update altinity\-kb\-memory\-configuration\-settings.md (46c82a0\)](https://github.com/Altinity/altinityknowledgebase/commit/46c82a0831c1aec0ddf1abfc1c05c68449adb23e)
