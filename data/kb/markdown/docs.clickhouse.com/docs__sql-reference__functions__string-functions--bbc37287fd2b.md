# Functions for working with strings \| ClickHouse Docs


- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- String
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/string-functions.md)# Functions for working with strings


Functions for [searching](/docs/sql-reference/functions/string-search-functions) in strings and for [replacing](/docs/sql-reference/functions/string-replace-functions) in strings are described separately.


NoteThe documentation below is generated from the `system.functions` system table.


## CRC32[​](#CRC32 "Direct link to CRC32")


Introduced in: v20\.1\.0


Calculates the CRC32 checksum of a string using the CRC\-32\-IEEE 802\.3 polynomial and initial value `0xffffffff` (zlib implementation).


**Syntax**



```
CRC32(s)

```

**Arguments**


- `s` — String to calculate CRC32 for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the CRC32 checksum of the string. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT CRC32('ClickHouse')

```


```
┌─CRC32('ClickHouse')─┐
│          1538217360 │
└─────────────────────┘

```

## CRC32IEEE[​](#CRC32IEEE "Direct link to CRC32IEEE")


Introduced in: v20\.1\.0


Calculates the CRC32 checksum of a string using the CRC\-32\-IEEE 802\.3 polynomial.


**Syntax**



```
CRC32IEEE(s)

```

**Arguments**


- `s` — String to calculate CRC32 for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the CRC32 checksum of the string. [`UInt32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT CRC32IEEE('ClickHouse');

```


```
┌─CRC32IEEE('ClickHouse')─┐
│              3089448422 │
└─────────────────────────┘

```

## CRC64[​](#CRC64 "Direct link to CRC64")


Introduced in: v20\.1\.0


Calculates the CRC64 checksum of a string using the CRC\-64\-ECMA polynomial.


**Syntax**



```
CRC64(s)

```

**Arguments**


- `s` — String to calculate CRC64 for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the CRC64 checksum of the string. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT CRC64('ClickHouse');

```


```
┌──CRC64('ClickHouse')─┐
│ 12126588151325169346 │
└──────────────────────┘

```

## appendTrailingCharIfAbsent[​](#appendTrailingCharIfAbsent "Direct link to appendTrailingCharIfAbsent")


Introduced in: v1\.1\.0


Appends character `c` to string `s` if `s` is non\-empty and does not end with character `c`.


**Syntax**



```
appendTrailingCharIfAbsent(s, c)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)
- `c` — Character to append if absent. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns string `s` with character `c` appended if `s` does not end with `c`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT appendTrailingCharIfAbsent('https://example.com', '/');

```


```
┌─appendTraili⋯.com', '/')─┐
│ https://example.com/     │
└──────────────────────────┘

```

## ascii[​](#ascii "Direct link to ascii")


Introduced in: v22\.11\.0


Returns the ASCII code point of the first character of string `s` as an `Int32`.


**Syntax**



```
ascii(s)

```

**Arguments**


- `s` — String input. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the ASCII code point of the first character. If `s` is empty, the result is `0`. If the first character is not an ASCII character or not part of the Latin\-1 supplement range of UTF\-16, the result is undefined. [`Int32`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT ascii('234')

```


```
┌─ascii('234')─┐
│           50 │
└──────────────┘

```

## base32Decode[​](#base32Decode "Direct link to base32Decode")


Introduced in: v25\.6\.0


Decodes a [Base32](https://datatracker.ietf.org/doc/html/rfc4648#section-6) (RFC 4648\) string.
If the string is not valid Base32\-encoded, an exception is thrown.


**Syntax**



```
base32Decode(encoded)

```

**Arguments**


- `encoded` — String column or constant. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base32Decode('IVXGG33EMVSA====');

```


```
┌─base32Decode('IVXGG33EMVSA====')─┐
│ Encoded                          │
└──────────────────────────────────┘

```

## base32Encode[​](#base32Encode "Direct link to base32Encode")


Introduced in: v25\.6\.0


Encodes a string using [Base32](https://datatracker.ietf.org/doc/html/rfc4648#section-6).


**Syntax**



```
base32Encode(plaintext)

```

**Arguments**


- `plaintext` — Plaintext to encode. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the encoded value of the argument. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Examples**


**Usage example**



```
SELECT base32Encode('Encoded')

```


```
┌─base32Encode('Encoded')─┐
│ IVXGG33EMVSA====        │
└─────────────────────────┘

```

## base58Decode[​](#base58Decode "Direct link to base58Decode")


Introduced in: v22\.7\.0


Decodes a [Base58](https://datatracker.ietf.org/doc/html/draft-msporny-base58-03#section-3) string.
If the string is not valid Base58\-encoded, an exception is thrown.
An optional second argument `expected_size` can be provided to select an optimized fixed\-size decoder.
Currently supported values are 32 and 64\. For other values, the generic decoder is used.
When the optimized decoder is selected but the input cannot be decoded to exactly that many bytes,
the function throws an exception (or returns an empty string for `tryBase58Decode`).


**Syntax**



```
base58Decode(encoded[, expected_size])

```

**Arguments**


- `encoded` — String column or constant to decode. [`String`](/docs/sql-reference/data-types/string)
- `expected_size` — Optional. Expected decoded size in bytes. When 32 or 64, an optimized decoder is used; for other values, the generic decoder is used. [`UInt8, UInt16, UInt32, or UInt64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base58Decode('JxF12TrwUP45BMd');

```


```
┌─base58Decode⋯rwUP45BMd')─┐
│ Hello World              │
└──────────────────────────┘

```

## base58Encode[​](#base58Encode "Direct link to base58Encode")


Introduced in: v22\.7\.0


Encodes a string using [Base58](https://tools.ietf.org/id/draft-msporny-base58-01.html) encoding.


**Syntax**



```
base58Encode(plaintext)

```

**Arguments**


- `plaintext` — Plaintext to encode. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the encoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base58Encode('ClickHouse');

```


```
┌─base58Encode('ClickHouse')─┐
│ 4nhk8K7GHXf6zx             │
└────────────────────────────┘

```

## base64Decode[​](#base64Decode "Direct link to base64Decode")


Introduced in: v18\.16\.0


Decodes a string from [Base64](https://en.wikipedia.org/wiki/Base64) representation, according to RFC 4648\.
Throws an exception in case of error.


**Syntax**



```
base64Decode(encoded)

```

**Aliases**: `FROM_BASE64`


**Arguments**


- `encoded` — String column or constant to decode. If the string is not valid Base64\-encoded, an exception is thrown. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the decoded string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base64Decode('Y2xpY2tob3VzZQ==')

```


```
┌─base64Decode('Y2xpY2tob3VzZQ==')─┐
│ clickhouse                       │
└──────────────────────────────────┘

```

## base64Encode[​](#base64Encode "Direct link to base64Encode")


Introduced in: v18\.16\.0


Encodes a string using [Base64](https://en.wikipedia.org/wiki/Base64) representation, according to RFC 4648\.


**Syntax**



```
base64Encode(plaintext)

```

**Aliases**: `TO_BASE64`


**Arguments**


- `plaintext` — Plaintext column or constant to decode. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the encoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base64Encode('clickhouse')

```


```
┌─base64Encode('clickhouse')─┐
│ Y2xpY2tob3VzZQ==           │
└────────────────────────────┘

```

## base64URLDecode[​](#base64URLDecode "Direct link to base64URLDecode")


Introduced in: v24\.6\.0


Decodes a string from [Base64](https://en.wikipedia.org/wiki/Base64) representation using URL\-safe alphabet, according to RFC 4648\.
Throws an exception in case of error.


**Syntax**



```
base64URLDecode(encoded)

```

**Arguments**


- `encoded` — String column or constant to encode. If the string is not valid Base64\-encoded, an exception is thrown. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')

```


```
┌─base64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')─┐
│ https://clickhouse.com                            │
└───────────────────────────────────────────────────┘

```

## base64URLEncode[​](#base64URLEncode "Direct link to base64URLEncode")


Introduced in: v18\.16\.0


Encodes a string using [Base64](https://datatracker.ietf.org/doc/html/rfc4648#section-4) (RFC 4648\) representation using URL\-safe alphabet.


**Syntax**



```
base64URLEncode(plaintext)

```

**Arguments**


- `plaintext` — Plaintext column or constant to encode. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the encoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT base64URLEncode('https://clickhouse.com')

```


```
┌─base64URLEncode('https://clickhouse.com')─┐
│ aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ            │
└───────────────────────────────────────────┘

```

## basename[​](#basename "Direct link to basename")


Introduced in: v20\.1\.0


Extracts the tail of a string following its last slash or backslash.
This function is often used to extract the filename from a path.


**Syntax**



```
basename(expr)

```

**Arguments**


- `expr` — A string expression. Backslashes must be escaped. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the tail of the input string after its last slash or backslash. If the input string ends with a slash or backslash, the function returns an empty string. Returns the original string if there are no slashes or backslashes. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Extract filename from Unix path**



```
SELECT 'some/long/path/to/file' AS a, basename(a)

```


```
┌─a──────────────────────┬─basename('some/long/path/to/file')─┐
│ some/long/path/to/file │ file                               │
└────────────────────────┴────────────────────────────────────┘

```

**Extract filename from Windows path**



```
SELECT 'some\\long\\path\\to\\file' AS a, basename(a)

```


```
┌─a──────────────────────┬─basename('some\\long\\path\\to\\file')─┐
│ some\long\path\to\file │ file                                   │
└────────────────────────┴────────────────────────────────────────┘

```

**String with no path separators**



```
SELECT 'some-file-name' AS a, basename(a)

```


```
┌─a──────────────┬─basename('some-file-name')─┐
│ some-file-name │ some-file-name             │
└────────────────┴────────────────────────────┘

```

## byteHammingDistance[​](#byteHammingDistance "Direct link to byteHammingDistance")


Introduced in: v23\.9\.0


Calculates the [hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) between two byte strings.


**Syntax**



```
byteHammingDistance(s1, s2)

```

**Aliases**: `mismatches`


**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Hamming distance between the two strings. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT byteHammingDistance('karolin', 'kathrin')

```


```
┌─byteHammingDistance('karolin', 'kathrin')─┐
│                                         3 │
└───────────────────────────────────────────┘

```

## caseFoldUTF8[​](#caseFoldUTF8 "Direct link to caseFoldUTF8")


Introduced in: v26\.3\.0


Applies Unicode case folding to a UTF\-8 string, converting it to a lowercase\-like normalized form suitable for case\-insensitive comparisons.


Applies standard Unicode case folding. Preserves compatibility characters that are not affected by case folding
(e.g. Roman numerals, circled numbers), but note that some ligatures like `ﬃ` are still decomposed because Unicode case folding itself expands them.


**Syntax**



```
caseFoldUTF8(str)

```

**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Case\-folded UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic case folding**



```
SELECT caseFoldUTF8('Straße')

```


```
┌─caseFoldUTF8('Straße')─┐
│ strasse                 │
└─────────────────────────┘

```

## compareSubstrings[​](#compareSubstrings "Direct link to compareSubstrings")


Introduced in: v25\.2\.0


Compares two strings lexicographically.


**Syntax**



```
compareSubstrings(s1, s2, s1_offset, s2_offset, num_bytes)

```

**Arguments**


- `s1` — The first string to compare. [`String`](/docs/sql-reference/data-types/string)
- `s2` — The second string to compare. [`String`](/docs/sql-reference/data-types/string)
- `s1_offset` — The position (zero\-based) in `s1` from which the comparison starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `s2_offset` — The position (zero\-based index) in `s2` from which the comparison starts. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `num_bytes` — The maximum number of bytes to compare in both strings. If `s1_offset` (or `s2_offset`) \+ `num_bytes` exceeds the end of an input string, `num_bytes` will be reduced accordingly. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns:


- `-1` if `s1`\[`s1_offset` : `s1_offset` \+ `num_bytes`] \< `s2`\[`s2_offset` : `s2_offset` \+ `num_bytes`].
- `0` if `s1`\[`s1_offset` : `s1_offset` \+ `num_bytes`] \= `s2`\[`s2_offset` : `s2_offset` \+ `num_bytes`].
- `1` if `s1`\[`s1_offset` : `s1_offset` \+ `num_bytes`] \> `s2`\[`s2_offset` : `s2_offset` \+ `num_bytes`].
[`Int8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT compareSubstrings('Saxony', 'Anglo-Saxon', 0, 6, 5) AS result

```


```
┌─result─┐
│      0 │
└────────┘

```

## concat[​](#concat "Direct link to concat")


Introduced in: v1\.1\.0


Concatenates the given arguments.


Arguments which are not of types [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) are converted to strings using their default serialization.
As this decreases performance, it is not recommended to use non\-String/FixedString arguments.


**Syntax**



```
concat([s1, s2, ...])

```

**Arguments**


- `s1, s2, ...` — Any number of values of arbitrary type. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the String created by concatenating the arguments. If any of arguments is `NULL`, the function returns `NULL`. If there are no arguments, it returns an empty string. [`Nullable(String)`](/docs/sql-reference/data-types/nullable)


**Examples**


**String concatenation**



```
SELECT concat('Hello, ', 'World!')

```


```
┌─concat('Hello, ', 'World!')─┐
│ Hello, World!               │
└─────────────────────────────┘

```

**Number concatenation**



```
SELECT concat(42, 144)

```


```
┌─concat(42, 144)─┐
│ 42144           │
└─────────────────┘

```

## concatAssumeInjective[​](#concatAssumeInjective "Direct link to concatAssumeInjective")


Introduced in: v1\.1\.0


Like [`concat`](#concat) but assumes that `concat(s1, s2, ...) → sn` is injective,
i.e, it returns different results for different arguments.


Can be used for optimization of `GROUP BY`.


**Syntax**



```
concatAssumeInjective([s1, s2, ...])

```

**Arguments**


- `s1, s2, ...` — Any number of values of arbitrary type. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the string created by concatenating the arguments. If any of argument values is `NULL`, the function returns `NULL`. If no arguments are passed, it returns an empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Group by optimization**



```
SELECT concat(key1, key2), sum(value) FROM key_val GROUP BY concatAssumeInjective(key1, key2)

```


```
┌─concat(key1, key2)─┬─sum(value)─┐
│ Hello, World!      │          3 │
│ Hello, World!      │          2 │
│ Hello, World       │          3 │
└────────────────────┴────────────┘

```

## concatWithSeparator[​](#concatWithSeparator "Direct link to concatWithSeparator")


Introduced in: v22\.12\.0


Concatenates the provided strings, separating them by the specified separator.


**Syntax**



```
concatWithSeparator(sep[, exp1, exp2, ...])

```

**Aliases**: `concat_ws`


**Arguments**


- `sep` — The separator to use. [`const String`](/docs/sql-reference/data-types/string) or [`const FixedString`](/docs/sql-reference/data-types/fixedstring)
- `exp1, exp2, ...` — Expression to be concatenated. Arguments which are not of type `String` or `FixedString` are converted to strings using their default serialization. As this decreases performance, it is not recommended to use non\-String/FixedString arguments. [`Any`](/docs/sql-reference/data-types)


**Returned value**


Returns the String created by concatenating the arguments. If any of the argument values is `NULL`, the function returns `NULL`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT concatWithSeparator('a', '1', '2', '3', '4')

```


```
┌─concatWithSeparator('a', '1', '2', '3', '4')─┐
│ 1a2a3a4                                      │
└──────────────────────────────────────────────┘

```

## concatWithSeparatorAssumeInjective[​](#concatWithSeparatorAssumeInjective "Direct link to concatWithSeparatorAssumeInjective")


Introduced in: v22\.12\.0


Like [`concatWithSeparator`](#concatWithSeparator) but assumes that `concatWithSeparator(sep[,exp1, exp2, ... ]) → result` is injective.
A function is called injective if it returns different results for different arguments.


Can be used for optimization of `GROUP BY`.


**Syntax**



```
concatWithSeparatorAssumeInjective(sep[, exp1, exp2, ... ])

```

**Arguments**


- `sep` — The separator to use. [`const String`](/docs/sql-reference/data-types/string) or [`const FixedString`](/docs/sql-reference/data-types/fixedstring)
- `exp1, exp2, ...` — Expression to be concatenated. Arguments which are not of type `String` or `FixedString` are converted to strings using their default serialization. As this decreases performance, it is not recommended to use non\-String/FixedString arguments. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)


**Returned value**


Returns the String created by concatenating the arguments. If any of the argument values is `NULL`, the function returns `NULL`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
CREATE TABLE user_data (
user_id UInt32,
first_name String,
last_name String,
score UInt32
)
ENGINE = MergeTree
ORDER BY tuple();

INSERT INTO user_data VALUES
(1, 'John', 'Doe', 100),
(2, 'Jane', 'Smith', 150),
(3, 'John', 'Wilson', 120),
(4, 'Jane', 'Smith', 90);

SELECT
    concatWithSeparatorAssumeInjective('-', first_name, last_name) as full_name,
    sum(score) as total_score
FROM user_data
GROUP BY concatWithSeparatorAssumeInjective('-', first_name, last_name);

```


```
┌─full_name───┬─total_score─┐
│ Jane-Smith  │         240 │
│ John-Doe    │         100 │
│ John-Wilson │         120 │
└─────────────┴─────────────┘

```

## conv[​](#conv "Direct link to conv")


Introduced in: v25\.10\.0


Converts numbers between different number bases.


The function converts a number from one base to another. It supports bases from 2 to 36\.
For bases higher than 10, letters A\-Z (case insensitive) are used to represent digits 10\-35\.


This function is compatible with MySQL's CONV() function.


**Syntax**



```
conv(number, from_base, to_base)

```

**Arguments**


- `number` — The number to convert. Can be a string or numeric type. \- `from_base` — The source base (2\-36\). Must be an integer. \- `to_base` — The target base (2\-36\). Must be an integer.


**Returned value**


String representation of the number in the target base.


**Examples**


**Convert decimal to binary**



```
SELECT conv('10', 10, 2)

```


```
1010

```

**Convert hexadecimal to decimal**



```
SELECT conv('FF', 16, 10)

```


```
255

```

**Convert with negative number**



```
SELECT conv('-1', 10, 16)

```


```
FFFFFFFFFFFFFFFF

```

**Convert binary to octal**



```
SELECT conv('1010', 2, 8)

```


```
12

```

## convertCharset[​](#convertCharset "Direct link to convertCharset")


Introduced in: v1\.1\.0


Returns string `s` converted from the encoding `from` to encoding `to`.


**Syntax**



```
convertCharset(s, from, to)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)
- `from` — Source character encoding. [`String`](/docs/sql-reference/data-types/string)
- `to` — Target character encoding. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns string `s` converted from encoding `from` to encoding `to`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT convertCharset('Café', 'UTF-8', 'ISO-8859-1');

```


```
┌─convertChars⋯SO-8859-1')─┐
│ Caf�                     │
└──────────────────────────┘

```

## damerauLevenshteinDistance[​](#damerauLevenshteinDistance "Direct link to damerauLevenshteinDistance")


Introduced in: v24\.1\.0


Calculates the [Damerau\-Levenshtein distance](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance) between two byte strings.


**Syntax**



```
damerauLevenshteinDistance(s1, s2)

```

**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Damerau\-Levenshtein distance between the two strings. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT damerauLevenshteinDistance('clickhouse', 'mouse')

```


```
┌─damerauLevenshteinDistance('clickhouse', 'mouse')─┐
│                                                 6 │
└───────────────────────────────────────────────────┘

```

## decodeHTMLComponent[​](#decodeHTMLComponent "Direct link to decodeHTMLComponent")


Introduced in: v23\.9\.0


Decodes HTML entities in a string to their corresponding characters.


**Syntax**



```
decodeHTMLComponent(s)

```

**Arguments**


- `s` — String containing HTML entities to decode. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the string with HTML entities decoded. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT decodeHTMLComponent('&lt;div&gt;Hello &amp; &quot;World&quot;&lt;/div&gt;')

```


```
┌─decodeHTMLComponent('&lt;div&gt;Hello &amp; &quot;World&quot;&lt;/div&gt;')─┐
│ <div>Hello & "World"</div>                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

```

## decodeXMLComponent[​](#decodeXMLComponent "Direct link to decodeXMLComponent")


Introduced in: v21\.2\.0


Decodes XML entities in a string to their corresponding characters.


**Syntax**



```
decodeXMLComponent(s)

```

**Arguments**


- `s` — String containing XML entities to decode. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the provided string with XML entities decoded. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT decodeXMLComponent('&lt;tag&gt;Hello &amp; World&lt;/tag&gt;')

```


```
┌─decodeXMLCom⋯;/tag&gt;')─┐
│ <tag>Hello & World</tag> │
└──────────────────────────┘

```

## editDistance[​](#editDistance "Direct link to editDistance")


Introduced in: v23\.9\.0


Calculates the [edit distance](https://en.wikipedia.org/wiki/Edit_distance) between two byte strings.


**Syntax**



```
editDistance(s1, s2)

```

**Aliases**: `levenshteinDistance`


**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the edit distance between the two strings. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT editDistance('clickhouse', 'mouse')

```


```
┌─editDistance('clickhouse', 'mouse')─┐
│                                   6 │
└─────────────────────────────────────┘

```

## editDistanceUTF8[​](#editDistanceUTF8 "Direct link to editDistanceUTF8")


Introduced in: v24\.6\.0


Calculates the [edit distance](https://en.wikipedia.org/wiki/Edit_distance) between two UTF8 strings.


**Syntax**



```
editDistanceUTF8(s1, s2)

```

**Aliases**: `levenshteinDistanceUTF8`


**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the edit distance between the two UTF8 strings. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT editDistanceUTF8('我是谁', '我是我')

```


```
┌─editDistanceUTF8('我是谁', '我是我')──┐
│                                   1 │
└─────────────────────────────────────┘

```

## encodeXMLComponent[​](#encodeXMLComponent "Direct link to encodeXMLComponent")


Introduced in: v21\.1\.0


Escapes characters to place string into XML text node or attribute.


**Syntax**



```
encodeXMLComponent(s)

```

**Arguments**


- `s` — String to escape. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the escaped string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    '<tag>Hello & "World"</tag>' AS original,
    encodeXMLComponent('<tag>Hello & "World"</tag>') AS xml_encoded;

```


```
┌─original───────────────────┬─xml_encoded──────────────────────────────────────────┐
│ <tag>Hello & "World"</tag> │ &lt;tag&gt;Hello &amp; &quot;World&quot;&lt;/tag&gt; │
└────────────────────────────┴──────────────────────────────────────────────────────┘

```

## endsWith[​](#endsWith "Direct link to endsWith")


Introduced in: v1\.1\.0


Checks whether a string ends with the provided suffix.


**Syntax**



```
endsWith(s, suffix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `suffix` — Suffix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` ends with `suffix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT endsWith('ClickHouse', 'House');

```


```
┌─endsWith('Cl⋯', 'House')─┐
│                        1 │
└──────────────────────────┘

```

## endsWithCaseInsensitive[​](#endsWithCaseInsensitive "Direct link to endsWithCaseInsensitive")


Introduced in: v25\.10\.0


Checks whether a string ends with the provided case\-insensitive suffix.


**Syntax**



```
endsWithCaseInsensitive(s, suffix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `suffix` — Case\-insensitive suffix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` ends with case\-insensitive `suffix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT endsWithCaseInsensitive('ClickHouse', 'HOUSE');

```


```
┌─endsWithCaseInsensitive('Cl⋯', 'HOUSE')─┐
│                                       1 │
└─────────────────────────────────────────┘

```

## endsWithCaseInsensitiveUTF8[​](#endsWithCaseInsensitiveUTF8 "Direct link to endsWithCaseInsensitiveUTF8")


Introduced in: v25\.10\.0


Returns whether string `s` ends with case\-insensitive `suffix`.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
endsWithCaseInsensitiveUTF8(s, suffix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `suffix` — Case\-insensitive suffix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` ends with case\-insensitive `suffix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT endsWithCaseInsensitiveUTF8('данных', 'ых');

```


```
┌─endsWithCaseInsensitiveUTF8('данных', 'ых')─┐
│                                           1 │
└─────────────────────────────────────────────┘

```

## endsWithUTF8[​](#endsWithUTF8 "Direct link to endsWithUTF8")


Introduced in: v23\.8\.0


Returns whether string `s` ends with `suffix`.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
endsWithUTF8(s, suffix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `suffix` — Suffix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` ends with `suffix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT endsWithUTF8('данных', 'ых');

```


```
┌─endsWithUTF8('данных', 'ых')─┐
│                            1 │
└──────────────────────────────┘

```

## extractTextFromHTML[​](#extractTextFromHTML "Direct link to extractTextFromHTML")


Introduced in: v21\.3\.0


Extracts text content from HTML or XHTML.


This function removes HTML tags, comments, and script/style elements, leaving only the text content. It handles:


- Removal of all HTML/XML tags
- Removal of comments (`<!-- -->`)
- Removal of script and style elements with their content
- Processing of CDATA sections (copied verbatim)
- Proper whitespace handling and normalization


Note: HTML entities are not decoded and should be processed with a separate function if needed.


**Syntax**



```
extractTextFromHTML(html)

```

**Arguments**


- `html` — String containing HTML content to extract text from. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the extracted text content with normalized whitespace. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT extractTextFromHTML('
<html>
    <head><title>Page Title</title></head>
    <body>
        <p>Hello <b>World</b>!</p>
        <script>alert("test");</script>
        <!-- comment -->
    </body>
</html>
');

```


```
┌─extractTextFromHTML('<html><head>...')─┐
│ Page Title Hello World!                │
└────────────────────────────────────────┘

```

## firstLine[​](#firstLine "Direct link to firstLine")


Introduced in: v23\.7\.0


Returns the first line of a multi\-line string.


**Syntax**



```
firstLine(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the first line of the input string or the whole string if there are no line separators. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT firstLine('foo\\nbar\\nbaz')

```


```
┌─firstLine('foo\nbar\nbaz')─┐
│ foo                        │
└────────────────────────────┘

```

## idnaDecode[​](#idnaDecode "Direct link to idnaDecode")


Introduced in: v24\.1\.0


Returns the Unicode (UTF\-8\) representation (ToUnicode algorithm) of a domain name according to the [Internationalized Domain Names in Applications](https://en.wikipedia.org/wiki/Internationalized_domain_name#Internationalizing_Domain_Names_in_Applications) (IDNA) mechanism.
In case of an error (e.g. because the input is invalid), the input string is returned.
Note that repeated application of [`idnaEncode()`](#idnaEncode) and [`idnaDecode()`](#idnaDecode) does not necessarily return the original string due to case normalization.


**Syntax**



```
idnaDecode(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Unicode (UTF\-8\) representation of the input string according to the IDNA mechanism of the input value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT idnaDecode('xn--strae-oqa.xn--mnchen-3ya.de')

```


```
┌─idnaDecode('xn--strae-oqa.xn--mnchen-3ya.de')─┐
│ straße.münchen.de                             │
└───────────────────────────────────────────────┘

```

## idnaEncode[​](#idnaEncode "Direct link to idnaEncode")


Introduced in: v24\.1\.0


Returns the ASCII representation (ToASCII algorithm) of a domain name according to the [Internationalized Domain Names in Applications](https://en.wikipedia.org/wiki/Internationalized_domain_name#Internationalizing_Domain_Names_in_Applications) (IDNA) mechanism.
The input string must be UTF\-encoded and translatable to an ASCII string, otherwise an exception is thrown.


NoteNo percent decoding or trimming of tabs, spaces or control characters is performed.


**Syntax**



```
idnaEncode(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an ASCII representation of the input string according to the IDNA mechanism of the input value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT idnaEncode('straße.münchen.de')

```


```
┌─idnaEncode('straße.münchen.de')─────┐
│ xn--strae-oqa.xn--mnchen-3ya.de     │
└─────────────────────────────────────┘

```

## initcap[​](#initcap "Direct link to initcap")


Introduced in: v23\.7\.0


Converts the first letter of each word to upper case and the rest to lower case.
Words are sequences of alphanumeric characters separated by non\-alphanumeric characters.


NoteBecause `initcap` converts only the first letter of each word to upper case you may observe unexpected behaviour for words containing apostrophes or capital letters.
This is a known behaviour and there are no plans to fix it currently.


**Syntax**



```
initcap(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `s` with the first letter of each word converted to upper case. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT initcap('building for fast')

```


```
┌─initcap('building for fast')─┐
│ Building For Fast            │
└──────────────────────────────┘

```

**Example of known behavior for words containing apostrophes or capital letters**



```
SELECT initcap('John''s cat won''t eat.');

```


```
┌─initcap('Joh⋯n\'t eat.')─┐
│ John'S Cat Won'T Eat.    │
└──────────────────────────┘

```

## initcapUTF8[​](#initcapUTF8 "Direct link to initcapUTF8")


Introduced in: v23\.7\.0


Like [`initcap`](#initcap), `initcapUTF8` converts the first letter of each word to upper case and the rest to lower case.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


NoteThis function does not detect the language, e.g. for Turkish the result might not be exactly correct (i/İ vs. i/I).
If the length of the UTF\-8 byte sequence is different for upper and lower case of a code point, the result may be incorrect for this code point.


**Syntax**



```
initcapUTF8(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `s` with the first letter of each word converted to upper case. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT initcapUTF8('не тормозит')

```


```
┌─initcapUTF8('не тормозит')─┐
│ Не Тормозит                │
└────────────────────────────┘

```

## isValidASCII[​](#isValidASCII "Direct link to isValidASCII")


Introduced in: v25\.9\.0


Returns 1 if the input String or FixedString contains only ASCII bytes (0x00–0x7F), otherwise 0\. Optimized for the positive case (the input *is* valid ASCII).


**Syntax**



```
isValidASCII(str)

```

**Aliases**: `isASCII`


**Arguments**


- None.


**Returned value**


**Examples**


**isValidASCII**



```
SELECT isValidASCII('hello') AS is_ascii, isValidASCII('你好') AS is_not_ascii

```


## isValidUTF8[​](#isValidUTF8 "Direct link to isValidUTF8")


Introduced in: v20\.1\.0


Checks if the set of bytes constitutes valid UTF\-8\-encoded text.


**Syntax**



```
isValidUTF8(s)

```

**Arguments**


- `s` — The string to check for UTF\-8 encoded validity. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1`, if the set of bytes constitutes valid UTF\-8\-encoded text, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT isValidUTF8('\\xc3\\xb1') AS valid, isValidUTF8('\\xc3\\x28') AS invalid

```


```
┌─valid─┬─invalid─┐
│     1 │       0 │
└───────┴─────────┘

```

## jaroSimilarity[​](#jaroSimilarity "Direct link to jaroSimilarity")


Introduced in: v24\.1\.0


Calculates the [Jaro similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance#Jaro_similarity) between two byte strings.


**Syntax**



```
jaroSimilarity(s1, s2)

```

**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Jaro similarity between the two strings. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT jaroSimilarity('clickhouse', 'click')

```


```
┌─jaroSimilarity('clickhouse', 'click')─┐
│                    0.8333333333333333 │
└───────────────────────────────────────┘

```

## jaroWinklerSimilarity[​](#jaroWinklerSimilarity "Direct link to jaroWinklerSimilarity")


Introduced in: v24\.1\.0


Calculates the [Jaro\-Winkler similarity](https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance) between two byte strings.


**Syntax**



```
jaroWinklerSimilarity(s1, s2)

```

**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Jaro\-Winkler similarity between the two strings. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT jaroWinklerSimilarity('clickhouse', 'click')

```


```
┌─jaroWinklerSimilarity('clickhouse', 'click')─┐
│                           0.8999999999999999 │
└──────────────────────────────────────────────┘

```

## left[​](#left "Direct link to left")


Introduced in: v22\.1\.0


Returns a substring of string `s` with a specified `offset` starting from the left.


**Syntax**



```
left(s, offset)

```

**Arguments**


- `s` — The string to calculate a substring from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `offset` — The number of bytes of the offset. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns:


- For positive `offset`, a substring of `s` with `offset` many bytes, starting from the left of the string.
- For negative `offset`, a substring of `s` with `length(s) - |offset|` bytes, starting from the left of the string.
- An empty string if `length` is `0`.
[`String`](/docs/sql-reference/data-types/string)


**Examples**


**Positive offset**



```
SELECT left('Hello World', 5)

```


```
Hello

```

**Negative offset**



```
SELECT left('Hello World', -6)

```


```
Hello

```

## leftPad[​](#leftPad "Direct link to leftPad")


Introduced in: v21\.8\.0


Pads a string from the left with spaces or with a specified string (multiple times, if needed) until the resulting string reaches the specified `length`.


**Syntax**



```
leftPad(string, length[, pad_string])

```

**Aliases**: `lpad`


**Arguments**


- `string` — Input string that should be padded. [`String`](/docs/sql-reference/data-types/string)
- `length` — The length of the resulting string. If the value is smaller than the input string length, then the input string is shortened to `length` characters. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `pad_string` — Optional. The string to pad the input string with. If not specified, then the input string is padded with spaces. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a left\-padded string of the given length. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT leftPad('abc', 7, '*'), leftPad('def', 7)

```


```
┌─leftPad('abc', 7, '*')─┬─leftPad('def', 7)─┐
│ ****abc                │     def           │
└────────────────────────┴───────────────────┘

```

## leftPadUTF8[​](#leftPadUTF8 "Direct link to leftPadUTF8")


Introduced in: v21\.8\.0


Pads a UTF8 string from the left with spaces or a specified string (multiple times, if needed) until the resulting string reaches the given length.
Unlike [`leftPad`](#leftPad) which measures the string length in bytes, the string length is measured in code points.


**Syntax**



```
leftPadUTF8(string, length[, pad_string])

```

**Arguments**


- `string` — Input string that should be padded. [`String`](/docs/sql-reference/data-types/string)
- `length` — The length of the resulting string. If the value is smaller than the input string length, then the input string is shortened to `length` characters. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `pad_string` — Optional. The string to pad the input string with. If not specified, then the input string is padded with spaces. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a left\-padded string of the given length. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT leftPadUTF8('абвг', 7, '*'), leftPadUTF8('дежз', 7)

```


```
┌─leftPadUTF8('абвг', 7, '*')─┬─leftPadUTF8('дежз', 7)─┐
│ ***абвг                     │    дежз                │
└─────────────────────────────┴────────────────────────┘

```

## leftUTF8[​](#leftUTF8 "Direct link to leftUTF8")


Introduced in: v22\.1\.0


Returns a substring of a UTF\-8\-encoded string `s` with a specified `offset` starting from the left.


**Syntax**



```
leftUTF8(s, offset)

```

**Arguments**


- `s` — The UTF\-8 encoded string to calculate a substring from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `offset` — The number of bytes of the offset. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns:


- For positive `offset`, a substring of `s` with `offset` many bytes, starting from the left of the string.\\n"
- For negative `offset`, a substring of `s` with `length(s) - |offset|` bytes, starting from the left of the string.\\n"
- An empty string if `length` is 0\.
[`String`](/docs/sql-reference/data-types/string)


**Examples**


**Positive offset**



```
SELECT leftUTF8('Привет', 4)

```


```
Прив

```

**Negative offset**



```
SELECT leftUTF8('Привет', -4)

```


```
Пр

```

## lengthUTF8[​](#lengthUTF8 "Direct link to lengthUTF8")


Introduced in: v1\.1\.0


Returns the length of a string in Unicode code points rather than in bytes or characters.
It assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
lengthUTF8(s)

```

**Aliases**: `CHARACTER_LENGTH`, `CHAR_LENGTH`


**Arguments**


- `s` — String containing valid UTF\-8 encoded text. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Length of the string `s` in Unicode code points. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT lengthUTF8('Здравствуй, мир!')

```


```
┌─lengthUTF8('Здравствуй, мир!')─┐
│                             16 │
└────────────────────────────────┘

```

## lower[​](#lower "Direct link to lower")


Introduced in: v1\.1\.0


Converts an ASCII string to lowercase.


**Syntax**



```
lower(s)

```

**Aliases**: `lcase`


**Arguments**


- `s` — A string to convert to lowercase. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a lowercase string from `s`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT lower('CLICKHOUSE')

```


```
┌─lower('CLICKHOUSE')─┐
│ clickhouse          │
└─────────────────────┘

```

## lowerUTF8[​](#lowerUTF8 "Direct link to lowerUTF8")


Introduced in: v1\.1\.0


Converts a string to lowercase, assuming that the string contains valid UTF\-8 encoded text. If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
lowerUTF8(input)

```

**Arguments**


- `input` — Input string to convert to lowercase. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a lowercase string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**first**



```
SELECT lowerUTF8('München') as Lowerutf8;

```


```
münchen

```

## naturalSortKey[​](#naturalSortKey "Direct link to naturalSortKey")


Introduced in: v26\.3\.0


The function is used for natural sorting.


**Syntax**



```
naturalSortKey(s)

```

**Aliases**: `NATURAL_SORT_KEY`


**Arguments**


- `s` — A string to convert to natural sort key. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a natural sort key string from `s`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT s FROM t ORDER BY naturalSortKey(s)

```


```
┌─s───┐
│ a1  │
| a02 │
└─────┘

```

## normalizeUTF8NFC[​](#normalizeUTF8NFC "Direct link to normalizeUTF8NFC")


Introduced in: v21\.11\.0


Normalizes a UTF\-8 string according to the [NFC normalization form](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms).


**Syntax**



```
normalizeUTF8NFC(str)

```

**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the NFC normalized form of the UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
'é' AS original, -- e + combining acute accent (U+0065 + U+0301)
length(original),
normalizeUTF8NFC('é') AS nfc_normalized, -- é (U+00E9)
length(nfc_normalized);

```


```
┌─original─┬─length(original)─┬─nfc_normalized─┬─length(nfc_normalized)─┐
│ é        │                2 │ é              │                      2 │
└──────────┴──────────────────┴────────────────┴────────────────────────┘

```

## normalizeUTF8NFD[​](#normalizeUTF8NFD "Direct link to normalizeUTF8NFD")


Introduced in: v21\.11\.0


Normalizes a UTF\-8 string according to the [NFD normalization form](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms).


**Syntax**



```
normalizeUTF8NFD(str)

```

**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the NFD normalized form of the UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    'é' AS original, -- é (U+00E9)
    length(original),
    normalizeUTF8NFD('é') AS nfd_normalized, -- e + combining acute (U+0065 + U+0301)
    length(nfd_normalized);

```


```
┌─original─┬─length(original)─┬─nfd_normalized─┬─length(nfd_normalized)─┐
│ é        │                2 │ é              │                      3 │
└──────────┴──────────────────┴────────────────┴────────────────────────┘

```

## normalizeUTF8NFKC[​](#normalizeUTF8NFKC "Direct link to normalizeUTF8NFKC")


Introduced in: v21\.11\.0


Normalizes a UTF\-8 string according to the [NFKC normalization form](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms).


**Syntax**



```
normalizeUTF8NFKC(str)

```

**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the NFKC normalized form of the UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    '① ② ③' AS original,                            -- Circled number characters
    normalizeUTF8NFKC('① ② ③') AS nfkc_normalized;  -- Converts to 1 2 3

```


```
┌─original─┬─nfkc_normalized─┐
│ ① ② ③  │ 1 2 3           │
└──────────┴─────────────────┘

```

## normalizeUTF8NFKCCasefold[​](#normalizeUTF8NFKCCasefold "Direct link to normalizeUTF8NFKCCasefold")


Introduced in: v26\.3\.0


Normalizes a UTF\-8 string according to the [NFKC\_Casefold normalization form](https://unicode.org/reports/tr44/#NFKC_Casefold), which applies NFKC normalization and then case folding.
This is useful for case\-insensitive matching of identifiers.


**Syntax**



```
normalizeUTF8NFKCCasefold(str)

```

**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the NFKC\_Casefold normalized form of the UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    'Ä ① Hello' AS original,
    normalizeUTF8NFKCCasefold('Ä ① Hello') AS nfkc_cf_normalized;

```


```
┌─original───┬─nfkc_cf_normalized─┐
│ Ä ① Hello │ ä 1 hello           │
└────────────┴────────────────────┘

```

## normalizeUTF8NFKD[​](#normalizeUTF8NFKD "Direct link to normalizeUTF8NFKD")


Introduced in: v21\.11\.0


Normalizes a UTF\-8 string according to the [NFKD normalization form](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms).


**Syntax**



```
normalizeUTF8NFKD(str)

```

**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the NFKD normalized form of the UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    'H₂O²' AS original,                            -- H + subscript 2 + O + superscript 2
    normalizeUTF8NFKD('H₂O²') AS nfkd_normalized;  -- Converts to H 2 O 2

```


```
┌─original─┬─nfkd_normalized─┐
│ H₂O²     │ H2O2            │
└──────────┴─────────────────┘

```

## punycodeDecode[​](#punycodeDecode "Direct link to punycodeDecode")


Introduced in: v24\.1\.0


Returns the UTF8\-encoded plaintext of a [Punycode](https://en.wikipedia.org/wiki/Punycode)\-encoded string.
If no valid Punycode\-encoded string is given, an exception is thrown.


**Syntax**



```
punycodeDecode(s)

```

**Arguments**


- `s` — Punycode\-encoded string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the plaintext of the input value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT punycodeDecode('Mnchen-3ya')

```


```
┌─punycodeDecode('Mnchen-3ya')─┐
│ München                      │
└──────────────────────────────┘

```

## punycodeEncode[​](#punycodeEncode "Direct link to punycodeEncode")


Introduced in: v24\.1\.0


Returns the [Punycode](https://en.wikipedia.org/wiki/Punycode) representation of a string.
The string must be UTF8\-encoded, otherwise the behavior is undefined.


**Syntax**



```
punycodeEncode(s)

```

**Arguments**


- `s` — Input value. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a Punycode representation of the input value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT punycodeEncode('München')

```


```
┌─punycodeEncode('München')─┐
│ Mnchen-3ya                │
└───────────────────────────┘

```

## regexpExtract[​](#regexpExtract "Direct link to regexpExtract")


Introduced in: v23\.2\.0


Extracts the first string in `haystack` that matches the regexp pattern and corresponds to the regex group index.


**Syntax**



```
regexpExtract(haystack, pattern[, index])

```

**Aliases**: `REGEXP_EXTRACT`


**Arguments**


- `haystack` — String, in which regexp pattern will be matched. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — String, regexp expression. `pattern` may contain multiple regexp groups, `index` indicates which regex group to extract. An index of 0 means matching the entire regular expression. [`const String`](/docs/sql-reference/data-types/string)
- `index` — Optional. An integer number greater or equal 0 with default 1\. It represents which regex group to extract. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a string match [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT
    regexpExtract('100-200', '(\\d+)-(\\d+)', 1),
    regexpExtract('100-200', '(\\d+)-(\\d+)', 2),
    regexpExtract('100-200', '(\\d+)-(\\d+)', 0),
    regexpExtract('100-200', '(\\d+)-(\\d+)');

```


```
┌─regexpExtract('100-200', '(\\d+)-(\\d+)', 1)─┬─regexpExtract('100-200', '(\\d+)-(\\d+)', 2)─┬─regexpExtract('100-200', '(\\d+)-(\\d+)', 0)─┬─regexpExtract('100-200', '(\\d+)-(\\d+)')─┐
│ 100                                          │ 200                                          │ 100-200                                      │ 100                                       │
└──────────────────────────────────────────────┴──────────────────────────────────────────────┴──────────────────────────────────────────────┴───────────────────────────────────────────┘

```

## regexpPosition[​](#regexpPosition "Direct link to regexpPosition")


Introduced in: v26\.5\.0


Returns the byte position (1\-based) of the `occurrence`\-th match of `pattern` in `haystack`, starting the search at byte position `position`.


If `return_option` is 0 (default), the position of the first byte of the match is returned. If 1, the position of the first byte *after* the match is returned.


If `subexpression` is greater than 0, the position of the corresponding capture group is returned instead of the whole match.


Returns 0 if no match is found, or if the requested capture group did not participate in the match.


Provided for compatibility with PostgreSQL's `regexp_instr` (also exposed under that alias). Note that positions are byte\-based, consistent with other ClickHouse regex functions; PostgreSQL's `regexp_instr` is character\-based.


**Syntax**



```
regexpPosition(haystack, pattern[, position[, occurrence[, return_option[, flags[, subexpression]]]]])

```

**Aliases**: `regexpInstr`, `regexp_instr`


**Arguments**


- `haystack` — String to search in. [`String`](/docs/sql-reference/data-types/string)
- `pattern` — Regular expression pattern. [`const String`](/docs/sql-reference/data-types/string)
- `position` — Optional. 1\-based byte position to start the search. Default: 1\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `occurrence` — Optional. Which match to return. Default: 1\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `return_option` — Optional. 0 returns the position of the match start, 1 returns the position right after the match. Default: 0\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `flags` — Optional. Regex flags. Supported: `i` (case\-insensitive), `c` (case\-sensitive), `m`/`n` (multiline anchors), `s` (dot matches newline). Default: empty. [`const String`](/docs/sql-reference/data-types/string)
- `subexpression` — Optional. Index of capture group whose position to return. 0 means whole match. Default: 0\. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns the byte position of the match, or 0 if not found. [`UInt64`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Basic usage**



```
SELECT
    regexpPosition('hello world', 'world'),
    regexpPosition('aXbXcXd', 'X', 1, 2),
    regexpPosition('aXbXcXd', 'X', 1, 2, 1),
    regexpPosition('Hello WORLD', 'world', 1, 1, 0, 'i'),
    regexpPosition('foo123bar456', '([a-z]+)([0-9]+)', 1, 2, 0, '', 2);

```


```
┌─...─┬─...─┬─...─┬─...─┬─...─┐
│   7 │   4 │   5 │   7 │  10 │
└─────┴─────┴─────┴─────┴─────┘

```

## removeDiacriticsUTF8[​](#removeDiacriticsUTF8 "Direct link to removeDiacriticsUTF8")


Introduced in: v26\.3\.0


Removes diacritical marks (accents) from a UTF\-8 string by decomposing characters via NFD,
stripping combining marks (Unicode category Mn), then recomposing via NFC.


**Syntax**



```
removeDiacriticsUTF8(str)

```

**Aliases**: `removeAccentsUTF8`


**Arguments**


- `str` — UTF\-8 encoded input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


UTF\-8 string with diacritics removed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic accent removal**



```
SELECT removeDiacriticsUTF8('café résumé naïve')

```


```
┌─removeDiacriticsUTF8('café résumé naïve')─┐
│ cafe resume naive                          │
└────────────────────────────────────────────┘

```

## repeat[​](#repeat "Direct link to repeat")


Introduced in: v20\.1\.0


Concatenates a string as many times with itself as specified.


**Syntax**



```
repeat(s, n)

```

**Arguments**


- `s` — The string to repeat. [`String`](/docs/sql-reference/data-types/string)
- `n` — The number of times to repeat the string. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


A string containing string `s` repeated `n` times. If `n` is negative, the function returns the empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT repeat('abc', 10)

```


```
┌─repeat('abc', 10)──────────────┐
│ abcabcabcabcabcabcabcabcabcabc │
└────────────────────────────────┘

```

## reverseUTF8[​](#reverseUTF8 "Direct link to reverseUTF8")


Introduced in: v1\.1\.0


Reverses a sequence of Unicode code points in a string.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
reverseUTF8(s)

```

**Arguments**


- `s` — String containing valid UTF\-8 encoded text. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string with the sequence of Unicode code points reversed. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT reverseUTF8('ClickHouse')

```


```
esuoHkcilC

```

## right[​](#right "Direct link to right")


Introduced in: v22\.1\.0


Returns a substring of string `s` with a specified `offset` starting from the right.


**Syntax**



```
right(s, offset)

```

**Arguments**


- `s` — The string to calculate a substring from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `offset` — The number of bytes of the offset. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns:


- For positive `offset`, a substring of `s` with `offset` many bytes, starting from the right of the string.
- For negative `offset`, a substring of `s` with `length(s) - |offset|` bytes, starting from the right of the string.
- An empty string if `length` is `0`.
[`String`](/docs/sql-reference/data-types/string)


**Examples**


**Positive offset**



```
SELECT right('Hello', 3)

```


```
llo

```

**Negative offset**



```
SELECT right('Hello', -3)

```


```
lo

```

## rightPad[​](#rightPad "Direct link to rightPad")


Introduced in: v21\.8\.0


Pads a string from the right with spaces or with a specified string (multiple times, if needed) until the resulting string reaches the specified `length`.


**Syntax**



```
rightPad(string, length[, pad_string])

```

**Aliases**: `rpad`


**Arguments**


- `string` — Input string that should be padded. [`String`](/docs/sql-reference/data-types/string)
- `length` — The length of the resulting string. If the value is smaller than the input string length, then the input string is shortened to `length` characters. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `pad_string` — Optional. The string to pad the input string with. If not specified, then the input string is padded with spaces. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a right\-padded string of the given length. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT rightPad('abc', 7, '*'), rightPad('abc', 7)

```


```
┌─rightPad('abc', 7, '*')─┬─rightPad('abc', 7)─┐
│ abc****                 │ abc                │
└─────────────────────────┴────────────────────┘

```

## rightPadUTF8[​](#rightPadUTF8 "Direct link to rightPadUTF8")


Introduced in: v21\.8\.0


Pads the string from the right with spaces or a specified string (multiple times, if needed) until the resulting string reaches the given length.
Unlike [`rightPad`](#rightPad) which measures the string length in bytes, the string length is measured in code points.


**Syntax**



```
rightPadUTF8(string, length[, pad_string])

```

**Arguments**


- `string` — Input string that should be padded. [`String`](/docs/sql-reference/data-types/string)
- `length` — The length of the resulting string. If the value is smaller than the input string length, then the input string is shortened to `length` characters. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `pad_string` — Optional. The string to pad the input string with. If not specified, then the input string is padded with spaces. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a right\-padded string of the given length. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT rightPadUTF8('абвг', 7, '*'), rightPadUTF8('абвг', 7)

```


```
┌─rightPadUTF8('абвг', 7, '*')─┬─rightPadUTF8('абвг', 7)─┐
│ абвг***                      │ абвг                    │
└──────────────────────────────┴─────────────────────────┘

```

## rightUTF8[​](#rightUTF8 "Direct link to rightUTF8")


Introduced in: v22\.1\.0


Returns a substring of UTF\-8 encoded string `s` with a specified `offset` starting from the right.


**Syntax**



```
rightUTF8(s, offset)

```

**Arguments**


- `s` — The UTF\-8 encoded string to calculate a substring from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring)
- `offset` — The number of bytes of the offset. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns:


- For positive `offset`, a substring of `s` with `offset` many bytes, starting from the right of the string.
- For negative `offset`, a substring of `s` with `length(s) - |offset|` bytes, starting from the right of the string.
- An empty string if `length` is `0`.
[`String`](/docs/sql-reference/data-types/string)


**Examples**


**Positive offset**



```
SELECT rightUTF8('Привет', 4)

```


```
ивет

```

**Negative offset**



```
SELECT rightUTF8('Привет', -4)

```


```
ет

```

## soundex[​](#soundex "Direct link to soundex")


Introduced in: v23\.4\.0


Returns the [Soundex code](https://en.wikipedia.org/wiki/Soundex) of a string.


**Syntax**



```
soundex(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Soundex code of the input string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT soundex('aksel')

```


```
┌─soundex('aksel')─┐
│ A240             │
└──────────────────┘

```

## space[​](#space "Direct link to space")


Introduced in: v23\.5\.0


Concatenates a space () as many times with itself as specified.


**Syntax**



```
space(n)

```

**Arguments**


- `n` — The number of times to repeat the space. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns astring containing a space repeated `n` times. If `n <= 0`, the function returns the empty string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT space(3) AS res, length(res);

```


```
┌─res─┬─length(res)─┐
│     │           3 │
└─────┴─────────────┘

```

## sparseGrams[​](#sparseGrams "Direct link to sparseGrams")


Introduced in: v25\.5\.0


Finds all substrings of a given string that have a length of at least `n`,
where the hashes of the (n\-1\)\-grams at the borders of the substring
are strictly greater than those of any (n\-1\)\-gram inside the substring.
Uses `CRC32` as a hash function.


**Syntax**



```
sparseGrams(s[, min_ngram_length[, max_ngram_length[, min_cutoff_length]]])

```

**Arguments**


- `s` — An input string. [`String`](/docs/sql-reference/data-types/string)
- `min_ngram_length` — Optional. The minimum length of extracted ngram. The default and minimal value is 3\. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `max_ngram_length` — Optional. The maximum length of extracted ngram. The default value is 100\. Should be not less than `min_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `min_cutoff_length` — Optional. If specified, only n\-grams with length greater or equal than `min_cutoff_length` are returned. The default value is the same as `min_ngram_length`. Should be not less than `min_ngram_length` and not greater than `max_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of selected substrings. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT sparseGrams('alice', 3)

```


```
┌─sparseGrams('alice', 3)────────────┐
│ ['ali','lic','lice','ice']         │
└────────────────────────────────────┘

```

## sparseGramsHashes[​](#sparseGramsHashes "Direct link to sparseGramsHashes")


Introduced in: v25\.5\.0


Finds hashes of all substrings of a given string that have a length of at least `n`,
where the hashes of the (n\-1\)\-grams at the borders of the substring
are strictly greater than those of any (n\-1\)\-gram inside the substring.
Uses `CRC32` as a hash function.


**Syntax**



```
sparseGramsHashes(s[, min_ngram_length, max_ngram_length])

```

**Arguments**


- `s` — An input string. [`String`](/docs/sql-reference/data-types/string)
- `min_ngram_length` — Optional. The minimum length of extracted ngram. The default and minimal value is 3\. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `max_ngram_length` — Optional. The maximum length of extracted ngram. The default value is 100\. Should be not less than `min_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `min_cutoff_length` — Optional. If specified, only n\-grams with length greater or equal than `min_cutoff_length` are returned. The default value is the same as `min_ngram_length`. Should be not less than `min_ngram_length` and not greater than `max_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of selected substrings CRC32 hashes. [`Array(UInt32)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT sparseGramsHashes('alice', 3)

```


```
┌─sparseGramsHashes('alice', 3)──────────────────────┐
│ [1481062250,2450405249,4012725991,1918774096]      │
└────────────────────────────────────────────────────┘

```

## sparseGramsHashesUTF8[​](#sparseGramsHashesUTF8 "Direct link to sparseGramsHashesUTF8")


Introduced in: v25\.5\.0


Finds hashes of all substrings of a given UTF\-8 string that have a length of at least `n`, where the hashes of the (n\-1\)\-grams at the borders of the substring are strictly greater than those of any (n\-1\)\-gram inside the substring.
Expects UTF\-8 string, throws an exception in case of invalid UTF\-8 sequence.
Uses `CRC32` as a hash function.


**Syntax**



```
sparseGramsHashesUTF8(s[, min_ngram_length, max_ngram_length])

```

**Arguments**


- `s` — An input string. [`String`](/docs/sql-reference/data-types/string)
- `min_ngram_length` — Optional. The minimum length of extracted ngram. The default and minimal value is 3\. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `max_ngram_length` — Optional. The maximum length of extracted ngram. The default value is 100\. Should be not less than `min_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `min_cutoff_length` — Optional. If specified, only n\-grams with length greater or equal than `min_cutoff_length` are returned. The default value is the same as `min_ngram_length`. Should be not less than `min_ngram_length` and not greater than `max_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of selected UTF\-8 substrings CRC32 hashes. [`Array(UInt32)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT sparseGramsHashesUTF8('алиса', 3)

```


```
┌─sparseGramsHashesUTF8('алиса', 3)─┐
│ [4178533925,3855635300,561830861] │
└───────────────────────────────────┘

```

## sparseGramsUTF8[​](#sparseGramsUTF8 "Direct link to sparseGramsUTF8")


Introduced in: v25\.5\.0


Finds all substrings of a given UTF\-8 string that have a length of at least `n`, where the hashes of the (n\-1\)\-grams at the borders of the substring are strictly greater than those of any (n\-1\)\-gram inside the substring.
Expects a UTF\-8 string, throws an exception in case of an invalid UTF\-8 sequence.
Uses `CRC32` as a hash function.


**Syntax**



```
sparseGramsUTF8(s[, min_ngram_length[, max_ngram_length[, min_cutoff_length]]])

```

**Arguments**


- `s` — An input string. [`String`](/docs/sql-reference/data-types/string)
- `min_ngram_length` — Optional. The minimum length of extracted ngram. The default and minimal value is 3\. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `max_ngram_length` — Optional. The maximum length of extracted ngram. The default value is 100\. Should be not less than `min_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)
- `min_cutoff_length` — Optional. If specified, only n\-grams with length greater or equal than `min_cutoff_length` are returned. The default value is the same as `min_ngram_length`. Should be not less than `min_ngram_length` and not greater than `max_ngram_length`. [`UInt*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns an array of selected UTF\-8 substrings. [`Array(String)`](/docs/sql-reference/data-types/array)


**Examples**


**Usage example**



```
SELECT sparseGramsUTF8('алиса', 3)

```


```
┌─sparseGramsUTF8('алиса', 3)─┐
│ ['али','лис','иса']         │
└─────────────────────────────┘

```

## startsWith[​](#startsWith "Direct link to startsWith")


Introduced in: v1\.1\.0


Checks whether a string begins with the provided string.


**Syntax**



```
startsWith(s, prefix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `prefix` — Prefix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` starts with `prefix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT startsWith('ClickHouse', 'Click');

```


```
┌─startsWith('⋯', 'Click')─┐
│                        1 │
└──────────────────────────┘

```

## startsWithCaseInsensitive[​](#startsWithCaseInsensitive "Direct link to startsWithCaseInsensitive")


Introduced in: v25\.10\.0


Checks whether a string begins with the provided case\-insensitive string.


**Syntax**



```
startsWithCaseInsensitive(s, prefix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `prefix` — Case\-insensitive prefix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` starts with case\-insensitive `prefix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT startsWithCaseInsensitive('ClickHouse', 'CLICK');

```


```
┌─startsWithCaseInsensitive('⋯', 'CLICK')─┐
│                                       1 │
└─────────────────────────────────────────┘

```

## startsWithCaseInsensitiveUTF8[​](#startsWithCaseInsensitiveUTF8 "Direct link to startsWithCaseInsensitiveUTF8")


Introduced in: v25\.10\.0


Checks if a string starts with the provided case\-insensitive prefix.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
startsWithCaseInsensitiveUTF8(s, prefix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `prefix` — Case\-insensitive prefix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` starts with case\-insensitive `prefix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT startsWithCaseInsensitiveUTF8('приставка', 'при')

```


```
┌─startsWithUT⋯ка', 'при')─┐
│                        1 │
└──────────────────────────┘

```

## startsWithUTF8[​](#startsWithUTF8 "Direct link to startsWithUTF8")


Introduced in: v23\.8\.0


Checks if a string starts with the provided prefix.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
startsWithUTF8(s, prefix)

```

**Arguments**


- `s` — String to check. [`String`](/docs/sql-reference/data-types/string)
- `prefix` — Prefix to check for. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns `1` if `s` starts with `prefix`, otherwise `0`. [`UInt8`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT startsWithUTF8('приставка', 'при')

```


```
┌─startsWithUT⋯ка', 'при')─┐
│                        1 │
└──────────────────────────┘

```

## stringBytesEntropy[​](#stringBytesEntropy "Direct link to stringBytesEntropy")


Introduced in: v25\.6\.0


Calculates Shannon's entropy of byte distribution in a string.


**Syntax**



```
stringBytesEntropy(s)

```

**Arguments**


- `s` — The string to analyze. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns Shannon's entropy of byte distribution in the string. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT stringBytesEntropy('Hello, world!')

```


```
┌─stringBytesEntropy('Hello, world!')─┐
│                         3.07049960  │
└─────────────────────────────────────┘

```

## stringBytesUniq[​](#stringBytesUniq "Direct link to stringBytesUniq")


Introduced in: v25\.6\.0


Counts the number of distinct bytes in a string.


**Syntax**



```
stringBytesUniq(s)

```

**Arguments**


- `s` — The string to analyze. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the number of distinct bytes in the string. [`UInt16`](/docs/sql-reference/data-types/int-uint)


**Examples**


**Usage example**



```
SELECT stringBytesUniq('Hello')

```


```
┌─stringBytesUniq('Hello')─┐
│                        4 │
└──────────────────────────┘

```

## stringJaccardIndex[​](#stringJaccardIndex "Direct link to stringJaccardIndex")


Introduced in: v23\.11\.0


Calculates the [Jaccard similarity index](https://en.wikipedia.org/wiki/Jaccard_index) between two byte strings.


**Syntax**



```
stringJaccardIndex(s1, s2)

```

**Arguments**


- `s1` — First input string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Jaccard similarity index between the two strings. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT stringJaccardIndex('clickhouse', 'mouse')

```


```
┌─stringJaccardIndex('clickhouse', 'mouse')─┐
│                                       0.4 │
└───────────────────────────────────────────┘

```

## stringJaccardIndexUTF8[​](#stringJaccardIndexUTF8 "Direct link to stringJaccardIndexUTF8")


Introduced in: v23\.11\.0


Like [`stringJaccardIndex`](#stringJaccardIndex) but for UTF8\-encoded strings.


**Syntax**



```
stringJaccardIndexUTF8(s1, s2)

```

**Arguments**


- `s1` — First input UTF8 string. [`String`](/docs/sql-reference/data-types/string)
- `s2` — Second input UTF8 string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the Jaccard similarity index between the two UTF8 strings. [`Float64`](/docs/sql-reference/data-types/float)


**Examples**


**Usage example**



```
SELECT stringJaccardIndexUTF8('我爱你', '我也爱你')

```


```
┌─stringJaccardIndexUTF8('我爱你', '我也爱你')─┐
│                                       0.75 │
└─────────────────────────────────────────────┘

```

## substring[​](#substring "Direct link to substring")


Introduced in: v1\.1\.0


Returns the substring of a string `s` which starts at the specified byte index `offset`.
Byte counting starts from 1 with the following logic:


- If `offset` is `0`, an empty string is returned.
- If `offset` is negative, the substring starts `offset` characters from the end of the string, rather than from the beginning.


An optional argument `length` specifies the maximum number of bytes the returned substring may have.


**Syntax**



```
substring(s, offset[, length])

```

**Aliases**: `byteSlice`, `mid`, `substr`


**Arguments**


- `s` — The string to calculate a substring from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Enum`](/docs/sql-reference/data-types/enum)
- `offset` — The starting position of the substring in `s`. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)
- `length` — Optional. The maximum length of the substring. [`(U)Int*`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a substring of `s` with `length` many bytes, starting at index `offset`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Basic usage**



```
SELECT 'database' AS db, substr(db, 5), substr(db, 5, 1)

```


```
┌─db───────┬─substring('database', 5)─┬─substring('database', 5, 1)─┐
│ database │ base                     │ b                           │
└──────────┴──────────────────────────┴─────────────────────────────┘

```

## substringIndex[​](#substringIndex "Direct link to substringIndex")


Introduced in: v23\.7\.0


Returns the substring of `s` before `count` occurrences of the delimiter `delim`, as in Spark or MySQL.


**Syntax**



```
substringIndex(s, delim, count)

```

**Aliases**: `SUBSTRING_INDEX`


**Arguments**


- `s` — The string to extract substring from. [`String`](/docs/sql-reference/data-types/string)
- `delim` — The character to split. [`String`](/docs/sql-reference/data-types/string)
- `count` — The number of occurrences of the delimiter to count before extracting the substring. If count is positive, everything to the left of the final delimiter (counting from the left) is returned. If count is negative, everything to the right of the final delimiter (counting from the right) is returned. [`UInt`](/docs/sql-reference/data-types/int-uint) or [`Int`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a substring of `s` before `count` occurrences of `delim`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT substringIndex('www.clickhouse.com', '.', 2)

```


```
┌─substringIndex('www.clickhouse.com', '.', 2)─┐
│ www.clickhouse                               │
└──────────────────────────────────────────────┘

```

## substringIndexUTF8[​](#substringIndexUTF8 "Direct link to substringIndexUTF8")


Introduced in: v23\.7\.0


Returns the substring of `s` before `count` occurrences of the delimiter `delim`, specifically for Unicode code points.
Assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
substringIndexUTF8(s, delim, count)

```

**Arguments**


- `s` — The string to extract substring from. [`String`](/docs/sql-reference/data-types/string)
- `delim` — The character to split. [`String`](/docs/sql-reference/data-types/string)
- `count` — The number of occurrences of the delimiter to count before extracting the substring. If count is positive, everything to the left of the final delimiter (counting from the left) is returned. If count is negative, everything to the right of the final delimiter (counting from the right) is returned. [`UInt`](/docs/sql-reference/data-types/int-uint) or [`Int`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a substring of `s` before `count` occurrences of `delim`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**UTF8 example**



```
SELECT substringIndexUTF8('www.straßen-in-europa.de', '.', 2)

```


```
www.straßen-in-europa

```

## substringUTF8[​](#substringUTF8 "Direct link to substringUTF8")


Introduced in: v1\.1\.0


Returns the substring of a string `s` which starts at the specified code point index `offset`.
Code point counting starts from `1` with the following logic:


- If `offset` is `0`, an empty string is returned.
- If `offset` is negative, the substring starts `offset` code points from the end of the string, rather than from the beginning.


An optional argument `length` specifies the maximum number of code points the returned substring may have.


NoteThis function assumes that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


**Syntax**



```
substringUTF8(s, offset[, length])

```

**Arguments**


- `s` — The string to calculate a substring from. [`String`](/docs/sql-reference/data-types/string) or [`FixedString`](/docs/sql-reference/data-types/fixedstring) or [`Enum`](/docs/sql-reference/data-types/enum)
- `offset` — The starting position of the substring in `s`. [`Int`](/docs/sql-reference/data-types/int-uint) or [`UInt`](/docs/sql-reference/data-types/int-uint)
- `length` — The maximum length of the substring. Optional. [`Int`](/docs/sql-reference/data-types/int-uint) or [`UInt`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a substring of `s` with `length` many code points, starting at code point index `offset`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT 'Täglich grüßt das Murmeltier.' AS str, substringUTF8(str, 9), substringUTF8(str, 9, 5)

```


```
Täglich grüßt das Murmeltier.    grüßt das Murmeltier.    grüßt

```

## toValidUTF8[​](#toValidUTF8 "Direct link to toValidUTF8")


Introduced in: v20\.1\.0


Converts a string to valid UTF\-8 encoding by replacing any invalid UTF\-8 characters with the replacement character `�` (U\+FFFD).
When multiple consecutive invalid characters are found, they are collapsed into a single replacement character.


**Syntax**



```
toValidUTF8(s)

```

**Arguments**


- `s` — Any set of bytes represented as the String data type object. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a valid UTF\-8 string. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT toValidUTF8('\\x61\\xF0\\x80\\x80\\x80b')

```


```
c
┌─toValidUTF8('a����b')─┐
│ a�b                   │
└───────────────────────┘

```

## trimBoth[​](#trimBoth "Direct link to trimBoth")


Introduced in: v20\.1\.0


Removes the specified characters from the start and end of a string.
By default, removes common whitespace (ASCII) characters.


**Syntax**



```
trimBoth(s[, trim_characters])

```

**Aliases**: `trim`


**Arguments**


- `s` — String to trim. [`String`](/docs/sql-reference/data-types/string)
- `trim_characters` — Optional. Characters to trim. If not specified, common whitespace characters are removed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the string with specified characters trimmed from both ends. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT trimBoth('$$ClickHouse$$', '$')

```


```
┌─trimBoth('$$⋯se$$', '$')─┐
│ ClickHouse               │
└──────────────────────────┘

```

## trimLeft[​](#trimLeft "Direct link to trimLeft")


Introduced in: v20\.1\.0


Removes the specified characters from the start of a string.
By default, removes common whitespace (ASCII) characters.


**Syntax**



```
trimLeft(input[, trim_characters])

```

**Aliases**: `ltrim`


**Arguments**


- `input` — String to trim. [`String`](/docs/sql-reference/data-types/string)
- `trim_characters` — Optional. Characters to trim. If not specified, common whitespace characters are removed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the string with specified characters trimmed from the left. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT trimLeft('ClickHouse', 'Click');

```


```
┌─trimLeft('Cl⋯', 'Click')─┐
│ House                    │
└──────────────────────────┘

```

## trimRight[​](#trimRight "Direct link to trimRight")


Introduced in: v20\.1\.0


Removes the specified characters from the end of a string.
By default, removes common whitespace (ASCII) characters.


**Syntax**



```
trimRight(s[, trim_characters])

```

**Aliases**: `rtrim`


**Arguments**


- `s` — String to trim. [`String`](/docs/sql-reference/data-types/string)
- `trim_characters` — Optional characters to trim. If not specified, common whitespace characters are removed. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the string with specified characters trimmed from the right. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT trimRight('ClickHouse','House');

```


```
┌─trimRight('C⋯', 'House')─┐
│ Click                    │
└──────────────────────────┘

```

## tryBase32Decode[​](#tryBase32Decode "Direct link to tryBase32Decode")


Introduced in: v25\.6\.0


Accepts a string and decodes it using [Base32](https://datatracker.ietf.org/doc/html/rfc4648#section-6) encoding scheme.


**Syntax**



```
tryBase32Decode(encoded)

```

**Arguments**


- `encoded` — String column or constant to decode. If the string is not valid Base32\-encoded, returns an empty string in case of error. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT tryBase32Decode('IVXGG33EMVSA====');

```


```
┌─tryBase32Decode('IVXGG33EMVSA====')─┐
│ Encoded                             │
└─────────────────────────────────────┘

```

## tryBase58Decode[​](#tryBase58Decode "Direct link to tryBase58Decode")


Introduced in: v22\.10\.0


Like [`base58Decode`](#base58Decode), but returns an empty string in case of error.


**Syntax**



```
tryBase58Decode(encoded[, expected_size])

```

**Arguments**


- `encoded` — String column or constant. If the string is not valid Base58\-encoded, returns an empty string in case of error. [`String`](/docs/sql-reference/data-types/string)
- `expected_size` — Optional. Expected decoded size in bytes. When 32 or 64, an optimized decoder is used; for other values, the generic decoder is used. [`UInt8, UInt16, UInt32, or UInt64`](/docs/sql-reference/data-types/int-uint)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT tryBase58Decode('3dc8KtHrwM') AS res, tryBase58Decode('invalid') AS res_invalid;

```


```
┌─res─────┬─res_invalid─┐
│ Encoded │             │
└─────────┴─────────────┘

```

## tryBase64Decode[​](#tryBase64Decode "Direct link to tryBase64Decode")


Introduced in: v18\.16\.0


Like [`base64Decode`](#base64Decode), but returns an empty string in case of error.


**Syntax**



```
tryBase64Decode(encoded)

```

**Arguments**


- `encoded` — String column or constant to decode. If the string is not valid Base64\-encoded, returns an empty string in case of error. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT tryBase64Decode('Y2xpY2tob3VzZQ==')

```


```
┌─tryBase64Decode('Y2xpY2tob3VzZQ==')─┐
│ clickhouse                          │
└─────────────────────────────────────┘

```

## tryBase64URLDecode[​](#tryBase64URLDecode "Direct link to tryBase64URLDecode")


Introduced in: v18\.16\.0


Like [`base64URLDecode`](#base64URLDecode), but returns an empty string in case of error.


**Syntax**



```
tryBase64URLDecode(encoded)

```

**Arguments**


- `encoded` — String column or constant to decode. If the string is not valid Base64\-encoded, returns an empty string in case of error. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns a string containing the decoded value of the argument. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT tryBase64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')

```


```
┌─tryBase64URLDecode('aHR0cHM6Ly9jbGlja2hvdXNlLmNvbQ')─┐
│ https://clickhouse.com                               │
└──────────────────────────────────────────────────────┘

```

## tryIdnaEncode[​](#tryIdnaEncode "Direct link to tryIdnaEncode")


Introduced in: v24\.1\.0


Returns the Unicode (UTF\-8\) representation (ToUnicode algorithm) of a domain name according to the [Internationalized Domain Names in Applications](https://en.wikipedia.org/wiki/Internationalized_domain_name#Internationalizing_Domain_Names_in_Applications) (IDNA) mechanism.
In case of an error it returns an empty string instead of throwing an exception.


**Syntax**



```
tryIdnaEncode(s)

```

**Arguments**


- `s` — Input string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an ASCII representation of the input string according to the IDNA mechanism of the input value, or empty string if input is invalid. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT tryIdnaEncode('straße.münchen.de')

```


```
┌─tryIdnaEncode('straße.münchen.de')──┐
│ xn--strae-oqa.xn--mnchen-3ya.de     │
└─────────────────────────────────────┘

```

## tryPunycodeDecode[​](#tryPunycodeDecode "Direct link to tryPunycodeDecode")


Introduced in: v24\.1\.0


Like `punycodeDecode` but returns an empty string if no valid Punycode\-encoded string is given.


**Syntax**



```
tryPunycodeDecode(s)

```

**Arguments**


- `s` — Punycode\-encoded string. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns the plaintext of the input value, or empty string if input is invalid. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT tryPunycodeDecode('Mnchen-3ya')

```


```
┌─tryPunycodeDecode('Mnchen-3ya')─┐
│ München                         │
└─────────────────────────────────┘

```

## upper[​](#upper "Direct link to upper")


Introduced in: v1\.1\.0


Converts the ASCII Latin symbols in a string to uppercase.


**Syntax**



```
upper(s)

```

**Aliases**: `ucase`


**Arguments**


- `s` — The string to convert to uppercase. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


Returns an uppercase string from `s`. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT upper('clickhouse')

```


```
┌─upper('clickhouse')─┐
│ CLICKHOUSE          │
└─────────────────────┘

```

## upperUTF8[​](#upperUTF8 "Direct link to upperUTF8")


Introduced in: v1\.1\.0


Converts a string to uppercase, assuming that the string contains valid UTF\-8 encoded text.
If this assumption is violated, no exception is thrown and the result is undefined.


NoteThis function doesn't detect the language, e.g. for Turkish the result might not be exactly correct (i/İ vs. i/I).
If the length of the UTF\-8 byte sequence is different for upper and lower case of a code point (such as `ẞ` and `ß`), the result may be incorrect for that code point.


**Syntax**



```
upperUTF8(s)

```

**Arguments**


- `s` — A string type. [`String`](/docs/sql-reference/data-types/string)


**Returned value**


A String data type value. [`String`](/docs/sql-reference/data-types/string)


**Examples**


**Usage example**



```
SELECT upperUTF8('München') AS Upperutf8

```


```
┌─Upperutf8─┐
│ MÜNCHEN   │
└───────────┘

```
[PreviousString splitting](/docs/sql-reference/functions/splitting-merging-functions)[NextString replacement](/docs/sql-reference/functions/string-replace-functions)- [CRC32](#CRC32)- [CRC32IEEE](#CRC32IEEE)- [CRC64](#CRC64)- [appendTrailingCharIfAbsent](#appendTrailingCharIfAbsent)- [ascii](#ascii)- [base32Decode](#base32Decode)- [base32Encode](#base32Encode)- [base58Decode](#base58Decode)- [base58Encode](#base58Encode)- [base64Decode](#base64Decode)- [base64Encode](#base64Encode)- [base64URLDecode](#base64URLDecode)- [base64URLEncode](#base64URLEncode)- [basename](#basename)- [byteHammingDistance](#byteHammingDistance)- [caseFoldUTF8](#caseFoldUTF8)- [compareSubstrings](#compareSubstrings)- [concat](#concat)- [concatAssumeInjective](#concatAssumeInjective)- [concatWithSeparator](#concatWithSeparator)- [concatWithSeparatorAssumeInjective](#concatWithSeparatorAssumeInjective)- [conv](#conv)- [convertCharset](#convertCharset)- [damerauLevenshteinDistance](#damerauLevenshteinDistance)- [decodeHTMLComponent](#decodeHTMLComponent)- [decodeXMLComponent](#decodeXMLComponent)- [editDistance](#editDistance)- [editDistanceUTF8](#editDistanceUTF8)- [encodeXMLComponent](#encodeXMLComponent)- [endsWith](#endsWith)- [endsWithCaseInsensitive](#endsWithCaseInsensitive)- [endsWithCaseInsensitiveUTF8](#endsWithCaseInsensitiveUTF8)- [endsWithUTF8](#endsWithUTF8)- [extractTextFromHTML](#extractTextFromHTML)- [firstLine](#firstLine)- [idnaDecode](#idnaDecode)- [idnaEncode](#idnaEncode)- [initcap](#initcap)- [initcapUTF8](#initcapUTF8)- [isValidASCII](#isValidASCII)- [isValidUTF8](#isValidUTF8)- [jaroSimilarity](#jaroSimilarity)- [jaroWinklerSimilarity](#jaroWinklerSimilarity)- [left](#left)- [leftPad](#leftPad)- [leftPadUTF8](#leftPadUTF8)- [leftUTF8](#leftUTF8)- [lengthUTF8](#lengthUTF8)- [lower](#lower)- [lowerUTF8](#lowerUTF8)- [naturalSortKey](#naturalSortKey)- [normalizeUTF8NFC](#normalizeUTF8NFC)- [normalizeUTF8NFD](#normalizeUTF8NFD)- [normalizeUTF8NFKC](#normalizeUTF8NFKC)- [normalizeUTF8NFKCCasefold](#normalizeUTF8NFKCCasefold)- [normalizeUTF8NFKD](#normalizeUTF8NFKD)- [punycodeDecode](#punycodeDecode)- [punycodeEncode](#punycodeEncode)- [regexpExtract](#regexpExtract)- [regexpPosition](#regexpPosition)- [removeDiacriticsUTF8](#removeDiacriticsUTF8)- [repeat](#repeat)- [reverseUTF8](#reverseUTF8)- [right](#right)- [rightPad](#rightPad)- [rightPadUTF8](#rightPadUTF8)- [rightUTF8](#rightUTF8)- [soundex](#soundex)- [space](#space)- [sparseGrams](#sparseGrams)- [sparseGramsHashes](#sparseGramsHashes)- [sparseGramsHashesUTF8](#sparseGramsHashesUTF8)- [sparseGramsUTF8](#sparseGramsUTF8)- [startsWith](#startsWith)- [startsWithCaseInsensitive](#startsWithCaseInsensitive)- [startsWithCaseInsensitiveUTF8](#startsWithCaseInsensitiveUTF8)- [startsWithUTF8](#startsWithUTF8)- [stringBytesEntropy](#stringBytesEntropy)- [stringBytesUniq](#stringBytesUniq)- [stringJaccardIndex](#stringJaccardIndex)- [stringJaccardIndexUTF8](#stringJaccardIndexUTF8)- [substring](#substring)- [substringIndex](#substringIndex)- [substringIndexUTF8](#substringIndexUTF8)- [substringUTF8](#substringUTF8)- [toValidUTF8](#toValidUTF8)- [trimBoth](#trimBoth)- [trimLeft](#trimLeft)- [trimRight](#trimRight)- [tryBase32Decode](#tryBase32Decode)- [tryBase58Decode](#tryBase58Decode)- [tryBase64Decode](#tryBase64Decode)- [tryBase64URLDecode](#tryBase64URLDecode)- [tryIdnaEncode](#tryIdnaEncode)- [tryPunycodeDecode](#tryPunycodeDecode)- [upper](#upper)- [upperUTF8](#upperUTF8)
Was this page helpful?
