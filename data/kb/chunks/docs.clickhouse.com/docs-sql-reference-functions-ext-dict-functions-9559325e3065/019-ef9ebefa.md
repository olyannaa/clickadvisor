---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/ext-dict-functions.md)#
topic: functions-for-working-with-dictionaries-clickhouse-docs
ch_version_introduced: '123.45'
last_updated: '2026-06-12'
chunk_index: 19
total_chunks_in_doc: 24
---

corresponds to `id_expr`, otherwise returns the value passed as the `default_value_expr` parameter. NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type. **Examples** **Usage example**

```
-- for key which exists
SELECT dictGetUInt16('all_types_dict', 'UInt16_value', 1);

-- for key which does not exist, returns the provided default value (0)
SELECT dictGetUInt16OrDefault('all_types_dict', 'UInt16_value', 999, 0);

```

```
┌─dictGetUInt1⋯_value', 1)─┐
│                     5000 │
└──────────────────────────┘
┌─dictGetUInt1⋯e', 999, 0)─┐
│                        0 │
└──────────────────────────┘

```

## dictGetUInt32[​](#dictGetUInt32 "Direct link to dictGetUInt32")

Introduced in: v1\.1\.0

Converts a dictionary attribute value to `UInt32` data type regardless of the dictionary configuration.

**Syntax**

```
dictGetUInt32(dict_name, attr_name, id_expr)

```

**Arguments**

- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. An expression returning a dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)

**Returned value**

Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the content of the `<null_value>` element specified for the attribute in the dictionary configuration.

NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.

**Examples**

**Usage example**

```
SELECT dictGetUInt32('all_types_dict', 'UInt32_value', 1)

```

```
┌─dictGetUInt3⋯_value', 1)─┐
│                  1000000 │
└──────────────────────────┘

```

## dictGetUInt32OrDefault[​](#dictGetUInt32OrDefault "Direct link to dictGetUInt32OrDefault")

Introduced in: v1\.1\.0

Converts a dictionary attribute value to `UInt32` data type regardless of the dictionary configuration, or returns the provided default value if the key is not found.

**Syntax**

```
dictGetUInt32OrDefault(dict_name, attr_name, id_expr, default_value_expr)

```

**Arguments**

- `dict_name` — Name of the dictionary. [`String`](/docs/sql-reference/data-types/string)
- `attr_name` — Name of the column of the dictionary. [`String`](/docs/sql-reference/data-types/string) or [`Tuple(String)`](/docs/sql-reference/data-types/tuple)
- `id_expr` — Key value. Expression returning dictionary key\-type value or tuple value (dictionary configuration dependent). [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)
- `default_value_expr` — Value(s) returned if the dictionary does not contain a row with the `id_expr` key. [`Expression`](/docs/sql-reference/data-types/special-data-types/expression) or [`Tuple(T)`](/docs/sql-reference/data-types/tuple)

**Returned value**

Returns the value of the dictionary attribute that corresponds to `id_expr`,
otherwise returns the value passed as the `default_value_expr` parameter.

NoteClickHouse throws an exception if it cannot parse the value of the attribute or the value does not match the attribute data type.

**Examples**

**Usage example**
