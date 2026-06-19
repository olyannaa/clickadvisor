---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/string-search-functions.md)#
topic: functions-for-searching-in-strings-clickhouse-docs
ch_version_introduced: '192.0'
last_updated: '2026-06-12'
chunk_index: 14
total_chunks_in_doc: 26
---

[pattern1, pattern2, ..., patternN]) ``` **Arguments** - `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) - `distance` — The maximum edit distance for fuzzy matching. [`UInt8`](/docs/sql-reference/data-types/int-uint) - `pattern` — Array of patterns to match against. [`Array(String)`](/docs/sql-reference/data-types/array)

**Returned value**

Returns an array of all indices (starting from 1\) that match the haystack within the specified edit distance in any order. Returns an empty array if no matches are found. [`Array(UInt64)`](/docs/sql-reference/data-types/array)

**Examples**

**Usage example**

```
SELECT multiFuzzyMatchAllIndices('ClickHouse', 2, ['ClickHouse', 'ClckHouse', 'ClickHose', 'House']);

```

```
┌─multiFuzzyMa⋯, 'House'])─┐
│ [3,1,4,2]                │
└──────────────────────────┘

```

## multiFuzzyMatchAny[​](#multiFuzzyMatchAny "Direct link to multiFuzzyMatchAny")

Introduced in: v20\.1\.0

Like [`multiMatchAny`](#multiMatchAny) but returns 1 if any pattern matches the haystack within a constant [edit distance](https://en.wikipedia.org/wiki/Edit_distance).
This function relies on the experimental feature of [hyperscan](https://intel.github.io/hyperscan/dev-reference/compilation.html#approximate-matching) library, and can be slow for some edge cases.
The performance depends on the edit distance value and patterns used, but it's always more expensive compared to non\-fuzzy variants.

Note`multiFuzzyMatch*()` function family do not support UTF\-8 regular expressions (it treats them as a sequence of bytes) due to restrictions of hyperscan.

**Syntax**

```
multiFuzzyMatchAny(haystack, distance, [pattern1, pattern2, ..., patternN])

```

**Arguments**

- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `distance` — The maximum edit distance for fuzzy matching. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `pattern` — Optional. An array of patterns to match against. [`Array(String)`](/docs/sql-reference/data-types/array)

**Returned value**

Returns `1` if any pattern matches the haystack within the specified edit distance, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Usage example**

```
SELECT multiFuzzyMatchAny('ClickHouse', 2, ['ClickHouse', 'ClckHouse', 'ClickHose']);

```

```
┌─multiFuzzyMa⋯lickHose'])─┐
│                        1 │
└──────────────────────────┘

```

## multiFuzzyMatchAnyIndex[​](#multiFuzzyMatchAnyIndex "Direct link to multiFuzzyMatchAnyIndex")

Introduced in: v20\.1\.0

Like [`multiFuzzyMatchAny`](#multiFuzzyMatchAny) but returns any index that matches the haystack within a constant [edit distance](https://en.wikipedia.org/wiki/Edit_distance).

**Syntax**

```
multiFuzzyMatchAnyIndex(haystack, distance, [pattern1, pattern2, ..., patternn])

```

**Arguments**

- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `distance` — The maximum edit distance for fuzzy matching. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `pattern` — Array of patterns to match against. [`Array(String)`](/docs/sql-reference/data-types/array)

**Returned value**

Returns the index (starting from 1\) of any pattern that matches the haystack within the specified edit distance, otherwise `0`. [`UInt64`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Usage example**

```
SELECT multiFuzzyMatchAnyIndex('ClickHouse', 2, ['ClckHouse', 'ClickHose', 'ClickHouse']);

```

```
┌─multiFuzzyMa⋯ickHouse'])─┐
│                        2 │
└──────────────────────────┘

```

## multiMatchAllIndices[​](#multiMatchAllIndices "Direct link to multiMatchAllIndices")

Introduced in: v20\.1\.0
