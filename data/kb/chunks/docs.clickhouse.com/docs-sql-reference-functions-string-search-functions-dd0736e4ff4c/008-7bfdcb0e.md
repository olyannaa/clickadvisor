---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/string-search-functions.md)#
topic: functions-for-searching-in-strings-clickhouse-docs
ch_version_introduced: '192.0'
last_updated: '2026-06-12'
chunk_index: 8
total_chunks_in_doc: 26
---

INDEX idx_attributes_vals mapValues(attributes) TYPE text(tokenizer = array) ) ENGINE = MergeTree ORDER BY id; INSERT INTO log VALUES (1, ['clickhouse', 'clickhouse cloud'], {'address': '192.0.0.1', 'log_level': 'INFO'}), (2, ['chdb'], {'embedded': 'true', 'log_level': 'DEBUG'}); ``` **Example with an array column**

```
SELECT count() FROM log WHERE hasAnyTokens(tags, 'clickhouse');

```

```
┌─count()─┐
│       1 │
└─────────┘

```

**Example with mapKeys**

```
SELECT count() FROM log WHERE hasAnyTokens(mapKeys(attributes), ['address', 'log_level']);

```

```
┌─count()─┐
│       2 │
└─────────┘

```

**Example with mapValues**

```
SELECT count() FROM log WHERE hasAnyTokens(mapValues(attributes), ['192.0.0.1', 'DEBUG']);

```

```
┌─count()─┐
│       2 │
└─────────┘

```

## hasPhrase[​](#hasPhrase "Direct link to hasPhrase")

Introduced in: v26\.4\.0

Checks if the `input` contains all tokens from the `phrase` in consecutive order.

NoteColumn `input` should have a [text index](/docs/engines/table-engines/mergetree-family/textindexes) defined for optimal performance.
If no text index is defined, the function performs a brute\-force column scan which is orders of magnitude slower than an index lookup.

Prior to searching, the function tokenizes both the `input` and the `phrase` arguments using the tokenizer specified for the text index.
If the column has no text index defined, the `splitByNonAlpha` tokenizer is used instead — unless a tokenizer is provided as the optional third argument.
The tokenizer argument must be one of `splitByNonAlpha`, `splitByString`, `ngrams`, or `asciiCJK`.

NoteWhen a text index defines a [preprocessor](/docs/engines/table-engines/mergetree-family/textindexes#creating-a-text-index) (for example `lowerUTF8`), `hasPhrase` applies it to both `input` and `phrase` before tokenization.
The preprocessor is only applied on the text index path, so results may differ between queries that use the text index and queries that do not (e.g. `SETTINGS use_skip_indexes = 0`).
This inconsistency is tolerated to improve the usability of full\-text search.

Unlike [`hasToken`](#hasToken), [`hasAnyTokens`](#hasAnyTokens) and [`hasAllTokens`](#hasAllTokens), `hasPhrase` requires the tokens to appear in the same order
and without any intervening tokens. For example, `hasPhrase('the quick brown fox', 'quick fox')` returns 0
because "brown" appears between "quick" and "fox".

**Syntax**

```
hasPhrase(input, phrase[, tokenizer])

```

**Aliases**: `matchPhrase`

**Arguments**

- `input` — The input column. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `phrase` — Phrase to search for. [`const String`](/docs/sql-reference/data-types/string)
- `tokenizer` — The tokenizer to use. Optional, defaults to `splitByNonAlpha`. [`const String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns `1` if the phrase is found as a consecutive token sequence, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)

**Examples**

**Phrase match**

```
SELECT hasPhrase('the quick brown fox jumps', 'quick brown')

```
