# Functions for Searching in Strings \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- String search
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/string-search-functions.md)# Functions for Searching in Strings

All functions in this section search case\-sensitively by default. Case\-insensitive search is usually provided by separate function variants.


NoteCase\-insensitive search follows the lowercase\-uppercase rules of the English language. E.g. Uppercased `i` in the English language is
`I` whereas in the Turkish language it is `İ` \- results for languages other than English may be unexpected.


Functions in this section also assume that the searched string (referred to in this section as `haystack`) and the search string (referred to in this section as `needle`) are single\-byte encoded text. If this assumption is
violated, no exception is thrown and results are undefined. Search with UTF\-8 encoded strings is usually provided by separate function
variants. Likewise, if a UTF\-8 function variant is used and the input strings are not UTF\-8 encoded text, no exception is thrown and the
results are undefined. Note that no automatic Unicode normalization is performed, however you can use the
[normalizeUTF8\*()](/docs/sql-reference/functions/string-functions#normalizeUTF8NFC) functions for that.


[General strings functions](/docs/sql-reference/functions/string-functions) and [functions for replacing in strings](/docs/sql-reference/functions/string-replace-functions) are described separately.


NoteThe documentation below is generated from the `system.functions` system table.


## countMatches[​](#countMatches "Direct link to countMatches")


Introduced in: v21\.1\.0


Returns number of matches of a regular expression in a string.


Version dependent behaviorThe behavior of this function depends on the ClickHouse version:- in versions \< v25\.6, the function stops counting at the first empty match even if a pattern accepts.
- in versions \>\= 25\.6, the function continues execution when an empty match occurs. The legacy behavior can be restored using setting `count_matches_stop_at_empty_match = true`;



**Syntax**



```
countMatches(haystack, pattern)

```

**Arguments**


- `haystack` — The string to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expression pattern. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number of matches found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Count digit sequences**



```
SELECT countMatches('hello 123 world 456 test', '[0-9]+')

```


```
┌─countMatches('hello 123 world 456 test', '[0-9]+')─┐
│                                                   2 │
└─────────────────────────────────────────────────────┘

```

## countMatchesCaseInsensitive[​](#countMatchesCaseInsensitive "Direct link to countMatchesCaseInsensitive")


Introduced in: v21\.1\.0


Like [`countMatches`](#countMatches) but performs case\-insensitive matching.


**Syntax**



```
countMatchesCaseInsensitive(haystack, pattern)

```

**Arguments**


- `haystack` — The string to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expression pattern. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number of matches found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case insensitive count**



```
SELECT countMatchesCaseInsensitive('Hello HELLO world', 'hello')

```


```
┌─countMatchesCaseInsensitive('Hello HELLO world', 'hello')─┐
│                                                         2 │
└───────────────────────────────────────────────────────────┘

```

## countSubstrings[​](#countSubstrings "Direct link to countSubstrings")


Introduced in: v21\.1\.0


Returns how often a substring `needle` occurs in a string `haystack`.


**Syntax**



```
countSubstrings(haystack, needle[, start_pos])

```

**Arguments**


- `haystack` — String in which the search is performed. [String](/docs/sql-reference/data-types/string) or [Enum](/docs/sql-reference/data-types/enum). \- `needle` — Substring to be searched. [String](/docs/sql-reference/data-types/string). \- `start_pos` — Position (1\-based) in `haystack` at which the search starts. [UInt](/docs/sql-reference/data-types/int-uint). Optional.


**Returned value**


The number of occurrences. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT countSubstrings('aaaa', 'aa');

```


```
┌─countSubstrings('aaaa', 'aa')─┐
│                             2 │
└───────────────────────────────┘

```

**With start\_pos argument**



```
SELECT countSubstrings('abc___abc', 'abc', 4);

```


```
┌─countSubstrings('abc___abc', 'abc', 4)─┐
│                                      1 │
└────────────────────────────────────────┘

```

## countSubstringsCaseInsensitive[​](#countSubstringsCaseInsensitive "Direct link to countSubstringsCaseInsensitive")


Introduced in: v21\.1\.0


Like [`countSubstrings`](#countSubstrings) but counts case\-insensitively.


**Syntax**



```
countSubstringsCaseInsensitive(haystack, needle[, start_pos])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `start_pos` — Optional. Position (1\-based) in `haystack` at which the search starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the number of occurrences of the neddle in the haystack. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT countSubstringsCaseInsensitive('AAAA', 'aa');

```


```
┌─countSubstri⋯AAA', 'aa')─┐
│                        2 │
└──────────────────────────┘

```

**With start\_pos argument**



```
SELECT countSubstringsCaseInsensitive('abc___ABC___abc', 'abc', 4);

```


```
┌─countSubstri⋯, 'abc', 4)─┐
│                        2 │
└──────────────────────────┘

```

## countSubstringsCaseInsensitiveUTF8[​](#countSubstringsCaseInsensitiveUTF8 "Direct link to countSubstringsCaseInsensitiveUTF8")


Introduced in: v21\.1\.0


Like [`countSubstrings`](#countSubstrings) but counts case\-insensitively and assumes that haystack is a UTF\-8 string.


**Syntax**



```
countSubstringsCaseInsensitiveUTF8(haystack, needle[, start_pos])

```

**Arguments**


- `haystack` — UTF\-8 string in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `start_pos` — Optional. Position (1\-based) in `haystack` at which the search starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the number of occurrences of the needle in the haystack. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT countSubstringsCaseInsensitiveUTF8('ложка, кошка, картошка', 'КА');

```


```
┌─countSubstri⋯шка', 'КА')─┐
│                        4 │
└──────────────────────────┘

```

**With start\_pos argument**



```
SELECT countSubstringsCaseInsensitiveUTF8('ложка, кошка, картошка', 'КА', 13);

```


```
┌─countSubstri⋯, 'КА', 13)─┐
│                        2 │
└──────────────────────────┘

```

## extract[​](#extract "Direct link to extract")


Introduced in: v1\.1\.0


Extracts the first match of a regular expression in a string.
If 'haystack' doesn't match 'pattern', an empty string is returned.


This function uses the RE2 regular expression library. Please refer to [re2](https://github.com/google/re2/wiki/Syntax) for supported syntax.


If the regular expression has capturing groups (sub\-patterns), the function matches the input string against the first capturing group.


**Syntax**



```
extract(haystack, pattern)

```

**Arguments**


- `haystack` — String from which to extract. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expression, typically containing a capturing group. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns extracted fragment as a string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Extract domain from email**



```
SELECT extract('[[email protected]](/cdn-cgi/l/email-protection)', '.*@(.*)$')

```


```
┌─extract('[[email protected]](/cdn-cgi/l/email-protection)', '.*@(.*)$')─┐
│ clickhouse.com                            │
└───────────────────────────────────────────┘

```

**No match returns empty string**



```
SELECT extract('[[email protected]](/cdn-cgi/l/email-protection)', 'no_match')

```


```
┌─extract('[[email protected]](/cdn-cgi/l/email-protection)', 'no_match')─┐
│                                            │
└────────────────────────────────────────────┘

```

## extractAll[​](#extractAll "Direct link to extractAll")


Introduced in: v1\.1\.0


Like [`extract`](#extract), but returns an array of all matches of a regular expression in a string.
If 'haystack' doesn't match the 'pattern' regex, an empty array is returned.


If the regular expression has capturing groups (sub\-patterns), the function matches the input string against the first capturing group.


**Syntax**



```
extractAll(haystack, pattern)

```

**Arguments**


- `haystack` — String from which to extract fragments. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expression, optionally containing capturing groups. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns array of extracted fragments. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Extract all numbers**



```
SELECT extractAll('hello 123 world 456', '[0-9]+')

```


```
┌─extractAll('hello 123 world 456', '[0-9]+')─┐
│ ['123','456']                               │
└─────────────────────────────────────────────┘

```

**Extract using capturing group**



```
SELECT extractAll('[[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection)', '([a-zA-Z0-9]+)@')

```


```
┌─extractAll('[[email protected]](/cdn-cgi/l/email-protection), [[email protected]](/cdn-cgi/l/email-protection)', '([a-zA-Z0-9]+)@')─┐
│ ['test','user']                                                    │
└────────────────────────────────────────────────────────────────────┘

```

## extractAllGroupsHorizontal[​](#extractAllGroupsHorizontal "Direct link to extractAllGroupsHorizontal")


Introduced in: v20\.5\.0


Matches all groups of a string using the provided regular expression and returns an array of arrays, where each array contains all captures from the same capturing group, organized by group number.


**Syntax**



```
extractAllGroupsHorizontal(s, regexp)

```

**Arguments**


- `s` — Input string to extract from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `regexp` — Regular expression to match by. [`const String`](/docs/sql-reference/data-types/string) or [`const FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns an array of arrays, where each inner array contains all captures from one capturing group across all matches. The first inner array contains all captures from group 1, the second from group 2, etc. If no matches are found, returns an empty array. [`Array(Array(String))`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
WITH '< Server: nginx
< Date: Tue, 22 Jan 2019 00:26:14 GMT
< Content-Type: text/html; charset=UTF-8
< Connection: keep-alive
' AS s
SELECT extractAllGroupsHorizontal(s, '< ([\\w\\-]+): ([^\\r\\n]+)');

```


```
[['Server','Date','Content-Type','Connection'],['nginx','Tue, 22 Jan 2019 00:26:14 GMT','text/html; charset=UTF-8','keep-alive']]

```

## extractGroups[​](#extractGroups "Direct link to extractGroups")


Introduced in: v20\.5\.0


Extracts the capturing groups from the first substring matched by a regular expression. To extract groups from all matches, use [`extractAllGroupsHorizontal`](#extractAllGroupsHorizontal) or [`extractAllGroupsVertical`](/docs/sql-reference/functions/splitting-merging-functions#extractAllGroupsVertical).


**Syntax**



```
extractGroups(s, regexp)

```

**Arguments**


- `s` — Input string to extract from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `regexp` — Regular expression. Must contain at least one capturing group. Constant. [`const String`](/docs/sql-reference/data-types/string) or [`const FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


If the regular expression matches, returns an array containing the captured groups (`1` to `N`, where `N` is the number of capturing groups in `regexp`) of the first match. If there is no match, returns an empty array. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
WITH '< Server: nginx
< Date: Tue, 22 Jan 2019 00:26:14 GMT
< Content-Type: text/html; charset=UTF-8
< Connection: keep-alive
' AS s
SELECT extractGroups(s, '< ([\\w\\-]+): ([^\\r\\n]+)');

```


```
['Server','nginx']

```

## hasAllTokens[​](#hasAllTokens "Direct link to hasAllTokens")


Introduced in: v25\.10\.0


Like [`hasAnyTokens`](#hasAnyTokens), but returns 1, if all tokens in the `needle` string or array match the `input` string, and 0 otherwise. If `input` is a column, returns all rows that satisfy this condition.


NoteColumn `input` should have a [text index](/docs/engines/table-engines/mergetree-family/textindexes) defined for optimal performance.
If no text index is defined, the function performs a brute\-force column scan which is orders of magnitude slower than an index lookup.


Prior to searching, the function tokenizes


- the `input` argument (always), and
- the `needle` argument (if given as a [String](/docs/sql-reference/data-types/string))
using the tokenizer specified for the text index.
If the column has no text index defined, the `splitByNonAlpha` tokenizer is used instead.
If the `needle` argument is of type [Array(String)](/docs/sql-reference/data-types/array), each array element is treated as a token — no additional tokenization takes place.


Duplicate tokens are ignored.
For example, needles \= \['ClickHouse', 'ClickHouse'] is treated the same as \['ClickHouse'].


NoteWhen a text index defines a [preprocessor](/docs/engines/table-engines/mergetree-family/textindexes#creating-a-text-index) (for example `lowerUTF8`), `hasAllTokens` applies it to `input` and, when `needles` is a [String](/docs/sql-reference/data-types/string), to `needles` before tokenization. When `needles` is an [Array(String)](/docs/sql-reference/data-types/array), its elements are passed through as\-is and the preprocessor is not applied to them.
The preprocessor is only applied on the text index path, so results may differ between queries that use the text index and queries that do not (e.g. `SETTINGS use_skip_indexes = 0`).
This inconsistency is tolerated to improve the usability of full\-text search.


**Syntax**



```
hasAllTokens(input, needles)

```

**Aliases**: `hasAllToken`


**Arguments**


- `input` — The input column. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Array(String)`](/docs/sql-reference/data-types/array) or [`Array(FixedString)`](/docs/sql-reference/data-types/array)
- `needles` — Tokens to be searched. [`String`](/docs/sql-reference/data-types/string) or [`Array(String)`](/docs/sql-reference/data-types/array)
- `tokenizer` — The tokenizer to use. Valid arguments are `splitByNonAlpha`, `splitByString`, `asciiCJK`, `ngrams`, `sparseGrams`, and `array`. Optional, if not set explicitly, defaults to `splitByNonAlpha`. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns 1, if all needles match. 0, otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage with a string needle**



```
CREATE TABLE table (
    id UInt32,
    msg String,
    INDEX idx(msg) TYPE text(tokenizer = splitByString(['()', '\\']))
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO table VALUES (1, '()a,\\bc()d'), (2, '()\\a()bc\\d'), (3, ',()a\\,bc,(),d,');

SELECT count() FROM table WHERE hasAllTokens(msg, 'a\\d()');

```


```
┌─count()─┐
│       1 │
└─────────┘

```

**Specify needles to be searched for AS\-IS (no tokenization) in an array**



```
SELECT count() FROM table WHERE hasAllTokens(msg, ['a', 'd']);

```


```
┌─count()─┐
│       1 │
└─────────┘

```

**Generate needles using the `tokens` function**



```
SELECT count() FROM table WHERE hasAllTokens(msg, tokens('a()d', 'splitByString', ['()', '\\']));

```


```
┌─count()─┐
│       1 │
└─────────┘

```

**Use a custom tokenizer via the 3rd argument**



```
SELECT hasAllTokens('abcdef', 'abc', 'ngrams(3)');

```


```
┌─hasAllTokens('abcdef', 'abc', 'ngrams(3)')─┐
│                                            1 │
└──────────────────────────────────────────────┘

```

**Usage examples for array and map columns**



```
CREATE TABLE log (
    id UInt32,
    tags Array(String),
    attributes Map(String, String),
    INDEX idx_tags (tags) TYPE text(tokenizer = splitByNonAlpha),
    INDEX idx_attributes_keys mapKeys(attributes) TYPE text(tokenizer = array),
    INDEX idx_attributes_vals mapValues(attributes) TYPE text(tokenizer = array)
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO log VALUES
    (1, ['clickhouse', 'clickhouse cloud'], {'address': '192.0.0.1', 'log_level': 'INFO'}),
    (2, ['chdb'], {'embedded': 'true', 'log_level': 'DEBUG'});

```


**Example with an array column**



```
SELECT count() FROM log WHERE hasAllTokens(tags, 'clickhouse');

```


```
┌─count()─┐
│       1 │
└─────────┘

```

**Example with mapKeys**



```
SELECT count() FROM log WHERE hasAllTokens(mapKeys(attributes), ['address', 'log_level']);

```


```
┌─count()─┐
│       1 │
└─────────┘

```

**Example with mapValues**



```
SELECT count() FROM log WHERE hasAllTokens(mapValues(attributes), ['192.0.0.1', 'DEBUG']);

```


```
┌─count()─┐
│       0 │
└─────────┘

```

## hasAnyTokens[​](#hasAnyTokens "Direct link to hasAnyTokens")


Introduced in: v25\.10\.0


Returns 1, if at least one token in the `needle` string or array matches the `input` string, and 0 otherwise. If `input` is a column, returns all rows that satisfy this condition.


NoteColumn `input` should have a [text index](/docs/engines/table-engines/mergetree-family/textindexes) defined for optimal performance.
If no text index is defined, the function performs a brute\-force column scan which is orders of magnitude slower than an index lookup.


Prior to searching, the function tokenizes


- the `input` argument (always), and
- the `needle` argument (if given as a [String](/docs/sql-reference/data-types/string))
using the tokenizer specified for the text index.
If the column has no text index defined, the `splitByNonAlpha` tokenizer is used instead.
If the `needle` argument is of type [Array(String)](/docs/sql-reference/data-types/array), each array element is treated as a token — no additional tokenization takes place.


Duplicate tokens are ignored.
For example, \['ClickHouse', 'ClickHouse'] is treated the same as \['ClickHouse'].


NoteWhen a text index defines a [preprocessor](/docs/engines/table-engines/mergetree-family/textindexes#creating-a-text-index) (for example `lowerUTF8`), `hasAnyTokens` applies it to `input` and, when `needles` is a [String](/docs/sql-reference/data-types/string), to `needles` before tokenization. When `needles` is an [Array(String)](/docs/sql-reference/data-types/array), its elements are passed through as\-is and the preprocessor is not applied to them.
The preprocessor is only applied on the text index path, so results may differ between queries that use the text index and queries that do not (e.g. `SETTINGS use_skip_indexes = 0`).
This inconsistency is tolerated to improve the usability of full\-text search.


**Syntax**



```
hasAnyTokens(input, needles)

```

**Aliases**: `hasAnyToken`


**Arguments**


- `input` — The input column. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Nullable(String)`](/docs/sql-reference/data-types/nullable) or [`Nullable(FixedString)`](/docs/sql-reference/data-types/nullable) or [`Array(String)`](/docs/sql-reference/data-types/array) or [`Array(FixedString)`](/docs/sql-reference/data-types/array) or [`Array(Nullable(String))`](/docs/sql-reference/data-types/array) or [`Array(Nullable(FixedString))`](/docs/sql-reference/data-types/array)
- `needles` — Tokens to be searched. [`String`](/docs/sql-reference/data-types/string) or [`Array(String)`](/docs/sql-reference/data-types/array)
- `tokenizer` — The tokenizer to use. Valid arguments are `splitByNonAlpha`, `splitByString`, `asciiCJK`, `ngrams`, `sparseGrams`, and `array`. Optional, if not set explicitly, defaults to `splitByNonAlpha`. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1`, if there was at least one match. `0`, otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage with a string needle**



```
CREATE TABLE table (
    id UInt32,
    msg String,
    INDEX idx(msg) TYPE text(tokenizer = splitByString(['()', '\\']))
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO table VALUES (1, '()a,\\bc()d'), (2, '()\\a()bc\\d'), (3, ',()a\\,bc,(),d,');

SELECT count() FROM table WHERE hasAnyTokens(msg, 'a\\d()');

```


```
┌─count()─┐
│       3 │
└─────────┘

```

**Specify needles to be searched for AS\-IS (no tokenization) in an array**



```
SELECT count() FROM table WHERE hasAnyTokens(msg, ['a', 'd']);

```


```
┌─count()─┐
│       3 │
└─────────┘

```

**Generate needles using the `tokens` function**



```
SELECT count() FROM table WHERE hasAnyTokens(msg, tokens('a()d', 'splitByString', ['()', '\\']));

```


```
┌─count()─┐
│       3 │
└─────────┘

```

**Usage examples for array and map columns**



```
CREATE TABLE log (
    id UInt32,
    tags Array(String),
    attributes Map(String, String),
    INDEX idx_tags (tags) TYPE text(tokenizer = splitByNonAlpha),
    INDEX idx_attributes_keys mapKeys(attributes) TYPE text(tokenizer = array),
    INDEX idx_attributes_vals mapValues(attributes) TYPE text(tokenizer = array)
)
ENGINE = MergeTree
ORDER BY id;

INSERT INTO log VALUES
    (1, ['clickhouse', 'clickhouse cloud'], {'address': '192.0.0.1', 'log_level': 'INFO'}),
    (2, ['chdb'], {'embedded': 'true', 'log_level': 'DEBUG'});

```


**Example with an array column**



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


```
┌─hasPhrase('the quick brown fox jumps', 'quick brown')─┐
│                                                      1 │
└────────────────────────────────────────────────────────┘

```

**Non\-consecutive tokens**



```
SELECT hasPhrase('the quick brown fox jumps', 'quick fox')

```


```
┌─hasPhrase('the quick brown fox jumps', 'quick fox')─┐
│                                                    0 │
└──────────────────────────────────────────────────────┘

```

## hasSubsequence[​](#hasSubsequence "Direct link to hasSubsequence")


Introduced in: v23\.7\.0


Checks if a needle is a subsequence of a haystack.
A subsequence of a string is a sequence that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.


**Syntax**



```
hasSubsequence(haystack, needle)

```

**Arguments**


- `haystack` — String in which to search for the subsequence. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Subsequence to be searched. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if needle is a subsequence of haystack, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic subsequence check**



```
SELECT hasSubsequence('Hello World', 'HlWrd')

```


```
┌─hasSubsequence('Hello World', 'HlWrd')─┐
│                                      1 │
└────────────────────────────────────────┘

```

**No subsequence found**



```
SELECT hasSubsequence('Hello World', 'xyz')

```


```
┌─hasSubsequence('Hello World', 'xyz')─┐
│                                    0 │
└──────────────────────────────────────┘

```

## hasSubsequenceCaseInsensitive[​](#hasSubsequenceCaseInsensitive "Direct link to hasSubsequenceCaseInsensitive")


Introduced in: v23\.7\.0


Like [`hasSubsequence`](#hasSubsequence) but searches case\-insensitively.


**Syntax**



```
hasSubsequenceCaseInsensitive(haystack, needle)

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Subsequence to be searched. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns 1, if needle is a subsequence of haystack, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT hasSubsequenceCaseInsensitive('garbage', 'ARG');

```


```
┌─hasSubsequenceCaseInsensitive('garbage', 'ARG')─┐
│                                               1 │
└─────────────────────────────────────────────────┘

```

## hasSubsequenceCaseInsensitiveUTF8[​](#hasSubsequenceCaseInsensitiveUTF8 "Direct link to hasSubsequenceCaseInsensitiveUTF8")


Introduced in: v23\.7\.0


Like [`hasSubsequenceUTF8`](#hasSubsequenceUTF8) but searches case\-insensitively.


**Syntax**



```
hasSubsequenceCaseInsensitiveUTF8(haystack, needle)

```

**Arguments**


- `haystack` — UTF8\-encoded string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — UTF8\-encoded subsequence string to be searched. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns 1, if needle is a subsequence of haystack, 0 otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT hasSubsequenceCaseInsensitiveUTF8('ClickHouse - столбцовая система управления базами данных', 'СИСТЕМА');

```


```
┌─hasSubsequen⋯ 'СИСТЕМА')─┐
│                        1 │
└──────────────────────────┘

```

## hasSubsequenceUTF8[​](#hasSubsequenceUTF8 "Direct link to hasSubsequenceUTF8")


Introduced in: v23\.7\.0


Like [`hasSubsequence`](/docs/sql-reference/functions/string-search-functions#hasSubsequence) but assumes haystack and needle are UTF\-8 encoded strings.


**Syntax**



```
hasSubsequenceUTF8(haystack, needle)

```

**Arguments**


- `haystack` — The string in which to search. [`String`](/docs/sql-reference/data-types/string)
- `needle` — The subsequence to search for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `needle` is a subsequence of `haystack`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT hasSubsequenceUTF8('картошка', 'кошка');

```


```
┌─hasSubsequen⋯', 'кошка')─┐
│                        1 │
└──────────────────────────┘

```

**Non\-matching subsequence**



```
SELECT hasSubsequenceUTF8('картошка', 'апельсин');

```


```
┌─hasSubsequen⋯'апельсин')─┐
│                        0 │
└──────────────────────────┘

```

## hasToken[​](#hasToken "Direct link to hasToken")


Introduced in: v20\.1\.0


Checks if the given token is present in the haystack.


Uses [splitByNonAlpha](/docs/sql-reference/functions/splitting-merging-functions#splitByNonAlpha) as tokenizer, i.e. a token is defined as the longest possible sub\-sequence of consecutive characters `[0-9A-Za-z_]` (numbers, ASCII characters and underscore).


**Syntax**



```
hasToken(haystack, token)

```

**Arguments**


- `haystack` — String to be searched. [`String`](/docs/sql-reference/data-types/string)
- `token` — Token to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the token is found, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Token search**



```
SELECT hasToken('clickhouse test', 'test')

```


```
┌─hasToken('clickhouse test', 'test')─┐
│                                   1 │
└─────────────────────────────────────┘

```

## hasTokenCaseInsensitive[​](#hasTokenCaseInsensitive "Direct link to hasTokenCaseInsensitive")


Introduced in: v20\.1\.0


Performs case insensitive lookup of needle in haystack using tokenbf\_v1 index.


**Syntax**



```
hasTokenCaseInsensitive(haystack, needle)

```

**Arguments**


- None.


**Returned value**


**Examples**


## hasTokenCaseInsensitiveOrNull[​](#hasTokenCaseInsensitiveOrNull "Direct link to hasTokenCaseInsensitiveOrNull")


Introduced in: v23\.1\.0


Performs case insensitive lookup of needle in haystack using tokenbf\_v1 index. Returns null if needle is ill\-formed.


**Syntax**



```
hasTokenCaseInsensitiveOrNull(haystack, needle)

```

**Arguments**


- None.


**Returned value**


**Examples**


## hasTokenOrNull[​](#hasTokenOrNull "Direct link to hasTokenOrNull")


Introduced in: v20\.1\.0


Like [`hasToken`](#hasToken) but returns null if token is ill\-formed.


**Syntax**



```
hasTokenOrNull(haystack, token)

```

**Arguments**


- `haystack` — String to be searched. Must be constant. [`String`](/docs/sql-reference/data-types/string)
- `token` — Token to search for. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the token is found, `0` otherwise, null if token is ill\-formed. [`Nullable(UInt8)`](/docs/sql-reference/data-types/nullable)


**Examples**


**Usage example**



```
SELECT hasTokenOrNull('apple banana cherry', 'ban ana');

```


```
┌─hasTokenOrNu⋯ 'ban ana')─┐
│                     ᴺᵁᴸᴸ │
└──────────────────────────┘

```

## highlight[​](#highlight "Direct link to highlight")


Introduced in: v26\.4\.0


Highlights occurrences of search terms in a text string by wrapping them with HTML tags.


The function performs ASCII case\-insensitive matching. If multiple search terms overlap or are adjacent in the text, the matched regions are merged into a single highlighted span.


**Syntax**



```
highlight(haystack, needles[, open_tag, close_tag])

```

**Arguments**


- `haystack` — The text to search in. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `needles` — An array of search terms to highlight. [`const Array(String)`](/docs/sql-reference/data-types/array)
- `open_tag` — The opening tag to insert before each match. Default: `<em>`. [`const String`](/docs/sql-reference/data-types/string)
- `close_tag` — The closing tag to insert after each match. Default: `</em>`. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the input text with matched terms wrapped in the specified tags. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic highlight**



```
SELECT highlight('The quick brown fox', ['quick', 'fox'])

```


```
┌─highlight('The quick brown fox', ['quick', 'fox'])─┐
│ The <em>quick</em> brown <em>fox</em>              │
└────────────────────────────────────────────────────┘

```

**Custom tags**



```
SELECT highlight('Hello World', ['hello'], '<b>', '</b>')

```


```
┌─highlight('Hello World', ['hello'], '<b>', '</b>')─┐
│ <b>Hello</b> World                                 │
└────────────────────────────────────────────────────┘

```

## ilike[​](#ilike "Direct link to ilike")


Introduced in: v20\.6\.0


Like [`like`](#like) but searches case\-insensitively.


**Syntax**



```
ilike(haystack, pattern)
-- haystack ILIKE pattern

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `pattern` — LIKE pattern to match against. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the string matches the LIKE pattern (case\-insensitive), otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT ilike('ClickHouse', '%house%');

```


```
┌─ilike('ClickHouse', '%house%')─┐
│                              1 │
└────────────────────────────────┘

```

## like[​](#like "Direct link to like")


Introduced in: v1\.1\.0


Returns whether string `haystack` matches the `LIKE` expression `pattern`.


A `LIKE` expression can contain normal characters and the following metasymbols:


- `%` indicates an arbitrary number of arbitrary characters (including zero characters).
- `_` indicates a single arbitrary character.
- `\` is for escaping literals `%`, `_` and `\`.


Matching is based on UTF\-8, e.g. `_` matches the Unicode code point `¥` which is represented in UTF\-8 using two bytes.


If the haystack or the `LIKE` expression are not valid UTF\-8, the behavior is undefined.


No automatic Unicode normalization is performed, you can use the `normalizeUTF8*` functions for that.


To match against literal `%`, `_` and `\` (which are `LIKE` metacharacters), prepend them with a backslash: `\%`, `\_` and `\\`.
The backslash loses its special meaning (i.e. is interpreted literally) if it prepends a character different than `%`, `_` or `\`.


NoteClickHouse requires backslashes in strings [to be quoted as well](/docs/sql-reference/syntax#string), so you would actually need to write `\\%`, `\\_` and `\\\\`.


For `LIKE` expressions of the form `%needle%`, the function is as fast as the `position` function.
All other LIKE expressions are internally converted to a regular expression and executed with a performance similar to function `match`.


**Syntax**



```
like(haystack, pattern)
-- haystack LIKE pattern

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `pattern` — `LIKE` pattern to match against. Can contain `%` (matches any number of characters), `_` (matches single character), and `\` for escaping. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the string matches the `LIKE` pattern, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT like('ClickHouse', '%House');

```


```
┌─like('ClickHouse', '%House')─┐
│                            1 │
└──────────────────────────────┘

```

**Single character wildcard**



```
SELECT like('ClickHouse', 'Click_ouse');

```


```
┌─like('ClickH⋯lick_ouse')─┐
│                        1 │
└──────────────────────────┘

```

**Non\-matching pattern**



```
SELECT like('ClickHouse', '%SQL%');

```


```
┌─like('ClickHouse', '%SQL%')─┐
│                           0 │
└─────────────────────────────┘

```

## locate[​](#locate "Direct link to locate")


Introduced in: v18\.16\.0


Like [`position`](#position) but with arguments `haystack` and `locate` switched.


Version dependent behaviorThe behavior of this function depends on the ClickHouse version:- in versions \< v24\.3, `locate` was an alias of function `position` and accepted arguments `(haystack, needle[, start_pos])`.
- in versions \>\= 24\.3, `locate` is an individual function (for better compatibility with MySQL) and accepts arguments `(needle, haystack[, start_pos])`.
The previous behavior can be restored using setting `function_locate_has_mysql_compatible_argument_order = false`.



**Syntax**



```
locate(needle, haystack[, start_pos])

```

**Arguments**


- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `start_pos` — Optional. Position (1\-based) in `haystack` at which the search starts. [`UInt`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns starting position in bytes and counting from 1, if the substring was found, `0`, if the substring was not found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT locate('ca', 'abcabc')

```


```
┌─locate('ca', 'abcabc')─┐
│                      3 │
└────────────────────────┘

```

## match[​](#match "Direct link to match")


Introduced in: v1\.1\.0


Checks if a provided string matches the provided regular expression pattern.


This function uses the RE2 regular expression library. Please refer to [re2](https://github.com/google/re2/wiki/Syntax) for supported syntax.


Matching works under UTF\-8 assumptions, e.g. `¥` uses two bytes internally but matching treats it as a single codepoint.
The regular expression must not contain NULL bytes.
If the haystack or the pattern are not valid UTF\-8, the behavior is undefined.


Unlike re2's default behavior, `.` matches line breaks. To disable this, prepend the pattern with `(?-s)`.


The pattern is not anchored. To match the entire string, anchor the pattern yourself using `^` and `$`.


If you just want to search for substrings, you can use functions [`like`](#like) or [`position`](#position) instead, which work much faster than this function.


Alternative operator syntax: `haystack REGEXP pattern`.


**Syntax**



```
match(haystack, pattern)

```

**Aliases**: `REGEXP_MATCHES`


**Arguments**


- `haystack` — String in which the pattern is searched. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expression pattern. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the pattern matches, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic pattern matching**



```
SELECT match('Hello World', 'Hello.*')

```


```
┌─match('Hello World', 'Hello.*')─┐
│                               1 │
└─────────────────────────────────┘

```

**Pattern not matching**



```
SELECT match('Hello World', 'goodbye.*')

```


```
┌─match('Hello World', 'goodbye.*')─┐
│                                 0 │
└───────────────────────────────────┘

```

**Matching a substring**



```
SELECT match('abcde', 'b.*d'), match('abcde', '^b.*d$')

```


```
┌─match('abcde', 'b.*d')─┬─match('abcde', '^b.*d$')─┐
│                       1 │                         0 │
└─────────────────────────┴───────────────────────────┘

```

## multiFuzzyMatchAllIndices[​](#multiFuzzyMatchAllIndices "Direct link to multiFuzzyMatchAllIndices")


Introduced in: v20\.1\.0


Like [`multiFuzzyMatchAny`](#multiFuzzyMatchAny) but returns the array of all indices in any order that match the haystack within a constant [edit distance](https://en.wikipedia.org/wiki/Edit_distance).


**Syntax**



```
multiFuzzyMatchAllIndices(haystack, distance, [pattern1, pattern2, ..., patternN])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `distance` — The maximum edit distance for fuzzy matching. [`UInt8`](/docs/sql-reference/data-types/int-uint)
- `pattern` — Array of patterns to match against. [`Array(String)`](/docs/sql-reference/data-types/array)


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


Like [`multiMatchAny`](#multiMatchAny) but returns the array of all indices that match the haystack in any order.


**Syntax**



```
multiMatchAllIndices(haystack, [pattern1, pattern2, ..., patternn])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expressions to match against. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Array of all indices (starting from 1\) that match the haystack in any order. Returns an empty array if no matches are found. [`Array(UInt64)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT multiMatchAllIndices('ClickHouse', ['[0-9]', 'House', 'Click', 'ouse']);

```


```
┌─multiMatchAl⋯', 'ouse'])─┐
│ [3, 2, 4]                │
└──────────────────────────┘

```

## multiMatchAny[​](#multiMatchAny "Direct link to multiMatchAny")


Introduced in: v20\.1\.0


Check if at least one of multiple regular expression patterns matches a haystack.


If you only want to search multiple substrings in a string, you can use function [`multiSearchAny`](#multiSearchAny) instead \- it works much faster than this function.


**Syntax**



```
multiMatchAny(haystack, pattern1[, pattern2, ...])

```

**Arguments**


- `haystack` — String in which patterns are searched. [`String`](/docs/sql-reference/data-types/string)
- `pattern1[, pattern2, ...]` — An array of one or more regular expression patterns. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1` if any pattern matches, `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Multiple pattern matching**



```
SELECT multiMatchAny('Hello World', ['Hello.*', 'foo.*'])

```


```
┌─multiMatchAny('Hello World', ['Hello.*', 'foo.*'])─┐
│                                                  1 │
└────────────────────────────────────────────────────┘

```

**No patterns match**



```
SELECT multiMatchAny('Hello World', ['goodbye.*', 'foo.*'])

```


```
┌─multiMatchAny('Hello World', ['goodbye.*', 'foo.*'])─┐
│                                                    0 │
└──────────────────────────────────────────────────────┘

```

## multiMatchAnyIndex[​](#multiMatchAnyIndex "Direct link to multiMatchAnyIndex")


Introduced in: v20\.1\.0


Like [`multiMatchAny`](#multiMatchAny) but returns any index that matches the haystack.


**Syntax**



```
multiMatchAnyIndex(haystack, [pattern1, pattern2, ..., patternn])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expressions to match against. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the index (starting from 1\) of the first pattern that matches, or 0 if no match is found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT multiMatchAnyIndex('ClickHouse', ['[0-9]', 'House', 'Click']);

```


```
┌─multiMatchAn⋯, 'Click'])─┐
│                        3 │
└──────────────────────────┘

```

## multiSearchAllPositions[​](#multiSearchAllPositions "Direct link to multiSearchAllPositions")


Introduced in: v20\.1\.0


Like [`position`](#position) but returns an array of positions (in bytes, starting at 1\) for multiple `needle` substrings in a `haystack` string.


All `multiSearch*()` functions only support up to 2^8 needles.


**Syntax**



```
multiSearchAllPositions(haystack, needle1[, needle2, ...])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle1[, needle2, ...]` — An array of one or more substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns array of the starting position in bytes and counting from 1, if the substring was found, `0`, if the substring was not found. [`Array(UInt64)`](/docs/sql-reference/data-types/array)


**Examples**


**Multiple needle search**



```
SELECT multiSearchAllPositions('Hello, World!', ['hello', '!', 'world'])

```


```
┌─multiSearchAllPositions('Hello, World!', ['hello', '!', 'world'])─┐
│ [0,13,0]                                                          │
└───────────────────────────────────────────────────────────────────┘

```

## multiSearchAllPositionsCaseInsensitive[​](#multiSearchAllPositionsCaseInsensitive "Direct link to multiSearchAllPositionsCaseInsensitive")


Introduced in: v20\.1\.0


Like [`multiSearchAllPositions`](#multiSearchAllPositions) but ignores case.


**Syntax**



```
multiSearchAllPositionsCaseInsensitive(haystack, needle1[, needle2, ...])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle1[, needle2, ...]` — An array of one or more substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns array of the starting position in bytes and counting from 1 (if the substring was found), `0` if the substring was not found. [`Array(UInt64)`](/docs/sql-reference/data-types/array)


**Examples**


**Case insensitive multi\-search**



```
SELECT multiSearchAllPositionsCaseInsensitive('ClickHouse',['c','h'])

```


```
┌─multiSearchA⋯['c', 'h'])─┐
│ [1,6]                    │
└──────────────────────────┘

```

## multiSearchAllPositionsCaseInsensitiveUTF8[​](#multiSearchAllPositionsCaseInsensitiveUTF8 "Direct link to multiSearchAllPositionsCaseInsensitiveUTF8")


Introduced in: v20\.1\.0


Like [`multiSearchAllPositionsUTF8`](#multiSearchAllPositionsUTF8) but ignores case.


**Syntax**



```
multiSearchAllPositionsCaseInsensitiveUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — UTF\-8 encoded string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — UTF\-8 encoded substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Array of the starting position in bytes and counting from 1 (if the substring was found). Returns 0 if the substring was not found. [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**Case\-insensitive UTF\-8 search**



```
SELECT multiSearchAllPositionsCaseInsensitiveUTF8('Здравствуй, мир!', ['здравствуй', 'МИР']);

```


```
┌─multiSearchA⋯й', 'МИР'])─┐
│ [1, 13]                  │
└──────────────────────────┘

```

## multiSearchAllPositionsUTF8[​](#multiSearchAllPositionsUTF8 "Direct link to multiSearchAllPositionsUTF8")


Introduced in: v20\.1\.0


Like [`multiSearchAllPositions`](#multiSearchAllPositions) but assumes `haystack` and the `needle` substrings are UTF\-8 encoded strings.


**Syntax**



```
multiSearchAllPositionsUTF8(haystack, needle1[, needle2, ...])

```

**Arguments**


- `haystack` — UTF\-8 encoded string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle1[, needle2, ...]` — An array of UTF\-8 encoded substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns array of the starting position in bytes and counting from 1 (if the substring was found), `0` if the substring was not found. [`Array`](/docs/sql-reference/data-types/array)


**Examples**


**UTF\-8 multi\-search**



```
SELECT multiSearchAllPositionsUTF8('ClickHouse',['C','H'])

```


```
┌─multiSearchAllPositionsUTF8('ClickHouse', ['C', 'H'])─┐
│ [1,6]                                                 │
└───────────────────────────────────────────────────────┘

```

## multiSearchAny[​](#multiSearchAny "Direct link to multiSearchAny")


Introduced in: v20\.1\.0


Checks if at least one of a number of needle strings matches the haystack string.


Functions [`multiSearchAnyCaseInsensitive`](#multiSearchAnyCaseInsensitive), [`multiSearchAnyUTF8`](#multiSearchAnyUTF8) and [`multiSearchAnyCaseInsensitiveUTF8`](#multiSearchAnyCaseInsensitiveUTF8) provide case\-insensitive and/or UTF\-8 variants of this function.


**Syntax**



```
multiSearchAny(haystack, needle1[, needle2, ...])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle1[, needle2, ...]` — An array of substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1`, if there was at least one match, otherwise `0`, if there was not at least one match. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Any match search**



```
SELECT multiSearchAny('ClickHouse',['C','H'])

```


```
┌─multiSearchAny('ClickHouse', ['C', 'H'])─┐
│                                        1 │
└──────────────────────────────────────────┘

```

## multiSearchAnyCaseInsensitive[​](#multiSearchAnyCaseInsensitive "Direct link to multiSearchAnyCaseInsensitive")


Introduced in: v20\.1\.0


Like [multiSearchAny](#multiSearchAny) but ignores case.


**Syntax**



```
multiSearchAnyCaseInsensitive(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1`, if there was at least one case\-insensitive match, otherwise `0`, if there was not at least one case\-insensitive match. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case insensitive search**



```
SELECT multiSearchAnyCaseInsensitive('ClickHouse',['c','h'])

```


```
┌─multiSearchAnyCaseInsensitive('ClickHouse', ['c', 'h'])─┐
│                                                       1 │
└─────────────────────────────────────────────────────────┘

```

## multiSearchAnyCaseInsensitiveUTF8[​](#multiSearchAnyCaseInsensitiveUTF8 "Direct link to multiSearchAnyCaseInsensitiveUTF8")


Introduced in: v20\.1\.0


Like [multiSearchAnyUTF8](#multiSearchAnyUTF8) but ignores case.


**Syntax**



```
multiSearchAnyCaseInsensitiveUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — UTF\-8 string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — UTF\-8 substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1`, if there was at least one case\-insensitive match, otherwise `0`, if there was not at least one case\-insensitive match. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Given a UTF\-8 string 'Здравствуйте', check if character 'з' (lowercase) is present**



```
SELECT multiSearchAnyCaseInsensitiveUTF8('Здравствуйте',['з'])

```


```
┌─multiSearchA⋯те', ['з'])─┐
│                        1 │
└──────────────────────────┘

```

## multiSearchAnyUTF8[​](#multiSearchAnyUTF8 "Direct link to multiSearchAnyUTF8")


Introduced in: v20\.1\.0


Like [multiSearchAny](#multiSearchAny) but assumes `haystack` and the `needle` substrings are UTF\-8 encoded strings.


**Syntax**



```
multiSearchAnyUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — UTF\-8 string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — UTF\-8 substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns `1`, if there was at least one match, otherwise `0`, if there was not at least one match. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Given '你好，世界' ('Hello, world') as a UTF\-8 string, check if there are any 你 or 界 characters in the string**



```
SELECT multiSearchAnyUTF8('你好，世界', ['你', '界'])

```


```
┌─multiSearchA⋯你', '界'])─┐
│                        1 │
└──────────────────────────┘

```

## multiSearchFirstIndex[​](#multiSearchFirstIndex "Direct link to multiSearchFirstIndex")


Introduced in: v20\.1\.0


Searches for multiple needle strings in a haystack string (case\-sensitive) and returns the 1\-based index of the first needle found.


**Syntax**



```
multiSearchFirstIndex(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — The string to search in. [`String`](/docs/sql-reference/data-types/string)
- `needles` — Array of strings to search for. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the 1\-based index (position in the needles array) of the first needle found in the haystack. Returns 0 if no needles are found. The search is case\-sensitive. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT multiSearchFirstIndex('ClickHouse Database', ['Click', 'Database', 'Server']);

```


```
┌─multiSearchF⋯ 'Server'])─┐
│                        1 │
└──────────────────────────┘

```

**Case\-sensitive behavior**



```
SELECT multiSearchFirstIndex('ClickHouse Database', ['CLICK', 'Database', 'Server']);

```


```
┌─multiSearchF⋯ 'Server'])─┐
│                        2 │
└──────────────────────────┘

```

**No match found**



```
SELECT multiSearchFirstIndex('Hello World', ['goodbye', 'test']);

```


```
┌─multiSearchF⋯', 'test'])─┐
│                        0 │
└──────────────────────────┘

```

## multiSearchFirstIndexCaseInsensitive[​](#multiSearchFirstIndexCaseInsensitive "Direct link to multiSearchFirstIndexCaseInsensitive")


Introduced in: v20\.1\.0


Returns the index `i` (starting from 1\) of the leftmost found needle\_i in the string `haystack` and 0 otherwise.
Ignores case.


**Syntax**



```
multiSearchFirstIndexCaseInsensitive(haystack, [needle1, needle2, ..., needleN]

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the index (starting from 1\) of the leftmost found needle. Otherwise `0`, if there was no match. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT multiSearchFirstIndexCaseInsensitive('hElLo WoRlD', ['World', 'Hello']);

```


```
┌─multiSearchF⋯, 'Hello'])─┐
│                        1 │
└──────────────────────────┘

```

## multiSearchFirstIndexCaseInsensitiveUTF8[​](#multiSearchFirstIndexCaseInsensitiveUTF8 "Direct link to multiSearchFirstIndexCaseInsensitiveUTF8")


Introduced in: v20\.1\.0


Searches for multiple needle strings in a haystack string, case\-insensitively with UTF\-8 encoding support, and returns the 1\-based index of the first needle found.


**Syntax**



```
multiSearchFirstIndexCaseInsensitiveUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — The string to search in. [`String`](/docs/sql-reference/data-types/string)
- `needles` — Array of strings to search for. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the 1\-based index (position in the needles array) of the first needle found in the haystack. Returns 0 if no needles are found. The search is case\-insensitive and respects UTF\-8 character encoding. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT multiSearchFirstIndexCaseInsensitiveUTF8('ClickHouse Database', ['CLICK', 'data', 'server']);

```


```
┌─multiSearchF⋯ 'server'])─┐
│                        1 │
└──────────────────────────┘

```

**UTF\-8 case handling**



```
SELECT multiSearchFirstIndexCaseInsensitiveUTF8('Привет Мир', ['мир', 'ПРИВЕТ']);

```


```
┌─multiSearchF⋯ 'ПРИВЕТ'])─┐
│                        1 │
└──────────────────────────┘

```

**No match found**



```
SELECT multiSearchFirstIndexCaseInsensitiveUTF8('Hello World', ['goodbye', 'test']);

```


```
┌─multiSearchF⋯', 'test'])─┐
│                        0 │
└──────────────────────────┘

```

## multiSearchFirstIndexUTF8[​](#multiSearchFirstIndexUTF8 "Direct link to multiSearchFirstIndexUTF8")


Introduced in: v20\.1\.0


Returns the index `i` (starting from 1\) of the leftmost found needle\_i in the string `haystack` and 0 otherwise.
Assumes `haystack` and `needle` are UTF\-8 encoded strings.


**Syntax**



```
multiSearchFirstIndexUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — UTF\-8 string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Array of UTF\-8 substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the index (starting from 1\) of the leftmost found needle. Otherwise 0, if there was no match. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT multiSearchFirstIndexUTF8('Здравствуйте мир', ['мир', 'здравствуйте']);

```


```
┌─multiSearchF⋯вствуйте'])─┐
│                        1 │
└──────────────────────────┘

```

## multiSearchFirstPosition[​](#multiSearchFirstPosition "Direct link to multiSearchFirstPosition")


Introduced in: v20\.1\.0


Like [`position`](#position) but returns the leftmost offset in a `haystack` string which matches any of multiple `needle` strings.


Functions [`multiSearchFirstPositionCaseInsensitive`](#multiSearchFirstPositionCaseInsensitive), [`multiSearchFirstPositionUTF8`](#multiSearchFirstPositionUTF8) and [`multiSearchFirstPositionCaseInsensitiveUTF8`](#multiSearchFirstPositionCaseInsensitiveUTF8) provide case\-insensitive and/or UTF\-8 variants of this function.


**Syntax**



```
multiSearchFirstPosition(haystack, needle1[, needle2, ...])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle1[, needle2, ...]` — An array of one or more substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the leftmost offset in a `haystack` string which matches any of multiple `needle` strings, otherwise `0`, if there was no match. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**First position search**



```
SELECT multiSearchFirstPosition('Hello World',['llo', 'Wor', 'ld'])

```


```
┌─multiSearchFirstPosition('Hello World', ['llo', 'Wor', 'ld'])─┐
│                                                             3 │
└───────────────────────────────────────────────────────────────┘

```

## multiSearchFirstPositionCaseInsensitive[​](#multiSearchFirstPositionCaseInsensitive "Direct link to multiSearchFirstPositionCaseInsensitive")


Introduced in: v20\.1\.0


Like [multiSearchFirstPosition](#multiSearchFirstPosition) but ignores case.


**Syntax**



```
multiSearchFirstPositionCaseInsensitive(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Array of substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the leftmost offset in a `haystack` string which matches any of multiple `needle` strings. Returns `0`, if there was no match. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case insensitive first position**



```
SELECT multiSearchFirstPositionCaseInsensitive('HELLO WORLD',['wor', 'ld', 'ello'])

```


```
┌─multiSearchFirstPositionCaseInsensitive('HELLO WORLD', ['wor', 'ld', 'ello'])─┐
│                                                                             2 │
└───────────────────────────────────────────────────────────────────────────────┘

```

## multiSearchFirstPositionCaseInsensitiveUTF8[​](#multiSearchFirstPositionCaseInsensitiveUTF8 "Direct link to multiSearchFirstPositionCaseInsensitiveUTF8")


Introduced in: v20\.1\.0


Like [multiSearchFirstPosition](#multiSearchFirstPosition) but assumes `haystack` and `needle` to be UTF\-8 strings and ignores case.


**Syntax**



```
multiSearchFirstPositionCaseInsensitiveUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — UTF\-8 string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Array of UTF\-8 substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Returns the leftmost offset in a `haystack` string which matches any of multiple `needle` strings, ignoring case. Returns `0`, if there was no match. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Find the leftmost offset in UTF\-8 string 'Здравствуй, мир' ('Hello, world') which matches any of the given needles**



```
SELECT multiSearchFirstPositionCaseInsensitiveUTF8('Здравствуй, мир', ['МИР', 'вст', 'Здра'])

```


```
┌─multiSearchFirstPositionCaseInsensitiveUTF8('Здравствуй, мир', ['мир', 'вст', 'Здра'])─┐
│                                                                                      3 │
└────────────────────────────────────────────────────────────────────────────────────────┘

```

## multiSearchFirstPositionUTF8[​](#multiSearchFirstPositionUTF8 "Direct link to multiSearchFirstPositionUTF8")


Introduced in: v20\.1\.0


Like [multiSearchFirstPosition](#multiSearchFirstPosition) but assumes `haystack` and `needle` to be UTF\-8 strings.


**Syntax**



```
multiSearchFirstPositionUTF8(haystack, [needle1, needle2, ..., needleN])

```

**Arguments**


- `haystack` — UTF\-8 string in which the search is performed. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Array of UTF\-8 substrings to be searched. [`Array(String)`](/docs/sql-reference/data-types/array)


**Returned value**


Leftmost offset in a `haystack` string which matches any of multiple `needle` strings. Returns `0`, if there was no match. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Find the leftmost offset in UTF\-8 string 'Здравствуй, мир' ('Hello, world') which matches any of the given needles**



```
SELECT multiSearchFirstPositionUTF8('Здравствуй, мир',['мир', 'вст', 'авст'])

```


```
┌─multiSearchFirstPositionUTF8('Здравствуй, мир', ['мир', 'вст', 'авст'])─┐
│                                                                       3 │
└─────────────────────────────────────────────────────────────────────────┘

```

## ngramDistance[​](#ngramDistance "Direct link to ngramDistance")


Introduced in: v20\.1\.0


Calculates the 4\-gram distance between two strings.
For this, it counts the symmetric difference between two multisets of 4\-grams and normalizes it by the sum of their cardinalities.
The smaller the returned value, the more similar the strings are.


For case\-insensitive search or/and in UTF8 format use functions [`ngramDistanceCaseInsensitive`](#ngramDistanceCaseInsensitive), [`ngramDistanceUTF8`](#ngramDistanceUTF8), [`ngramDistanceCaseInsensitiveUTF8`](#ngramDistanceCaseInsensitiveUTF8).


**Syntax**



```
ngramDistance(haystack, needle)

```

**Arguments**


- `haystack` — String for comparison. [`String`](/docs/sql-reference/data-types/string)
- `needle` — String for comparison. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Float32 number between `0` and `1`. The smaller the returned value, the more similar the strings are. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Calculate 4\-gram distance**



```
SELECT ngramDistance('ClickHouse', 'ClickHouses')

```


```
┌─ngramDistance('ClickHouse', 'ClickHouses')─┐
│                                        0.1 │
└────────────────────────────────────────────┘

```

## ngramDistanceCaseInsensitive[​](#ngramDistanceCaseInsensitive "Direct link to ngramDistanceCaseInsensitive")


Introduced in: v20\.1\.0


Provides a case\-insensitive variant of [`ngramDistance`](#ngramDistance).
Calculates the 4\-gram distance between two strings, ignoring case.
The smaller the returned value, the more similar the strings are.


**Syntax**



```
ngramDistanceCaseInsensitive(haystack, needle)

```

**Arguments**


- `haystack` — First comparison string. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Second comparison string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Float32 number between `0` and `1`. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Case\-insensitive 4\-gram distance**



```
SELECT ngramDistanceCaseInsensitive('ClickHouse','clickhouse')

```


```
┌─ngramDistanceCaseInsensitive('ClickHouse','clickhouse')─┐
│                                                       0 │
└─────────────────────────────────────────────────────────┘

```

## ngramDistanceCaseInsensitiveUTF8[​](#ngramDistanceCaseInsensitiveUTF8 "Direct link to ngramDistanceCaseInsensitiveUTF8")


Introduced in: v20\.1\.0


Provides a case\-insensitive UTF\-8 variant of [`ngramDistance`](#ngramDistance).
Assumes that `needle` and `haystack` strings are UTF\-8 encoded strings and ignores case.
Calculates the 3\-gram distance between two UTF\-8 strings, ignoring case.
The smaller the returned value, the more similar the strings are.


**Syntax**



```
ngramDistanceCaseInsensitiveUTF8(haystack, needle)

```

**Arguments**


- `haystack` — First UTF\-8 encoded comparison string. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Second UTF\-8 encoded comparison string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Float32 number between `0` and `1`. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**Case\-insensitive UTF\-8 3\-gram distance**



```
SELECT ngramDistanceCaseInsensitiveUTF8('abcde','CDE')

```


```
┌─ngramDistanceCaseInsensitiveUTF8('abcde','CDE')─┐
│                                             0.5 │
└─────────────────────────────────────────────────┘

```

## ngramDistanceUTF8[​](#ngramDistanceUTF8 "Direct link to ngramDistanceUTF8")


Introduced in: v20\.1\.0


Provides a UTF\-8 variant of [`ngramDistance`](#ngramDistance).
Assumes that `needle` and `haystack` strings are UTF\-8 encoded strings.
Calculates the 3\-gram distance between two UTF\-8 strings.
The smaller the returned value, the more similar the strings are.


**Syntax**



```
ngramDistanceUTF8(haystack, needle)

```

**Arguments**


- `haystack` — First UTF\-8 encoded comparison string. [`String`](/docs/sql-reference/data-types/string)
- `needle` — Second UTF\-8 encoded comparison string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Float32 number between `0` and `1`. [`Float32`](/docs/sql-reference/data-types/float)


**Examples**


**UTF\-8 3\-gram distance**



```
SELECT ngramDistanceUTF8('abcde','cde')

```


```
┌─ngramDistanceUTF8('abcde','cde')─┐
│                               0.5 │
└───────────────────────────────────┘

```

## ngramSearch[​](#ngramSearch "Direct link to ngramSearch")


Introduced in: v20\.1\.0


Checks if the 4\-gram distance between two strings is less than or equal to a given threshold.


For case\-insensitive search or/and in UTF8 format use functions `ngramSearchCaseInsensitive`, `ngramSearchUTF8`, `ngramSearchCaseInsensitiveUTF8`.


**Syntax**



```
ngramSearch(haystack, needle)

```

**Arguments**


- `haystack` — String for comparison. [`String`](/docs/sql-reference/data-types/string)
- `needle` — String for comparison. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the 4\-gram distance between the strings is less than or equal to a threshold (`1.0` by default), `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Search using 4\-grams**



```
SELECT ngramSearch('ClickHouse', 'Click')

```


```
┌─ngramSearch('ClickHouse', 'Click')─┐
│                                  1 │
└────────────────────────────────────┘

```

## ngramSearchCaseInsensitive[​](#ngramSearchCaseInsensitive "Direct link to ngramSearchCaseInsensitive")


Introduced in: v20\.1\.0


Provides a case\-insensitive variant of [`ngramSearch`](#ngramSearch).
Calculates the non\-symmetric difference between a needle string and a haystack string, i.e. the number of n\-grams from the needle minus the common number of n\-grams normalized by the number of needle n\-grams.
Checks if the 4\-gram distance between two strings is less than or equal to a given threshold, ignoring case.


**Syntax**



```
ngramSearchCaseInsensitive(haystack, needle)

```

**Arguments**


- `haystack` — String for comparison. [`String`](/docs/sql-reference/data-types/string)
- `needle` — String for comparison. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the 4\-gram distance between the strings is less than or equal to a threshold (`1.0` by default), `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case\-insensitive search using 4\-grams**



```
SELECT ngramSearchCaseInsensitive('Hello World','hello')

```


```
┌─ngramSearchCaseInsensitive('Hello World','hello')─┐
│                                                  1 │
└────────────────────────────────────────────────────┘

```

## ngramSearchCaseInsensitiveUTF8[​](#ngramSearchCaseInsensitiveUTF8 "Direct link to ngramSearchCaseInsensitiveUTF8")


Introduced in: v20\.1\.0


Provides a case\-insensitive UTF\-8 variant of [`ngramSearch`](#ngramSearch).
Assumes `haystack` and `needle` to be UTF\-8 strings and ignores case.
Checks if the 3\-gram distance between two UTF\-8 strings is less than or equal to a given threshold, ignoring case.


**Syntax**



```
ngramSearchCaseInsensitiveUTF8(haystack, needle)

```

**Arguments**


- `haystack` — UTF\-8 string for comparison. [`String`](/docs/sql-reference/data-types/string)
- `needle` — UTF\-8 string for comparison. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the 3\-gram distance between the strings is less than or equal to a threshold (`1.0` by default), `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case\-insensitive UTF\-8 search using 3\-grams**



```
SELECT ngramSearchCaseInsensitiveUTF8('абвГДЕёжз', 'АбвгдЕЁжз')

```


```
┌─ngramSearchCaseInsensitiveUTF8('абвГДЕёжз', 'АбвгдЕЁжз')─┐
│                                                        1 │
└──────────────────────────────────────────────────────────┘

```

## ngramSearchUTF8[​](#ngramSearchUTF8 "Direct link to ngramSearchUTF8")


Introduced in: v20\.1\.0


Provides a UTF\-8 variant of `ngramSearch`.
Assumes `haystack` and `needle` to be UTF\-8 strings.
Checks if the 3\-gram distance between two UTF\-8 strings is less than or equal to a given threshold.


**Syntax**



```
ngramSearchUTF8(haystack, needle)

```

**Arguments**


- `haystack` — UTF\-8 string for comparison. [`String`](/docs/sql-reference/data-types/string)
- `needle` — UTF\-8 string for comparison. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the 3\-gram distance between the strings is less than or equal to a threshold (`1.0` by default), `0` otherwise. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**UTF\-8 search using 3\-grams**



```
SELECT ngramSearchUTF8('абвгдеёжз', 'гдеёзд')

```


```
┌─ngramSearchUTF8('абвгдеёжз', 'гдеёзд')─┐
│                                      1 │
└────────────────────────────────────────┘

```

## notILike[​](#notILike "Direct link to notILike")


Introduced in: v20\.6\.0


Checks whether a string does not match a pattern, case\-insensitive. The pattern can contain special characters `%` and `_` for SQL LIKE matching.


**Syntax**



```
notILike(haystack, pattern)

```

**Arguments**


- `haystack` — The input string to search in. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `pattern` — The SQL LIKE pattern to match against. `%` matches any number of characters (including zero), `_` matches exactly one character. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the string does not match the pattern (case\-insensitive), otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT notILike('ClickHouse', '%house%');

```


```
┌─notILike('Cl⋯ '%house%')─┐
│                        0 │
└──────────────────────────┘

```

## notLike[​](#notLike "Direct link to notLike")


Introduced in: v1\.1\.0


Similar to [`like`](#like) but negates the result.


**Syntax**



```
notLike(haystack, pattern)
-- haystack NOT LIKE pattern

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `pattern` — LIKE pattern to match against. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if the string does not match the `LIKE` pattern, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT notLike('ClickHouse', '%House%');

```


```
┌─notLike('Cli⋯ '%House%')─┐
│                        0 │
└──────────────────────────┘

```

**Non\-matching pattern**



```
SELECT notLike('ClickHouse', '%SQL%');

```


```
┌─notLike('Cli⋯', '%SQL%')─┐
│                        1 │
└──────────────────────────┘

```

## position[​](#position "Direct link to position")


Introduced in: v1\.1\.0


Returns the position (in bytes, starting at 1\) of a substring `needle` in a string `haystack`.


If substring `needle` is empty, these rules apply:


- if no `start_pos` was specified: return `1`
- if `start_pos = 0`: return `1`
- if `start_pos >= 1` and `start_pos <= length(haystack) + 1`: return `start_pos`
- otherwise: return `0`


The same rules also apply to functions [`locate`](#locate), [`positionCaseInsensitive`](#positionCaseInsensitive), [`positionUTF8`](#positionUTF8) and [`positionCaseInsensitiveUTF8`](#positionCaseInsensitiveUTF8).


**Syntax**



```
position(haystack, needle[, start_pos])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `start_pos` — Position (1\-based) in `haystack` at which the search starts. Optional. [`UInt`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns starting position in bytes and counting from 1, if the substring was found, otherwise `0`, if the substring was not found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT position('Hello, world!', '!')

```


```
┌─position('Hello, world!', '!')─┐
│                             13 │
└────────────────────────────────┘

```

**With start\_pos argument**



```
SELECT position('Hello, world!', 'o', 1), position('Hello, world!', 'o', 7)

```


```
┌─position('Hello, world!', 'o', 1)─┬─position('Hello, world!', 'o', 7)─┐
│                                 5 │                                 9 │
└───────────────────────────────────┴───────────────────────────────────┘

```

**Needle IN haystack syntax**



```
SELECT 6 = position('/' IN s) FROM (SELECT 'Hello/World' AS s)

```


```
┌─equals(6, position(s, '/'))─┐
│                           1 │
└─────────────────────────────┘

```

**Empty needle substring**



```
SELECT position('abc', ''), position('abc', '', 0), position('abc', '', 1), position('abc', '', 2), position('abc', '', 3), position('abc', '', 4), position('abc', '', 5)

```


```
┌─position('abc', '')─┬─position('abc', '', 0)─┬─position('abc', '', 1)─┬─position('abc', '', 2)─┬─position('abc', '', 3)─┬─position('abc', '', 4)─┬─position('abc', '', 5)─┐
│                   1 │                      1 │                      1 │                      2 │                      3 │                      4 │                      0 │
└─────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┴────────────────────────┘

```

## positionCaseInsensitive[​](#positionCaseInsensitive "Direct link to positionCaseInsensitive")


Introduced in: v1\.1\.0


Like [`position`](#position) but case\-insensitive.


**Syntax**



```
positionCaseInsensitive(haystack, needle[, start_pos])

```

**Aliases**: `instr`


**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `start_pos` — Optional. Position (1\-based) in `haystack` at which the search starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns starting position in bytes and counting from 1, if the substring was found, otherwise `0`, if the substring was not found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case insensitive search**



```
SELECT positionCaseInsensitive('Hello, world!', 'hello')

```


```
┌─positionCaseInsensitive('Hello, world!', 'hello')─┐
│                                                 1 │
└───────────────────────────────────────────────────┘

```

## positionCaseInsensitiveUTF8[​](#positionCaseInsensitiveUTF8 "Direct link to positionCaseInsensitiveUTF8")


Introduced in: v1\.1\.0


Like [`positionUTF8`](#positionUTF8) but searches case\-insensitively.


**Syntax**



```
positionCaseInsensitiveUTF8(haystack, needle[, start_pos])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `start_pos` — Optional. Position (1\-based) in `haystack` at which the search starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns starting position in bytes and counting from 1, if the substring was found, otherwise `0`, if the substring was not found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Case insensitive UTF\-8 search**



```
SELECT positionCaseInsensitiveUTF8('Привет мир', 'МИР')

```


```
┌─positionCaseInsensitiveUTF8('Привет мир', 'МИР')─┐
│                                                8 │
└──────────────────────────────────────────────────┘

```

## positionUTF8[​](#positionUTF8 "Direct link to positionUTF8")


Introduced in: v1\.1\.0


Like [`position`](#position) but assumes `haystack` and `needle` are UTF\-8 encoded strings.


**Syntax**



```
positionUTF8(haystack, needle[, start_pos])

```

**Arguments**


- `haystack` — String in which the search is performed. [`String`](/docs/sql-reference/data-types/string) or [`Enum`](/docs/sql-reference/data-types/enum)
- `needle` — Substring to be searched. [`String`](/docs/sql-reference/data-types/string)
- `start_pos` — Optional. Position (1\-based) in `haystack` at which the search starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns starting position in bytes and counting from 1, if the substring was found, otherwise `0`, if the substring was not found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**UTF\-8 character counting**



```
SELECT positionUTF8('Motörhead', 'r')

```


```
┌─position('Motörhead', 'r')─┐
│                          5 │
└────────────────────────────┘

```
[PreviousString replacement](/docs/sql-reference/functions/string-replace-functions)[NextTimeSeries](/docs/sql-reference/functions/time-series-functions)- [countMatches](#countMatches)- [countMatchesCaseInsensitive](#countMatchesCaseInsensitive)- [countSubstrings](#countSubstrings)- [countSubstringsCaseInsensitive](#countSubstringsCaseInsensitive)- [countSubstringsCaseInsensitiveUTF8](#countSubstringsCaseInsensitiveUTF8)- [extract](#extract)- [extractAll](#extractAll)- [extractAllGroupsHorizontal](#extractAllGroupsHorizontal)- [extractGroups](#extractGroups)- [hasAllTokens](#hasAllTokens)- [hasAnyTokens](#hasAnyTokens)- [hasPhrase](#hasPhrase)- [hasSubsequence](#hasSubsequence)- [hasSubsequenceCaseInsensitive](#hasSubsequenceCaseInsensitive)- [hasSubsequenceCaseInsensitiveUTF8](#hasSubsequenceCaseInsensitiveUTF8)- [hasSubsequenceUTF8](#hasSubsequenceUTF8)- [hasToken](#hasToken)- [hasTokenCaseInsensitive](#hasTokenCaseInsensitive)- [hasTokenCaseInsensitiveOrNull](#hasTokenCaseInsensitiveOrNull)- [hasTokenOrNull](#hasTokenOrNull)- [highlight](#highlight)- [ilike](#ilike)- [like](#like)- [locate](#locate)- [match](#match)- [multiFuzzyMatchAllIndices](#multiFuzzyMatchAllIndices)- [multiFuzzyMatchAny](#multiFuzzyMatchAny)- [multiFuzzyMatchAnyIndex](#multiFuzzyMatchAnyIndex)- [multiMatchAllIndices](#multiMatchAllIndices)- [multiMatchAny](#multiMatchAny)- [multiMatchAnyIndex](#multiMatchAnyIndex)- [multiSearchAllPositions](#multiSearchAllPositions)- [multiSearchAllPositionsCaseInsensitive](#multiSearchAllPositionsCaseInsensitive)- [multiSearchAllPositionsCaseInsensitiveUTF8](#multiSearchAllPositionsCaseInsensitiveUTF8)- [multiSearchAllPositionsUTF8](#multiSearchAllPositionsUTF8)- [multiSearchAny](#multiSearchAny)- [multiSearchAnyCaseInsensitive](#multiSearchAnyCaseInsensitive)- [multiSearchAnyCaseInsensitiveUTF8](#multiSearchAnyCaseInsensitiveUTF8)- [multiSearchAnyUTF8](#multiSearchAnyUTF8)- [multiSearchFirstIndex](#multiSearchFirstIndex)- [multiSearchFirstIndexCaseInsensitive](#multiSearchFirstIndexCaseInsensitive)- [multiSearchFirstIndexCaseInsensitiveUTF8](#multiSearchFirstIndexCaseInsensitiveUTF8)- [multiSearchFirstIndexUTF8](#multiSearchFirstIndexUTF8)- [multiSearchFirstPosition](#multiSearchFirstPosition)- [multiSearchFirstPositionCaseInsensitive](#multiSearchFirstPositionCaseInsensitive)- [multiSearchFirstPositionCaseInsensitiveUTF8](#multiSearchFirstPositionCaseInsensitiveUTF8)- [multiSearchFirstPositionUTF8](#multiSearchFirstPositionUTF8)- [ngramDistance](#ngramDistance)- [ngramDistanceCaseInsensitive](#ngramDistanceCaseInsensitive)- [ngramDistanceCaseInsensitiveUTF8](#ngramDistanceCaseInsensitiveUTF8)- [ngramDistanceUTF8](#ngramDistanceUTF8)- [ngramSearch](#ngramSearch)- [ngramSearchCaseInsensitive](#ngramSearchCaseInsensitive)- [ngramSearchCaseInsensitiveUTF8](#ngramSearchCaseInsensitiveUTF8)- [ngramSearchUTF8](#ngramSearchUTF8)- [notILike](#notILike)- [notLike](#notLike)- [position](#position)- [positionCaseInsensitive](#positionCaseInsensitive)- [positionCaseInsensitiveUTF8](#positionCaseInsensitiveUTF8)- [positionUTF8](#positionUTF8)
Was this page helpful?
