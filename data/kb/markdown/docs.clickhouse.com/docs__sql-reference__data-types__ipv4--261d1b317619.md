# IPv4 \| ClickHouse Docs


- - [Introduction](/docs/sql-reference)- [Data types](/docs/sql-reference/data-types)- IPv4
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/data-types/ipv4.md)# IPv4

## IPv4[​](#ipv4 "Direct link to IPv4")


IPv4 addresses. Stored in 4 bytes as UInt32\.


### Basic Usage[​](#basic-usage "Direct link to Basic Usage")



```
CREATE TABLE hits (url String, from IPv4) ENGINE = MergeTree() ORDER BY url;

DESCRIBE TABLE hits;

```


```
┌─name─┬─type───┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┐
│ url  │ String │              │                    │         │                  │
│ from │ IPv4   │              │                    │         │                  │
└──────┴────────┴──────────────┴────────────────────┴─────────┴──────────────────┘

```

OR you can use IPv4 domain as a key:



```
CREATE TABLE hits (url String, from IPv4) ENGINE = MergeTree() ORDER BY from;

```

`IPv4` domain supports custom input format as IPv4\-strings:



```
INSERT INTO hits (url, from) VALUES ('https://wikipedia.org', '116.253.40.133')('https://clickhouse.com', '183.247.232.58')('https://clickhouse.com/docs/en/', '116.106.34.242');

SELECT * FROM hits;

```


```
┌─url────────────────────────────────┬───────────from─┐
│ https://clickhouse.com/docs/en/ │ 116.106.34.242 │
│ https://wikipedia.org              │ 116.253.40.133 │
│ https://clickhouse.com          │ 183.247.232.58 │
└────────────────────────────────────┴────────────────┘

```

Values are stored in compact binary form:



```
SELECT toTypeName(from), hex(from) FROM hits LIMIT 1;

```


```
┌─toTypeName(from)─┬─hex(from)─┐
│ IPv4             │ B7F7E83A  │
└──────────────────┴───────────┘

```

IPv4 addresses can be directly compared to IPv6 addresses:



```
SELECT toIPv4('127.0.0.1') = toIPv6('::ffff:127.0.0.1');

```


```
┌─equals(toIPv4('127.0.0.1'), toIPv6('::ffff:127.0.0.1'))─┐
│                                                       1 │
└─────────────────────────────────────────────────────────┘

```

**See Also**


- [Functions for Working with IPv4 and IPv6 Addresses](/docs/sql-reference/functions/ip-address-functions)
[PreviousUUID](/docs/sql-reference/data-types/uuid)[NextIPv6](/docs/sql-reference/data-types/ipv6)- [IPv4](#ipv4)
	- [Basic Usage](#basic-usage)
Was this page helpful?
