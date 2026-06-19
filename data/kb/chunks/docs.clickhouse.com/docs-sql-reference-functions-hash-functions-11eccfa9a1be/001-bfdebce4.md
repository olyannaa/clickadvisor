---
source: docs.clickhouse.com
url: https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/hash-functions.md)#
topic: hash-functions-clickhouse-docs
ch_version_introduced: '1.0'
last_updated: '2026-06-12'
chunk_index: 1
total_chunks_in_doc: 25
---

# Hash Functions \| ClickHouse Docs

- - [Functions](/docs/sql-reference/functions)- [Regular functions](/docs/sql-reference/functions/regular-functions)- Hash
[Edit this page](https://github.com/ClickHouse/ClickHouse/tree/master/docs/en/sql-reference/functions/hash-functions.md)# Hash Functions

Hash functions can be used for the deterministic pseudo\-random shuffling of elements.

Simhash is a hash function, which returns close hash values for close (similar) arguments.

Most hash functions accept any number of arguments of any types.

NoteHash of NULL is NULL. To get a non\-NULL hash of a Nullable column, wrap it in a tuple:
```
SELECT cityHash64(tuple(NULL))

```

NoteTo calculate hash of the whole contents of a table, use `sum(cityHash64(tuple(*)))` (or other hash function). `tuple` ensures that rows with NULL values are not skipped. `sum` ensures that the order of rows doesn't matter.

## BLAKE3[​](#BLAKE3 "Direct link to BLAKE3")

Introduced in: v22\.10\.0

Calculates BLAKE3 hash string and returns the resulting set of bytes as FixedString.
This cryptographic hash\-function is integrated into ClickHouse with BLAKE3 Rust library.
The function is rather fast and shows approximately two times faster performance compared to SHA\-2, while generating hashes of the same length as SHA\-256\.
It returns a BLAKE3 hash as a byte array with type FixedString(32\).

**Syntax**

```
BLAKE3(message)

```

**Arguments**

- `message` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns the 32\-byte BLAKE3 hash of the input string as a fixed\-length string. [`FixedString(32)`](/docs/sql-reference/data-types/fixedstring)

**Examples**

**hash**

```
SELECT hex(BLAKE3('ABC'))

```

```
┌─hex(BLAKE3('ABC'))───────────────────────────────────────────────┐
│ D1717274597CF0289694F75D96D444B992A096F1AFD8E7BBFA6EBB1D360FEDFC │
└──────────────────────────────────────────────────────────────────┘

```

## MD4[​](#MD4 "Direct link to MD4")

Introduced in: v21\.11\.0

Calculates the MD4 hash of the given string.

**Syntax**

```
MD4(s)

```

**Arguments**

- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns the MD4 hash of the given input string as a fixed\-length string. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)

**Examples**

**Usage example**

```
SELECT HEX(MD4('abc'));

```

```
┌─hex(MD4('abc'))──────────────────┐
│ A448017AAF21D8525FC10AE87AA6729D │
└──────────────────────────────────┘

```

## MD5[​](#MD5 "Direct link to MD5")

Introduced in: v1\.1\.0

Calculates the MD5 hash of the given string.

**Syntax**

```
MD5(s)

```

**Arguments**

- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)

**Returned value**

Returns the MD5 hash of the given input string as a fixed\-length string. [`FixedString(16)`](/docs/sql-reference/data-types/fixedstring)

**Examples**

**Usage example**

```
SELECT HEX(MD5('abc'));

```

```
┌─hex(MD5('abc'))──────────────────┐
│ 900150983CD24FB0D6963F7D28E17F72 │
└──────────────────────────────────┘

```

## RIPEMD160[​](#RIPEMD160 "Direct link to RIPEMD160")

Introduced in: v24\.10\.0

Calculates the RIPEMD\-160 hash of the given string.

**Syntax**

```
RIPEMD160(s)

```

**Arguments**

- `s` — The input string to hash. [`String`](/docs/sql-reference/data-types/string)

**Returned value**
