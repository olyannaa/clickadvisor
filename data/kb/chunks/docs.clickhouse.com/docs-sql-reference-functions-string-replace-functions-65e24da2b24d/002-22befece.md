---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/string-replace-functions.md)#
topic: functions-for-string-replacement-clickhouse-docs
ch_version_introduced: auto
last_updated: '2026-06-12'
chunk_index: 2
total_chunks_in_doc: 5
---

``` SELECT overlay('My father is from Mexico.', 'mother', 4) AS res; ``` ``` ┌─res──────────────────────┐ │ My mother is from Mexico.│ └──────────────────────────┘ ``` **Replacement with length** ``` SELECT overlay('My father is from Mexico.', 'dad', 4, 6) AS res; ```

```
┌─res───────────────────┐
│ My dad is from Mexico.│
└───────────────────────┘

```

## overlayUTF8[​](#overlayUTF8 "Direct link to overlayUTF8")

Introduced in: v24\.9\.0

Replace part of the string `s` with another string `replace`, starting at the 1\-based index `offset`.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.

**Syntax**

```
overlayUTF8(s, replace, offset[, length])

```

**Arguments**

- `s` — The input string. [`String`](/docs/sql-reference/data-types/string)
- `replace` — The replacement string. [`const String`](/docs/sql-reference/data-types/string)
- `offset` — An integer type `Int` (1\-based). If `offset` is negative, it is counted from the end of the input string `s`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `length` — Optional. Specifies the length of the snippet within the input string `s` to be replaced. If `length` is not specified, the number of characters removed from `s` equals the length of `replace`, otherwise `length` characters are removed. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)

**Returned value**

Returns a string with replacement. [`String`](/docs/sql-reference/data-types/string)

**Examples**

**UTF\-8 replacement**

```
SELECT overlayUTF8('Mein Vater ist aus Österreich.', 'der Türkei', 20) AS res;

```

```
┌─res───────────────────────────┐
│ Mein Vater ist aus der Türkei.│
└───────────────────────────────┘

```

## printf[​](#printf "Direct link to printf")

Introduced in: v24\.8\.0

The `printf` function formats the given string with the values (strings, integers, floating\-points etc.) listed in the arguments, similar to printf function in C\+\+.
The format string can contain format specifiers starting with `%` character.
Anything not contained in `%` and the following format specifier is considered literal text and copied verbatim into the output.
Literal `%` character can be escaped by `%%`.
The format string can be either a constant or a column expression, allowing different format patterns per row.

**Syntax**

```
printf(format[, sub1, sub2, ...])

```

**Arguments**

- `format` — The format string with `%` specifiers. [`String`](/docs/sql-reference/data-types/string)
- `sub1, sub2, ...` — Optional. Zero or more values to substitute into the format string. [`Any`](/docs/sql-reference/data-types)

**Returned value**

Returns a formatted string. [`String`](/docs/sql-reference/data-types/string)

**Examples**

**C\+\+\-style formatting**

```
SELECT printf('%%%s %s %d', 'Hello', 'World', 2024);

```

```
┌─printf('%%%s %s %d', 'Hello', 'World', 2024)─┐
│ %Hello World 2024                            │
└──────────────────────────────────────────────┘

```

## regexpQuoteMeta[​](#regexpQuoteMeta "Direct link to regexpQuoteMeta")
