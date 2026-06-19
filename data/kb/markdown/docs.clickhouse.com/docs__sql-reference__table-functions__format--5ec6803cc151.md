# format \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Table functions](/docs/sql-reference/table-functions)- format
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/table-functions/format.md)# format

Parses data from arguments according to specified input format. If structure argument is not specified, it's extracted from the data.


## Syntax[​](#syntax "Direct link to Syntax")



```
format(format_name, [structure], data)

```

## Arguments[​](#arguments "Direct link to Arguments")


- `format_name` — The [format](/docs/sql-reference/formats) of the data.
- `structure` \- Structure of the table. Optional. Format 'column1\_name column1\_type, column2\_name column2\_type, ...'.
- `data` — String literal or constant expression that returns a string containing data in specified format


## Returned value[​](#returned_value "Direct link to Returned value")


A table with data parsed from `data` argument according to specified format and specified or extracted structure.


## Examples[​](#examples "Direct link to Examples")


Without `structure` argument:



```
SELECT * FROM format(JSONEachRow,
$$
{"a": "Hello", "b": 111}
{"a": "World", "b": 123}
{"a": "Hello", "b": 112}
{"a": "World", "b": 124}
$$)

```


```
┌───b─┬─a─────┐
│ 111 │ Hello │
│ 123 │ World │
│ 112 │ Hello │
│ 124 │ World │
└─────┴───────┘

```


```
DESC format(JSONEachRow,
$$
{"a": "Hello", "b": 111}
{"a": "World", "b": 123}
{"a": "Hello", "b": 112}
{"a": "World", "b": 124}
$$)

```


```
┌─name─┬─type──────────────┬─default_type─┬─default_expression─┬─comment─┬─codec_expression─┬─ttl_expression─┐
│ b    │ Nullable(Float64) │              │                    │         │                  │                │
│ a    │ Nullable(String)  │              │                    │         │                  │                │
└──────┴───────────────────┴──────────────┴────────────────────┴─────────┴──────────────────┴────────────────┘

```

With `structure` argument:



```
SELECT * FROM format(JSONEachRow, 'a String, b UInt32',
$$
{"a": "Hello", "b": 111}
{"a": "World", "b": 123}
{"a": "Hello", "b": 112}
{"a": "World", "b": 124}
$$)

```


```
┌─a─────┬───b─┐
│ Hello │ 111 │
│ World │ 123 │
│ Hello │ 112 │
│ World │ 124 │
└───────┴─────┘

```

## Related[​](#related "Direct link to Related")


- [Formats](/docs/interfaces/formats)
[Previousfilesystem](/docs/sql-reference/table-functions/filesystem)[Nextgcs](/docs/sql-reference/table-functions/gcs)- [Syntax](#syntax)- [Arguments](#arguments)- [Returned value](#returned_value)- [Examples](#examples)- [Related](#related)
Was this page helpful?
