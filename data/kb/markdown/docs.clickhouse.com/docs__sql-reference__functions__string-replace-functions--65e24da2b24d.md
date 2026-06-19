# Functions for string replacement \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- String replacement
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/string-replace-functions.md)# Functions for string replacement

[General strings functions](/docs/sql-reference/functions/string-functions) and [functions for searching in strings](/docs/sql-reference/functions/string-search-functions) are described separately.


NoteThe documentation below is generated from the `system.functions` system table.


## format[​](#format "Direct link to format")


Introduced in: v20\.1\.0


Format the `pattern` string with the values (strings, integers, etc.) listed in the arguments, similar to formatting in Python.
The pattern string can contain replacement fields surrounded by curly braces `{}`.
Anything not contained in braces is considered literal text and copied verbatim into the output.
Literal brace character can be escaped by two braces: `{{` and `}}`.
Field names can be numbers (starting from zero) or empty (then they are implicitly given monotonically increasing numbers).


**Syntax**



```
format(pattern, s0[, s1, ...])

```

**Arguments**


- `pattern` — The format string containing placeholders. [`String`](/docs/sql-reference/data-types/string)
- `s0[, s1, ...]` — One or more values to substitute into the pattern. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns a formatted string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Numbered placeholders**



```
SELECT format('{1} {0} {1}', 'World', 'Hello')

```


```
┌─format('{1} {0} {1}', 'World', 'Hello')─┐
│ Hello World Hello                       │
└─────────────────────────────────────────┘

```

**Implicit numbering**



```
SELECT format('{} {}', 'Hello', 'World')

```


```
┌─format('{} {}', 'Hello', 'World')─┐
│ Hello World                       │
└───────────────────────────────────┘

```

## overlay[​](#overlay "Direct link to overlay")


Introduced in: v24\.9\.0


Replaces part of the string `input` with another string `replace`, starting at the 1\-based index `offset`.


**Syntax**



```
overlay(s, replace, offset[, length])

```

**Arguments**


- `s` — The input string. [`String`](/docs/sql-reference/data-types/string)
- `replace` — The replacement string [`const String`](/docs/sql-reference/data-types/string)
- `offset` — An integer type `Int` (1\-based). If `offset` is negative, it is counted from the end of the string `s`. [`Int`](/docs/sql-reference/data-types/int-uint)
- `length` — Optional. An integer type `Int`. `length` specifies the length of the snippet within the input string `s` to be replaced. If `length` is not specified, the number of bytes removed from `s` equals the length of `replace`; otherwise `length` bytes are removed. [`Int`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a string with replacement. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic replacement**



```
SELECT overlay('My father is from Mexico.', 'mother', 4) AS res;

```


```
┌─res──────────────────────┐
│ My mother is from Mexico.│
└──────────────────────────┘

```

**Replacement with length**



```
SELECT overlay('My father is from Mexico.', 'dad', 4, 6) AS res;

```


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


Introduced in: v20\.1\.0


Adds a backslash before these characters with special meaning in regular expressions: `\0`, `\\`, `|`, `(`, `)`, `^`, `$`, `.`, `[`, `]`, `?`, `*`, `+`, `{`, `:`, `-`.
This implementation slightly differs from re2::RE2::QuoteMeta.
It escapes zero byte as `\0` instead of `\x00` and it escapes only required characters.


**Syntax**



```
regexpQuoteMeta(s)

```

**Arguments**


- `s` — The input string containing characters to be escaped for regex. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with regex special characters escaped. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Escape regex special characters**



```
SELECT regexpQuoteMeta('Hello. [World]? (Yes)*') AS res

```


```
┌─res───────────────────────────┐
│ Hello\. \[World\]\? \(Yes\)\* │
└───────────────────────────────┘

```

## replaceAll[​](#replaceAll "Direct link to replaceAll")


Introduced in: v1\.1\.0


Replaces all occurrences of the substring `pattern` in `haystack` by the `replacement` string.


**Syntax**



```
replaceAll(haystack, pattern, replacement)

```

**Aliases**: `replace`


**Arguments**


- `haystack` — The input string to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — The substring to find and replace. [`const String`](/docs/sql-reference/data-types/string)
- `replacement` — The string to replace the pattern with. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with all occurrences of pattern replaced. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Replace all occurrences**



```
SELECT replaceAll('Hello, Hello world', 'Hello', 'Hi') AS res;

```


```
┌─res──────────┐
│ Hi, Hi world │
└──────────────┘

```

## replaceOne[​](#replaceOne "Direct link to replaceOne")


Introduced in: v1\.1\.0


Replaces the first occurrence of the substring `pattern` in `haystack` by the `replacement` string.


**Syntax**



```
replaceOne(haystack, pattern, replacement)

```

**Arguments**


- `haystack` — The input string to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — The substring to find and replace. [`const String`](/docs/sql-reference/data-types/string)
- `replacement` — The string to replace the pattern with. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with the first occurrence of pattern replaced. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Replace first occurrence**



```
SELECT replaceOne('Hello, Hello world', 'Hello', 'Hi') AS res;

```


```
┌─res─────────────┐
│ Hi, Hello world │
└─────────────────┘

```

## replaceRegexpAll[​](#replaceRegexpAll "Direct link to replaceRegexpAll")


Introduced in: v1\.1\.0


Like `replaceRegexpOne` but replaces all occurrences of the pattern.
As an exception, if a regular expression worked on an empty substring, the replacement is not made more than once.


**Syntax**



```
replaceRegexpAll(haystack, pattern, replacement)

```

**Aliases**: `REGEXP_REPLACE`


**Arguments**


- `haystack` — The input string to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — The regular expression pattern to find. [`const String`](/docs/sql-reference/data-types/string)
- `replacement` — The string to replace the pattern with, may contain substitutions. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with all regex matches replaced. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Replace all characters with doubled version**



```
SELECT replaceRegexpAll('Hello123', '.', '\\\\0\\\\0') AS res

```


```
┌─res──────────────────┐
│ HHeelllloo112233     │
└──────────────────────┘

```

**Empty substring replacement example**



```
SELECT replaceRegexpAll('Hello, World!', '^', 'here: ') AS res

```


```
┌─res─────────────────┐
│ here: Hello, World! │
└─────────────────────┘

```

## replaceRegexpOne[​](#replaceRegexpOne "Direct link to replaceRegexpOne")


Introduced in: v1\.1\.0


Replaces the first occurrence of the substring matching the regular expression `pattern` (in re2 syntax) in `haystack` by the `replacement` string.
`replacement` can contain substitutions `\0-\9`.
Substitutions `\1-\9` correspond to the 1st to 9th capturing group (submatch), substitution `\0` corresponds to the entire match.
To use a verbatim `\` character in the `pattern` or `replacement` strings, escape it using `\`.
Also keep in mind that string literals require extra escaping.


**Syntax**



```
replaceRegexpOne(haystack, pattern, replacement)

```

**Arguments**


- `haystack` — The input string to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — The regular expression pattern to find. [`const String`](/docs/sql-reference/data-types/string)
- `replacement` — The string to replace the pattern with, may contain substitutions. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with the first regex match replaced. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Converting ISO dates to American format**



```
SELECT DISTINCT
    EventDate,
    replaceRegexpOne(toString(EventDate), '(\\d{4})-(\\d{2})-(\\d{2})', '\\2/\\3/\\1') AS res
FROM test.hits
LIMIT 7
FORMAT TabSeparated

```


```
2014-03-17      03/17/2014
2014-03-18      03/18/2014
2014-03-19      03/19/2014
2014-03-20      03/20/2014
2014-03-21      03/21/2014
2014-03-22      03/22/2014
2014-03-23      03/23/2014

```

**Copying a string ten times**



```
SELECT replaceRegexpOne('Hello, World!', '.*', '\\\\0\\\\0\\\\0\\\\0\\\\0\\\\0\\\\0\\\\0\\\\0\\\\0') AS res

```


```
┌─res────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World!Hello, World! │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

```

## translate[​](#translate "Direct link to translate")


Introduced in: v22\.7\.0


Replaces characters in the string `s` using a one\-to\-one character mapping defined by `from` and `to` strings.
`from` and `to` must be constant ASCII strings.
If `from` and `to` have equal sizes, each occurrence of the first character of `first` in `s` is replaced by the first character of `to`, the second character of `first` in `s` is replaced by the second character of `to`, etc.
If `from` contains more characters than `to`, all occurrences of the characters at the end of `from` that have no corresponding character in `to` are deleted from `s`.
Non\-ASCII characters in `s` are not modified by the function.


**Syntax**



```
translate(s, from, to)

```

**Arguments**


- `s` — The input string to translate. [`String`](/docs/sql-reference/data-types/string)
- `from` — A constant ASCII string containing characters to replace. [`const String`](/docs/sql-reference/data-types/string)
- `to` — A constant ASCII string containing replacement characters. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with character translations applied. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Character mapping**



```
SELECT translate('Hello, World!', 'delor', 'DELOR') AS res

```


```
┌─res───────────┐
│ HELLO, WORLD! │
└───────────────┘

```

**Different lengths**



```
SELECT translate('clickhouse', 'clickhouse', 'CLICK') AS res

```


```
┌─res───┐
│ CLICK │
└───────┘

```

## translateUTF8[​](#translateUTF8 "Direct link to translateUTF8")


Introduced in: v22\.7\.0


Like [`translate`](#translate) but assumes `s`, `from` and `to` are UTF\-8 encoded strings.


**Syntax**



```
translateUTF8(s, from, to)

```

**Arguments**


- `s` — UTF\-8 input string to translate. [`String`](/docs/sql-reference/data-types/string)
- `from` — A constant UTF\-8 string containing characters to replace. [`const String`](/docs/sql-reference/data-types/string)
- `to` — A constant UTF\-8 string containing replacement characters. [`const String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a `String` data type value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**UTF\-8 character translation**



```
SELECT translateUTF8('Münchener Straße', 'üß', 'us') AS res;

```


```
┌─res──────────────┐
│ Munchener Strase │
└──────────────────┘

```
[PreviousString](/docs/sql-reference/functions/string-functions)[NextString search](/docs/sql-reference/functions/string-search-functions)- [format](#format)- [overlay](#overlay)- [overlayUTF8](#overlayUTF8)- [printf](#printf)- [regexpQuoteMeta](#regexpQuoteMeta)- [replaceAll](#replaceAll)- [replaceOne](#replaceOne)- [replaceRegexpAll](#replaceRegexpAll)- [replaceRegexpOne](#replaceRegexpOne)- [translate](#translate)- [translateUTF8](#translateUTF8)
Was this page helpful?
