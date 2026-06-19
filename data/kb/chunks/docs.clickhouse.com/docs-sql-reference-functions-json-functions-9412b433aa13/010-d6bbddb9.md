---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/json-functions.md)#
topic: json-functions-clickhouse-docs
ch_version_introduced: '200.0'
last_updated: '2026-06-12'
chunk_index: 10
total_chunks_in_doc: 19
---

provided value(s) in the JSON document. **Syntax** ``` JSONHas(json[ ,indices_or_keys, ...]) ``` **Arguments** - `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string) - `[ ,indices_or_keys, ...]` — A list of zero or more arguments. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int*`](/docs/sql-reference/data-types/int-uint) **Returned value**

Returns `1` if the value exists in `json`, otherwise `0` [`UInt8`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Usage example**

```
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 'b') = 1;
SELECT JSONHas('{"a": "hello", "b": [-100, 200.0, 300]}', 'b', 4) = 0;

```

```
1
0

```

## JSONKey[​](#JSONKey "Direct link to JSONKey")

Introduced in: v20\.1\.0

Returns the key of a JSON object field by its index (1\-based). If the JSON is passed as a string, it is parsed first. The second argument is a JSON path to navigate into nested objects. The function returns the key name at the specified position.

**Syntax**

```
JSONKey(json[, indices_or_keys, ...])

```

**Arguments**

- `json` — JSON string to parse. [`String`](/docs/sql-reference/data-types/string)
- `indices_or_keys` — Optional list of indices or keys specifying a path to a nested element. Each argument can be either a string (access by key) or an integer (access by index starting from 1\). [`String`](/docs/sql-reference/data-types/string) or [`Int*`](/docs/sql-reference/data-types/int-uint)

**Returned value**

Returns the key name at the specified position in the JSON object. [`String`](/docs/sql-reference/data-types/string)

**Examples**

**Usage example**

```
SELECT JSONKey('{"a": "hello", "b": [-100, 200.0, 300]}', 1);

```

```
a

```

## JSONLength[​](#JSONLength "Direct link to JSONLength")

Introduced in: v20\.1\.0

Return the length of a JSON array or a JSON object.
If the value does not exist or has the wrong type, `0` will be returned.

**Syntax**

```
JSONLength(json [, indices_or_keys, ...])

```

**Arguments**

- `json` — JSON string to parse [`String`](/docs/sql-reference/data-types/string)
- `[, indices_or_keys, ...]` — Optional. A list of zero or more arguments. [`String`](/docs/sql-reference/data-types/string) or [`(U)Int8/16/32/64`](/docs/sql-reference/data-types/int-uint)

**Returned value**

Returns the length of the JSON array or JSON object, otherwise returns `0` if the value does not exist or has the wrong type. [`UInt64`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Usage example**

```
SELECT JSONLength('{"a": "hello", "b": [-100, 200.0, 300]}', 'b') = 3;
SELECT JSONLength('{"a": "hello", "b": [-100, 200.0, 300]}') = 2;

```

```
1
1

```

## JSONMergePatch[​](#JSONMergePatch "Direct link to JSONMergePatch")

Introduced in: v23\.10\.0

Returns the merged JSON object string which is formed by merging multiple JSON objects.

**Syntax**

```
JSONMergePatch(json1[, json2, ...])

```

**Aliases**: `jsonMergePatch`

**Arguments**
